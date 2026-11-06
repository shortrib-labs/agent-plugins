#!/usr/bin/env python3
"""Validate a repository that manages a collection of Tessl plugins."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "plugins"
WORKSPACE = "shortrib-labs"


class Problem:
    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        self.message = message

    def __str__(self) -> str:
        try:
            rel = self.path.relative_to(ROOT)
        except ValueError:
            rel = self.path
        return f"{rel}: {self.message}"


def run(cmd: list[str]) -> int:
    print(f"::group::{ ' '.join(cmd) }")
    proc = subprocess.run(cmd, cwd=ROOT)
    print("::endgroup::")
    return proc.returncode


def load_json(path: Path, problems: list[Problem]) -> dict | None:
    try:
        with path.open() as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        problems.append(Problem(path, f"invalid JSON: {exc}"))
    except OSError as exc:
        problems.append(Problem(path, f"cannot read file: {exc}"))
    return None


def plugin_dirs() -> list[Path]:
    if not PLUGINS_DIR.exists():
        return []
    return sorted(path.parent.parent for path in PLUGINS_DIR.glob("*/.tessl-plugin/plugin.json"))


def skill_files(plugin: Path) -> list[Path]:
    return sorted(plugin.glob("skills/*/SKILL.md"))


def main() -> int:
    problems: list[Problem] = []

    manifest_path = ROOT / "tessl.json"
    manifest = load_json(manifest_path, problems)
    plugins = plugin_dirs()

    if manifest is None:
        return 1

    if manifest.get("mode") not in {"managed", "vendored"}:
        problems.append(Problem(manifest_path, "mode must be managed or vendored"))

    agents = set(manifest.get("agents", []))
    for required_agent in {"claude-code", "tessl-agent"}:
        if required_agent not in agents:
            problems.append(Problem(manifest_path, f"agents must include {required_agent}"))

    deps = manifest.get("dependencies", {})
    if not isinstance(deps, dict):
        problems.append(Problem(manifest_path, "dependencies must be an object"))
        deps = {}

    if not plugins:
        problems.append(Problem(PLUGINS_DIR, "no plugins found under plugins/*/.tessl-plugin/plugin.json"))

    expected_deps: dict[str, str] = {}
    for plugin in plugins:
        plugin_manifest_path = plugin / ".tessl-plugin" / "plugin.json"
        plugin_manifest = load_json(plugin_manifest_path, problems)
        if plugin_manifest is None:
            continue

        name = plugin_manifest.get("name")
        version = plugin_manifest.get("version")
        description = plugin_manifest.get("description")

        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*", name):
            problems.append(Problem(plugin_manifest_path, "name must be workspace/plugin-name using lowercase kebab-case"))
        elif not name.startswith(f"{WORKSPACE}/"):
            problems.append(Problem(plugin_manifest_path, f"name should use the {WORKSPACE}/ workspace"))
        else:
            expected_deps[name] = f"file:{plugin.relative_to(ROOT).as_posix()}"

        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            problems.append(Problem(plugin_manifest_path, "version must be explicit semver, for example 0.1.0"))

        if not isinstance(description, str) or len(description.strip()) < 20:
            problems.append(Problem(plugin_manifest_path, "description should be a useful one-line summary"))

        if plugin_manifest.get("private") is not True:
            problems.append(Problem(plugin_manifest_path, "private must stay true until publish visibility is intentionally changed"))

        skills = skill_files(plugin)
        if not skills:
            problems.append(Problem(plugin, "plugin must contain at least one skills/*/SKILL.md"))

        for skill in skills:
            text = skill.read_text()
            if "TODO" in text:
                problems.append(Problem(skill, "replace TODO instructions before committing"))
            if len(text.splitlines()) > 80:
                problems.append(Problem(skill, "SKILL.md should stay concise; move details to references/"))
            if "$(cat" in text or "$(<" in text:
                problems.append(Problem(skill, "do not inline file contents into Tessl CLI prompts"))

        evals_dir = plugin / "evals"
        if evals_dir.exists() and not any(evals_dir.glob("**/task.md")):
            problems.append(Problem(evals_dir, "evals/ exists but contains no scenarios with task.md"))

    for name, source in expected_deps.items():
        dep = deps.get(name)
        if dep != {"source": source}:
            problems.append(Problem(manifest_path, f"dependencies must include {name}: {{\"source\": \"{source}\"}}"))

    for name, dep in deps.items():
        source = dep.get("source") if isinstance(dep, dict) else None
        if isinstance(source, str) and source.startswith("file:plugins/") and name not in expected_deps:
            problems.append(Problem(manifest_path, f"dependency {name} points at a missing local plugin"))

    for problem in problems:
        print(f"ERROR: {problem}", file=sys.stderr)

    if problems:
        return 1

    print(f"Validated {len(plugins)} plugin(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
