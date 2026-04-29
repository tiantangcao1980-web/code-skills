"""code-skills CLI 共享辅助:统一 JSON 输出与错误格式。

对齐 opencli 规范:
- ok=true/false 顶层字段
- error 字段固定 schema: {code, message, hint, request_id}
- 退出码标准化(EXIT_*)
- 自动发现 skill(避免硬编码列表)
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2
EXIT_DEPENDENCY = 3
EXIT_INTERRUPTED = 130

ERR_USAGE = "USAGE_ERROR"
ERR_VALIDATION = "VALIDATION_FAILED"
ERR_TARGET_EXISTS = "TARGET_EXISTS"
ERR_NOT_INSTALLED = "NOT_INSTALLED"
ERR_DEPENDENCY_MISSING = "DEPENDENCY_MISSING"
ERR_NOT_FOUND = "NOT_FOUND"
ERR_INTERNAL = "INTERNAL_ERROR"


def request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def emit_ok(payload: dict, as_json: bool) -> None:
    if as_json:
        out = {"ok": True, "data": payload, "request_id": request_id(), "ts": int(time.time())}
        print(json.dumps(out, ensure_ascii=False, indent=2))


def emit_err(code: str, message: str, hint: str = "", as_json: bool = False) -> None:
    if as_json:
        out = {
            "ok": False,
            "error": {
                "code": code,
                "message": message,
                "hint": hint,
                "request_id": request_id(),
            },
            "ts": int(time.time()),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2), file=sys.stdout)
    else:
        print(f"error: {message}", file=sys.stderr)
        if hint:
            print(f"hint:  {hint}", file=sys.stderr)


def discover_skills(root: Path) -> list[str]:
    """扫描仓库根目录下所有含 SKILL.md 的子目录,返回 skill 名称列表。"""
    return sorted(
        d.name for d in root.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists() and not d.name.startswith(".")
    )


def parse_common_flags(argv: list[str]) -> tuple[dict, list[str]]:
    """从 argv 中抽出通用 flag(--json/--quiet/--verbose/--no-color/--dry-run/--yes)。
    返回 (flags_dict, 剩余参数)。
    """
    flags = {
        "json": False,
        "quiet": False,
        "verbose": False,
        "no_color": False,
        "dry_run": False,
        "yes": False,
        "help": False,
    }
    rest: list[str] = []
    aliases = {
        "-h": "--help",
        "-q": "--quiet",
        "-v": "--verbose",
        "-y": "--yes",
    }
    for arg in argv:
        norm = aliases.get(arg, arg)
        if norm == "--json":
            flags["json"] = True
        elif norm == "--quiet":
            flags["quiet"] = True
        elif norm == "--verbose":
            flags["verbose"] = True
        elif norm == "--no-color":
            flags["no_color"] = True
        elif norm == "--dry-run":
            flags["dry_run"] = True
        elif norm == "--yes":
            flags["yes"] = True
        elif norm == "--help":
            flags["help"] = True
        else:
            rest.append(arg)
    if os.environ.get("NO_COLOR"):
        flags["no_color"] = True
    return flags, rest
