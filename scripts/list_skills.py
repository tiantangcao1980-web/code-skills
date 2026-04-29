#!/usr/bin/env python3
"""列出仓库内的 skill,支持 --json。

替代 bin/code-skills 里的 inline bash 实现。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import EXIT_OK, discover_skills, emit_ok, parse_common_flags  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def first_description_line(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.*?)(?=\n[a-z_-]+:|\n---)", text, re.S | re.M)
    if not m:
        return ""
    desc = m.group(1).strip()
    # multi-line YAML scalar (|) → take first non-empty content line
    for line in desc.splitlines():
        line = line.strip().lstrip("|").strip()
        if line and line != "|":
            return line[:120]
    return desc[:120]


def main(argv: list[str]) -> int:
    flags, _rest = parse_common_flags(argv)
    skills = discover_skills(ROOT)
    items = [
        {
            "name": s,
            "description": first_description_line(ROOT / s / "SKILL.md"),
            "has_plugin": (ROOT / s / "plugin").exists(),
        }
        for s in skills
    ]
    if flags["json"]:
        emit_ok({"skills": items, "total": len(items)}, as_json=True)
        return EXIT_OK
    print(f"Skills in this repo ({len(items)}):")
    for it in items:
        plugin = " 📦" if it["has_plugin"] else "   "
        print(f"  {it['name']:<24}{plugin} {it['description']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
