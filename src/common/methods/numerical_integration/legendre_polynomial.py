from functools import cached_property, lru_cache
from typing import Callable, List

from src.common.methods.root_finding.secant_method import SecantMethod
from src.common.methods.root_separation.segment_tabulation import Tabulator
from src.common.model.line_segment import LineSegment


@lru_cache
def _get_legendre_polynomial_recursively(n: int):
    if n == 0:
        return lambda x: 1
    elif n == 1:
        return lambda x: x

    return (
        lambda x: (
            (2 * n - 1) * _get_legendre_polynomial_recursively(n - 1)(x) * x
            - (n - 1) * _get_legendre_polynomial_recursively(n - 2)(x)
        )
        / n
    )


class LegendrePolynomial:
    roots = {}

    def __init__(self, degree: int):
        assert degree >= 0, 'The degree must be non-negative.'

        self.degree = degree

    def __call__(self, x: float) -> float:
        return self._as_lambda(x)

    def get_roots(  # noqa: WPS615
        self,
        line_segment: LineSegment = LineSegment(-1, 1),  # noqa: B008, WPS404
        number_of_part: int = 10000,
        accuracy: float = 10 ** -12,  # noqa: WPS404
    ) -> List[float]:
        if (self.degree, line_segment) in self.roots:
            return self.roots[(self.degree, line_segment)]  # noqa: WPS529

        tabulator = Tabulator(number_of_part)
        segments = tabulator.separate(f=self, line_segment=line_segment)

        secant_method = SecantMethod()
        roots = []
        for segment in segments:
            roots.append(secant_method.find(derivatives=[self], line_segment=segment, accuracy=accuracy))

        self.roots[(self.degree, line_segment)] = roots

        return roots

    @cached_property
    def _as_lambda(self) -> Callable[[float], float]:
        return _get_legendre_polynomial_recursively(self.degree)
