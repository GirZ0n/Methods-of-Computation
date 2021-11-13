from typing import Callable

from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


class LeftRectangleMethod(NumericalIntegrator):
    accuracy_degree = 0

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum(f(x_left) * (x_right - x_left) for x_left, x_right in zip(points, points[1:]))


class RightRectangleMethod(NumericalIntegrator):
    accuracy_degree = 0

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum(f(x_right) * (x_right - x_left) for x_left, x_right in zip(points, points[1:]))


class MiddleRectangleMethod(NumericalIntegrator):
    accuracy_degree = 1

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum(f((x_right + x_left) / 2) * (x_right - x_left) for x_left, x_right in zip(points, points[1:]))


class TrapezoidalMethod(NumericalIntegrator):
    accuracy_degree = 1

    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        points = segment.split_into_points(n)
        return sum((f(x_left) + f(x_right)) * (x_right - x_left) / 2 for x_left, x_right in zip(points, points[1:]))
