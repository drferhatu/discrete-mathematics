"""Tests for Lab 3 (quantifiers.py). Run them with:  python check.py"""
import ast
import inspect
import random

import pytest

import quantifiers as q

EVEN = lambda n: n % 2 == 0
BIG = lambda n: n > 2


def calls_in(fn):
    """names of the functions called inside fn (docstring ignored)"""
    tree = ast.parse(inspect.getsource(fn)).body[0]
    return {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}


def implemented(fn):
    return not any(isinstance(n, ast.Raise) for n in ast.walk(ast.parse(inspect.getsource(fn))))


def random_domains(seed=0, count=60):
    rng = random.Random(seed)
    for _ in range(count):
        yield [rng.randint(-5, 9) for _ in range(rng.randint(0, 7))]


# Part A ---------------------------------------------------------------------

def test_for_all_examples():
    """for_all: [2, 4, 6] all even → True, [2, 3, 6] → False, [] → True"""
    assert q.for_all([2, 4, 6], EVEN) is True
    assert q.for_all([2, 3, 6], EVEN) is False
    assert q.for_all([], lambda n: False) is True, "an empty domain has no counterexample, so ∀ is True"


def test_exists_examples():
    """exists: [1, 3, 4] has an even number → True, [1, 3, 5] → False, [] → False"""
    assert q.exists([1, 3, 4], EVEN) is True
    assert q.exists([1, 3, 5], EVEN) is False
    assert q.exists([], lambda n: True) is False, "an empty domain has no witness, so ∃ is False"


def test_for_all_stops_early():
    """for_all stops at the first counterexample"""
    seen = []
    q.for_all([1, 2, 3, 4], lambda n: seen.append(n) or n < 2)
    assert seen == [1, 2], f"for_all looked at {seen}; it should stop right after 2"


def test_exists_stops_early():
    """exists stops at the first witness"""
    seen = []
    q.exists([1, 2, 3, 4], lambda n: seen.append(n) or n >= 2)
    assert seen == [1, 2], f"exists looked at {seen}; it should stop right after 2"


def test_part_a_writes_its_own_loops():
    """for_all and exists use a loop, not all() or any()"""
    for fn in (q.for_all, q.exists):
        assert implemented(fn), f"{fn.__name__} is not implemented yet"
        used = calls_in(fn) & {"all", "any"}
        assert not used, f"{fn.__name__} uses {used}; write the loop yourself"


def test_counterexample_and_witness():
    """counterexample and witness return the FIRST such element, or None"""
    assert q.counterexample([2, 3, 5], EVEN) == 3
    assert q.counterexample([2, 4], EVEN) is None
    assert q.witness([1, 3, 4, 6], EVEN) == 4
    assert q.witness([1, 3], EVEN) is None


def test_part_a_random():
    """Part A agrees with Python's all()/any() on 60 random domains"""
    for d in random_domains(1):
        assert q.for_all(d, EVEN) == all(EVEN(x) for x in d), f"for_all on {d}"
        assert q.exists(d, EVEN) == any(EVEN(x) for x in d), f"exists on {d}"
        assert q.counterexample(d, EVEN) == next((x for x in d if not EVEN(x)), None), f"counterexample on {d}"
        assert q.witness(d, EVEN) == next((x for x in d if EVEN(x)), None), f"witness on {d}"


# Part B ---------------------------------------------------------------------

def test_every_such_that():
    """every_such_that is ∀x (A(x) → B(x))"""
    assert q.every_such_that([1, 2, 3, 4], BIG, EVEN) is False
    assert q.every_such_that([1, 2, 4], BIG, EVEN) is True
    assert q.every_such_that([1, 2], BIG, EVEN) is True, "no element passes the filter: vacuously True"


def test_some_such_that():
    """some_such_that is ∃x (A(x) ∧ B(x))"""
    assert q.some_such_that([1, 2, 3, 4], BIG, EVEN) is True
    assert q.some_such_that([1, 2, 3], BIG, EVEN) is False
    assert q.some_such_that([1, 2], BIG, lambda n: True) is False, "no element passes the filter: False"


def test_part_b_random():
    """Part B is correct on 60 random domains"""
    for d in random_domains(2):
        assert q.every_such_that(d, BIG, EVEN) == all((not BIG(x)) or EVEN(x) for x in d), f"every_such_that on {d}"
        assert q.some_such_that(d, BIG, EVEN) == any(BIG(x) and EVEN(x) for x in d), f"some_such_that on {d}"


# Part C ---------------------------------------------------------------------

def S(name, year, langs, github, math):
    return {"name": name, "year": year, "langs": set(langs), "github": github, "math": math}


OTHER_CLASSES = [
    [S("A", 2, ["Python"], True, 70), S("B", 1, ["Java"], True, 80), S("C", 2, ["Python", "C"], True, 51)],
    [S("D", 1, [], False, 30), S("E", 2, ["C"], True, 90), S("F", 3, ["Java"], True, 45)],
    [S("G", 4, ["SQL"], True, 99)],
    [],
]


def expected(cls):
    y2_no_py = [s["name"] for s in cls if s["year"] == 2 and "Python" not in s["langs"]]
    return {
        "everyone_has_github": all(s["github"] for s in cls),
        "someone_knows_java": any("Java" in s["langs"] for s in cls),
        "every_second_year_knows_python": not y2_no_py,
        "no_first_year_failed_math": not any(s["year"] == 1 and s["math"] < 50 for s in cls),
        "who_breaks_q3": y2_no_py[0] if y2_no_py else None,
    }


def test_q_on_our_class():
    """Q1–Q5 give the right answers for the class in data.py"""
    assert q.everyone_has_github() is False, "Q1: Doruk, Hakan and Kaan have no GitHub account"
    assert q.someone_knows_java() is True, "Q2"
    assert q.every_second_year_knows_python() is False, "Q3"
    assert q.no_first_year_failed_math() is True, "Q4: first-years Bora, Ece and Hakan all have 50 or more"
    assert q.who_breaks_q3() == "Fırat", "Q5: should return the student's name"


@pytest.mark.parametrize("i", range(len(OTHER_CLASSES)), ids=["class-1", "class-2", "class-3", "empty"])
def test_q_on_other_classes(i):
    """Q1–Q5 also work for other classes (no hard-coded answers)"""
    cls = OTHER_CLASSES[i]
    for name, want in expected(cls).items():
        got = getattr(q, name)(cls)
        assert got == want, f"{name} on {[s['name'] for s in cls]} should be {want!r}, got {got!r}"


# Part D ---------------------------------------------------------------------

def test_not_all_and_not_any_values():
    """not_all and not_any have the right values on 60 random domains"""
    for d in random_domains(3):
        assert q.not_all(d, EVEN) == (not all(EVEN(x) for x in d)), f"not_all on {d}"
        assert q.not_any(d, EVEN) == (not any(EVEN(x) for x in d)), f"not_any on {d}"


def test_de_morgan_is_used():
    """not_all uses exists (∃¬) and not_any uses for_all (∀¬)"""
    assert implemented(q.not_all) and implemented(q.not_any), "not implemented yet"
    a, b = calls_in(q.not_all), calls_in(q.not_any)
    assert "exists" in a and "for_all" not in a, "not_all should be  exists(domain, <not P>)"
    assert "for_all" in b and "exists" not in b, "not_any should be  for_all(domain, <not P>)"
