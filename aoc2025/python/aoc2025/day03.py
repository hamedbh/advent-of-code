import time

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]):
    """Parse the input lines."""
    return [tuple(map(int, s)) for s in lines]


def locate_max(batteries: tuple[int, ...]) -> tuple[int, int]:
    return max(enumerate(batteries), key=lambda x: x[1])


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    input_data = parse_input(lines)
    left_tuples = [locate_max(bank[:-1]) for bank in input_data]
    right_tuples = [
        locate_max(bank[left[0] + 1 :])
        for left, bank in zip(left_tuples, input_data, strict=True)
    ]
    max_values = [
        (10 * left[1]) + right[1]
        for left, right in zip(left_tuples, right_tuples, strict=True)
    ]
    return sum(max_values)


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    input_data = parse_input(lines)
    slices = range(-11, 1)
    total = 0
    for bank in input_data:
        left_slice = 0
        for i in slices:
            right_slice = i if i < 0 else len(bank)
            index, value = locate_max(bank[left_slice : right_slice])
            left_slice += index + 1
            total += value * (10**(-i))
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
    """Solve Advent of Code 2025 Day 03."""
    day = 3
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
