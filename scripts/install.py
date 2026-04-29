#!/usr/bin/env python3
"""把仓库内的 skill 装到 ~/.claude/skills/。

模式:
- --symlink (默认): 软链
- --copy: 复制
- --uninstall: 卸载(只删本仓库装上去的链/目录)

支持 --json,对齐 opencli。skill 列表自动发现(无需硬编码)。
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    EXIT_OK,
    EXIT_RUNTIME,
    ERR_TARGET_EXISTS,
    discover_skills,
    emit_err,
    emit_ok,
)

ROOT = Path(__file__).resolve().parent.parent
TARGET_BASE = Path.home() / ".claude" / "skills"


def install_one(name: str, mode: str) -> dict:
    src = ROOT / name
    dst = TARGET_BASE / name

    if not src.exists():
        return {"name": name, "ok": False, "action": "skip", "reason": "source not found"}

    if dst.exists() or dst.is_symlink():
        if dst.is_symlink() and Path(os.readlink(dst)) == src:
            return {"name": name, "ok": True, "action": "already-installed", "target": str(dst)}
        return {
            "name": name,
            "ok": False,
            "action": "refuse",
            "reason": f"target exists at {dst}",
        }

    if mode == "symlink":
        os.symlink(src, dst)
        return {"name": name, "ok": True, "action": "symlinked", "target": str(dst)}
    if mode == "copy":
        shutil.copytree(src, dst)
        return {"name": name, "ok": True, "action": "copied", "target": str(dst)}
    return {"name": name, "ok": False, "action": "error", "reason": f"unknown mode {mode}"}


def uninstall_one(name: str) -> dict:
    dst = TARGET_BASE / name
    if not dst.exists() and not dst.is_symlink():
        return {"name": name, "ok": True, "action": "not-installed"}
    if dst.is_symlink():
        if Path(os.readlink(dst)) != ROOT / name:
            return {
                "name": name,
                "ok": True,
                "action": "skip",
                "reason": "symlink points elsewhere, not removed",
            }
        dst.unlink()
        return {"name": name, "ok": True, "action": "unlinked", "target": str(dst)}
    return {"name": name, "ok": True, "action": "skip", "reason": "not a symlink (manual removal)"}


def main() -> int:
    p = argparse.ArgumentParser(description="Install code-skills into ~/.claude/skills/")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--symlink", action="store_const", dest="mode", const="symlink")
    g.add_argument("--copy", action="store_const", dest="mode", const="copy")
    g.add_argument("--uninstall", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    TARGET_BASE.mkdir(parents=True, exist_ok=True)
    mode = args.mode or "symlink"
    skills = discover_skills(ROOT)
    results = []
    failed = 0
    for s in skills:
        r = uninstall_one(s) if args.uninstall else install_one(s, mode)
        results.append(r)
        if not r["ok"]:
            failed += 1

    if args.json:
        if failed:
            emit_err(
                ERR_TARGET_EXISTS,
                f"{failed}/{len(skills)} install(s) failed",
                "see results array",
                as_json=True,
            )
            return EXIT_RUNTIME
        emit_ok(
            {
                "results": results,
                "mode": "uninstall" if args.uninstall else mode,
                "target": str(TARGET_BASE),
            },
            as_json=True,
        )
        return EXIT_OK

    for r in results:
        mark = "[OK]  " if r["ok"] else "[FAIL]"
        line = f"{mark} {r['name']}: {r['action']}"
        if "target" in r:
            line += f" -> {r['target']}"
        if "reason" in r:
            line += f" ({r['reason']})"
        print(line)
    print()
    print(f"target: {TARGET_BASE}")
    print(f"mode: {'uninstall' if args.uninstall else mode}")
    return EXIT_RUNTIME if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
