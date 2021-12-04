from math import cos, pi
from typing import Callable, List

from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


def get_mohler_roots(n: int) -> List[float]:
    return [cos((2 * k - 1) / (2 * n) * pi) for k in range(1, n + 1)]


def get_mohler_coefficients(n: int) -> List[float]:
    return [pi / n] * n


class MohlerMethod(NumericalIntegrator):
    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        roots = get_mohler_roots(n)
        coefficients = get_mohler_coefficients(n)
        return sum([coefficient * f(root) for coefficient, root in zip(coefficients, roots)])

    @property
    def accuracy_degree(self) -> int:
        raise NotImplementedError
