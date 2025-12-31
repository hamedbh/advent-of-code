import time
from collections.abc import Callable
from math import prod

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input_human(
    lines: list[str],
) -> tuple[tuple[int, ...], tuple[Callable[[tuple[int, ...]], int], ...]]:
    """Parse the input lines."""
    operands = tuple(
        zip(*(map(int, line.split()) for line in lines[:-1]), strict=True)
    )
    operators = tuple(sum if s == "+" else prod for s in lines[-1].split())
    return operands, operators


def parse_input_ceph(
    lines: list[str],
) -> tuple[tuple[int, ...], tuple[Callable[[tuple[int, ...]], int], ...]]:
    """
    Parse the input lines in the cephalopod style, i.e.
    right-to-left and top to bottom.
    """
    operators = tuple(sum if s == "+" else prod for s in lines[-1].split())
    columns = tuple(zip(*lines[:-1], strict=True))
    groups = []
    current_group = []
    for column in columns:
        if all(s == " " for s in column):
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(column)
    if current_group:
        groups.append(current_group)
    operands = tuple(
        tuple(int("".join(c for c in column if c != " ")) for column in group)
        for group in groups
    )
    return operands, operators  # ty:ignore[invalid-return-type]


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    all_operands, operators = parse_input_human(lines)
    total = 0
    for operands, operator in zip(all_operands, operators, strict=True):
        total += operator(operands)
    return total


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    all_operands, operators = parse_input_ceph(lines)
    total = 0
    for operands, operator in zip(all_operands, operators, strict=True):
        total += operator(operands)
    return total


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 06."""
    day = 6
    lines = load_lines(day, use_example=test)

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
