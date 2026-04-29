#!/usr/bin/env bash
# Example 03 self-test: design spec / tokens / copy validity.
set -euo pipefail

EX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXP="$EX_DIR/expected"
pass=0
fail=0
ok()  { echo "[ OK ] $1"; pass=$((pass+1)); }
bad() { echo "[FAIL] $1"; fail=$((fail+1)); }

# 1. DESIGN.md sections (≥8 of the 10 standard headings)
required_sections=("Aesthetic Direction" "Voice & Tone" "Color" "Typography"
                   "Spacing" "Layout" "Motion" "Accessibility")
missing=0
for s in "${required_sections[@]}"; do
  if ! grep -q "## .* ${s}" "$EXP/DESIGN.md" && ! grep -q "## ${s}" "$EXP/DESIGN.md"; then
    missing=$((missing+1))
  fi
done
if [[ $missing -eq 0 ]]; then
  ok "DESIGN.md: all ${#required_sections[@]} required sections present"
else
  bad "DESIGN.md missing $missing required sections"
fi

# 2. design-tokens.json is valid JSON + has color/spacing/radius groups
python3 -c "
import json, sys
d = json.load(open('$EXP/design-tokens.json'))
for g in ('color','spacing','radius'):
    assert g in d, f'missing token group: {g}'
assert 'accent' in d['color'], 'color.accent required'
assert d['color']['accent']['value'].startswith('#'), 'accent must be hex'
print('OK')
" >/dev/null 2>&1 \
  && ok "design-tokens.json: valid JSON with color/spacing/radius" \
  || bad "design-tokens.json invalid or missing required groups"

# 3. copy.json: 5 keys + no banned words
python3 -c "
import json
d = json.load(open('$EXP/copy.json'))
required = ['hero_title','cta_primary','empty_state','error_state','success_state']
for k in required:
    assert k in d, f'missing key: {k}'
banned = ['极致','超快','极速','亲','哦','操作成功','暂无数据','立即体验']
for k, v in d.items():
    if k.startswith('_'): continue
    for w in banned:
        assert w not in v, f'banned word \"{w}\" found in {k}: {v}'
print('OK')
" >/dev/null 2>&1 \
  && ok "copy.json: 5 keys present, zero banned words" \
  || bad "copy.json missing keys or contains banned words"

# 4. index.html: doctype + title + main heading
grep -qi '<!DOCTYPE html>' "$EXP/index.html" \
  && grep -q '<title>' "$EXP/index.html" \
  && grep -q '<h1>' "$EXP/index.html" \
  && ok "index.html: doctype + title + h1 present" \
  || bad "index.html missing required tags"

# 5. index.html actually uses tokens (sanity: hex from tokens appears in CSS)
hex="$(python3 -c "import json; print(json.load(open('$EXP/design-tokens.json'))['color']['accent']['value'])")"
grep -qi "$hex" "$EX_DIR/expected/index.html" \
  && ok "index.html uses --color-accent value ($hex) from tokens" \
  || bad "index.html does not reference accent hex from tokens"

echo
if [[ $fail -eq 0 ]]; then
  echo "ALL PASS ($pass/$((pass+fail)))"
  exit 0
fi
echo "FAILED $fail / $((pass+fail))"
exit 1
