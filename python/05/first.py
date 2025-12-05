from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Data:
    ranges: List[Tuple[int, int]]
    available: List[int]


def solve(data: Data) -> int:
    out = 0
    for id in data.available:
        for start, stop in data.ranges:
            if start <= id <= stop:
                out += 1
                break
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        ranges = []
        i = 0
        for row in rows:
            if row == "":
                break
            i += 1
            start, stop = map(int, row.split("-"))
            ranges.append((start, stop))

        available = []
        for row in rows[i + 1 :]:
            available.append(int(row))
        data = Data(ranges=ranges, available=available)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 3),
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
