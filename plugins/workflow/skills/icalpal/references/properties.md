# Property selection

### Event Properties
Available: ROWID, UUID, account, address, all_day, attendees, availability, calendar, color, conference_url_detected, count, duration, end_date, end_tz, flags, frequency, has_recurrences, interval, invitation_status, location, notes, orig_date, orig_item_id, rend_date, specifier, start_date, start_tz, status, subcal_url, symbolic_color_name, title, trigger_interval, type, unique_identifier, url, xdate

- `--iep=PROPERTIES` - Include only these event properties
- `--eep=PROPERTIES` - Exclude these event properties
- `--aep=PROPERTIES` - Add properties to default list

### Task Properties
Available: alert, all_day, assignee, badge, color, completed, due_date, flagged, grocery, group, id, list_name, location, members, messaging, notes, parent, priority, proximity, radius, shared, tags, title, url, utc_offset

- `--itp=PROPERTIES` - Include only these task properties
- `--etp=PROPERTIES` - Exclude these task properties
- `--atp=PROPERTIES` - Add properties to default list

Use `--iep=all` or `--itp=all` to include all properties.
