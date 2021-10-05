from functools import reduce
from typing import List

import pandas as pd

from src.common.model.interpolator import Interpolator


class LagrangeInterpolator(Interpolator):
    def get_approximate_value(self, x: float, table: pd.DataFrame) -> float:
        return table.apply(
            lambda row: self._multiply_basis_polynomial_by_function_value(x, table['x'], row['y'], row.name),
            axis=1,
        ).sum()

    def _multiply_basis_polynomial_by_function_value(
        self,
        x: float,
        points: List[float],
        function_value: float,
        index: int,
    ) -> float:
        basis_polynomial_value = (
            reduce(lambda a, b: a * b, self._get_differences(x, points, index), 1)
            / reduce(lambda a, b: a * b, self._get_differences(points[index], points, index), 1)
        )

        return basis_polynomial_value * function_value

    @staticmethod
    def _get_differences(x: float, points: List[float], ignored_index: int) -> List[float]:
        return [x - point for index, point in enumerate(points) if index != ignored_index]
