"""
Lab 3 · Quantifiers over Real Data
Discrete Mathematics (YMT211) · Fall 2026

Week 4 in code. Fill in every function marked TODO, one at a time, top to bottom.
Check yourself with:  python check.py

Words you need (from the week 4 notes)
- domain:          the list of things we talk about, e.g. the list of students
- predicate:       a function that takes ONE element and returns True or False, e.g.
                       lambda s: s["github"]          # "s has a GitHub account"
- counterexample:  an element that makes a "for all" statement false
- witness:         an element that makes a "there exists" statement true

Rules
- Do not change function names or parameters: the autograder calls them by name.
- In Part A, write the loops yourself: do NOT use all() or any() there.
  From Part B on, you may use your Part A functions, all() and any().
"""

from data import STUDENTS


# ---------------------------------------------------------------------------
# Part A · ∀ and ∃ as loops
# ---------------------------------------------------------------------------

def for_all(domain, P) -> bool:
    """
    ∀x P(x): True if P(x) is True for EVERY x in the domain.

    Walk through the domain with a for loop. As soon as you meet an x with P(x) False,
    return False right away (do not look at the rest). If the loop finishes, return True.

    for_all([2, 4, 6], lambda n: n % 2 == 0)   → True
    for_all([2, 3, 6], lambda n: n % 2 == 0)   → False   (3 is a counterexample)
    for_all([], lambda n: False)               → True    (an empty domain has no counterexample)
    """
    # TODO
    raise NotImplementedError


def exists(domain, P) -> bool:
    """
    ∃x P(x): True if P(x) is True for AT LEAST ONE x in the domain.

    Stop and return True at the first x with P(x) True. If the loop finishes, return False.

    exists([1, 3, 4], lambda n: n % 2 == 0)    → True    (4 is a witness)
    exists([1, 3, 5], lambda n: n % 2 == 0)    → False
    exists([], lambda n: True)                 → False   (an empty domain has no witness)
    """
    # TODO
    raise NotImplementedError


def counterexample(domain, P):
    """
    Return the FIRST x in the domain with P(x) False, or None if there is none.

    counterexample([2, 3, 5], lambda n: n % 2 == 0)   → 3
    counterexample([2, 4], lambda n: n % 2 == 0)      → None
    """
    # TODO
    raise NotImplementedError


def witness(domain, P):
    """
    Return the FIRST x in the domain with P(x) True, or None if there is none.

    witness([1, 3, 4, 6], lambda n: n % 2 == 0)   → 4
    witness([1, 3], lambda n: n % 2 == 0)         → None
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · The golden rule: ∀ goes with →, ∃ goes with ∧
# A and B are predicates. A is the "filter" (for example: "x is a second-year student").
# ---------------------------------------------------------------------------

def every_such_that(domain, A, B) -> bool:
    """
    "Every A is B":   ∀x (A(x) → B(x))

    Only the elements with A(x) True are tested. Elements with A(x) False never make it false.
    Hint: for_all with a predicate that computes  (not A(x)) or B(x).

    every_such_that([1, 2, 3, 4], lambda n: n > 2, lambda n: n % 2 == 0)   → False   (3 > 2 but 3 is odd)
    every_such_that([1, 2, 4], lambda n: n > 2, lambda n: n % 2 == 0)      → True    (only 4 is > 2, and it is even)
    """
    # TODO
    raise NotImplementedError


def some_such_that(domain, A, B) -> bool:
    """
    "Some A is B":   ∃x (A(x) ∧ B(x))

    some_such_that([1, 2, 3, 4], lambda n: n > 2, lambda n: n % 2 == 0)   → True    (4)
    some_such_that([1, 2, 3], lambda n: n > 2, lambda n: n % 2 == 0)      → False
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Questions about the class (data.py)
# Each function gets the list of students and answers one question.
# A student s is a dict:  s["name"], s["year"], s["langs"], s["github"], s["math"]
# The tests also call these functions with OTHER lists of students, so do not hard-code answers.
# ---------------------------------------------------------------------------

def everyone_has_github(students=STUDENTS) -> bool:
    """Q1. Every student has a GitHub account.          ∀s G(s)"""
    # TODO
    raise NotImplementedError


def someone_knows_java(students=STUDENTS) -> bool:
    """Q2. Some student knows Java.                     ∃s J(s)       Hint: "Java" in s["langs"]"""
    # TODO
    raise NotImplementedError


def every_second_year_knows_python(students=STUDENTS) -> bool:
    """Q3. Every second-year student knows Python.      ∀s (Y2(s) → P(s))"""
    # TODO
    raise NotImplementedError


def no_first_year_failed_math(students=STUDENTS) -> bool:
    """
    Q4. No first-year student failed Math I (a grade below 50 is a fail).
        ¬∃s (Y1(s) ∧ F(s))      which is the same as      ∀s (Y1(s) → ¬F(s))
    """
    # TODO
    raise NotImplementedError


def who_breaks_q3(students=STUDENTS):
    """
    Q5. Return the NAME of the first second-year student who does not know Python,
        that is, the counterexample to Q3. Return None if Q3 is true.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · De Morgan's laws for quantifiers
#   ¬∀x P(x)  ≡  ∃x ¬P(x)          ¬∃x P(x)  ≡  ∀x ¬P(x)
# ---------------------------------------------------------------------------

def not_all(domain, P) -> bool:
    """
    ¬∀x P(x), computed as  ∃x ¬P(x).
    Use your exists() with a NEW predicate that returns the opposite of P.
    Do not write  not for_all(...)  here: the point is to use the law.
    """
    # TODO
    raise NotImplementedError


def not_any(domain, P) -> bool:
    """
    ¬∃x P(x), computed as  ∀x ¬P(x).
    Use your for_all() with a predicate that returns the opposite of P.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Try it:  python quantifiers.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Q1 everyone has GitHub          :", everyone_has_github())
    print("Q2 someone knows Java           :", someone_knows_java())
    print("Q3 every 2nd-year knows Python  :", every_second_year_knows_python())
    print("Q4 no 1st-year failed Math I    :", no_first_year_failed_math())
    print("Q5 who breaks Q3                :", who_breaks_q3())
