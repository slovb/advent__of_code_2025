from dataclasses import dataclass
from typing import Dict, Set, Tuple

from PIL import Image, ImageDraw


@dataclass(frozen=True)
class Data:
    input: Set[Tuple[int, int]]
    width: int
    height: int


def is_removable(boxes: Set[Tuple[int, int]], position: Tuple[int, int]):
    x, y = position
    subcount = 0
    for delta_x in range(-1, 2):
        for delta_y in range(-1, 2):
            if delta_x == delta_y == 0:
                continue
            if (x + delta_x, y + delta_y) in boxes:
                subcount += 1
    return subcount < 4


def display(
    boxes: Set[Tuple[int, int]],
    width: int,
    height: int,
    step: int,
    removed_at: Dict[Tuple[int, int], int],
):
    pixel_size = 4
    background_color = (0x1E, 0x27, 0x2E)
    box_color = (0x4B, 0xCF, 0xFA)
    removed_color = (0xF5, 0x3B, 0x57)

    image = Image.new(
        "RGB", (width * pixel_size, height * pixel_size), background_color
    )

    draw = ImageDraw.Draw(image)
    for y in range(height):
        for x in range(width):
            pos = (x, y)
            color = background_color
            if pos in boxes:
                color = box_color
            elif pos in removed_at:
                value = removed_at[pos]
                diff = max(0, (8 - (step - value)))
                if diff > 0:
                    multiplier = diff / 8.0
                    color = (
                        int(removed_color[0] * multiplier),
                        int(removed_color[1] * multiplier),
                        int(removed_color[2] * multiplier),
                    )
            draw.rectangle(
                [
                    (pixel_size * x, pixel_size * y),
                    (pixel_size * (x + 1), pixel_size * (y + 1)),
                ],
                fill=color,
            )
    return image


def solve(data: Data) -> int:
    out = 0
    fps = 30
    boxes = set(data.input)
    step = 0
    removed_at: Dict[Tuple[int, int], int] = {}
    images = [display(boxes, data.width, data.height, step, removed_at)] * fps
    while True:
        removed = set()
        for position in boxes:
            if is_removable(boxes, position):
                removed.add(position)
                removed_at[position] = step
                out += 1
        if len(removed) == 0:
            break
        boxes = boxes.difference(removed)
        images.append(display(boxes, data.width, data.height, step, removed_at))
        step += 1
    # extra frames
    for i in range(2 * fps):
        images.append(display(boxes, data.width, data.height, step + i, removed_at))
    # save
    images[0].save(
        "image/animation.gif",
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // fps,
        loop=0,
    )

    return out


def read(filename) -> Data:
    width = 0
    height = 0
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "@":
                    input.add((x, y))
                    width = max(width, x + 1)
                    height = max(height, y + 1)
        data = Data(input=input, width=width, height=height)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    filename = "input.txt"
    print(f"{filename}   {main(filename)}")
