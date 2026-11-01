"""
Lab 6 · Counterexample Hunting
Discrete Mathematics (YMT211) · Fall 2026

Week 7 in code. Fill in every function marked TODO, one at a time, top to bottom.
Check yourself with:  python check.py

What a "claim" looks like in this lab
- A claim about integers is a Python function  prop(n) -> bool.
  For example, "n² + n is even" is   lambda n: (n * n + n) % 2 == 0
- A counterexample is an n for which prop(n) is False.

Rules
- Do not change function names or parameters: the autograder calls them by name.
- Use only the standard library (math is already imported for you).
"""

from math import isqrt


# ---------------------------------------------------------------------------
# Part A · Primes, the raw material of famous claims
# ---------------------------------------------------------------------------

def is_prime(n) -> bool:
    """
    True if n is a prime number, False otherwise (so False for 0, 1 and negative numbers).

    Try divisors d = 2, 3, 4, ... but only while d <= isqrt(n): the week 7 theorem
    "if n = ab, then a <= √n or b <= √n" says that is enough.

    is_prime(2) → True     is_prime(1) → False     is_prime(91) → False (7 × 13)
    """
    # TODO
    raise NotImplementedError


def smallest_factor(n) -> int:
    """
    For n >= 2, the smallest divisor of n that is greater than 1. (For a prime, that is n itself.)

    smallest_factor(91) → 7     smallest_factor(1681) → 41     smallest_factor(13) → 13
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · The hunter's tools
# ---------------------------------------------------------------------------

def first_counterexample(prop, start, stop):
    """
    The FIRST n in range(start, stop) for which prop(n) is False, or None if prop holds for all of them.
    Stop as soon as you find one: do not call prop on any later n.

    first_counterexample(lambda n: n < 10, 0, 100)   → 10
    first_counterexample(lambda n: n < 10, 0, 5)     → None
    """
    # TODO
    raise NotImplementedError


def holds_for_all(prop, start, stop) -> bool:
    """
    True if prop(n) is True for EVERY n in range(start, stop).
    On a finite range this is an exhaustive proof; outside the range it proves nothing.

    holds_for_all(lambda n: (n + 1) ** 3 >= 3 ** n, 1, 5)   → True    (n = 1, 2, 3, 4)
    holds_for_all(lambda n: (n + 1) ** 3 >= 3 ** n, 1, 6)   → False   (n = 5 fails)
    """
    # TODO
    raise NotImplementedError


def streak(prop, start=0, limit=10_000) -> int:
    """
    How many values in a row, starting at n = start, satisfy prop before the first failure?
    Look at no more than `limit` values: if all of start, start+1, ..., start+limit-1 pass, return limit.

    streak(lambda n: n < 10)                               → 10
    streak(lambda n: (n + 1) ** 3 >= 3 ** n, start=1)      → 4
    streak(lambda n: True, limit=50)                       → 50
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Famous claims, written as functions of n
# ---------------------------------------------------------------------------

def euler_poly(n) -> bool:
    """Euler's claim for one n: is n² + n + 41 prime?"""
    # TODO
    raise NotImplementedError


def fermat(n) -> bool:
    """Fermat's claim for one n (n >= 0): is 2^(2^n) + 1 prime?   (In Python: 2 ** (2 ** n) + 1)"""
    # TODO
    raise NotImplementedError


def three_squares(n) -> bool:
    """
    Is n (n >= 0) a sum of three squares a² + b² + c² of non-negative integers a, b, c?
    Repetitions are allowed:  3 = 1 + 1 + 1 → True,   0 = 0 + 0 + 0 → True,   7 → False.
    """
    # TODO
    raise NotImplementedError


def goldbach_other(n) -> bool:
    """
    Goldbach's other claim (1752): every ODD COMPOSITE number is a prime plus twice a square,
    n = p + 2k² with p prime and k >= 1.       9 = 7 + 2·1²,   15 = 7 + 2·2²,   21 = 3 + 2·3²

    The claim says nothing about other numbers, so for an n that is not an odd composite
    (even, prime, or smaller than 9) return True: the claim is vacuously true there.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · Existence proofs by construction: find the witness
# ---------------------------------------------------------------------------

def goldbach_pair(n):
    """
    For an even n > 2, return a pair (p, q) of primes with p + q == n and p as SMALL as possible.
    For any other n (odd, or n <= 2) return None.

    goldbach_pair(4) → (2, 2)     goldbach_pair(28) → (5, 23)     goldbach_pair(9) → None
    """
    # TODO
    raise NotImplementedError


def two_ways_cubes(limit, start=1):
    """
    The smallest n with start <= n <= limit that can be written as a³ + b³ (1 <= a <= b) in at least
    TWO different ways. Return None if there is no such n in that range.

    two_ways_cubes(2000)          → 1729   (1³ + 12³ = 9³ + 10³, the taxicab number)
    two_ways_cubes(1000)          → None
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part E · An open problem
# ---------------------------------------------------------------------------

def collatz_steps(n) -> int:
    """
    The Collatz rule: if n is even, n → n // 2; if n is odd, n → 3n + 1.
    Return how many steps it takes to reach 1, starting from n >= 1. (collatz_steps(1) → 0)

    6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1        collatz_steps(6) → 8
    Nobody has proved that every n reaches 1. Nobody has found one that does not.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Try it:  python hunt.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("n² + n + 41 prime, streak from 0 :", streak(euler_poly))
    print("first counterexample             :", first_counterexample(euler_poly, 0, 1000))
    print("Fermat fails first at n =        :", first_counterexample(fermat, 0, 6))
    print("three squares fails first at     :", first_counterexample(three_squares, 0, 100))
    print("Goldbach's other claim fails at  :", first_counterexample(goldbach_other, 1, 10_000))
    print("Goldbach for 4, 6, ..., 10000?   :", holds_for_all(lambda m: goldbach_pair(2 * m) is not None, 2, 5001))
    print("taxicab number                   :", two_ways_cubes(5000))
    print("Collatz steps for 27             :", collatz_steps(27))
