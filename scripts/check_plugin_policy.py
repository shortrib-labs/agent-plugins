#!/usr/bin/env python3
"""Checks the plugin-collection rules that Tessl tooling cannot express.

Covers our plugin.json policy, the plugins/ to tessl.json cross-check, and
the MCP server pinning rules.
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

# An unpinned launcher installs whatever is latest each session, so a new or
# hijacked release would run unreviewed. Ranges and tags are as bad as nothing.
NPM_PINNED = re.compile(r"^(@[^/@]+/)?[^/@\s]+@\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$")
PY_PINNED = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]+\])?==\d+(\.\d+)*([A-Za-z0-9.+!-]*)$")
# Flags that take a separate value, so the value is not mistaken for the package.
NPM_VALUE_FLAGS = {"-c", "--call", "--registry", "--cache", "--prefix"}


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


def launcher_package(command: str, args: list[str]):
    """Returns (kind, package spec) for a known package launcher, else None.

    The spec is None when the launcher names no package at all.
    """
    if command in ("npx", "bunx") or (command == "pnpm" and args[:1] == ["dlx"]):
        rest = args[1:] if command == "pnpm" else args
        skip = False
        for arg in rest:
            if skip:
                if skip == "package":
                    return "npm", arg
                skip = False
            elif arg in ("-p", "--package"):
                skip = "package"
            elif arg.startswith("--package="):
                return "npm", arg.split("=", 1)[1]
            elif arg in NPM_VALUE_FLAGS:
                skip = True
            elif not arg.startswith("-"):
                return "npm", arg
        return "npm", None
    if command == "uvx" or (command == "pipx" and args[:1] == ["run"]):
        rest = args[1:] if command == "pipx" else args
        for i, arg in enumerate(rest):
            if arg == "--from":
                return "python", rest[i + 1] if i + 1 < len(rest) else None
            if arg.startswith("--from="):
                return "python", arg.split("=", 1)[1]
        return "python", next((a for a in rest if not a.startswith("-")), None)
    return None


def check_server(rel: str, name: str, server: dict, warnings: list[str]) -> list[str]:
    where = f"{rel}: server {name!r}"
    url = server.get("url")
    if isinstance(url, str):
        if not url.startswith("https://"):
            return [f"{where}: rule https: url must start with https://, got {url!r}"]
        return []

    command = server.get("command")
    args = server.get("args", [])
    if not isinstance(args, list):
        args = []
    args = [a for a in args if isinstance(a, str)]
    launcher = launcher_package(command, args) if isinstance(command, str) else None
    if launcher is None:
        warnings.append(f"{where}: rule unknown-command: command {command!r} is not a known package launcher, review by hand")
        return []

    kind, spec = launcher
    pattern = NPM_PINNED if kind == "npm" else PY_PINNED
    if spec is None or not pattern.match(spec):
        example = "name@1.2.3" if kind == "npm" else "name==1.2.3"
        return [f"{where}: rule pinned-version: package must name an exact version like {example}, got {spec!r}"]
    return []


def check_mcp(root: Path, plugin: Path, manifest: dict, warnings: list[str]) -> list[str]:
    declared = manifest.get("mcpServers")
    if declared is None:
        return []

    if isinstance(declared, str):
        path = plugin / declared
        try:
            rel = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            rel = declared
        if not path.is_file():
            return [f"{rel}: rule mcp-config: file named by mcpServers does not exist"]
        config = load(path)
    else:
        rel = (plugin / ".tessl-plugin" / "plugin.json").relative_to(root).as_posix()
        config = declared

    # Config files wrap servers in "mcpServers"; an inline manifest value may not.
    servers = config.get("mcpServers", config) if isinstance(config, dict) else None
    if not isinstance(servers, dict):
        return []

    problems = []
    for name, server in servers.items():
        if isinstance(server, dict):
            problems.extend(check_server(rel, name, server, warnings))
    return problems


def check(root: Path, warnings: list[str] | None = None) -> list[str]:
    problems = []
    warnings = [] if warnings is None else warnings

    local = set()
    for path in sorted(root.glob("plugins/*/.tessl-plugin/plugin.json")):
        rel = path.relative_to(root).as_posix()
        local.add(path.parents[1].name)
        manifest = load(path)
        if isinstance(manifest, dict):
            problems.extend(check_manifest(rel, manifest))
            problems.extend(check_mcp(root, path.parents[1], manifest, warnings))

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
    warnings: list[str] = []
    problems = check(root, warnings)
    for warning in warnings:
        print(f"WARN {warning}", file=sys.stderr)
    for problem in problems:
        print(f"ERROR {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
