from dataclasses import dataclass
from typing import List

from src.common.config import OUTPUT_PRECISION


@dataclass
class LineSegment:
    left: float
    right: float

    def __post_init__(self):
        if self.left > self.right:
            raise ValueError(f'The start of the segment should not exceed its end ({self.left} > {self.right}).')

    def __str__(self) -> str:
        return f'[{round(self.left, OUTPUT_PRECISION)}, {round(self.right, OUTPUT_PRECISION)}]'

    def split_into_segments(self, parts: int = 2) -> List['LineSegment']:
        points = self.split_into_points(parts)

        return [LineSegment(left_boundary, right_boundary) for left_boundary, right_boundary in zip(points, points[1:])]

    def split_into_points(self, parts: int = 2) -> List[float]:
        part_length = self.length / parts

        points = [self.left]
        left_boundary = self.left
        for _ in range(parts):
            right_boundary = left_boundary + part_length
            points.append(right_boundary)
            left_boundary = right_boundary

        return points

    @property
    def length(self) -> float:
        return self.right - self.left

    @property
    def midpoint(self) -> float:
        return (self.left + self.right) / 2
