
CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform basic arithmetic calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Arithmetic operation"
                }
            },
            "required": ["a", "b", "operation"]
        }
    }
}


KNOWLEDGE_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "knowledge_search",
        "description": (
            "Search local security notes for information about "
            "Windows events and SOC incident response."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Security question to search for"
                }
            },
            "required": ["question"]
        }
    }
}


TOOLS = [CALCULATOR_TOOL, KNOWLEDGE_SEARCH_TOOL]
