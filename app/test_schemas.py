
from pydantic import ValidationError
from schemas import CalculatorInput

# Test valid input
valid = CalculatorInput(
    a=15,
    b=27,
    operation="multiply"
)

print("Valid input:", valid.model_dump())

# Test invalid input
try:
    CalculatorInput(
        a="hello",
        b=27,
        operation="multiply"
    )
except ValidationError:
    print("Rejected: a must be a number")

# Test invalid operation
try:
    CalculatorInput(
        a=15,
        b=27,
        operation="delete_database"
    )
except ValidationError:
    print("Rejected: operation is not allowed")
