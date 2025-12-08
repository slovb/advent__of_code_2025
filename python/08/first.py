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


def solve(data: Data, n: int) -> int:
    circuits = [set([c]) for c in data.input]
    connections = set()

    def find_group(x: Coord):
        for i, group in enumerate(circuits):
            if x in group:
                return group, i
        print("error")
        exit(1)

    for _ in range(n):
        # find nodes to merge
        best_distance = None
        best_pair = None
        for i, x in enumerate(data.input):
            for y in data.input[i + 1 :]:
                if (x, y) in connections:
                    continue
                delta = distance(x, y)
                if best_distance is None or delta < best_distance:
                    best_distance = delta
                    best_pair = (x, y)
        # connect
        if best_pair is None:
            print("Early exit?")
            break
        print(best_pair)
        connections.add(best_pair)
        # merge nodes
        x, y = best_pair
        x_group, x_group_i = find_group(x)
        y_group, y_group_i = find_group(y)
        if x_group_i != y_group_i:
            circuits[x_group_i] = x_group.union(y_group)
            del circuits[y_group_i]
    sorted_sizes = sorted([len(group) for group in circuits], reverse=True)
    print(sorted_sizes)
    return sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            x, y, z = list(map(int, row.split(",")))
            input.append((x, y, z))
        data = Data(input=input)
        return data


def main(filename, n: int):
    return solve(read(filename), n)


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 40),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename, 10)
            print(f"{filename}   {str(res)}\n")
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed:
            filename = "input.txt"
            print(f"{filename}   {main(filename, 1000)}\n")
    else:
        print("Not supported at the moment")
