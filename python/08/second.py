from dataclasses import dataclass
from functools import cache
from math import dist
from typing import List, Tuple

type Coord = Tuple[int, int, int]


@dataclass(frozen=True)
class Data:
    input: List[Coord]


@cache
def distance(x: Coord, y: Coord):
    return dist(x, y)


def solve(data: Data) -> int:
    circuits = [set([c]) for c in data.input]

    def find_circuit(x: Coord):
        for i, group in enumerate(circuits):
            if x in group:
                return group, i
        print("error")
        exit(1)

    while len(circuits) > 1:
        # find nodes to merge
        best_distance = None
        best_pair = None
        for i, x in enumerate(data.input):
            x_group, x_group_i = find_circuit(x)
            for y in data.input[i + 1 :]:
                if best_distance is not None and abs(y[0] - x[0]) > best_distance:
                    break
                if y in x_group:
                    continue
                delta = distance(x, y)
                if best_distance is None or delta < best_distance:
                    best_distance = delta
                    best_pair = (x, y)
        # merge nodes
        if best_pair is None:
            print("Early exit?")
            break
        print(best_pair)
        x, y = best_pair
        x_group, x_group_i = find_circuit(x)
        y_group, y_group_i = find_circuit(y)
        circuits[x_group_i] = x_group.union(y_group)
        del circuits[y_group_i]
    return x[0] * y[0]


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            x, y, z = list(map(int, row.split(",")))
            input.append((x, y, z))
        data = Data(input=sorted(input))
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 25272),
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
        print("Not supported at the moment")
