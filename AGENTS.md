# Agent instructions

This repository manages a collection of Tessl agent plugins.

## Repository layout

- `plugins/<plugin-name>/` — one Tessl plugin per directory.
- `plugins/<plugin-name>/.tessl-plugin/plugin.json` — plugin manifest.
- `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` — skill entrypoint.
- `plugins/<plugin-name>/skills/<skill-name>/references/` — supporting docs for complex skills.
- `plugins/<plugin-name>/evals/` — optional Tessl eval scenarios.
- `scripts/` — deterministic validation and release helpers.
- `.tessl/memory/` — private project memory for Tessl harness agents.

## Plugin conventions

- Use workspace prefix `shortrib-labs/` for plugin names.
- Keep plugin manifests `private: true` until publishing visibility is intentionally changed.
- Keep each `SKILL.md` short; move details to `references/`.
- Avoid markdown tables in skills and reference docs.
- For large prompts or generated context passed to Tessl CLI commands, write a file and reference the path. Do not use `$(cat file)` or `$(<file)` in CLI arguments.

## Validation

Run these before opening a PR:

```bash
scripts/validate-plugins.sh
```

For skill changes with Tessl credentials available:

```bash
scripts/review-changed-skills.sh origin/main
```

For release dry-runs:

```bash
DRY_RUN=true scripts/publish-plugins.sh plugins/<plugin-name> patch
```

## Creating a plugin

Prefer Tessl scaffolding:

```bash
tessl plugin new \
  --workspace shortrib-labs \
  --name shortrib-labs/<plugin-name> \
  --summary '<one-line summary>' \
  --path plugins/<plugin-name> \
  --skill-name <skill-name> \
  --skill-description '<when to use this skill>'
```

Then add the plugin to `tessl.json` dependencies as a local file source and run validation.

## Ticket-to-PR factory

GitHub Issues with the `tessl` label are delegated to Tessl for implementation.

- Action: `implement-ticket`
- Skill: `tessl/factory#implement-github-issue`
- Environment: `factory`
- Agent: `claude-code`
- Gate label: `tessl`

A delegated issue should include a clear goal, context, acceptance criteria, and validation commands. The factory opens one PR for the issue. Human comments, reviews, and check results wake `shepherd-pull-request` to keep the PR moving.

Remove the `tessl` label or close the issue to take work back from Tessl.

## Factory maintenance

The recurring maintenance loop is the Tessl schedule in `tessl.json`, not a GitHub Actions cron.

- Action: `plugin-collection-maintenance`
- Environment: `factory`
- Agent: `claude-code`
- Schedule: weekly on Monday morning America/New_York

The maintenance skill may open a focused PR, but it must not publish plugins. Publishing stays manual through `scripts/publish-plugins.sh` or the publish workflow.

# Agent Rules <!-- tessl-managed -->

@.tessl/RULES.md follow the [instructions](.tessl/RULES.md)
