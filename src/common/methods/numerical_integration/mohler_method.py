from math import cos, pi
from typing import Callable, List

from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


def get_mohler_roots(n: int, segment: LineSegment) -> List[float]:
    roots = [cos((2 * k - 1) / (2 * n) * pi) for k in range(1, n + 1)]
    q = segment.length / 2
    return list(map(lambda root: segment.left + q * (root + 1), roots))


def get_mohler_coefficients(n: int, segment: LineSegment) -> List[float]:
    coefficients = [pi / n] * n
    q = segment.length / 2
    return list(map(lambda coefficient: coefficient * q, coefficients))


class MohlerMethod(NumericalIntegrator):
    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        roots = get_mohler_roots(n, segment)
        coefficients = get_mohler_coefficients(n, segment)

        return sum([coefficient * f(root) for coefficient, root in zip(coefficients, roots)])

    @property
    def accuracy_degree(self) -> int:
        raise NotImplementedError
