---
name: writing-pull-requests
description: Use when opening a PR, drafting or rewriting a pull request (PR) title or description, or running `gh pr create`. Finds and fills the repository's PR template, falls back to the canonical TL;DR/Details template, and checks the title and body against the house style before submitting.
---

# Writing pull requests

1. Look for the repository's template, in order: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `pull_request_template.md`, `docs/pull_request_template.md`, then any file in `.github/PULL_REQUEST_TEMPLATE/`. Use the first one found.
2. If none exists, use [the canonical template](references/pull-request-template.md).
3. Read the template's comments in full. They are the instructions; follow them over anything you remember.
4. Gather what the body needs: `git log <base>..HEAD`, `git diff <base>...HEAD --stat`, the linked issue, and how the work was verified. Write from the reason for the change, not a walk through the diff.
5. Write the body to a file with the template's comment blocks removed, and keep its headings exactly as the template shows them.
6. Check before submitting:
   - Title is 40 characters or fewer and starts with a third-person present-tense verb (it ends in "s").
   - The title, the TL;DR, and the first sentence of Details each start with a different verb.
   - The body never says "this PR", "this change", "this commit", or "this update".
   - Details ends with something the reviewer can do to verify the work.
   - Optional sections appear only when they have something to say.
7. Create the PR with `gh pr create --title "<title>" --body-file <file>`. Never use `--body` when a template exists. Show the user the title and body if they haven't already approved them.

When rewriting an existing PR, read its current body first with `gh pr view <n> --json title,body`, then update it with `gh pr edit <n> --title ... --body-file <file>`.
