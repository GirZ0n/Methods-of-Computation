from typing import List

from src.common.model.line_segment import LineSegment
from src.common.model.nodes_generator import NodesGenerator


class EquidistantNodesGenerator(NodesGenerator):
    def generate_nodes(self, *, line_segment: LineSegment, number_of_nodes: int) -> List[float]:
        return line_segment.split_into_points(number_of_nodes - 1)
