from google.adk.tools import FunctionTool
from multi_agent_system.database.db import get_connection

def _create_task(title: str, priority: str = "medium", due_date: str = "") -> str:
    """Create a new task and store it in the database.
    
    Args:
        title: The title of the task
        priority: Priority level - low, medium, or high
        due_date: Optional due date in YYYY-MM-DD HH:MM format
    
    Returns:
        Confirmation message with task ID
    """
    valid_priorities = ["low", "medium", "high"]
    if priority not in valid_priorities:
        priority = "medium"
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (title, priority, due_date)
    )
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    return (
        f"✅ Task Created Successfully!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID      : {task_id}\n"
        f"📌 Title   : {title}\n"
        f"⚡ Priority : {priority.capitalize()}\n"
        f"📅 Due     : {due_date if due_date else 'Not set'}"
    )

def _list_tasks(status: str = "all") -> str:
    """List all tasks from the database, optionally filtered by status.
    
    Args:
        status: Filter by status - all, pending, in_progress, or completed
    
    Returns:
        Formatted list of tasks
    """
    conn = get_connection()
    c = conn.cursor()
    if status == "all":
        c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    else:
        c.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC", (status,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return f"📋 No tasks found."
    status_emoji = {"pending": "🔵", "in_progress": "🟡", "completed": "🟢"}
    priority_emoji = {"low": "🟩", "medium": "🟨", "high": "🟥"}
    result = f"📋 Task List — {len(rows)} task(s) found\n"
    result += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in rows:
        s_emoji = status_emoji.get(r['status'], "⚪")
        p_emoji = priority_emoji.get(r['priority'], "⚪")
        result += f"{s_emoji} [{r['id']}] {r['title']}\n"
        result += f"     Priority: {p_emoji} {str(r['priority']).capitalize()} | Status: {r['status'].replace('_',' ').title()}"
        if r['due_date']:
            result += f" | Due: {r['due_date']}"
        result += "\n"
    return result.strip()

def _update_task(task_id: int, status: str) -> str:
    """Update the status of an existing task.
    
    Args:
        task_id: The ID of the task to update
        status: New status - pending, in_progress, or completed
    
    Returns:
        Confirmation message
    """
    valid = ["pending", "in_progress", "completed"]
    if status not in valid:
        return f"❌ Invalid status. Use: {', '.join(valid)}"
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected == 0:
        return f"❌ Task ID {task_id} not found."
    status_emoji = {"pending": "🔵", "in_progress": "🟡", "completed": "🟢"}
    return f"{status_emoji.get(status,'✅')} Task [{task_id}] marked as {status.replace('_',' ').title()}."

def _delete_task(task_id: int) -> str:
    """Delete a task from the database.
    
    Args:
        task_id: The ID of the task to delete
    
    Returns:
        Confirmation message
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected == 0:
        return f"❌ Task ID {task_id} not found."
    return f"🗑️ Task [{task_id}] deleted successfully."

# MCP-compliant tool definitions
create_task = FunctionTool(_create_task)
list_tasks  = FunctionTool(_list_tasks)
update_task = FunctionTool(_update_task)
delete_task = FunctionTool(_delete_task)
