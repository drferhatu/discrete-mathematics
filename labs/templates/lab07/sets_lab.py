"""
Lab 7 · Sets and a Mini Recommender
Discrete Mathematics (YMT211) · Fall 2026

Week 8 in code. Fill in every function marked TODO, one at a time, top to bottom.
Check yourself with:  python check.py

Rules
- Do not change function names or parameters: the autograder calls them by name.
- Use only the standard library, and do NOT import itertools: building the power set and the
  Cartesian product yourself is the point of Part A.
"""

import re


# ---------------------------------------------------------------------------
# Part A · Building sets from sets
# ---------------------------------------------------------------------------

def power_set(s) -> set:
    """
    The power set P(s): the set of ALL subsets of s, including the empty set and s itself.
    A Python set cannot contain ordinary sets, so return a set of frozensets.

    power_set({1, 2}) → {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})}
    power_set(set())  → {frozenset()}                 (P(∅) = {∅} has one element)

    Idea: start with {∅}. For each element x of s, every subset found so far gives two
    subsets: one without x and one with x. (That is why |P(s)| doubles with each element.)
    """
    # TODO
    raise NotImplementedError


def cartesian(a, b) -> set:
    """
    The Cartesian product a × b: the set of all ordered pairs (x, y) with x in a and y in b.

    cartesian({1, 2}, {"x", "y"}) → {(1, "x"), (1, "y"), (2, "x"), (2, "y")}
    cartesian({1, 2}, set())      → set()
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · Sets as bit strings
# ---------------------------------------------------------------------------

def to_bits(subset, universe) -> str:
    """
    Encode a subset of the universe as a bit string. `universe` is a LIST, so it fixes an order:
    character i is "1" if universe[i] is in the subset, and "0" otherwise.

    to_bits({1, 3, 5}, [1, 2, 3, 4, 5])          → "10101"
    to_bits(set(), ["a", "b"])                    → "00"
    """
    # TODO
    raise NotImplementedError


def from_bits(bits, universe) -> set:
    """
    The opposite of to_bits: the set of universe[i] for every position i where bits has a "1".

    from_bits("10101", [1, 2, 3, 4, 5])           → {1, 3, 5}
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Membership tables: proving and breaking set identities
#
# A set expression in A, B, C is written as a Python function of k booleans, one per set,
# which says whether an element with that membership is in the result:
#     A ∩ B        →  lambda a, b: a and b
#     (A ∪ B)′     →  lambda a, b: not (a or b)
#     A − (B − C)  →  lambda a, b, c: a and not (b and not c)
# ---------------------------------------------------------------------------

def build(f, sets, universe) -> set:
    """
    Turn an expression into an actual set: all x in the universe for which
    f(x in sets[0], x in sets[1], ...) is True.

    U = {1, ..., 10}, A = {1, 2, 3}, B = {3, 4}
    build(lambda a, b: a and not b, [A, B], U)    → {1, 2}          (A − B)
    build(lambda a: not a, [A], U)                → {4, 5, ..., 10} (complement of A)
    """
    # TODO
    raise NotImplementedError


def membership_table(f, k) -> list:
    """
    The membership table of an expression in k sets, as a list of 2**k rows. Each row is a tuple of
    k + 1 integers: the k memberships (1 = in, 0 = not in), then the value of f for that row.
    Rows go in the textbook order, from all ones down to all zeros.

    membership_table(lambda a, b: a and b, 2)
      → [(1, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 0)]
    """
    # TODO
    raise NotImplementedError


def first_difference(f, g, k):
    """
    Compare two expressions in k sets row by row, in membership-table order.
    Return the memberships of the FIRST row where they differ, as a tuple of k ints (0/1),
    or None if they agree on every row (then f = g is a set identity).

    first_difference(lambda a, b: not (a or b), lambda a, b: (not a) and (not b), 2) → None
    first_difference(lambda a, b: not (a and b), lambda a, b: (not a) and (not b), 2) → (1, 0)
    """
    # TODO
    raise NotImplementedError


def counterexample_sets(f, g, k):
    """
    Turn a failed identity into a concrete counterexample: k actual sets for which build(f, ...)
    and build(g, ...) differ. Use a single element, 1: put it into set i exactly when the
    differing row has a 1 in position i. Return a list of k sets, or None if f = g is an identity.

    counterexample_sets(lambda a, b: a and not b, lambda a, b: a, 2)  → [{1}, {1}]
      (A − B = A fails for A = {1}, B = {1}: then A − B = ∅ but A = {1})
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · Jaccard similarity and a course recommender
# ---------------------------------------------------------------------------

def jaccard(a, b) -> float:
    """
    The Jaccard similarity |a ∩ b| / |a ∪ b|, a number from 0 to 1.
    By convention two empty sets are identical: jaccard(set(), set()) → 1.0

    jaccard({1, 2, 3}, {2, 3, 4}) → 0.5
    """
    # TODO
    raise NotImplementedError


def most_similar(user, profiles):
    """
    profiles maps each student's name to the set of courses they liked.
    Return the name of the OTHER student whose set is most similar to `user`'s (by Jaccard).
    If several are equally similar, return the one that comes first alphabetically.
    Return None if there is no other student.
    """
    # TODO
    raise NotImplementedError


def recommend(user, profiles) -> list:
    """
    Recommend to `user` everything the most similar student liked that `user` has not:
    the set difference  profiles[best] − profiles[user],  returned as a SORTED list.
    Return [] if there is no other student.
    """
    # TODO
    raise NotImplementedError


def shingles(text, k=3) -> set:
    """
    The set of k-shingles of a text: every run of k consecutive words, as a tuple.
    Words are the lowercase runs of letters, digits and apostrophes (use the regular expression
    r"[a-z0-9']+" on text.lower()). A text with fewer than k words has no shingles.

    shingles("The cat sat on the mat", 3)
      → {("the", "cat", "sat"), ("cat", "sat", "on"), ("sat", "on", "the"), ("on", "the", "mat")}
    """
    # TODO
    raise NotImplementedError


def text_similarity(t1, t2, k=3) -> float:
    """How alike are two texts? The Jaccard similarity of their k-shingle sets."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Try it:  python sets_lab.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("P({a, b, c}) has", len(power_set({"a", "b", "c"})), "subsets")
    print("{1, 2} × {x, y} =", sorted(cartesian({1, 2}, {"x", "y"})))
    print("{1, 3, 5} as bits over 1..10:", to_bits({1, 3, 5}, list(range(1, 11))))

    de_morgan = (lambda a, b: not (a or b), lambda a, b: (not a) and (not b))
    wrong = (lambda a, b: not (a and b), lambda a, b: (not a) and (not b))
    print("De Morgan, first difference      :", first_difference(*de_morgan, 2))
    print("wrong De Morgan, first difference:", first_difference(*wrong, 2))
    print("  counterexample sets A, B       :", counterexample_sets(*wrong, 2))

    profiles = {
        "Ayşe": {"Algorithms", "Databases", "Discrete Math", "Machine Learning"},
        "Mert": {"Databases", "Discrete Math", "Web Programming"},
        "Elif": {"Algorithms", "Discrete Math", "Machine Learning", "Computer Vision"},
    }
    print("most similar to Ayşe:", most_similar("Ayşe", profiles))
    print("recommend to Ayşe   :", recommend("Ayşe", profiles))
    a = "Sets are unordered collections of distinct objects called elements"
    b = "Sets are unordered collections of different objects called members"
    print("text similarity     :", round(text_similarity(a, b), 3))
