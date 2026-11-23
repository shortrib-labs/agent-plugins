---
name: publish
description: Publish a collection of markdown or HTML files as a navigable Quartz site on GitHub Pages with org-level access control. Use when sharing research, session transcripts, meeting notes, or any clump of hypertext with colleagues.
---

# Publish Hypertext

Publish a collection of interconnected documents as a navigable website on GitHub Pages. Produces a Quartz site with graph view, backlinks, wiki-link resolution, search, and hover previews. Access is restricted to GitHub org members when the repo is private.

## Arguments

`$1` is a natural language description of what to publish. Examples:
- "the OpenHands research and meeting summaries"
- "my Claude Code session from today"
- "the files in docs/research/"

## Phase 1: Gather

1. **Identify the source files.** Parse the user's description to determine which files to include. This might be:
   - A list of specific files or directories
   - A glob pattern
   - Files matching a tag or topic
   - A single note and everything it links to (follow wiki-links one level deep)

2. **Confirm the file list with the user.** Show the files that will be published and ask if anything should be added or removed. Include file count and rough total size.

3. **Ask where to publish.** The user needs to provide:
   - **GitHub org** (or personal account)
   - **Repo name** (will be created if it doesn't exist)
   - **Visibility**: private (default, org-only access) or public

## Phase 2: Scaffold

4. **Check if the repo exists.**
   - If it exists and already has Quartz: update the `content/` directory with the new files.
   - If it exists but is empty: set up Quartz from scratch.
   - If it doesn't exist: create it with `gh repo create`, then set up Quartz.

5. **Set up Quartz** (only for new sites). Clone the Quartz template repo and configure it:

   ```bash
   git clone --branch v5.2.2 --depth 1 https://github.com/jackyzha0/quartz.git <repo-dir>
   cd <repo-dir>
   git remote set-url origin git@github.com:<org>/<repo>.git
   npm install
   ```

   Configure `quartz.config.ts` as described in [references/quartz-config.md](references/quartz-config.md), which lists each setting to change.

6. **Create the deploy workflow** at `.github/workflows/deploy.yml`:

   Copy [assets/deploy.yml](assets/deploy.yml) to that path unchanged. It builds with `npx quartz build` and deploys from `main` with Pages permissions.

## Phase 3: Populate

7. **Copy source files into `content/`.** Preserve directory structure relative to the common ancestor of the source files. For example, if publishing files from `Replicated/Vendors/OpenHands/Summaries/` and `Replicated/Strategy/`, the content directory might look like:

   ```
   content/
   ├── index.md          (generated landing page or user-specified)
   ├── openhands/
   │   └── summaries/
   └── strategy/
   ```

8. **Generate an index page** if the source files don't include one. The index should:
   - Have a `title` field in frontmatter (ask the user what to call it)
   - Link to all included documents, organized by directory/topic
   - Include a brief description of what this collection contains

9. **Handle frontmatter cleanup.** Obsidian frontmatter sometimes has fields that Quartz can't parse:
   - Dates in non-ISO format (e.g., "Friday, March 13th 2026, 12:00:00 am") -- these produce warnings but don't break the build, so leave them
   - `transcript` or other fields with wiki-links -- add an explicit link in the page body since frontmatter wiki-links aren't rendered
   - Remove any `cssclasses` or Obsidian-only fields that would be confusing in the published output

10. **Strip local-only references.** Scan for and remove:
    - Absolute file paths (e.g., `/Users/chuck/workspace/...`)
    - References to files not included in the publish set (broken wiki-links are fine -- Quartz handles them gracefully -- but explicit "see file X" references to missing files should be flagged)

## Phase 4: Deploy

11. **Create an orphan `main` branch** to avoid inheriting Quartz's git history:

    ```bash
    git checkout --orphan main
    git add -A
    git commit -m "Publish: <description>"
    ```

12. **Push and set as default branch:**

    ```bash
    git push -u origin main
    gh api repos/<org>/<repo> -X PATCH -f default_branch=main
    ```

13. **Enable GitHub Pages** with Actions as the build source:

    ```bash
    gh api repos/<org>/<repo>/pages -X POST -f "build_type=workflow"
    ```

14. **Wait for the deploy workflow to complete.** Watch with:

    ```bash
    gh run watch --repo <org>/<repo> <run-id> --exit-status
    ```

15. **Get the Pages URL** and update `baseUrl` in `quartz.config.ts` if it differs from what was configured. Push the update if needed.

16. **Report the result:**
    - The live URL
    - Who can access it (org members for private repos, everyone for public)
    - How to update: "push to main and it redeploys automatically"

## More detail

- If the repo already exists with Quartz content, read [references/updating-an-existing-site.md](references/updating-an-existing-site.md).
- If a deploy fails or a workflow does not trigger, read [references/troubleshooting.md](references/troubleshooting.md).
