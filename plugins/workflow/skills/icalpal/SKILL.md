---
name: icalpal
description: Query macOS Calendar and Reminders using icalpal CLI. Use this skill when you need to fetch calendar events, reminders/tasks, or calendar metadata from the local macOS Calendar database. Supports filtering by date, calendar, account, and various output formats including JSON.
---

# icalpal Calendar Query Skill

Query macOS Calendar events and Reminders using the icalpal command-line tool.

Install icalpal via Homebrew: `brew install icalpal`

## Commands

### Event Commands
- `events` - Print all events
- `eventsToday` - Print events occurring today
- `eventsToday+N` - Print events from today through N days ahead (e.g., `eventsToday+7` for the week)
- `eventsNow` - Print events occurring at the present time
- `eventsRemaining` - Print events from now until midnight

### Task/Reminder Commands
- `tasks` or `reminders` - Print all tasks
- `datedTasks` - Print tasks with a due date
- `undatedTasks` - Print tasks with no due date
- `tasksDueBefore` - Print uncompleted tasks due between given dates

### Metadata Commands
- `calendars` - Print available calendars
- `accounts` or `stores` - Print calendar accounts

## Output Formats

Use `-o FORMAT` to specify output format:
- `json` - JSON format (best for programmatic use)
- `default` - Human-readable default format
- `ansi` - Colored terminal output
- `csv` - Comma-separated values
- `md` - Markdown format
- `yaml` - YAML format
- `html` - HTML format
- `xml` - XML format

**Recommendation**: Always use `-o json` when processing data programmatically.

## Date Filtering

- `--from=DATE` - Events starting on or after DATE
- `--to=DATE` - Events starting on or before DATE
- `--days=N` - Show N days of events including start date
- `-n` - Include only events from now on

DATE can be: `yesterday`, `today`, `tomorrow`, `+N`, `-N`, or any DateTime.parse() format.

## Calendar/Account Filtering

Common: `--ic`/`--ec` include or exclude calendars, `--il`/`--el` include or exclude reminder lists, `--et=Birthdays` excludes a calendar type.

Read [references/filters.md](references/filters.md) when you need account filters (`--is`/`--es`), the full list of calendar types, or exact filter semantics.

## Task Filtering

- `--id` - Include completed reminders
- `--ed` - Exclude uncompleted reminders

## Event Filtering

- `--ia` - Include only all-day events
- `--ea` - Exclude all-day events
- `--match=FIELD=REGEX` - Include items where FIELD matches REGEX (case insensitive)

## Property Selection

Use `--iep=PROPERTIES` (events) or `--itp=PROPERTIES` (tasks) to limit output to named properties, and `--iep=all` or `--itp=all` for everything.

Read [references/properties.md](references/properties.md) for the available property names and the exclude/add variants (`--eep`, `--aep`, `--etp`, `--atp`).

## Sorting and Formatting

- `--sort=PROPERTY` - Sort by property
- `--std` - Sort tasks by due date
- `-r` - Reverse sort order
- `--sc` - Separate by calendar
- `--sd` - Separate by date
- `--sp` - Separate by priority
- `--li=N` - Limit to N items

## Usage Examples

### Get today's events as JSON
```bash
icalpal eventsToday -o json
```

### Get this week's events from a specific calendar
```bash
icalpal eventsToday+7 --ic="chuck@replicated.com" -o json
```

### Get events for the next 14 days excluding birthdays
```bash
icalpal eventsToday+14 --et=Birthdays -o json
```

### Get all tasks with due dates sorted by date
```bash
icalpal datedTasks --std -o json
```

### Get tasks from a specific reminder list
```bash
icalpal tasks --il="To Do" -o json
```

### Get events containing "meeting" in the title
```bash
icalpal events --match=title=meeting -o json
```

### Get remaining events today with specific properties
```bash
icalpal eventsRemaining --iep=title,start_date,end_date,location,attendees -o json
```

### List all calendars
```bash
icalpal calendars -o json
```

## Key JSON Fields

Read [references/json-fields.md](references/json-fields.md) when you need to interpret JSON output, such as timestamps, all-day flags or task priority values.

## Notes

- icalpal reads directly from the macOS Calendar SQLite database
- Changes made in Calendar.app may take a moment to appear
- Some calendars (like Google) sync periodically
- The tool is read-only; it cannot create or modify events
