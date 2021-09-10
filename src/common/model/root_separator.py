from abc import ABC, abstractmethod
from typing import Callable, List

from src.common.model.aliases import Value
from src.common.model.line_segment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(self, function: Callable[[Value], Value], line_segment: LineSegment) -> List[LineSegment]:
        raise NotImplementedError
