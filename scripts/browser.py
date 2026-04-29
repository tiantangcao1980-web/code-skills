#!/usr/bin/env python3
"""browser-use passthrough — `code-skills browser <subcmd>`。

不打包 browser-use(避免 Python 重依赖),只检测 + 转发。
未装时给安装提示并退出码 3。

用法:
  code-skills browser run <task>           # 用 browser-use 跑一个 LLM 驱动的浏览器任务
  code-skills browser version              # 查 browser-use 版本
  code-skills browser doctor               # 检查 browser-use 及其依赖

注:browser-use 实际工作流以 Python script 为主。本命令是最小桥接,
更复杂用法直接调 Python:
  python -m browser_use --task "Find obra/superpowers and star it"
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    EXIT_DEPENDENCY,
    EXIT_OK,
    EXIT_USAGE,
    ERR_DEPENDENCY_MISSING,
    ERR_USAGE,
    emit_err,
    parse_common_flags,
)


def ensure_browser_use(as_json: bool) -> bool:
    if shutil.which("browser-use") is None:
        # try python -m browser_use as a fallback
        if shutil.which("python3") is None:
            emit_err(
                ERR_DEPENDENCY_MISSING,
                "neither 'browser-use' CLI nor python3 in PATH",
                "install: pip3 install browser-use",
                as_json,
            )
            return False
        check = subprocess.run(
            ["python3", "-c", "import browser_use"],
            capture_output=True,
        )
        if check.returncode != 0:
            emit_err(
                ERR_DEPENDENCY_MISSING,
                "browser-use is not installed",
                "install: pip3 install browser-use",
                as_json,
            )
            return False
    return True


def main(argv: list[str]) -> int:
    flags, rest = parse_common_flags(argv)
    as_json = flags["json"]

    if flags["help"] or not rest:
        print(__doc__)
        return EXIT_OK

    sub, *args = rest

    if sub == "doctor":
        ok = ensure_browser_use(as_json)
        if ok and not as_json:
            print("browser-use: available")
        return EXIT_OK if ok else EXIT_DEPENDENCY

    if sub == "version":
        if not ensure_browser_use(as_json):
            return EXIT_DEPENDENCY
        # try CLI first, fall back to Python module
        if shutil.which("browser-use"):
            return subprocess.call(["browser-use", "--version"])
        return subprocess.call(["python3", "-c",
                                "import browser_use; print(browser_use.__version__)"])

    if sub == "run":
        if not args:
            emit_err(ERR_USAGE, "browser run requires <task>",
                     'code-skills browser run "find obra/superpowers and star it"',
                     as_json)
            return EXIT_USAGE
        if not ensure_browser_use(as_json):
            return EXIT_DEPENDENCY
        task = " ".join(args)
        if shutil.which("browser-use"):
            return subprocess.call(["browser-use", "--task", task])
        # Python module fallback
        return subprocess.call([
            "python3", "-c",
            f"import asyncio; from browser_use import Agent; "
            f"asyncio.run(Agent(task={task!r}).run())",
        ])

    emit_err(ERR_USAGE, f"unknown browser subcommand: {sub}",
             "valid: run / version / doctor", as_json)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
