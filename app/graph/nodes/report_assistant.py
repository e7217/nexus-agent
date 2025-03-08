from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_core.messages import HumanMessage

from app.graph.nodes.base import Node


class ReportAssistantNode(Node):
    def __init__(self):
        super().__init__()
        self.agent = None

    def _run(self, state: dict) -> dict:
        if self.agent is None:
            tools = [WriteFileTool()]
            llm = state["llm"]
            self.agent = create_react_agent(
                llm,
                tools,
            )
        result = self.agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content, name="report_assistant"
                    )
                ]
            },
            goto="supervisor",
        )
