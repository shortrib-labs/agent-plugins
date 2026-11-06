# Agents

## Supported agents

Agents installed and available for CI and local use:

- claude-code
- tessl-agent

## Default agent

claude-code

## Preferred models

No project-specific model pins yet.

## Agent ids

Use Tessl `--agent` values: `claude-code`, `codex`, `gemini`, `cursor`, `copilot`, `openhands`, `tessl-agent`.

## CI usage

- Use `tessl-agent` for harness-engineering workflows that do not need local coding-agent CLIs.
- Use `claude-code` for scheduled plugin-maintenance skill execution.
- Keep Tessl CLI prompts short. Put large generated context in a workspace file and reference the file path.
