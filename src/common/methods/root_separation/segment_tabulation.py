from typing import Callable, List

from src.common.model.line_segment import LineSegment
from src.common.model.root_separator import RootSeparator


class Tabulator(RootSeparator):
    number_of_parts: int

    def __init__(self, number_of_parts: int):
        self.number_of_parts = number_of_parts

    def separate(self, *, f: Callable[[float], float], line_segment: LineSegment) -> List[LineSegment]:
        segments = line_segment.split_into_segments(self.number_of_parts)

        found_segments = []
        for segment in segments:
            left_value = f(segment.left)
            right_value = f(segment.right)

            if left_value * right_value <= 0:
                found_segments.append(segment)

        return found_segments
