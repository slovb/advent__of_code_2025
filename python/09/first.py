from dataclasses import dataclass
from typing import List, Tuple

type Coord = Tuple[int, int]


@dataclass(frozen=True)
class Data:
    input: List[Coord]


def area(a: Coord, b: Coord) -> int:
    width = 1 + abs(a[0] - b[0])
    height = 1 + abs(a[1] - b[1])
    return width * height


def solve(data: Data) -> int:
    out = 0
    max_x = max([c[0] for c in data.input])
    max_y = max([c[1] for c in data.input])
    corners = [(0, 0), (max_x, 0), (0, max_y), (max_x, max_y)]
    for i, a in enumerate(data.input):
        limit = max([area(a, corner) for corner in corners])
        if limit < out:  # Ended up being mostly useless
            # print("skip")
            continue
        for b in data.input[i + 1 :]:
            out = max(out, area(a, b))
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            bits = row.split(",")
            x, y = list(map(int, bits))
            input.append((x, y))
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 50),
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
