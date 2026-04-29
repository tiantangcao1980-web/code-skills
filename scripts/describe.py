#!/usr/bin/env python3
"""输出整个 code-skills CLI 的命令树 schema(对齐 opencli 规范)。

让其它 agent / CLI 能通过一次调用就发现所有命令、参数、退出码、错误码。

用法:
  python3 scripts/describe.py            # 人类可读
  python3 scripts/describe.py --json     # 机器可读(opencli schema)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import EXIT_OK, discover_skills, parse_common_flags  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.3.0"

SCHEMA = {
    "opencli": "0.1",
    "name": "code-skills",
    "version": VERSION,
    "description": "Comprehensive design + dev skill suite for Claude Code, with embedded plugins and discovery schema.",
    "homepage": "https://github.com/<your-org>/code-skills",
    "license": "MIT (skills) + Apache-2.0 (embedded plugins)",
    "common_flags": [
        {"name": "--help", "alias": "-h", "type": "bool", "description": "Show command help"},
        {"name": "--json", "type": "bool", "description": "Emit machine-readable JSON output"},
        {"name": "--quiet", "alias": "-q", "type": "bool", "description": "Suppress non-error output"},
        {"name": "--verbose", "alias": "-v", "type": "bool", "description": "Verbose logging"},
        {"name": "--no-color", "type": "bool", "description": "Disable ANSI colors"},
        {"name": "--dry-run", "type": "bool", "description": "Show what would happen, don't execute"},
        {"name": "--yes", "alias": "-y", "type": "bool", "description": "Skip confirmation prompts"},
    ],
    "exit_codes": {
        "0": "success",
        "1": "runtime error (validation failed, install failed, etc.)",
        "2": "usage error (bad argument, unknown command)",
        "3": "missing dependency (external tool not installed)",
        "130": "interrupted (Ctrl-C / SIGINT)",
    },
    "error_codes": {
        "USAGE_ERROR":         "Bad argument or unknown command",
        "VALIDATION_FAILED":   "Skill structure check failed",
        "TARGET_EXISTS":       "Install target already exists",
        "NOT_INSTALLED":       "Skill / plugin is not installed",
        "DEPENDENCY_MISSING":  "Required external tool not in PATH",
        "NOT_FOUND":           "Resource (skill, plugin, file) not found",
        "INTERNAL_ERROR":      "Unexpected error inside the CLI",
    },
    "commands": [
        {
            "name": "validate",
            "summary": "Validate skill structure and consistency",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0", "1", "2"],
            "examples": ["bin/code-skills validate", "bin/code-skills validate --json"],
        },
        {
            "name": "install",
            "summary": "Install skills into ~/.claude/skills/",
            "args": [],
            "flags": [
                {"name": "--symlink", "type": "bool", "description": "Symlink (default)"},
                {"name": "--copy", "type": "bool", "description": "Copy instead of symlink"},
                {"name": "--json", "type": "bool"},
            ],
            "exits": ["0", "1", "2"],
            "examples": ["bin/code-skills install", "bin/code-skills install --copy"],
        },
        {
            "name": "uninstall",
            "summary": "Uninstall skills (only removes symlinks pointing to this repo)",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0", "1"],
            "examples": ["bin/code-skills uninstall"],
        },
        {
            "name": "list",
            "summary": "List skills in this repo",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0"],
        },
        {
            "name": "doctor",
            "summary": "Detect external tools needed by skills (browser-use, remotion, jq, etc.)",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0"],
        },
        {
            "name": "describe",
            "summary": "Print this CLI's command tree schema (opencli)",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0"],
        },
        {
            "name": "version",
            "summary": "Print CLI version",
            "args": [],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0"],
        },
        {
            "name": "plugin",
            "summary": "Manage embedded plugins (ralph-loop, code-simplifier)",
            "args": [{"name": "subcommand", "type": "string", "values": ["list", "status", "install", "uninstall"]}],
            "flags": [
                {"name": "--copy", "type": "bool"},
                {"name": "--all", "type": "bool"},
                {"name": "--json", "type": "bool"},
            ],
            "exits": ["0", "1", "2"],
            "examples": [
                "bin/code-skills plugin list",
                "bin/code-skills plugin install ralph-loop",
                "bin/code-skills plugin install --all",
                "bin/code-skills plugin status",
            ],
        },
        {
            "name": "demo",
            "summary": "Remotion passthrough — programmatic video generation",
            "args": [{"name": "subcommand", "type": "string",
                      "values": ["init", "render", "studio", "preview"]}],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0", "2", "3"],
            "examples": [
                "bin/code-skills demo init my-demo",
                "bin/code-skills demo render Main out.mp4",
                "bin/code-skills demo studio",
            ],
        },
        {
            "name": "browser",
            "summary": "browser-use passthrough — LLM-driven browser automation",
            "args": [{"name": "subcommand", "type": "string",
                      "values": ["run", "version", "doctor"]}],
            "flags": [{"name": "--json", "type": "bool"}],
            "exits": ["0", "2", "3"],
            "examples": [
                'bin/code-skills browser run "find obra/superpowers and star it"',
                "bin/code-skills browser doctor",
            ],
        },
        {
            "name": "cli-init",
            "summary": "Scaffold a new opencli-aligned CLI project",
            "args": [{"name": "name", "type": "string", "required": True}],
            "flags": [
                {"name": "--lang", "type": "string", "values": ["python"], "default": "python"},
                {"name": "--force", "type": "bool"},
                {"name": "--json", "type": "bool"},
            ],
            "exits": ["0", "1", "2"],
            "examples": ["bin/code-skills cli-init my-cli", "bin/code-skills cli-init my-cli --force"],
        },
        {
            "name": "help",
            "summary": "Show CLI help",
            "args": [{"name": "command", "type": "string", "required": False}],
            "flags": [],
            "exits": ["0"],
        },
    ],
    "embedded_plugins": [
        {
            "name": "ralph-loop",
            "version": "1.0.0",
            "source": "claude-plugins-official",
            "license": "Apache-2.0",
            "install_path_template": "~/.claude/plugins/code-skills/ralph-loop",
        },
        {
            "name": "code-simplifier",
            "version": "1.0.0",
            "source": "claude-plugins-official",
            "license": "Apache-2.0",
            "install_path_template": "~/.claude/plugins/code-skills/code-simplifier",
        },
    ],
}


def _populate_skills(schema: dict) -> dict:
    """运行时扫描仓库,把 skills 字段填入实际发现的 skill 列表。"""
    schema["skills"] = [{"name": s} for s in discover_skills(ROOT)]
    return schema


def main(argv: list[str]) -> int:
    flags, _rest = parse_common_flags(argv)
    schema = _populate_skills(dict(SCHEMA))
    if flags["json"]:
        print(json.dumps(schema, indent=2, ensure_ascii=False))
        return EXIT_OK

    print(f"{SCHEMA['name']} v{SCHEMA['version']}")
    print(SCHEMA["description"])
    print()
    print("Commands:")
    for c in SCHEMA["commands"]:
        print(f"  {c['name']:<12} {c['summary']}")
    print()
    print("Common flags (every command supports these):")
    for f in SCHEMA["common_flags"]:
        alias = f" / {f['alias']}" if "alias" in f else ""
        print(f"  {f['name']}{alias:<8}  {f['description']}")
    print()
    print("Exit codes:")
    for code, desc in SCHEMA["exit_codes"].items():
        print(f"  {code:<4} {desc}")
    print()
    print("Embedded plugins:")
    for p in schema["embedded_plugins"]:
        print(f"  {p['name']} v{p['version']} ({p['license']})")
    print()
    print(f"Skills ({len(schema['skills'])}):")
    for s in schema["skills"]:
        print(f"  {s['name']}")
    print()
    print("(For machine-readable schema: bin/code-skills describe --json)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
