###
# Generated wit ChatGPT
###

import json
from datetime import datetime, timedelta
import pytz

INPUT_FILE = "data/CppCon2025.json"
OUTPUT_FILE = "cppcon2025.ics"

# Load JSON
with open(INPUT_FILE) as f:
    events = json.load(f)

tz = pytz.timezone("America/Denver")


def format_dt(dt: datetime) -> str:
    # Format as UTC for ICS
    return dt.strftime("%Y%m%dT%H%M%SZ")


ics_events = []
for ev in events:
    start = datetime.fromisoformat(ev["begin"])
    if start.tzinfo is None:
        start = pytz.UTC.localize(start)  # assume UTC if missing
    start = start.astimezone(tz)

    dur = timedelta(minutes=ev["duration"])
    end = start + dur

    # ICS requires UTC
    start_utc = start.astimezone(pytz.UTC)
    end_utc = end.astimezone(pytz.UTC)

    ics_event = f"""BEGIN:VEVENT
UID:{ev["name"].replace(" ", "_")}#{ev["tracks"] if "tracks" in ev else ""}
SEQUENCE:0
SUMMARY:{ev["name"]} {ev["tracks"] if "tracks" in ev else ""}
DTSTART:{format_dt(start_utc)}
DTEND:{format_dt(end_utc)}
END:VEVENT"""
    ics_events.append(ics_event)

ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\n" + \
    "\n".join(ics_events) + "\nEND:VCALENDAR\n"

with open(OUTPUT_FILE, "w") as f:
    f.write(ics_content)

print(f"ICS file written to {OUTPUT_FILE}")
