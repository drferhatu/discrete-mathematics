"""Tests for Lab 2, part 1 (circuits.py). Run them with:  python check.py"""
import ast
import inspect
from itertools import product

import pytest

import circuits as c

BITS2 = list(product([1, 0], repeat=2))
BITS3 = list(product([1, 0], repeat=3))


def body_nodes(fn):
    """AST nodes of a function body, without its docstring."""
    tree = ast.parse(inspect.getsource(fn)).body[0]
    body = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
    return [x for n in body for x in ast.walk(n)]


# Part A ---------------------------------------------------------------------

@pytest.mark.parametrize("gate,rule", [
    ("AND", lambda a, b: a & b), ("OR", lambda a, b: a | b),
    ("XOR", lambda a, b: a ^ b), ("NAND", lambda a, b: 1 - (a & b)),
], ids=["AND", "OR", "XOR", "NAND"])
def test_gate(gate, rule):
    """the gate matches its truth table and returns 0/1"""
    for a, b in BITS2:
        got = getattr(c, gate)(a, b)
        assert got in (0, 1) and got == rule(a, b), f"{gate}({a}, {b}) should be {rule(a, b)}, got {got!r}"


def test_not():
    """NOT(1) == 0 and NOT(0) == 1"""
    assert c.NOT(1) == 0 and c.NOT(0) == 1


# Part B ---------------------------------------------------------------------

def test_counterexample_found():
    """counterexample finds the first differing row of p→q vs q→p"""
    imp = lambda p, q: c.OR(c.NOT(p), q)
    conv = lambda p, q: c.OR(c.NOT(q), p)
    assert c.counterexample(imp, conv, 2) == (1, 0)


def test_counterexample_none():
    """counterexample is None for De Morgan (they are equivalent)"""
    f = lambda p, q: c.NOT(c.AND(p, q))
    g = lambda p, q: c.OR(c.NOT(p), c.NOT(q))
    assert c.counterexample(f, g, 2) is None


def test_equivalent():
    """equivalent: distributive law holds, (p→q)→r ≢ p→(q→r)"""
    imp = lambda a, b: c.OR(c.NOT(a), b)
    assert c.equivalent(lambda p, q, r: c.OR(p, c.AND(q, r)), lambda p, q, r: c.AND(c.OR(p, q), c.OR(p, r)), 3)
    assert not c.equivalent(lambda p, q, r: imp(imp(p, q), r), lambda p, q, r: imp(p, imp(q, r)), 3)


# Part C ---------------------------------------------------------------------

def test_half_adder():
    """half_adder returns (sum, carry) for all four inputs"""
    for a, b in BITS2:
        assert tuple(c.half_adder(a, b)) == ((a + b) % 2, (a + b) // 2), f"half_adder({a}, {b})"


def test_full_adder():
    """full_adder returns (sum, carry_out) for all eight inputs"""
    for a, b, k in BITS3:
        t = a + b + k
        assert tuple(c.full_adder(a, b, k)) == (t % 2, t // 2), f"full_adder({a}, {b}, {k}) should be {(t % 2, t // 2)}"


def test_adders_use_gates_not_arithmetic():
    """half_adder and full_adder use gates, not + - // %"""
    for fn in (c.half_adder, c.full_adder):
        nodes = body_nodes(fn)
        calls = [n for n in nodes if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id in {"AND", "OR", "XOR", "NOT", "NAND", "half_adder"}]
        assert calls, f"{fn.__name__} does not call any gate yet"
        ops = [n for n in nodes if isinstance(n, (ast.BinOp, ast.AugAssign))]
        assert not ops, f"{fn.__name__} uses arithmetic; build it from the gate functions"


@pytest.mark.parametrize("x,y,expected", [
    ("1011", "0110", "10001"), ("0011", "0001", "0100"), ("1", "1", "10"),
    ("0", "0", "0"), ("1111", "1", "10000"), ("101", "11", "1000"),
])
def test_add_binary_examples(x, y, expected):
    """add_binary gives the right bits, including the final carry"""
    assert c.add_binary(x, y) == expected, f"add_binary({x!r}, {y!r})"


def test_add_binary_all_4bit():
    """add_binary is correct for all 256 pairs of 4-bit numbers"""
    for a in range(16):
        for b in range(16):
            got = c.add_binary(format(a, "04b"), format(b, "04b"))
            assert int(got, 2) == a + b and len(got) == (5 if a + b > 15 else 4), f"{a} + {b} gave {got}"


# Part D ---------------------------------------------------------------------

@pytest.mark.parametrize("name,rule", [
    ("nand_and", lambda a, b: a & b), ("nand_or", lambda a, b: a | b), ("nand_xor", lambda a, b: a ^ b),
], ids=["nand_and", "nand_or", "nand_xor"])
def test_nand_gates(name, rule):
    """the NAND-only gate matches its truth table"""
    for a, b in BITS2:
        assert getattr(c, name)(a, b) == rule(a, b), f"{name}({a}, {b})"


def test_nand_not():
    """nand_not inverts its input"""
    assert c.nand_not(1) == 0 and c.nand_not(0) == 1


@pytest.mark.parametrize("name", ["nand_not", "nand_and", "nand_or", "nand_xor"])
def test_only_nand(name):
    """the function uses only NAND calls"""
    nodes = body_nodes(getattr(c, name))
    assert any(isinstance(n, ast.Call) for n in nodes), f"{name} does not call NAND yet"
    for n in nodes:
        if isinstance(n, ast.Call):
            assert isinstance(n.func, ast.Name) and n.func.id == "NAND", f"{name} calls something other than NAND"
        assert not isinstance(n, (ast.BoolOp, ast.UnaryOp, ast.BinOp, ast.Compare, ast.IfExp, ast.If)), \
            f"{name} uses an operator or condition; use only NAND"
