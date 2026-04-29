"""Behavior baseline. Both before/calculator.py and expected/calculator.py
must pass these tests — that's how we know simplifier preserved behavior.
"""

import sys
from pathlib import Path

# Allow this file to be run from either before/ or expected/ as cwd by
# resolving relative to its own location.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from calculator import add, sub, mul, safe_div, is_valid, announce_add, announce_sub, announce_mul


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0.5, 0.5) == 1.0


def test_sub():
    assert sub(5, 3) == 2
    assert sub(0, 0) == 0


def test_mul():
    assert mul(2, 3) == 6
    assert mul(0, 100) == 0


def test_safe_div():
    assert safe_div(10, 2) == 5
    assert safe_div(10, 0) is None
    assert safe_div(None, 2) is None
    assert safe_div(10, None) is None


def test_is_valid():
    assert is_valid("hello") is True
    assert is_valid([1, 2]) is True
    assert is_valid(None) is False
    assert is_valid("") is False
    assert is_valid([]) is False


def test_announce_returns_correct_value(capsys):
    assert announce_add(1, 2) == 3
    assert announce_sub(5, 3) == 2
    assert announce_mul(2, 3) == 6
    captured = capsys.readouterr()
    # all three should print announce lines
    assert "computing add" in captured.out
    assert "computing sub" in captured.out
    assert "computing mul" in captured.out


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
