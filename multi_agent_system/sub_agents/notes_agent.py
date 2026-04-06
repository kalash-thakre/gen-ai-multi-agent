from multi_agent_system.tools.notes_tools import create_note, list_notes, search_notes, update_note
import re

def handle(message: str) -> str:
    msg = message.lower()

    # CREATE NOTE
    if any(w in msg for w in ["create note", "add note", "new note", "save note", "take note"]):
        match = re.search(r"(?:create note|add note|new note|save note|take note)[:\s]+(.+?)(?:\s+content[:\s]+(.+?))?(?:\s+tags?[:\s]+(.+))?$", message, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            content = match.group(2).strip() if match.group(2) else title
            tags = match.group(3).strip() if match.group(3) else ""
            return create_note(title, content, tags)
        return "❓ Please say: 'create note: <title> content: <content> tags: <tags>'"

    # SEARCH NOTES
    if any(w in msg for w in ["search note", "find note", "search in notes"]):
        match = re.search(r"(?:search note|find note|search in notes)[:\s]+(.+)", message, re.IGNORECASE)
        if match:
            return search_notes(match.group(1).strip())
        return "❓ Please say: 'search notes: <keyword>'"

    # LIST NOTES
    if any(w in msg for w in ["list notes", "show notes", "my notes", "all notes"]):
        tag_match = re.search(r"tag[:\s]+(\w+)", message, re.IGNORECASE)
        return list_notes(tag_match.group(1) if tag_match else "")

    # UPDATE NOTE
    if any(w in msg for w in ["update note", "edit note"]):
        match = re.search(r"(?:update note|edit note)\s+(\d+)[:\s]+(.+)", message, re.IGNORECASE)
        if match:
            return update_note(int(match.group(1)), match.group(2).strip())
        return "❓ Please say: 'update note 3: <new content>'"

    return None
