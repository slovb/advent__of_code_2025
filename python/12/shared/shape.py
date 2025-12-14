from __future__ import annotations

from dataclasses import dataclass
from typing import Set

from shared.position import Position


@dataclass(frozen=True)
class Shape:
    positions: Set[Position]
    index: int

    def hash(self) -> int:
        out = 0
        for x, y in self.positions:
            out += 2 ** (x + 3 * y)
        return out

    def rotated(self) -> Shape:
        p = set()
        for x, y in self.positions:
            p.add((2 - y, x))
        return Shape(positions=p, index=self.index)

    def flipped(self) -> Shape:
        p = set()
        for x, y in self.positions:
            p.add((y, x))
        return Shape(positions=p, index=self.index)

    def translate(self, x: int, y: int) -> Shape:
        p = set()
        for a, b in self.positions:
            p.add((a + x, b + y))
        return Shape(positions=p, index=self.index)
