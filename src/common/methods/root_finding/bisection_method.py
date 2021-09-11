from typing import Optional

from sympy import lambdify

from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder, RootFinderStats


class BisectionMethod(RootFinder):
    stats: Optional[RootFinderStats]

    def __init__(self):
        self.stats = None

    def find(self, *, expression, variable: str = 'x', line_segment: LineSegment, accuracy: float) -> Optional[float]:
        self.stats = RootFinderStats()

        f = lambdify(variable, expression)

        current_segment = line_segment
        current_step = 0
        current_x = current_segment.midpoint
        while current_segment.length > 2 * accuracy:
            current_x = current_segment.midpoint

            left_value = f(current_segment.left)
            midpoint_value = f(current_x)
            right_value = f(current_segment.right)

            if left_value * midpoint_value <= 0:
                current_segment = LineSegment(current_segment.left, current_x)
            elif midpoint_value * right_value <= 0:
                current_segment = LineSegment(current_x, current_segment.right)
            else:
                return None

            current_step += 1

        approximate_solution = current_segment.midpoint

        self.stats.line_segment = line_segment
        self.stats.initial_approximation = line_segment.midpoint
        self.stats.number_of_steps = current_step
        self.stats.approximate_solution = approximate_solution
        self.stats.error = abs(approximate_solution - current_x)
        self.stats.residual = f(approximate_solution)

        return current_segment.midpoint
