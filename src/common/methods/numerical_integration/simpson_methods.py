from typing import Callable

from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


class FirstSimpsonMethod(NumericalIntegrator):
    accuracy_degree = 3

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum(
            (x_right - x_left) * (f(x_left) + 4 * f((x_left + x_right) / 2) + f(x_right)) / 6
            for x_left, x_right in zip(points, points[1:])
        )


class SecondSimpsonMethod(NumericalIntegrator):
    accuracy_degree = 3

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum(
            (x_right - x_left)
            * (f(x_left) + 3 * f((2 * x_left + x_right) / 3) + 3 * f((x_left + 2 * x_right) / 3) + f(x_right))
            / 8
            for x_left, x_right in zip(points, points[1:])
        )


# ----------------------------------------------------------------------------------------------------------------------


class OptimizedSimpsonMethod(NumericalIntegrator):
    accuracy_degree = 3

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        inner_sum = kwargs.pop('inner_sum')
        middle_sum = kwargs.pop('middle_sum')
        boundary_sum = kwargs.pop('boundary_sum')
        h = segment.length / n

        return h / 6 * (boundary_sum + 2 * inner_sum + 4 * middle_sum)
