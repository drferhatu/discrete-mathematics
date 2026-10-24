"""Tests for Lab 5 (inference.py). Run them with:  python check.py"""
import random

import pytest

import inference as e

IMP = lambda a, b: (not a) or b


def ref_reasons(facts, rules):
    """reference: forward chaining with reasons, rules in order, new facts usable in the same pass"""
    why = {f: None for f in facts}
    changed = True
    while changed:
        changed = False
        for i, (cond, concl) in enumerate(rules):
            if concl not in why and all(c in why for c in cond):
                why[concl] = i
                changed = True
    return why


def random_kb(seed):
    rng = random.Random(seed)
    atoms = [f"f{i}" for i in range(9)]
    rules = [(tuple(rng.sample(atoms, rng.randint(1, 3))), rng.choice(atoms)) for _ in range(rng.randint(3, 10))]
    facts = set(rng.sample(atoms, rng.randint(0, 3)))
    return facts, rules, atoms


# Part A ---------------------------------------------------------------------

def test_valid_rules():
    """modus ponens, modus tollens and hypothetical syllogism are valid"""
    assert e.is_valid([lambda p, q: p, lambda p, q: IMP(p, q)], lambda p, q: q, 2)
    assert e.is_valid([lambda p, q: not q, lambda p, q: IMP(p, q)], lambda p, q: not p, 2)
    assert e.is_valid([lambda p, q, r: IMP(p, q), lambda p, q, r: IMP(q, r)], lambda p, q, r: IMP(p, r), 3)


def test_fallacies():
    """affirming the conclusion and denying the hypothesis are invalid, with the right counterexample"""
    assert e.counterexample([lambda p, q: IMP(p, q), lambda p, q: q], lambda p, q: p, 2) == (False, True)
    assert e.counterexample([lambda p, q: IMP(p, q), lambda p, q: not p], lambda p, q: not q, 2) == (False, True)
    assert e.is_valid([lambda p, q: IMP(p, q), lambda p, q: q], lambda p, q: p, 2) is False


def test_canoe_trip():
    """the canoe trip argument from the notes is valid"""
    prem = [lambda p, q, r, s, t: (not p) and q, lambda p, q, r, s, t: IMP(r, p),
            lambda p, q, r, s, t: IMP(not r, s), lambda p, q, r, s, t: IMP(s, t)]
    assert e.is_valid(prem, lambda p, q, r, s, t: t, 5)
    assert e.counterexample(prem, lambda p, q, r, s, t: t, 5) is None


def test_inconsistent_premises():
    """from inconsistent premises (p and not p) every conclusion is valid"""
    assert e.is_valid([lambda p, q: p, lambda p, q: not p], lambda p, q: q, 2)


# Part B ---------------------------------------------------------------------

def test_can_fire():
    """can_fire needs all conditions and a NEW conclusion"""
    assert e.can_fire((("a", "b"), "c"), {"a", "b"}) is True
    assert e.can_fire((("a", "b"), "c"), {"a"}) is False
    assert e.can_fire((("a",), "c"), {"a", "c"}) is False


def test_forward_chain_example():
    """forward_chain follows a chain a → b → c and does not change its input"""
    facts = {"a"}
    out = e.forward_chain(facts, [(("a",), "b"), (("b",), "c")])
    assert out == {"a", "b", "c"}
    assert facts == {"a"}, "forward_chain must not modify the facts it receives"


def test_forward_chain_needs_several_passes():
    """forward_chain keeps going when the rules are listed in the 'wrong' order"""
    rules = [(("c",), "d"), (("b",), "c"), (("a",), "b")]
    assert e.forward_chain({"a"}, rules) == {"a", "b", "c", "d"}


def test_forward_chain_random():
    """forward_chain finds exactly the derivable facts in 40 random knowledge bases"""
    for seed in range(40):
        facts, rules, _ = random_kb(seed)
        assert e.forward_chain(set(facts), rules) == set(ref_reasons(facts, rules)), f"knowledge base #{seed}"


# Part C ---------------------------------------------------------------------

def test_reasons_example():
    """reasons records the rule that first added each fact"""
    assert e.reasons({"a"}, [(("a",), "b"), (("b",), "c")]) == {"a": None, "b": 0, "c": 1}


def test_reasons_random():
    """reasons matches the reference on 40 random knowledge bases"""
    for seed in range(40):
        facts, rules, _ = random_kb(seed)
        assert e.reasons(set(facts), rules) == ref_reasons(facts, rules), f"knowledge base #{seed}"


def test_explain():
    """explain lists what is needed, in a derivable order, ending with the goal"""
    rules = [(("a",), "b"), (("b", "x"), "c"), (("a",), "x")]
    assert e.explain("c", {"a"}, rules) == ["a", "b", "x", "c"]
    assert e.explain("a", {"a"}, rules) == ["a"]
    assert e.explain("zzz", {"a"}, rules) is None


def test_explain_no_duplicates():
    """explain never lists a fact twice"""
    rules = [(("a",), "b"), (("a", "b"), "c")]
    assert e.explain("c", {"a"}, rules) == ["a", "b", "c"]


# Part D ---------------------------------------------------------------------

def test_backward_chain_examples():
    """backward_chain proves chains and handles loops"""
    assert e.backward_chain("c", {"a"}, [(("a",), "b"), (("b",), "c")]) is True
    assert e.backward_chain("x", {"a"}, [(("x",), "y"), (("y",), "x")]) is False
    assert e.backward_chain("x", {"a"}, [(("x",), "y"), (("y",), "x"), (("a",), "y")]) is True


def test_backward_agrees_with_forward():
    """backward_chain agrees with forward chaining on every fact of 40 random knowledge bases"""
    for seed in range(40):
        facts, rules, atoms = random_kb(seed)
        known = set(ref_reasons(facts, rules))
        for goal in atoms:
            assert e.backward_chain(goal, set(facts), rules) == (goal in known), f"goal {goal} in knowledge base #{seed}"


# Part E ---------------------------------------------------------------------

STUDENTS = {
    "everything": ({"passed_math1", "passed_programming1", "passed_physics1"},
                   {"can_take_discrete", "can_take_algorithms", "can_take_data_structures", "can_take_signals", "can_take_ml"}),
    "math only": ({"passed_math1"}, {"can_take_discrete"}),
    "math and physics": ({"passed_math1", "passed_physics1"}, {"can_take_discrete", "can_take_signals"}),
    "programming only": ({"passed_programming1"}, set()),
    "no physics": ({"passed_math1", "passed_programming1"}, {"can_take_discrete", "can_take_algorithms", "can_take_data_structures"}),
    "nothing": (set(), set()),
}


@pytest.mark.parametrize("who", list(STUDENTS))
def test_advisor(who):
    """the advisor rules give the right courses for each student"""
    start, can = STUDENTS[who]
    got = {f for f in e.forward_chain(set(start), e.advisor_rules()) if f.startswith("can_take")}   # a copy: never let a test change the fixtures
    assert got == can, f"a student with {sorted(start) or 'nothing'} can take {sorted(can) or 'nothing'}, your rules give {sorted(got)}"
