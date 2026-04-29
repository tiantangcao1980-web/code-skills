"""Calculator module — expected post-simplifier output.

Behavior identical to before/calculator.py; tests in test_calculator.py pass
against both. ~50 lines vs ~95 in before (≥45% reduction).
"""

import math


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def _announce(name, fn, a, b):
    print(f"[ANNOUNCE] computing {name}({a}, {b})")
    r = fn(a, b)
    print(f"[ANNOUNCE] result: {r}")
    return r


def announce_add(a, b):
    return _announce("add", add, a, b)


def announce_sub(a, b):
    return _announce("sub", sub, a, b)


def announce_mul(a, b):
    return _announce("mul", mul, a, b)


def safe_div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def is_valid(x):
    if x is None:
        return False
    if isinstance(x, str) and len(x) == 0:
        return False
    if isinstance(x, list) and not x:
        return False
    return True
