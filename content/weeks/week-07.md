---
week: 7
title: "Introduction to Proofs"
description: "Direct proof, contrapositive, contradiction, cases and counterexamples. How to be certain."
module: m3
status: draft
reading: "Rosen 1.7–1.8"
lab: lab-06
objectives:
  - "Write a direct proof of a statement of the form p → q."
  - "Prove a statement by contraposition and by contradiction, and choose between them."
  - "Use proof by cases and exhaustive proof on small domains."
  - "Disprove a universal statement with a counterexample."
  - "Use a computer to search for counterexamples and understand why that is not a proof."
wow:
  title: "n² + n + 41 is prime for n = 0, 1, …, 39. Then it isn’t."
  text: "Forty cases in a row look like a pattern, and a pattern is not a proof. In the lab you let Python test millions of cases of famous claims, find where some break, and see why only a proof settles ∀n."
industry:
  - {"t": "Verified software", "d": "The seL4 microkernel and the CompCert C compiler come with machine-checked proofs of correctness."}
  - {"t": "AI and mathematics", "d": "Proof assistants like Lean now check proofs written by humans and AI systems alike."}
  - {"t": "Security", "d": "Cryptographic protocols are proven secure by contradiction: “if an attacker could break this, they could also factor large numbers”."}
slides: []
resources:
  - {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/", "note": "Chapters 4–6, direct, contrapositive, contradiction"}
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 1, proofs"}
  - {"title": "Lean Natural Number Game", "url": "https://adam.math.hhu.de/#/g/leanprover-community/nng4", "note": "prove theorems with a computer"}
  - {"title": "seL4: the verified microkernel", "url": "https://sel4.systems/"}
tags: ["proof", "direct proof", "contrapositive", "contradiction", "counterexample", "Lean"]
---

## Topics

- Direct proof
- Proof by contraposition
- Proof by contradiction (√2 is irrational)
- Proof by cases, exhaustive proof
- Counterexamples
- Proof strategy

## Before class

- Skim Rosen 1.7–1.8 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
