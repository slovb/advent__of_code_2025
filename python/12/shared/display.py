from typing import List, Set

from shared.position import Position


def display(occupied: Set[Position], width: int, height: int, remaining: List[int]):
    out = [f"{width}x{height}:"]
    out.append(" ".join([str(i) for i in remaining]))
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in occupied:
                row.append("#")
            else:
                row.append(".")
        out.append("".join(row))
    out.append("")
    return "\n".join(out)
