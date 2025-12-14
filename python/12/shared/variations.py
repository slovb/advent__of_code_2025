from typing import List

from shared.shape import Shape


def variations(shape: Shape) -> List[Shape]:
    shapes = []
    seen = set()
    for _i in range(2):
        for _j in range(4):
            h = shape.hash()
            if h not in seen:
                seen.add(h)
                shapes.append(shape)
            shape = shape.rotated()
        shape = shape.flipped()
    return shapes
