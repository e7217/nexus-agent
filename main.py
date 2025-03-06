from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Self

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv

from app.graph.nodes.websearch import WebSearchNode
from app.models.graph import SimpleState
from app.utils.tools import ToolSet
from app.utils.logger import setup_logger

load_dotenv(override=True)

logger = setup_logger("nexus_agent")

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
        self.logger = logger

    def build(self) -> Self:
        self.logger.info("Building graph...")
        self._builder = StateGraph(SimpleState)
        self._builder.add_node("web_search", WebSearchNode())
        # TODO: WebSearchNode에서 tool을 가져오는게 나을지도 
        # TODO: 리스트 타입 체크
        self._builder.add_node("web_search_tool", ToolNode([ToolSet().web_search]))  

        self._builder.add_edge(START, "web_search")
        self._builder.add_conditional_edges(
            "web_search",
            tools_condition,
            {
                "tools": "web_search_tool",
                "__end__": END,
            },
        )
        self._builder.add_edge("web_search_tool", "web_search")
        self._builder.add_edge("web_search", END)

        self._graph = self._builder.compile()
        self.logger.info("Graph built successfully")
        return self

    def execute(self, state: SimpleState) -> Any:
        self.logger.info(f"Executing graph with state: {state}")
        assert self._graph is not None, "Graph is not built"
        result = self._graph.invoke(state)
        self.logger.info(f"Execution completed with result: {result}")
        return result

    def run(self): ...


if __name__ == "__main__":
    logger.info("Starting Nexus Agent...")
    builder = LanggraphBuilder()
    app = builder.build()
    import datetime as dt
    today = dt.datetime.now().strftime("%Y-%m-%d")
    answer = app.execute(SimpleState(messages=[("user", f"{today} 일자의 삼성전자 관련 경제 뉴스를 알려줘.")]))
    logger.info(f"Final answer: {answer}")
