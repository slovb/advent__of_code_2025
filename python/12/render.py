from typing import List

from PIL import Image, ImageDraw

from shared import Region, Shape


def render(placed: List[Shape], region: Region, path: str):
    pixel_size = 16
    gap_size = 4

    def pixel_square(x: int, y: int):
        start_x = (pixel_size + gap_size) * x
        start_y = (pixel_size + gap_size) * y
        end_x = start_x + pixel_size - 1
        end_y = start_y + pixel_size - 1
        return [
            (start_x, start_y),
            (end_x, end_y),
        ]

    def horizontal_gap(x: int, y: int):
        start_x = (pixel_size + gap_size) * x
        start_y = (pixel_size + gap_size) * y + pixel_size
        end_x = start_x + pixel_size - 1
        end_y = start_y + gap_size - 1
        return [
            (start_x, start_y),
            (end_x, end_y),
        ]

    def vertical_gap(x: int, y: int):
        start_x = (pixel_size + gap_size) * x + pixel_size
        start_y = (pixel_size + gap_size) * y
        end_x = start_x + gap_size - 1
        end_y = start_y + pixel_size - 1
        return [
            (start_x, start_y),
            (end_x, end_y),
        ]

    def corner_gap(x: int, y: int):
        start_x = (pixel_size + gap_size) * x + pixel_size
        start_y = (pixel_size + gap_size) * y + pixel_size
        end_x = start_x + gap_size - 1
        end_y = start_y + gap_size - 1
        return [
            (start_x, start_y),
            (end_x, end_y),
        ]

    background_color = (0x1E, 0x27, 0x2E)
    colors = [
        (0xF5, 0x3B, 0x57),
        (0x3C, 0x40, 0xC6),
        (0xFF, 0xA8, 0x01),
        (0x0F, 0xBC, 0xF9),
        (0xFF, 0xD3, 0x2A),
        (0x00, 0xD8, 0xD6),
        (0xFF, 0x3F, 0x34),
        (0x05, 0xC4, 0x6B),
        (0x80, 0x8E, 0x9B),
        (0x9B, 0x59, 0xB6),
        (0xEC, 0xF0, 0xF1),
        (0xE7, 0x4C, 0x3C),
        (0x34, 0x98, 0xDB),
        (0xE6, 0x7E, 0x22),
        (0x2E, 0xCC, 0x71),
        (0xF1, 0xC4, 0x0F),
        (0x1A, 0xBC, 0x9C),
        (0xB3, 0x37, 0x71),
        (0x1B, 0x9C, 0xFC),
        (0xF8, 0xEF, 0xBA),
        (0x55, 0xE6, 0xC1),
        (0xD6, 0xA2, 0xE8),
        (0xF9, 0x7F, 0x51),
        (0xBD, 0xC5, 0x81),
        (0xFC, 0x42, 0x7B),
        (0x3B, 0x3B, 0x98),
    ]

    fps = 12
    image = Image.new(
        "RGB",
        (
            region.width * (pixel_size + gap_size),
            region.height * (pixel_size + gap_size),
        ),
        background_color,
    )
    images = [image] * fps  # pad the start for effect

    # render placed
    for i, shape in enumerate(placed):
        image = image.copy()
        draw = ImageDraw.Draw(image)
        color = colors[i % len(colors)]
        for x, y in shape.positions:
            draw.rectangle(pixel_square(x, y), fill=color)
            adjacent = [
                (x, y + 1) in shape.positions,
                (x + 1, y) in shape.positions,
                (x + 1, y + 1) in shape.positions,
            ]
            if adjacent[0]:
                draw.rectangle(horizontal_gap(x, y), fill=color)
            if adjacent[1]:
                draw.rectangle(vertical_gap(x, y), fill=color)
            if all(adjacent):
                draw.rectangle(corner_gap(x, y), fill=color)
        images.append(image)

    # pad the end
    images += [image] * 2 * fps

    # save
    images[0].save(
        f"{path}/animation_{region.index:04d}.gif",
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // fps,
        loop=0,
    )
