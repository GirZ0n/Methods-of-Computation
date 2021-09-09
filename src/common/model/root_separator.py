from abc import ABC, abstractmethod
from typing import List

from src.common.model.LineSegment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(self, line_segment: LineSegment, function, variable: str = 'x') -> List[LineSegment]:
        raise NotImplementedError
