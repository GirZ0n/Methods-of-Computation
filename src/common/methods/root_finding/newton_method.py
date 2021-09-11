from typing import Optional

from sympy import diff, lambdify

from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder, RootFinderStats


class NewtonMethod(RootFinder):
    stats: Optional[RootFinderStats]

    def __init__(self):
        self.stats = None

    def find(self, *, expression, variable: str = 'x', line_segment: LineSegment, accuracy: float) -> Optional[float]:
        diff_expression = diff(expression)
        f = lambdify(variable, expression)
        df = lambdify(variable, diff_expression)

        previous_x = line_segment.left
        current_x = previous_x - f(previous_x) / df(previous_x)

        current_step = 1
        while abs(current_x - previous_x) > accuracy:
            previous_x = current_x
            current_x = previous_x - f(previous_x) / df(previous_x)

            current_step += 1

        approximate_solution = current_x

        self.stats = RootFinderStats(
            line_segment=line_segment,
            initial_approximation=line_segment.left,
            number_of_steps=current_step,
            approximate_solution=approximate_solution,
            error=abs(approximate_solution - previous_x),
            residual=f(approximate_solution),
        )

        return approximate_solution


class ModifiedNewtonMethod(RootFinder):
    stats: Optional[RootFinderStats]

    def __init__(self):
        self.stats = None

    def find(self, *, expression, variable: str = 'x', line_segment: LineSegment, accuracy: float) -> Optional[float]:
        diff_expression = diff(expression)
        f = lambdify(variable, expression)
        df = lambdify(variable, diff_expression)

        previous_x = line_segment.left
        current_x = previous_x - f(previous_x) / df(line_segment.left)

        current_step = 1
        while abs(current_x - previous_x) > accuracy:
            previous_x = current_x
            current_x = previous_x - f(previous_x) / df(line_segment.left)

            current_step += 1

        approximate_solution = current_x

        self.stats = RootFinderStats(
            line_segment=line_segment,
            initial_approximation=line_segment.left,
            number_of_steps=current_step,
            approximate_solution=approximate_solution,
            error=abs(approximate_solution - previous_x),
            residual=f(approximate_solution),
        )

        return approximate_solution
