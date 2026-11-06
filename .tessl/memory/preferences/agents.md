# Agents

## Supported agents

Agents installed and available for CI, local use, and Tessl scheduled factory runs:

- claude-code
- tessl-agent

## Default agent

claude-code

## Preferred models

No project-specific model pins yet.

## Agent ids

Use Tessl `--agent` values: `claude-code`, `codex`, `gemini`, `cursor`, `copilot`, `openhands`, `tessl-agent`.

## Factory usage

- Use `claude-code` for the scheduled `plugin-collection-maintenance` factory action in `tessl.json`.
- The action runs in the Tessl `factory` environment, not in GitHub Actions.
- The `factory` environment has GitHub pull-request access for opening focused maintenance PRs.

## CI usage

- Use Tessl CLI commands directly for CI/CD checks such as `tessl plugin lint`, `tessl eval lint`, `tessl schedule validate`, and `tessl review run`.
- Do not install or run Claude Code in GitHub Actions unless a future workflow explicitly needs a local `claude-code` runner.
- Keep Tessl CLI prompts short. Put large generated context in a workspace file and reference the file path.
