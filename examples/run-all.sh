#!/usr/bin/env bash
# Run every example's self-test, summarize.
set -uo pipefail

EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

declare -a EXAMPLES=(
  "01-todo-cli"
  "02-bloated-code"
  "03-landing-page"
  "04-ralph-bugfix"
  "05-auto-flow-gate"
)

results=()
overall_fail=0

for name in "${EXAMPLES[@]}"; do
  echo "═══════════════════════════════════════════════════════════"
  echo "▶ $name"
  echo "═══════════════════════════════════════════════════════════"
  if [[ -x "$EX_DIR/$name/run.sh" ]]; then
    if bash "$EX_DIR/$name/run.sh"; then
      results+=("✅ $name")
    else
      results+=("❌ $name")
      overall_fail=1
    fi
  else
    results+=("⚠️  $name (run.sh not executable)")
    overall_fail=1
  fi
  echo
done

echo "═══════════════════════════════════════════════════════════"
echo "SUMMARY"
echo "═══════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  echo "  $r"
done

exit "$overall_fail"
