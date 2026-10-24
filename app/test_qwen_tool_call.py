
from llm import ask_llm_with_tools
from tool_definitions import TOOLS
from tool_executor import execute_tool

messages = [
    {
        "role": "user",
        "content": "Calculate 15 multiplied by 27. Use the calculator tool."
    }
]

# Ask Qwen to choose a tool
response = ask_llm_with_tools(messages, TOOLS)

print("Qwen requested:", response.tool_calls)

# Execute the tool selected by Qwen
if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        result = execute_tool(tool_name, arguments)

        print("Tool name:", tool_name)
        print("Arguments:", arguments)
        print("Tool result:", result)
else:
    print("No tool was requested.")
