import itertools
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Problem:
    target: Tuple[bool, ...]
    buttons: Tuple[Tuple[int, ...], ...]
    requirement: Tuple[int, ...]


@dataclass(frozen=True)
class Data:
    problems: List[Problem]


def multiplier(buttons: Tuple[Tuple[int, ...], ...], requirement: Tuple[int, ...]):
    state = [0] * len(requirement)
    for button in buttons:
        for i in button:
            state[i] += 1
    # return all([state[i] == requirement[i] for i in range(len(requirement))])
    out = None
    for i in range(len(state)):
        if state[i] == 0:
            if requirement[i] != 0:
                return None
        if requirement[i] % state[i] != 0:
            return None
        value = requirement[i] // state[i]
        if out is None:
            out = value
        if value != out:
            return None
    return out


def solve_problem(problem: Problem) -> int:
    r = 0
    while True:
        for buttons in itertools.combinations_with_replacement(problem.buttons, r):
            # TODO actually knapsack
            mul = multiplier(buttons, problem.requirement)
            if mul is not None:
                print(r * mul)
                return r * mul
        r += 1
    print("error")
    exit()


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
