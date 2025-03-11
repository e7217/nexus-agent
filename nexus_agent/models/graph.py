from typing import TypedDict, Annotated, Any

from langgraph.graph import add_messages, MessagesState


class SimpleState(TypedDict):
    input: str
    model_name: str
    query: str
    output: str
    messages: Annotated[list, add_messages]


class SupervisorState(MessagesState):
    llm: Any
    members: list[str]
