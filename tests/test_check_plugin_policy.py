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
        path.mkdir(parents=True)
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
