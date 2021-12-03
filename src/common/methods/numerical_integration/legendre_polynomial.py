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
    else:
        return (
            lambda x: (
                (2 * n - 1) * _get_legendre_polynomial_recursively(n - 1)(x) * x
                - (n - 1) * _get_legendre_polynomial_recursively(n - 2)(x)
            )
            / n
        )


class LegendrePolynomial:
    def __init__(self, degree: int):
        assert degree >= 0, 'The degree must be non-negative.'

        self.degree = degree

    def __call__(self, x: float) -> float:
        return self._as_lambda(x)

    @cached_property
    def _as_lambda(self) -> Callable[[float], float]:
        return _get_legendre_polynomial_recursively(self.degree)

    def get_roots(
        self,
        line_segment: LineSegment = LineSegment(-1, 1),
        number_of_part: int = 10000,
        accuracy: float = 10 ** -12,
    ) -> List[float]:
        tabulator = Tabulator(number_of_part)
        segments = tabulator.separate(f=self, line_segment=line_segment)

        secant_method = SecantMethod()
        roots = []
        for segment in segments:
            roots.append(secant_method.find(derivatives=[self], line_segment=segment, accuracy=accuracy))

        return roots
