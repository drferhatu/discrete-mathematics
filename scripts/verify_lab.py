#!/usr/bin/env python
"""Check a lab's tests in both directions before releasing it.

  starter  (labs/templates/<lab>)            → no test may pass (otherwise the test checks nothing)
  solution (private/solutions/<lab>/*.py)    → every test must pass

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/verify_lab.py lab01
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(tmp: Path) -> tuple[int, int]:
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                         cwd=tmp, capture_output=True, text=True).stdout
    last = out.strip().splitlines()[-1] if out.strip() else ""
    passed = int(next((w for w, n in zip(last.split(), last.split()[1:]) if n.startswith("passed")), 0))
    failed = int(next((w for w, n in zip(last.split(), last.split()[1:]) if n.startswith("failed")), 0))
    return passed, failed


def main():
    lab = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    tpl = ROOT / "labs" / "templates" / lab
    sol = ROOT / "private" / "solutions" / lab
    ok = True
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t) / lab
        shutil.copytree(tpl, tmp)
        p, f = run(tmp)
        print(f"starter : {p} passed, {f} failed")
        if p:
            print("  ✗ some tests pass on the empty starter"); ok = False
        if sol.exists():
            for s in sol.glob("*.py"):
                shutil.copy(s, tmp / s.name)
            p, f = run(tmp)
            print(f"solution: {p} passed, {f} failed")
            if f or not p:
                print("  ✗ the solution does not pass every test"); ok = False
        else:
            print(f"· no solution at {sol.relative_to(ROOT)}, skipped")
    print("✓ lab verified" if ok else "✗ fix the tests before release")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
