"""Tests for Lab 2, part 2 (puzzles.py). Run them with:  python check.py"""
import puzzles as z

K, N = True, False


def test_solve_example():
    """solve finds the single world of the docstring example"""
    st = {"A": lambda w: w["B"], "B": lambda w: w["A"] != w["B"]}
    assert z.solve(["A", "B"], st) == [{"A": N, "B": N}]


def test_solve_order_and_silent_people():
    """solve lists every consistent world in order; silent people are free"""
    st = {"A": lambda w: w["A"]}            # "I am a knight": true for both kinds
    assert z.solve(["A", "B"], st) == [{"A": K, "B": K}, {"A": K, "B": N}, {"A": N, "B": K}, {"A": N, "B": N}]
    assert z.solve(["A"], {"A": lambda w: not w["A"]}) == []   # "I am a knave": impossible


def test_puzzle_1():
    """puzzle 1: both are knaves"""
    assert z.solve(["A", "B"], z.puzzle_1()) == [{"A": N, "B": N}]


def test_puzzle_2():
    """puzzle 2: A is a knight, B is a knave"""
    assert z.solve(["A", "B"], z.puzzle_2()) == [{"A": K, "B": N}]


def test_puzzle_3():
    """puzzle 3: only B is a knight"""
    assert z.solve(["A", "B", "C"], z.puzzle_3()) == [{"A": N, "B": K, "C": N}]


def test_satisfying_row():
    """satisfying_row returns the first row that satisfies all, or None"""
    assert z.satisfying_row([lambda p, q: p or q, lambda p, q: not p], 2) == (False, True)
    assert z.satisfying_row([lambda p: p, lambda p: not p], 1) is None
    assert z.satisfying_row([], 2) == (True, True)


def test_login_requirements_each():
    """each login requirement has the right truth table"""
    r1, r2, r3, r4 = z.login_requirements()
    imp = lambda a, b: (not a) or b
    for p in (K, N):
        for q in (K, N):
            for r in (K, N):
                assert bool(r1(p, q, r)) == imp(q, p), f"requirement 1 at p={p}, q={q}, r={r}"
                assert bool(r2(p, q, r)) == imp(r, not q), f"requirement 2 at p={p}, q={q}, r={r}"
                assert bool(r3(p, q, r)) == imp(p, q), f"requirement 3 at p={p}, q={q}, r={r}"
                assert bool(r4(p, q, r)) == (p and r), f"requirement 4 at p={p}, q={q}, r={r}"


def test_login_consistency():
    """requirements 1–3 are consistent, adding 4 makes them inconsistent"""
    reqs = z.login_requirements()
    assert z.satisfying_row(reqs[:3], 3) == (True, True, False)
    assert z.satisfying_row(reqs, 3) is None
