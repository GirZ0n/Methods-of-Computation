from typing import List

import pandas as pd

from src.common.model.interpolator import Interpolator


class NewtonInterpolator(Interpolator):
    def get_approximate_value(self, x: float, table: pd.DataFrame) -> float:
        approximate_solution = 0
        current_product_of_differences = 1
        divided_differences = self._get_divided_differences(table)
        for index, divided_difference in enumerate(divided_differences):
            approximate_solution += divided_difference * current_product_of_differences
            current_product_of_differences *= x - table.at[index, 'x']

        return approximate_solution

    @staticmethod
    def _get_divided_differences(table: pd.DataFrame) -> List[float]:
        divided_differences = []
        current_values = list(table['y'])
        for i in range(1, len(table)):
            next_values = []
            for j, (first, second) in enumerate(zip(current_values, current_values[1:])):
                next_values.append((second - first) / (table.at[j + i, 'x'] - table.at[j, 'x']))
            divided_differences.append(current_values[0])
            current_values = next_values

        return divided_differences
