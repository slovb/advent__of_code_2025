from dataclasses import dataclass
from typing import List, Tuple

from z3 import Int, Optimize, sat

type IntV = Tuple[int, ...]


@dataclass(frozen=True)
class Problem:
    target: Tuple[bool, ...]
    buttons: Tuple[IntV, ...]
    requirement: IntV


@dataclass(frozen=True)
class Data:
    problems: List[Problem]


def solve_problem(problem: Problem) -> int:
    num_buttons = len(problem.buttons)
    button_presses = [Int(f"b{i}") for i in range(num_buttons)]

    opt = Optimize()

    # positive
    for press in button_presses:
        opt.add(press >= 0)

    # requirements
    for index, total in enumerate(problem.requirement):
        buttons_that_affect_requirement = [
            press
            for i, press in enumerate(button_presses)
            if index in problem.buttons[i]
        ]
        opt.add(sum(buttons_that_affect_requirement) == total)

    opt.minimize(sum(button_presses))

    if opt.check() != sat:
        print("error")
        exit()
    m = opt.model()
    out = sum([m[press].as_long() for press in button_presses])
    print(out)
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
