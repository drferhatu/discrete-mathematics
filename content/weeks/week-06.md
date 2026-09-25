---
week: 6
title: "Rules of Inference"
description: "Valid arguments, modus ponens and friends, resolution, and how machines draw conclusions."
module: m3
status: draft
reading: "Rosen 1.6"
lab: lab-05
objectives:
  - "Decide whether an argument form is valid using a truth table."
  - "Apply the rules of inference (modus ponens, modus tollens, hypothetical syllogism, …)."
  - "Build a step-by-step argument, naming the rule used at each step."
  - "Use rules of inference with quantifiers (universal instantiation and generalization)."
  - "Spot common fallacies: affirming the conclusion and denying the hypothesis."
wow:
  title: "A program that reasons: forward chaining in 20 lines of Python."
  text: "Give the computer facts and if-then rules, and it keeps applying modus ponens until nothing new appears. This is the engine behind expert systems, Prolog and the rule engines that approve your bank transactions."
industry:
  - {"t": "Type checkers", "d": "Compilers infer types with inference rules; a type error is a failed proof."}
  - {"t": "Rule engines", "d": "Fraud detection and insurance systems chain thousands of if-then rules with modus ponens."}
  - {"t": "AI reasoning", "d": "Neuro-symbolic systems check a language model's step-by-step reasoning against formal inference rules."}
slides: []
resources:
  - {"title": "forall x: Calgary, an open logic textbook", "url": "https://forallx.openlogicproject.org/", "note": "natural deduction chapters"}
  - {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/", "note": "Chapter 2, logic"}
  - {"title": "Hacettepe BBM 205 slides", "url": "https://web.cs.hacettepe.edu.tr/~bbm205/", "note": "rules of inference slides"}
tags: ["inference", "modus ponens", "modus tollens", "resolution", "fallacy", "argument"]
---

## Topics

- Arguments and validity
- Rules of inference for propositional logic
- Resolution
- Fallacies
- Rules of inference for quantified statements

## Before class

- Skim Rosen 1.6 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
