#!/usr/bin/env python
"""Collect a Classroom 50 lab's autograded scores into private/grades/<lab>.csv (same format as collect_lab.py).

Classroom 50 grades every push and publishes the result as a GitHub Release on the student's
repository (tag  submit/<UTC time>-<sha>, body  "classroom50 autograde: X/Y"). This script:
  1. reads the classroom roster (username → name, student number) from the classroom50 repository,
  2. finds every repository  <classroom slug>-<lab>-<username>  in the organization,
  3. takes the LAST graded submission before the deadline; if there is none, the last one
     within --late-days after it, with 10% off per started late day,
  4. writes private/grades/<lab>.csv. Then run:  scripts/export_grades.py <lab> --points 100 --source classroom50

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/collect_classroom50.py lab02
"""
import argparse
import base64
import csv
import io
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_lab import lab_due  # noqa: E402  (deadline from the lab page, default Friday 23:59)

CL = json.loads((ROOT / "content" / "data" / "course.json").read_text(encoding="utf-8"))["classroom"]
TZ = timezone(timedelta(hours=3))
TAG = re.compile(r"^submit/(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\dZ)-([0-9a-f]+)$")
SCORE = re.compile(r"autograde:\s*([\d.]+)\s*/\s*([\d.]+)")


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError(out.stderr.strip())
    return json.loads(out.stdout)


def gh_all(path):
    items, page = [], 1
    while True:
        batch = gh(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def roster():
    raw = gh(f"repos/{CL['org']}/classroom50/contents/{CL['slug']}/roster.csv")
    text = base64.b64decode(raw["content"]).decode("utf-8")
    return {r["username"].lower(): r for r in csv.DictReader(io.StringIO(text)) if r["username"] and r["role"] == "student"}


def norm(text):
    """lower-case, Turkish-aware, for matching names"""
    return " ".join(text.replace("İ", "i").replace("I", "ı").lower().split())


def class_list_ids():
    """(first, last) → student number, from the official class list private/roster.csv"""
    path = ROOT / "private" / "roster.csv"
    if not path.exists():
        return {}
    return {(norm(r["first_name"]), norm(r["last_name"])): r["student_id"] for r in csv.DictReader(path.open(encoding="utf-8"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lab")
    ap.add_argument("--late-days", type=int, default=5)
    ap.add_argument("--exclude", nargs="*", default=["softeng-researcher"], help="test accounts to leave out")
    a = ap.parse_args()

    due_local = lab_due(a.lab)
    due = datetime.strptime(due_local, "%Y-%m-%d %H:%M").replace(tzinfo=TZ).astimezone(timezone.utc)
    cutoff = due + timedelta(days=a.late_days)
    print(f"· deadline {due_local} (Türkiye), late submissions until {cutoff.astimezone(TZ):%Y-%m-%d %H:%M}")

    people = roster()
    ids_by_name = class_list_ids()
    # older GitHub accounts a student used before (column github_lab01 of the class list)
    old_accounts = {}
    cl_path = ROOT / "private" / "roster.csv"
    if cl_path.exists():
        for r in csv.DictReader(cl_path.open(encoding="utf-8")):
            if r.get("github_lab01"):
                old_accounts[r["github_lab01"].lower()] = {"username": r["github_lab01"], "first_name": r["first_name"],
                                                           "last_name": r["last_name"], "email": r["email"]}
    prefix = f"{CL['slug']}-{a.lab}-".lower()
    repos = sorted(r["name"] for r in gh_all(f"orgs/{CL['org']}/repos?type=all") if r["name"].lower().startswith(prefix))
    print(f"· {len(repos)} repositories\n")

    rows = []
    for name in repos:
        user = name[len(prefix):]
        if user in {x.lower() for x in a.exclude}:
            continue
        p = people.get(user) or old_accounts.get(user, {})
        email = p.get("email") or ""
        # a university address carries the student number; otherwise (e.g. a personal Gmail) match by name
        sid = email.split("@")[0] if email.lower().endswith("@firat.edu.tr") else \
            ids_by_name.get((norm(p.get("first_name", "")), norm(p.get("last_name", ""))), "")
        subs = []
        for rel in gh_all(f"repos/{CL['org']}/{name}/releases"):
            m, s = TAG.match(rel["tag_name"]), SCORE.search(rel.get("body") or "")
            if m and s:
                when = datetime.strptime(m.group(1), "%Y-%m-%dT%H-%M-%SZ").replace(tzinfo=timezone.utc)
                subs.append((when, float(s.group(1)), float(s.group(2)), m.group(2)))
        on_time = sorted(x for x in subs if x[0] <= due)
        late = sorted(x for x in subs if due < x[0] <= cutoff)
        pick = on_time[-1] if on_time else (late[-1] if late else None)
        row = {"github": p.get("username") or user, "name": f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
               "student_id": sid, "repo": f"{CL['org']}/{name}", "pushed_at": "", "sha": "", "passed": 0, "total": 0,
               "raw": 0, "late_days": 0, "score": 0, "note": ""}
        if pick:
            when, got, of, sha = pick
            days = max(0, math.ceil((when - due).total_seconds() / 86400))
            row.update(pushed_at=when.astimezone(TZ).strftime("%Y-%m-%d %H:%M"), sha=sha, passed=got, total=of,
                       raw=round(100 * got / of, 2), late_days=days, score=round(100 * got / of * max(0, 1 - 0.1 * days), 2))
            notes = [f"{len(subs)} graded pushes"]
            if days:
                notes.append("late")
            if late and on_time and late[-1][1] / late[-1][2] > got / of:
                notes.append(f"a better late push exists ({late[-1][1]:g}/{late[-1][2]:g})")
            row["note"] = "; ".join(notes)
        else:
            row["note"] = "accepted, no graded push" if not subs else "only pushes after the late window"
        rows.append(row)
        print(f"{'✓' if pick else '·'} {row['github']:<20} {row['passed']:>5g}/{row['total']:<5g} → {row['score']:>6}  {row['pushed_at']}  {row['name']}")

    out = ROOT / "private" / "grades" / f"{a.lab}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["github"])
        w.writeheader()
        w.writerows(rows)
    print(f"\n✓ {out.relative_to(ROOT)} ({len(rows)} students)")


if __name__ == "__main__":
    main()
