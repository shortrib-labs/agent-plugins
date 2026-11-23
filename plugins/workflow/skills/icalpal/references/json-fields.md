# Key JSON fields

### Event Fields
- `title` - Event title
- `start_date` - Start time (Unix timestamp in event's timezone)
- `end_date` - End time (Unix timestamp)
- `sseconds` / `eseconds` - Start/end as Unix epoch seconds
- `sdate` / `edate` - Relative date strings ("today", "tomorrow", etc.)
- `sctime` / `ectime` - Formatted datetime strings
- `all_day` - 1 if all-day event, 0 otherwise
- `calendar` - Calendar name
- `account` - Account name (Google, iCloud, etc.)
- `location` - Event location
- `attendees` - Array of attendee emails
- `notes` - Event description/notes
- `conference_url_detected` - Video conference URL if detected

### Task Fields
- `title` - Task title
- `due_date` - Due date (Unix timestamp, null if undated)
- `due` - Formatted due date string
- `priority` - Priority (0=none, 1=high, 2=medium, 3=low)
- `long_priority` - Human-readable priority
- `completed` - 1 if completed, 0 otherwise
- `flagged` - 1 if flagged, 0 otherwise
- `list_name` - Reminder list name
- `notes` - Task notes
- `tags` - Array of tags
