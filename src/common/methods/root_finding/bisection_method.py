from typing import Optional

from sympy import lambdify

from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder, RootFinderStats


class BisectionMethod(RootFinder):
    stats: Optional[RootFinderStats]

    def __init__(self):
        self.stats = None

    def find(
        self,
        *,
        expression,
        variable: str = 'x',
        line_segment: LineSegment,
        accuracy: float,
        loop_threshold: int = 1000,
    ) -> Optional[float]:
        f = lambdify(variable, expression)

        current_segment = line_segment
        current_step = 0
        while current_segment.length > 2 * accuracy:
            if loop_threshold == current_step:
                return None

            left_value = f(current_segment.left)
            midpoint_value = f(current_segment.midpoint)
            right_value = f(current_segment.right)

            if left_value * midpoint_value <= 0:
                current_segment = LineSegment(current_segment.left, current_segment.midpoint)
            elif midpoint_value * right_value <= 0:
                current_segment = LineSegment(current_segment.midpoint, current_segment.right)
            else:
                return None

            current_step += 1

        approximate_solution = current_segment.midpoint

        self.stats = RootFinderStats(
            line_segment=line_segment,
            initial_approximation=line_segment.midpoint,
            number_of_steps=current_step,
            approximate_solution=approximate_solution,
            error=current_segment.length,
            residual=f(approximate_solution),
        )

        return approximate_solution
