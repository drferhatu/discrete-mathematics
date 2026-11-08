---
week: 14
title: "Connectivity, Coloring and Trees"
description: "Paths and connectivity, graph coloring, and trees."
module: m6
status: draft
reading: "Rosen 10.4, 10.8, 11.1"
lab: lab-13
objectives:
  - "Decide connectivity and find connected components."
  - "Explain Euler and Hamilton paths and when they exist."
  - "Color graphs, compute simple chromatic numbers and apply coloring to scheduling."
  - "Use the properties of trees: n vertices, n − 1 edges, unique paths."
wow:
  title: "Four colors are enough for any map, and the proof needed a computer."
  text: "The four color theorem was proved in 1976 by checking about 1,500 cases by computer, the first famous computer-assisted proof. Graph coloring also schedules your exams and assigns CPU registers in every compiler."
industry:
  - {"t": "Scheduling", "d": "Exam timetables: courses are vertices, shared students are edges, time slots are colors."}
  - {"t": "Compilers", "d": "Register allocation colors an interference graph so that variables share CPU registers safely."}
  - {"t": "File systems and data", "d": "Folders, JSON documents and HTML pages are trees; Huffman trees compress files."}
slides: []
resources:
  - {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/", "note": "Chapter 4.4, coloring"}
  - {"title": "Four color theorem (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Four_color_theorem"}
  - {"title": "Register allocation (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Register_allocation"}
tags: ["connectivity", "Euler", "Hamilton", "coloring", "chromatic number", "tree", "spanning tree"]
---

## Topics

- Paths, connectivity, components
- Euler and Hamilton paths
- Graph coloring and chromatic number
- Trees and spanning trees

## Before class

- Skim Rosen 10.4, 10.8, 11.1 (20 minutes is enough; we go through it together).
- Bring paper and a pen: part of every lecture is solving by hand.
