
from tools.calculator import calculator
from tools.knowledge_search import knowledge_search

TOOLS = {
    "calculator": calculator,
    "knowledge_search": knowledge_search,
}


def get_tool(tool_name: str):
    if tool_name not in TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not allowed")

    return TOOLS[tool_name]
