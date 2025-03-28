from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.types import Command
from langchain_core.messages import HumanMessage

from nexus_agent.graph.nodes.base import Node


class NewsSearcherNode(Node):
    def __init__(self):
        super().__init__()
        self.system_prompt = (
            "You are a new search agent. search for US news from BBC Source only."
            "Do nothing else"
        )
        self.agent = None

    def _run(self, state: dict) -> dict:
        if self.agent is None:
            tools = [TavilySearchResults(max_results=2)]
            llm = state["llm"]
            self.agent = create_react_agent(
                llm,
                tools,
                prompt=self.system_prompt,
            )
        result = self.agent.invoke(state)

        self.logger.info(f"NewsSearcherNode result: \n{result['messages'][-1].content}")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content,
                        name=self.__class__.__name__.lower().replace("node", ""),
                    )
                ]
            },
            goto="supervisor",
        )
