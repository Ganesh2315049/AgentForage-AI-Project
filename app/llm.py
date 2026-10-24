
from ollama import chat

MODEL = "qwen3:8b"


def ask_llm(prompt: str) -> str:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    return response.message.content


def ask_llm_with_tools(messages: list, tools: list):
    """Ask Qwen to answer or request an available tool."""

    response = chat(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    return response.message
