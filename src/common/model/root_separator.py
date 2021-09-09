from abc import ABC, abstractmethod
from typing import List

from src.common.model.line_segment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(self, line_segment: LineSegment, function, variable: str = 'x') -> List[LineSegment]:
        raise NotImplementedError
