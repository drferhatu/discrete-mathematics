---
week: 4
title: "Predicates and Quantifiers"
description: "Statements with variables: predicates, domains, ∀ and ∃, and negating quantified statements."
module: m2
status: draft
reading: "Rosen 1.4"
lab: lab-03
objectives:
  - "Explain the difference between a proposition and a propositional function P(x)."
  - "Evaluate ∀x P(x) and ∃x P(x) over a given domain."
  - "Translate English statements into predicate logic and back."
  - "Negate quantified statements with De Morgan's laws for quantifiers."
  - "Recognize how Python's all() and any() implement ∀ and ∃ on finite domains."
wow:
  title: "SQL is predicate logic with a nicer keyboard."
  text: "SELECT name FROM students WHERE NOT EXISTS (…) is ∃ and ¬ over a finite domain. Every database you will use this term and in your career evaluates quantified formulas millions of times per second."
industry:
  - {"t": "Databases", "d": "WHERE clauses are predicates; EXISTS and NOT EXISTS are quantifiers; the query planner rewrites them with logical equivalences."}
  - {"t": "Access control", "d": "Cloud permission systems check statements like “for every request, there exists a policy that allows it”."}
  - {"t": "Testing", "d": "Property-based testing (Hypothesis in Python) checks ∀-statements on thousands of random inputs."}
slides:
  - {"title": "Slides: predicate logic", "file": "dm-2026-w04-predicate-logic.pdf"}
resources:
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 3.6, predicate formulas"}
  - {"title": "Stanford CS103 Mathematical Foundations of Computing", "url": "https://web.stanford.edu/class/cs103/", "note": "first-order logic lectures and translation practice"}
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Section 0.2"}
tags: ["predicate", "quantifier", "forall", "exists", "SQL", "all", "any"]
---

## Topics

- Propositional functions and domains
- Universal and existential quantifiers
- Quantifiers with restricted domains
- Precedence and binding of quantifiers
- De Morgan's laws for quantifiers
- Translating English ↔ logic

## Before class

- Skim Rosen 1.4 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
