from abc import ABC, abstractmethod

import pandas as pd


class NumericalDifferentiator(ABC):
    @abstractmethod
    def calculate_derivatives_table(self, *, function_values: pd.Series, step: float) -> pd.Series:
        raise NotImplementedError
