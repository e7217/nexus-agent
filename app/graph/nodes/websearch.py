from langchain_openai.chat_models.base import ChatOpenAI

from app.graph.nodes.base import Node
from app.utils.tools import ToolSet


# TODO : 프롬프트 변경사항이 있다면 자체 반영
class WebSearchNode(Node):
    def __init__(self):
        super().__init__()
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        web_search = ToolSet().web_search
        self.llm = llm.bind_tools([web_search])

    def _run(self, state: dict) -> dict:
        self.logger.info(f"hash : {self.__hash__()}")
        self.logger.info(f"Running WebSearchNode with state: {state}")

        state["messages"] = [self.llm.invoke(state["messages"])]
        return state
        # return {"messages": [self.llm.invoke(state["messages"])]}
