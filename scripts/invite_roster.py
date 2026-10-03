#!/usr/bin/env python
"""Invite every student in private/roster.csv to the Classroom 50 classroom by email.

Each student gets a GitHub organization invitation (to student_id@firat.edu.tr) carrying the
classroom team; their first and last name go into roster.csv on classroom50.org.
Safe to re-run: addresses that are already invited or already members are skipped by gh teacher.

  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/invite_roster.py            # dry run, prints the commands
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/invite_roster.py --send     # actually invite
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cl = json.loads((ROOT / "content" / "data" / "course.json").read_text(encoding="utf-8"))["classroom"]
send = "--send" in sys.argv

ok = fail = 0
for s in csv.DictReader((ROOT / "private" / "roster.csv").open(encoding="utf-8")):
    cmd = ["gh", "teacher", "roster", "invite", cl["org"], cl["slug"], s["email"],
           "--first-name", s["first_name"], "--last-name", s["last_name"]]
    if not send:
        print(" ".join(cmd))
        continue
    r = subprocess.run(cmd, capture_output=True, text=True)
    msg = (r.stdout + r.stderr).strip().splitlines()
    print(f"{'✓' if r.returncode == 0 else '✗'} {s['email']:<24} {s['first_name']} {s['last_name']}  {msg[-1] if msg else ''}")
    ok += r.returncode == 0
    fail += r.returncode != 0
if send:
    print(f"\n{ok} invited or already in, {fail} failed")
