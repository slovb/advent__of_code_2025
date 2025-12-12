from dataclasses import dataclass
from typing import List, Set, Tuple

type Position = Tuple[int, int]


@dataclass(frozen=True)
class Shape:
    positions: Set[Position]


@dataclass(frozen=True)
class Region:
    width: int
    height: int
    demand: Tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class Data:
    shapes: List[Shape]
    regions: List[Region]


def solve(data: Data) -> int:
    out = 0
    print(data)
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
            shapes.append(Shape(positions=positions))
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
