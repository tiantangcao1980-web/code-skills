#!/usr/bin/env bash
# Example 05: verify auto-flow Phase 0 gate has all required components.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pass=0
fail=0
ok()  { echo "[ OK ] $1"; pass=$((pass+1)); }
bad() { echo "[FAIL] $1"; fail=$((fail+1)); }

# 1. inputs exist
for f in 01-vague.md 02-partial.md 03-complete.md; do
  [[ -f "$EX_DIR/inputs/$f" ]] && ok "inputs/$f present" || bad "inputs/$f missing"
done

# 2. expected outputs exist
for f in 01-response-vague.md 02-response-partial.md 03-snapshot.md; do
  [[ -f "$EX_DIR/expected/$f" ]] && ok "expected/$f present" || bad "expected/$f missing"
done

# 3. snapshot has 11 completeness items + 4 feasibility items
snap="$EX_DIR/expected/03-snapshot.md"
items=$(grep -cE '^- (项目|用户|主流程|平台|技术栈|不做|验收|部署|时间|外部依赖|视觉)' "$snap" || echo 0)
if [[ "$items" -ge 11 ]]; then
  ok "snapshot lists 11 completeness items"
else
  bad "snapshot only lists $items / 11 items"
fi

feas=$(grep -cE '^- (技术可行|平台可行|资源可行|时间可行)' "$snap" || echo 0)
if [[ "$feas" -ge 4 ]]; then
  ok "snapshot lists 4 feasibility checks"
else
  bad "snapshot only lists $feas / 4 feasibility checks"
fi

# 4. auto-flow SKILL.md declares all 11 fields and 6 intervention points
skill="$ROOT/auto-flow/SKILL.md"
required_fields=("项目名" "用户人群" "核心场景" "平台/端" "技术栈" "不做清单" "验收标准" "部署目标" "时间预算" "外部依赖" "视觉")
missing_f=0
for f in "${required_fields[@]}"; do
  grep -q "$f" "$skill" || missing_f=$((missing_f+1))
done
if [[ $missing_f -eq 0 ]]; then
  ok "auto-flow/SKILL.md declares all 11 completeness fields"
else
  bad "auto-flow/SKILL.md missing $missing_f / 11 completeness fields"
fi

# 6 intervention points: count rows in the intervention table (numbered 1-6)
interv=$(grep -cE '^\| [1-6] \| ' "$skill" || echo 0)
if [[ "$interv" -ge 6 ]]; then
  ok "auto-flow/SKILL.md declares 6+ intervention points"
else
  bad "auto-flow/SKILL.md only declares $interv intervention points"
fi

# 5. SKILL.md references 3 reference docs
for ref in requirement-checklist.md ralph-simplifier-loop.md workflow-states.md; do
  if grep -q "references/$ref" "$skill"; then
    ok "SKILL.md references $ref"
  else
    bad "SKILL.md does not reference $ref"
  fi
done

# 6. ralph-loop SKILL.md mentions the 20-iteration default + application form
rl="$ROOT/ralph-loop/SKILL.md"
grep -q "默认上限" "$rl" && grep -q "20 轮" "$rl" \
  && ok "ralph-loop SKILL.md declares 20-iteration default" \
  || bad "ralph-loop SKILL.md missing 20-iteration default"
grep -q "续轮申请" "$rl" \
  && ok "ralph-loop SKILL.md declares ≥20 application form" \
  || bad "ralph-loop SKILL.md missing application form"

echo
if [[ $fail -eq 0 ]]; then
  echo "ALL PASS ($pass/$((pass+fail)))"
  exit 0
fi
echo "FAILED $fail / $((pass+fail))"
exit 1
