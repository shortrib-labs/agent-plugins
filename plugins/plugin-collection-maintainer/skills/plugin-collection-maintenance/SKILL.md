---
name: plugin-collection-maintenance
description: Use when asked to maintain, audit, clean up, or perform upkeep on a Tessl plugin repository by validating plugins, reviewing skill quality, checking dependency updates, identifying oversized skills or missing evals, and opening focused pull requests.
---

# Plugin collection maintenance

Use this skill for scheduled or manual upkeep of a repository that stores plugins under `plugins/`.

1. Inspect `README.md`, `AGENTS.md`, `tessl.json`, `.tessl/memory/`, recent commits, open issues, and CI results.
2. Run `scripts/validate-plugins.sh` before making changes.
3. For changed skills, run `scripts/review-changed-skills.sh` when Tessl review credentials are available.
4. Check `tessl outdated` and update dependencies only when the change is low risk and easy to validate.
5. Look for one focused improvement:
   - unclear or oversized `SKILL.md`
   - missing or stale reference docs
   - missing eval scenarios for high-value skills
   - plugin manifest drift
   - CI/CD or publishing friction
6. Make the smallest coherent change that improves the collection.
7. Re-run the relevant validation script.
8. Open or update one pull request with:
   - what changed
   - validation run
   - remaining follow-up, if any

Do not publish plugins from this skill. Use the manual publish workflow or `scripts/publish-plugins.sh`.
