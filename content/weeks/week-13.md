---
week: 13
title: "Counting and the Pigeonhole Principle"
description: "Product and sum rules, permutations, combinations, and the pigeonhole principle."
module: m5
status: draft
reading: "Rosen 6.1–6.3"
lab: lab-11
objectives:
  - "Apply the product rule, the sum rule and the subtraction rule."
  - "Count arrangements with permutations and selections with combinations."
  - "Use the pigeonhole principle and its generalized form."
  - "Estimate password spaces and brute-force times."
  - "Simulate the birthday paradox and connect it to hash collisions."
wow:
  title: "With 23 people in a room, two probably share a birthday."
  text: "It feels impossible, but counting says so, and a 10-line simulation agrees. The same math tells attackers how many tries it takes to find a hash collision, which is why hash sizes are chosen the way they are."
industry:
  - {"t": "Security", "d": "Password policies and key lengths are chosen by counting the search space an attacker must cover."}
  - {"t": "Hashing", "d": "The pigeonhole principle guarantees collisions; the birthday bound says how soon they appear."}
  - {"t": "Testing", "d": "Combinatorial (pairwise) testing picks a small set of configurations that covers every pair of options."}
slides: []
resources:
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Chapter 1, counting"}
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 15, cardinality rules"}
  - {"title": "Birthday problem (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Birthday_problem"}
tags: ["counting", "product rule", "pigeonhole", "permutation", "combination", "binomial", "birthday paradox"]
---

## Topics

- Product and sum rules
- Inclusion–exclusion for two sets
- The pigeonhole principle
- Permutations and combinations
- Binomial coefficients and Pascal's triangle

## Before class

- Skim Rosen 6.1–6.3 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
