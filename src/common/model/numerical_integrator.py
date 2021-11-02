from abc import ABC, abstractmethod
from typing import Callable

from src.common.model.line_segment import LineSegment


class NumericalIntegrator(ABC):
    @abstractmethod
    def integrate(self, *, f: Callable, segments: LineSegment, n: int) -> float:
        raise NotImplementedError
