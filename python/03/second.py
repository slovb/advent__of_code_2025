from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Data:
    input: List[List[int]]


def subscore(bank: List[int], remaining: int) -> int:
    if remaining == 0:
        return 0
    shortened = bank[: len(bank) - (remaining - 1)]
    value = max(shortened)
    index = bank.index(value)
    return value * 10 ** (remaining - 1) + subscore(bank[index + 1 :], remaining - 1)


def solve(data: Data) -> int:
    out = 0
    for bank in data.input:
        out += subscore(bank, 12)
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            parsed = list(map(int, row))
            input.append(parsed)
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 3121910778619),
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
