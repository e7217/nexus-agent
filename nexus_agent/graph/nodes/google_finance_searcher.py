from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from langchain_core.messages import HumanMessage

from nexus_agent.graph.nodes.base import Node
from nexus_agent.models.graph import RawResponse
from langchain_community.tools.google_finance.tool import GoogleFinanceQueryRun


class GoogleFinanceSearcherNode(Node):
    def __init__(self):
        super().__init__()
        self.system_prompt = (
            "You are a finance search agent for US finance using google finance search api."
            "Only use US source and data to conduct finance search."
            "Do nothing else"
        )
        self.agent = None
        self.tools = [GoogleFinanceQueryRun()]

    def _run(self, state: dict) -> dict:
        if self.agent is None:
            assert state["llm"] is not None, "The State model should include llm"
            llm = state["llm"]
            self.agent = create_react_agent(
                llm,
                self.tools,
                prompt=self.system_prompt,
            )
        result = self.agent.invoke(state)
        self.logger.info(f"   result: \n{result['messages'][-1].content}")
        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content,
                        name="googlefinancesearcher",
                    )
                ]
            },
            goto="supervisor",
        )

    def _invoke(self, query: str) -> RawResponse:
        agent = self.agent or create_react_agent(
            ChatOpenAI(model=self.DEFAULT_LLM_MODEL),
            self.tools,
            prompt=self.system_prompt,
        )
        result = agent.invoke({"messages": [("human", query)]})
        return RawResponse(answer=result["messages"][-1].content)
