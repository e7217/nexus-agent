from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Self

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from nexus_agent.graph.nodes.base import Node
from nexus_agent.graph.nodes.websearch import WebSearchNode
from nexus_agent.graph.nodes import (
    SupervisorNode,
)
from nexus_agent.models.graph import SimpleState, SupervisorState
from nexus_agent.utils.tools import ToolSet
from nexus_agent.utils.logger import setup_logger

logger = setup_logger("nexus_agent")


class BuilderABC(ABC):
    def __init__(self):
        self.logger = setup_logger("nexus_agent")

    @abstractmethod
    def build(self) -> Self: ...

    @abstractmethod
    def execute(self, state: SimpleState) -> Any: ...

    @abstractmethod
    def run(self): ...


# TODO: 동적 빌더로 변경
class LanggraphBuilder(BuilderABC):
    def __init__(self):
        super().__init__()
        self._builder = None
        self._graph = None

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
        super().__init__()
        self._builder = None
        self._graph = None
        self._node_list = []
        # TODO: OPENAI 라이브러리 처리

    def build(self) -> Self:
        self.logger.info("Building graph...")
        self._builder = StateGraph(SupervisorState)

        self._builder.add_node("supervisor", SupervisorNode())
        for node in self._node_list:
            self._builder.add_node(node.__class__.__name__, node)
        self.members = list(map(lambda x: x.__class__.__name__, self._node_list))

        # # self._builder.add_node("news_searcher", NewsSearcherNode())
        # # self._builder.add_node("community_searcher", CommunitySearcherNode())
        # self._builder.add_node("naver_news_searcher", NaverNewsSearcherNode())
        # self._builder.add_node("report_assistant", ReportAssistantNode())

        # self.members = [
        #     # "news_searcher",
        #     # "community_searcher",
        #     "report_assistant",
        #     "naver_news_searcher",
        # ]

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

    def add_node(self, node: Node):
        self._node_list.append(node)

    def remove_node(self, node: Node):
        self._node_list.remove(node)

    def get_nodes(self) -> list[Node]:
        return self._node_list

    def get_members(self) -> list[str]:
        return self.members


# TODO: 주석 삭제
# class SupervisorGraphBuilder(BuilderABC):
#     def __init__(self):
#         self._builder = None
#         self._graph = None
#         self.logger = logger

#     def build(self) -> Self:
#         self.logger.info("Building graph...")
#         self._builder = StateGraph(SupervisorState)
#         self._builder.add_node("supervisor", SupervisorNode())
#         # self._builder.add_node("news_searcher", NewsSearcherNode())
#         # self._builder.add_node("community_searcher", CommunitySearcherNode())
#         self._builder.add_node("naver_news_searcher", NaverNewsSearcherNode())
#         self._builder.add_node("report_assistant", ReportAssistantNode())

#         self.members = [
#             # "news_searcher",
#             # "community_searcher",
#             "report_assistant",
#             "naver_news_searcher",
#         ]

#         self._builder.add_edge(START, "supervisor")

#         self._graph = self._builder.compile()

#         self.logger.info("Graph built successfully")
#         return self

#     def execute(self, state: SupervisorState) -> Any:
#         state["members"] = self.members

#         self.logger.info(f"Executing graph with state: {state}")
#         assert self._graph is not None, "Graph is not built"
#         result = self._graph.invoke(state)
#         self.logger.info(f"Execution completed with result: {result}")
#         return result

#     def run(self): ...
