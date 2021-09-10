from abc import ABC, abstractmethod
from typing import List

from src.common.model.line_segment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(self, *, function, variable: str = 'x', line_segment: LineSegment) -> List[LineSegment]:
        raise NotImplementedError
