from dataclasses import dataclass
from typing import Set, Tuple


@dataclass(frozen=True)
class Data:
    input: Set[Tuple[int, int]]


def solve(data: Data) -> int:
    out = 0
    while True:
        to_remove = set()
        for x, y in data.input:
            subcount = 0
            for delta_x in range(-1, 2):
                for delta_y in range(-1, 2):
                    if delta_x == delta_y == 0:
                        continue
                    if (x + delta_x, y + delta_y) in data.input:
                        subcount += 1
            if subcount < 4:
                to_remove.add((x, y))
                out += 1
        if len(to_remove) == 0:
            break
        for pos in to_remove:
            data.input.remove(pos)
        to_remove = set()
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
            print("{}   {}\n".format(filename, str(res)))
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
