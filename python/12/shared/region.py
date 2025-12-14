from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Region:
    width: int
    height: int
    demand: Tuple[int, int, int, int, int, int]
    index: int
