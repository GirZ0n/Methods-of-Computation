import textwrap
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Union

from src.common.config import OUTPUT_PRECISION
from src.common.model.line_segment import LineSegment


class RootFinderStats:
    line_segment: Optional[LineSegment]
    initial_approximation: Optional[Union[float, List[float]]]
    number_of_steps: Optional[float]
    approximate_solution: Optional[float]
    error: Optional[float]
    residual: Optional[float]

    def __init__(
        self,
        *,
        line_segment: Optional[LineSegment] = None,
        initial_approximation: Optional[Union[float, List[float]]] = None,
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

    def round_initial_approximation(self):
        initials = self.initial_approximation

        if isinstance(self.initial_approximation, float):
            initials = round(self.initial_approximation, OUTPUT_PRECISION)
        elif isinstance(self.initial_approximation, list):
            initials = [round(elem, OUTPUT_PRECISION) for elem in self.initial_approximation]
            initials = ', '.join(map(str, initials))

        return initials

    def __str__(self):
        output = f"""
            Line segment: {self.line_segment}
            Initial approximation: {self.round_initial_approximation()}
            Number of steps: {self.number_of_steps}
            Approximate solution: {round(self.approximate_solution, OUTPUT_PRECISION)}
            Error: {round(self.error, OUTPUT_PRECISION)}
            Residual: {round(self.residual, OUTPUT_PRECISION)}
        """

        return textwrap.dedent(output).strip()


class RootFinder(ABC):
    @abstractmethod
    def find(
        self,
        *,
        derivatives: List[Callable],
        line_segment: LineSegment,
        accuracy: float,
        loop_threshold: int = 1000,
    ) -> Optional[float]:
        raise NotImplementedError
