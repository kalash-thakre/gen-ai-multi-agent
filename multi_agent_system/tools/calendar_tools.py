from google.adk.tools import FunctionTool
from multi_agent_system.database.db import get_connection

def _create_event(title: str, start_time: str, end_time: str = "", description: str = "", location: str = "") -> str:
    """Create a new calendar event.
    
    Args:
        title: Title of the event
        start_time: Start time in YYYY-MM-DD HH:MM format
        end_time: Optional end time in YYYY-MM-DD HH:MM format
        description: Optional description
        location: Optional location
    
    Returns:
        Confirmation message with event ID
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO events (title, description, start_time, end_time, location) VALUES (?,?,?,?,?)",
        (title, description, start_time, end_time, location)
    )
    conn.commit()
    event_id = c.lastrowid
    conn.close()
    return (
        f"📅 Event Created Successfully!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID       : {event_id}\n"
        f"📌 Title    : {title}\n"
        f"🕐 Start    : {start_time}\n"
        f"🕐 End      : {end_time if end_time else 'Not set'}\n"
        f"📍 Location : {location if location else 'Not set'}"
    )

def _list_events(date_filter: str = "") -> str:
    """List all calendar events, optionally filtered by date.
    
    Args:
        date_filter: Optional date filter in YYYY-MM-DD format
    
    Returns:
        Formatted list of events
    """
    conn = get_connection()
    c = conn.cursor()
    if date_filter:
        c.execute("SELECT * FROM events WHERE start_time LIKE ? ORDER BY start_time", (f"{date_filter}%",))
    else:
        c.execute("SELECT * FROM events ORDER BY start_time")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "📅 No events found."
    result = f"📅 Events — {len(rows)} found\n"
    result += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in rows:
        result += f"🗓️ [{r['id']}] {r['title']} | {r['start_time']}"
        if r['location']:
            result += f" | 📍 {r['location']}"
        result += "\n"
    return result.strip()

def _delete_event(event_id: int) -> str:
    """Delete a calendar event.
    
    Args:
        event_id: The ID of the event to delete
    
    Returns:
        Confirmation message
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected == 0:
        return f"❌ Event ID {event_id} not found."
    return f"🗑️ Event [{event_id}] deleted successfully."

create_event = FunctionTool(_create_event)
list_events  = FunctionTool(_list_events)
delete_event = FunctionTool(_delete_event)
