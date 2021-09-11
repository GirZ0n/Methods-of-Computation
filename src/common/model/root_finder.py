import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from src.common.model.line_segment import LineSegment


@dataclass
class RootFinderStats:
    line_segment: Optional[LineSegment] = None
    initial_approximation: Optional[float] = None
    number_of_steps: Optional[float] = None
    approximate_solution: Optional[float] = None
    error: Optional[float] = None
    residual: Optional[float] = None

    def clear(self):
        self.line_segment = None
        self.initial_approximation = None
        self.number_of_steps = None
        self.approximate_solution = None
        self.error = None
        self.residual = None

    def __str__(self):
        output = f"""
            Line segment: {self.line_segment}            
            Initial approximation: {self.initial_approximation:.10f}
            Number of steps: {self.number_of_steps}
            Approximate solution: {self.approximate_solution:.10f}
            Error: {self.error:.10f}
            Residual: {self.residual:.10f}
        """

        return textwrap.dedent(output).strip()


class RootFinder(ABC):
    @abstractmethod
    def find(self, *, expression, variable: str = 'x', line_segment: LineSegment, accuracy: float) -> Optional[float]:
        raise NotImplementedError
