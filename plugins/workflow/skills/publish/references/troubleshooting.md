# Troubleshooting

Common issues encountered in practice:

- **"Branch X is not allowed to deploy to github-pages"**: The Pages environment protection rules reference the wrong branch. Fix by deleting and recreating Pages: `gh api repos/<org>/<repo>/pages -X DELETE` then re-create.
- **Workflow doesn't trigger on first push**: GitHub sometimes doesn't trigger workflows on the same push that creates the workflow file. Add `workflow_dispatch` trigger and manually dispatch, or push a follow-up commit.
- **Quartz clone brings upstream branches**: Use `--orphan` when creating the main branch to get a clean history.
