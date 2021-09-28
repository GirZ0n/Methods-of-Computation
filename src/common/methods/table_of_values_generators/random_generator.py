import random
from typing import List, Optional

from src.common.model.line_segment import LineSegment
from src.common.model.table_of_values_generator import TableOfValuesGenerator
from src.common.utils import sample_floats


class RandomTableOfValuesGenerator(TableOfValuesGenerator):
    seed: Optional[int]

    def __init__(self, seed: int = None):
        self.seed = seed

    def generate_points(self, *, line_segment: LineSegment, number_of_points: int) -> List[float]:
        random.seed(self.seed)
        nodes = sample_floats(line_segment.left, line_segment.right, number_of_points)
        random.seed(None)
        return nodes
