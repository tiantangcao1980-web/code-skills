#!/usr/bin/env bash
# Example 02: verify simplifier behavior preservation + size reduction.
set -euo pipefail

EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pass=0
fail=0
ok()  { echo "[ OK ] $1"; pass=$((pass+1)); }
bad() { echo "[FAIL] $1"; fail=$((fail+1)); }

if ! command -v pytest >/dev/null 2>&1; then
  echo "[SKIP] pytest not in PATH; install: pip install pytest"
  echo "       or run with: python3 -m pytest"
  exit 0
fi

# 1. before tests pass (bloated but functional)
( cd "$EX_DIR/before" && pytest -q test_calculator.py >/dev/null 2>&1 ) \
  && ok "before/calculator.py: tests pass" \
  || bad "before tests should pass"

# 2. expected tests pass (slim, same behavior)
( cd "$EX_DIR/expected" && pytest -q test_calculator.py >/dev/null 2>&1 ) \
  && ok "expected/calculator.py: tests pass (behavior preserved)" \
  || bad "expected tests should pass"

# 3. line reduction ≥ 30%
before_lines=$(wc -l < "$EX_DIR/before/calculator.py")
expected_lines=$(wc -l < "$EX_DIR/expected/calculator.py")
reduction=$(python3 -c "print(int((1 - $expected_lines/$before_lines)*100))")
if [[ "$reduction" -ge 30 ]]; then
  ok "size reduction: ${reduction}% (${before_lines} -> ${expected_lines} lines, target ≥30%)"
else
  bad "size reduction only ${reduction}% (target ≥30%)"
fi

# 4. changelog has ≥ 8 P-level markers
markers=$(grep -cE "^\| [0-9]+ \|" "$EX_DIR/expected/changelog.md" || true)
if [[ "$markers" -ge 8 ]]; then
  ok "changelog has $markers P-marked changes (target ≥8)"
else
  bad "changelog only has $markers P-marked changes (target ≥8)"
fi

# 5. tests files identical (simplifier must NOT touch tests)
if diff -q "$EX_DIR/before/test_calculator.py" "$EX_DIR/expected/test_calculator.py" >/dev/null; then
  ok "test files identical (red-line: simplifier must not edit tests)"
else
  bad "test files differ — red-line violation"
fi

echo
if [[ $fail -eq 0 ]]; then
  echo "ALL PASS ($pass/$((pass+fail)))"
  exit 0
fi
echo "FAILED $fail / $((pass+fail))"
exit 1
