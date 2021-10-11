import pandas as pd

from src.common.model.numerical_differentiator import NumericalDifferentiator


class FirstDerivativeFinder(NumericalDifferentiator):
    def calculate_derivatives_table(self, *, function_values: pd.Series, step: float) -> pd.Series:
        if len(function_values) < 3:
            raise ValueError('There must be at least three values in the table.')

        left_derivative = -3 * function_values[0] + 4 * function_values[1] - function_values[2]
        left_derivative /= 2 * step

        last_index = len(function_values) - 1
        right_derivative = (
            3 * function_values[last_index] - 4 * function_values[last_index - 1] + function_values[last_index - 2]
        )
        right_derivative /= 2 * step

        middle_derivatives = []
        for left_value, right_value in zip(function_values, function_values[2:]):
            middle_derivatives.append((right_value - left_value) / (2 * step))

        return pd.Series([left_derivative, *middle_derivatives, right_derivative], name='y')
