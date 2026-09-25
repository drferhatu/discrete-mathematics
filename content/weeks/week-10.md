---
week: 10
title: "Relations and Functions"
description: "Relations and their properties, equivalence relations, and functions: injective, surjective, bijective."
module: m4
status: draft
reading: "Rosen 2.3, 9.1, 9.5"
lab: lab-08
objectives:
  - "Represent relations as sets of pairs, matrices and directed graphs."
  - "Test reflexivity, symmetry, antisymmetry and transitivity."
  - "Find equivalence classes and explain partitions."
  - "Classify functions as injective, surjective or bijective, and compose and invert them."
  - "Explain hash functions and collisions in terms of functions."
wow:
  title: "A relational database is literally a set of relations."
  text: "Edgar Codd built the relational model in 1970 directly on this week's definitions. Every table you query is a relation, and every key constraint is a statement about functions."
industry:
  - {"t": "Relational databases", "d": "Tables are relations; primary keys make them functions from key to row."}
  - {"t": "Hash tables", "d": "A hash function maps keys to buckets. It cannot be injective, which is why collisions must be handled."}
  - {"t": "Version control", "d": "Git's commit history is a relation (“is an ancestor of”) that is reflexive, antisymmetric and transitive: a partial order."}
slides: []
resources:
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapters 4.3–4.4, 10"}
  - {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/", "note": "Chapters 11–12, relations and functions"}
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Section 0.4, functions"}
tags: ["relation", "equivalence relation", "partial order", "function", "bijection", "hash"]
---

## Topics

- Relations and representations
- Properties of relations
- Equivalence relations and partitions
- Functions, domain, codomain, range
- Injective, surjective, bijective
- Composition and inverses; floor and ceiling

## Before class

- Skim Rosen 2.3, 9.1, 9.5 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
