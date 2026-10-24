
from registry import get_tool

# Test an approved tool
tool = get_tool("calculator")
print("Allowed tool:", tool.__name__)

# Test a tool that is not registered
try:
    get_tool("delete_database")
except ValueError as error:
    print("Blocked:", error)
