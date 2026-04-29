"""A deliberately bloated calculator module — used as code-simplifier test input.

DO NOT clean this up by hand. The whole point is that simplifier should.
Each smell is labeled with [Pn] in a comment so you can grade simplifier output.
"""

import os  # [P0] unused
import sys  # [P0] unused
import math


# [P0] tombstone comment referencing removed code
# Note: legacy_compat() was here, removed in v2 cleanup. Kept this comment
# in case anyone is searching for it.

# [P0] dead branch — never True
if False:
    raise RuntimeError("unreachable")


# [P1] single-implementation interface — only AbstractCalc + Calc, never mocked
class _AbstractCalc:
    def add(self, a, b): raise NotImplementedError
    def sub(self, a, b): raise NotImplementedError


def add(a, b):
    # [P1] over-defensive: this is internal, callers always pass numbers
    if not isinstance(a, (int, float)):
        raise TypeError("a must be number")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be number")
    return a + b


def sub(a, b):
    if not isinstance(a, (int, float)):
        raise TypeError("a must be number")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be number")
    return a - b


def mul(a, b):
    if not isinstance(a, (int, float)):
        raise TypeError("a must be number")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be number")
    return a * b


# [P0] dead — no caller anywhere
def legacy_log(x):
    return math.log(x)


# [P1] empty wrapper — does nothing but forward
def add_wrapper(a, b):
    return add(a, b)


# [P0] repeated 3x identical structure — should be extracted
def announce_add(a, b):
    print(f"[ANNOUNCE] computing add({a}, {b})")
    r = add(a, b)
    print(f"[ANNOUNCE] result: {r}")
    return r


def announce_sub(a, b):
    print(f"[ANNOUNCE] computing sub({a}, {b})")
    r = sub(a, b)
    print(f"[ANNOUNCE] result: {r}")
    return r


def announce_mul(a, b):
    print(f"[ANNOUNCE] computing mul({a}, {b})")
    r = mul(a, b)
    print(f"[ANNOUNCE] result: {r}")
    return r


# [P2] nested ifs — should use guard clauses
def safe_div(a, b, unused_param=None):  # [P1] tombstone parameter
    if a is not None:
        if b is not None:
            if b != 0:
                return a / b
    return None


# [P2] complex boolean
def is_valid(x):
    if not (x is None or (isinstance(x, str) and len(x) == 0) or (isinstance(x, list) and not x)):
        return True
    return False
