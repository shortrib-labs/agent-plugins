# Agent Plugins

A Tessl-managed repository for building, validating, improving, and publishing Shortrib Labs agent plugins.

## What is here

- Local Tessl project: `shortrib-labs/agent-plugins`
- Plugin workspace: `shortrib-labs`
- Plugin source directory: `plugins/`
- Maintenance plugin: `plugins/plugin-collection-maintainer`
- CI/CD workflows for validation, skill review, scheduled maintenance, and manual publish

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

- **Plugin collection validation** runs deterministic checks, `tessl schedule validate`, plugin lint, and eval lint.
- **Skill quality review** runs Tessl quality/security review on changed `SKILL.md` files.
- **Plugin maintenance factory** runs the checked-in maintenance skill manually or on a weekly schedule.
- **Publish plugin** is manual and can dry-run or publish one plugin or all plugins.

Required repository secrets:

- `TESSL_TOKEN`
- `ANTHROPIC_API_KEY` for workflows that run `claude-code`

## Publishing

Dry-run first:

```bash
DRY_RUN=true scripts/publish-plugins.sh plugins/<plugin-name> patch
```

Publish manually through GitHub Actions after the dry-run passes.

## Factory loop

1. Humans and agents add or update plugins in `plugins/`.
2. PR validation catches manifest, structure, eval, and skill-quality issues.
3. The weekly maintenance skill looks for one focused improvement and opens a PR.
4. Publish remains a deliberate manual workflow.
5. Findings feed back into plugin docs, skills, evals, checks, or CI.
