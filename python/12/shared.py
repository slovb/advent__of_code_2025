from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

type Position = Tuple[int, int]


@dataclass(frozen=True)
class Shape:
    positions: Set[Position]
    index: int

    def hash(self) -> int:
        out = 0
        for x, y in self.positions:
            out += 2 ** (x + 3 * y)
        return out

    def rotated(self) -> Shape:
        p = set()
        for x, y in self.positions:
            p.add((2 - y, x))
        return Shape(positions=p, index=self.index)

    def flipped(self) -> Shape:
        p = set()
        for x, y in self.positions:
            p.add((y, x))
        return Shape(positions=p, index=self.index)

    def translate(self, x: int, y: int) -> Shape:
        p = set()
        for a, b in self.positions:
            p.add((a + x, b + y))
        return Shape(positions=p, index=self.index)


@dataclass(frozen=True)
class Region:
    width: int
    height: int
    demand: Tuple[int, int, int, int, int, int]
    index: int


@dataclass(frozen=True)
class Data:
    shapes: List[Shape]
    regions: List[Region]


def display(occupied: Set[Position], width: int, height: int, remaining: List[int]):
    out = [f"{width}x{height}:"]
    out.append(" ".join([str(i) for i in remaining]))
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in occupied:
                row.append("#")
            else:
                row.append(".")
        out.append("".join(row))
    out.append("")
    return "\n".join(out)


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


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        shapes = []
        regions = []
        for i in range(6):
            positions = set()
            for y in range(3):
                for x in range(3):
                    row = rows[5 * i + 1 + y]
                    if row[x] == "#":
                        positions.add((x, y))
                    elif row[x] == ".":
                        pass
                    else:
                        print("error")
                        exit()
            shapes.append(Shape(positions=positions, index=i))
        index = 0
        for row in rows[5 * 6 :]:
            dims, dems = row.split(":")
            width, height = list(map(int, dims.split("x")))
            d0, d1, d2, d3, d4, d5 = list(map(int, dems[1:].split(" ")))
            demand = (d0, d1, d2, d3, d4, d5)
            regions.append(
                Region(width=width, height=height, demand=demand, index=index)
            )
            index += 1
        data = Data(shapes=shapes, regions=regions)
        return data
