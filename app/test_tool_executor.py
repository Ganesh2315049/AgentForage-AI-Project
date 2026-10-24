
from pydantic import ValidationError

from tool_executor import execute_tool


# Test 1: Valid tool request
result = execute_tool(
    "calculator",
    {"a": 15, "b": 27, "operation": "multiply"}
)
print("Valid result:", result)


# Test 2: Invalid arguments
try:
    execute_tool(
        "calculator",
        {"a": "hello", "b": 27, "operation": "multiply"}
    )
except ValidationError:
    print("Invalid arguments rejected")


# Test 3: Unregistered tool
try:
    execute_tool("delete_database", {})
except ValueError as error:
    print("Unregistered tool rejected:", error)
