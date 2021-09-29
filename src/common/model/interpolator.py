from abc import ABC, abstractmethod

import pandas as pd


class Interpolator(ABC):
    @abstractmethod
    def get_approximate_value(self, x: float, table: pd.DataFrame) -> float:
        raise NotImplementedError
