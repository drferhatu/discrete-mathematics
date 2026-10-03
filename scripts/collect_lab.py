#!/usr/bin/env python
"""Collect and grade a lab submitted through student-owned repositories (plan B, no Classroom 50).

How students submit: they create a PRIVATE repository named  <classroom>-<lab>  (e.g. dm-2026-lab01)
from the public template, add the instructor as a collaborator, and push.

What this script does:
  1. accepts pending collaborator invitations for repositories with that name (unless --no-accept),
  2. finds every such repository shared with you,
  3. picks the last push before the deadline, using GitHub's own record of the `check` workflow runs
     (pushed times cannot be faked like commit dates); late pushes within --late-days get 10%/day off,
  4. clones that exact commit, replaces tests/ with the OFFICIAL tests from labs/templates/<lab>/tests,
     runs pytest, and
  5. writes private/grades/<lab>.csv (gitignored) and prints a summary.

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/collect_lab.py lab01          # deadline read from the lab page
  ... --due "2026-10-02 23:59"                                                        # or given explicitly
  ... --repos alice/dm-2026-lab01 bob/dm-2026-lab01   # grade only these
  ... --no-accept                                     # do not accept invitations
  ... --extra bob/discrete-lab1                       # also accept + grade misnamed repositories

Note: student code runs on this machine (inside a temporary folder, without your GitHub token,
with a timeout). Only run it for your own course's submissions.
"""
import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURSE = json.loads((ROOT / "content" / "data" / "course.json").read_text(encoding="utf-8"))
TZ = timezone(timedelta(hours=3))  # Türkiye, no DST


def gh(*args):
    out = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"gh api {' '.join(args)} failed")
    return json.loads(out.stdout) if out.stdout.strip() else None


def gh_all(path):
    """Every item of a paginated list endpoint."""
    items, page = [], 1
    sep = "&" if "?" in path else "?"
    while True:
        batch = gh(f"{path}{sep}per_page=100&page={page}") or []
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def parse_time(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def accept_invitations(repo_name):
    n = 0
    for inv in gh_all("user/repository_invitations"):
        if inv["repository"]["name"].lower() == repo_name:
            gh("-X", "PATCH", f"user/repository_invitations/{inv['id']}")
            n += 1
    return n


def shared_repos(repo_name):
    repos = gh_all("user/repos?affiliation=collaborator")
    return sorted(r["full_name"] for r in repos if r["name"].lower() == repo_name)


def pushes(full):
    """(time, sha) of every push, from the check workflow's runs; falls back to commit dates."""
    try:
        runs = gh(f"repos/{full}/actions/workflows/check.yml/runs?event=push&per_page=100")["workflow_runs"]
        got = [(parse_time(r["created_at"]), r["head_sha"]) for r in runs]
        if got:
            return got, "push"
    except RuntimeError:
        pass
    commits = gh_all(f"repos/{full}/commits")
    return [(parse_time(c["commit"]["committer"]["date"]), c["sha"]) for c in commits], "commit-date"


def run_tests(full, sha, lab, timeout):
    official = ROOT / "labs" / "templates" / lab
    with tempfile.TemporaryDirectory() as t:
        work = Path(t) / "repo"
        env = {k: v for k, v in os.environ.items() if not k.startswith(("GH_", "GITHUB_"))}
        subprocess.run(["gh", "repo", "clone", full, str(work), "--", "-q"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(work), "checkout", "-q", sha], check=True, capture_output=True)
        readme = (work / "README.md").read_text(encoding="utf-8", errors="ignore") if (work / "README.md").exists() else ""
        shutil.rmtree(work / "tests", ignore_errors=True)
        shutil.copytree(official / "tests", work / "tests")
        shutil.copy(official / "pytest.ini", work / "pytest.ini")
        env.update(HOME=t, PYTHONDONTWRITEBYTECODE="1")
        try:
            out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "tests"],
                                 cwd=work, capture_output=True, text=True, timeout=timeout, env=env).stdout
        except subprocess.TimeoutExpired:
            return 0, 0, readme, "timeout"
    last = out.strip().splitlines()[-1] if out.strip() else ""
    num = lambda word: int(m.group(1)) if (m := re.search(rf"(\d+) {word}", last)) else 0
    passed, failed, errors = num("passed"), num("failed"), num("error")
    return passed, passed + failed + errors, readme, "" if passed + failed + errors else "no tests ran"


def field(readme, name):
    m = re.search(rf"^\s*[-*]?\s*{name}\s*:\s*(.+?)\s*$", readme, re.M | re.I)
    return m.group(1) if m and not m.group(1).startswith("<!--") else ""


def lab_due(lab):
    """`due:` of the lab page whose assignment is <lab>, else Friday 23:59 of its week."""
    for p in sorted((ROOT / "content" / "labs").glob("*.md*")):
        fm = p.read_text(encoding="utf-8").split("---")[1]
        if re.search(rf"^assignment:\s*{lab}\s*$", fm, re.M):
            if m := re.search(r'^due:\s*"?(\d{4}-\d\d-\d\d \d\d:\d\d)"?', fm, re.M):
                return m.group(1)
            week = int(re.search(r"^week:\s*(\d+)", fm, re.M).group(1))
            sched = json.loads((ROOT / "content" / "data" / "schedule.json").read_text(encoding="utf-8"))["weeks"]
            monday = datetime.strptime(next(r["date"] for r in sched if r["week"] == week), "%Y-%m-%d")
            return (monday + timedelta(days=4)).strftime("%Y-%m-%d 23:59")
    raise SystemExit(f"no lab page with assignment: {lab} (give --due)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lab")
    ap.add_argument("--due", help='local time, e.g. "2026-10-02 23:59" (default: from content/labs, else Friday of the lab week)')
    ap.add_argument("--points", type=float, default=10)
    ap.add_argument("--late-days", type=int, default=5, help="accept late pushes up to N days, 10%% off per started day")
    ap.add_argument("--repos", nargs="*", help="grade only these owner/name repositories")
    ap.add_argument("--no-accept", action="store_true")
    ap.add_argument("--extra", nargs="*", default=[], help="misnamed owner/name repositories to accept and grade too")
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()

    repo_name = f"{COURSE['classroom']['slug']}-{a.lab}".lower()
    a.due = a.due or lab_due(a.lab)
    print(f"· deadline {a.due} (Türkiye time)")
    due = datetime.strptime(a.due, "%Y-%m-%d %H:%M").replace(tzinfo=TZ).astimezone(timezone.utc)
    hard_stop = due + timedelta(days=a.late_days)

    if not a.no_accept and not a.repos:
        print(f"✓ accepted {accept_invitations(repo_name)} invitation(s) for {repo_name}")
    if a.extra and not a.no_accept:
        wanted = {r.lower() for r in a.extra}
        for inv in gh_all("user/repository_invitations"):
            if inv["repository"]["full_name"].lower() in wanted:
                gh("-X", "PATCH", f"user/repository_invitations/{inv['id']}")
                print(f"✓ accepted {inv['repository']['full_name']}")
    repos = (a.repos or shared_repos(repo_name)) + [r for r in a.extra if r not in (a.repos or [])]
    print(f"· {len(repos)} repositories to grade\n")

    rows = []
    for full in repos:
        owner = full.split("/")[0]
        row = {"github": owner, "name": "", "student_id": "", "repo": full, "pushed_at": "", "sha": "",
               "passed": 0, "total": 0, "raw": 0, "late_days": 0, "score": 0, "note": ""}
        try:
            events, source = pushes(full)
            ok = sorted([e for e in events if e[0] <= hard_stop], reverse=True)
            if not ok:
                row["note"] = "no push before the cut-off"
                rows.append(row); print(f"✗ {owner:<24} {row['note']}"); continue
            when, sha = ok[0]
            late = max(0, math.ceil((when - due).total_seconds() / 86400))
            passed, total, readme, note = run_tests(full, sha, a.lab, a.timeout)
            raw = round(a.points * passed / total, 2) if total else 0
            row.update(name=field(readme, "Name"), student_id=field(readme, "Student ID"),
                       pushed_at=when.astimezone(TZ).strftime("%Y-%m-%d %H:%M"), sha=sha[:7],
                       passed=passed, total=total, raw=raw, late_days=late,
                       score=round(raw * max(0, 1 - 0.1 * late), 2),
                       note="; ".join(x for x in [note, "commit dates only (Actions off)" if source != "push" else "",
                                                  "name missing in README" if not field(readme, "Name") else ""] if x))
            print(f"{'✓' if passed == total and total else '·'} {owner:<24} {passed:>2}/{total:<2} {row['score']:>5}"
                  f"  {row['pushed_at']}{'  late ' + str(late) + 'd' if late else ''}  {row['name']}")
        except Exception as e:  # keep going: one broken repository must not stop the collection
            row["note"] = f"error: {e}"
            print(f"✗ {owner:<24} {row['note']}")
        rows.append(row)

    best = {}
    for r in rows:
        k = r["github"].lower()
        if k not in best or r["score"] > best[k]["score"]:
            n = best[k]["_n"] + 1 if k in best else 1
            best[k] = {**r, "_n": n}
        else:
            best[k]["_n"] += 1
    rows = []
    for r in best.values():
        if r["_n"] > 1:
            r["note"] = "; ".join(x for x in [r["note"], f"best of {r['_n']} repositories"] if x)
        if r["repo"].split("/")[1].lower() != repo_name:
            r["note"] = "; ".join(x for x in [r["note"], "misnamed repository"] if x)
        r.pop("_n")
        rows.append(r)
    rows.sort(key=lambda r: r["github"].lower())

    out = ROOT / "private" / "grades" / f"{a.lab}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["github"])
        w.writeheader(); w.writerows(rows)
    print(f"\n✓ {out.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
