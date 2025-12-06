from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass(frozen=True)
class Data:
    numbers: List[List[int]]
    operations: List[str]


def solve(data: Data) -> int:
    out = 0
    print(data)
    for i, op in enumerate(data.operations):
        if op == "+":
            out += reduce(lambda x, y: x + y, data.numbers[i])
        else:
            out += reduce(lambda x, y: x * y, data.numbers[i], 1)
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row for row in f.readlines()]
        numbers = []
        operations = []
        column = len(rows[1]) - 2

        nums = []
        while column >= 0:
            op = rows[-1][column]
            num = "".join([rows[i][column] for i in range(len(rows) - 1)]).strip()
            nums.append(int(num))
            if op != " ":
                numbers.append(nums)
                operations.append(op)
                nums = []
                column -= 1
            column -= 1

        data = Data(numbers=numbers, operations=operations)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 3263827),
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
