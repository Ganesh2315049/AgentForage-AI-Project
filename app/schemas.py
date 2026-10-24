
from typing import Literal
from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt


class CalculatorInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    a: StrictFloat | StrictInt
    b: StrictFloat | StrictInt
    operation: Literal["add", "subtract", "multiply", "divide"]
