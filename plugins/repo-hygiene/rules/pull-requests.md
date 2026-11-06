# Pull requests

- Before `gh pr create`, read the repository's PR template (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, or `.github/PULL_REQUEST_TEMPLATE/`). Fill it in and pass it with `--body-file`; a bare `--body` silently skips the template. Don't write the body from memory.
- With no template in the repo, use the `writing-pull-requests` skill, which carries the canonical template.
- Title: 40 characters or fewer, starting with a third-person present-tense verb (`Adds`, `Fixes`, `Tracks`). No first person. Name the intent, not the mechanism.
- Body: `TL;DR` and `Details` as setext headings (dash underline matching the heading length). The TL;DR, the first sentence of Details, and the title each start with a different verb.
- Explain why the change exists and how to verify it. The diff already shows what changed; don't retrace it.
- Never write "this PR", "this change", "this commit", or "this update". Use active voice and present tense.
- Reference the issue with `Closes #<n>`.
