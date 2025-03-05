from app.graph.nodes.base import Node

class GeneratorNode(Node):
    def __init__(self):
        super().__init__()
        
    def __call__(self, state: dict) -> dict:
        ...
