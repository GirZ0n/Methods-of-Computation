from dataclasses import dataclass
from typing import List


@dataclass
class LineSegment:
    left: float
    right: float

    def __post_init__(self):
        if self.left > self.right:
            raise ValueError(f'The start of the segment should not exceed its end ({self.left} > {self.right}).')

    def __str__(self) -> str:
        return f'[{self.left}, {self.right}]'

    def split(self, parts: int = 2) -> List['LineSegment']:
        part_length = self.length / parts

        segments = []
        left_boundary = self.left
        for _ in range(parts):
            right_boundary = left_boundary + part_length
            segments.append(LineSegment(left_boundary, right_boundary))
            left_boundary = right_boundary

        return segments

    @property
    def length(self) -> float:
        return self.right - self.left

    @property
    def midpoint(self) -> float:
        return (self.left + self.right) / 2