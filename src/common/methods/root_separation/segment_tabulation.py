from src.common.model.LineSegment import LineSegment
from src.common.model.root_separator import RootSeparator


class Tabulator(RootSeparator):
    number_of_parts: int

    def __init__(self, number_of_parts: int):
        self.number_of_parts = number_of_parts

    def separate(self, line_segment: LineSegment, function, variable: str = 'x'):
        segments = line_segment.split(self.number_of_parts)

        found_segments = []
        for segment in segments:
            left_value = function.evalf(subs={variable: segment.left})
            right_value = function.evalf(subs={variable: segment.right})

            if left_value * right_value <= 0:
                found_segments.append(segment)

        return found_segments
