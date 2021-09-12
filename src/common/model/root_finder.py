import textwrap
from abc import ABC, abstractmethod
from typing import Optional

from src.common.model.line_segment import LineSegment


class RootFinderStats:
    line_segment: Optional[LineSegment]
    initial_approximation: Optional[float]
    number_of_steps: Optional[float]
    approximate_solution: Optional[float]
    error: Optional[float]
    residual: Optional[float]

    def __init__(
        self,
        *,
        line_segment: Optional[LineSegment] = None,
        initial_approximation: Optional[float] = None,
        number_of_steps: Optional[float] = None,
        approximate_solution: Optional[float] = None,
        error: Optional[float] = None,
        residual: Optional[float] = None,
    ):
        self.line_segment = line_segment
        self.initial_approximation = initial_approximation
        self.number_of_steps = number_of_steps
        self.approximate_solution = approximate_solution
        self.error = error
        self.residual = residual

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
    def find(
        self,
        *,
        expression,
        variable: str = 'x',
        line_segment: LineSegment,
        accuracy: float,
        loop_threshold: int = 1000,
    ) -> Optional[float]:
        raise NotImplementedError
