from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd
from sympy import lambdify

from src.common.model.line_segment import LineSegment


class NodesGenerator(ABC):
    @abstractmethod
    def generate_nodes(self, *, line_segment: LineSegment, number_of_nodes: int) -> List[float]:
        raise NotImplementedError

    def generate_table(
        self,
        *,
        expression,
        variable: str = 'x',
        line_segment: LineSegment,
        number_of_nodes: int,
    ) -> pd.DataFrame:
        f = lambdify(variable, expression)

        nodes = np.array(sorted(self.generate_nodes(line_segment=line_segment, number_of_nodes=number_of_nodes)))
        values = f(nodes)

        return pd.DataFrame.from_dict({'x': nodes, 'y': values})
