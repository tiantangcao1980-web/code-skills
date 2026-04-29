#!/usr/bin/env python3
"""管理 vendor/cowork/ 下的 19 个领域插件。

用法:
  bin/code-skills vendor list                       列出所有 plugin + skill 计数
  bin/code-skills vendor list --json                机器可读
  bin/code-skills vendor status [<plugin>]          查看激活状态(在 ~/.claude/plugins/code-skills-vendor/ 下)
  bin/code-skills vendor install <plugin>           把指定 plugin 软链/复制到 ~/.claude/plugins/code-skills-vendor/
  bin/code-skills vendor install --all-vendored     把全部 15 个 vendored 全装上(跳过 placeholder)
  bin/code-skills vendor uninstall <plugin>         卸载
  bin/code-skills vendor diff                       对比 vendor 版本 vs 用户机器 Cowork cache 是否有更新
  bin/code-skills vendor sync                       从 Cowork cache 同步更新(仅对 LICENSE 完整的)

退出码: 0 成功 / 1 运行时错 / 2 用法错 / 3 缺依赖
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    EXIT_OK,
    EXIT_RUNTIME,
    EXIT_USAGE,
    ERR_NOT_FOUND,
    ERR_TARGET_EXISTS,
    ERR_USAGE,
    emit_err,
    emit_ok,
    parse_common_flags,
)

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor" / "cowork"
LOCK_FILE = VENDOR / "VERSIONS.lock"
INSTALL_BASE = Path.home() / ".claude" / "plugins" / "code-skills-vendor"

# 上游 Cowork cache 路径(用户机器上)
COWORK_CACHE_CANDIDATES = [
    Path.home() / "Library/Application Support/Claude/local-agent-mode-sessions",
]


def load_lock() -> dict:
    if not LOCK_FILE.exists():
        return {"plugins": {}}
    return json.loads(LOCK_FILE.read_text())


def find_cowork_cache() -> Path | None:
    """在用户机器上找 Cowork knowledge-work-plugins 目录(最新 session)。"""
    for base in COWORK_CACHE_CANDIDATES:
        if not base.exists():
            continue
        for session in base.iterdir():
            if not session.is_dir():
                continue
            for sub in session.iterdir():
                kw = sub / "cowork_plugins" / "cache" / "knowledge-work-plugins"
                if kw.exists():
                    return kw
    return None


def cmd_list(as_json: bool) -> int:
    lock = load_lock()
    plugins = lock.get("plugins", {})
    if as_json:
        emit_ok({"plugins": plugins, "snapshot_date": lock.get("snapshot_date")}, as_json=True)
        return EXIT_OK
    print(f"Vendor cowork ({len(plugins)} plugins, snapshot {lock.get('snapshot_date', '?')}):")
    print(f"{'plugin':<28} {'status':<12} {'license':<22} skills")
    print("-" * 80)
    for name, meta in sorted(plugins.items()):
        status = "✅" if meta["status"] == "vendored" else "📋"
        lic = (meta.get("license") or "")[:20]
        print(f"  {name:<26} {status} {meta['status']:<10} {lic:<22} {meta['skill_count']}")
    return EXIT_OK


def cmd_status(name: str | None, as_json: bool) -> int:
    lock = load_lock()
    targets = [name] if name else list(lock["plugins"].keys())
    statuses = []
    for n in targets:
        if n not in lock["plugins"]:
            emit_err(ERR_NOT_FOUND, f"unknown plugin: {n}",
                     "see 'vendor list'", as_json)
            return EXIT_USAGE
        ver = lock["plugins"][n]["version"]
        installed_path = INSTALL_BASE / n
        installed = installed_path.exists() or installed_path.is_symlink()
        target = ""
        if installed_path.is_symlink():
            target = os.readlink(installed_path)
        statuses.append({
            "name": n,
            "vendored_version": ver,
            "vendor_status": lock["plugins"][n]["status"],
            "installed": installed,
            "install_path": str(installed_path) if installed else None,
            "symlink_target": target if target else None,
        })
    if as_json:
        emit_ok({"statuses": statuses}, as_json=True)
        return EXIT_OK
    for s in statuses:
        mark = "🟢 installed" if s["installed"] else "⚪️ not installed"
        print(f"{s['name']:<28} v{s['vendored_version']:<10} {mark}")
    return EXIT_OK


def cmd_install(name: str | None, all_vendored: bool, mode: str, as_json: bool) -> int:
    lock = load_lock()
    if not name and not all_vendored:
        emit_err(ERR_USAGE, "install requires <plugin> or --all-vendored",
                 "see 'vendor --help'", as_json)
        return EXIT_USAGE

    if all_vendored:
        targets = [n for n, m in lock["plugins"].items() if m["status"] == "vendored"]
    else:
        if name not in lock["plugins"]:
            emit_err(ERR_NOT_FOUND, f"unknown plugin: {name}",
                     "see 'vendor list'", as_json)
            return EXIT_USAGE
        if lock["plugins"][name]["status"] != "vendored":
            emit_err(ERR_USAGE,
                     f"plugin '{name}' is placeholder-only (no LICENSE)",
                     "install Cowork and activate it from there", as_json)
            return EXIT_USAGE
        targets = [name]

    INSTALL_BASE.mkdir(parents=True, exist_ok=True)
    results = []
    for n in targets:
        ver = lock["plugins"][n]["version"]
        src = VENDOR / n / ver
        dst = INSTALL_BASE / n
        if dst.exists() or dst.is_symlink():
            results.append({"name": n, "ok": True, "action": "already-installed"})
            continue
        if mode == "copy":
            shutil.copytree(src, dst)
            results.append({"name": n, "ok": True, "action": "copied", "target": str(dst)})
        else:
            os.symlink(src, dst)
            results.append({"name": n, "ok": True, "action": "symlinked", "target": str(dst)})

    if as_json:
        emit_ok({"installed": results}, as_json=True)
        return EXIT_OK
    for r in results:
        print(f"[OK]  {r['name']}: {r['action']}", r.get("target", ""))
    print(f"\ntarget base: {INSTALL_BASE}")
    print("note: restart Claude Code session to load plugins")
    return EXIT_OK


def cmd_uninstall(name: str, as_json: bool) -> int:
    lock = load_lock()
    if name not in lock["plugins"]:
        emit_err(ERR_NOT_FOUND, f"unknown plugin: {name}", "see 'vendor list'", as_json)
        return EXIT_USAGE
    dst = INSTALL_BASE / name
    if not dst.exists() and not dst.is_symlink():
        if as_json:
            emit_ok({"name": name, "action": "not-installed"}, as_json=True)
        else:
            print(f"[SKIP] {name}: not installed")
        return EXIT_OK
    if dst.is_symlink():
        # 只删指向本仓库 vendor 的链
        target = Path(os.readlink(dst))
        expected = VENDOR / name / lock["plugins"][name]["version"]
        if target.resolve() != expected.resolve():
            if as_json:
                emit_err(ERR_USAGE, f"symlink points elsewhere",
                         f"expected {expected}, got {target}", as_json=True)
            else:
                print(f"[SKIP] {name}: symlink points elsewhere ({target})")
            return EXIT_OK
        dst.unlink()
    else:
        shutil.rmtree(dst)
    if as_json:
        emit_ok({"name": name, "action": "uninstalled"}, as_json=True)
    else:
        print(f"[OK]  {name}: uninstalled")
    return EXIT_OK


def cmd_diff(as_json: bool) -> int:
    """比较 vendor 内容 vs 上游 Cowork cache。"""
    upstream = find_cowork_cache()
    if not upstream:
        emit_err(ERR_USAGE, "Cowork cache not found on this machine",
                 "this command requires Claude Desktop with knowledge-work-plugins", as_json)
        return EXIT_USAGE

    lock = load_lock()
    diffs = []
    for name, meta in lock["plugins"].items():
        ver = meta["version"]
        ours = VENDOR / name / ver
        theirs = upstream / name / ver
        if not theirs.exists():
            diffs.append({"name": name, "status": "upstream-missing"})
            continue
        # 简单文件计数对比
        ours_files = sorted(p.relative_to(ours).as_posix()
                            for p in ours.rglob("*") if p.is_file())
        theirs_files = sorted(p.relative_to(theirs).as_posix()
                              for p in theirs.rglob("*") if p.is_file())
        if ours_files == theirs_files:
            # 内容比对(取 SKILL.md mtime 粗判)
            theirs_mtimes = [(theirs / f).stat().st_mtime for f in theirs_files
                             if f.endswith("SKILL.md")]
            ours_mtimes = [(ours / f).stat().st_mtime for f in ours_files
                           if f.endswith("SKILL.md")]
            if theirs_mtimes and (max(theirs_mtimes) > max(ours_mtimes) + 1):
                diffs.append({"name": name, "status": "upstream-newer"})
            else:
                diffs.append({"name": name, "status": "in-sync"})
        else:
            added = set(theirs_files) - set(ours_files)
            removed = set(ours_files) - set(theirs_files)
            diffs.append({
                "name": name, "status": "files-differ",
                "added": sorted(added)[:5],
                "removed": sorted(removed)[:5],
            })

    if as_json:
        emit_ok({"upstream": str(upstream), "diffs": diffs}, as_json=True)
        return EXIT_OK
    print(f"upstream: {upstream}\n")
    for d in diffs:
        marker = {"in-sync": "✅", "upstream-newer": "🔄", "files-differ": "⚠️",
                  "upstream-missing": "❌"}.get(d["status"], "?")
        print(f"  {marker} {d['name']:<28} {d['status']}")
        if d.get("added"):
            print(f"      + {len(d['added'])} files: {', '.join(d['added'][:3])}")
        if d.get("removed"):
            print(f"      - {len(d['removed'])} files")
    return EXIT_OK


def cmd_sync(as_json: bool, dry_run: bool) -> int:
    """从用户机器上的 Cowork cache 拉最新内容到 vendor。"""
    upstream = find_cowork_cache()
    if not upstream:
        emit_err(ERR_USAGE, "Cowork cache not found on this machine",
                 "this command requires Claude Desktop with knowledge-work-plugins", as_json)
        return EXIT_USAGE

    lock = load_lock()
    synced = []
    for name, meta in lock["plugins"].items():
        if meta["status"] != "vendored":
            continue
        ver = meta["version"]
        theirs = upstream / name / ver
        ours = VENDOR / name / ver
        if not theirs.exists():
            continue
        # 必须有 LICENSE 才同步
        if not (theirs / "LICENSE").exists():
            synced.append({"name": name, "action": "skip", "reason": "upstream LICENSE missing"})
            continue
        if dry_run:
            synced.append({"name": name, "action": "would-sync"})
            continue
        # 先备份再覆盖
        shutil.rmtree(ours)
        ours.mkdir(parents=True)
        shutil.copytree(theirs, ours, dirs_exist_ok=True)
        synced.append({"name": name, "action": "synced"})

    if as_json:
        emit_ok({"synced": synced, "dry_run": dry_run}, as_json=True)
    else:
        print("vendor sync (dry-run)" if dry_run else "vendor sync")
        for s in synced:
            print(f"  {s['name']:<28} {s['action']}", s.get('reason', ''))
        if not dry_run:
            print("\nNext: regenerate VERSIONS.lock if any version bumped")
    return EXIT_OK


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
        all_v = "--all-vendored" in args
        positional = [a for a in args if not a.startswith("-")]
        mode = "copy" if "--copy" in args else "symlink"
        return cmd_install(positional[0] if positional else None, all_v, mode, as_json)
    if cmd == "uninstall":
        if not args:
            emit_err(ERR_USAGE, "uninstall requires <plugin>", "see 'vendor list'", as_json)
            return EXIT_USAGE
        return cmd_uninstall(args[0], as_json)
    if cmd == "diff":
        return cmd_diff(as_json)
    if cmd == "sync":
        return cmd_sync(as_json, flags["dry_run"])

    emit_err(ERR_USAGE, f"unknown vendor subcommand: {cmd}",
             "valid: list / status / install / uninstall / diff / sync", as_json)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
