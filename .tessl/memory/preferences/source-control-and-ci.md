# Source control and CI

## Hosting platform

github

## Repository

shortrib-labs/agent-plugins

## Default branch

main

## CI platform

GitHub Actions

## CI workflows directory

.github/workflows/

## Workflow file naming convention

Use descriptive workflow filenames:

- `plugin-validation.yml`
- `skill-quality-review.yml`
- `plugin-maintenance.yml`
- `publish-plugin.yml`

## Required CI secrets

Secrets that must be set for agent-driven CI workflows:

- `TESSL_TOKEN`
- `ANTHROPIC_API_KEY` for workflows that run `claude-code`

`GITHUB_TOKEN` is provided by GitHub Actions for repository-local operations.

## GitHub auth

Start with `GITHUB_TOKEN` for validation and manual publishing. If scheduled factory runs need to push branches or open PRs that trigger downstream CI reliably, install/configure the Tessl GitHub App and update this file with the chosen auth method.

## Deterministic invariant checks

Records the repo's non-LLM tools for enforcing broad invariants that should apply to future files or changes.

- **Lint / format tools**: `tessl plugin lint` for plugin manifests and file structure; `tessl eval lint` for eval scenario structure.
- **Structural search tools**: none.
- **Typecheck tools**: none.
- **Schema/config validators**: `tessl schedule validate`; `scripts/validate-plugin-collection.py` for repository-specific plugin collection policy.
- **Import-boundary or architecture checks**: none.
- **Generated-artifact sync checks**: none.
- **Contract/golden checks with broad invariant value**: none.
- **Broad invariant test suites**: none.
- **Primary CI workflows that run these checks**: `.github/workflows/plugin-validation.yml`.
- **Preferred destination for new deterministic checks**: extend `scripts/validate-plugin-collection.py` for plugin collection policy; prefer standard Tessl lint commands where available.
- **Missing deterministic guardrail gaps**: actionlint is not configured for GitHub workflow YAML; markdown lint is not configured for docs/skills.
- **Recommended first tool to add**: actionlint for GitHub workflow validation after the first CI iteration.

## Tessl verify

- **Configured**: no.
- **Manifest**: `tessl.json`.
- **Verifier files**: none.
- **Monorepo child manifests**: none.
- **CI gate**: none.
- **TESSL_TOKEN for verify**: required secret listed above, but verify is not set up yet.

## Branch conventions

- Feature branches: `<author>/<description>` or `factory/<description>` for automated work.
- PR required before merging to default branch.

## CI/CD design

- PR plugin validation is deterministic and should be required once it has passed on the initial setup PR.
- Skill quality/security review is advisory at first and can become required after threshold tuning.
- Plugin maintenance runs weekly and manually through GitHub Actions for now; move it to a repository-defined Tessl schedule after the GitHub remote is connected and the `factory` environment exists.
- Publishing is a manual GitHub Actions workflow with dry-run support.
