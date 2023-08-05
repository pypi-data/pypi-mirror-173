from abc import ABC, abstractmethod
from typing import AsyncIterable, Awaitable, Callable, Dict, Tuple
from uuid import UUID

from kilroy_server_py_utils import Categorizable, classproperty, normalize


class PostScheduler(Categorizable, ABC):
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("PostScheduler"))

    @abstractmethod
    def wait(self) -> AsyncIterable[None]:
        pass
