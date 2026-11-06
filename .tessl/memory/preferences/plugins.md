# Plugins

## Plugin directory

Plugin directories are created under:

- `plugins/`

## Workspace

Use Tessl workspace prefix:

- `shortrib-labs/`

## Local plugin dependencies

Local plugins should be listed in root `tessl.json` dependencies with file sources:

```json
"shortrib-labs/<plugin-name>": {
  "source": "file:plugins/<plugin-name>"
}
```

## Hook scripts directory

Hook and helper scripts are written under:

- `scripts/`

## Hook script language

- Bash for shell wrappers.
- Python for deterministic repository validation.

## Quality conventions

- `SKILL.md` should stay concise and delegate detail to `references/`.
- Plugin manifests stay `private: true` until publishing visibility is intentionally changed.
- Add eval scenarios under `evals/` for high-value or frequently changed skills.
- Use `scripts/validate-plugins.sh` for local and CI validation.
- Use `scripts/review-changed-skills.sh` for Tessl quality/security review of changed skills.
