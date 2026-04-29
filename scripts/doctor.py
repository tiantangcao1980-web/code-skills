#!/usr/bin/env python3
"""检测外部 CLI 工具的安装情况(零依赖,只用 shutil.which)。

只检查"是否在 PATH 里",不检查版本兼容性(那是各自工具自己的事)。
退出码 0 = 检测完成(无论结果);1 = 缺少必装工具(目前没有必装项)。
"""
from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    bin: str
    purpose: str
    install_hint: str
    integration: str


TOOLS: list[Tool] = [
    Tool(
        name="git",
        bin="git",
        purpose="version control (clone/pull external integrations)",
        install_hint="brew install git  # or use Apple Command Line Tools",
        integration="baseline",
    ),
    Tool(
        name="node",
        bin="node",
        purpose="run remotion / npm-based CLIs",
        install_hint="brew install node  # or fnm install --lts",
        integration="prerequisite for remotion",
    ),
    Tool(
        name="npx",
        bin="npx",
        purpose="invoke remotion without global install",
        install_hint="bundled with node",
        integration="code-skills demo",
    ),
    Tool(
        name="python3",
        bin="python3",
        purpose="run browser-use / this CLI itself",
        install_hint="brew install python@3.11",
        integration="code-skills browser",
    ),
    Tool(
        name="pip",
        bin="pip3",
        purpose="install browser-use",
        install_hint="bundled with python3",
        integration="prerequisite for browser-use",
    ),
    Tool(
        name="browser-use",
        bin="browser-use",
        purpose="LLM-driven browser automation",
        install_hint="pip3 install browser-use",
        integration="code-skills browser",
    ),
    Tool(
        name="remotion",
        bin="remotion",
        purpose="programmatic video generation",
        install_hint="cd <project> && npm i remotion  # or use npx remotion",
        integration="code-skills demo",
    ),
    Tool(
        name="playwright",
        bin="playwright",
        purpose="E2E browser testing (used by browser verify)",
        install_hint="npx playwright install",
        integration="design-dev-flow act 6",
    ),
    Tool(
        name="ffmpeg",
        bin="ffmpeg",
        purpose="video post-processing for remotion outputs",
        install_hint="brew install ffmpeg",
        integration="code-skills demo (optional)",
    ),
]


def check(tool: Tool) -> tuple[bool, str]:
    path = shutil.which(tool.bin)
    return (path is not None, path or "")


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    results = []
    for t in TOOLS:
        ok, path = check(t)
        results.append({
            "name": t.name,
            "bin": t.bin,
            "installed": ok,
            "path": path,
            "purpose": t.purpose,
            "install_hint": t.install_hint,
            "integration": t.integration,
        })

    if as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    print("Tool                Status        Path / Hint")
    print("-" * 78)
    for r in results:
        mark = "✓" if r["installed"] else "✗"
        loc = r["path"] if r["installed"] else f"→ {r['install_hint']}"
        print(f"{r['name']:<18}  {mark:<10}  {loc}")
        print(f"{'':<18}  {'':<10}  ({r['integration']})")

    missing = [r["name"] for r in results if not r["installed"]]
    print()
    if missing:
        print(f"missing: {', '.join(missing)}")
        print("(none of these are mandatory; install only what you actually need)")
    else:
        print("all tools available")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
