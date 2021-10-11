import pandas as pd

from src.common.model.numerical_differentiator import NumericalDifferentiator


class SecondDerivativeFinder(NumericalDifferentiator):
    def calculate_derivatives_table(self, *, function_values: pd.Series, step: float) -> pd.Series:
        if len(function_values) < 3:
            raise ValueError('There must be at least three values in the table.')

        derivatives = []
        for left_value, middle_value, right_value in zip(function_values, function_values[1:], function_values[2:]):
            derivatives.append((right_value - 2 * middle_value + left_value) / (step ** 2))

        return pd.Series([None, *derivatives, None])
