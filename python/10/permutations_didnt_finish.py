import itertools
from dataclasses import dataclass
from typing import List, Tuple

type IntVector = Tuple[int, ...]


@dataclass(frozen=True)
class Problem:
    target: Tuple[bool, ...]
    buttons: Tuple[IntVector, ...]
    requirement: IntVector


@dataclass(frozen=True)
class Data:
    problems: List[Problem]


def max_presses(button: IntVector, requirement: IntVector) -> int:
    return min([requirement[i] for i in button])


def reduced_requirement(
    button: IntVector, requirement: IntVector, presses: int
) -> IntVector:
    reduction = lambda i: presses if i in button else 0
    return tuple([requirement[i] - reduction(i) for i in range(len(requirement))])


def smash_buttons(
    buttons: Tuple[IntVector, ...], requirement: IntVector, limit: int | None
) -> int | None:
    if all([r == 0 for r in requirement]):
        return 0
    if len(buttons) == 0:
        return None
    presses = max_presses(buttons[0], requirement)
    if limit is not None:
        presses = min(presses, limit)
    subsmashes = []
    for i in range(
        1, presses + 1
    ):  # just going ham did not work, looping is too slow...
        subsmash = smash_buttons(
            buttons[1:],
            reduced_requirement(buttons[0], requirement, i),
            None if limit is None else limit - i,
        )
        if subsmash is not None:
            subsmashes.append(i + subsmash)
    if len(subsmashes) == 0:
        return None
    return min(subsmashes)


def solve_problem(problem: Problem) -> int:
    out = None
    for buttons in itertools.permutations(problem.buttons):
        candidate = smash_buttons(buttons, problem.requirement, out)
        if candidate is not None:
            if out is None or out > candidate:
                out = candidate
    if out is None:
        print("error")
        exit()
    return out


def solve(data: Data) -> int:
    out = 0
    for problem in data.problems:
        out += solve_problem(problem)
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        problems = []
        for row in rows:
            parts = row.split(" ")
            target_part = parts[0][1:-1]
            buttons_part = [group[1:-1] for group in parts[1:-1]]
            requirement_part = parts[-1][1:-1]

            target = tuple([True if c == "#" else False for c in target_part])
            buttons = tuple(
                [tuple(map(int, button.split(","))) for button in buttons_part]
            )
            requirement = tuple([int(num) for num in requirement_part.split(",")])

            problem = Problem(target=target, buttons=buttons, requirement=requirement)

            problems.append(problem)
        data = Data(problems=problems)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 33),
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
