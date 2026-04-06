from multi_agent_system.tools.calendar_tools import create_event, list_events, delete_event
import re

def handle(message: str) -> str:
    msg = message.lower()

    # CREATE EVENT
    if any(w in msg for w in ["schedule", "create event", "add event", "new event", "book meeting", "set meeting"]):
        match = re.search(r"(?:schedule|create event|add event|new event|book meeting|set meeting)[:\s]+(.+?)\s+(?:at|on)\s+(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)", message, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            start_time = match.group(2).strip()
            loc_match = re.search(r"(?:at|in|location)\s+([A-Za-z][\w\s]+)$", message, re.IGNORECASE)
            location = loc_match.group(1).strip() if loc_match else ""
            return create_event(title, start_time, location=location)
        return "❓ Please say: 'schedule: <title> on YYYY-MM-DD HH:MM'"

    # LIST EVENTS
    if any(w in msg for w in ["list events", "show events", "my events", "calendar", "show schedule"]):
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", message)
        date_filter = date_match.group(1) if date_match else ""
        return list_events(date_filter)

    # DELETE EVENT
    if any(w in msg for w in ["delete event", "cancel event", "remove event"]):
        match = re.search(r"(\d+)", message)
        if match:
            return delete_event(int(match.group(1)))
        return "❓ Please say: 'delete event 2'"

    return None
