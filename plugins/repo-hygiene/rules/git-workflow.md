# Git workflow

- Stage files explicitly by name. Never `git add -A`, `git add .`, `git add -u`, or `git commit -a`. Review what you staged with `git diff --staged` before committing.
- Sign every commit. Never pass `--no-gpg-sign` or `-c commit.gpgsign=false`. Signing may use a smartcard: if it fails, retry once, then stop and ask.
- Never skip git hooks with `--no-verify`. Fix what the hook reports, or ask if the hook looks wrong. If the repo has a `make setup-hooks` (or similar) target, run it before the first commit.
- Name branches `<type>/<user>/<purpose>`:
  - type, spelled out in full: `build`, `chore`, `ci`, `content`, `docs`, `edit`, `feature`, `fix`, `performance`, `refactor`, `revert`, `spike`, `style`, `test`
  - user: who is doing the work; `claude` for agent-authored branches
  - purpose: a third-person verb phrase describing intent, not implementation (`feature/crdant/writes-hpd-files`, not `feature/crdant/adds-hpd-writer`)
- Put worktrees under `.worktrees/`, named after the last fragment of the branch (`.worktrees/writes-hpd-files`), and make sure `.worktrees/` is ignored.
- Land changes on the default branch through a pull request, even small ones.
- Before pushing, check `git log origin/<branch>..HEAD` so you know every commit a push will send.

A `PreToolUse` hook in this plugin blocks broad staging, unsigned commits, `--no-verify`, and badly named branches. When it blocks a command, fix the command; don't look for another way around the rule.
