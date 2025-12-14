from typing import Set

from shared.position import Position
from shared.shape import Shape


def added_dead_pixels(
    shape: Shape,
    new_width: int,
    new_height: int,
    occupied: Set[Position],
):
    min_x = min([p[0] for p in shape.positions])
    min_y = min([p[1] for p in shape.positions])
    max_x = min_x + 2
    max_y = min_y + 2
    alive: Set[Position] = set()
    dead: Set[Position] = set()

    def blocked(pos):
        x, y = pos
        if x < 0 or new_width < x:
            return True
        if y < 0 or new_height < y:
            return True
        return pos in shape.positions or pos in occupied

    def process(x, y, alive, dead):
        batch = set()
        processing = [(x, y)]
        while len(processing) > 0:
            p = processing.pop()
            if p in alive or p[0] >= new_width or p[1] >= new_height:
                for b in batch:
                    alive.add(b)
                return
            if p in dead:
                for b in batch:
                    dead.add(b)
                return
            px, py = p
            neighbors = [
                (px - 1, py),
                (px, py - 1),
                (px + 1, py),
                (px, py + 1),
            ]
            for neighbor in neighbors:
                if not blocked(neighbor) and neighbor not in batch:
                    batch.add(neighbor)
        # failed to end early
        for b in batch:
            dead.add(b)

    for x in range(min_x, max_x):
        # can ignore outer edge
        for y in range(min_y, max_y):
            if (x, y) in alive or (x, y) in dead:
                continue
            process(x, y, alive, dead)
    return len(dead)
