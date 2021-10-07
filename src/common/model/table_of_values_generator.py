from abc import ABC, abstractmethod
from typing import Callable, List

import numpy as np
import pandas as pd

from src.common.model.line_segment import LineSegment


class TableOfValuesGenerator(ABC):
    @abstractmethod
    def generate_points(self, *, line_segment: LineSegment, number_of_points: int) -> List[float]:
        raise NotImplementedError

    def generate_table(
        self,
        *,
        f: Callable,
        line_segment: LineSegment,
        number_of_points: int,
    ) -> pd.DataFrame:
        nodes = np.array(sorted(self.generate_points(line_segment=line_segment, number_of_points=number_of_points)))
        values = f(nodes)

        return pd.DataFrame.from_dict({'x': nodes, 'y': values})
