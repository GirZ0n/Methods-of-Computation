from typing import Callable, List, Optional

from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder, RootFinderStats


class SecantMethod(RootFinder):
    stats: Optional[RootFinderStats]

    def __init__(self):
        self.stats = None

    def find(
        self,
        *,
        derivatives: List[Callable[[float], float]],
        line_segment: LineSegment,
        accuracy: float,
        loop_threshold: int = 1000,
    ) -> Optional[float]:
        self.stats = None

        f = derivatives[0]

        previous_x = line_segment.left
        current_x = line_segment.right
        next_x = current_x - (f(current_x) / (f(current_x) - f(previous_x))) * (current_x - previous_x)

        current_step = 1
        while abs(next_x - current_x) > accuracy:
            if loop_threshold == current_step:
                return None

            previous_x = current_x
            current_x = next_x
            next_x = current_x - (f(current_x) / (f(current_x) - f(previous_x))) * (current_x - previous_x)

            current_step += 1

        approximate_solution = next_x

        self.stats = RootFinderStats(
            line_segment=line_segment,
            initial_approximation=[line_segment.left, line_segment.right],
            number_of_steps=current_step,
            approximate_solution=approximate_solution,
            error=abs(approximate_solution - current_x),
            residual=abs(f(approximate_solution)),
        )

        return approximate_solution
