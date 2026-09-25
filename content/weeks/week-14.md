---
week: 14
title: "Graphs: Models, Terminology and Representations"
description: "Graphs as models of networks, degree and the handshake theorem, special graphs, representations and isomorphism."
module: m6
status: draft
reading: "Rosen 10.1–10.3"
lab: lab-12
objectives:
  - "Model real problems as simple graphs, multigraphs and directed graphs."
  - "Use degree and the handshake theorem."
  - "Recognize complete, cycle, wheel, cube and bipartite graphs."
  - "Represent graphs with adjacency lists and matrices and choose between them."
  - "Decide whether two graphs are isomorphic using invariants."
wow:
  title: "Google Maps, LinkedIn and your compiler all see the world as G = (V, E)."
  text: "Cities and roads, people and connections, variables and conflicts: one abstraction, dozens of billion-dollar products. This week you learn the vocabulary; in the lab you load a real network and query it."
industry:
  - {"t": "Navigation", "d": "Route planning runs shortest-path algorithms on graphs with millions of vertices."}
  - {"t": "Social networks", "d": "Friend suggestions, influence and communities are graph problems."}
  - {"t": "Dependencies", "d": "Package managers (pip, npm) resolve dependency graphs; build systems order them."}
slides: []
resources:
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Chapter 4, graph theory"}
  - {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf", "note": "Chapters 11–12, graphs"}
  - {"title": "Graph Online", "url": "https://graphonline.top/en/", "note": "draw and explore graphs"}
tags: ["graph", "degree", "handshake", "bipartite", "adjacency", "isomorphism"]
---

## Topics

- Graph models
- Degree, handshake theorem
- Special graphs and bipartite graphs
- Adjacency lists and matrices
- Graph isomorphism and invariants

## Before class

- Skim Rosen 10.1–10.3 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
