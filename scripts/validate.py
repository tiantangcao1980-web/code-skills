#!/usr/bin/env python3
"""校验仓库内每个 skill 的结构与一致性。

检查项(对齐 skill-authoring/references/checklist.md):
- 文件夹名 == frontmatter.name
- name 仅含小写字母/数字/连字符
- description 同时含"做什么"和"何时触发"信号
- agents/openai.yaml 存在且 display_name 不为空
- references/ 下文件均被 SKILL.md 引用(无孤儿)

支持 --json,对齐 opencli 错误格式。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    EXIT_OK,
    EXIT_RUNTIME,
    ERR_VALIDATION,
    discover_skills,
    emit_err,
    emit_ok,
    parse_common_flags,
)

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TRIGGER_HINTS = ["触发词", "trigger", "适合", "适用", "when to use", "适用阶段"]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in block.splitlines():
        if line and not line.startswith(" ") and ":" in line:
            if key is not None:
                out[key] = "\n".join(buf).strip()
            k, _, v = line.partition(":")
            key = k.strip()
            buf = [v.lstrip()]
        else:
            buf.append(line)
    if key is not None:
        out[key] = "\n".join(buf).strip()
    return out


def check_skill(folder: Path) -> list[str]:
    errors: list[str] = []
    skill_md = folder / "SKILL.md"
    if not skill_md.exists():
        return ["missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter.name missing")
    elif name != folder.name:
        errors.append(f"frontmatter.name '{name}' != folder '{folder.name}'")
    elif not NAME_RE.match(name):
        errors.append(f"frontmatter.name '{name}' must be lowercase[a-z0-9-]")

    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter.description missing")
    else:
        low = desc.lower()
        if not any(h in low for h in TRIGGER_HINTS):
            errors.append("description lacks trigger hints (e.g. '触发词'/'trigger')")
        if len(desc) < 40:
            errors.append("description too short (< 40 chars)")

    yaml_path = folder / "agents" / "openai.yaml"
    if not yaml_path.exists():
        errors.append("agents/openai.yaml missing")
    else:
        y = yaml_path.read_text(encoding="utf-8")
        if "display_name:" not in y or "short_description:" not in y:
            errors.append("openai.yaml missing display_name/short_description")

    refs_dir = folder / "references"
    if refs_dir.exists():
        for f in refs_dir.iterdir():
            if f.is_file() and f.suffix == ".md":
                rel = f"references/{f.name}"
                if rel not in text:
                    errors.append(f"orphan reference: {rel} not linked from SKILL.md")

    return errors


def main(argv: list[str]) -> int:
    flags, _rest = parse_common_flags(argv)
    as_json = flags["json"]

    skills = discover_skills(ROOT)
    results = []
    failed = 0
    for s in skills:
        folder = ROOT / s
        errs = check_skill(folder)
        results.append({"name": s, "ok": not errs, "errors": errs})
        if errs:
            failed += 1

    if as_json:
        if failed:
            emit_err(
                ERR_VALIDATION,
                f"{failed}/{len(skills)} skill(s) failed validation",
                "see 'errors' array per skill in stderr or run without --json",
                as_json=True,
            )
            return EXIT_RUNTIME
        emit_ok({"skills": results, "total": len(skills), "passed": len(skills)}, as_json=True)
        return EXIT_OK

    for r in results:
        if r["ok"]:
            print(f"[ OK ] {r['name']}")
        else:
            print(f"[FAIL] {r['name']}")
            for e in r["errors"]:
                print(f"   - {e}")
    print()
    print(f"summary: {len(skills) - failed}/{len(skills)} passed")
    return EXIT_RUNTIME if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
