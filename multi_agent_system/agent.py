from multi_agent_system.llm import ask_llm
from multi_agent_system.mcp_registry import (
    execute_tool,
    get_tools_for_prompt,
    list_available_tools,
    TOOL_SCHEMAS
)
import json
import re
from datetime import datetime

HELP_TEXT = """👋 Welcome! I am your AI productivity assistant.

Just talk to me naturally! Examples:

📋 Tasks:
  "Create a task to buy groceries, high priority"
  "Remind me to call mom tomorrow at 9am"
  "Show all my pending tasks"
  "Mark task 3 as completed"
  "Mark ALL tasks as completed"

📅 Calendar:
  "Schedule a team meeting on April 10 at 2pm"
  "What events do I have this week?"
  "Cancel event 2"

📝 Notes:
  "Save a note: project deadline is April 15"
  "Search my notes for deployment"
  "Show all my notes"

💬 You can also just chat with me normally!"""

conversation_history = {}

def get_system_prompt() -> str:
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    day_name = now.strftime("%A")
    time_now = now.strftime("%H:%M")
    tools_json = get_tools_for_prompt()

    return f"""You are a smart personal productivity assistant with MCP (Model Context Protocol) tool access.
Today is {day_name}, {today} and current time is {time_now}.

You have access to these MCP tools:
{tools_json}

DECISION FLOW:
1. Read the user message
2. Decide which tool(s) to use OR respond conversationally
3. Respond ONLY with valid JSON

For SINGLE tool call:
{{"action": "tool_call", "tool": "create_task", "args": {{"title": "...", "priority": "medium", "due_date": ""}}}}

For MULTIPLE tool calls (e.g. mark ALL tasks):
{{"action": "multi_tool_call", "calls": [
  {{"tool": "update_task", "args": {{"task_id": 1, "status": "completed"}}}},
  {{"tool": "update_task", "args": {{"task_id": 2, "status": "completed"}}}}
]}}

For casual conversation:
{{"action": "chat", "message": "your friendly response here"}}

For help:
{{"action": "help"}}

DATE RULES:
- Today = {today}
- "tomorrow" = add 1 day to today
- "next monday" = calculate actual date
- "5pm" = 17:00, "9am" = 09:00
- priority must ONLY be: low, medium, high

IMPORTANT RULES:
- NEVER put date in priority field
- NEVER ask for clarification — make smart assumptions
- ALWAYS respond with valid JSON only
- Use tool names EXACTLY as listed in the MCP schema above"""

def process_message(message: str, session_id: str = "default") -> str:
    msg = message.strip()
    if not msg:
        return "Please type something!"

    if msg.lower() in ["help", "?"]:
        return HELP_TEXT

    # Build conversation history
    history = conversation_history.get(session_id, [])
    history_text = ""
    if history:
        history_text = "\n\nPrevious conversation:\n"
        for h in history[-6:]:
            history_text += f"{h['role']}: {h['content']}\n"

    # ── LLM DECISION LAYER ──
    llm_response = ask_llm(get_system_prompt() + history_text, msg)
    history.append({"role": "User", "content": msg})

    # ── PARSE LLM RESPONSE ──
    try:
        json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found")
        parsed = json.loads(json_match.group())
        action = parsed.get("action")
    except Exception:
        history.append({"role": "Assistant", "content": llm_response})
        conversation_history[session_id] = history
        return llm_response

    result = ""

    # ── SINGLE TOOL CALL ──
    if action == "tool_call":
        tool_name = parsed.get("tool", "")
        args = parsed.get("args", {})
        print(f"🔧 MCP Tool Call: {tool_name} | Args: {args}")
        result = execute_tool(tool_name, args)

    # ── MULTI TOOL CALL ──
    elif action == "multi_tool_call":
        calls = parsed.get("calls", [])
        results = []
        for call in calls:
            tool_name = call.get("tool", "")
            args = call.get("args", {})
            print(f"🔧 MCP Multi-Tool: {tool_name} | Args: {args}")
            r = execute_tool(tool_name, args)
            results.append(r)
        result = "\n".join(results)

    # ── CHAT ──
    elif action == "chat":
        result = parsed.get("message", "I am here to help!")

    # ── HELP ──
    elif action == "help":
        result = HELP_TEXT

    else:
        result = "❓ I did not understand that. Type `help` to see what I can do."

    history.append({"role": "Assistant", "content": result})
    conversation_history[session_id] = history
    return result
