
import pytest

from tool_executor import execute_tool


def test_approved_calculator_tool_works():
    result = execute_tool(
        "calculator",
        {"a": 15, "b": 27, "operation": "multiply"}
    )
    assert result == 405


def test_unapproved_tool_is_rejected():
    with pytest.raises(ValueError, match="not allowed"):
        execute_tool("delete_database", {})


def test_extra_arguments_are_rejected():
    with pytest.raises(ValueError):
        execute_tool(
            "calculator",
            {
                "a": 15,
                "b": 27,
                "operation": "multiply",
                "admin": True
            }
        )


def test_invalid_operation_is_rejected():
    with pytest.raises(ValueError):
        execute_tool(
            "calculator",
            {"a": 15, "b": 27, "operation": "delete"}
        )


def test_division_by_zero_is_rejected():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        execute_tool(
            "calculator",
            {"a": 10, "b": 0, "operation": "divide"}
        )
