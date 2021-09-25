import random
from typing import List, Optional

from src.common.model.line_segment import LineSegment
from src.common.model.nodes_generator import NodesGenerator
from src.utils import sample_floats


class RandomNodesGenerator(NodesGenerator):
    seed: Optional[int]

    def __init__(self, seed: int = None):
        self.seed = seed
        random.seed(seed)

    def generate_nodes(self, *, line_segment: LineSegment, number_of_nodes: int) -> List[float]:
        return sample_floats(line_segment.left, line_segment.right, number_of_nodes)
