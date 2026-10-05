#!/usr/bin/env python
"""Export a lab's grades for the WHOLE class to Excel: private/grades/<lab>.xlsx

Merges the class list (private/roster.csv, 21 students) with the collected results
(private/grades/<lab>.csv from scripts/collect_lab.py). Students without a submission get 0.
Grades are Excel formulas, so correcting "Geçen test" or "Geç gün" by hand updates the grade.

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/export_grades.py lab01 [--points 10]
"""
import argparse
import csv
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ROOT = Path(__file__).resolve().parent.parent
FONT = "Arial"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lab")
    ap.add_argument("--points", type=float, default=10, help="maximum grade of the lab (Lab 1: 10, from Lab 2 on: 100)")
    a = ap.parse_args()

    roster = list(csv.DictReader((ROOT / "private" / "roster.csv").open(encoding="utf-8")))
    src = ROOT / "private" / "grades" / f"{a.lab}.csv"
    results = {r["student_id"].strip(): r for r in csv.DictReader(src.open(encoding="utf-8"))}
    # match by GitHub username too, in case a README had no student ID
    by_github = {r["github"].lower(): r for r in results.values()}

    wb = Workbook()
    ws = wb.active
    ws.title = a.lab.replace("lab", "Lab ")
    collected = datetime.fromtimestamp(src.stat().st_mtime).strftime("%d.%m.%Y %H:%M")

    ws["A1"] = f"Discrete Mathematics (YMT211) · {ws.title} notları"
    ws["A1"].font = Font(name=FONT, bold=True, size=13)
    ws["A2"] = (f"Kaynak: collect_lab.py ({collected}), resmi testlerle. "
                f"Not = {a.points:g} × geçen/toplam × (1 − 0,1 × geç gün). Teslim olmayanlar 0.")
    ws["A2"].font = Font(name=FONT, italic=True, size=9, color="666666")

    headers = ["#", "Öğrenci No", "Ad Soyad", "GitHub", "Durum", "Geçen test", "Toplam test",
               "Geç gün", f"Not (/{a.points:g})", "Son push", "Açıklama"]
    hr = 4
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(row=hr, column=c, value=h)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="15161D")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    thin = Side(style="thin", color="D9D6CC")
    first = hr + 1
    for i, s in enumerate(roster):
        r = first + i
        res = results.get(s["student_id"]) or by_github.get((s.get("github_lab01") or "").lower())
        total_tests = int(res["total"]) if res and res["total"] not in ("", "0") else 21
        if not res:
            status, passed, late, pushed, note = "Teslim yok", 0, 0, "", "Depo oluşturulmadı / paylaşılmadı"
        else:
            passed, late, pushed = int(res["passed"] or 0), int(res["late_days"] or 0), res["pushed_at"]
            status = "Teslim edildi" if passed else "Kod push edilmedi"
            note = res["note"] or ("Yalnızca README güncellenmiş" if not passed else "")
        values = [i + 1, int(s["student_id"]), f"{s['first_name']} {s['last_name']}",
                  res["github"] if res else (s.get("github_lab01") or ""), status, passed, total_tests, late]
        for c, v in enumerate(values, start=1):
            ws.cell(row=r, column=c, value=v)
        ws.cell(row=r, column=9, value=f"=IF(G{r}>0,ROUND({a.points:g}*F{r}/G{r}*MAX(0,1-0.1*H{r}),2),0)")
        ws.cell(row=r, column=10, value=pushed)
        ws.cell(row=r, column=11, value=note)
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = Font(name=FONT, size=10, color="0000FF" if c in (6, 7, 8) else "000000")
            cell.border = Border(bottom=thin)
            cell.alignment = Alignment(horizontal="center" if c in (1, 2, 6, 7, 8, 9) else "left", vertical="center")
        ws.cell(row=r, column=9).number_format = "0.00"
    last = first + len(roster) - 1

    # summary
    sr = last + 2
    rows = [
        ("Öğrenci sayısı", f"=COUNTA(B{first}:B{last})"),
        ("Kodu teslim eden", f'=COUNTIF(E{first}:E{last},"Teslim edildi")'),
        ("Tam puan alan", f"=COUNTIF(I{first}:I{last},{a.points:g})"),
        ("Sınıf ortalaması", f"=ROUND(AVERAGE(I{first}:I{last}),2)"),
        ("Teslim edenlerin ortalaması", f'=IFERROR(ROUND(AVERAGEIF(E{first}:E{last},"Teslim edildi",I{first}:I{last}),2),0)'),
    ]
    for k, (label, formula) in enumerate(rows):
        ws.cell(row=sr + k, column=8, value=label).font = Font(name=FONT, bold=True, size=10)
        ws.cell(row=sr + k, column=8).alignment = Alignment(horizontal="right")
        c = ws.cell(row=sr + k, column=9, value=formula)
        c.font = Font(name=FONT, bold=True, size=10)
        c.alignment = Alignment(horizontal="center")

    # highlight zero grades and status
    ws.conditional_formatting.add(f"I{first}:I{last}", CellIsRule(operator="equal", formula=["0"], fill=PatternFill("solid", fgColor="FBE3E3")))
    ws.conditional_formatting.add(f"I{first}:I{last}", CellIsRule(operator="equal", formula=[f"{a.points:g}"], fill=PatternFill("solid", fgColor="DCF3EA")))
    ws["F4"].comment = Comment("Mavi sütunlar elle düzeltilebilir girdilerdir; Not sütunu formülle güncellenir.", "Discrete Math")

    widths = [5, 12, 26, 20, 18, 11, 11, 9, 11, 17, 38]
    for c, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=hr, column=c).column_letter].width = w
    ws.row_dimensions[hr].height = 30
    ws.freeze_panes = ws.cell(row=first, column=4)
    ws.auto_filter.ref = f"A{hr}:K{last}"
    ws.merge_cells("A1:K1")
    ws.merge_cells("A2:K2")

    wb.calculation.fullCalcOnLoad = True   # Excel computes every formula when the file is opened
    out = ROOT / "private" / "grades" / f"{a.lab}.xlsx"
    wb.save(out)
    print(f"✓ {out.relative_to(ROOT)}  ({len(roster)} students)")


if __name__ == "__main__":
    main()
