---
week: 3
title: "Logical Equivalences and Boolean Circuits"
description: "Biconditional, XOR, the laws of logic, simplifying formulas, and how the same laws build the adder inside your CPU."
module: m1
status: draft
reading: "Rosen 1.2–1.3"
lab: lab-02
objectives:
  - "Use the biconditional and exclusive or, and state when each is true."
  - "Prove equivalences with truth tables and with the laws of logic (De Morgan, distributive, absorption …)."
  - "Simplify a compound proposition step by step, citing a law at every step."
  - "Classify formulas as tautology, contradiction or contingency, and decide satisfiability."
  - "Translate a Boolean formula into a logic circuit and back."
wow:
  title: "Your CPU adds numbers with the logic you learned last week."
  text: "A one-bit adder is just two formulas: sum = p ⊕ q and carry = p ∧ q. Chain 64 of them and you have the adder in your laptop. In the lab you build it from gates and add real binary numbers with nothing but ∧, ∨, ¬ and ⊕."
industry:
  - {"t": "Chip design", "d": "Hardware compilers minimize Boolean formulas so that chips use fewer transistors and less power."}
  - {"t": "SAT solvers", "d": "Satisfiability solvers schedule flights, verify chips and solve Sudoku by searching for a truth assignment that makes a formula true."}
  - {"t": "Bit tricks in code", "d": "x ^ y, masks and flags in C, Python and databases are propositional logic applied bit by bit."}
  - {"t": "Search engines", "d": "Boolean queries (AND, OR, NOT) are how library catalogs and advanced search work."}
slides:
  - {"title": "Slides: biconditional, XOR, simplification", "file": "dm-2026-w03-equivalences-xor.pdf"}
resources:
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Section 3.1, propositional logic"}
  - {"title": "forall x: Calgary, an open logic textbook", "url": "https://forallx.openlogicproject.org/", "note": "Part II, truth tables"}
  - {"title": "Peter Norvig: Solving every Sudoku puzzle", "url": "https://norvig.com/sudoku.html", "note": "constraint propagation, a close cousin of SAT solving"}
  - {"title": "Buffalo CSE 191 lecture notes", "url": "https://cse.buffalo.edu/~epmikida/teaching/sp23/cse191/index.html", "note": "logic lecture slides"}
tags: ["equivalence", "De Morgan", "XOR", "biconditional", "tautology", "SAT", "logic gates", "adder"]
---

## Topics

- Biconditional (↔) and XOR (⊕)
- Tautology, contradiction, contingency
- Logical equivalence (≡) and the table of laws
- De Morgan's laws and simplification proofs
- Satisfiability; Sudoku as a SAT problem
- Logic gates and the half/full adder

## Before class

- Skim Rosen 1.2–1.3 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
