from typing import TypedDict
from typing import Annotated

from langgraph.graph import add_messages

class SimpleState(TypedDict):
    input: str
    model_name: str
    query: str
    output: str
    messages: Annotated[list, add_messages]
