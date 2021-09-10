from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.common.model.aliases import Value


@dataclass(init=False)
class LineSegment:
    left: Decimal
    right: Decimal

    def __init__(self, left: Value, right: Value):
        self.left = Decimal(left)
        self.right = Decimal(right)

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
    def length(self) -> Decimal:
        return self.right - self.left

    @property
    def midpoint(self) -> Decimal:
        return (self.left + self.right) / 2
