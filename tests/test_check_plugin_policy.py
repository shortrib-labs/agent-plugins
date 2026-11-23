"""Tests for scripts/check_plugin_policy.py.

Run with: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_plugin_policy  # noqa: E402

GOOD_MANIFEST = {
    "name": "shortrib-labs/example",
    "version": "1.2.3",
    "description": "A real one-line summary of the plugin.",
    "private": True,
}


class Repo:
    """A throwaway repo root holding plugins and a tessl.json."""

    def __init__(self, tmp: str):
        self.root = Path(tmp)
        self.deps: dict = {}

    def plugin(self, directory: str = "example", manifest: dict | None = None, listed: bool = True):
        path = self.root / "plugins" / directory / ".tessl-plugin"
        path.mkdir(parents=True, exist_ok=True)
        (path / "plugin.json").write_text(json.dumps(GOOD_MANIFEST if manifest is None else manifest))
        if listed:
            self.depend(directory)

    def depend(self, directory: str):
        self.deps[f"shortrib-labs/{directory}"] = {"source": f"file:plugins/{directory}"}

    def check(self) -> list[str]:
        (self.root / "tessl.json").write_text(json.dumps({"dependencies": self.deps}))
        return check_plugin_policy.check(self.root)


class PolicyTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Repo(tmp.name)

    def manifest(self, **changes) -> dict:
        manifest = dict(GOOD_MANIFEST)
        for key, value in changes.items():
            if value is None:
                manifest.pop(key, None)
            else:
                manifest[key] = value
        return manifest

    def problems_for(self, **changes) -> list[str]:
        self.repo.plugin(manifest=self.manifest(**changes))
        return self.repo.check()

    def assertRule(self, problems: list[str], rule: str):
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("plugins/example/.tessl-plugin/plugin.json", problems[0])
        self.assertIn(rule, problems[0])


class Valid(PolicyTest):
    def test_conforming_plugin_passes(self):
        self.repo.plugin()
        self.assertEqual(self.repo.check(), [])

    def test_no_plugins_passes(self):
        self.assertEqual(self.repo.check(), [])


class Version(PolicyTest):
    def test_semver_with_prerelease_passes(self):
        self.assertEqual(self.problems_for(version="1.0.0-rc.1"), [])

    def test_missing_version_fails(self):
        self.assertRule(self.problems_for(version=None), "version")

    def test_non_semver_version_fails(self):
        self.assertRule(self.problems_for(version="1.0"), "version")


class Name(PolicyTest):
    def test_kebab_case_name_passes(self):
        self.assertEqual(self.problems_for(name="shortrib-labs/my-plugin-2"), [])

    def test_other_workspace_fails(self):
        self.assertRule(self.problems_for(name="tessl/example"), "name")

    def test_non_kebab_name_fails(self):
        self.assertRule(self.problems_for(name="shortrib-labs/My_Plugin"), "name")

    def test_missing_name_fails(self):
        self.assertRule(self.problems_for(name=None), "name")


class Description(PolicyTest):
    def test_twenty_characters_passes(self):
        self.assertEqual(self.problems_for(description="x" * 20), [])

    def test_short_description_fails(self):
        self.assertRule(self.problems_for(description="x" * 19), "description")

    def test_multi_line_description_fails(self):
        self.assertRule(self.problems_for(description="A summary that runs\nacross two lines."), "description")

    def test_missing_description_fails(self):
        self.assertRule(self.problems_for(description=None), "description")


class Private(PolicyTest):
    def test_private_true_passes(self):
        self.assertEqual(self.problems_for(private=True), [])

    def test_private_false_fails(self):
        self.assertRule(self.problems_for(private=False), "private")

    def test_missing_private_fails(self):
        self.assertRule(self.problems_for(private=None), "private")

    def test_string_true_fails(self):
        self.assertRule(self.problems_for(private="true"), "private")


class Listing(PolicyTest):
    def test_listed_plugin_passes(self):
        self.repo.plugin(listed=True)
        self.assertEqual(self.repo.check(), [])

    def test_unlisted_plugin_fails(self):
        self.repo.plugin(listed=False)
        problems = self.repo.check()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("tessl.json", problems[0])
        self.assertIn("file:plugins/example", problems[0])

    def test_dependency_without_folder_fails(self):
        self.repo.depend("gone")
        problems = self.repo.check()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("tessl.json", problems[0])
        self.assertIn("file:plugins/gone", problems[0])

    def test_registry_dependency_is_ignored(self):
        self.repo.deps["tessl/factory"] = {"version": "1.0.1"}
        self.assertEqual(self.repo.check(), [])


class Mcp(PolicyTest):
    def servers(self, **servers) -> tuple[list[str], list[str]]:
        self.repo.plugin(manifest=self.manifest(mcpServers="./.mcp.json"))
        plugin = self.repo.root / "plugins" / "example"
        (plugin / ".mcp.json").write_text(json.dumps({"mcpServers": servers}))
        (self.repo.root / "tessl.json").write_text(json.dumps({"dependencies": self.repo.deps}))
        warnings: list[str] = []
        return check_plugin_policy.check(self.repo.root, warnings), warnings

    def npx(self, spec: str) -> dict:
        return {"command": "npx", "args": ["-y", spec]}

    def assertMcpRule(self, problems: list[str], rule: str, server: str = "srv"):
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("plugins/example/.mcp.json", problems[0])
        self.assertIn(f"server '{server}'", problems[0])
        self.assertIn(f"rule {rule}", problems[0])

    def test_https_url_passes(self):
        problems, warnings = self.servers(srv={"type": "http", "url": "https://example.com/mcp"})
        self.assertEqual((problems, warnings), ([], []))

    def test_http_url_fails(self):
        problems, _ = self.servers(srv={"type": "http", "url": "http://example.com/mcp"})
        self.assertMcpRule(problems, "https")

    def test_npx_exact_version_passes(self):
        problems, warnings = self.servers(srv=self.npx("displaybuddy-mcp@3.2.2"))
        self.assertEqual((problems, warnings), ([], []))

    def test_scoped_exact_version_passes(self):
        problems, _ = self.servers(srv=self.npx("@scope/name@1.2.3-rc.1"))
        self.assertEqual(problems, [])

    def test_npx_missing_version_fails(self):
        problems, _ = self.servers(srv=self.npx("displaybuddy-mcp"))
        self.assertMcpRule(problems, "pinned-version")

    def test_npx_latest_tag_fails(self):
        problems, _ = self.servers(srv=self.npx("displaybuddy-mcp@latest"))
        self.assertMcpRule(problems, "pinned-version")

    def test_npx_range_fails(self):
        problems, _ = self.servers(srv=self.npx("displaybuddy-mcp@^3.2.2"))
        self.assertMcpRule(problems, "pinned-version")

    def test_scoped_without_version_fails(self):
        problems, _ = self.servers(srv=self.npx("@scope/name"))
        self.assertMcpRule(problems, "pinned-version")

    def test_bunx_and_pnpm_dlx_are_checked(self):
        problems, _ = self.servers(
            a={"command": "bunx", "args": ["name@1.0.0"]},
            b={"command": "pnpm", "args": ["dlx", "name@1.0.0"]},
        )
        self.assertEqual(problems, [])
        problems, _ = self.servers(srv={"command": "pnpm", "args": ["dlx", "name"]})
        self.assertMcpRule(problems, "pinned-version")

    def test_uvx_pinned_passes(self):
        problems, _ = self.servers(srv={"command": "uvx", "args": ["name==1.2.3"]})
        self.assertEqual(problems, [])

    def test_uvx_from_pinned_passes(self):
        problems, _ = self.servers(srv={"command": "uvx", "args": ["--from", "name==1.2.3", "tool"]})
        self.assertEqual(problems, [])

    def test_uvx_unpinned_fails(self):
        problems, _ = self.servers(srv={"command": "uvx", "args": ["name"]})
        self.assertMcpRule(problems, "pinned-version")

    def test_uvx_from_range_fails(self):
        problems, _ = self.servers(srv={"command": "uvx", "args": ["--from", "name>=1.2", "tool"]})
        self.assertMcpRule(problems, "pinned-version")

    def test_pipx_run_is_checked(self):
        problems, _ = self.servers(srv={"command": "pipx", "args": ["run", "name==1.0.0"]})
        self.assertEqual(problems, [])
        problems, _ = self.servers(srv={"command": "pipx", "args": ["run", "name"]})
        self.assertMcpRule(problems, "pinned-version")

    def test_unknown_command_warns_without_failing(self):
        problems, warnings = self.servers(srv={"command": "/usr/local/bin/mine"})
        self.assertEqual(problems, [])
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("plugins/example/.mcp.json", warnings[0])
        self.assertIn("server 'srv'", warnings[0])
        self.assertIn("rule unknown-command", warnings[0])

    def test_missing_config_file_fails(self):
        self.repo.plugin(manifest=self.manifest(mcpServers="./.mcp.json"))
        problems = self.repo.check()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("rule mcp-config", problems[0])

    def test_plugin_without_mcp_servers_is_untouched(self):
        self.repo.plugin()
        self.assertEqual(self.repo.check(), [])


class Cli(PolicyTest):
    def test_reports_every_problem_and_exits_non_zero(self):
        self.repo.plugin(manifest=self.manifest(private=False, version="x"))
        (self.repo.root / "tessl.json").write_text(json.dumps({"dependencies": self.repo.deps}))
        self.assertEqual(check_plugin_policy.main([str(self.repo.root)]), 1)

    def test_exits_zero_when_clean(self):
        self.repo.plugin()
        (self.repo.root / "tessl.json").write_text(json.dumps({"dependencies": self.repo.deps}))
        self.assertEqual(check_plugin_policy.main([str(self.repo.root)]), 0)


if __name__ == "__main__":
    unittest.main()
