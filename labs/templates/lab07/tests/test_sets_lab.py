"""Tests for Lab 7 (sets_lab.py). Run them with:  python check.py"""
import ast
import random
from pathlib import Path

import sets_lab as s

U10 = set(range(1, 11))


def all_subsets(xs):
    """reference power set, by bit masks"""
    xs = list(xs)
    return {frozenset(x for i, x in enumerate(xs) if m >> i & 1) for m in range(2 ** len(xs))}


# Part A ---------------------------------------------------------------------

def test_power_set_examples():
    """power_set gives every subset, including ∅ and the set itself, as frozensets"""
    assert s.power_set({1, 2}) == {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})}
    assert s.power_set(set()) == {frozenset()}, "P(∅) = {∅}: one element, the empty set"
    p = s.power_set({"a", "b", "c"})
    assert frozenset() in p, "the empty set is a subset of every set"
    assert frozenset({"a", "b", "c"}) in p, "every set is a subset of itself"
    assert all(isinstance(x, frozenset) for x in p), "return a set of frozensets"


def test_power_set_sizes():
    """|P(S)| = 2^n for n = 0 to 12, and power_set agrees with a reference"""
    for n in range(13):
        S = set(range(n))
        assert len(s.power_set(S)) == 2 ** n, f"P of a {n}-element set should have {2 ** n} subsets"
    rng = random.Random(8)
    for _ in range(5):
        S = set(rng.sample("abcdefghijklmnopqrstuvwxyz", rng.randint(1, 8)))
        assert s.power_set(S) == all_subsets(S)


def test_power_set_does_not_change_input():
    """power_set leaves its argument unchanged"""
    S = {1, 2, 3}
    s.power_set(S)
    assert S == {1, 2, 3}


def test_cartesian():
    """cartesian gives ordered pairs (x from a, y from b), |a × b| = |a|·|b|, without itertools"""
    assert s.cartesian({1, 2}, {"x", "y"}) == {(1, "x"), (1, "y"), (2, "x"), (2, "y")}
    assert s.cartesian({1, 2}, set()) == set(), "A × ∅ = ∅"
    assert s.cartesian(set(), {1}) == set()
    assert ("x", 1) not in s.cartesian({1, 2}, {"x", "y"}), "order matters: the first element comes from a"
    A, B = set(range(7)), set("abcde")
    assert len(s.cartesian(A, B)) == 35
    assert s.cartesian(A, B) == {(a, b) for a in A for b in B}
    assert s.cartesian({1, 2}, {3}) != s.cartesian({3}, {1, 2}), "A × B ≠ B × A in general"
    # Part A is built by hand: sets_lab.py may not import itertools
    tree = ast.parse(Path(s.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(a.name.split(".")[0] != "itertools" for a in node.names), "do not import itertools"
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] != "itertools", "do not import itertools"


# Part B ---------------------------------------------------------------------

def test_to_bits():
    """to_bits follows the order of the universe list"""
    assert s.to_bits({1, 3, 5}, [1, 2, 3, 4, 5]) == "10101"
    assert s.to_bits({1, 3, 5, 7, 9}, list(range(1, 11))) == "1010101010"
    assert s.to_bits(set(), ["a", "b"]) == "00"
    assert s.to_bits({"a"}, ["b", "a", "c"]) == "010", "use the order of the list, not sorted order"


def test_from_bits():
    """from_bits decodes a bit string, and undoes to_bits for every subset"""
    assert s.from_bits("10101", [1, 2, 3, 4, 5]) == {1, 3, 5}
    assert s.from_bits("000", ["a", "b", "c"]) == set()
    assert s.from_bits("011", ["b", "a", "c"]) == {"a", "c"}
    universe = ["p", "q", "r", "s", "t", "u"]
    for sub in all_subsets(universe):
        assert s.from_bits(s.to_bits(set(sub), universe), universe) == set(sub)


# Part C ---------------------------------------------------------------------

def test_build_examples():
    """build turns an expression into the actual set"""
    A, B = {1, 2, 3}, {3, 4}
    assert s.build(lambda a, b: a and not b, [A, B], U10) == {1, 2}
    assert s.build(lambda a: not a, [A], U10) == set(range(4, 11))
    assert s.build(lambda a, b: a or b, [A, B], U10) == {1, 2, 3, 4}
    assert s.build(lambda a: True, [A], set()) == set(), "an empty universe gives the empty set"


def test_build_random():
    """build agrees with Python's set operators on random sets"""
    rng = random.Random(7)
    U = set(range(40))
    for _ in range(50):
        A, B, C = (set(rng.sample(sorted(U), rng.randint(0, 25))) for _ in range(3))
        assert s.build(lambda a, b, c: (a or b) and not c, [A, B, C], U) == (A | B) - C
        assert s.build(lambda a, b, c: a != b, [A, B, C], U) == A ^ B
        assert s.build(lambda a, b, c: not (a and c), [A, B, C], U) == U - (A & C)


def test_membership_table_two():
    """membership_table for two sets, rows from 11 down to 00"""
    assert s.membership_table(lambda a, b: a and b, 2) == [(1, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 0)]
    assert s.membership_table(lambda a, b: a or b, 2) == [(1, 1, 1), (1, 0, 1), (0, 1, 1), (0, 0, 0)]
    assert s.membership_table(lambda a: not a, 1) == [(1, 0), (0, 1)]


def test_membership_table_three():
    """membership_table for three sets: 8 rows in textbook order, values as 0/1"""
    t = s.membership_table(lambda a, b, c: a or (b and c), 3)
    assert [r[:3] for r in t] == [(1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1), (0, 0, 0)]
    assert [r[3] for r in t] == [1, 1, 1, 1, 1, 0, 0, 0]
    assert all(len(r) == 4 for r in t)
    assert len(s.membership_table(lambda a, b, c, d: a, 4)) == 16


IDENTITIES = [
    ("De Morgan (union)", lambda a, b: not (a or b), lambda a, b: (not a) and (not b), 2),
    ("De Morgan (intersection)", lambda a, b: not (a and b), lambda a, b: (not a) or (not b), 2),
    ("difference", lambda a, b: a and not b, lambda a, b: a and (not b), 2),
    ("distributive", lambda a, b, c: a and (b or c), lambda a, b, c: (a and b) or (a and c), 3),
    ("distributive (union)", lambda a, b, c: a or (b and c), lambda a, b, c: (a or b) and (a or c), 3),
    ("absorption", lambda a, b: a or (a and b), lambda a, b: a, 2),
    ("symmetric difference", lambda a, b: a != b, lambda a, b: (a and not b) or (b and not a), 2),
]

TRAPS = [
    ("wrong De Morgan", lambda a, b: not (a and b), lambda a, b: (not a) and (not b), 2, (1, 0)),
    ("(A − B) ∪ B = A", lambda a, b: (a and not b) or b, lambda a, b: a, 2, (0, 1)),
    ("A − (B − C) = (A − B) − C", lambda a, b, c: a and not (b and not c), lambda a, b, c: (a and not b) and not c, 3, (1, 1, 1)),
    ("A ∪ (B ∩ C) = (A ∪ B) ∩ C", lambda a, b, c: a or (b and c), lambda a, b, c: (a or b) and c, 3, (1, 1, 0)),
]


def test_first_difference_identities():
    """first_difference is None for true identities"""
    for name, f, g, k in IDENTITIES:
        assert s.first_difference(f, g, k) is None, f"{name} is an identity: expected None"


def test_first_difference_traps():
    """first_difference finds the first row (in table order) where a false identity fails"""
    for name, f, g, k, row in TRAPS:
        got = s.first_difference(f, g, k)
        assert got == row, f"{name}: the first differing row is {row}, got {got}"


def test_counterexample_sets():
    """counterexample_sets gives actual sets that break a false identity, and None for a true one"""
    assert s.counterexample_sets(lambda a, b: a and not b, lambda a, b: a, 2) == [{1}, {1}]
    for name, f, g, k, row in TRAPS:
        sets = s.counterexample_sets(f, g, k)
        assert sets == [{1} if bit else set() for bit in row], f"{name}: wrong sets {sets}"
        assert s.build(f, sets, {1}) != s.build(g, sets, {1}), f"{name}: these sets do not break the identity"
    for name, f, g, k in IDENTITIES:
        assert s.counterexample_sets(f, g, k) is None, f"{name} is an identity: expected None"


# Part D ---------------------------------------------------------------------

def test_jaccard():
    """jaccard = |a ∩ b| / |a ∪ b|, with jaccard(∅, ∅) = 1"""
    assert s.jaccard({1, 2, 3}, {2, 3, 4}) == 0.5
    assert s.jaccard({1, 2}, {1, 2}) == 1.0
    assert s.jaccard({1}, {2}) == 0.0
    assert s.jaccard(set(), {1, 2}) == 0.0
    assert s.jaccard(set(), set()) == 1.0, "two empty sets: return 1.0 instead of dividing by zero"
    rng = random.Random(3)
    for _ in range(100):
        a, b = set(rng.sample(range(30), rng.randint(0, 12))), set(rng.sample(range(30), rng.randint(1, 12)))
        assert abs(s.jaccard(a, b) - len(a & b) / len(a | b)) < 1e-12
        assert s.jaccard(a, b) == s.jaccard(b, a)


PROFILES = {
    "Ayşe": {"Algorithms", "Databases", "Discrete Math", "Machine Learning"},
    "Mert": {"Databases", "Discrete Math", "Web Programming"},
    "Elif": {"Algorithms", "Discrete Math", "Machine Learning", "Computer Vision"},
    "Can": {"Networks", "Operating Systems"},
}


def test_most_similar():
    """most_similar picks the other student with the highest Jaccard similarity"""
    assert s.most_similar("Ayşe", PROFILES) == "Elif"     # 3/5 beats Mert's 2/5
    assert s.most_similar("Mert", PROFILES) == "Ayşe"     # 2/5 beats Elif's 1/6
    assert s.most_similar("Can", {**PROFILES, "Can": {"Networks"}, "Deniz": {"Networks", "Security"}}) == "Deniz"
    assert s.most_similar("Solo", {"Solo": {"x"}}) is None, "no other student: None"


def test_most_similar_ties_and_self():
    """most_similar never returns the user, and breaks ties alphabetically"""
    tie = {"Zeynep": {1, 2}, "Bora": {1}, "Arda": {2}}
    assert s.most_similar("Zeynep", tie) == "Arda", "Arda and Bora tie at 0.5: pick the first name alphabetically"
    twins = {"Selin": {1, 2}, "Kerem": {1, 2}, "Lina": {3}}
    assert s.most_similar("Selin", twins) == "Kerem", "the user is always similar to themselves: skip them"


def test_recommend():
    """recommend returns, sorted, what the most similar student liked and the user has not"""
    assert s.recommend("Ayşe", PROFILES) == ["Computer Vision"]
    assert s.recommend("Mert", PROFILES) == ["Algorithms", "Machine Learning"]
    assert s.recommend("Solo", {"Solo": {"x"}}) == []
    twins = {"Selin": {1, 2}, "Kerem": {1, 2}, "Lina": {3}}
    assert s.recommend("Selin", twins) == [], "the most similar student has nothing new: recommend nothing"


def test_shingles():
    """shingles: runs of k lowercase words, as tuples"""
    assert s.shingles("The cat sat on the mat", 3) == {
        ("the", "cat", "sat"), ("cat", "sat", "on"), ("sat", "on", "the"), ("on", "the", "mat")}
    assert s.shingles("Hello, world!", 3) == set(), "fewer than k words: no shingles"
    assert s.shingles("To be, or not to be", 1) == {("to",), ("be",), ("or",), ("not",)}
    assert s.shingles("It's TIME. it's time", 2) == {("it's", "time"), ("time", "it's")}
    assert s.shingles("a b c d") == {("a", "b", "c"), ("b", "c", "d")}, "k defaults to 3"


def test_text_similarity():
    """text_similarity compares the shingle sets of two texts"""
    t = "Sets are unordered collections of distinct objects"
    assert s.text_similarity(t, t.upper()) == 1.0
    assert s.text_similarity("one two three four", "one two three five") == 1 / 3
    assert s.text_similarity("a b c", "x y z") == 0.0
    assert s.text_similarity("one two three four", "one two three five", k=1) == 3 / 5
