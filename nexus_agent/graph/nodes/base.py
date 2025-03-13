from abc import ABC, abstractmethod
from functools import wraps
import time
from rich.console import Console

from nexus_agent.utils.logger import setup_logger


console = Console()


def log_steps(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        console.print("\n" + "=" * (console.width))
        logger = setup_logger(f"nexus_agent.nodes.{self.__class__.__name__.lower()}")
        logger.info(f"Starting {self.__class__.__name__}...")

        start_time = time.time()

        # 함수 실행
        result = func(self, *args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time

        logger.info(
            f"{self.__class__.__name__} completed successfully. "
            f"(실행 시간: {execution_time:.4f}초)"
        )
        console.print("=" * (console.width) + "\n")

        return result

    return wrapper


# TODO : singletone 로거 적용
# TODO : 에이전트의 기능 구현시 노드 내에서 완료 또는 노드+서비스


class Node(ABC):
    def __init__(self):
        self._instance = None
        self._logger_name = f"nexus_agent.nodes.{self.__class__.__name__.lower()}"
        self.logger = setup_logger(self._logger_name)
        self.DEFAULT_LLM_MODEL = "gpt-4o-mini"

    @log_steps
    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)

    @abstractmethod
    def _run(self, *args, **kwargs): ...

    @abstractmethod
    def _invoke(self, query: str): ...

    def invoke(self, query: str):
        return self._invoke(query)
