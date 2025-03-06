from app.graph.nodes.base import Node


class SupervisorNode(Node):
    def __call__(self, state: dict) -> dict: ...
