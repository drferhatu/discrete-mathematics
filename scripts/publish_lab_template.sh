#!/usr/bin/env bash
# Publish a lab's starter code as a Classroom 50 template repository in the course organization.
#
#   scripts/publish_lab_template.sh lab01
#
# Creates (or updates) the PRIVATE repository  <ORG>/<CLASSROOM>-<lab>-template  from labs/templates/<lab>,
# marks it as a template, and prints the next Classroom 50 step. Needs: gh (logged in as an org owner).
set -euo pipefail
LAB="${1:?usage: $0 labNN}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORG=$(python3 -c "import json;print(json.load(open('$ROOT/content/data/course.json'))['classroom']['org'])")
CLS=$(python3 -c "import json;print(json.load(open('$ROOT/content/data/course.json'))['classroom']['slug'])")
SRC="$ROOT/labs/templates/$LAB"
REPO="$ORG/$CLS-$LAB-template"
[ -d "$SRC" ] || { echo "no template folder: $SRC"; exit 1; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp -R "$SRC/." "$TMP/"
cd "$TMP"
git init -q -b main
git add -A
git commit -q -m "Starter code for $LAB"

if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "· $REPO exists, pushing new starter code (students who already accepted keep their copy)"
  git remote add origin "https://github.com/$REPO.git"
  git push -q --force origin main
else
  gh repo create "$REPO" --private --source . --push --description "Discrete Mathematics $LAB starter code (Classroom 50 template)"
fi
gh api -X PATCH "repos/$REPO" -f is_template=true >/dev/null
echo "✓ https://github.com/$REPO is a template repository"
echo
echo "Next, on classroom50.org → $ORG → $CLS → New assignment:"
echo "  slug: $LAB   template: $REPO   grading: Autograded"
echo "  tests: paste labs/autograders/$LAB/tests.json  (or: gh teacher assignment test set $ORG $CLS $LAB --tests labs/autograders/$LAB/tests.json)"
