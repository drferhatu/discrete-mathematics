#!/usr/bin/env python
"""Build the lab notebooks and render them to HTML for the website.

- Writes labs/templates/<lab>/<lab>.ipynb from the cell definitions below (only if missing, unless --force).
- Optionally executes them (--execute) and renders public/notebooks/<name>.html (embedded on lab pages).
- Cells tagged "skip-execution" (the ones that import the student's own code) are not executed.

Usage:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/build_notebooks.py [--execute] [--force]
"""
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "public" / "notebooks"
REPO = "drferhatu/discrete-mathematics"
md = new_markdown_cell


def code(src, skip=False):
    c = new_code_cell(src)
    if skip:
        c.metadata["tags"] = ["skip-execution"]
    return c


# ---------------------------------------------------------------------------
# LAB 1 · Truth tables, explored
# ---------------------------------------------------------------------------
LAB01 = [
md("""# Lab 1 · Explore: truth tables, explosions and a famous equivalence

**Discrete Mathematics (YMT211)** · Fall 2026

This notebook is the *playground* half of Lab 1. Nothing here is graded: run each cell (`Shift+Enter`),
read the output, change something, run it again. The graded half is `truth.py`, checked with `python check.py`.

> Where to run it: in your cs50.dev workspace (open the file, pick a Python kernel) or in Google Colab
> (the **Open in Colab** button on the lab page)."""),
md("""## 1 · Every row of a truth table

`itertools.product([True, False], repeat=n)` produces every assignment of `n` variables in standard order.
It is the single most useful line for this lab."""),
code("""from itertools import product

for row in product([True, False], repeat=3):
    print(row)"""),
md("""Let's print a real truth table for $p \\to q$, using $\\neg p \\lor q$ as its definition:"""),
code("""print("p q | p→q")
for p, q in product([True, False], repeat=2):
    print(int(p), int(q), "|", int((not p) or q))"""),
md("""## 2 · A prettier table with pandas

Engineers look at truth tables as data. A `DataFrame` gives us colors and columns for free."""),
code("""import pandas as pd

def table(f, names):
    rows = [dict(zip(names, map(int, r)), result=int(f(*r))) for r in product([True, False], repeat=len(names))]
    return pd.DataFrame(rows)

df = table(lambda p, q, r: ((not p) or q) and r, ["p", "q", "r"])
df.style.map(lambda v: "background-color:#dcf3ea;color:#0e8a63" if v == 1 else "background-color:#fbe3e3;color:#d83a3f")"""),
md("""## 3 · The contrapositive, checked by brute force

A claim about **all** truth values of two variables has only 4 cases, so the computer can check every one.
This is a *proof by exhaustion*: with finitely many cases, checking them all **is** a proof."""),
code("""implies = lambda p, q: (not p) or q

contrapositive = all(implies(p, q) == implies(not q, not p) for p, q in product([True, False], repeat=2))
converse       = all(implies(p, q) == implies(q, p)         for p, q in product([True, False], repeat=2))

print("p → q  ≡  ¬q → ¬p ?", contrapositive)
print("p → q  ≡   q →  p ?", converse)"""),
md("""Which rows break the converse? Let's find the **counterexamples**:"""),
code("""for p, q in product([True, False], repeat=2):
    if implies(p, q) != implies(q, p):
        print(f"counterexample: p={p}, q={q}   p→q={implies(p, q)}, q→p={implies(q, p)}")"""),
md("""## 4 · The explosion: $2^n$ rows

Each new variable doubles the table. Let's time a brute-force tautology check as $n$ grows."""),
code("""import time
import matplotlib.pyplot as plt

ns, secs = [], []
for n in range(4, 22, 2):
    f = lambda *v: any(v) or not any(v)          # a tautology, so we must check every row
    t0 = time.perf_counter()
    all(f(*row) for row in product([True, False], repeat=n))
    ns.append(n); secs.append(time.perf_counter() - t0)

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(ns, secs, "o-", color="#3a39d0")
ax.set_xlabel("number of variables n"); ax.set_ylabel("seconds"); ax.set_title("Brute-force tautology check: time doubles with every variable")
ax.grid(alpha=.3); plt.tight_layout(); plt.show()"""),
code("""for n in [10, 20, 40, 64, 300]:
    rows = 2 ** n
    print(f"n = {n:>3}: 2^n = {rows:.3e} rows")
print("atoms in the observable universe ≈ 1e80")"""),
md("""> **Think:** if checking one row took a nanosecond, how long would $n = 64$ take? (Hint: about 585 years.)
> This is why SAT solvers are clever searches, not truth tables. We meet them in week 3."""),
md("""## 5 · How many different truth tables exist?

A truth table with $n$ variables has $2^n$ rows, and each row can end in 0 or 1. So there are $2^{2^n}$ different
Boolean functions of $n$ variables. For $n = 2$ that is 16: our five connectives are just a few of them."""),
code("""for n in range(1, 6):
    print(f"n = {n}: {2 ** n:>2} rows, {2 ** (2 ** n):,} different Boolean functions")"""),
md("""## 6 · Logic on bits

Python's `&`, `|`, `^` and `~` apply the connectives to every bit of an integer at once."""),
code("""a, b = 0b0110_1100, 0b1010_1010
for name, v in [("a", a), ("b", b), ("a & b", a & b), ("a | b", a | b), ("a ^ b", a ^ b)]:
    print(f"{name:>6} = {v:08b}")"""),
md("""A classic trick: XOR swaps two variables without a temporary, because $x \\oplus y \\oplus y = x$."""),
code("""x, y = 0b1010, 0b0110
x ^= y; y ^= x; x ^= y
print(f"x = {x:04b}, y = {y:04b}")"""),
md("""## 7 · Connect to your lab

Once your `truth.py` passes some checks, import it here and play with **your own** engine.
(This cell only works inside your lab repository, next to `truth.py`.)"""),
code("""from truth import format_table, is_tautology, implies, iff

print(format_table(lambda p, q: implies(p, q), ["p", "q"], "p→q"))
print("De Morgan is a tautology:", is_tautology(lambda p, q: iff(not (p and q), (not p) or (not q)), 2))""", skip=True),
md("""## Your turn

1. Use `table(...)` from section 2 to print the truth table of $(p \\oplus q) \\leftrightarrow \\neg(p \\leftrightarrow q)$. What kind of formula is it?
2. Find all counterexamples to "$p \\to (q \\to r)$ is equivalent to $(p \\to q) \\to r$".
3. Change the timing loop in section 4 to go up to $n = 24$. Estimate from the plot how long $n = 30$ would take, then check your guess."""),
]


# ---------------------------------------------------------------------------
# LAB 2 · XOR, parity and NAND, explored
# ---------------------------------------------------------------------------
LAB02 = [
md("""# Lab 2 · Explore: XOR secrets, self-healing disks and a world made of NAND

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 2. Nothing here is graded: run each cell (`Shift+Enter`), read, change, run again.
The graded half is `circuits.py` and `puzzles.py`, checked with `python check.py`."""),
md("""## 1 · XOR undoes itself

The week 3 notes say $(p \\oplus k) \\oplus k = p$. Python's `^` is XOR on every bit of an integer at once."""),
code("""m, k = 0b1011_0010, 0b0110_1100
c = m ^ k
print(f"message    {m:08b}")
print(f"key        {k:08b}")
print(f"cipher     {c:08b}")
print(f"cipher ^ k {c ^ k:08b}   ← the message again")"""),
md("""## 2 · A tiny one-time pad

Encrypt a sentence by XOR-ing every byte with a random key byte. Without the key the ciphertext is just noise."""),
code("""import secrets

message = "Discrete math is fun".encode()
key = secrets.token_bytes(len(message))          # random, used once
cipher = bytes(m ^ k for m, k in zip(message, key))
back = bytes(c ^ k for c, k in zip(cipher, key))

print("cipher (hex):", cipher.hex())
print("decrypted   :", back.decode())"""),
md("""> **Think:** what happens if you use the *same* key twice for two messages? XOR the two ciphertexts and the key disappears:
> $(m_1 \\oplus k) \\oplus (m_2 \\oplus k) = m_1 \\oplus m_2$. That is exactly how real systems that reused keys were broken."""),
code("""m1, m2 = b"ATTACK AT DAWN", b"RETREAT AT TEN"
k = secrets.token_bytes(len(m1))
c1 = bytes(a ^ b for a, b in zip(m1, k))
c2 = bytes(a ^ b for a, b in zip(m2, k))
leak = bytes(a ^ b for a, b in zip(c1, c2))
print("c1 ^ c2 == m1 ^ m2 :", leak == bytes(a ^ b for a, b in zip(m1, m2)))"""),
md("""## 3 · RAID: a disk dies, the data survives

Three data disks and one parity disk that stores the XOR of the other three. Lose any one disk and XOR the rest."""),
code("""import random

disks = [bytes(random.randrange(256) for _ in range(8)) for _ in range(3)]
parity = bytes(a ^ b ^ c for a, b, c in zip(*disks))

lost = 1
survivors = [d for i, d in enumerate(disks) if i != lost] + [parity]
rebuilt = bytes(a ^ b ^ c for a, b, c in zip(*survivors))
print("disk", lost, "rebuilt correctly:", rebuilt == disks[lost])"""),
md("""## 4 · Counting NAND gates

Everything can be built from NAND. But how many gates does it cost? Let's count by building with a function that records every call."""),
code("""calls = 0
def NAND(a, b):
    global calls
    calls += 1
    return 1 - (a & b)

def NOT(a): return NAND(a, a)
def AND(a, b): n = NAND(a, b); return NAND(n, n)
def OR(a, b): return NAND(NAND(a, a), NAND(b, b))
def XOR(a, b): n = NAND(a, b); return NAND(NAND(a, n), NAND(b, n))

def full_adder(a, b, c):
    x = XOR(a, b)
    return XOR(x, c), OR(AND(a, b), AND(x, c))

for name, f, n in [("NOT", NOT, 1), ("AND", AND, 2), ("OR", OR, 2), ("XOR", XOR, 2), ("full adder", full_adder, 3)]:
    calls = 0
    f(*[1] * n)
    print(f"{name:<11} {calls:>2} NAND gates")"""),
md("""> This straightforward full adder costs 15 NAND gates; a careful design needs only 9. A 64-bit adder needs 64 of them.
> Shaving gates off one adder saves billions of transistors across a factory's production run."""),
md("""## 5 · How fast does brute force grow?

`solve` in `puzzles.py` tries every world: $2^n$ of them for $n$ islanders. Here is the same idea timed for growing $n$."""),
code("""import time
from itertools import product
import matplotlib.pyplot as plt

ns, secs = [], []
for n in range(4, 21, 2):
    t0 = time.perf_counter()
    count = sum(1 for w in product([True, False], repeat=n) if w[0] == (w.count(True) == 1))
    ns.append(n); secs.append(time.perf_counter() - t0)

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.semilogy(ns, secs, "o-", color="#e8560f")
ax.set_xlabel("islanders n"); ax.set_ylabel("seconds (log scale)")
ax.set_title("Brute force: a straight line on a log scale means exponential growth")
ax.grid(alpha=.3); plt.tight_layout(); plt.show()"""),
md("""## Your turn

1. In section 2, encrypt your own name. Then change one bit of the key and decrypt: what happens to the message?
2. In section 3, set `lost = 3` (the parity disk). Does the rebuild still work? Why?
3. Find a full adder with fewer NAND gates than section 4 (hint: reuse the `NAND(a, b)` inside XOR)."""),
]

# ---------------------------------------------------------------------------
# LAB 3 · Quantifiers in pandas and SQL
# ---------------------------------------------------------------------------
LAB03 = [
md("""# Lab 3 · Explore: ∀ and ∃ in pandas and in a real SQL database

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 3. Nothing here is graded. You will ask the **same questions** as in `quantifiers.py`,
first with a table library (pandas), then with a real SQL database. Watch how ∀ and ∃ show up everywhere."""),
md("""## 1 · The class as a table

The same ten fictional students as in `data.py`, written out here so the notebook also runs on its own."""),
code("""import pandas as pd

STUDENTS = [
    ("Ada", 2, "Python,C", True, 92), ("Bora", 1, "Python", True, 67), ("Cemre", 2, "Python,Java", True, 74),
    ("Doruk", 3, "Java,C,SQL", False, 58), ("Ece", 1, "C", True, 81), ("Fırat", 2, "Java", True, 49),
    ("Gizem", 4, "Python,SQL", True, 88), ("Hakan", 1, "", False, 55), ("Irmak", 3, "Python,Java,C", True, 95),
    ("Kaan", 2, "Python", False, 62),
]
df = pd.DataFrame(STUDENTS, columns=["name", "year", "langs", "github", "math"])
df["python"] = df.langs.str.contains("Python")
df["java"] = df.langs.str.contains("Java")
df"""),
md("""## 2 · ∀ and ∃ in pandas

A column of True/False values has `.all()` (∀) and `.any()` (∃)."""),
code("""print("Q1 ∀ github            :", df.github.all())
print("Q2 ∃ java              :", df.java.any())

second = df[df.year == 2]                         # the filter A(x): restrict the domain
print("Q3 ∀ (Y2 → Python)     :", second.python.all())
print("   counterexample      :", list(second[~second.python].name))

first = df[df.year == 1]
print("Q4 ¬∃ (Y1 ∧ fail)      :", not (first.math < 50).any())"""),
md("""> **Notice:** `df[df.year == 2]` *is* the golden rule. Keeping only the second-years and then asking `.all()`
> is exactly $\\forall x\\,(Y_2(x) \\to P(x))$: the people outside the filter can never break it."""),
md("""## 3 · The same questions in SQL

Python ships with a small database engine, SQLite. We load the class into a table and ask SQL."""),
code("""import sqlite3

db = sqlite3.connect(":memory:")
df.drop(columns=["langs"]).to_sql("students", db, index=False)

def ask(query):
    return db.execute(query).fetchone()[0]

print("Q2 ∃ java:", ask("SELECT EXISTS (SELECT * FROM students WHERE java)"))"""),
md("""SQL has **no FOR ALL**. To ask “does every second-year know Python?” a database uses De Morgan:
$\\forall x\\,(Y_2 \\to P) \\equiv \\neg\\exists x\\,(Y_2 \\land \\neg P)$, that is, *there is no second-year who does not know Python*."""),
code("""q3 = (
    "SELECT NOT EXISTS ("
    "  SELECT * FROM students"
    "  WHERE year = 2 AND NOT python"
    ")"
)
print("Q3 ∀ (Y2 → Python):", ask(q3))
print("who breaks it:", db.execute("SELECT name FROM students WHERE year = 2 AND NOT python").fetchall())"""),
md("""## 4 · The two classic mistakes, in data

The wrong translations from the week 4 notes give silly answers on real data too."""),
code("""wrong_and = (df.year.eq(2) & df.python).all()        # ∀x (Y2 ∧ P): "everyone is a 2nd-year who knows Python"
wrong_imp = ((~df.year.eq(2)) | df.python).any()     # ∃x (Y2 → P): true thanks to anyone who is not a 2nd-year
print("∀x (Y2 ∧ P) :", wrong_and)
print("∃x (Y2 → P) :", wrong_imp)"""),
md("""## 5 · Empty domains

What is “every student in year 5 has GitHub”? There are no year-5 students."""),
code("""fifth = df[df.year == 5]
print("rows       :", len(fifth))
print("∀ (.all()) :", fifth.github.all(), "  ← vacuously true: no counterexample exists")
print("∃ (.any()) :", fifth.github.any(), " ← false: no witness exists")"""),
md("""## 6 · Hunting for counterexamples

A claim about **all** integers can never be checked by a loop, but a loop can **hunt for a counterexample**.
The polynomial $n^2 - n + 41$ looks like it always gives a prime. Does it?"""),
code("""def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))

n = next(n for n in range(1000) if not is_prime(n * n - n + 41))
print(f"counterexample: n = {n},  n² - n + 41 = {n*n - n + 41} = 41 × {(n*n - n + 41)//41}")"""),
md("""> Every value from $n = 0$ to $n = 40$ gives a prime, then $n = 41$ breaks it. Checking examples can **disprove** a ∀ statement, never prove it.
> That is why week 7 is about proofs.

## Your turn

1. Ask in pandas **and** in SQL: “some first-year student knows C.”
2. Ask “every student with a GitHub account knows at least one language.” (Hint: `df.langs != ""`.)
3. Change one student in `STUDENTS` so that Q3 becomes true, and re-run sections 2 and 3."""),
]

# ---------------------------------------------------------------------------
# LAB 4 · Nested quantifiers on a network
# ---------------------------------------------------------------------------
LAB04 = [
md("""# Lab 4 · Explore: rows, columns, and how rare a celebrity is

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 4. Nothing here is graded. You will draw the network from `data.py`, look at the follow
relation as a grid of rows and columns, and run an experiment that shows how differently $\\forall x\\, \\exists y$ and
$\\exists y\\, \\forall x$ behave."""),
md("""## 1 · Draw the network

The same eight fictional people as in `data.py`. An arrow from $x$ to $y$ means “$x$ follows $y$”."""),
code("""import networkx as nx
import matplotlib.pyplot as plt

FOLLOWS = {
    "Ada": {"Bora"}, "Bora": {"Ada", "Can"}, "Can": {"Ada"}, "Defne": {"Ada", "Emir"},
    "Emir": {"Ada", "Defne"}, "Funda": {"Ada", "Gökay"}, "Gökay": {"Ada"}, "Hira": {"Ada"},
}
G = nx.DiGraph((x, y) for x, ys in FOLLOWS.items() for y in ys)

fig, ax = plt.subplots(figsize=(6, 4.5))
pos = nx.spring_layout(G, seed=3)
nx.draw_networkx(G, pos, ax=ax, node_color="#e8e8fc", edgecolors="#3a39d0", node_size=1100,
                 font_size=9, arrowsize=14, edge_color="#6c6e7f")
ax.set_axis_off(); plt.tight_layout(); plt.show()"""),
md("""Can you see the celebrity? Every arrow seems to point at one person."""),
md("""## 2 · The same relation as a grid

Row $x$, column $y$, and a dark cell when $x$ follows $y$. This is the picture from the week 5 page:
$\\forall x\\, \\exists y$ asks whether **every row** has a dark cell, $\\exists y\\, \\forall x$ whether **some column** is dark everywhere
(off the diagonal)."""),
code("""import numpy as np

names = list(FOLLOWS)
M = np.array([[1 if y in FOLLOWS[x] else 0 for y in names] for x in names])

fig, ax = plt.subplots(figsize=(5.5, 5))
ax.imshow(M, cmap="Blues", vmin=0, vmax=1.4)
ax.set_xticks(range(len(names)), names, rotation=45); ax.set_yticks(range(len(names)), names)
ax.set_xlabel("y  (is followed)"); ax.set_ylabel("x  (follows)")
for i in range(len(names)):
    for j in range(len(names)):
        ax.text(j, i, M[i, j], ha="center", va="center", fontsize=9, color="#15161d")
plt.tight_layout(); plt.show()

off = ~np.eye(len(names), dtype=bool)
print("∀x ∃y : every row has a 1     →", bool((M * off).any(axis=1).all()))
print("∃y ∀x : some column is full   →", bool(((M == 1) | ~off).all(axis=0).any()))"""),
md("""## 3 · An experiment: how often is each statement true?

Make random networks of 12 people where each possible follow exists with probability $p$.
For each $p$, count how often “everyone follows someone” ($\\forall x \\exists y$) and “there is a celebrity”
($\\exists y \\forall x$) are true."""),
code("""import random

def random_net(n, p, rng):
    return [[i != j and rng.random() < p for j in range(n)] for i in range(n)]

def forall_exists(F):
    return all(any(row) for row in F)

def exists_forall(F):
    n = len(F)
    return any(all(F[x][y] for x in range(n) if x != y) for y in range(n))

rng = random.Random(1)
ps = [i / 20 for i in range(1, 20)]
fe, ef = [], []
for p in ps:
    nets = [random_net(12, p, rng) for _ in range(400)]
    fe.append(sum(forall_exists(F) for F in nets) / 400)
    ef.append(sum(exists_forall(F) for F in nets) / 400)

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(ps, fe, "o-", color="#3a39d0", label="∀x ∃y  everyone follows someone")
ax.plot(ps, ef, "s-", color="#e8560f", label="∃y ∀x  there is a celebrity")
ax.set_xlabel("probability p that a given person follows another"); ax.set_ylabel("fraction of networks")
ax.legend(); ax.grid(alpha=.3); plt.tight_layout(); plt.show()"""),
md("""> The blue curve shoots up early: with even a modest number of follows, almost every network satisfies
> $\\forall x\\, \\exists y$. The orange curve stays near zero until $p$ is very large, because a celebrity needs
> **eleven** specific follows to all happen at once. This is the strong-versus-weak difference from the notes,
> measured. Notice also that orange is never above blue: $\\exists y\\, \\forall x$ always implies $\\forall x\\, \\exists y$."""),
md("""## 4 · Nested loops cost $n^2$

Checking a nested statement may look at every pair. Let's time `all(any(...))` on growing networks where the
answer is False only at the very end, so the loops cannot stop early."""),
code("""import time

sizes, secs = [], []
for n in [200, 400, 800, 1600]:
    F = [[False] * n for _ in range(n)]
    for x in range(n - 1):
        F[x][n - 1] = True          # everyone follows the last person, except the last person
    t0 = time.perf_counter()
    forall_exists(F)                 # False, but only discovered at the last row
    sizes.append(n); secs.append(time.perf_counter() - t0)

for n, s in zip(sizes, secs):
    print(f"n = {n:>5}: {s * 1000:7.1f} ms")
print("double n → roughly four times the work")"""),
md("""## Your turn

1. In section 1, remove Hira's follow of Ada (`"Hira": set()`). Which of Q1–Q6 change? Re-run sections 1 and 2 to see it.
2. In section 3, change 12 people to 6. Does the orange curve rise earlier? Explain why in one sentence.
3. Write `exists_forall` for the statement “someone follows everyone” and add it to the plot."""),
]

# ---------------------------------------------------------------------------
# LAB 5 · Watching an inference engine think
# ---------------------------------------------------------------------------
LAB05 = [
md("""# Lab 5 · Explore: watching an inference engine think

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 5. Nothing here is graded. We draw a rule base, watch forward chaining work pass by pass,
see how backward chaining branches out from a goal, and finish with a tiny resolution prover that proves the
canoe-trip argument from the notes by deriving a contradiction."""),
md("""## 1 · The course advisor as a picture

Each rule “if A and B then C” becomes arrows from its conditions to its conclusion. Starting facts are on the left."""),
code("""import networkx as nx
import matplotlib.pyplot as plt

RULES = [
    (("passed_math1",), "can_take_discrete"),
    (("passed_programming1", "can_take_discrete"), "can_take_algorithms"),
    (("can_take_algorithms",), "can_take_data_structures"),
    (("passed_math1", "passed_physics1"), "can_take_signals"),
    (("can_take_data_structures", "can_take_signals"), "can_take_ml"),
]
G = nx.DiGraph()
for conds, concl in RULES:
    for c in conds:
        G.add_edge(c, concl)

layers = {n: 0 for n in G if G.in_degree(n) == 0}
for n in nx.topological_sort(G):
    if n not in layers:
        layers[n] = 1 + max(layers[p] for p in G.predecessors(n))
nx.set_node_attributes(G, layers, "layer")
pos = nx.multipartite_layout(G, subset_key="layer")

fig, ax = plt.subplots(figsize=(10, 4.5))
nx.draw_networkx(G, pos, ax=ax, node_color=["#dcf3ea" if layers[n] == 0 else "#e8e8fc" for n in G],
                 edgecolors="#3a39d0", node_size=2600, font_size=7.5, arrowsize=14, edge_color="#6c6e7f")
ax.set_axis_off(); plt.tight_layout(); plt.show()"""),
md("""## 2 · Forward chaining, pass by pass

The same loop as in `forward_chain`, but it prints what each pass learns."""),
code("""def forward_trace(facts, rules):
    known = set(facts)
    step = 0
    while True:
        step += 1
        new = []
        for conds, concl in rules:
            if concl not in known and all(c in known for c in conds):
                known.add(concl)
                new.append(concl)
        print(f"pass {step}: {', '.join(new) if new else 'nothing new, stop'}")
        if not new:
            return known

forward_trace({"passed_math1", "passed_programming1", "passed_physics1"}, RULES);"""),
md("""Now the same rules in the **opposite** order. The result is identical, but it takes more passes, exactly as the
week 6 notes predicted."""),
code("""forward_trace({"passed_math1", "passed_programming1", "passed_physics1"}, RULES[::-1]);"""),
md("""## 3 · Backward chaining branches out from the goal

Backward chaining asks “what would I need?” and recurses. Printing each question with indentation shows the shape of
the search: a tree whose root is the goal and whose leaves are known facts."""),
code("""def backward_trace(goal, facts, rules, depth=0, visiting=frozenset()):
    pad = "    " * depth
    if goal in facts:
        print(f"{pad}{goal}  ✓ known fact")
        return True
    if goal in visiting:
        print(f"{pad}{goal}  ↺ loop, give up on this branch")
        return False
    for conds, concl in rules:
        if concl == goal:
            print(f"{pad}{goal}  ? try: {' and '.join(conds)}")
            if all(backward_trace(c, facts, rules, depth + 1, visiting | {goal}) for c in conds):
                print(f"{pad}{goal}  ✓ proved")
                return True
    print(f"{pad}{goal}  ✗ no rule works")
    return False

backward_trace("can_take_ml", {"passed_math1", "passed_programming1", "passed_physics1"}, RULES)"""),
md("""Try a student who never took Physics I: the search fails exactly at `passed_physics1`."""),
code("""backward_trace("can_take_ml", {"passed_math1", "passed_programming1"}, RULES)"""),
md("""## 4 · A resolution prover in fifteen lines

A **clause** is a set of literals such as `{"~p", "q"}` (meaning ¬p ∨ q). Resolution takes two clauses with a
complementary pair, like `p` and `~p`, and joins what is left. To prove a conclusion, add its **negation** to the
premises and resolve until the **empty clause** appears: then the premises and “not the conclusion” cannot all be
true, so the conclusion follows."""),
code("""from itertools import combinations

def neg(lit):
    return lit[1:] if lit.startswith("~") else "~" + lit

def resolve_all(clauses):
    clauses = {frozenset(c) for c in clauses}
    while True:
        new = set()
        for a, b in combinations(clauses, 2):
            for lit in a:
                if neg(lit) in b:
                    r = (a - {lit}) | (b - {neg(lit)})
                    if not r:
                        return True                   # empty clause: contradiction found
                    new.add(frozenset(r))
        if new <= clauses:
            return False                              # nothing new: no contradiction
        clauses |= new

# Canoe trip: ¬p ∧ q,  r → p,  ¬r → s,  s → t   ∴ t
premises = [{"~p"}, {"q"}, {"~r", "p"}, {"r", "s"}, {"~s", "t"}]
print("premises + ¬t contradictory?", resolve_all(premises + [{"~t"}]))   # True: so t follows
print("premises + t contradictory? ", resolve_all(premises + [{"t"}]))    # False: ¬t does not follow"""),
md("""> Notice how each rule became a clause: $r \\to p$ is $\\neg r \\lor p$, and $\\neg r \\to s$ is $r \\lor s$.
> The prover knows **only one rule**, resolution, and that is enough.

## Your turn

1. Add a rule of your own to `RULES` (for example a course that needs Signals) and re-run sections 1 and 2.
2. In section 3, remove the rule for `can_take_signals`. What does the trace print?
3. Use `resolve_all` to check the debugging argument from the notes: `a ∨ d`, `d → f`, `¬f`, therefore `a`."""),
]

# ---------------------------------------------------------------------------
# LAB 6 · Evidence, patterns and proof
# ---------------------------------------------------------------------------
LAB06 = [
md("""# Lab 6 · Explore: evidence, patterns and proof

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 6. Nothing here is graded. We look at famous patterns in pictures: where Euler's prime
polynomial hides in a spiral, why mathematicians believe Goldbach's conjecture without a proof, how wild the Collatz
sequences are, and how a modern testing tool hunts for counterexamples in your own code."""),
md("""## 1 · The Ulam spiral

Write 1, 2, 3, … in a square spiral and mark the primes. The mathematician Stanisław Ulam did this in 1963, doodling
during a boring talk, and noticed that primes like to sit on **diagonal lines**. Some of those diagonals are values of
quadratic polynomials, and Euler's $n^2 + n + 41$ produces one of the longest prime-rich diagonals of all."""),
code("""from math import isqrt
import matplotlib.pyplot as plt

def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))

def spiral(count):
    x = y = 0
    dx, dy = 1, 0
    pos, step, n = {}, 1, 1
    while n <= count:
        for _ in range(2):
            for _ in range(step):
                if n > count:
                    break
                pos[n] = (x, y)
                x, y, n = x + dx, y + dy, n + 1
            dx, dy = -dy, dx
        step += 1
    return pos

pos = spiral(40_000)
pts = [pos[n] for n in pos if is_prime(n)]
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(*zip(*pts), s=0.6, color="#3a39d0")
ax.set_aspect("equal"); ax.set_axis_off(); ax.set_title("Primes up to 40,000 on the Ulam spiral")
plt.show()"""),
md("""Now start the spiral at 41 instead of 1 and colour the values of $n^2 + n + 41$. They line up on one diagonal,
and the first forty of them are all prime."""),
code("""start = 41
pos = spiral(3000)
euler = {n * n + n + 41 for n in range(60)}
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(*zip(*[pos[k] for k in pos if is_prime(k + start - 1)]), s=6, color="#c9c6bb", label="prime")
ax.scatter(*zip(*[pos[k] for k in pos if (k + start - 1) in euler and is_prime(k + start - 1)]), s=18, color="#0e8a63", label="n²+n+41, prime")
ax.scatter(*zip(*[pos[k] for k in pos if (k + start - 1) in euler and not is_prime(k + start - 1)]), s=40, color="#d83a3f", marker="x", label="n²+n+41, NOT prime")
ax.set_aspect("equal"); ax.set_axis_off(); ax.legend(loc="lower left", fontsize=8)
plt.show()"""),
md("""## 2 · Goldbach's comet

Goldbach's conjecture says every even number $n > 2$ is a sum of two primes. For each even $n$, count **how many**
ways there are. If the conjecture were in danger, some counts would be creeping down towards 0. Instead they grow,
in a beautiful band called **Goldbach's comet**. This is strong evidence, and it is why almost every mathematician
believes the conjecture. It is still not a proof."""),
code("""N = 20_000
P = [is_prime(k) for k in range(N + 1)]
evens = list(range(4, N + 1, 2))
ways = [sum(1 for p in range(2, n // 2 + 1) if P[p] and P[n - p]) for n in evens]

fig, ax = plt.subplots(figsize=(9, 4))
ax.scatter(evens, ways, s=0.4, color="#7a3fc4")
ax.set_xlabel("even n"); ax.set_ylabel("number of ways n = p + q, p ≤ q")
ax.set_title("Goldbach's comet")
plt.show()
print("smallest number of ways for n > 1000:", min(w for n, w in zip(evens, ways) if n > 1000))"""),
md("""## 3 · Collatz: simple rule, wild behaviour

Even: halve it. Odd: $3n + 1$. Starting from 27, the sequence climbs to 9,232 before it finally falls to 1.
Computers have checked every starting number up to about $2.95 \\times 10^{20}$; nobody has a proof that they all reach 1."""),
code("""def collatz(n):
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq

s = collatz(27)
print(len(s) - 1, "steps, highest value", max(s))
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(s, color="#e8560f", lw=1.2)
ax.set_xlabel("step"); ax.set_title("The Collatz sequence of 27")
plt.show()"""),
code("""steps = [len(collatz(n)) - 1 for n in range(1, 10_001)]
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.scatter(range(1, 10_001), steps, s=0.4, color="#0c7c77")
ax.set_xlabel("starting number n"); ax.set_ylabel("steps to reach 1")
plt.show()"""),
md("""## 4 · A tiny property-based tester

Tools such as Python's *Hypothesis* test a **property** that should hold for all inputs: they generate random inputs,
look for a counterexample, and then **shrink** it to the smallest failing input they can find. Here is the idea in a
few lines. The property below is false; can you see why before running the cell?"""),
code("""import random

def prop(a, b):
    # claim: sorting a joined list is the same as joining two sorted lists
    return sorted(a + b) == sorted(a) + sorted(b)

def shrink(a, b):
    changed = True
    while changed:
        changed = False
        for lst in (a, b):
            for i in range(len(lst)):
                trial = lst[:i] + lst[i + 1:]
                cand = (trial, b) if lst is a else (a, trial)
                if not prop(*cand):
                    a, b = cand
                    changed = True
                    break
            if changed:
                break
    return a, b

rng = random.Random(1)
for attempt in range(1, 1001):
    a = [rng.randint(0, 9) for _ in range(rng.randint(0, 6))]
    b = [rng.randint(0, 9) for _ in range(rng.randint(0, 6))]
    if not prop(a, b):
        print(f"attempt {attempt}: counterexample a = {a}, b = {b}")
        print("shrunk to                  :", shrink(a, b))
        break"""),
md("""The shrunk counterexample is the kind a programmer can understand at a glance: one number in each list, the larger one in `a`, such as `a = [9], b = [7]`.
That is exactly what you did by hand with $n^2 + n + 41$: one small, clear case that breaks the claim.

## 5 · Your own code

This cell uses your `hunt.py` (run it in your lab repository after you have written the functions)."""),
code("""from hunt import streak, first_counterexample, euler_poly, goldbach_other, two_ways_cubes

print("Euler's streak       :", streak(euler_poly))
print("Goldbach's other     :", first_counterexample(goldbach_other, 1, 10_000))
print("taxicab numbers      :", [two_ways_cubes(50_000, s) for s in (1, 1730, 4105)])""", skip=True),
md("""## Your turn

1. In section 1, try the polynomial $n^2 - n + 41$ or $2n^2 + 29$. Do they line up too? How long are their prime streaks?
2. In section 2, plot only the even numbers that are multiples of 3 (in a different colour). What do you notice?
3. In section 4, write a property of your own that you think is true for all lists (for example about `reversed`, `max`
   or `set`). Does the tester find a counterexample?"""),
]

# ---------------------------------------------------------------------------
# LAB 7 · Sets in pictures
# ---------------------------------------------------------------------------
LAB07 = [
md("""# Lab 7 · Explore: sets in pictures

**Discrete Mathematics (YMT211)** · Fall 2026

The playground half of Lab 7. Nothing here is graded. We draw set identities, watch the power set explode,
let Jaccard similarity discover groups of listeners nobody told it about, catch a copied paragraph, and see why
computers love to store sets as bits."""),
md("""## 1 · Identities you can see

A Venn diagram is a picture of membership: every point of the plane is in or out of each circle. So we can draw any
set expression by colouring the points that belong to it. Below, De Morgan's law: the two pictures are the same,
and the wrong version is not."""),
code("""import numpy as np
import matplotlib.pyplot as plt

xs, ys = np.meshgrid(np.linspace(-2.2, 2.2, 400), np.linspace(-1.6, 1.6, 300))
A = (xs + 0.6) ** 2 + ys ** 2 < 1.1 ** 2
B = (xs - 0.6) ** 2 + ys ** 2 < 1.1 ** 2

def draw(ax, region, title):
    ax.imshow(region, extent=(-2.2, 2.2, -1.6, 1.6), cmap="Blues", vmin=0, vmax=1.6, origin="lower")
    for cx in (-0.6, 0.6):
        ax.add_patch(plt.Circle((cx, 0), 1.1, fill=False, lw=1.5))
    ax.text(-1.6, 1.2, "A", fontsize=13, weight="bold"); ax.text(1.45, 1.2, "B", fontsize=13, weight="bold")
    ax.set_title(title); ax.set_axis_off()

fig, axs = plt.subplots(1, 3, figsize=(12, 3.4))
draw(axs[0], ~(A | B), "(A ∪ B)′")
draw(axs[1], ~A & ~B, "A′ ∩ B′   (the same!)")
draw(axs[2], ~A | ~B, "A′ ∪ B′   (a different set)")
plt.show()"""),
md("""The arrays `A` and `B` hold one boolean per pixel, and NumPy's `|`, `&` and `~` act on every pixel at once:
they are exactly ∪, ∩ and complement. The same operators work on Python sets."""),
md("""## 2 · The power set explodes

Every subset of $\\{0, 1, \\dots, n-1\\}$ is a bit pattern, so the subsets are just the numbers $0, 1, \\dots, 2^n - 1$
written in binary. That makes listing them easy, and it also shows why it quickly becomes hopeless."""),
code("""def subsets(n):
    for mask in range(2 ** n):
        yield {i for i in range(n) if mask >> i & 1}

print([sorted(s) for s in subsets(3)])

import time
ns, secs = [], []
for n in range(10, 21):
    t = time.perf_counter()
    for _ in subsets(n):
        pass
    ns.append(n); secs.append(time.perf_counter() - t)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(ns, secs, "o-", color="#e8560f")
ax.set_xlabel("n (elements)"); ax.set_ylabel("seconds to list P(S)")
ax.set_title("Each new element doubles the work")
plt.show()
print(f"at this speed, n = 60 would take about {secs[-1] * 2 ** 40 / 3.15e7:,.0f} years")"""),
md("""## 3 · Jaccard finds the groups

We invent 30 listeners. Each one secretly belongs to one of three taste groups and picks most artists from that
group's list, plus a few random ones. Then we compute the Jaccard similarity of every pair and draw it as a picture.
Jaccard is never told about the groups, yet three bright blocks appear."""),
code("""import random
rng = random.Random(7)
groups = {
    "rock": ["Duman", "Mor ve Ötesi", "Coldplay", "Muse", "Radiohead", "Arctic Monkeys", "Foo Fighters", "Linkin Park"],
    "pop": ["Tarkan", "Sezen Aksu", "Adele", "Taylor Swift", "Dua Lipa", "Ed Sheeran", "Hande Yener", "Kenan Doğulu"],
    "electronic": ["Daft Punk", "Avicii", "Deadmau5", "Kygo", "Calvin Harris", "Aphex Twin", "Moby", "Röyksopp"],
}
everyone = sorted({a for g in groups.values() for a in g})
users = {}
for i in range(30):
    g = list(groups)[i // 10]
    users[f"u{i:02d}"] = set(rng.sample(groups[g], 5)) | set(rng.sample(everyone, 2))

def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0

names = list(users)
M = np.array([[jaccard(users[a], users[b]) for b in names] for a in names])
fig, ax = plt.subplots(figsize=(5.5, 5))
im = ax.imshow(M, cmap="viridis")
ax.set_title("Jaccard similarity of 30 listeners"); ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, shrink=0.8)
plt.show()"""),
code("""def recommend(u):
    best = max((v for v in users if v != u), key=lambda v: jaccard(users[u], users[v]))
    return best, round(jaccard(users[u], users[best]), 2), sorted(users[best] - users[u])

for u in ["u00", "u15", "u27"]:
    print(u, "→", recommend(u))"""),
md("""## 4 · Catching a copied paragraph

A paragraph becomes a set of **shingles**: runs of 3 consecutive words. Small edits change only a few shingles,
so a lightly reworded copy still shares many of them, while an honest paragraph on the same topic shares almost none."""),
code("""import re

def shingles(text, k=3):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(w[i:i + k]) for i in range(len(w) - k + 1)}

texts = {
    "original": "A set is an unordered collection of distinct objects called elements. Two sets are equal "
                "when they have exactly the same elements, no matter how they are described.",
    "reworded": "A set is an unordered collection of different objects called members. Two sets are equal "
                "when they have exactly the same elements, however they are described.",
    "honest":   "We say two sets coincide if each element of the first belongs to the second and vice versa; "
                "order and repetition play no role at all.",
}
for k in (1, 2, 3, 4):
    print(f"k = {k}:", {n: round(jaccard(shingles(texts['original'], k), shingles(t, k)), 2) for n, t in texts.items()})"""),
md("""With $k = 1$ (single words) the honest paragraph still gets a few points, just because everyone writes *sets*,
*the* and *of*. From $k = 3$ on it scores exactly 0, while the reworded copy keeps a clear score. Make $k$ too large,
though, and every small edit breaks many shingles, so even the copy starts to look original. Choosing $k$ is a real
engineering decision in plagiarism checkers and search engines."""),
md("""## 5 · Sets as bits are fast

For a small universe, a set can be one Python integer whose bit $i$ says whether $i$ is in the set.
Then intersection is a single `&` on two integers."""),
code("""import timeit
N = 100_000
A_set = set(range(0, N, 2)); B_set = set(range(0, N, 3))
A_bits = sum(1 << i for i in A_set); B_bits = sum(1 << i for i in B_set)

t_set = timeit.timeit(lambda: A_set & B_set, number=50) / 50
t_bits = timeit.timeit(lambda: A_bits & B_bits, number=50) / 50
print(f"set  intersection: {t_set * 1e6:8.1f} µs   -> {len(A_set & B_set)} elements")
print(f"bits intersection: {t_bits * 1e6:8.1f} µs   -> {(A_bits & B_bits).bit_count()} elements")
print(f"the bit version is about {t_set / t_bits:.0f} times faster")"""),
md("""## 6 · Your own code

This cell uses your `sets_lab.py` (run it in your lab repository after you have written the functions)."""),
code("""from sets_lab import power_set, first_difference, counterexample_sets, recommend as my_recommend

print(len(power_set(set(range(10)))), "subsets of a 10-element set")
print(first_difference(lambda a, b, c: a and not (b and not c), lambda a, b, c: (a and not b) and not c, 3))
print(counterexample_sets(lambda a, b: not (a and b), lambda a, b: (not a) and (not b), 2))
print(my_recommend("u00", users))""", skip=True),
md("""## Your turn

1. In section 1, draw $A \\oplus B$ (use `A ^ B`) and $(A - B) \\cup (B - A)$. Then add a third circle $C$ and draw
   both sides of the distributive law $A \\cap (B \\cup C) = (A \\cap B) \\cup (A \\cap C)$.
2. In section 3, make the listeners pick 3 random artists instead of 2. How much noise can the blocks survive?
3. In section 4, write a fourth paragraph that copies the original but changes every third word. Which $k$ still
   catches it?"""),
]

NOTEBOOKS = {
    "lab01": (ROOT / "labs" / "templates" / "lab01" / "lab01.ipynb", LAB01),
    "lab02": (ROOT / "labs" / "templates" / "lab02" / "lab02.ipynb", LAB02),
    "lab03": (ROOT / "labs" / "templates" / "lab03" / "lab03.ipynb", LAB03),
    "lab04": (ROOT / "labs" / "templates" / "lab04" / "lab04.ipynb", LAB04),
    "lab05": (ROOT / "labs" / "templates" / "lab05" / "lab05.ipynb", LAB05),
    "lab06": (ROOT / "labs" / "templates" / "lab06" / "lab06.ipynb", LAB06),
    "lab07": (ROOT / "labs" / "templates" / "lab07" / "lab07.ipynb", LAB07),
}

SKIP_TAG = "skip-execution"


def build(path, cells, force=False):
    if path.exists() and not force:
        print(f"· {path.relative_to(ROOT)} exists, kept")
        return
    nb = new_notebook(cells=cells, metadata={
        "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
        "language_info": {"name": "python"},
        "colab": {"name": path.name, "toc_visible": True},
    })
    nbformat.write(nb, path)
    print(f"✓ {path.relative_to(ROOT)} written")


def execute(path):
    from nbclient import NotebookClient
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=300, kernel_name="python3", allow_errors=True,
                            skip_cells_with_tag=SKIP_TAG, resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    errs = [o for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
    print(f"✓ {path.name} executed ({len(errs)} error cells)")
    return nb


CSS = """<style>
  body{background:#fff !important;margin:0}
  .jp-Notebook{padding:16px 20px !important;max-width:100% !important}
  .jp-Cell{padding:0 !important}
  .jp-InputArea-editor{border-radius:10px;border:1px solid #e1dfd7}
  .jp-RenderedHTMLCommon{font-family:Geist,system-ui,sans-serif;color:#15161d}
  .jp-RenderedHTMLCommon table{font-size:13px}
</style></head>"""


def to_html(name, path, nb=None):
    from nbconvert import HTMLExporter
    exp = HTMLExporter(template_name="lab")
    exp.exclude_input_prompt = True
    exp.exclude_output_prompt = True
    body, _ = exp.from_notebook_node(nb) if nb is not None else exp.from_filename(str(path))
    body = body.replace("</head>", CSS, 1)
    out = OUT_DIR / f"{name}.html"
    out.write_text(body, encoding="utf-8")
    print(f"✓ {out.relative_to(ROOT)} ({len(body) // 1024} KB)")


def main():
    force = "--force" in sys.argv
    run = "--execute" in sys.argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, (path, cells) in NOTEBOOKS.items():
        build(path, cells, force)
        nb = execute(path) if run else None
        to_html(name, path, nb)


if __name__ == "__main__":
    main()
