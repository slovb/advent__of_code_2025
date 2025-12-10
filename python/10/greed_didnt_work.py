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


def how_many_presses(button: IntVector, requirement: IntVector) -> int:
    return min([requirement[i] for i in button])


def reduced_requirement(
    button: IntVector, requirement: IntVector, presses: int
) -> IntVector:
    reduction = lambda i: presses if i in button else 0
    return tuple([requirement[i] - reduction(i) for i in range(len(requirement))])


def recurse(
    buttons: List[IntVector], requirement: IntVector, count: int = 0
) -> int | None:
    if all([r == 0 for r in requirement]):
        return count
    if len(buttons) == 0:
        return None
    first = buttons[0]
    rest = buttons[1:]
    candidate = None
    amount = how_many_presses(first, requirement)
    if amount > 0:
        candidate = recurse(
            rest, reduced_requirement(first, requirement, amount), count + amount
        )
    alternative = recurse(rest, requirement, count)
    if candidate is None:
        return alternative
    elif alternative is None:
        return candidate
    return min(alternative, candidate)


def solve_problem(problem: Problem) -> int:
    buttons = sorted(problem.buttons, key=len, reverse=True)
    ans = recurse(buttons=buttons, requirement=problem.requirement)
    print(ans)
    if ans is None:
        print("error")
        exit()
    return ans


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
