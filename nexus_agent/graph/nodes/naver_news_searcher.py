from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.types import Command
from langchain_core.messages import HumanMessage

from nexus_agent.graph.nodes.base import Node
from nexus_agent.tools.naver.tool import NaverNewsSearch


class NaverNewsSearcherNode(Node):
    def __init__(self):
        super().__init__()
        self.system_prompt = (
            "You are a news search agent for korean news using naver search api."
            "Only use korean source and data to conduct news search."
            "Do nothing else"
        )
        self.agent = None

    def _run(self, state: dict) -> dict:
        if self.agent is None:
            tools = [NaverNewsSearch(sort="date")]
            llm = state["llm"]
            self.agent = create_react_agent(
                llm,
                tools,
                prompt=self.system_prompt,
            )
        result = self.agent.invoke(state)
        self.logger.info(
            f"   result: \n{result['messages'][-1].content}"
        )
        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content,
                        name="naver_news_searcher",
                    )
                ]
            },
            goto="supervisor",
        )
