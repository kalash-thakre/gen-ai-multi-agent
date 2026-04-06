import inspect
import json
from typing import Callable, Any
from multi_agent_system.tools.task_tools import (
    _create_task, _list_tasks, _update_task, _delete_task
)
from multi_agent_system.tools.calendar_tools import (
    _create_event, _list_events, _delete_event
)
from multi_agent_system.tools.notes_tools import (
    _create_note, _list_notes, _search_notes, _update_note
)

# ─────────────────────────────────────────
# 1. TOOL REGISTRY — Central catalog
# ─────────────────────────────────────────
TOOL_REGISTRY: dict[str, Callable] = {
    "create_task":    _create_task,
    "list_tasks":     _list_tasks,
    "update_task":    _update_task,
    "delete_task":    _delete_task,
    "create_event":   _create_event,
    "list_events":    _list_events,
    "delete_event":   _delete_event,
    "create_note":    _create_note,
    "list_notes":     _list_notes,
    "search_notes":   _search_notes,
    "update_note":    _update_note,
}

# ─────────────────────────────────────────
# 2. SCHEMA GENERATOR — JSON schema per tool
# ─────────────────────────────────────────
PYTHON_TO_JSON_TYPE = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "NoneType": "null",
}

def generate_schema(fn: Callable) -> dict:
    """Convert a Python function into MCP-compliant JSON schema."""
    sig = inspect.signature(fn)
    doc = inspect.getdoc(fn) or ""

    # Parse description from docstring
    lines = doc.split("\n")
    description = lines[0].strip() if lines else fn.__name__

    # Parse args from docstring
    arg_descriptions = {}
    in_args = False
    for line in lines:
        line = line.strip()
        if line.lower() == "args:":
            in_args = True
            continue
        if line.lower() in ("returns:", "raises:"):
            in_args = False
            continue
        if in_args and ":" in line:
            arg_name, arg_desc = line.split(":", 1)
            arg_descriptions[arg_name.strip()] = arg_desc.strip()

    # Build parameters schema
    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        annotation = param.annotation
        type_name = annotation.__name__ if hasattr(annotation, "__name__") else "string"
        json_type = PYTHON_TO_JSON_TYPE.get(type_name, "string")

        properties[param_name] = {
            "type": json_type,
            "description": arg_descriptions.get(param_name, param_name)
        }

        # If no default → required
        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    return {
        "name": fn.__name__.lstrip("_"),
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }

# Generate schemas for ALL tools
TOOL_SCHEMAS: list[dict] = [
    generate_schema(fn) for fn in TOOL_REGISTRY.values()
]

# ─────────────────────────────────────────
# 3. EXECUTION WRAPPER — MCP runtime
# ─────────────────────────────────────────
def execute_tool(name: str, args: dict) -> str:
    """MCP execution layer — routes tool name + args to correct function."""
    # Normalize name (remove leading underscore if present)
    clean_name = name.lstrip("_")

    if clean_name not in TOOL_REGISTRY:
        available = ", ".join(TOOL_REGISTRY.keys())
        return f"❌ Unknown tool: '{clean_name}'. Available: {available}"

    fn = TOOL_REGISTRY[clean_name]
    sig = inspect.signature(fn)

    # Type cast args based on signature
    casted_args = {}
    for param_name, param in sig.parameters.items():
        if param_name in args:
            val = args[param_name]
            annotation = param.annotation
            try:
                if annotation == int:
                    val = int(val)
                elif annotation == float:
                    val = float(val)
                elif annotation == bool:
                    val = bool(val)
                else:
                    val = str(val)
            except (ValueError, TypeError):
                pass
            casted_args[param_name] = val

    try:
        result = fn(**casted_args)
        return result
    except TypeError as e:
        return f"❌ Tool execution error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error in '{clean_name}': {str(e)}"

def get_tools_for_prompt() -> str:
    """Returns tool schemas as formatted string for LLM system prompt."""
    return json.dumps(TOOL_SCHEMAS, indent=2)

def list_available_tools() -> list[str]:
    """Returns list of all registered tool names."""
    return list(TOOL_REGISTRY.keys())
