# Discrete Mathematics (YMT211) · Fall 2026

Course website for **Discrete Mathematics**, Fırat University, Software Engineering (UOLP, taught in English).
Instructor: Assoc. Prof. Ferhat Uçar.

**Live site:** https://drferhatu.github.io/discrete-mathematics/

## Structure

```
content/
  data/course.json         course info, outcomes, grading, policies, books, Classroom 50 settings
  data/modules.json        six modules and their weeks
  data/schedule.json       Monday dates, exam weeks, final
  weeks/week-NN.md(x)      one file per week (frontmatter: objectives, wow moment, industry, lab, slides, resources)
  labs/lab-NN.md(x)        step-by-step lab instructions
  guides/                  setup guides (/guides/<name>)
  announcements/           announcements
labs/
  templates/labNN/         starter repository for each lab (published as a Classroom 50 template)
  autograders/labNN/       Classroom 50 declarative tests
src/                       Astro pages, components, design system (src/styles/global.css)
scripts/                   content generator, notebook builder, validators, template publisher
public/slides/             lecture slides (PDF)
docs/                      maintainer notes (Turkish)
```

## Develop

Node.js 22+, Python 3.12+.

```bash
npm install
npm run dev                                   # http://localhost:4321/discrete-mathematics/
python scripts/build_notebooks.py --execute   # lab notebooks → public/notebooks/*.html
npm run build                                 # dist/ + search index
python scripts/validate_content.py            # content, schedule and link checks
python scripts/verify_lab.py lab01            # starter fails every test, solution passes
```

Every push to `main` builds and deploys to GitHub Pages (`.github/workflows/deploy.yml`).

## Labs

Labs are distributed and autograded with [Classroom 50](https://github.com/foundation50/classroom50/wiki)
and solved in GitHub Codespaces. See `docs/OGRETIM-UYESI-REHBERI.md` for the setup.
