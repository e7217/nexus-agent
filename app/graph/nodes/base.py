from abc import ABC, abstractmethod
import logging
from functools import wraps


def log_steps(func):
    logger = logging.getLogger("nexus-agent")

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.info(f"Starting {self.__class__.__name__}...")
        result = func(self, *args, **kwargs)
        logger.info(f"{self.__class__.__name__} completed successfully.")
        return result

    return wrapper


# TODO : singletone 로거 적용
# TODO : 노드 실행 시간 측정
# TODO : 에이전트의 기능 구현시 노드 내에서 완료 또는 노드+서비스


class Node(ABC):
    _instance = None
    _logger_name = "nexus-agent"
    logger = logging.getLogger(_logger_name)

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)

    @log_steps
    @abstractmethod
    def _run(self, *args, **kwargs): ...
