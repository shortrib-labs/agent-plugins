# Agent Plugins

A Tessl-managed repository for building, validating, improving, and publishing Shortrib Labs agent plugins.

## What is here

- Local Tessl project: `shortrib-labs/agent-plugins`
- Plugin workspace: `shortrib-labs`
- Plugin source directory: `plugins/`
- Maintenance plugin: `plugins/plugin-collection-maintainer`
- Tessl issue-to-PR factory actions and weekly maintenance schedule declared in `tessl.json`
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

## Tessl issue-to-PR factory

GitHub Issues are the primary ticket queue for this repository.

To delegate work to Tessl:

1. Create a GitHub issue with a clear goal, context, acceptance criteria, and validation commands.
2. Add the `tessl` label.
3. Tessl runs `implement-ticket` with `tessl/factory#implement-github-issue` using `claude-code` in the `factory` environment.
4. Tessl opens one PR for the issue.
5. Review comments, PR comments, and check results wake `shepherd-pull-request` so Tessl can keep the PR moving.

To take work back from Tessl, remove the `tessl` label or close the issue.

The `.github/ISSUE_TEMPLATE/tessl-task.yml` template applies the `tessl` label and captures the information the factory needs.

## Tessl maintenance loop

The weekly maintenance loop is also declared in `tessl.json`:

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

The `factory` Tessl environment is bound to this project and has GitHub write access so it can manage issues and pull requests.

## Publishing

Dry-run first:

```bash
DRY_RUN=true scripts/publish-plugins.sh plugins/<plugin-name> patch
```

Publish manually through GitHub Actions after the dry-run passes.
