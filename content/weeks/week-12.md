---
week: 12
title: "Induction, Recursion and Growth of Functions"
description: "Mathematical and strong induction, recursive definitions, and Big-O for comparing algorithms."
module: m5
status: draft
reading: "Rosen 5.1–5.3, 3.2"
lab: lab-10
objectives:
  - "Write complete proofs by mathematical induction and strong induction."
  - "Define sets, sequences and functions recursively."
  - "Prove properties of recursive definitions by structural induction."
  - "Use Big-O, Big-Ω and Big-Θ to compare growth rates."
  - "Connect loop invariants to induction when reasoning about code."
wow:
  title: "Induction is how you know your recursive code works."
  text: "If the base case is right and each call is right assuming the smaller calls are right, the whole function is right. That sentence is a proof by induction, and it is how you should read every recursive function you write."
industry:
  - {"t": "Loop invariants", "d": "Correctness arguments for loops (binary search, sorting) are induction on the number of iterations."}
  - {"t": "Performance", "d": "Big-O decides whether a feature survives a million users: O(n²) that is fine at 1,000 users can fail at 1,000,000."}
  - {"t": "Parsers and compilers", "d": "Grammars are recursive definitions; compilers process programs by structural recursion."}
slides: []
resources:
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 5, induction"}
  - {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/", "note": "Chapter 10, induction"}
  - {"title": "MIT 6.042J video lectures (OpenCourseWare)", "url": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/", "note": "induction lectures"}
tags: ["induction", "strong induction", "recursion", "Big-O", "growth", "loop invariant"]
---

## Topics

- Mathematical induction
- Strong induction and well-ordering
- Recursive definitions and structural induction
- Recursive algorithms
- Big-O, Big-Ω, Big-Θ

## Before class

- Skim Rosen 5.1–5.3, 3.2 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
