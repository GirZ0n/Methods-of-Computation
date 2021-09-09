from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LineSegment:
    left: float
    right: float

    def __post_init__(self):
        if self.left > self.right:
            raise ValueError(f'The start of the segment should not exceed its end ({self.left} > {self.right}).')

    def __str__(self) -> str:
        return f'[{self.left}, {self.right}]'

    def __len__(self) -> float:
        return self.right - self.left

    def split(self) -> Tuple['LineSegment', 'LineSegment']:
        return LineSegment(self.left, self.midpoint), LineSegment(self.midpoint, self.right)

    @property
    def midpoint(self) -> float:
        return (self.left + self.right) / 2
