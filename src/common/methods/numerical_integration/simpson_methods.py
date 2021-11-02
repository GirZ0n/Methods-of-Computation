from typing import Callable

from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


class FirstSimpsonMethod(NumericalIntegrator):
    def integrate(self, *, f: Callable, segment: LineSegment, n: int) -> float:
        points = segment.split_into_points(n)
        return sum(
            (x_right - x_left) * (f(x_left) + 4 * f((x_left + x_right) / 2) + f(x_right)) / 6
            for x_left, x_right in zip(points, points[1:])
        )


class SecondSimpsonMethod(NumericalIntegrator):
    def integrate(self, *, f: Callable, segment: LineSegment, n: int) -> float:
        points = segment.split_into_points(n)
        return sum(
            (x_right - x_left)
            * (f(x_left) + 3 * f((2 * x_left + x_right) / 3) + 3 * f((x_left + 2 * x_right) / 3) + f(x_right))
            / 8
            for x_left, x_right in zip(points, points[1:])
        )
