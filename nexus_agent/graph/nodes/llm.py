from nexus_agent.graph.nodes.base import Node
from langchain_openai import ChatOpenAI

# TODO : 모델을 환경변수로 받을 지, 체인에서 받을 지 생각해보기


class LLMNode(Node):
    def __init__(self):
        self.model_name = "gpt-4o-mini"
        self.temperature = 0.0
        self.llm = None

    def __call__(self, state: dict) -> dict:
        if not state.get("model_name", None):
            self.logger.warning(
                "model_name is not set, using default model_name: %s", self.model_name
            )
            state["model_name"] = self.model_name
        else:
            self.model_name = (
                state["model_name"]
                if state["model_name"] in ["gpt-4o-mini", "gpt-4o", "o1-mini", "o1"]
                else self.model_name
            )

        self.logger.info("model_name: %s", self.model_name)

        _opt = {
            "model": self.model_name,
            "temperature": self.temperature,
        }

        if not self.llm:
            self.llm = ChatOpenAI(**_opt)

        self.llm.bind(**_opt)
        state["llm"] = self.llm

        return state
