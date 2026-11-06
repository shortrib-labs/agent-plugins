# Goals

## Onboarding goals

- [x] Initialize Tessl project identity for this repository.
- [x] Create baseline plugin collection layout under `plugins/`.
- [x] Add deterministic validation for plugin manifests, skills, schedules, plugin lint, and eval lint.
- [x] Add CI/CD workflows for plugin validation, skill review, and manual publish.
- [x] Create the Tessl `factory` environment and move weekly maintenance to a repository-defined `tessl.json` schedule.
- [ ] Confirm repository secrets and Tessl GitHub app/integration installation after the first PR workflow run.
- [ ] Confirm the reconciled `plugin-collection-maintenance-weekly` schedule is active after merge with `tessl schedule list`.
- [ ] Backtest the skill quality workflow on the first real plugin PR and tune thresholds.
- [ ] Decide when each plugin is ready for public publishing.

## Top line goals

Set up this directory for managing a collection of Tessl agent plugins with CI/CD and a real Tessl-run factory loop. GitHub Actions provide validation, skill review, and manual publishing; the recurring maintenance factory is the Tessl schedule declared in `tessl.json`.

## Current bottlenecks

The initial repository structure, CI/CD harness, and Tessl factory declaration are in place. Remaining bottlenecks are first-run validation in GitHub Actions, confirming required secrets/integrations, confirming the reconciled schedule after merge, and tuning quality-review thresholds from real PR feedback.
