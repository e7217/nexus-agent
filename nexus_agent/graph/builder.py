from langgraph.graph.state import CompiledStateGraph
from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Self

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from nexus_agent.graph.nodes.naver_news_searcher import NaverNewsSearcherNode
from nexus_agent.graph.nodes.websearch import WebSearchNode
from nexus_agent.graph.nodes import (
    SupervisorNode,
    NewsSearcherNode,
    CommunitySearcherNode,
    ReportAssistantNode,
)
from nexus_agent.models.graph import SimpleState, SupervisorState
from nexus_agent.utils.tools import ToolSet
from nexus_agent.utils.logger import setup_logger

logger = setup_logger("nexus_agent")


class GraphBuilder:
    def __init__(cls): ...

    def _build(cls) -> CompiledStateGraph: ...

    def build_from_dict(cls, graph_dict: dict) -> CompiledStateGraph: ...

    def build_from_json(cls, json_path: str) -> CompiledStateGraph: ...

    def build_from_yaml(cls, yaml_path: str) -> CompiledStateGraph: ...


class BuilderABC(ABC):
    @abstractmethod
    def build(self) -> Self: ...

    @abstractmethod
    def execute(self, state: SimpleState) -> Any: ...

    @abstractmethod
    def run(self): ...


# TODO: 동적 빌더로 변경
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


# TODO: 동적 빌더로 변경
class SupervisorGraphBuilder(BuilderABC):
    def __init__(self):
        self._builder = None
        self._graph = None
        self.logger = logger
        # TODO: OPENAI 라이브러리 처리

    def build(self) -> Self:
        self.logger.info("Building graph...")
        self._builder = StateGraph(SupervisorState)
        self._builder.add_node("supervisor", SupervisorNode())
        # self._builder.add_node("news_searcher", NewsSearcherNode())
        # self._builder.add_node("community_searcher", CommunitySearcherNode())
        self._builder.add_node("naver_news_searcher", NaverNewsSearcherNode())
        self._builder.add_node("report_assistant", ReportAssistantNode())

        self.members = [
            # "news_searcher",
            # "community_searcher",
            "report_assistant",
            "naver_news_searcher"
        ]

        self._builder.add_edge(START, "supervisor")

        self._graph = self._builder.compile()

        self.logger.info("Graph built successfully")
        return self

    def execute(self, state: SupervisorState) -> Any:
        state["members"] = self.members

        self.logger.info(f"Executing graph with state: {state}")
        assert self._graph is not None, "Graph is not built"
        result = self._graph.invoke(state)
        self.logger.info(f"Execution completed with result: {result}")
        return result

    def run(self): ...
