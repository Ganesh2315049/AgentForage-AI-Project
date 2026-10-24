
MAX_INPUT_LENGTH = 1000


def validate_user_input(user_input: str) -> str:
    """Reject empty or excessively long user input."""

    if not isinstance(user_input, str):
        raise ValueError("Input must be text.")

    user_input = user_input.strip()

    if not user_input:
        raise ValueError("Question cannot be empty.")

    if len(user_input) > MAX_INPUT_LENGTH:
        raise ValueError("Question is too long. Maximum: 1000 characters.")

    return user_input
