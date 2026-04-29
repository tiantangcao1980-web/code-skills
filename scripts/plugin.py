#!/usr/bin/env python3
"""统一管理嵌入式 plugin 的安装/卸载/状态。

委托给每个 skill 自己的 install-plugin.sh,本脚本只做枚举与转发。

用法:
  python3 scripts/plugin.py list                      # 列出所有可装 plugin
  python3 scripts/plugin.py status [<name>]           # 查看状态
  python3 scripts/plugin.py install <name> [--copy]   # 安装(默认软链)
  python3 scripts/plugin.py uninstall <name>          # 卸载
  python3 scripts/plugin.py install --all             # 全部安装

退出码: 0 成功 / 1 运行时错 / 2 用法错 / 3 缺依赖
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    EXIT_OK,
    EXIT_RUNTIME,
    EXIT_USAGE,
    ERR_NOT_FOUND,
    ERR_USAGE,
    emit_err,
    emit_ok,
    parse_common_flags,
)

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = {
    "ralph-loop": {
        "skill": "ralph-loop",
        "script": ROOT / "ralph-loop" / "scripts" / "install-plugin.sh",
        "summary": "Stop-hook based loop with /ralph-loop slash command",
        "license": "Apache-2.0 (Anthropic)",
    },
    "code-simplifier": {
        "skill": "code-simplifier",
        "script": ROOT / "code-simplifier" / "scripts" / "install-plugin.sh",
        "summary": "Anthropic-authored simplifier agent (subagent_type=code-simplifier)",
        "license": "Apache-2.0 (Anthropic)",
    },
}


def cmd_list(as_json: bool) -> int:
    items = [
        {
            "name": k,
            "skill": v["skill"],
            "summary": v["summary"],
            "license": v["license"],
            "script": str(v["script"].relative_to(ROOT)),
        }
        for k, v in PLUGINS.items()
    ]
    if as_json:
        emit_ok({"plugins": items}, as_json=True)
    else:
        print(f"{'name':<18} {'license':<22} summary")
        print("-" * 78)
        for it in items:
            print(f"{it['name']:<18} {it['license']:<22} {it['summary']}")
    return EXIT_OK


def cmd_status(name: str | None, as_json: bool) -> int:
    targets = [name] if name else list(PLUGINS.keys())
    statuses = []
    for n in targets:
        if n not in PLUGINS:
            emit_err(ERR_NOT_FOUND, f"unknown plugin: {n}", "see 'plugin list'", as_json)
            return EXIT_USAGE
        proc = subprocess.run(
            ["bash", str(PLUGINS[n]["script"]), "status"],
            capture_output=True, text=True,
        )
        statuses.append({
            "name": n,
            "output": (proc.stdout or proc.stderr).strip(),
            "exit_code": proc.returncode,
        })
    if as_json:
        emit_ok({"statuses": statuses}, as_json=True)
    else:
        for s in statuses:
            print(f"== {s['name']} ==")
            print(s["output"])
            print()
    return EXIT_OK


def cmd_install(name: str | None, mode: str, all_: bool, as_json: bool) -> int:
    if not all_ and not name:
        emit_err(ERR_USAGE, "install requires <name> or --all", "see 'plugin --help'", as_json)
        return EXIT_USAGE
    if all_:
        targets = list(PLUGINS.keys())
    else:
        if name not in PLUGINS:
            emit_err(ERR_NOT_FOUND, f"unknown plugin: {name}", "see 'plugin list'", as_json)
            return EXIT_USAGE
        targets = [name]

    results = []
    for n in targets:
        cmd = ["bash", str(PLUGINS[n]["script"]), "install"]
        if mode == "copy":
            cmd.append("--copy")
        else:
            cmd.append("--symlink")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        results.append({
            "name": n,
            "exit_code": proc.returncode,
            "output": (proc.stdout or proc.stderr).strip(),
        })
        if not as_json:
            print(f"== {n} ==")
            print((proc.stdout or proc.stderr).rstrip())
            print()

    failed = [r for r in results if r["exit_code"] != 0]
    if as_json:
        if failed:
            emit_err(ERR_RUNTIME := "RUNTIME_ERROR", f"{len(failed)} plugin install(s) failed",
                     "; ".join(r["name"] for r in failed), as_json=True)
            return EXIT_RUNTIME
        emit_ok({"installed": results}, as_json=True)
    return EXIT_RUNTIME if failed else EXIT_OK


def cmd_uninstall(name: str | None, all_: bool, as_json: bool) -> int:
    if not all_ and not name:
        emit_err(ERR_USAGE, "uninstall requires <name> or --all", "see 'plugin --help'", as_json)
        return EXIT_USAGE
    targets = list(PLUGINS.keys()) if all_ else [name]
    if not all_ and name not in PLUGINS:
        emit_err(ERR_NOT_FOUND, f"unknown plugin: {name}", "see 'plugin list'", as_json)
        return EXIT_USAGE

    results = []
    for n in targets:
        proc = subprocess.run(
            ["bash", str(PLUGINS[n]["script"]), "uninstall"],
            capture_output=True, text=True,
        )
        results.append({"name": n, "exit_code": proc.returncode,
                        "output": (proc.stdout or proc.stderr).strip()})
        if not as_json:
            print(f"== {n} ==")
            print((proc.stdout or proc.stderr).rstrip())
            print()
    if as_json:
        emit_ok({"uninstalled": results}, as_json=True)
    failed = [r for r in results if r["exit_code"] != 0]
    return EXIT_RUNTIME if failed else EXIT_OK


def main(argv: list[str]) -> int:
    flags, rest = parse_common_flags(argv)
    if flags["help"] or not rest:
        print(__doc__)
        return EXIT_OK

    cmd, *args = rest
    as_json = flags["json"]

    if cmd == "list":
        return cmd_list(as_json)

    if cmd == "status":
        return cmd_status(args[0] if args else None, as_json)

    if cmd == "install":
        all_ = "--all" in args
        positional = [a for a in args if not a.startswith("-")]
        mode = "copy" if "--copy" in args else "symlink"
        return cmd_install(positional[0] if positional else None, mode, all_, as_json)

    if cmd == "uninstall":
        all_ = "--all" in args
        positional = [a for a in args if not a.startswith("-")]
        return cmd_uninstall(positional[0] if positional else None, all_, as_json)

    emit_err(ERR_USAGE, f"unknown subcommand: {cmd}",
             "valid: list / status / install / uninstall", as_json)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
