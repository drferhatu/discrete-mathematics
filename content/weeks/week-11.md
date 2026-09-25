---
week: 11
title: "Sequences, Sums and the Sizes of Infinity"
description: "Sequences and recurrences, summation formulas, and why some infinite sets are bigger than others."
module: m4
status: draft
reading: "Rosen 2.4–2.5"
lab: lab-09
objectives:
  - "Define sequences explicitly and by recurrence, including Fibonacci."
  - "Evaluate arithmetic and geometric sums and use summation notation."
  - "Decide whether two sets have the same cardinality using bijections."
  - "Show that ℤ and ℚ are countable and that ℝ is not (Cantor's diagonal argument)."
  - "Connect uncountability to the existence of problems no program can solve."
wow:
  title: "There are more problems than programs."
  text: "Programs are finite strings, so there are countably many of them. Yes/no problems are subsets of ℕ, and there are uncountably many. Cantor's 1891 diagonal trick therefore proves that most problems cannot be solved by any computer, ever."
industry:
  - {"t": "Algorithm analysis", "d": "Running times are sums: a nested loop costs 1 + 2 + … + n = n(n+1)/2 steps."}
  - {"t": "Finance and growth", "d": "Compound interest and population models are geometric sequences and recurrences."}
  - {"t": "Computability", "d": "The halting problem uses the same diagonal argument as Cantor."}
slides:
  - {"title": "Slides: sequences and sums", "file": "dm-2026-w11-sequences-sums.pdf"}
  - {"title": "Slides: cardinality of sets", "file": "dm-2026-w11-cardinality.pdf"}
resources:
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 8, infinite sets"}
  - {"title": "Stanford CS103 Mathematical Foundations of Computing", "url": "https://web.stanford.edu/class/cs103/", "note": "cardinality and unsolvable problems lectures"}
  - {"title": "Cantor's diagonal argument (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument"}
tags: ["sequence", "recurrence", "summation", "Fibonacci", "cardinality", "countable", "Cantor", "halting problem"]
---

## Topics

- Sequences, recurrence relations, Fibonacci
- Arithmetic and geometric progressions
- Summations and closed forms
- Cardinality, countable sets
- Cantor's diagonal argument
- Uncountability and computability

## Before class

- Skim Rosen 2.4–2.5 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
