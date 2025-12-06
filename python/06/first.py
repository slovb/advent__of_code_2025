import re
from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass(frozen=True)
class Data:
    input: List[List[int]]
    operations: List[str]


def solve(data: Data) -> int:
    out = 0
    for i, op in enumerate(data.operations):
        numbers = [data.input[j][i] for j in range(len(data.input))]
        if op == "+":
            out += reduce(lambda x, y: x + y, numbers)
        else:
            out += reduce(lambda x, y: x * y, numbers, 1)
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.strip() for row in f.readlines()]
        input = []
        for row in rows[:-1]:
            input.append(list(map(int, re.split(r" +", row))))
        operations = re.split(r" +", rows[-1])
        data = Data(input=input, operations=operations)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 4277556),
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
