from dataclasses import dataclass
from functools import cache
from typing import Dict, List


@dataclass(frozen=True)
class Node:
    name: str
    children: List[str]


@dataclass(frozen=True)
class Data:
    nodes: Dict[str, Node]


def solve(data: Data) -> int:
    @cache
    def traverse(name: str) -> int:
        if name == "out":
            return 1
        node = data.nodes[name]
        if len(node.children) == 0:
            return 0
        return sum([traverse(child) for child in node.children])

    return traverse("you")


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        nodes = {}
        for row in rows:
            name, rest = row.split(":")
            children = rest[1:].split(" ")
            nodes[name] = Node(name=name, children=children)
        data = Data(nodes=nodes)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 5),
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
