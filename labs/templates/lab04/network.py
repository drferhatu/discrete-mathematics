"""
Lab 4 · Nested Quantifiers: Checking a Social Network
Discrete Mathematics (YMT211) · Fall 2026

Week 5 in code. Fill in every function marked TODO, one at a time, top to bottom.
Check yourself with:  python check.py

Words you need (from the week 5 notes)
- A two-place predicate P(x, y) is a function of TWO elements that returns True or False,
  for example   lambda x, y: x + y == 10
- ∀x ∃y P(x, y)   "for every x there is some y"   → a loop over x, with a loop over y inside
- ∃x ∀y P(x, y)   "there is one x that works for every y"

This week you MAY use all() and any(). A nested statement becomes nested calls:
    ∀x ∃y P(x, y)   is   all(any(P(x, y) for y in domain) for x in domain)

Rules
- Do not change function names or parameters: the autograder calls them by name.
- Inside Part C use the parameter `net`, never the global FOLLOWS: the tests use other networks too.
"""

from data import FOLLOWS


def follows(net, x, y) -> bool:
    """F(x, y): does x follow y in the network `net`? (Given, nothing to do here.)"""
    return y in net[x]


def people(net) -> list:
    """The domain: everyone in the network, in the order of the dictionary. (Given.)"""
    return list(net)


# ---------------------------------------------------------------------------
# Part A · The four shapes of a nested statement
# D is a list (the domain), P is a two-place predicate P(x, y).
# ---------------------------------------------------------------------------

def forall_forall(D, P) -> bool:
    """∀x ∀y P(x, y): P holds for EVERY pair."""
    # TODO
    raise NotImplementedError


def forall_exists(D, P) -> bool:
    """
    ∀x ∃y P(x, y): for every x there is at least one y.

    forall_exists([1, 2, 3], lambda x, y: x + y == 4)    → True   (1+3, 2+2, 3+1)
    forall_exists([1, 2], lambda x, y: x + y == 4)       → False  (1 has no partner)
    """
    # TODO
    raise NotImplementedError


def exists_forall(D, P) -> bool:
    """
    ∃x ∀y P(x, y): there is ONE x that works for every y.

    exists_forall([1, 2, 3], lambda x, y: x <= y)        → True   (x = 1 is ≤ everything)
    exists_forall([1, 2, 3], lambda x, y: x < y)         → False  (no x is smaller than itself)
    """
    # TODO
    raise NotImplementedError


def exists_exists(D, P) -> bool:
    """∃x ∃y P(x, y): at least one pair works."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · Witnesses for ∀x ∃y
# ---------------------------------------------------------------------------

def witnesses(D, P) -> dict:
    """
    For a statement ∀x ∃y P(x, y), return a dictionary that gives every x its FIRST witness y
    (the first y in D with P(x, y) True). An x without any witness gets None.

    witnesses([1, 2, 3], lambda x, y: x + y == 4)   → {1: 3, 2: 2, 3: 1}
    witnesses([1, 2], lambda x, y: x + y == 4)      → {1: None, 2: 2}
    """
    # TODO
    raise NotImplementedError


def first_failure(D, P):
    """
    The counterexample to ∀x ∃y P(x, y): the FIRST x that has no witness at all, or None.

    first_failure([1, 2], lambda x, y: x + y == 4)   → 1
    first_failure([1, 2, 3], lambda x, y: x + y == 4)   → None
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Questions about the network
# `net` is a dictionary like FOLLOWS. Use follows(net, x, y) and people(net).
# Nobody follows themselves, so "everyone" below always means "everyone ELSE" (x != y).
# ---------------------------------------------------------------------------

def everyone_follows_someone(net=FOLLOWS) -> bool:
    """Q1. ∀x ∃y (x ≠ y ∧ F(x, y)): every person follows at least one other person."""
    # TODO
    raise NotImplementedError


def celebrity(net=FOLLOWS):
    """
    Q2. ∃y ∀x (x ≠ y → F(x, y)): return the NAME of the first person who is followed by
    everyone else, or None if there is no such person.
    """
    # TODO
    raise NotImplementedError


def someone_follows_everyone(net=FOLLOWS) -> bool:
    """Q3. ∃x ∀y (x ≠ y → F(x, y)): some person follows everyone else."""
    # TODO
    raise NotImplementedError


def all_mutual(net=FOLLOWS) -> bool:
    """Q4. ∀x ∀y (F(x, y) → F(y, x)): every follow is returned."""
    # TODO
    raise NotImplementedError


def first_unreturned(net=FOLLOWS):
    """
    Q5. The counterexample to Q4: the first pair (x, y) with F(x, y) but not F(y, x), or None.
    Go through x in the order of people(net), and for each x through y in the order of people(net).
    Return a tuple, e.g. ("Bora", "Can").
    """
    # TODO
    raise NotImplementedError


def loners(net=FOLLOWS) -> list:
    """
    Q6. Everyone who follows nobody AND is followed by nobody:
        the x with ∀y (¬F(x, y) ∧ ¬F(y, x)).   Return their names as a list, in the order of people(net).
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · Negating a nested statement
#   ¬∀x ∃y P(x, y)  ≡  ∃x ∀y ¬P(x, y)
# ---------------------------------------------------------------------------

def not_forall_exists(D, P) -> bool:
    """
    ¬∀x ∃y P(x, y), computed as ∃x ∀y ¬P(x, y).
    Use your exists_forall with a new predicate that returns the opposite of P.
    Do not write  not forall_exists(...)  here: the point is to use the rule.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part E · A specification for sorting (week 5 notes)
# ---------------------------------------------------------------------------

def is_sorted(b) -> bool:
    """∀i (0 ≤ i < n−1 → b[i] ≤ b[i+1]).   is_sorted([1, 3, 3]) → True,  is_sorted([2, 1]) → False"""
    # TODO
    raise NotImplementedError


def keeps_values(a, b) -> bool:
    """∀i ∃j (a[i] = b[j]): every value of a appears somewhere in b."""
    # TODO
    raise NotImplementedError


def is_correct_sort(a, b) -> bool:
    """
    The complete specification: b is a correct sorted version of a.
    b must be sorted AND every value must occur the SAME NUMBER OF TIMES in a and in b.
    (keeps_values alone is not enough: [3, 3, 1] → [1, 3, 5] fools it.)  Hint: list.count
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Try it:  python network.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Q1 everyone follows someone :", everyone_follows_someone())
    print("Q2 celebrity                :", celebrity())
    print("Q3 someone follows everyone :", someone_follows_everyone())
    print("Q4 all follows mutual       :", all_mutual())
    print("Q5 first unreturned follow  :", first_unreturned())
    print("Q6 loners                   :", loners())
    print("[3,3,1] → [1,3,5] correct?  :", is_correct_sort([3, 3, 1], [1, 3, 5]))
