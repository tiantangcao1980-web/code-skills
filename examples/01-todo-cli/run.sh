#!/usr/bin/env bash
# Example 01 self-test: scaffold a CLI and verify it self-describes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAFFOLD="$EX_DIR/scaffold"

pass=0
fail=0
ok()   { echo "[ OK ] $1"; pass=$((pass+1)); }
bad()  { echo "[FAIL] $1"; fail=$((fail+1)); }

# 1. clean & scaffold
rm -rf "$SCAFFOLD"
cd "$EX_DIR"
"$ROOT/bin/code-skills" cli-init scaffold >/dev/null 2>&1 \
  && ok "scaffold created" \
  || bad "scaffold cli-init failed"

# 2. describe --json shape
schema="$("$SCAFFOLD/bin/scaffold" describe --json 2>/dev/null || echo '')"
python3 -c "
import json, sys
s = json.loads('''$schema''')
assert s['opencli'] == '0.1'
assert s['name'] == 'scaffold'
assert len(s['commands']) >= 2
" 2>/dev/null \
  && ok "describe --json: opencli=0.1, valid schema" \
  || bad "describe --json shape invalid"

# 3. help works (capture to var to avoid pipefail+SIGPIPE false negative)
help_out="$("$SCAFFOLD/bin/scaffold" help 2>/dev/null || true)"
if echo "$help_out" | grep -q "USAGE"; then
  ok "help works"
else
  bad "help missing or malformed"
fi

# 4. version works
ver_out="$("$SCAFFOLD/bin/scaffold" version 2>/dev/null || true)"
if echo "$ver_out" | grep -qE "^[0-9]+\."; then
  ok "version works (semver-ish)"
else
  bad "version missing or malformed"
fi

# 5. INTERFACE.md
if [[ -f "$SCAFFOLD/INTERFACE.md" ]] && grep -q "Command tree" "$SCAFFOLD/INTERFACE.md"; then
  ok "INTERFACE.md exists with command tree"
else
  bad "INTERFACE.md missing or empty"
fi

# 6. README.md
if [[ -f "$SCAFFOLD/README.md" ]] && grep -q "Quick start" "$SCAFFOLD/README.md"; then
  ok "README.md exists with Quick start"
else
  bad "README.md missing or empty"
fi

echo
if [[ $fail -eq 0 ]]; then
  echo "ALL PASS ($pass/$((pass+fail)))"
  exit 0
fi
echo "FAILED $fail / $((pass+fail))"
exit 1
