from dataclasses import dataclass
from typing import List, Tuple

type Coord = Tuple[int, int]


@dataclass(frozen=True)
class Data:
    input: List[Coord]


def valid(a: Coord, b: Coord, data: Data) -> bool:
    min_x = min(a[0], b[0])
    min_y = min(a[1], b[1])
    max_x = max(a[0], b[0])
    max_y = max(a[1], b[1])
    # invalidate lines as while valid that should not be interesting
    if min_x == max_x or min_y == max_y:
        return False
    # is there a node inside?
    for c in data.input:
        if min_x < c[0] < max_x and min_y < c[1] < max_y:
            return False

    # check if any line goes through the interior
    for i, c in enumerate(data.input):
        j = (i + 1) % len(data.input)
        d = data.input[j]  # next point makes an edge of the polygon
        cd_min_x = min(c[0], d[0])
        cd_min_y = min(c[1], d[1])
        cd_max_x = max(c[0], d[0])
        cd_max_y = max(c[1], d[1])
        if cd_min_x == cd_max_x:  # vertical
            if min_x < cd_min_x < max_x:
                if cd_min_y <= min_y and max_y <= cd_max_y:
                    return False
        elif cd_min_y == cd_max_y:  # horizontal
            if min_y < cd_min_y < max_y:
                if cd_min_x <= min_x and max_x <= cd_max_x:
                    return False
        else:
            print("error")
            exit()

    # ray-casting to check if there is a point inside the polygon
    # using floats as the logic should still hold and I can ignore parallel lines
    positions = [
        (min_x + 0.5, min_y + 0.5),
    ]
    for x, y in positions:
        # assume ray from above
        count = 0
        for i, c in enumerate(data.input):
            j = (i + 1) % len(data.input)
            d = data.input[j]  # next point makes an edge of the polygon
            if c[0] == d[0]:  # ray is vertical so ignore vertical edges
                continue
            if c[1] != d[1]:  # sanity check, no diagonals
                print("error")
                exit()
            if c[1] > y:  # we are coming from above so can ignore edges below
                continue
            if min(c[0], d[0]) < x < max(c[0], d[0]):
                count += 1
        if count % 2 == 0:  # odd counts are inside
            return False
    return True


def area(a: Coord, b: Coord) -> int:
    width = 1 + abs(a[0] - b[0])
    height = 1 + abs(a[1] - b[1])
    return width * height


def solve(data: Data) -> int:
    out = 0
    for i, a in enumerate(data.input):
        for b in data.input[i + 1 :]:
            if valid(a, b, data):
                value = area(a, b)
                if value > out:
                    print(f"{value}: {a} x {b}")
                    out = value
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            bits = row.split(",")
            x, y = list(map(int, bits))
            input.append((x, y))
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 24),
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
