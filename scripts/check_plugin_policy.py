#!/usr/bin/env python3
"""Checks the plugin-collection rules that Tessl tooling cannot express.

Covers our plugin.json policy and the plugins/ to tessl.json cross-check.
Each rule should be removed once Tessl can enforce it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"
)
NAME = re.compile(r"^shortrib-labs/[a-z0-9]+(-[a-z0-9]+)*$")
MIN_DESCRIPTION = 20
LOCAL_PREFIX = "file:plugins/"


def load(path: Path):
    # Malformed JSON is `tessl plugin lint`'s to report, so it is skipped here.
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def check_manifest(rel: str, manifest: dict) -> list[str]:
    problems = []

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER.match(version):
        problems.append(f"{rel}: version must be an explicit semver string, got {version!r}")

    name = manifest.get("name")
    if not isinstance(name, str) or not NAME.match(name):
        problems.append(f"{rel}: name must be shortrib-labs/<kebab-case>, got {name!r}")

    description = manifest.get("description")
    if (
        not isinstance(description, str)
        or len(description.strip()) < MIN_DESCRIPTION
        or "\n" in description.strip()
    ):
        problems.append(
            f"{rel}: description must be a one-line summary of at least {MIN_DESCRIPTION} characters"
        )

    # `is not True` so that "true" or 1 cannot slip through as private.
    if manifest.get("private") is not True:
        problems.append(f'{rel}: private must be true (got {manifest.get("private")!r})')

    return problems


def check(root: Path) -> list[str]:
    problems = []

    local = set()
    for path in sorted(root.glob("plugins/*/.tessl-plugin/plugin.json")):
        rel = path.relative_to(root).as_posix()
        local.add(path.parents[1].name)
        manifest = load(path)
        if isinstance(manifest, dict):
            problems.extend(check_manifest(rel, manifest))

    tessl = load(root / "tessl.json")
    dependencies = tessl.get("dependencies", {}) if isinstance(tessl, dict) else {}
    sources = {
        dep["source"]
        for dep in dependencies.values()
        if isinstance(dep, dict) and isinstance(dep.get("source"), str)
    }

    for directory in sorted(local):
        if f"{LOCAL_PREFIX}{directory}" not in sources:
            problems.append(
                f"tessl.json: plugins/{directory} has no dependency with source {LOCAL_PREFIX}{directory}"
            )

    for source in sorted(s for s in sources if s.startswith(LOCAL_PREFIX)):
        directory = source[len(LOCAL_PREFIX):]
        if directory not in local:
            problems.append(f"tessl.json: dependency {source} has no plugin folder at plugins/{directory}")

    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path(__file__).resolve().parents[1]
    problems = check(root)
    for problem in problems:
        print(f"ERROR {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
