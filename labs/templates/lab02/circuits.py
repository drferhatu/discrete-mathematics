"""
Lab 2 · Part 1: Gates, Equivalence and Adders
Discrete Mathematics (YMT211) · Fall 2026

In this file a bit is the integer 1 (true) or 0 (false), like a wire in a circuit.
Fill in every function marked TODO. Check yourself with:  python check.py

Rules
- Do not change function names or parameters: the autograder calls them by name.
- Part C must be built from the gate functions of Part A (no +, -, //, % on bits).
- Part D must use ONLY the NAND function (no and/or/not, no other gates, no operators).
"""

from itertools import product


# ---------------------------------------------------------------------------
# Part A · Logic gates on bits (0 or 1)
# ---------------------------------------------------------------------------

def NOT(a: int) -> int:
    """1 → 0, 0 → 1"""
    # TODO
    raise NotImplementedError


def AND(a: int, b: int) -> int:
    """1 only when both inputs are 1."""
    # TODO
    raise NotImplementedError


def OR(a: int, b: int) -> int:
    """1 when at least one input is 1."""
    # TODO
    raise NotImplementedError


def XOR(a: int, b: int) -> int:
    """1 when the inputs differ."""
    # TODO
    raise NotImplementedError


def NAND(a: int, b: int) -> int:
    """NOT of AND."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · Equivalence by brute force
# A formula is a function of n bits that returns a bit, e.g.  lambda p, q: OR(NOT(p), q)
# ---------------------------------------------------------------------------

def counterexample(f, g, n: int):
    """
    Return the FIRST row (a tuple of n bits, rows in the order of
    itertools.product([1, 0], repeat=n)) where f and g give different outputs,
    or None if they agree on every row.

    counterexample(lambda p, q: OR(NOT(p), q), lambda p, q: OR(NOT(q), p), 2) == (1, 0)
    """
    # TODO
    raise NotImplementedError


def equivalent(f, g, n: int) -> bool:
    """True if f ≡ g. Hint: use counterexample."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Adders, built from the gates above
# ---------------------------------------------------------------------------

def half_adder(a: int, b: int) -> tuple[int, int]:
    """Return (sum, carry) of two bits.  half_adder(1, 1) == (0, 1)"""
    # TODO
    raise NotImplementedError


def full_adder(a: int, b: int, cin: int) -> tuple[int, int]:
    """
    Return (sum, carry_out) of three bits.
        sum       = a ⊕ b ⊕ cin
        carry_out = (a ∧ b) ∨ (cin ∧ (a ⊕ b))
    Bonus thought: you can build it from two half adders and one OR gate.
    """
    # TODO
    raise NotImplementedError


def add_binary(x: str, y: str) -> str:
    """
    Add two binary numbers given as strings of '0'/'1' (most significant bit first)
    with a ripple-carry adder: one full_adder per column, from right to left.

    - If the strings have different lengths, pad the shorter one with '0' on the left.
    - The result has as many bits as the longer input, plus a leading '1'
      only if there is a final carry.

    add_binary("1011", "0110") == "10001"      # 11 + 6 = 17
    add_binary("0011", "0001") == "0100"       # 3 + 1 = 4, no final carry
    add_binary("1", "1")       == "10"
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · NAND is enough
# Use ONLY calls to NAND (and variables). No other gates, no and/or/not, no operators.
# ---------------------------------------------------------------------------

def nand_not(a: int) -> int:
    # TODO
    raise NotImplementedError


def nand_and(a: int, b: int) -> int:
    # TODO
    raise NotImplementedError


def nand_or(a: int, b: int) -> int:
    # TODO
    raise NotImplementedError


def nand_xor(a: int, b: int) -> int:
    """Hint: four NAND gates are enough. Start with n = NAND(a, b)."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    print("half_adder(1, 1) =", half_adder(1, 1))
    print("11 + 6 =", add_binary("1011", "0110"), "(binary)")
    print("p→q ≡ ¬q→¬p ?", equivalent(lambda p, q: OR(NOT(p), q), lambda p, q: OR(NOT(NOT(q)), NOT(p)), 2))
    print("p→q ≡ q→p   ? counterexample:", counterexample(lambda p, q: OR(NOT(p), q), lambda p, q: OR(NOT(q), p), 2))
