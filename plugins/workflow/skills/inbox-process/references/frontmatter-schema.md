# Frontmatter Schema

Reference for the inbox-process skill. Defines the canonical frontmatter fields, controlled vocabularies, and field handling rules.

## Canonical Fields

Every processed note must have these fields after processing:

- `date` (required): Preserve the existing format; don't fight the Obsidian Linter's date format. If missing, use file creation date or today.
- `type` (required): Controlled vocabulary (see below). Inferred from content if not present.
- `tags` (required): YAML list of flat tags from the PARA Design taxonomy when that note exists. Can be an empty list.
- `last_updated` (required): ISO 8601 (YYYY-MM-DD). Set to today's date on processing.
- `status` (required): Controlled vocabulary (see below). Set based on type if not present.
- `aliases` (when applicable): YAML list of abbreviations, informal names, shortened titles. Only add when obvious.

## Type Vocabulary

Flat list, no hierarchy:

- `meeting` - Meeting notes, syncs, 1:1s, all-hands, retros, kickoffs
- `brief` - Decision documents, proposals, recommendations
- `research` - Analysis, investigation, deep-dives
- `concept` - Ideas, explorations, thought pieces
- `session-transcript` - AI session logs, Claude transcripts
- `strategy` - Strategic plans, roadmaps, vision documents
- `vendor-profile` - Vendor assessments, product evaluations
- `case-study` - Customer stories, implementation examples
- `idea` - Quick captures, seeds for future work
- `reference` - How-to guides, cheat sheets, documentation

Meeting subtypes (1:1, sync, all-hands, retro, kickoff, customer-call, direct-report) are expressed as **tags**, not as type values.

## Status Vocabulary

Tight lifecycle:

- `draft` - Work in progress, not yet actionable
- `active` - Current, relevant, actionable
- `waiting` - Blocked on someone or something
- `complete` - Finished, outcome achieved
- `archived` - No longer relevant, kept for reference

### Default Status by Type

When a note has no existing `status` field:

- `meeting`, `brief`, `strategy`, `vendor-profile`, `case-study`, `reference`: `active`
- `idea`, `concept`, `research`: `draft`
- `session-transcript`: `complete`

## Tag Taxonomy

Tags are read from the PARA Design note at runtime when it exists (search for it; see SKILL.md). Do not hardcode them here. Without the note, reuse tags already on the note and in the vault, and add none you cannot justify. The note defines three tag categories:

- **Topic tags** - Subject matter (#cooking, #ai, #sales, etc.)
- **Entity tags** - People, pets, tools, companies (#leo, #shelley, etc.)
- **Workflow tags** - Status/process (#review, #waiting, #someday)

Apply tags that match the note's content. Use existing tags from the taxonomy. Do not invent new tags unless the note clearly covers a topic not represented in the taxonomy.

Meeting characteristics are expressed as tags: `1:1`, `sync`, `direct-report`, `customer-call`, `all-hands`, `retro`, `kickoff`, `standup`, `prep`.

## Field Handling Rules

### Preserving Existing Fields

- **Non-canonical fields** (e.g., `researcher`, `git_commit`, `branch`, `source`, `transcript`, `related`): Preserve as-is. Never remove or rename fields you don't recognize.
- **Existing canonical fields with values:** Merge, don't overwrite. If a note already has `tags: [ai, sales]`, add new tags to the list rather than replacing.
- **`title` field:** Preserve if present. The Obsidian Linter manages this field.
- **`aliases` field:** Preserve existing aliases. Only append new obvious ones.

### Synonym Mapping

Known synonyms that should be renamed to canonical form:

- `link` becomes `url` (different semantic meaning from wiki-links)

The Obsidian Linter manages a `last updated` field (with a space). Leave it alone. The skill's canonical field is `last_updated` (with an underscore). Both can coexist.

### Renaming Process

Renaming a frontmatter field via Obsidian CLI requires three steps:

1. `obsidian property:read name="old_name" path="..."` - Read the current value
2. `obsidian property:set name="new_name" value="..." path="..."` - Set the new field
3. `obsidian property:remove name="old_name" path="..."` - Remove the old field

### Unrecognized Vocabulary Values

When existing `type` or `status` values don't match the controlled vocabulary:

- **Preserve the original value.** Do not silently overwrite.
- **Log a warning:** "Note X has unrecognized type/status 'Y', preserved as-is."
- The user can review and correct these manually.
