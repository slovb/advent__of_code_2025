from dataclasses import dataclass
from typing import List

from shared.region import Region
from shared.shape import Shape


@dataclass(frozen=True)
class Data:
    shapes: List[Shape]
    regions: List[Region]
