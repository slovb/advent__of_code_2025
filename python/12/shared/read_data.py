from shared.data import Data
from shared.region import Region
from shared.shape import Shape


def read_data(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        shapes = []
        regions = []
        for i in range(6):
            positions = set()
            for y in range(3):
                for x in range(3):
                    row = rows[5 * i + 1 + y]
                    if row[x] == "#":
                        positions.add((x, y))
                    elif row[x] == ".":
                        pass
                    else:
                        print("error")
                        exit()
            shapes.append(Shape(positions=positions, index=i))
        index = 0
        for row in rows[5 * 6 :]:
            dims, dems = row.split(":")
            width, height = list(map(int, dims.split("x")))
            d0, d1, d2, d3, d4, d5 = list(map(int, dems[1:].split(" ")))
            demand = (d0, d1, d2, d3, d4, d5)
            regions.append(
                Region(width=width, height=height, demand=demand, index=index)
            )
            index += 1
        data = Data(shapes=shapes, regions=regions)
        return data
