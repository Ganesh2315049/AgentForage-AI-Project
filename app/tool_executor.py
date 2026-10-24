
from pydantic import BaseModel, ConfigDict, StrictStr

from schemas import CalculatorInput
from tools.registry import get_tool


class KnowledgeSearchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: StrictStr


def execute_tool(tool_name: str, arguments: dict):
    """Validate and execute an approved tool."""

    tool = get_tool(tool_name)

    if tool_name == "calculator":
        validated = CalculatorInput.model_validate(arguments)
        arguments = validated.model_dump()

    elif tool_name == "knowledge_search":
        validated = KnowledgeSearchInput.model_validate(arguments)
        arguments = validated.model_dump()

    else:
        raise ValueError(f"No argument validator configured for '{tool_name}'")

    return tool(**arguments)
