from typing import List, Set

from shared.data import Data
from shared.display import display
from shared.position import Position
from shared.read_data import read_data
from shared.region import Region
from shared.render import render
from shared.shape import Shape
from shared.variations import variations

IMAGE_PATH = "image/meh"


def solve_region(shapes: List[Shape], region: Region):
    remaining = [region.demand[i] for i in range(6)]
    occupied: Set[Position] = set()
    placed: List[Shape] = []
    width, height = 0, 0

    def fits(shape: Shape):
        for position in shape.positions:
            if position in occupied:
                return False
        return True

    # meh packing, greedy minimize area and try to use the most demanded remaining piece
    while True:
        if all([remaining[i] == 0 for i in range(6)]):
            print("WIN")
            print(display(occupied, region.width, region.height, remaining))
            render(placed, region, IMAGE_PATH)
            return 1
        candidate = None
        best_score = None
        for shape in shapes:
            if remaining[shape.index] <= 0:
                continue
            lx = max(0, width - 3)
            ux = min(width, region.width - 3)
            ly = max(0, height - 3)
            uy = min(height, region.height - 3)

            # place above
            for x in range(0, ux + 1):
                for y in range(ly, uy + 1):
                    c = shape.translate(x, y)
                    if fits(c):
                        new_area = max(x + 3, width) * max(y + 3, height)
                        score = (new_area, 0 - remaining[c.index])
                        if (
                            candidate is None
                            or best_score is None
                            or score < best_score
                        ):
                            candidate = c
                            best_score = score
                        break

            # place right of
            for y in range(0, uy + 1):
                for x in range(lx, ux + 1):
                    c = shape.translate(x, y)
                    if fits(c):
                        new_area = max(x + 3, width) * max(y + 3, height)
                        score = (new_area, 0 - remaining[c.index])
                        if (
                            candidate is None
                            or best_score is None
                            or score < best_score
                        ):
                            candidate = c
                            best_score = score
                        break
        if candidate is None:
            break
        # validate
        valid = True
        for p in candidate.positions:
            if p in occupied:
                print("error #0")
                valid = False
            x, y = p
            width = max(width, x + 1)
            height = max(height, y + 1)
            if width > region.width:
                print("error #1")
                valid = False
            if height > region.height:
                print("error #2")
                valid = False
            if remaining[candidate.index] <= 0:
                print("error #3")
                valid = False
        if valid:
            placed.append(candidate)
            for p in candidate.positions:
                occupied.add(p)
            remaining[candidate.index] -= 1
        else:
            break

    print("FAIL")
    print(display(occupied, region.width, region.height, remaining))
    return 0


def solve(data: Data) -> int:
    out = 0
    shapes: List[Shape] = []
    for shape in data.shapes:
        shapes = shapes + variations(shape)
    for region in data.regions:
        area = region.width * region.height
        shape_area = sum(
            [region.demand[shape.index] * len(shape.positions) for shape in data.shapes]
        )
        if sum(region.demand) * 9 < area:
            # Trivially solvable
            out += 1
        elif shape_area > area:
            # Trivially impossible
            pass
        else:
            out += solve_region(shapes, region)
    return out


def main(filename):
    return solve(read_data(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 2),
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
