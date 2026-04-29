"""Behavior contract for parse_url. DO NOT MODIFY (red line for ralph-loop)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from parser import parse_url


def test_basic_https():
    r = parse_url("https://example.com/foo")
    assert r["scheme"] == "https"
    assert r["host"] == "example.com"
    assert r["path"] == "/foo"


def test_no_scheme_defaults_to_https():
    """Bug-1: should default scheme to https when missing."""
    r = parse_url("example.com/foo")
    assert r["scheme"] == "https"
    assert r["host"] == "example.com"
    assert r["path"] == "/foo"


def test_query_with_equals_in_value():
    """Bug-2: a=1=1 should keep value as '1=1', not split further."""
    r = parse_url("https://x.com/?a=1=1")
    assert r["query"] == {"a": "1=1"}


def test_fragment_stripped_from_path():
    """Bug-3: fragment should not be in path."""
    r = parse_url("https://x.com/page#top")
    assert r["path"] == "/page"
    assert r["fragment"] == "top"


def test_full():
    r = parse_url("https://api.example.com/v1/users?id=42&q=foo#section")
    assert r["scheme"] == "https"
    assert r["host"] == "api.example.com"
    assert r["path"] == "/v1/users"
    assert r["query"] == {"id": "42", "q": "foo"}
    assert r["fragment"] == "section"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
