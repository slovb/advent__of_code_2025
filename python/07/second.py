from dataclasses import dataclass
from typing import Set, Tuple

type Pos = Tuple[int, int]


@dataclass(frozen=True)
class Data:
    source: Pos
    splitters: Set[Pos]
    height: int


def solve(data: Data) -> int:
    beams = {data.source: 1}
    processing_y = 0
    while processing_y < data.height:
        future_beams = {}

        def add_to_future(pos: Pos, count: int):
            if pos not in future_beams:
                future_beams[pos] = 0
            future_beams[pos] += count

        for pos, count in beams.items():
            x, y = pos
            candidate = (x, y + 1)
            if candidate not in data.splitters:
                add_to_future(candidate, count)
            else:
                add_to_future((x - 1, y + 1), count)
                add_to_future((x + 1, y + 1), count)
        beams = future_beams
        processing_y += 1
    return sum(beams.values())


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        source = None
        splitters = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == ".":
                    continue
                pos = (x, y)
                if c == "S":
                    if source != None:
                        print("Invalid assumption")
                        exit(1)
                    source = pos
                else:
                    splitters.add(pos)
        if source == None:
            print("Invalid assumption")
            exit(1)
        data = Data(source=source, splitters=splitters, height=y + 1)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 40),
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
