# Obsidian CLI commands

Read this when the `obsidian-cli` skill is not installed. Every command takes `path=<vault-relative path>`; avoid `file=`.

- `obsidian vault`: prints the vault name and path. Non-zero exit or the text `Command line interface is not enabled` means stop (see SKILL.md prerequisites).
- `obsidian folders`: prints the folder tree, one path per line.
- `obsidian files folder="Inbox" ext=md`: lists files in a folder. Without `folder=`, lists the whole vault.
- `obsidian read path="Inbox/Note.md"`: prints the note.
- `obsidian links path="Inbox/Note.md"`: prints the notes this note links to, as vault paths.
- `obsidian search query="text" limit=5`: searches note content.
- `obsidian move path="Inbox/Note.md" to="Projects/Acme/"`: moves a note or attachment and rewrites links. Creates the destination folder if it is missing.
- `obsidian reload`: reindexes the vault after moves.

## Properties

- Set a value: `obsidian property:set name="status" value="active" path="..."`
- Set a list: `obsidian property:set name="tags" value="a,b" type=list path="..."`. If append behavior is uncertain, read the current list with `property:read`, merge in memory, and write the complete list.
- Read: `obsidian property:read name="status" path="..."`
- Remove: `obsidian property:remove name="status" path="..."`

## Renaming a property

There is no rename command. Read the old value, set the new name with it, then remove the old name:

1. `obsidian property:read name="link" path="..."`
2. `obsidian property:set name="url" value="<value>" path="..."`
3. `obsidian property:remove name="link" path="..."`
