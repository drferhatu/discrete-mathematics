---
week: 5
title: "Nested Quantifiers and Specifications"
description: "∀x∃y versus ∃y∀x: order matters. Writing precise specifications for programs and systems."
module: m2
status: draft
reading: "Rosen 1.5"
lab: lab-04
objectives:
  - "Read and write statements with nested quantifiers."
  - "Explain why swapping ∀ and ∃ can change the meaning."
  - "Negate nested quantified statements mechanically and correctly."
  - "Write a precise specification (pre/postcondition) for a small program."
  - "Check nested-quantifier statements on finite data in Python."
wow:
  title: "“Every user has a friend” ≠ “Someone is everyone’s friend”."
  text: "∀u ∃f Friend(u, f) versus ∃f ∀u Friend(u, f). One swap of two symbols turns a normal social network into one with a celebrity everyone follows. Specifications fail exactly on such swaps, and so do exam answers."
industry:
  - {"t": "Formal specifications", "d": "Engineers at AWS and Microsoft write TLA+ specifications with nested quantifiers to find design bugs before code exists."}
  - {"t": "Limits and continuity", "d": "The ε–δ definition of a limit is ∀ε ∃δ ∀x. Calculus is built on nested quantifiers."}
  - {"t": "Load balancing", "d": "“For every request there exists a server with capacity” is the guarantee a balancer must keep."}
slides:
  - {"title": "Slides: predicate logic practice", "file": "dm-2026-w05-predicate-practice.pdf"}
resources:
  - {"title": "Stanford CS103 Mathematical Foundations of Computing", "url": "https://web.stanford.edu/class/cs103/", "note": "first-order logic, nested quantifiers"}
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 3.6"}
  - {"title": "Leslie Lamport: TLA+", "url": "https://lamport.azurewebsites.net/tla/tla.html", "note": "how industry writes specifications"}
tags: ["nested quantifiers", "specification", "negation", "TLA+"]
---

## Topics

- Nested quantifiers as nested loops
- Order of quantifiers
- Translating nested statements
- Negating nested quantifiers
- Specifications, preconditions and postconditions

## Before class

- Skim Rosen 1.5 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
