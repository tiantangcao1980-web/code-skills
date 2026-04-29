#!/usr/bin/env python3
"""Remotion passthrough — `code-skills demo <subcmd>`。

不打包 remotion(避免依赖膨胀),只检测它是否在 PATH 里,然后转发参数。
未装时给安装提示并退出码 3(EXIT_DEPENDENCY)。

用法:
  code-skills demo init <project>          # 初始化新 demo 项目(npx create-video)
  code-skills demo render <id> [<file>]    # 渲染视频
  code-skills demo studio                  # 启动 Remotion Studio
  code-skills demo preview                 # 启动预览(等同 studio,旧名)
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


def ensure_npx(as_json: bool) -> bool:
    if shutil.which("npx") is None:
        emit_err(
            ERR_DEPENDENCY_MISSING,
            "npx not in PATH",
            "install Node.js (brew install node) — npx ships with it",
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

    if sub == "init":
        if not args:
            emit_err(ERR_USAGE, "demo init requires <project> name",
                     "code-skills demo init my-demo", as_json)
            return EXIT_USAGE
        if not ensure_npx(as_json):
            return EXIT_DEPENDENCY
        project = args[0]
        return subprocess.call(["npx", "--yes", "create-video@latest", project])

    if sub in {"studio", "preview"}:
        if not ensure_npx(as_json):
            return EXIT_DEPENDENCY
        return subprocess.call(["npx", "--yes", "remotion", "studio"])

    if sub == "render":
        if not ensure_npx(as_json):
            return EXIT_DEPENDENCY
        if not args:
            emit_err(ERR_USAGE, "demo render requires <composition-id>",
                     "code-skills demo render Main out.mp4", as_json)
            return EXIT_USAGE
        return subprocess.call(["npx", "--yes", "remotion", "render", *args])

    emit_err(ERR_USAGE, f"unknown demo subcommand: {sub}",
             "valid: init / render / studio / preview", as_json)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
