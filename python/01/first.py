from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    input: list[tuple[str, int]]


def solve(data: Data) -> int:
    out = 0
    state = 50
    for direction, amount in data.input:
        if direction == "L":
            amount *= -1
        state = (state + amount) % 100
        if state == 0:
            out += 1
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            input.append((row[0], int(row[1:])))
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 3),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
            print("{}   {}\n".format(filename, str(res)))
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
