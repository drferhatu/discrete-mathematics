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

NOTEBOOKS = {
    "lab01": (ROOT / "labs" / "templates" / "lab01" / "lab01.ipynb", LAB01),
    "lab02": (ROOT / "labs" / "templates" / "lab02" / "lab02.ipynb", LAB02),
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
