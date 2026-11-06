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
- `publish-plugin.yml`

## Required CI secrets

Secrets that must be set for CI workflows:

- `TESSL_TOKEN`

`GITHUB_TOKEN` is provided by GitHub Actions for repository-local operations.

The recurring Tessl factory action uses `claude-code` through the `factory` Tessl environment, not through a GitHub Actions runner. Do not add `ANTHROPIC_API_KEY` to GitHub Actions unless a future workflow runs Claude Code in CI.

## GitHub auth

GitHub Actions use `GITHUB_TOKEN` for validation and manual publishing. The Tessl `factory` environment has GitHub `pull-requests` access and is bound to the `shortrib-labs/agent-plugins` project so scheduled factory runs can open focused PRs.

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

## Tessl factory schedule

- **Manifest**: `tessl.json`.
- **Action**: `plugin-collection-maintenance`.
- **Schedule**: `plugin-collection-maintenance-weekly`.
- **Cron**: `0 9 * * 1`.
- **Timezone**: `America/New_York`.
- **Environment**: `factory`.
- **Agent**: `claude-code`.
- **Environment status**: created with GitHub `pull-requests` access and bound to project `shortrib-labs/agent-plugins`.
- **Validation**: `scripts/validate-plugins.sh` passes and reports `✔ schedules block is valid.`.
- **Post-merge check**: run `tessl schedule list` and confirm `plugin-collection-maintenance-weekly` is active.

## Branch conventions

- Feature branches: `<author>/<description>` or `factory/<description>` for automated work.
- PR required before merging to default branch.

## CI/CD design

- PR plugin validation is deterministic and should be required once it has passed on the initial setup PR.
- Skill quality/security review is advisory at first and can become required after threshold tuning.
- Recurring plugin maintenance is a Tessl schedule in `tessl.json`, not a GitHub Actions cron.
- Publishing is a manual GitHub Actions workflow with dry-run support.
