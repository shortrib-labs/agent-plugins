---
name: inbox-process
description: >
  Scan, classify, enrich, and file Obsidian notes from Inbox/ and the vault root
  into the PARA folder structure. Use when the user wants to process their inbox,
  triage notes, or organize unfiled content. Triggers on "process inbox",
  "triage notes", "file inbox", "organize notes", "clean up inbox".
argument-hint: "[--dry-run] [--batch-size N]"
disable-model-invocation: true
allowed-tools: Bash(obsidian *), Bash(mkdir *), Bash(kill -0 *), Read, Glob, Grep
---

# Inbox Process

Scan, classify, and file Obsidian notes from Inbox/ and the vault root into the PARA folder structure. The vault's live folder tree is the source of truth for where notes can go. Every move goes through the Obsidian CLI, never `mv`: the vault uses Obsidian Sync, which can revert changes made outside Obsidian, and the CLI keeps wiki-links intact.

## Arguments

Parse `$ARGUMENTS` for:
- `--dry-run`: Classify and report without moving or editing anything.
- `--batch-size N`: Maximum notes to process per run. Default: 25.

## Prerequisites

1. **Check the CLI.** Run `obsidian vault`. Read its output and exit code:
   - Output contains `Command line interface is not enabled`: stop and report "The Obsidian command line interface is not enabled. Please turn it on in Settings > General > Advanced." Do not fall back to `mv` or any other file operation.
   - Any other failure: stop and report "Obsidian is not running. Start Obsidian and try again." Do not try to launch it.
   - Success: the output includes the vault path. Use it wherever a vault path is needed, and never write one into commands from memory.

2. **Use the CLI reference.** If the `obsidian-cli` skill is installed, use it for command syntax. Plugins cannot declare dependencies, so the commands this skill needs are in [references/obsidian-cli.md](references/obsidian-cli.md); read it when `obsidian-cli` is not installed. Use `path=` (not `file=`) for deterministic resolution.

3. **Read the rules.** Read [classification-rules.md](references/classification-rules.md) and [frontmatter-schema.md](references/frontmatter-schema.md) before classifying anything.

## Phase 1: Gather Context

### 1.1 Build the destination list from the folder tree

Run `obsidian folders`. Destinations are every folder under `Projects/`, `Areas/`, `Resources/` and `Archive/`, nested subfolders included. Every other top-level folder (Daily, Readwise, Books, Templates, Excalidraw, Clippings, and whatever else the vault has) is neither processed nor a destination. Derive that list from the output; do not hardcode it.

### 1.2 Read the PARA Design note (optional)

Search for it with `obsidian search query="PARA" limit=5`; do not assume a path. If found, use it for the tag taxonomy and the meaning of each area. If it is missing, carry on without it. When it disagrees with the folder tree, the folder tree wins.

### 1.3 Enumerate notes to process

1. `obsidian files folder="Inbox" ext=md` for Inbox notes.
2. `obsidian files ext=md` for the whole vault, keeping only paths with no `/`, for loose notes at the root.

Exclude the PARA Design and PARA Operating Manual notes, `favorite.md`, and anything that is not `.md`. Sort alphabetically by filename and trim to `--batch-size`.

Report: "Found N notes to process (M in Inbox, K at vault root). Batch size: B."

## Phase 2: Classify and Execute

Process each note in order.

### 2.1 Read the note

`obsidian read path="<path>"` for content and frontmatter, `obsidian links path="<path>"` for wiki-link targets, and scan the body for `![[...]]` attachments.

### 2.2 Classify the destination

Apply [classification-rules.md](references/classification-rules.md). In short:
- Link targets are the strongest signal, but a link into `Archive/` only tells you the topic. Never file into `Archive/` automatically. If the only signals point there, skip the note and log "needs manual filing".
- When the note is about a company or asset, find a folder with that name anywhere under `Projects/` and `Areas/` and use the live one. Never perform a graduation move between them yourself.
- A meeting with a company that has no folder anywhere is most likely a new prospect: propose `Projects/<Company>/`.
- Empty notes, or notes with only frontmatter: skip and log "empty, needs manual review".
- Truly ambiguous notes: skip and log "needs manual filing" with a one-line explanation.

New folders are capped at 3 per run. A note that needs a 4th is skipped and logged "needs manual filing".

### 2.3 Normalize frontmatter

Apply [frontmatter-schema.md](references/frontmatter-schema.md). Merge, never overwrite, and keep fields you do not recognize. Use `obsidian property:set` with `path=`; the commands for lists and renames are in [references/obsidian-cli.md](references/obsidian-cli.md). Skip this step in dry-run mode.

### 2.4 Move the note

In dry-run mode, print the proposed move and go on:

```
[DRY RUN] Would move: "Note Title" -> Projects/Acme/ (type: meeting, tags: [acme])
```

Otherwise run `obsidian move path="<current-path>" to="<destination-folder>/"`. Obsidian creates a missing destination folder as part of the move, so there is no separate folder step. Then move embedded attachments as described in [references/attachments.md](references/attachments.md).

If any step fails for a note, log the error and continue with the next note.

### 2.5 Track the result

Keep per note: filename, source, destination, inferred type, whether a new folder was created, and any warnings.

## Phase 3: Report

Print the terminal summary and append the monthly log using the formats in [references/report-and-log.md](references/report-and-log.md). In dry-run mode, prefix the summary with `[DRY RUN] No changes were made.`, show "Would move" rows, and do not write the log or reload. After real moves, run `obsidian reload`.

## Error Handling

- **Single note failure:** log, skip, continue.
- **CLI stops responding mid-run:** retry once. If it fails again, stop and report what was completed.
- **Three consecutive failures:** pause and check whether one root cause affects all remaining notes.
- **Path safety:** reject any path containing `..` that would escape the vault path reported by `obsidian vault`.
