from typing import TypedDict


class SimpleState(TypedDict):
    input: str
    model_name: str
    query: str
    output: str
