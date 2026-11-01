"""Tests for Lab 6 (hunt.py). Run them with:  python check.py"""
import random
import time
from math import isqrt

import pytest

import hunt as h


def sieve(n):
    """reference: primes below n"""
    s = [True] * n
    s[0] = s[1] = False
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = [False] * len(s[i * i::i])
    return s


PRIME = sieve(30_000)


# Part A ---------------------------------------------------------------------

def test_is_prime_small():
    """is_prime agrees with a sieve for every n from -5 to 3000"""
    for n in range(-5, 3000):
        assert h.is_prime(n) == (n >= 0 and PRIME[n]), f"is_prime({n}) should be {n >= 0 and PRIME[n]}"


def test_is_prime_fast():
    """is_prime stops at √n, so a ten-digit prime takes well under a second"""
    t = time.perf_counter()
    assert h.is_prime(100_000_007) is True
    assert time.perf_counter() - t < 1.0, "is_prime is too slow: only try divisors up to isqrt(n)"
    assert h.is_prime(1_000_000_007) is True
    assert h.is_prime(1_000_003 * 999_983) is False  # two six-digit primes


def test_smallest_factor():
    """smallest_factor finds the smallest divisor greater than 1"""
    assert h.smallest_factor(91) == 7
    assert h.smallest_factor(1681) == 41
    assert h.smallest_factor(13) == 13
    assert h.smallest_factor(2) == 2
    for n in range(2, 2000):
        d = next(d for d in range(2, n + 1) if n % d == 0)
        assert h.smallest_factor(n) == d, f"smallest_factor({n}) should be {d}"


# Part B ---------------------------------------------------------------------

def test_first_counterexample():
    """first_counterexample returns the first failing n, or None"""
    assert h.first_counterexample(lambda n: n < 10, 0, 100) == 10
    assert h.first_counterexample(lambda n: n < 10, 0, 5) is None
    assert h.first_counterexample(lambda n: n % 7 != 3, 4, 50) == 10
    assert h.first_counterexample(lambda n: n % 7 != 3, 4, 10) is None, "stop is not included in the range"
    assert h.first_counterexample(lambda n: n > 0, 5, 5) is None


def test_first_counterexample_stops_early():
    """first_counterexample does not look at any n after the first failure"""
    def prop(n):
        if n > 12:
            raise RuntimeError("looked past the first counterexample")
        return n != 12
    assert h.first_counterexample(prop, 0, 1000) == 12


def test_holds_for_all():
    """holds_for_all is an exhaustive proof on a finite range"""
    ineq = lambda n: (n + 1) ** 3 >= 3 ** n
    assert h.holds_for_all(ineq, 1, 5) is True
    assert h.holds_for_all(ineq, 1, 6) is False
    assert h.holds_for_all(lambda n: (n * n + n) % 2 == 0, -500, 500) is True
    assert h.holds_for_all(lambda n: False, 3, 3) is True, "on an empty range the claim is vacuously true"


def test_streak():
    """streak counts the values in a row that pass, starting at start, at most limit of them"""
    assert h.streak(lambda n: n < 10) == 10
    assert h.streak(lambda n: (n + 1) ** 3 >= 3 ** n, start=1) == 4
    assert h.streak(lambda n: n < 1000, limit=50) == 50
    assert h.streak(lambda n: n < 1000, start=990, limit=50) == 10
    assert h.streak(lambda n: n % 5 != 0) == 0
    assert h.streak(lambda n: n % 5 != 0, start=6) == 4
    assert h.streak(lambda n: n * n - 79 * n + 1601 > 0 and PRIME[n * n - 79 * n + 1601]) == 80


# Part C ---------------------------------------------------------------------

def test_euler_poly():
    """euler_poly is n² + n + 41 is prime, checked for n = 0 to 150"""
    for n in range(151):
        assert h.euler_poly(n) == PRIME[n * n + n + 41], f"euler_poly({n}) is wrong"


def test_euler_hunt():
    """the hunt finds Euler's polynomial failing first at n = 40, after a streak of 40"""
    assert h.first_counterexample(h.euler_poly, 0, 1000) == 40
    assert h.streak(h.euler_poly) == 40
    assert h.first_counterexample(h.euler_poly, 41, 1000) == 41


def test_fermat():
    """fermat: 3, 5, 17, 257, 65537 are prime, 2^32 + 1 = 641 × 6700417 is not"""
    assert [h.fermat(n) for n in range(5)] == [True] * 5
    assert h.fermat(5) is False
    assert h.first_counterexample(h.fermat, 0, 6) == 5


def test_three_squares():
    """three_squares agrees with a brute-force search for n = 0 to 400"""
    sums = {a * a + b * b + c * c for a in range(21) for b in range(21) for c in range(21)}
    for n in range(401):
        assert h.three_squares(n) == (n in sums), f"three_squares({n}) should be {n in sums}"
    assert h.first_counterexample(h.three_squares, 0, 100) == 7


def test_goldbach_other_examples():
    """goldbach_other: 9, 15, 21 work; primes, even numbers and small numbers are vacuously true"""
    for n in (9, 15, 21, 25, 27, 33):
        assert h.goldbach_other(n) is True, f"{n} is a prime plus twice a square"
    for n in (1, 2, 3, 4, 7, 8, 13, 100, 5779):
        assert h.goldbach_other(n) is True, f"the claim says nothing about {n}: return True"


def test_goldbach_other_hunt():
    """Goldbach's other claim fails first at 5777, and then at 5993"""
    assert h.goldbach_other(5777) is False
    assert h.goldbach_other(5993) is False
    assert h.first_counterexample(h.goldbach_other, 1, 10_000) == 5777
    assert h.first_counterexample(h.goldbach_other, 5778, 10_000) == 5993


# Part D ---------------------------------------------------------------------

def test_goldbach_pair_examples():
    """goldbach_pair gives the pair with the smallest p, or None"""
    assert h.goldbach_pair(4) == (2, 2)
    assert h.goldbach_pair(28) == (5, 23)
    assert h.goldbach_pair(100) == (3, 97)
    for n in (9, 2, 0, -4, 1):
        assert h.goldbach_pair(n) is None, f"goldbach_pair({n}) should be None"


def test_goldbach_pair_random():
    """goldbach_pair is correct for 200 random even numbers up to 20000"""
    rng = random.Random(7)
    for n in (2 * rng.randint(2, 9999) for _ in range(200)):
        p = next(p for p in range(2, n) if PRIME[p] and PRIME[n - p])
        assert h.goldbach_pair(n) == (p, n - p), f"goldbach_pair({n}) should be {(p, n - p)}"


def test_taxicab():
    """two_ways_cubes finds 1729, and 4104 when you start after it"""
    assert h.two_ways_cubes(2000) == 1729
    assert h.two_ways_cubes(1728) is None
    assert h.two_ways_cubes(5000, start=1730) == 4104
    assert h.two_ways_cubes(14000, start=4105) == 13832


# Part E ---------------------------------------------------------------------

def test_collatz_examples():
    """collatz_steps: 1 → 0, 6 → 8, 27 → 111"""
    assert h.collatz_steps(1) == 0
    assert h.collatz_steps(2) == 1
    assert h.collatz_steps(6) == 8
    assert h.collatz_steps(27) == 111


def test_collatz_many():
    """collatz_steps agrees with a reference for n = 1 to 3000"""
    def ref(n):
        s = 0
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            s += 1
        return s
    for n in range(1, 3001):
        assert h.collatz_steps(n) == ref(n), f"collatz_steps({n}) should be {ref(n)}"
