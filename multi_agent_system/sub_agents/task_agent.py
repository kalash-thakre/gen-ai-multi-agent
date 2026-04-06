from multi_agent_system.tools.task_tools import create_task, list_tasks, update_task, delete_task
import re

def handle(message: str) -> str:
    msg = message.lower().strip()

    # CREATE TASK
    if any(w in msg for w in ["create task", "add task", "new task"]):
        # Extract everything after the keyword
        match = re.search(r"(?:create task|add task|new task)[:\s]+(.+)", message, re.IGNORECASE)
        if match:
            rest = match.group(1).strip()
            # Extract optional priority
            priority = "medium"
            p_match = re.search(r"\bpriority[:\s]+(\w+)", rest, re.IGNORECASE)
            if p_match:
                priority = p_match.group(1).lower()
                rest = re.sub(r"\bpriority[:\s]+\w+", "", rest).strip()
            # Extract optional due date
            due = ""
            d_match = re.search(r"\bdue[:\s]+(\S+)", rest, re.IGNORECASE)
            if d_match:
                due = d_match.group(1)
                rest = re.sub(r"\bdue[:\s]+\S+", "", rest).strip()
            title = rest.strip(": ").strip()
            if title:
                return create_task(title, priority=priority, due_date=due)
        return (
            "❓ Please type the full command in one line:\n"
            "`create task: Buy groceries`\n"
            "`create task: Submit report priority high due 2025-04-10`"
        )

    # LIST TASKS
    if any(w in msg for w in ["list task", "show task", "my task", "all task", "view task"]):
        if "pending" in msg:
            return list_tasks("pending")
        elif "complet" in msg:
            return list_tasks("completed")
        elif "progress" in msg:
            return list_tasks("in_progress")
        return list_tasks("all")

    # COMPLETE / UPDATE TASK
    if any(w in msg for w in ["complete task", "finish task", "done task", "mark task", "update task"]):
        match = re.search(r"(\d+)", message)
        if match:
            task_id = int(match.group(1))
            if any(w in msg for w in ["complet", "done", "finish"]):
                return update_task(task_id, "completed")
            elif "progress" in msg:
                return update_task(task_id, "in_progress")
            elif "pending" in msg:
                return update_task(task_id, "pending")
            return update_task(task_id, "completed")
        return "❓ Please say: `complete task 3`"

    # DELETE TASK
    if any(w in msg for w in ["delete task", "remove task"]):
        match = re.search(r"(\d+)", message)
        if match:
            return delete_task(int(match.group(1)))
        return "❓ Please say: `delete task 3`"

    return None
