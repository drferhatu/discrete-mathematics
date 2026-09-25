---
week: 1
title: "Welcome: What Is Discrete Mathematics?"
description: "The course, the plan for the semester, and why computer science is built on discrete, countable things rather than smooth curves."
module: m1
status: ready
reading: "Rosen, Preface and 1.1 (skim)"
objectives:
  - "Explain what makes mathematics discrete and name five discrete objects you already use in code."
  - "Describe the six modules of the course and how they connect to software."
  - "Know how a Monday works: lecture first, then an autograded Python lab."
  - "Have a GitHub account ready for the labs."
wow:
  title: "A computer can only store discrete things."
  text: "Your laptop has no real numbers. Every float is one of about 2⁶⁴ bit patterns, every image a finite grid, every program a finite string. Discrete mathematics is not a side topic of computer science: it is the mathematics of everything a computer can actually hold."
industry:
  - {"t": "Algorithms and data structures", "d": "Arrays, trees, hash tables and graphs are discrete structures; their analysis is counting and induction."}
  - {"t": "Databases", "d": "Tables are relations, queries are predicate logic, joins are set operations."}
  - {"t": "Cryptography", "d": "Every HTTPS connection relies on number theory and modular arithmetic."}
  - {"t": "Artificial intelligence", "d": "Search, planning, knowledge graphs and the verification of AI-written code are logic and graph theory."}
resources:
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapter 1 is a great first read"}
  - {"title": "Discrete Mathematics YMT211, previous year's site", "url": "https://ferhatucar.notion.site/discrete-mathematics"}
tags: ["introduction", "discrete", "course overview", "GitHub"]
---

> [!note] This lecture took place on Monday, September 21
> The notes below summarize the introduction. If you missed it, read this page and complete the checklist at the bottom before week 2.

## Discrete versus continuous

Calculus studies things that change smoothly: position, speed, area under a curve. **Discrete mathematics** studies objects that are *separate and distinct*: integers, propositions, sets, relations, graphs, strings, programs. You can count them, list them, and often check every one of them.

| Continuous | Discrete |
|---|---|
| Real numbers, $\mathbb{R}$ | Integers $\mathbb{Z}$, rationals $\mathbb{Q}$, bit strings |
| Limits, derivatives | Sums, recurrences, induction |
| A smooth road | A road network: intersections and streets |
| Measuring | Counting |

> [!definition]
> An object is **discrete** when it is made of separate, distinguishable elements with nothing “in between”. A set of such objects is finite or can be listed one after another.

## Why computer scientists need it

Discrete mathematics gives you three things you will use for the rest of your career:

1. **A precise language.** Specifications, requirements and code reviews fail when statements are vague. Logic makes “always”, “sometimes”, “if” and “only if” exact.
2. **A way to be certain.** Tests show that code works on the inputs you tried. A proof shows it works on *all* inputs. Much of modern software verification is proof, done by machines.
3. **Tools for counting and structure.** How many passwords? How long will this loop run? Is this network connected? Can these exams be scheduled without clashes?

> [!example] Where you already met it
> `if (loggedIn && !banned)` is propositional logic. A Python `set` is a set. A folder tree is a tree. A dictionary is a function. A Git history is a graph.

## The semester

We follow six modules over fifteen Mondays. The full plan is on the [schedule](/schedule).

| Module | Weeks | Big question |
|---|---|---|
| Propositional logic | 1–3 | How do we reason with true/false statements? |
| Predicate logic | 4–5 | How do we talk precisely about *all* and *some*? |
| Reasoning and proof | 6–8 | How can we be certain? |
| Sets, relations, functions | 9–11 | What are the data types of mathematics? |
| Induction and counting | 12–13 | How do we prove for every $n$ and count without listing? |
| Graphs and trees | 14–15 | How do we model connected things? |

## How a Monday works

- **Part 1, lecture.** Definitions, examples, and problems you solve by hand. Paper and pen, please.
- **Part 2, lab.** You turn the idea into Python. Each lab has a page with numbered steps so you can start on your own, tests that check your work instantly, and an autograder on GitHub. See [how labs work](/labs).
- **Grading.** Midterm 40%, final 60%. Inside the final, 15% comes from your personal semester [project](/project).

## Before week 2: your checklist

> [!warning] Do this before Monday, September 28
> The first lab needs these three things. It takes about ten minutes.

1. **Create a GitHub account** at [github.com/signup](https://github.com/signup) if you do not have one. Use a username you would be happy to show an employer.
2. **Accept the GitHub organization invitation** that arrives by email (from `FiratUniversity-IJDP-SoftEng`). No email yet? It will come before the lab; check your spam folder.
3. **Sign in once at [classroom50.org](https://classroom50.org)** with that GitHub account and check that you see the course. The full walkthrough is in the [lab setup guide](/guides/lab-setup).

Optional but recommended: apply for the free [GitHub Student Developer Pack](https://education.github.com/pack) with your university email.
