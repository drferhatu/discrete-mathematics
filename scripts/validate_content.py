#!/usr/bin/env python
"""Content and build checks.

  1. content/weeks has weeks 1..N (N = rows in schedule.json), unique, each in exactly the module that lists it.
  2. schedule.json dates are valid, increasing Mondays; statuses are known.
  3. Every week's `lab:` points to an existing lab file; every lab's `week` exists.
  4. Every slide file referenced by a week exists in public/slides/.
  5. Every lab with a template folder has README, tests and an autograder tests.json.
  6. (if dist/ exists) internal links in the built HTML resolve.

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/validate_content.py
"""
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
WEEKS_DIR = ROOT / "content" / "weeks"
LABS_DIR = ROOT / "content" / "labs"
DATA = ROOT / "content" / "data"
DIST = ROOT / "dist"
BASE = "/discrete-mathematics"
errors: list[str] = []


def frontmatter(path: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    if not m:
        errors.append(f"{path.name}: no frontmatter")
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^(\w+):\s*(.*)$", line)
        if mm and mm.group(2):
            fm[mm.group(1)] = mm.group(2).strip().strip('"')
    fm["_raw"] = m.group(1)
    return fm


def content_files(d: Path):
    return sorted(list(d.glob("*.md")) + list(d.glob("*.mdx")))


def main():
    schedule = json.loads((DATA / "schedule.json").read_text(encoding="utf-8"))["weeks"]
    modules = json.loads((DATA / "modules.json").read_text(encoding="utf-8"))
    n_weeks = len(schedule)

    # schedule
    if [r["week"] for r in schedule] != list(range(1, n_weeks + 1)):
        errors.append("schedule.json weeks are not 1..N in order")
    prev = None
    for r in schedule:
        if r.get("status") not in {"normal", "holiday", "postponed", "exam"}:
            errors.append(f"schedule week {r['week']}: unknown status {r.get('status')!r}")
        if r.get("date"):
            try:
                d = date.fromisoformat(r["date"])
                if d.weekday() != 0:
                    errors.append(f"schedule week {r['week']}: {d} is not a Monday")
                if prev and d <= prev:
                    errors.append(f"schedule week {r['week']}: date not after previous week")
                prev = d
            except ValueError:
                errors.append(f"schedule week {r['week']}: bad date {r['date']!r}")

    # labs
    labs = {}
    for p in content_files(LABS_DIR):
        fm = frontmatter(p)
        labs[p.stem] = fm
        if not fm.get("assignment"):
            errors.append(f"{p.name}: no assignment slug")
        tdir = ROOT / "labs" / "templates" / fm.get("assignment", "?")
        if tdir.exists():
            for need in ["README.md", "tests"]:
                if not (tdir / need).exists():
                    errors.append(f"template {tdir.name}: missing {need}")
            if not (ROOT / "labs" / "autograders" / tdir.name / "tests.json").exists():
                errors.append(f"template {tdir.name}: missing labs/autograders/{tdir.name}/tests.json")
        elif fm.get("status") == "open":
            errors.append(f"{p.name}: status open but no template at labs/templates/{fm.get('assignment')}")

    # weeks
    mod_by_id = {m["id"]: m for m in modules}
    seen = {}
    for p in content_files(WEEKS_DIR):
        fm = frontmatter(p)
        n = int(fm.get("week", -1))
        if n in seen:
            errors.append(f"{p.name}: week {n} already in {seen[n]}")
        seen[n] = p.name
        mod = fm.get("module")
        if mod not in mod_by_id:
            errors.append(f"{p.name}: unknown module {mod!r}")
        elif n not in mod_by_id[mod]["weeks"]:
            errors.append(f"{p.name}: week {n} is not listed in module {mod}")
        if fm.get("lab") and fm["lab"] not in labs:
            errors.append(f"{p.name}: lab {fm['lab']!r} has no file in content/labs")
        for f in re.findall(r'"file":\s*"([^"]+\.pdf)"', fm["_raw"]):
            if not (ROOT / "public" / "slides" / f).exists():
                errors.append(f"{p.name}: slide file public/slides/{f} missing")
    if sorted(seen) != list(range(1, n_weeks + 1)):
        errors.append(f"week files {sorted(seen)} do not match schedule 1..{n_weeks}")
    union = sorted(w for m in modules for w in m["weeks"])
    if union != list(range(1, n_weeks + 1)):
        errors.append(f"modules.json weeks {union} do not cover 1..{n_weeks} exactly once")
    print(f"✓ {len(seen)} weeks, {len(modules)} modules, {len(labs)} labs")

    check_dist(n_weeks)

    if errors:
        print("\n✗ ERRORS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("\nAll checks passed.")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def check_dist(n_weeks):
    if not DIST.exists():
        print("· no dist/, link check skipped (run npm run build first)")
        return
    pages = list(DIST.rglob("*.html"))
    broken = set()
    for page in pages:
        if "notebooks" in page.parts:
            continue
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        page_url = "/" + page.relative_to(DIST).as_posix().replace("index.html", "")
        for link in parser.links:
            u = urlsplit(link)
            if u.scheme or link.startswith(("#", "mailto:", "data:")):
                continue
            path = unquote(urlsplit(urljoin(BASE + page_url, link)).path)
            if not path.startswith(BASE + "/") and path != BASE:
                broken.add((page.relative_to(DIST).as_posix(), link, "outside base"))
                continue
            target = DIST / path[len(BASE):].lstrip("/")
            if not (target.exists() or (target / "index.html").exists() or target.with_suffix(".html").exists()):
                broken.add((page.relative_to(DIST).as_posix(), link, "missing"))
    for b in sorted(broken):
        errors.append(f"broken link: {b[0]} → {b[1]} ({b[2]})")
    week_pages = [p for p in pages if "/weeks/week-" in p.as_posix()]
    if len(week_pages) != n_weeks:
        errors.append(f"dist has {len(week_pages)} week pages, expected {n_weeks}")
    print(f"✓ dist: {len(pages)} pages, links checked")


if __name__ == "__main__":
    main()
