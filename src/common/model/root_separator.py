from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Callable, List, Union

from src.common.model.line_segment import LineSegment


class RootSeparator(ABC):
    @abstractmethod
    def separate(
        self,
        function: Callable[[Union[Decimal, float]], Union[Decimal, float]],
        line_segment: LineSegment,
    ) -> List[LineSegment]:
        raise NotImplementedError
