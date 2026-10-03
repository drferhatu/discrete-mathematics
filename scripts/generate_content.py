#!/usr/bin/env python
"""Generate week and lab outline files from the plan below.

Existing files are never overwritten unless --force is given, so hand-written
notes (week-01, week-02, lab-01 …) are safe.

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/generate_content.py [--force]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEEKS = ROOT / "content" / "weeks"
LABS = ROOT / "content" / "labs"

MCS = {"title": "Mathematics for Computer Science (Lehman, Leighton, Meyer)", "url": "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf"}
LEVIN = {"title": "Discrete Mathematics: An Open Introduction (Oscar Levin)", "url": "https://discrete.openmathbooks.org/"}
CS103 = {"title": "Stanford CS103 Mathematical Foundations of Computing", "url": "https://web.stanford.edu/class/cs103/"}
OCW = {"title": "MIT 6.042J video lectures (OpenCourseWare)", "url": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/"}
BOP = {"title": "Book of Proof (Richard Hammack)", "url": "https://richardhammack.github.io/BookOfProof/"}
FORALLX = {"title": "forall x: Calgary, an open logic textbook", "url": "https://forallx.openlogicproject.org/"}
BBM205 = {"title": "Hacettepe BBM 205 slides", "url": "https://web.cs.hacettepe.edu.tr/~bbm205/"}
CSE191 = {"title": "Buffalo CSE 191 lecture notes", "url": "https://cse.buffalo.edu/~epmikida/teaching/sp23/cse191/index.html"}


def r(base, note):
    return {**base, "note": note}


PLAN = [
    # week 3
    dict(week=3, module="m1", lab="lab-02",
         title="Logical Equivalences and Boolean Circuits",
         description="Biconditional, XOR, the laws of logic, simplifying formulas, and how the same laws build the adder inside your CPU.",
         reading="Rosen 1.2–1.3",
         slides=[{"title": "Slides: biconditional, XOR, simplification", "file": "dm-2026-w03-equivalences-xor.pdf"}],
         objectives=[
             "Use the biconditional and exclusive or, and state when each is true.",
             "Prove equivalences with truth tables and with the laws of logic (De Morgan, distributive, absorption …).",
             "Simplify a compound proposition step by step, citing a law at every step.",
             "Classify formulas as tautology, contradiction or contingency, and decide satisfiability.",
             "Translate a Boolean formula into a logic circuit and back.",
         ],
         wow=dict(title="Your CPU adds numbers with the logic you learned last week.",
                  text="A one-bit adder is just two formulas: sum = p ⊕ q and carry = p ∧ q. Chain 64 of them and you have the adder in your laptop. In the lab you build it from gates and add real binary numbers with nothing but ∧, ∨, ¬ and ⊕."),
         industry=[
             {"t": "Chip design", "d": "Hardware compilers minimize Boolean formulas so that chips use fewer transistors and less power."},
             {"t": "SAT solvers", "d": "Satisfiability solvers schedule flights, verify chips and solve Sudoku by searching for a truth assignment that makes a formula true."},
             {"t": "Bit tricks in code", "d": "x ^ y, masks and flags in C, Python and databases are propositional logic applied bit by bit."},
             {"t": "Search engines", "d": "Boolean queries (AND, OR, NOT) are how library catalogs and advanced search work."},
         ],
         topics=["Biconditional (↔) and XOR (⊕)", "Tautology, contradiction, contingency", "Logical equivalence (≡) and the table of laws", "De Morgan's laws and simplification proofs", "Satisfiability; Sudoku as a SAT problem", "Logic gates and the half/full adder"],
         resources=[r(LEVIN, "Section 3.1, propositional logic"), r(FORALLX, "Part II, truth tables"), {"title": "Peter Norvig: Solving every Sudoku puzzle", "url": "https://norvig.com/sudoku.html", "note": "constraint propagation, a close cousin of SAT solving"}, r(CSE191, "logic lecture slides")],
         tags=["equivalence", "De Morgan", "XOR", "biconditional", "tautology", "SAT", "logic gates", "adder"]),
    # week 4
    dict(week=4, module="m2", lab="lab-03",
         title="Predicates and Quantifiers",
         description="Statements with variables: predicates, domains, ∀ and ∃, and negating quantified statements.",
         reading="Rosen 1.4",
         slides=[{"title": "Slides: predicate logic", "file": "dm-2026-w04-predicate-logic.pdf"}],
         objectives=[
             "Explain the difference between a proposition and a propositional function P(x).",
             "Evaluate ∀x P(x) and ∃x P(x) over a given domain.",
             "Translate English statements into predicate logic and back.",
             "Negate quantified statements with De Morgan's laws for quantifiers.",
             "Recognize how Python's all() and any() implement ∀ and ∃ on finite domains.",
         ],
         wow=dict(title="SQL is predicate logic with a nicer keyboard.",
                  text="SELECT name FROM students WHERE NOT EXISTS (…) is ∃ and ¬ over a finite domain. Every database you will use this term and in your career evaluates quantified formulas millions of times per second."),
         industry=[
             {"t": "Databases", "d": "WHERE clauses are predicates; EXISTS and NOT EXISTS are quantifiers; the query planner rewrites them with logical equivalences."},
             {"t": "Access control", "d": "Cloud permission systems check statements like “for every request, there exists a policy that allows it”."},
             {"t": "Testing", "d": "Property-based testing (Hypothesis in Python) checks ∀-statements on thousands of random inputs."},
         ],
         topics=["Propositional functions and domains", "Universal and existential quantifiers", "Quantifiers with restricted domains", "Precedence and binding of quantifiers", "De Morgan's laws for quantifiers", "Translating English ↔ logic"],
         resources=[r(MCS, "Chapter 3.6, predicate formulas"), r(CS103, "first-order logic lectures and translation practice"), r(LEVIN, "Section 0.2")],
         tags=["predicate", "quantifier", "forall", "exists", "SQL", "all", "any"]),
    # week 5
    dict(week=5, module="m2", lab="lab-04",
         title="Nested Quantifiers and Specifications",
         description="∀x∃y versus ∃y∀x: order matters. Writing precise specifications for programs and systems.",
         reading="Rosen 1.5",
         slides=[{"title": "Slides: predicate logic practice", "file": "dm-2026-w05-predicate-practice.pdf"}],
         objectives=[
             "Read and write statements with nested quantifiers.",
             "Explain why swapping ∀ and ∃ can change the meaning.",
             "Negate nested quantified statements mechanically and correctly.",
             "Write a precise specification (pre/postcondition) for a small program.",
             "Check nested-quantifier statements on finite data in Python.",
         ],
         wow=dict(title="“Every user has a friend” ≠ “Someone is everyone’s friend”.",
                  text="∀u ∃f Friend(u, f) versus ∃f ∀u Friend(u, f). One swap of two symbols turns a normal social network into one with a celebrity everyone follows. Specifications fail exactly on such swaps, and so do exam answers."),
         industry=[
             {"t": "Formal specifications", "d": "Engineers at AWS and Microsoft write TLA+ specifications with nested quantifiers to find design bugs before code exists."},
             {"t": "Limits and continuity", "d": "The ε–δ definition of a limit is ∀ε ∃δ ∀x. Calculus is built on nested quantifiers."},
             {"t": "Load balancing", "d": "“For every request there exists a server with capacity” is the guarantee a balancer must keep."},
         ],
         topics=["Nested quantifiers as nested loops", "Order of quantifiers", "Translating nested statements", "Negating nested quantifiers", "Specifications, preconditions and postconditions"],
         resources=[r(CS103, "first-order logic, nested quantifiers"), r(MCS, "Chapter 3.6"), {"title": "Leslie Lamport: TLA+", "url": "https://lamport.azurewebsites.net/tla/tla.html", "note": "how industry writes specifications"}],
         tags=["nested quantifiers", "specification", "negation", "TLA+"]),
    # week 6
    dict(week=6, module="m3", lab="lab-05",
         title="Rules of Inference",
         description="Valid arguments, modus ponens and friends, resolution, and how machines draw conclusions.",
         reading="Rosen 1.6",
         objectives=[
             "Decide whether an argument form is valid using a truth table.",
             "Apply the rules of inference (modus ponens, modus tollens, hypothetical syllogism, …).",
             "Build a step-by-step argument, naming the rule used at each step.",
             "Use rules of inference with quantifiers (universal instantiation and generalization).",
             "Spot common fallacies: affirming the conclusion and denying the hypothesis.",
         ],
         wow=dict(title="A program that reasons: forward chaining in 20 lines of Python.",
                  text="Give the computer facts and if-then rules, and it keeps applying modus ponens until nothing new appears. This is the engine behind expert systems, Prolog and the rule engines that approve your bank transactions."),
         industry=[
             {"t": "Type checkers", "d": "Compilers infer types with inference rules; a type error is a failed proof."},
             {"t": "Rule engines", "d": "Fraud detection and insurance systems chain thousands of if-then rules with modus ponens."},
             {"t": "AI reasoning", "d": "Neuro-symbolic systems check a language model's step-by-step reasoning against formal inference rules."},
         ],
         topics=["Arguments and validity", "Rules of inference for propositional logic", "Resolution", "Fallacies", "Rules of inference for quantified statements"],
         resources=[r(FORALLX, "natural deduction chapters"), r(BOP, "Chapter 2, logic"), r(BBM205, "rules of inference slides")],
         tags=["inference", "modus ponens", "modus tollens", "resolution", "fallacy", "argument"]),
    # week 7
    dict(week=7, module="m3", lab="lab-06",
         title="Introduction to Proofs",
         description="Direct proof, contrapositive, contradiction, cases and counterexamples. How to be certain.",
         reading="Rosen 1.7–1.8",
         objectives=[
             "Write a direct proof of a statement of the form p → q.",
             "Prove a statement by contraposition and by contradiction, and choose between them.",
             "Use proof by cases and exhaustive proof on small domains.",
             "Disprove a universal statement with a counterexample.",
             "Use a computer to search for counterexamples and understand why that is not a proof.",
         ],
         wow=dict(title="n² + n + 41 is prime for n = 0, 1, …, 39. Then it isn’t.",
                  text="Forty cases in a row look like a pattern, and a pattern is not a proof. In the lab you let Python test millions of cases of famous claims, find where some break, and see why only a proof settles ∀n."),
         industry=[
             {"t": "Verified software", "d": "The seL4 microkernel and the CompCert C compiler come with machine-checked proofs of correctness."},
             {"t": "AI and mathematics", "d": "Proof assistants like Lean now check proofs written by humans and AI systems alike."},
             {"t": "Security", "d": "Cryptographic protocols are proven secure by contradiction: “if an attacker could break this, they could also factor large numbers”."},
         ],
         topics=["Direct proof", "Proof by contraposition", "Proof by contradiction (√2 is irrational)", "Proof by cases, exhaustive proof", "Counterexamples", "Proof strategy"],
         resources=[r(BOP, "Chapters 4–6, direct, contrapositive, contradiction"), r(MCS, "Chapter 1, proofs"), {"title": "Lean Natural Number Game", "url": "https://adam.math.hhu.de/#/g/leanprover-community/nng4", "note": "prove theorems with a computer"}, {"title": "seL4: the verified microkernel", "url": "https://sel4.systems/"}],
         tags=["proof", "direct proof", "contrapositive", "contradiction", "counterexample", "Lean"]),
    # week 8
    dict(week=8, module="m3", lab=None, exam=True,
         title="Midterm Exam",
         description="Written midterm on weeks 1–7: propositional logic, predicate logic, rules of inference and proofs.",
         reading="Review Rosen 1.1–1.8",
         objectives=[
             "Show fluency with truth tables, equivalences and translations.",
             "Negate and translate quantified statements correctly.",
             "Write short, correct proofs using the methods from week 7.",
         ],
         topics=["Scope: weeks 1–7", "Closed book; one handwritten A4 sheet of your own notes may be allowed (confirmed in class)", "Past midterms are discussed in the week 7 lab"],
         resources=[r(BBM205, "practice problems"), r(CS103, "practice problem sets with solutions")],
         tags=["midterm", "exam", "review"]),
    # week 9
    dict(week=9, module="m4", lab="lab-07",
         title="Sets and Set Operations",
         description="Sets, subsets, power sets, Cartesian products, and the algebra of sets.",
         reading="Rosen 2.1–2.2",
         objectives=[
             "Describe sets by roster and by set-builder notation.",
             "Decide subset relations and compute power sets and Cartesian products.",
             "Apply union, intersection, difference and complement, and prove set identities.",
             "Connect set identities to the logical equivalences from week 3.",
             "Use Python sets, and measure similarity with the Jaccard index.",
         ],
         wow=dict(title="Netflix, Spotify and plagiarism checkers all compute |A ∩ B| / |A ∪ B|.",
                  text="The Jaccard similarity of two sets is a single line of set algebra. It recommends songs, finds near-duplicate web pages and flags copied homework. You will build a mini recommender with it."),
         industry=[
             {"t": "Databases", "d": "UNION, INTERSECT and EXCEPT in SQL are set operations; a JOIN starts as a Cartesian product."},
             {"t": "Bloom filters", "d": "Browsers and databases test set membership approximately with tiny memory."},
             {"t": "Access rights", "d": "Permissions are sets; “can this user do X” is a membership test."},
         ],
         topics=["Sets, elements, the empty set", "Subsets and power sets", "Cartesian products", "Union, intersection, difference, complement", "Set identities and membership tables", "Computer representation with bit strings"],
         resources=[r(LEVIN, "Section 0.3, sets"), r(BOP, "Chapter 1, sets"), r(MCS, "Chapter 4.1")],
         tags=["sets", "power set", "Cartesian product", "union", "intersection", "Jaccard"]),
    # week 10
    dict(week=10, module="m4", lab="lab-08",
         title="Relations and Functions",
         description="Relations and their properties, equivalence relations, and functions: injective, surjective, bijective.",
         reading="Rosen 2.3, 9.1, 9.5",
         objectives=[
             "Represent relations as sets of pairs, matrices and directed graphs.",
             "Test reflexivity, symmetry, antisymmetry and transitivity.",
             "Find equivalence classes and explain partitions.",
             "Classify functions as injective, surjective or bijective, and compose and invert them.",
             "Explain hash functions and collisions in terms of functions.",
         ],
         wow=dict(title="A relational database is literally a set of relations.",
                  text="Edgar Codd built the relational model in 1970 directly on this week's definitions. Every table you query is a relation, and every key constraint is a statement about functions."),
         industry=[
             {"t": "Relational databases", "d": "Tables are relations; primary keys make them functions from key to row."},
             {"t": "Hash tables", "d": "A hash function maps keys to buckets. It cannot be injective, which is why collisions must be handled."},
             {"t": "Version control", "d": "Git's commit history is a relation (“is an ancestor of”) that is reflexive, antisymmetric and transitive: a partial order."},
         ],
         topics=["Relations and representations", "Properties of relations", "Equivalence relations and partitions", "Functions, domain, codomain, range", "Injective, surjective, bijective", "Composition and inverses; floor and ceiling"],
         resources=[r(MCS, "Chapters 4.3–4.4, 10"), r(BOP, "Chapters 11–12, relations and functions"), r(LEVIN, "Section 0.4, functions")],
         tags=["relation", "equivalence relation", "partial order", "function", "bijection", "hash"]),
    # week 11
    dict(week=11, module="m4", lab="lab-09",
         title="Sequences, Sums and the Sizes of Infinity",
         description="Sequences and recurrences, summation formulas, and why some infinite sets are bigger than others.",
         reading="Rosen 2.4–2.5",
         slides=[{"title": "Slides: sequences and sums", "file": "dm-2026-w11-sequences-sums.pdf"}, {"title": "Slides: cardinality of sets", "file": "dm-2026-w11-cardinality.pdf"}],
         objectives=[
             "Define sequences explicitly and by recurrence, including Fibonacci.",
             "Evaluate arithmetic and geometric sums and use summation notation.",
             "Decide whether two sets have the same cardinality using bijections.",
             "Show that ℤ and ℚ are countable and that ℝ is not (Cantor's diagonal argument).",
             "Connect uncountability to the existence of problems no program can solve.",
         ],
         wow=dict(title="There are more problems than programs.",
                  text="Programs are finite strings, so there are countably many of them. Yes/no problems are subsets of ℕ, and there are uncountably many. Cantor's 1891 diagonal trick therefore proves that most problems cannot be solved by any computer, ever."),
         industry=[
             {"t": "Algorithm analysis", "d": "Running times are sums: a nested loop costs 1 + 2 + … + n = n(n+1)/2 steps."},
             {"t": "Finance and growth", "d": "Compound interest and population models are geometric sequences and recurrences."},
             {"t": "Computability", "d": "The halting problem uses the same diagonal argument as Cantor."},
         ],
         topics=["Sequences, recurrence relations, Fibonacci", "Arithmetic and geometric progressions", "Summations and closed forms", "Cardinality, countable sets", "Cantor's diagonal argument", "Uncountability and computability"],
         resources=[r(MCS, "Chapter 8, infinite sets"), r(CS103, "cardinality and unsolvable problems lectures"), {"title": "Cantor's diagonal argument (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument"}],
         tags=["sequence", "recurrence", "summation", "Fibonacci", "cardinality", "countable", "Cantor", "halting problem"]),
    # week 12
    dict(week=12, module="m5", lab="lab-10",
         title="Induction, Recursion and Growth of Functions",
         description="Mathematical and strong induction, recursive definitions, and Big-O for comparing algorithms.",
         reading="Rosen 5.1–5.3, 3.2",
         objectives=[
             "Write complete proofs by mathematical induction and strong induction.",
             "Define sets, sequences and functions recursively.",
             "Prove properties of recursive definitions by structural induction.",
             "Use Big-O, Big-Ω and Big-Θ to compare growth rates.",
             "Connect loop invariants to induction when reasoning about code.",
         ],
         wow=dict(title="Induction is how you know your recursive code works.",
                  text="If the base case is right and each call is right assuming the smaller calls are right, the whole function is right. That sentence is a proof by induction, and it is how you should read every recursive function you write."),
         industry=[
             {"t": "Loop invariants", "d": "Correctness arguments for loops (binary search, sorting) are induction on the number of iterations."},
             {"t": "Performance", "d": "Big-O decides whether a feature survives a million users: O(n²) that is fine at 1,000 users can fail at 1,000,000."},
             {"t": "Parsers and compilers", "d": "Grammars are recursive definitions; compilers process programs by structural recursion."},
         ],
         topics=["Mathematical induction", "Strong induction and well-ordering", "Recursive definitions and structural induction", "Recursive algorithms", "Big-O, Big-Ω, Big-Θ"],
         resources=[r(MCS, "Chapter 5, induction"), r(BOP, "Chapter 10, induction"), r(OCW, "induction lectures")],
         tags=["induction", "strong induction", "recursion", "Big-O", "growth", "loop invariant"]),
    # week 13
    dict(week=13, module="m5", lab="lab-11",
         title="Counting and the Pigeonhole Principle",
         description="Product and sum rules, permutations, combinations, and the pigeonhole principle.",
         reading="Rosen 6.1–6.3",
         objectives=[
             "Apply the product rule, the sum rule and the subtraction rule.",
             "Count arrangements with permutations and selections with combinations.",
             "Use the pigeonhole principle and its generalized form.",
             "Estimate password spaces and brute-force times.",
             "Simulate the birthday paradox and connect it to hash collisions.",
         ],
         wow=dict(title="With 23 people in a room, two probably share a birthday.",
                  text="It feels impossible, but counting says so, and a 10-line simulation agrees. The same math tells attackers how many tries it takes to find a hash collision, which is why hash sizes are chosen the way they are."),
         industry=[
             {"t": "Security", "d": "Password policies and key lengths are chosen by counting the search space an attacker must cover."},
             {"t": "Hashing", "d": "The pigeonhole principle guarantees collisions; the birthday bound says how soon they appear."},
             {"t": "Testing", "d": "Combinatorial (pairwise) testing picks a small set of configurations that covers every pair of options."},
         ],
         topics=["Product and sum rules", "Inclusion–exclusion for two sets", "The pigeonhole principle", "Permutations and combinations", "Binomial coefficients and Pascal's triangle"],
         resources=[r(LEVIN, "Chapter 1, counting"), r(MCS, "Chapter 15, cardinality rules"), {"title": "Birthday problem (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Birthday_problem"}],
         tags=["counting", "product rule", "pigeonhole", "permutation", "combination", "binomial", "birthday paradox"]),
    # week 14
    dict(week=14, module="m6", lab="lab-12",
         title="Graphs: Models, Terminology and Representations",
         description="Graphs as models of networks, degree and the handshake theorem, special graphs, representations and isomorphism.",
         reading="Rosen 10.1–10.3",
         objectives=[
             "Model real problems as simple graphs, multigraphs and directed graphs.",
             "Use degree and the handshake theorem.",
             "Recognize complete, cycle, wheel, cube and bipartite graphs.",
             "Represent graphs with adjacency lists and matrices and choose between them.",
             "Decide whether two graphs are isomorphic using invariants.",
         ],
         wow=dict(title="Google Maps, LinkedIn and your compiler all see the world as G = (V, E).",
                  text="Cities and roads, people and connections, variables and conflicts: one abstraction, dozens of billion-dollar products. This week you learn the vocabulary; in the lab you load a real network and query it."),
         industry=[
             {"t": "Navigation", "d": "Route planning runs shortest-path algorithms on graphs with millions of vertices."},
             {"t": "Social networks", "d": "Friend suggestions, influence and communities are graph problems."},
             {"t": "Dependencies", "d": "Package managers (pip, npm) resolve dependency graphs; build systems order them."},
         ],
         topics=["Graph models", "Degree, handshake theorem", "Special graphs and bipartite graphs", "Adjacency lists and matrices", "Graph isomorphism and invariants"],
         resources=[r(LEVIN, "Chapter 4, graph theory"), r(MCS, "Chapters 11–12, graphs"), {"title": "Graph Online", "url": "https://graphonline.top/en/", "note": "draw and explore graphs"}],
         tags=["graph", "degree", "handshake", "bipartite", "adjacency", "isomorphism"]),
    # week 15
    dict(week=15, module="m6", lab="lab-13",
         title="Connectivity, Coloring and Trees · Project Demo Day",
         description="Paths and connectivity, graph coloring, and trees. Project demos in the second half.",
         reading="Rosen 10.4, 10.8, 11.1",
         objectives=[
             "Decide connectivity and find connected components.",
             "Explain Euler and Hamilton paths and when they exist.",
             "Color graphs, compute simple chromatic numbers and apply coloring to scheduling.",
             "Use the properties of trees: n vertices, n − 1 edges, unique paths.",
             "Present your semester project clearly in five minutes.",
         ],
         wow=dict(title="Four colors are enough for any map, and the proof needed a computer.",
                  text="The four color theorem was proved in 1976 by checking about 1,500 cases by computer, the first famous computer-assisted proof. Graph coloring also schedules your exams and assigns CPU registers in every compiler."),
         industry=[
             {"t": "Scheduling", "d": "Exam timetables: courses are vertices, shared students are edges, time slots are colors."},
             {"t": "Compilers", "d": "Register allocation colors an interference graph so that variables share CPU registers safely."},
             {"t": "File systems and data", "d": "Folders, JSON documents and HTML pages are trees; Huffman trees compress files."},
         ],
         topics=["Paths, connectivity, components", "Euler and Hamilton paths", "Graph coloring and chromatic number", "Trees and spanning trees", "Project demo day"],
         resources=[r(LEVIN, "Chapter 4.4, coloring"), {"title": "Four color theorem (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Four_color_theorem"}, {"title": "Register allocation (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Register_allocation"}],
         tags=["connectivity", "Euler", "Hamilton", "coloring", "chromatic number", "tree", "spanning tree", "project"]),
]

LAB_PLAN = [
    dict(lab=2, week=3, assignment="lab02", title="Gates, Adders and Knights & Knaves",
         description="Check equivalences by brute force, build a binary adder from logic gates, and solve Knights & Knaves puzzles.",
         files=["circuits.py", "puzzles.py"], topics=["equivalence", "logic gates", "SAT by brute force"]),
    dict(lab=3, week=4, assignment="lab03", title="Quantifiers over Real Data",
         description="Evaluate ∀ and ∃ statements over a student–course dataset with all() and any(), then write the same queries in SQL style.",
         files=["quantifiers.py"], topics=["all/any", "domains", "negation"]),
    dict(lab=4, week=5, assignment="lab04", title="Nested Quantifiers: Checking a Social Network",
         description="Test nested-quantifier properties of a small social network and find the witnesses and counterexamples.",
         files=["network.py"], topics=["∀∃ vs ∃∀", "witnesses", "counterexamples"]),
    dict(lab=5, week=6, assignment="lab05", title="A Tiny Inference Engine",
         description="Implement forward chaining with modus ponens, then use it to answer questions from a rule base.",
         files=["inference.py"], topics=["modus ponens", "forward chaining", "valid arguments"]),
    dict(lab=6, week=7, assignment="lab06", title="Counterexample Hunting",
         description="Test famous claims about primes and integers by computer, find counterexamples, and see what a search can and cannot prove.",
         files=["hunt.py"], topics=["primes", "counterexamples", "exhaustive proof"]),
    dict(lab=7, week=9, assignment="lab07", title="Sets and a Mini Recommender",
         description="Implement power sets and Cartesian products, verify set identities, and recommend courses with Jaccard similarity.",
         files=["sets_lab.py"], topics=["power set", "Cartesian product", "Jaccard"]),
    dict(lab=8, week=10, assignment="lab08", title="Relation Properties and Hashing",
         description="Check properties of relations, compute equivalence classes and transitive closure, and measure hash collisions.",
         files=["relations.py"], topics=["reflexive/symmetric/transitive", "closure", "hash functions"]),
    dict(lab=9, week=11, assignment="lab09", title="Recurrences and Cantor's Diagonal",
         description="Compute recurrences three ways, check summation formulas, and run Cantor's diagonal argument on a list of binary strings.",
         files=["sequences.py"], topics=["recurrences", "memoization", "diagonalization"]),
    dict(lab=10, week=12, assignment="lab10", title="Recursion and Growth",
         description="Write recursive functions, check them against induction proofs, and measure running times to see Big-O on a plot.",
         files=["recursion.py"], topics=["recursion", "induction", "timing"]),
    dict(lab=11, week=13, assignment="lab11", title="Counting and the Birthday Paradox",
         description="Count with itertools, verify formulas, estimate password spaces and simulate the birthday paradox.",
         files=["counting.py"], topics=["itertools", "permutations", "simulation"]),
    dict(lab=12, week=14, assignment="lab12", title="Graphs from Scratch",
         description="Build adjacency lists and matrices, verify the handshake theorem, test bipartiteness and compare with networkx.",
         files=["graphs.py"], topics=["adjacency list", "BFS", "bipartite"]),
    dict(lab=13, week=15, assignment="lab13", title="Coloring an Exam Timetable",
         description="Build the conflict graph of real courses and color it greedily to produce an exam schedule.",
         files=["coloring.py"], topics=["greedy coloring", "scheduling", "trees"]),
]


def yaml_list(key, items, indent=""):
    if not items:
        return f"{indent}{key}: []\n"
    out = f"{indent}{key}:\n"
    for it in items:
        out += f"{indent}  - {json.dumps(it, ensure_ascii=False)}\n"
    return out


def week_file(p):
    fm = "---\n"
    fm += f"week: {p['week']}\n"
    fm += f"title: {json.dumps(p['title'], ensure_ascii=False)}\n"
    fm += f"description: {json.dumps(p['description'], ensure_ascii=False)}\n"
    fm += f"module: {p['module']}\n"
    if p.get("exam"):
        fm += "exam: true\n"
    fm += "status: draft\n"
    fm += f"reading: {json.dumps(p['reading'], ensure_ascii=False)}\n"
    if p.get("lab"):
        fm += f"lab: {p['lab']}\n"
    fm += yaml_list("objectives", p["objectives"])
    if p.get("wow"):
        fm += "wow:\n"
        fm += f"  title: {json.dumps(p['wow']['title'], ensure_ascii=False)}\n"
        fm += f"  text: {json.dumps(p['wow']['text'], ensure_ascii=False)}\n"
    fm += yaml_list("industry", p.get("industry", []))
    fm += yaml_list("slides", p.get("slides", []))
    fm += yaml_list("resources", p.get("resources", []))
    fm += f"tags: {json.dumps(p.get('tags', []), ensure_ascii=False)}\n"
    fm += "---\n\n"
    body = "## Topics\n\n" + "\n".join(f"- {t}" for t in p["topics"]) + "\n\n"
    if not p.get("exam"):
        body += ("## Before class\n\n"
                 f"- Skim {p['reading']} (20 minutes is enough; we go through it together).\n"
                 "- Bring paper and a pen: part of every lecture is solving by hand.\n")
    return fm + body


def lab_file(p):
    fm = "---\n"
    for k in ("lab", "week"):
        fm += f"{k}: {p[k]}\n"
    fm += f"title: {json.dumps(p['title'], ensure_ascii=False)}\n"
    fm += f"description: {json.dumps(p['description'], ensure_ascii=False)}\n"
    fm += f"assignment: {p['assignment']}\n"
    fm += "status: draft\n"
    fm += 'duration: "75 min"\n'
    fm += "points: 100\n"
    fm += f"files: {json.dumps(p['files'])}\n"
    fm += f"topics: {json.dumps(p['topics'], ensure_ascii=False)}\n"
    fm += "---\n\n"
    body = ("## What you will build\n\n" + p["description"] + "\n\n"
            "> [!note] Coming soon\n> The full step-by-step instructions, starter code and tests are published before the lab opens in week "
            f"{p['week']}. The workflow is the same as in [Lab 1](/labs/lab-01): accept, solve, `pytest`, submit.\n")
    return fm + body


def main():
    force = "--force" in sys.argv
    WEEKS.mkdir(parents=True, exist_ok=True)
    LABS.mkdir(parents=True, exist_ok=True)
    for p in PLAN:
        path = WEEKS / f"week-{p['week']:02d}.md"
        if path.exists() and not force:
            print(f"· {path.name} exists, kept")
            continue
        path.write_text(week_file(p), encoding="utf-8")
        print(f"✓ {path.name}")
    for p in LAB_PLAN:
        path = LABS / f"lab-{p['lab']:02d}.md"
        if path.exists() and not force:
            print(f"· {path.name} exists, kept")
            continue
        path.write_text(lab_file(p), encoding="utf-8")
        print(f"✓ {path.name}")


if __name__ == "__main__":
    main()
