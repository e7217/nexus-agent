from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Self

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv

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
        self._builder.add_node("news_searcher", NewsSearcherNode())
        self._builder.add_node("community_searcher", CommunitySearcherNode())
        self._builder.add_node("report_assistant", ReportAssistantNode())

        self.members = [
            "news_searcher",
            "community_searcher",
            "report_assistant",
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

if __name__ == "__main__":
    logger.info("Starting Nexus Agent...")
    builder = SupervisorGraphBuilder()
    app = builder.build()
    import datetime as dt

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    today = dt.datetime.now().strftime("%Y-%m-%d")
    # answer = app.execute(SimpleState(messages=[("user", f"{today} 일자의 삼성전자 관련 경제 뉴스를 알려줘.")]))
    answer = app.execute(SupervisorState(llm = llm, messages=[("user", f"{today} 일자의 삼정전자와 관련된 주요 뉴스는 무엇이 있을까? 방송사 CNN의 뉴스 페이지를 참고해서 알려줘")]))
    # answer = app.execute(SupervisorState(messages=[("user", f"3 더하기 2는?")]))
    

    # answer = app.execute(
    #     SupervisorState(
    #         llm=llm,
    #         messages=[
    #             (
    #                 "user",
    #                 "네이버의 주식 토론 방에서 삼성전자에 대한 긍정적인 의견을 찾아주고, report.txt 파일을 생성하여 참조 링크 목록을 저장해줘",
    #             )
    #         ]
    #     )
    # )
    logger.info(f"Final answer: {answer}")
