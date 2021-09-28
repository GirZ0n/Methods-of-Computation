from typing import List

from src.common.model.line_segment import LineSegment
from src.common.model.table_of_values_generator import TableOfValuesGenerator


class EquidistantTableOfValuesGenerator(TableOfValuesGenerator):
    def generate_points(self, *, line_segment: LineSegment, number_of_points: int) -> List[float]:
        return line_segment.split_into_points(number_of_points - 1)
