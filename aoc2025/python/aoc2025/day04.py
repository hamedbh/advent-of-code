import time

import click

from aoc2025.grid import find_neighbours
from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]) -> list[list[int]]:
    """Parse the input lines."""
    return [[1 if x == "@" else 0 for x in line] for line in lines]


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    input_data = parse_input(lines)
    m = len(input_data)
    n = len(input_data[0])
    total = 0
    for i in range(m):
        for j in range(n):
            if input_data[i][j] != 1:
                continue
            neighbours = find_neighbours(i, j, m, n)
            roll_count = sum([input_data[row][col] for row, col in neighbours])
            if roll_count < 4:
                total += 1
    return total


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    input_data = parse_input(lines)
    m = len(input_data)
    n = len(input_data[0])
    total = 0
    while True:
        removable = []
        for i in range(m):
            for j in range(n):
                if input_data[i][j] != 1:
                    continue
                neighbours = find_neighbours(i, j, m, n)
                roll_count = sum(
                    [input_data[row][col] for row, col in neighbours]
                )
                if roll_count < 4:
                    removable.append((i, j))
        if len(removable) > 0:
            total += len(removable)
            for row, col in removable:
                input_data[row][col] = 0
        else:
            break
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
    """Solve Advent of Code 2025 Day 04."""
    day = 4
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
