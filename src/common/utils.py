import random
from typing import List


def sample_floats(low: float, high: float, k: int = 1) -> List[float]:
    """Return a k-length list of unique random floats in the range of low <= x <= high."""
    seen = set()
    for _ in range(k):
        x = random.uniform(low, high)
        while x in seen:
            x = random.uniform(low, high)
        seen.add(x)

    return list(seen)
