# Report and log formats

Read this in Phase 3.

## Terminal summary

```
## Inbox Processing Complete

Processed: N | Skipped: M | Errors: E | New folders: F

### Moved
- Note Title: Inbox/ -> Projects/Acme/ (meeting)

### Skipped (if any)
- Empty Note: empty, needs manual review

### Warnings (if any)
- Note X has unrecognized type 'foo', preserved as-is
- Shared attachment image.png left in place (referenced by Note A and Note B)

### New Folders Created (if any)
- Projects/Acme/
```

In dry-run mode, prefix with `[DRY RUN] No changes were made.` and list "Would move" lines instead of "Moved".

## Monthly log

Skip in dry-run mode. Append to `~/.local/share/inbox-process/logs/YYYY-MM.md`, creating the directory if needed. If the file is new, start it with `# Inbox Processing Log - YYYY-MM`. Then append:

```markdown
## YYYY-MM-DD HH:MM

- Note Title: Inbox/ -> Projects/Acme/ (meeting)
- Other Note: Inbox/ -> Resources/New Topic/ (concept, new folder)

Processed: N | Skipped: M | Errors: E | New folders: F
```

Include skipped notes with their reason, such as "needs manual filing".
