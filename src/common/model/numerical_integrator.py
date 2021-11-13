from abc import ABC, abstractmethod
from typing import Callable

from src.common.model.line_segment import LineSegment


class NumericalIntegrator(ABC):
    @property
    @abstractmethod
    def accuracy_degree(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def integrate(self, *, f: Callable, segments: LineSegment, n: int, **kwargs) -> float:
        raise NotImplementedError
