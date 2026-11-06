# Agent Plugins

A Tessl-managed repository for building, validating, improving, and publishing Shortrib Labs agent plugins.

## What is here

- Local Tessl project: `shortrib-labs/agent-plugins`
- Plugin workspace: `shortrib-labs`
- Plugin source directory: `plugins/`
- Maintenance plugin: `plugins/plugin-collection-maintainer`
- Tessl factory action and weekly schedule declared in `tessl.json`
- GitHub Actions CI/CD for validation, skill review, and manual publish

## Quick start

```bash
tessl init
scripts/validate-plugins.sh
```

Create a plugin:

```bash
tessl plugin new \
  --workspace shortrib-labs \
  --name shortrib-labs/<plugin-name> \
  --summary '<one-line summary>' \
  --path plugins/<plugin-name> \
  --skill-name <skill-name> \
  --skill-description '<when to use this skill>'
```

Add it to `tessl.json`:

```json
"shortrib-labs/<plugin-name>": {
  "source": "file:plugins/<plugin-name>"
}
```

Validate it:

```bash
scripts/validate-plugins.sh
```

## CI/CD

GitHub Actions are CI/CD checks, not the factory loop.

- **Plugin collection validation** runs deterministic checks, `tessl schedule validate`, plugin lint, and eval lint.
- **Skill quality review** runs Tessl quality/security review on changed `SKILL.md` files.
- **Publish plugin** is manual and can dry-run or publish one plugin or all plugins.

Required repository secrets:

- `TESSL_TOKEN`

## Tessl factory loop

The factory loop is declared in `tessl.json`:

- **Action**: `plugin-collection-maintenance`
- **Skill**: `file:plugins/plugin-collection-maintainer#plugin-collection-maintenance`
- **Agent**: `claude-code`
- **Environment**: `factory`
- **Schedule**: Mondays at 09:00 America/New_York

When reconciled by Tessl, the scheduled run should:

1. Inspect the plugin collection, project memory, recent commits, open issues, and CI results.
2. Run repository validation.
3. Check `tessl outdated`.
4. Find one focused improvement to plugin quality, eval coverage, CI/CD, or publishing flow.
5. Open or update one pull request.
6. Leave publishing to the manual publish workflow.

The `factory` Tessl environment must be bound to this project and granted GitHub pull-request access before the schedule can open PRs.

## Publishing

Dry-run first:

```bash
DRY_RUN=true scripts/publish-plugins.sh plugins/<plugin-name> patch
```

Publish manually through GitHub Actions after the dry-run passes.
