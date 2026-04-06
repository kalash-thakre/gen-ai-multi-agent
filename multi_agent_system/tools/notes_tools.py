from google.adk.tools import FunctionTool
from multi_agent_system.database.db import get_connection
from datetime import datetime

def _create_note(title: str, content: str, tags: str = "") -> str:
    """Create a new note and save it to the database.
    
    Args:
        title: Title of the note
        content: Content body of the note
        tags: Optional comma-separated tags
    
    Returns:
        Confirmation message with note ID
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content, tags) VALUES (?,?,?)", (title, content, tags))
    conn.commit()
    note_id = c.lastrowid
    conn.close()
    return (
        f"📝 Note Created Successfully!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID      : {note_id}\n"
        f"📌 Title   : {title}\n"
        f"📄 Content : {content[:80] + '...' if len(content) > 80 else content}\n"
        f"🏷️  Tags    : {tags if tags else 'None'}"
    )

def _list_notes(tag_filter: str = "") -> str:
    """List all notes, optionally filtered by tag.
    
    Args:
        tag_filter: Optional tag to filter notes by
    
    Returns:
        Formatted list of notes
    """
    conn = get_connection()
    c = conn.cursor()
    if tag_filter:
        c.execute("SELECT * FROM notes WHERE tags LIKE ? ORDER BY updated_at DESC", (f"%{tag_filter}%",))
    else:
        c.execute("SELECT * FROM notes ORDER BY updated_at DESC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "📝 No notes found."
    result = f"📝 Notes — {len(rows)} found\n"
    result += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in rows:
        preview = r['content'][:60] + "..." if len(r['content']) > 60 else r['content']
        result += f"📄 [{r['id']}] {r['title']}\n     {preview}\n"
        if r['tags']:
            result += f"     🏷️ {r['tags']}\n"
    return result.strip()

def _search_notes(query: str) -> str:
    """Search notes by title or content keyword.
    
    Args:
        query: Keyword to search for in notes
    
    Returns:
        Matching notes
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
        (f"%{query}%", f"%{query}%")
    )
    rows = c.fetchall()
    conn.close()
    if not rows:
        return f"🔍 No notes found matching '{query}'"
    result = f"🔍 Results for '{query}' — {len(rows)} found\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in rows:
        result += f"📄 [{r['id']}] {r['title']}\n     {r['content'][:80]}\n"
    return result.strip()

def _update_note(note_id: int, title: str = "", content: str = "") -> str:
    """Update an existing note's title or content.
    
    Args:
        note_id: ID of the note to update
        title: New title (optional)
        content: New content (optional)
    
    Returns:
        Confirmation message
    """
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    if title and content:
        c.execute("UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?", (title, content, now, note_id))
    elif title:
        c.execute("UPDATE notes SET title=?, updated_at=? WHERE id=?", (title, now, note_id))
    elif content:
        c.execute("UPDATE notes SET content=?, updated_at=? WHERE id=?", (content, now, note_id))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected == 0:
        return f"❌ Note ID {note_id} not found."
    return f"✅ Note [{note_id}] updated successfully."

create_note = FunctionTool(_create_note)
list_notes  = FunctionTool(_list_notes)
search_notes = FunctionTool(_search_notes)
update_note = FunctionTool(_update_note)
