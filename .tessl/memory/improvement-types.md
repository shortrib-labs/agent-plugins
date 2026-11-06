# Improvement types

Use this project taxonomy when classifying opportunities found from plugin reviews, CI failures, scheduled maintenance, or PR feedback.

- **Skill**: Improve instructions, activation trigger, workflow steps, safety boundaries, or outputs in a skill.
- **Review skill**: Add or tune a code-review lens or skill/plugin review rubric.
- **Rule**: Add durable guidance that should apply broadly to future agent work.
- **Hook**: Add local or CI automation that runs before, during, or after agent work.
- **Test**: Add deterministic tests, lint, schema validation, eval scenarios, or golden checks.
- **Refactor**: Restructure plugins, references, scripts, or manifests to make future agent work safer and simpler.
- **Verifier**: Add a `tessl change verify` rule for binary file invariants that are better judged by LLM than deterministic tooling.
- **Publishing**: Improve versioning, visibility, release notes, dry-runs, or registry publishing flow.
