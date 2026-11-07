"""Tests for hooks/guard_git.py.

Run with: python3 -m unittest discover -s plugins/repo-hygiene/tests
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "guard_git.py"
sys.path.insert(0, str(HOOK.parent))

import guard_git  # noqa: E402


def violation(command: str) -> str | None:
    return guard_git.check_command(command)


class BroadStaging(unittest.TestCase):
    def test_blocks_add_all_forms(self):
        for cmd in [
            "git add -A",
            "git add --all",
            "git add .",
            "git add -u",
            "git add --update",
            "git add *",
            "git add :/",
            "git add -v .",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_blocks_commit_all(self):
        for cmd in ['git commit -a -m "msg"', 'git commit -am "msg"', "git commit --all"]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_allows_explicit_paths(self):
        for cmd in [
            "git add src/foo.py src/bar.py",
            "git add ./src/foo.py",
            "git add -p src/foo.py",
            "git add .github/workflows/ci.yml",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(violation(cmd))


class Signing(unittest.TestCase):
    def test_blocks_signing_bypass(self):
        for cmd in [
            'git commit --no-gpg-sign -m "msg"',
            'git -c commit.gpgsign=false commit -m "msg"',
            "git merge --no-gpg-sign feature/crdant/adds-x",
            "git rebase --no-gpg-sign main",
            "git -c tag.gpgsign=false tag v1.0.0",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_allows_normal_commit(self):
        self.assertIsNone(violation('git commit -S -m "Adds thing"'))
        self.assertIsNone(violation('git commit -m "Adds thing"'))


class SkippingHooks(unittest.TestCase):
    def test_blocks_no_verify(self):
        for cmd in [
            'git commit --no-verify -m "msg"',
            'git commit -n -m "msg"',
            'git commit -nm "msg"',
            "git push --no-verify",
            "git merge --no-verify topic",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_push_dry_run_is_not_no_verify(self):
        self.assertIsNone(violation("git push -n origin feature/crdant/adds-x"))


class BranchNaming(unittest.TestCase):
    def test_blocks_bad_names(self):
        for cmd in [
            "git checkout -b my-branch",
            "git switch -c feat/crdant/adds-x",
            "git branch fix-thing",
            "git worktree add -b quick .worktrees/quick",
            "git checkout -B feature/adds-x",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_allows_good_names(self):
        for cmd in [
            "git checkout -b feature/crdant/adds-mx-support",
            "git switch --create fix/claude/stops-crash",
            "git branch spike/crdant/tries-hooks",
            "git worktree add -b docs/claude/explains-setup .worktrees/explains-setup main",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(violation(cmd))

    def test_allows_tessl_factory_branches(self):
        for cmd in [
            "git checkout -b tessl/issue-5",
            "git switch -c tessl/eng-123",
            "git worktree add -b tessl/issue-42 .worktrees/issue-42 origin/main",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(violation(cmd))

    def test_blocks_other_tessl_branches(self):
        for cmd in [
            "git checkout -b tessl/foo/bar",
            "git checkout -b tessl/",
            "git checkout -b tessl",
            "git checkout -b tessl/5",
            "git checkout -b tessl/issue-5/extra",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_ignores_non_creating_branch_commands(self):
        for cmd in [
            "git branch",
            "git branch -d old",
            "git branch --show-current",
            "git branch -m old new",
            "git checkout main",
            "git switch main",
            "git worktree add .worktrees/x existing-branch",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(violation(cmd))


class Parsing(unittest.TestCase):
    def test_finds_git_after_shell_operators_and_prefixes(self):
        for cmd in [
            "cd repo && git add -A",
            "make fmt; git commit --no-verify -m x",
            "FOO=1 git add .",
            "git -C ../other add -A",
            "/usr/bin/git add --all",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(violation(cmd))

    def test_ignores_text_inside_messages_and_heredocs(self):
        heredoc = "git commit -F - <<'EOF'\nNever run git add -A or --no-verify\nEOF"
        substitution = (
            'git commit -m "$(cat <<\'EOF\'\nExplains why git add . is blocked\nEOF\n)"'
        )
        for cmd in [
            'git commit -m "Blocks git add -A and --no-verify"',
            heredoc,
            substitution,
            'echo "git add -A"',
            "grep -- --no-verify README.md",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(violation(cmd))

    def test_unparseable_command_fails_open(self):
        self.assertIsNone(violation('git commit -m "unterminated'))


class HookProtocol(unittest.TestCase):
    def run_hook(self, payload: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )

    def test_denied_command_exits_2_with_reason(self):
        result = self.run_hook({"tool_name": "Bash", "tool_input": {"command": "git add -A"}})
        self.assertEqual(result.returncode, 2)
        self.assertIn("git add", result.stderr)

    def test_allowed_command_exits_0_silently(self):
        result = self.run_hook({"tool_name": "Bash", "tool_input": {"command": "git status"}})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    def test_accepts_cmd_field_and_bad_input(self):
        result = self.run_hook({"tool_input": {"cmd": "git add ."}})
        self.assertEqual(result.returncode, 2)
        bad = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
        self.assertEqual(bad.returncode, 0)


if __name__ == "__main__":
    unittest.main()
