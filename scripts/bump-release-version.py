#!/usr/bin/env python3
"""
Bump semver release version across plugin / package manifests.

Updates only known release manifests (not hook schema integers like hooks-cursor.json).

Usage:
  python3 scripts/bump-release-version.py 3.0.0
  python3 scripts/bump-release-version.py 3.0.0 --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


# (relative path, mutator)
# mutator: (data dict) -> bool  (True if changed)


def bump_package_json(data: dict, version: str) -> bool:
    if data.get("version") == version:
        return False
    data["version"] = version
    return True


def bump_top_level_version(data: dict, version: str) -> bool:
    if data.get("version") == version:
        return False
    data["version"] = version
    return True


def bump_marketplace_plugins(data: dict, version: str) -> bool:
    changed = False
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        return False
    for p in plugins:
        if isinstance(p, dict) and "version" in p:
            if p.get("version") != version:
                p["version"] = version
                changed = True
    return changed


MANIFESTS: list[tuple[str, Callable[[dict, str], bool]]] = [
    ("package.json", bump_package_json),
    (".claude-plugin/plugin.json", bump_top_level_version),
    (".cursor-plugin/plugin.json", bump_top_level_version),
    ("gemini-extension.json", bump_top_level_version),
    (".claude-plugin/marketplace.json", bump_marketplace_plugins),
]


def write_json(path: Path, data: dict) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump release semver in JSON manifests.")
    parser.add_argument(
        "version",
        nargs="?",
        default=None,
        help="Semver string, e.g. 3.0.0 (required unless --show-files)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print changes only")
    parser.add_argument(
        "--show-files",
        action="store_true",
        help="List managed manifest paths and exit",
    )
    args = parser.parse_args()

    root = repo_root()

    if args.show_files:
        for rel, _ in MANIFESTS:
            print(rel)
        return 0

    if not args.version:
        print("error: version argument required (e.g. 3.0.0)", file=sys.stderr)
        return 2

    version = args.version.strip()
    if not version:
        print("error: empty version", file=sys.stderr)
        return 2

    any_change = False
    for rel, mutator in MANIFESTS:
        path = root / rel
        if not path.is_file():
            print(f"skip (missing): {rel}", file=sys.stderr)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"error: {rel}: {e}", file=sys.stderr)
            return 1
        if not isinstance(data, dict):
            print(f"skip (not object): {rel}", file=sys.stderr)
            continue
        changed = mutator(data, version)
        if changed:
            any_change = True
            print(f"{'would update' if args.dry_run else 'updated'}: {rel} -> {version}")
            if not args.dry_run:
                write_json(path, data)
        else:
            print(f"unchanged: {rel} ({version})")

    if args.dry_run and any_change:
        print("\n(dry-run: no files written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
