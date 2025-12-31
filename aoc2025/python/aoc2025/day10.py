"""Advent of Code 2025, Day 10

This one was quite tricky. Ended up having to look for help online,
again. The first part was simpler when I stopped trying to parse the
whole input in one go and instead operated line-by-line.

The second part I solved using an integer linear programming approach,
with help from hyperhelios.
"""

import re
import time
from itertools import combinations

import click
import z3

from aoc2025.utils import load_lines, save_answer, save_timing


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    result: int = 0
    for line in lines:
        match = re.match(r"^\[([#.]+)\] ([()\d, ]+) \{([\d,]+)\}$", line)
        if match:
            lights: set[int] = {
                index
                for index, light in enumerate(match.groups()[0])
                if light == "#"
            }
            buttons: list[set[int]] = [
                set(map(int, button[1:-1].split(",")))
                for button in match.groups()[1].split()
            ]
            for r in range(1, len(buttons) + 1):
                for combo in combinations(buttons, r=r):
                    switched_on: set[int] = set()
                    for button in combo:
                        switched_on ^= button
                    if switched_on == lights:
                        result += r
                        break
                else:
                    continue
                break

    return result


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    result: int = 0
    for line in lines:
        match = re.match(r"^\[([#.]+)\] ([()\d, ]+) \{([\d,]+)\}$", line)
        if match:
            buttons: list[set[int]] = [
                set(map(int, button[1:-1].split(",")))
                for button in match.groups()[1].split()
            ]
            joltages: list[int] = list(map(int, match.groups()[2].split(",")))
            o = z3.Optimize()
            vars = z3.Ints(f"n{i}" for i in range(len(buttons)))
            for var in vars:
                o.add(var >= 0)
            for i, joltage in enumerate(joltages):
                equation = 0
                for b, button in enumerate(buttons):
                    if i in button:
                        equation += vars[b]
                o.add(equation == joltage)
            o.minimize(sum(vars))
            o.check()
            result += o.model().eval(sum(vars)).as_long()
    return result


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 10."""
    day = 10
    lines: list[str] = load_lines(day, use_example=test)

    if part in ("1", "both"):
        start = time.perf_counter()
        answer1 = solve_part1(lines)
        elapsed1 = time.perf_counter() - start
        print(f"Part 1: {answer1} ({elapsed1:.3f}s)")
        save_answer(day, 1, answer1, use_example=test)
        if not test:
            save_timing(day, 1, elapsed1)

    if part in ("2", "both"):
        start = time.perf_counter()
        answer2 = solve_part2(lines)
        elapsed2 = time.perf_counter() - start
        print(f"Part 2: {answer2} ({elapsed2:.3f}s)")
        save_answer(day, 2, answer2, use_example=test)
        if not test:
            save_timing(day, 2, elapsed2)


if __name__ == "__main__":
    main()
