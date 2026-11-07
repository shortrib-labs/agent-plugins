#!/usr/bin/env python3
"""PreToolUse guard for shell commands that break the git hygiene rules.

Blocks, with a reason the agent can act on:
- broad staging (`git add -A`, `git add .`, `git commit -a`, ...)
- bypassing commit signing (`--no-gpg-sign`, `-c commit.gpgsign=false`)
- skipping git hooks (`--no-verify`, `git commit -n`)
- creating branches that don't match `<type>/<user>/<purpose>`

Reads the hook payload as JSON on stdin. Exits 2 with the reason on stderr to
block, and 0 otherwise. Anything it cannot parse is allowed through: a guard
that crashes or guesses would block legitimate work.

Only commands whose first word is `git` are inspected, after splitting on shell
operators and dropping heredoc bodies, so commit messages that mention these
commands don't trip the guard.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

BRANCH_TYPES = (
    "build|chore|ci|content|docs|edit|feature|fix|performance"
    "|refactor|revert|spike|style|test"
)
BRANCH_PATTERN = re.compile(
    os.environ.get("REPO_HYGIENE_BRANCH_PATTERN")
    or rf"^({BRANCH_TYPES})/[^/\s]+/[^\s]+$"
)
# Temporary exception: the Tessl factory names its branches `tessl/<id>`, where
# <id> is `issue-<n>` for GitHub issues or a lowercased Linear identifier such
# as `eng-123`. Drop this once the factory takes a branch name as input.
FACTORY_BRANCH_PATTERN = re.compile(r"^tessl/[a-z][a-z0-9]*-[0-9]+$")

SEPARATORS = {";", "&&", "||", "|", "&", "\n", "(", ")", "|&", ";;"}
COMMAND_PREFIXES = {"env", "command", "exec", "time", "nohup", "sudo"}
GIT_GLOBAL_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
BROAD_PATHSPECS = {".", "*", ":/", ":", "-A", "--all", "-u", "--update", "--no-ignore-removal"}
# git commit short options whose value follows (attached or as the next word)
COMMIT_OPTS_WITH_VALUE = set("mFCct")
COMMIT_LONG_OPTS_WITH_VALUE = {
    "--message", "--file", "--reuse-message", "--reedit-message",
    "--template", "--author", "--date", "--cleanup", "--fixup", "--squash",
    "--trailer",
}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def strip_heredocs(command: str) -> str:
    """Remove heredoc bodies so their text is never read as commands."""
    out: list[str] = []
    pending: list[str] = []
    for line in command.split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        out.append(line)
        pending.extend(m.group(2) for m in HEREDOC.finditer(line))
    return "\n".join(out)


def segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(strip_heredocs(command), posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    result: list[list[str]] = [[]]
    for token in lexer:
        if token in SEPARATORS or set(token) <= set(";&|()\n"):
            result.append([])
        else:
            result[-1].append(token)
    return [seg for seg in result if seg]


def git_invocation(words: list[str]) -> tuple[list[str], list[str]] | None:
    """Return (config overrides, args from the subcommand on) if this runs git."""
    i = 0
    while i < len(words) and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[i]) or words[i] in COMMAND_PREFIXES):
        i += 1
    if i >= len(words) or os.path.basename(words[i]) != "git":
        return None
    i += 1
    configs: list[str] = []
    while i < len(words) and words[i].startswith("-"):
        opt = words[i]
        if opt in GIT_GLOBAL_OPTS_WITH_VALUE and i + 1 < len(words):
            if opt == "-c":
                configs.append(words[i + 1])
            i += 2
        else:
            i += 1
    return configs, words[i:]


def check_staging(sub: str, args: list[str]) -> str | None:
    if sub == "add":
        broad = [a for a in args if a in BROAD_PATHSPECS]
        if broad:
            return (
                f"Stage files explicitly by name instead of `git add {broad[0]}`. "
                "Broad staging can pick up secrets, build output, and unrelated changes."
            )
    if sub == "commit" and commit_flags(args) & {"all"}:
        return (
            "Don't use `git commit -a`/`--all`. Stage the files you mean to commit "
            "by name with `git add <path>`, then commit."
        )
    return None


def commit_flags(args: list[str]) -> set[str]:
    """Flags of interest on `git commit`, skipping option values like messages."""
    flags: set[str] = set()
    skip = False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg == "--":
            break
        if arg in ("--all",):
            flags.add("all")
        elif arg == "--no-verify":
            flags.add("no-verify")
        elif arg.startswith("--"):
            if arg in COMMIT_LONG_OPTS_WITH_VALUE:
                skip = True
        elif arg.startswith("-") and len(arg) > 1:
            for pos, ch in enumerate(arg[1:]):
                if ch == "a":
                    flags.add("all")
                elif ch == "n":
                    flags.add("no-verify")
                elif ch in COMMIT_OPTS_WITH_VALUE:
                    skip = pos == len(arg) - 2  # value is the next word
                    break
                elif ch == "S":
                    break  # optional attached key id
    return flags


def check_signing(configs: list[str], args: list[str]) -> str | None:
    disabled = [c for c in configs if re.match(r"^(commit|tag)\.gpgsign=(false|no|off|0)$", c, re.I)]
    if "--no-gpg-sign" in args or disabled:
        return (
            "Commits and tags must be signed. Don't pass `--no-gpg-sign` or "
            "`-c commit.gpgsign=false`. If signing fails, retry once (a smartcard "
            "may need a moment), then stop and ask."
        )
    return None


def check_hooks(sub: str, args: list[str]) -> str | None:
    if "--no-verify" in args or (sub == "commit" and "no-verify" in commit_flags(args)):
        return (
            "Don't skip git hooks with `--no-verify` or `git commit -n`. Fix what the "
            "hook reports, or ask if the hook itself looks wrong."
        )
    return None


def created_branch(sub: str, args: list[str]) -> str | None:
    def value_after(flags: set[str]) -> str | None:
        for i, arg in enumerate(args):
            if arg in flags and i + 1 < len(args):
                return args[i + 1]
            for flag in flags:
                if flag.startswith("--") and arg.startswith(flag + "="):
                    return arg.split("=", 1)[1]
        return None

    if sub == "checkout":
        return value_after({"-b", "-B"})
    if sub == "switch":
        return value_after({"-c", "-C", "--create", "--force-create"})
    if sub == "worktree" and args[:1] == ["add"]:
        return value_after({"-b", "-B"})
    if sub == "branch":
        modes = {"-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy",
                 "-l", "--list", "-a", "--all", "-r", "--remotes", "--show-current",
                 "--contains", "--no-contains", "--merged", "--no-merged",
                 "-u", "--set-upstream-to", "--unset-upstream", "--edit-description"}
        if any(a in modes or a.startswith(("--set-upstream-to=", "--sort", "--format", "--points-at")) for a in args):
            return None
        positional = [a for a in args if not a.startswith("-")]
        return positional[0] if positional else None
    return None


def check_branch(sub: str, args: list[str]) -> str | None:
    name = created_branch(sub, args)
    if name and not (BRANCH_PATTERN.match(name) or FACTORY_BRANCH_PATTERN.match(name)):
        return (
            f"Branch `{name}` doesn't match `<type>/<user>/<purpose>`. Type is one of "
            f"{BRANCH_TYPES.replace('|', ', ')} (spelled out in full); user is who is "
            "doing the work (`claude` for agent-authored branches); purpose is a "
            "third-person verb phrase describing intent, e.g. `feature/crdant/adds-mx-support`."
        )
    return None


def check_command(command: str) -> str | None:
    try:
        segs = segments(command)
    except ValueError:
        return None
    for words in segs:
        invocation = git_invocation(words)
        if not invocation:
            continue
        configs, rest = invocation
        sub, args = (rest[0], rest[1:]) if rest else ("", [])
        for check in (
            lambda: check_signing(configs, args),
            lambda: check_hooks(sub, args),
            lambda: check_staging(sub, args),
            lambda: check_branch(sub, args),
        ):
            reason = check()
            if reason:
                return reason
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        tool_input = payload.get("tool_input") or {}
        command = tool_input.get("command") or tool_input.get("cmd") or ""
        if isinstance(command, list):
            command = " ".join(shlex.quote(part) for part in command)
    except Exception:
        return 0
    reason = check_command(command) if isinstance(command, str) else None
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
