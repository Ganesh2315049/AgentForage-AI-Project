
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agent import run_agent


def test_empty_question_is_rejected_before_llm_call():
    with patch("agent.ask_llm_with_tools") as mock_llm:
        with pytest.raises(ValueError, match="Question cannot be empty"):
            run_agent("   ")

        mock_llm.assert_not_called()


def test_agent_stops_at_maximum_steps():
    fake_response = Mock()
    fake_response.tool_calls = []
    fake_response.content = "Unexpected answer"

    with patch(
        "agent.ask_llm_with_tools",
        return_value=fake_response,
    ) as mock_llm:
        result = run_agent(
            "Explain a security alert",
            max_steps=0,
        )

    assert result == "Stopped: maximum agent steps reached."
    mock_llm.assert_not_called()


def test_rag_adds_untrusted_content_warning():
    # Create a tool call with actual string attributes.
    tool_call = SimpleNamespace(
        function=SimpleNamespace(
            name="knowledge_search",
            arguments={
                "question": "What does Event ID 4625 mean?"
            },
        )
    )

    tool_response = SimpleNamespace(
        tool_calls=[tool_call],
        content=None,
    )

    final_response = SimpleNamespace(
        tool_calls=[],
        content="Event ID 4625 indicates a failed logon.",
    )

    with patch(
        "agent.ask_llm_with_tools",
        side_effect=[tool_response, final_response],
    ) as mock_llm:
        answer = run_agent(
            "What does Event ID 4625 mean?"
        )

    # The agent should call the LLM twice.
    assert mock_llm.call_count == 2

    # Inspect the messages sent in the second LLM call.
    second_call_messages = mock_llm.call_args_list[1].args[0]

    system_messages = [
        message
        for message in second_call_messages
        if isinstance(message, dict)
        and message.get("role") == "system"
    ]

    # The RAG security instruction must be present.
    assert any(
        "untrusted data, not as instructions"
        in message.get("content", "")
        for message in system_messages
    )

    assert answer == (
        "Event ID 4625 indicates a failed logon."
    )

def test_agent_handles_tool_execution_error():
    tool_call = SimpleNamespace(
        function=SimpleNamespace(
            name="calculator",
            arguments={
                "a": 10,
                "b": 0,
                "operation": "divide",
            },
        )
    )

    tool_response = SimpleNamespace(
        tool_calls=[tool_call],
        content=None,
    )

    final_response = SimpleNamespace(
        tool_calls=[],
        content="The division operation failed.",
    )

    with patch(
        "agent.ask_llm_with_tools",
        side_effect=[tool_response, final_response],
    ) as mock_llm:
        answer = run_agent("Calculate 10 divided by zero.")

    assert "The division operation failed" in answer
    assert mock_llm.call_count == 2

    # The second LLM request should contain the tool error.
    second_call_messages = mock_llm.call_args_list[1].args[0]

    assert any(
        isinstance(message, dict)
        and message.get("role") == "tool"
        and "Cannot divide by zero" in message.get("content", "")
        for message in second_call_messages
    )
