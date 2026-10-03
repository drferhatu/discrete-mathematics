"""
Lab 2 · Part 2: Knights, Knaves and Consistent Requirements
Discrete Mathematics (YMT211) · Fall 2026

Here truth values are Python booleans (True / False).
Fill in every function marked TODO. Check yourself with:  python check.py
"""

from itertools import product


# ---------------------------------------------------------------------------
# Part E · A Knights and Knaves solver
#
# On the island, knights always tell the truth and knaves always lie.
# A "world" is a dict that says who is a knight:  {"A": True, "B": False}  means A is a knight, B a knave.
# A statement is a function of the world that returns True or False, e.g.
#     lambda w: w["B"]                 # "B is a knight"
#     lambda w: w["A"] != w["B"]       # "We are of opposite types"
#
# Key idea from the lecture: a speaker is a knight IF AND ONLY IF what they say is true.
# ---------------------------------------------------------------------------

def solve(people: list[str], statements: dict) -> list[dict]:
    """
    Return every world consistent with the statements, as a list of dicts.
    Try the worlds in the order of itertools.product([True, False], repeat=len(people)).
    People who say nothing are not constrained.

    solve(["A", "B"], {"A": lambda w: w["B"], "B": lambda w: w["A"] != w["B"]})
        == [{"A": False, "B": False}]
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part F · Write the puzzles as statements
# Each function returns the `statements` dict for its puzzle (keys are the speakers).
# ---------------------------------------------------------------------------

def puzzle_1() -> dict:
    """People A, B.   A says: "B is a knight."   B says: "The two of us are of opposite types." """
    # TODO
    raise NotImplementedError


def puzzle_2() -> dict:
    """People A, B.   A says: "At least one of us is a knave."   (B says nothing.)"""
    # TODO
    raise NotImplementedError


def puzzle_3() -> dict:
    """
    People A, B, C.
    A says: "All three of us are knaves."
    B says: "Exactly one of us is a knight."
    (C says nothing.)
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part G · Are these requirements consistent?
# p: the user is authenticated   q: access is granted   r: the account is locked
# ---------------------------------------------------------------------------

def satisfying_row(formulas: list, n: int):
    """
    Return the FIRST row (tuple of n booleans, order of product([True, False], repeat=n))
    that makes EVERY formula in the list true, or None if there is none (inconsistent).
    """
    # TODO
    raise NotImplementedError


def login_requirements() -> list:
    """
    Return the four requirements from the week 3 notes, in this order, as functions of (p, q, r):
      1. Access is granted only if the user is authenticated.
      2. If the account is locked, access is not granted.
      3. Authenticated users are granted access.
      4. Some authenticated user has a locked account   (read it as: p and r).
    """
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    for i, puzzle in enumerate([puzzle_1, puzzle_2, puzzle_3], start=1):
        people = sorted({"A", "B", "C"} if i == 3 else {"A", "B"})
        print(f"puzzle {i}:", solve(people, puzzle()))
    reqs = login_requirements()
    print("requirements 1–3 consistent:", satisfying_row(reqs[:3], 3))
    print("requirements 1–4 consistent:", satisfying_row(reqs, 3))
