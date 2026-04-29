#!/usr/bin/env bash
# Example 04 self-test: verify before is broken in expected ways,
# expected is fixed, contract has required fields.
set -euo pipefail

EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pass=0
fail=0
ok()  { echo "[ OK ] $1"; pass=$((pass+1)); }
bad() { echo "[FAIL] $1"; fail=$((fail+1)); }

if ! command -v pytest >/dev/null 2>&1; then
  echo "[SKIP] pytest not in PATH; install: pip install pytest"
  exit 0
fi

# 1. before tests should have exactly 4 failures
#    (3 individual bug tests + 1 integration test_full that hits all bugs)
before_out="$(cd "$EX_DIR/before" && pytest -q test_parser.py 2>&1 || true)"
before_failed=$(echo "$before_out" | grep -oE '[0-9]+ failed' | head -1 | grep -oE '[0-9]+' || echo 0)
if [[ "$before_failed" -eq 4 ]]; then
  ok "before: 4 tests fail (3 bug tests + integration, bugs are real)"
else
  bad "before: expected 4 failures, got $before_failed"
fi

# 2. expected tests should all pass
( cd "$EX_DIR/expected" && pytest -q test_parser.py >/dev/null 2>&1 ) \
  && ok "expected: 5/5 pass (reference fix works)" \
  || bad "expected/parser.py reference fix should pass"

# 3. test files identical (red line: never edit tests)
if diff -q "$EX_DIR/before/test_parser.py" "$EX_DIR/expected/test_parser.py" >/dev/null; then
  ok "test files identical (red-line: ralph-loop must not edit tests)"
else
  bad "test files differ — red-line violation"
fi

# 4. contract.md has required 4 fields
required=("目标" "退出条件" "最大迭代数" "验证手段")
missing=0
for f in "${required[@]}"; do
  grep -q "$f:" "$EX_DIR/expected/contract.md" || missing=$((missing+1))
done
if [[ $missing -eq 0 ]]; then
  ok "contract.md has all 4 required fields"
else
  bad "contract.md missing $missing required fields"
fi

# 5. contract has at least 2 iterations + exit report
iter_count=$(grep -cE '^### Iteration [0-9]+' "$EX_DIR/expected/contract.md")
if [[ "$iter_count" -ge 2 ]]; then
  ok "contract.md shows $iter_count+ iterations (≥2 expected)"
else
  bad "contract.md only shows $iter_count iterations"
fi

if grep -q "退出报告" "$EX_DIR/expected/contract.md"; then
  ok "contract.md includes exit report"
else
  bad "contract.md missing exit report"
fi

echo
if [[ $fail -eq 0 ]]; then
  echo "ALL PASS ($pass/$((pass+fail)))"
  exit 0
fi
echo "FAILED $fail / $((pass+fail))"
exit 1
