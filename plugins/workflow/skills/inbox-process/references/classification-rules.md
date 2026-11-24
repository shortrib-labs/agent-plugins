# Classification Rules

Reference for the inbox-process skill. Read this file during Phase 1 to inform classification decisions.

## Destinations

The destination list comes from the vault's live folder tree (`obsidian folders`): every folder under `Projects/`, `Areas/`, `Resources/` and `Archive/`, nested subfolders included. The PARA Design note, when it exists, adds tags and area meanings but never adds or removes destinations. When it disagrees with the folders, the folders win.

## Signal Priority

Consider these signals in roughly this order:

1. **Wiki-link targets** (strongest signal). If a note links to items that live in a specific `Projects/` or `Areas/` subfolder, that subfolder is the likely destination. Count link matches per subfolder.
2. **Frontmatter fields**. Existing `type`, `tags`, and `related` fields are direct hints.
3. **Filename patterns**. Date-prefixed notes containing meeting keywords (sync, standup, 1:1, prep, retro, review, check-in, kickoff, all-hands) are meetings. Date-prefixed notes without meeting keywords need content analysis.
4. **Content analysis**. Topic keywords, headings, and structure reveal the note's purpose. Meeting notes have attendee lists and action items. Research notes have citations and analysis.

## Archive Links Are Weak Signals

A link that resolves to a note in `Archive/` tells you the topic, not the destination. Archived notes often belong to companies or people whose live folder is elsewhere. Count such links for topic only, then look for a live folder (see "Same Name, Wherever It Lives Now"). Never file a note into `Archive/` automatically. If every signal points at the archive, skip the note and log "needs manual filing".

## Same Name, Wherever It Lives Now

Things start as projects and move into areas when they become ongoing. A prospect is a project folder until the deal closes, then it moves under an area; a demo is a project while being built, then moves under an area once maintained. Lost deals go to `Archive/`.

So when a note is about a company or asset, look for a folder with that name anywhere under `Projects/` and `Areas/`, at any depth, and file the note to the live one. The skill never performs the graduation move itself.

## New Companies

A meeting with a company that has no folder anywhere (not under `Projects/`, `Areas/`, `Resources/`, or `Archive/`) is most likely a new prospect. Propose `Projects/<Company>/`. It counts toward the new-folder cap.

## PARA Category Priority

When multiple live categories could fit, prefer:

1. **Projects** (active, time-bound work with a deliverable)
2. **Areas** (ongoing responsibilities)
3. **Resources** (reference material)

When in doubt, put it in the Area.

## Tiebreaking

1. Prefer the subfolder with the most wiki-link matches, excluding `Archive/`.
2. If tied, apply the category priority above.
3. If still ambiguous, choose the most specific folder.

## Subfolder Selection

Match **existing** folders first. Create a new one only when none is a confident match.

- Use Title Case with spaces, matching the existing convention in the tree.
- Cap at **3 new folders per run**. A note that would need a 4th is skipped and logged "needs manual filing".
- The `obsidian move` command creates the destination folder, so a new folder is made by moving the note into it.

## Scope

**Process:**
- All `.md` files in `Inbox/`
- All `.md` files directly at the vault root

**Do not process, and never use as a destination:**
- Files already in `Projects/`, `Areas/`, `Resources/` or `Archive/`
- Any other top-level folder in the vault, derived from the folder tree
- `favorite.md`, Obsidian system files, and the PARA Design and PARA Operating Manual notes

## Special Cases

- **Tag-only resource topics:** Topics with no dedicated Resource folder go to the most relevant Area with the topic tag applied.
- **Empty notes or notes with only frontmatter:** Skip and log "empty, needs manual review".
- **Notes that defy classification:** Skip and log "needs manual filing".
