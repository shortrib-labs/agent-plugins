# Goals

## Onboarding goals

- [x] Initialize Tessl project identity for this repository.
- [x] Create baseline plugin collection layout under `plugins/`.
- [x] Add deterministic validation for plugin manifests, skills, schedules, plugin lint, and eval lint.
- [x] Add CI/CD workflows for plugin validation, skill review, scheduled maintenance, and manual publish.
- [ ] Confirm repository secrets and Tessl GitHub app/integration installation after the GitHub remote exists.
- [ ] Create the Tessl `factory` environment and consider moving weekly maintenance from GitHub Actions to a repository-defined `tessl.json` schedule.
- [ ] Backtest the skill quality workflow on the first real plugin PR and tune thresholds.
- [ ] Decide when each plugin is ready for public publishing.

## Top line goals

Set up this directory as a full Tessl-managed software factory for a collection of agent plugins, including CI/CD, scheduled maintenance, quality review, and controlled publishing.

## Current bottlenecks

The repository started empty, so the main bottleneck is missing structure: no plugin layout, no validation scripts, no project memory, no CI/CD workflows, and no documented publishing path.
