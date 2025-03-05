from abc import ABC, abstractmethod

from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv

from app.graph.nodes.llm import LLMNode

load_dotenv()

class BuilderABC(ABC):
    
    @abstractmethod
    def build(self) -> self.__class__:
        ...
        
    @abstractmethod
    def execute(self):
        ...
    
    @abstractmethod
    def run(self):
        ...

class Builder(BuilderABC):
    def __init__(self):
        self._builder = None
        self._graph = None
        
    def build(self) -> self.__class__:
        
        self._builder = StateGraph(State)
        self._builder.add_node("llm", LLMNode())
        
        self._builder.add_edge(START, "llm")
        self._builder.add_edge("llm", END)
        self._graph = self._builder.compile()
        return self

    def execute(self, state: SimpleState):
        assert self._graph is not None, "Graph is not built"
        return self._graph.invoke(state)
    
    def run(self):
        ...
        

if __name__ == "__main__":
    builder = Builder()
    app = builder.build()
    answer = app.execute(SimpleState(model_name="gpt-4o-mini", query="Hello, world!"))
    print(answer)