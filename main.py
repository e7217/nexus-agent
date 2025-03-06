from abc import ABC, abstractmethod
from typing import Any, Self

from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv

from app.graph.nodes.llm import LLMNode
from app.models.graph import SimpleState


load_dotenv()


class BuilderABC(ABC):
    @abstractmethod
    def build(self) -> Self: ...

    @abstractmethod
    def execute(self, state: SimpleState) -> Any: ...

    @abstractmethod
    def run(self): ...


class LanggraphBuilder(BuilderABC):
    def __init__(self):
        self._builder = None
        self._graph = None

    def build(self) -> Self:
        self._builder = StateGraph(SimpleState)
        self._builder.add_node("llm", LLMNode())

        self._builder.add_edge(START, "llm")
        self._builder.add_edge("llm", END)
        self._graph = self._builder.compile()
        return self

    def execute(self, state: SimpleState) -> Any:
        assert self._graph is not None, "Graph is not built"
        return self._graph.invoke(state)

    def run(self): ...


if __name__ == "__main__":
    builder = LanggraphBuilder()
    app = builder.build()
    answer = app.execute(SimpleState(model_name="gpt-4o-mini", query="Hello, world!"))
    print(answer)
