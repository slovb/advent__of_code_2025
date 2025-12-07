from dataclasses import dataclass
from math import log
from typing import Dict, List, Set, Tuple

from PIL import Image, ImageDraw

type Pos = Tuple[int, int]


@dataclass(frozen=True)
class Data:
    source: Pos
    splitters: Set[Pos]
    width: int
    height: int


def render(data: Data, memory: List[Dict[Pos, int]], max_count: int):
    pixel_size = 4
    image_size = (data.width * pixel_size, data.height * pixel_size)

    def rectangle(x: int, y: int):
        return [
            (pixel_size * x, pixel_size * y),
            (pixel_size * (x + 1) - 1, pixel_size * (y + 1) - 1),
        ]

    background_color = (0x00, 0x00, 0x00)
    lo_beam_color = (0x1E, 0x27, 0x2E)
    hi_beam_color = (0xFF, 0x3F, 0x34)
    effect_color = (0xFF, 0xD3, 0x2A)
    splitter_color = (0x05, 0xC4, 0x4B)

    def beam_color(count: int):
        value = log(count) / log(max_count)
        multiplier = min(1.0, max(0.0, value))
        mix = lambda a, b: int(a * (1.0 - multiplier) + b * multiplier)
        color = (
            mix(lo_beam_color[0], hi_beam_color[0]),
            mix(lo_beam_color[1], hi_beam_color[1]),
            mix(lo_beam_color[2], hi_beam_color[2]),
        )
        return color

    fps = 30
    background_image = Image.new("RGB", image_size, background_color)
    mask = Image.new("1", image_size, None)

    # Render splitters and start
    draw = ImageDraw.Draw(background_image)
    draw_mask = ImageDraw.Draw(mask)
    x, y = data.source
    draw.rectangle(
        rectangle(x, y),
        fill=lo_beam_color,
    )
    draw_mask.rectangle(
        rectangle(x, y),
        fill=1,
    )
    for x, y in data.splitters:
        draw.rectangle(
            rectangle(x, y),
            fill=splitter_color,
        )
        draw_mask.rectangle(
            rectangle(x, y),
            fill=1,
        )

    # Pad the start
    images = [background_image] * fps

    def blast_some_noise(foreground_image, effect_image):
        effect_mask = Image.effect_noise((data.width // 4, data.height // 4), 2048.0)
        effect_mask = effect_mask.resize(image_size, Image.Resampling.NEAREST)
        masked_image = Image.composite(effect_image, foreground_image, effect_mask)
        effect_mask = Image.effect_noise((data.width // 2, data.height // 2), 256.0)
        effect_mask = effect_mask.resize(image_size, Image.Resampling.NEAREST)
        masked_image = Image.composite(masked_image, foreground_image, effect_mask)
        effect_mask = Image.effect_noise((data.width // 1, data.height // 1), 32.0)
        effect_mask = effect_mask.resize(image_size, Image.Resampling.NEAREST)
        masked_image = Image.composite(masked_image, foreground_image, effect_mask)
        return masked_image

    # Animate
    foreground_image = Image.new("RGB", image_size, None)
    effect_image = Image.new("RGB", image_size, None)
    for beams in memory:
        foreground_image = foreground_image.copy()
        effect_image = effect_image.copy()
        draw = ImageDraw.Draw(foreground_image)
        draw_effect = ImageDraw.Draw(effect_image)
        for pos, count in beams.items():
            x, y = pos
            draw.rectangle(
                rectangle(x, y),
                fill=beam_color(count),
            )
            draw_effect.rectangle(
                rectangle(x, y),
                fill=effect_color,
            )
        final = Image.composite(
            background_image, blast_some_noise(foreground_image, effect_image), mask
        )
        images.append(final)

    # Pad the end
    for _ in range(2 * fps):
        final = Image.composite(
            background_image, blast_some_noise(foreground_image, effect_image), mask
        )
        images.append(final)
    images += [images[-1]] * (fps // 4)

    # Save
    images[0].save(
        "image/animation2.gif",
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // fps,
        loop=0,
    )


def solve(data: Data) -> int:
    beams = {data.source: 1}
    memory = [beams]
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
        memory.append(beams)
        processing_y += 1
    max_count = max(beams.values())
    render(data, memory, max_count)
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
        data = Data(source=source, splitters=splitters, width=x + 1, height=y + 1)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    filename = "input.txt"
    print(f"{filename}   {main(filename)}\n")
