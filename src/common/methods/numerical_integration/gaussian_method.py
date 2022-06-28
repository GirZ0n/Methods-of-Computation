from typing import Callable, List

from src.common.methods.numerical_integration.legendre_polynomial import LegendrePolynomial
from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator


def get_gaussian_roots(n: int, segment: LineSegment) -> List[float]:
    roots = LegendrePolynomial(n).get_roots()
    q = segment.length / 2
    return [segment.left + q * (root + 1) for root in roots]


def get_gaussian_coefficients(n: int, segment: LineSegment) -> List[float]:
    roots = LegendrePolynomial(n).get_roots()
    coefficients = []
    for root in roots:
        coefficients.append(2 * (1 - root ** 2) / (n ** 2 * LegendrePolynomial(n - 1)(root) ** 2))

    q = segment.length / 2

    return [coefficient * q for coefficient in coefficients]


class GaussianMethod(NumericalIntegrator):
    def integrate(self, *, f: Callable, segment: LineSegment, n: int, **kwargs) -> float:
        roots = get_gaussian_roots(n, segment)
        coefficients = get_gaussian_coefficients(n, segment)

        return sum([coefficient * f(root) for coefficient, root in zip(coefficients, roots)])

    @property
    def accuracy_degree(self) -> int:
        raise NotImplementedError
