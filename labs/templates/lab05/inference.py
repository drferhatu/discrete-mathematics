"""
Lab 5 · A Tiny Inference Engine
Discrete Mathematics (YMT211) · Fall 2026

Week 6 in code. Fill in every function marked TODO, one at a time, top to bottom.
Check yourself with:  python check.py

How facts and rules look in this lab
- A FACT is a string, e.g. "passed_math1".
- A RULE is a pair (conditions, conclusion):
      (("passed_programming", "can_take_discrete"), "can_take_algorithms")
  means: IF passed_programming AND can_take_discrete THEN can_take_algorithms.
  `conditions` is a tuple of facts (it may have one element: ("passed_math1",) ).
- A list of rules is just a Python list of such pairs. Rule number i is rules[i].

Rules
- Do not change function names or parameters: the autograder calls them by name.
- Never modify the `facts` you receive: work on a copy (set(facts)) and return a new set.
"""

from itertools import product


# ---------------------------------------------------------------------------
# Part A · Is an argument valid?   (propositional logic, by brute force)
# A premise or a conclusion is a function of n booleans, e.g.  lambda p, q: (not p) or q   for p → q
# ---------------------------------------------------------------------------

def counterexample(premises, conclusion, n):
    """
    Return the FIRST row (a tuple of n booleans, in the order of product([True, False], repeat=n))
    in which EVERY premise is True but the conclusion is False. Return None if there is no such row.

    Affirming the conclusion,  p → q,  q   ∴ p :
        counterexample([lambda p, q: (not p) or q, lambda p, q: q], lambda p, q: p, 2)  → (False, True)
    """
    # TODO
    raise NotImplementedError


def is_valid(premises, conclusion, n) -> bool:
    """An argument is valid exactly when it has no counterexample."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part B · Forward chaining: modus ponens until nothing new appears
# ---------------------------------------------------------------------------

def can_fire(rule, facts) -> bool:
    """
    A rule can fire when ALL its conditions are known facts and its conclusion is NOT yet a fact.

    can_fire((("a", "b"), "c"), {"a", "b"})   → True
    can_fire((("a", "b"), "c"), {"a"})        → False   (b is not known)
    can_fire((("a",), "c"), {"a", "c"})       → False   (c is already known: nothing new)
    """
    # TODO
    raise NotImplementedError


def forward_chain(facts, rules) -> set:
    """
    Return the set of ALL facts that follow from `facts` with the `rules`.

    Repeat passes over the rules. In each pass, go through the rules IN ORDER and fire every rule that
    can fire (add its conclusion). A fact added earlier in a pass may already be used by later rules
    in the same pass. Stop when a whole pass adds nothing new. Do not modify `facts`: start from a copy.

    forward_chain({"a"}, [(("a",), "b"), (("b",), "c")])   → {"a", "b", "c"}
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C · Explaining a conclusion
# ---------------------------------------------------------------------------

def reasons(facts, rules) -> dict:
    """
    Run forward chaining, but remember WHY each fact is known.
    Return a dictionary  fact → rule number  (the index in `rules` of the rule that FIRST added it),
    and  fact → None  for the starting facts.

    reasons({"a"}, [(("a",), "b"), (("b",), "c")])   → {"a": None, "b": 0, "c": 1}
    Use exactly the same passes as forward_chain (rules in order, new facts usable at once).
    """
    # TODO
    raise NotImplementedError


def explain(goal, facts, rules):
    """
    Return the list of facts needed to establish `goal`, in an order in which each one can be derived
    from those before it, ending with `goal`. Return None if `goal` does not follow at all.

    Use reasons(). For a fact with reason None, the list is just [fact]. For a fact derived by rule i,
    first explain each condition of rules[i] (in the order the conditions are written), then add the fact.
    Never list the same fact twice.

    explain("c", {"a"}, [(("a",), "b"), (("b",), "c")])   → ["a", "b", "c"]
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part D · Backward chaining: start from the goal
# ---------------------------------------------------------------------------

def backward_chain(goal, facts, rules, visiting=None) -> bool:
    """
    Can `goal` be proved? Work BACKWARDS:
    - if goal is a known fact, it is proved;
    - otherwise, it is proved if SOME rule with conclusion == goal has ALL its conditions provable
      (call backward_chain again for each condition: this is recursion).

    `visiting` is the set of goals we are currently trying to prove. If goal is already in it, we are in a
    loop (for example rules a → b and b → a): return False for this branch. Start with an empty set
    when visiting is None, and pass  visiting | {goal}  to the recursive calls.

    backward_chain("c", {"a"}, [(("a",), "b"), (("b",), "c")])   → True
    backward_chain("x", {"a"}, [(("x",), "y"), (("y",), "x")])   → False   (a loop, never grounded)
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part E · A course advisor
# ---------------------------------------------------------------------------

def advisor_rules() -> list:
    """
    Turn these five sentences into rules (the order of the rules does not matter):

      1. A student who passed Math I can take Discrete Mathematics.
      2. A student who passed Programming I and can take Discrete Mathematics can take Algorithms.
      3. A student who can take Algorithms can take Data Structures.
      4. A student who passed Math I and passed Physics I can take Signals.
      5. A student who can take Data Structures and can take Signals can take Machine Learning.

    Use exactly these fact names:
      passed_math1, passed_programming1, passed_physics1,
      can_take_discrete, can_take_algorithms, can_take_data_structures, can_take_signals, can_take_ml
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Try it:  python inference.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    implies = lambda a, b: (not a) or b
    print("modus ponens valid?            :", is_valid([lambda p, q: p, lambda p, q: implies(p, q)], lambda p, q: q, 2))
    print("affirming the conclusion valid?:", is_valid([lambda p, q: implies(p, q), lambda p, q: q], lambda p, q: p, 2))

    student = {"passed_math1", "passed_programming1", "passed_physics1"}
    rules = advisor_rules()
    print("this student can take          :", sorted(f for f in forward_chain(student, rules) if f.startswith("can_take")))
    print("why can_take_ml?               :", explain("can_take_ml", student, rules))
    print("backward: can_take_ml?         :", backward_chain("can_take_ml", student, rules))
