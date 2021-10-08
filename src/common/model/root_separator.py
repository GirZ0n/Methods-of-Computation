from abc import ABC, abstractmethod
from typing import Callable, List

from src.common.model.line_segment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(self, *, f: Callable, line_segment: LineSegment) -> List[LineSegment]:
        raise NotImplementedError
