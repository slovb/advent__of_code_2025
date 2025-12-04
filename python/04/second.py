from dataclasses import dataclass
from typing import Set, Tuple


@dataclass(frozen=True)
class Data:
    input: Set[Tuple[int, int]]


def is_removable(boxes: Set[Tuple[int, int]], position: Tuple[int, int]):
    x, y = position
    subcount = 0
    for delta_x in range(-1, 2):
        for delta_y in range(-1, 2):
            if delta_x == delta_y == 0:
                continue
            if (x + delta_x, y + delta_y) in boxes:
                subcount += 1
    return subcount < 4


def solve(data: Data) -> int:
    out = 0
    boxes = set(data.input)
    while True:
        removed = set()
        for position in boxes:
            if is_removable(boxes, position):
                removed.add(position)
                out += 1
        if len(removed) == 0:
            break
        boxes = boxes.difference(removed)
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "@":
                    input.add((x, y))
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 43),
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
