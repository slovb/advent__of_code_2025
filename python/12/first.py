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


@dataclass(frozen=True)
class Data:
    shapes: List[Shape]
    regions: List[Region]


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


def solve_region(shapes: List[Shape], region: Region):
    remaining = [region.demand[i] for i in range(6)]
    occupied: Set[Position] = set()
    placed: List[Shape] = []
    width, height = 0, 0

    def fits(shape: Shape):
        for position in shape.positions:
            if position in occupied:
                return False
        return True

    # meh packing, greedy minimize area and try to use the most demanded remaining piece
    while True:
        if all([remaining[i] == 0 for i in range(6)]):
            print("WIN")
            print(display(occupied, region.width, region.height, remaining))
            return 1
        candidate = None
        best_score = None
        for shape in shapes:
            if remaining[shape.index] <= 0:
                continue
            lx = max(0, width - 3)
            ux = min(width, region.width - 3)
            ly = max(0, height - 3)
            uy = min(height, region.height - 3)

            # place above
            for x in range(0, ux + 1):
                for y in range(ly, uy + 1):
                    c = shape.translate(x, y)
                    if fits(c):
                        new_area = max(x + 3, width) * max(y + 3, height)
                        score = (new_area, 0 - remaining[c.index])
                        if (
                            candidate is None
                            or best_score is None
                            or score < best_score
                        ):
                            candidate = c
                            best_score = score
                        break

            # place right of
            for y in range(0, uy + 1):
                for x in range(lx, ux + 1):
                    c = shape.translate(x, y)
                    if fits(c):
                        new_area = max(x + 3, width) * max(y + 3, height)
                        score = (new_area, 0 - remaining[c.index])
                        if (
                            candidate is None
                            or best_score is None
                            or score < best_score
                        ):
                            candidate = c
                            best_score = score
                        break
        if candidate is None:
            break
        # validate
        valid = True
        for p in candidate.positions:
            if p in occupied:
                print("error #0")
                valid = False
            x, y = p
            width = max(width, x + 1)
            height = max(height, y + 1)
            if width > region.width:
                print("error #1")
                valid = False
            if height > region.height:
                print("error #2")
                valid = False
            if remaining[candidate.index] <= 0:
                print("error #3")
                valid = False
        if valid:
            placed.append(candidate)
            for p in candidate.positions:
                occupied.add(p)
            remaining[candidate.index] -= 1
        else:
            break

    print("FAIL")
    print(display(occupied, region.width, region.height, remaining))
    return 0


def solve(data: Data) -> int:
    out = 0
    shapes: List[Shape] = []
    for shape in data.shapes:
        shapes = shapes + variations(shape)
    for region in data.regions:
        area = region.width * region.height
        shape_area = sum(
            [region.demand[shape.index] * len(shape.positions) for shape in data.shapes]
        )
        if sum(region.demand) * 9 < area:
            # Trivially solvable
            out += 1
        elif shape_area > area:
            # Trivially impossible
            pass
        else:
            out += solve_region(shapes, region)
    return out


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
        for row in rows[5 * 6 :]:
            dims, dems = row.split(":")
            width, height = list(map(int, dims.split("x")))
            d0, d1, d2, d3, d4, d5 = list(map(int, dems[1:].split(" ")))
            demand = (d0, d1, d2, d3, d4, d5)
            regions.append(Region(width=width, height=height, demand=demand))
        data = Data(shapes=shapes, regions=regions)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 2),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
            print(f"{filename}   {str(res)}\n")
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed:
            filename = "input.txt"
            print(f"{filename}   {main(filename)}\n")
    else:
        for f in sys.argv[1:]:
            print(f"{f}:\n{main(f)}\n")
