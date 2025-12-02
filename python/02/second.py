from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Data:
    input: List[Tuple[int, int]]


def is_invalid(n: int):
    lazy = str(n)
    length = len(lazy)
    half = length // 2
    for i in range(1, half + 1):
        if length % i != 0:
            continue
        multiplier = length // i
        candidate = lazy[:i] * multiplier
        if lazy == candidate:
            return True
    return False


def solve(data: Data) -> int:
    out = 0
    for start, stop in data.input:
        for i in range(start, stop + 1):
            if is_invalid(i):
                print(i)
                out += i
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        ranges = rows[0].split(",")
        for range in ranges:
            parsed = tuple(map(int, range.split("-")))
            input.append(parsed)
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 4174379265),
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
