---
week: 9
title: "Sets and Set Operations"
description: "Sets, subsets, power sets, Cartesian products, and the algebra of sets."
module: m4
status: draft
reading: "Rosen 2.1–2.2"
lab: lab-07
objectives:
  - "Describe sets by roster and by set-builder notation."
  - "Decide subset relations and compute power sets and Cartesian products."
  - "Apply union, intersection, difference and complement, and prove set identities."
  - "Connect set identities to the logical equivalences from week 3."
  - "Use Python sets, and measure similarity with the Jaccard index."
wow:
  title: "Netflix, Spotify and plagiarism checkers all compute |A ∩ B| / |A ∪ B|."
  text: "The Jaccard similarity of two sets is a single line of set algebra. It recommends songs, finds near-duplicate web pages and flags copied homework. You will build a mini recommender with it."
industry:
  - {"t": "Databases", "d": "UNION, INTERSECT and EXCEPT in SQL are set operations; a JOIN starts as a Cartesian product."}
  - {"t": "Bloom filters", "d": "Browsers and databases test set membership approximately with tiny memory."}
  - {"t": "Access rights", "d": "Permissions are sets; “can this user do X” is a membership test."}
slides: []
resources:
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Section 0.3, sets"}
  - {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/", "note": "Chapter 1, sets"}
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 4.1"}
tags: ["sets", "power set", "Cartesian product", "union", "intersection", "Jaccard"]
---

## Topics

- Sets, elements, the empty set
- Subsets and power sets
- Cartesian products
- Union, intersection, difference, complement
- Set identities and membership tables
- Computer representation with bit strings

## Before class

- Skim Rosen 2.1–2.2 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
