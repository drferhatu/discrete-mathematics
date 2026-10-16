"""Tests for Lab 4 (network.py). Run them with:  python check.py"""
import ast
import inspect
import random
from itertools import product

import pytest

import network as n

SUM4 = lambda x, y: x + y == 4
LE = lambda x, y: x <= y
LT = lambda x, y: x < y


def calls_in(fn):
    tree = ast.parse(inspect.getsource(fn)).body[0]
    return {c.func.id for c in ast.walk(tree) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}


def implemented(fn):
    return not any(isinstance(x, ast.Raise) for x in ast.walk(ast.parse(inspect.getsource(fn))))


def random_cases(seed, count=60):
    rng = random.Random(seed)
    for _ in range(count):
        D = rng.sample(range(-3, 6), rng.randint(0, 5))
        k = rng.randint(-2, 6)
        yield D, (lambda x, y, k=k: x + y == k), (lambda x, y, k=k: (x * y) % 3 == k % 3)


# Part A ---------------------------------------------------------------------

def test_forall_exists_examples():
    """forall_exists: [1,2,3] with x+y=4 → True, [1,2] → False"""
    assert n.forall_exists([1, 2, 3], SUM4) is True
    assert n.forall_exists([1, 2], SUM4) is False


def test_exists_forall_examples():
    """exists_forall: some x ≤ every y → True, some x < every y → False"""
    assert n.exists_forall([1, 2, 3], LE) is True
    assert n.exists_forall([1, 2, 3], LT) is False


def test_same_kind_quantifiers():
    """forall_forall and exists_exists on small examples"""
    assert n.forall_forall([1, 2], lambda x, y: x + y > 0) is True
    assert n.forall_forall([1, 2], lambda x, y: x < y) is False
    assert n.exists_exists([1, 2], lambda x, y: x < y) is True
    assert n.exists_exists([1, 2], lambda x, y: x + y > 10) is False


def test_part_a_random():
    """the four shapes agree with a brute-force check on 60 random cases"""
    for D, P, Q in random_cases(1):
        for R in (P, Q):
            assert n.forall_forall(D, R) == all(R(x, y) for x, y in product(D, D)), f"forall_forall on {D}"
            assert n.exists_exists(D, R) == any(R(x, y) for x, y in product(D, D)), f"exists_exists on {D}"
            assert n.forall_exists(D, R) == all(any(R(x, y) for y in D) for x in D), f"forall_exists on {D}"
            assert n.exists_forall(D, R) == any(all(R(x, y) for y in D) for x in D), f"exists_forall on {D}"


def test_order_matters():
    """∀x∃y and ∃x∀y really differ (x + y = 4 on [1, 2, 3])"""
    assert n.forall_exists([1, 2, 3], SUM4) is True and n.exists_forall([1, 2, 3], SUM4) is False


# Part B ---------------------------------------------------------------------

def test_witnesses():
    """witnesses gives each x its first witness y, or None"""
    assert n.witnesses([1, 2, 3], SUM4) == {1: 3, 2: 2, 3: 1}
    assert n.witnesses([1, 2], SUM4) == {1: None, 2: 2}
    assert n.witnesses([], SUM4) == {}


def test_first_failure():
    """first_failure is the first x with no witness, or None"""
    assert n.first_failure([1, 2], SUM4) == 1
    assert n.first_failure([1, 2, 3], SUM4) is None
    assert n.first_failure([2, 5, 9], SUM4) == 5


# Part C ---------------------------------------------------------------------

def expected(net):
    P = list(net)
    F = lambda x, y: y in net[x]
    unret = next(((x, y) for x in P for y in P if F(x, y) and not F(y, x)), None)
    return {
        "everyone_follows_someone": all(any(x != y and F(x, y) for y in P) for x in P),
        "celebrity": next((y for y in P if all(x == y or F(x, y) for x in P)), None),
        "someone_follows_everyone": any(all(x == y or F(x, y) for y in P) for x in P),
        "all_mutual": unret is None,
        "first_unreturned": unret,
        "loners": [x for x in P if all(not F(x, y) and not F(y, x) for y in P)],
    }


def test_questions_on_our_network():
    """Q1–Q6 are right for the network in data.py"""
    assert n.everyone_follows_someone() is True, "Q1"
    assert n.celebrity() == "Ada", "Q2: everyone else follows Ada"
    assert n.someone_follows_everyone() is False, "Q3"
    assert n.all_mutual() is False, "Q4"
    assert n.first_unreturned() == ("Bora", "Can"), "Q5: Bora follows Can, Can does not follow back"
    assert n.loners() == [], "Q6"


OTHER = {
    "two-friends": {"A": {"B"}, "B": {"A"}},
    "star": {"S": set(), "A": {"S"}, "B": {"S"}, "C": {"S", "A"}},
    "fan-and-loner": {"F": {"A", "B"}, "A": {"B"}, "B": {"A"}, "L": set()},
    "empty-follows": {"X": set(), "Y": set()},
    "cycle": {"P": {"Q"}, "Q": {"R"}, "R": {"P"}},
}


@pytest.mark.parametrize("name", list(OTHER))
def test_questions_on_other_networks(name):
    """Q1–Q6 also work on other networks (no hard-coded answers)"""
    net = OTHER[name]
    for fn, want in expected(net).items():
        got = getattr(n, fn)(net)
        assert got == want, f"{fn} on the '{name}' network should be {want!r}, got {got!r}"


# Part D ---------------------------------------------------------------------

def test_not_forall_exists_value():
    """not_forall_exists equals ¬∀x∃y on 60 random cases"""
    for D, P, _ in random_cases(2):
        assert n.not_forall_exists(D, P) == (not all(any(P(x, y) for y in D) for x in D)), f"on {D}"


def test_negation_uses_the_rule():
    """not_forall_exists uses exists_forall (∃x∀y¬P), not forall_exists"""
    assert implemented(n.not_forall_exists), "not implemented yet"
    used = calls_in(n.not_forall_exists)
    assert "exists_forall" in used and "forall_exists" not in used, "write it as exists_forall(D, <not P>)"


# Part E ---------------------------------------------------------------------

def test_is_sorted():
    """is_sorted: [], [5], [1, 3, 3] sorted; [2, 1] not"""
    assert n.is_sorted([]) and n.is_sorted([5]) and n.is_sorted([1, 3, 3])
    assert not n.is_sorted([2, 1]) and not n.is_sorted([1, 3, 2])


def test_keeps_values():
    """keeps_values is ∀i ∃j (a[i] = b[j])"""
    assert n.keeps_values([3, 3, 1], [1, 3, 5]) is True
    assert n.keeps_values([3, 2], [3, 3]) is False
    assert n.keeps_values([], [7]) is True


def test_is_correct_sort():
    """is_correct_sort catches [3,3,1] → [1,3,5] and accepts the real answer"""
    assert n.is_correct_sort([3, 3, 1], [1, 3, 3]) is True
    assert n.is_correct_sort([3, 3, 1], [1, 3, 5]) is False, "a 3 was lost and a 5 appeared"
    assert n.is_correct_sort([3, 3, 1], [3, 3, 1]) is False, "not sorted"
    assert n.is_correct_sort([2, 1], [1, 2, 2]) is False, "an extra 2 appeared"
    rng = random.Random(4)
    for _ in range(40):
        a = [rng.randint(0, 5) for _ in range(rng.randint(0, 6))]
        assert n.is_correct_sort(a, sorted(a)) is True, f"sorted({a}) should be accepted"
