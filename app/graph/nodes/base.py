from abc import ABC, abstractmethod
import logging
from functools import wraps


def log_steps(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.logger.info(f"Starting {self.__class__.__name__}...")
        result = func(self, *args, **kwargs)
        self.logger.info(f"{self.__class__.__name__} completed successfully.")
        return result

    return wrapper


# TODO : singletone 로거 적용


class Node(ABC):
    _instance = None
    _logger_name = "nexus-agent"
    logger = logging.getLogger(_logger_name)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Node, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

    @log_steps
    @abstractmethod
    def run(self, *args, **kwargs): ...
