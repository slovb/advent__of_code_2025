from typing import Set

from shared.position import Position
from shared.shape import Shape


def fits(shape: Shape, occupied: Set[Position]):
    for position in shape.positions:
        if position in occupied:
            return False
    return True
