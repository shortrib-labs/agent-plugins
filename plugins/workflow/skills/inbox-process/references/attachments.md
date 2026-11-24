# Attachments

Read this when a note being moved embeds `![[file]]` attachments. Skip in dry-run mode.

1. Resolve each attachment's current location: `Inbox/attachments/`, `Inbox/`, or next to the note.
2. Reject any resolved path containing `..` that escapes the vault.
3. Search the vault for other notes that embed `![[file]]`.
4. If notes going to different destinations share it, leave it in place and log "shared attachment, left in place".
5. Otherwise move it through the CLI, never `mv`: `obsidian move path="<attachment path>" to="<destination>/attachments/"`. Obsidian creates the folder.

If an attachment move fails, log the error and keep the note's move.
