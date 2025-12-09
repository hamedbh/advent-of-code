import time
from itertools import chain
from math import floor, log10

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def decimal_length(n: int) -> int:
    if n == 0:
        return 1
    return floor(log10(abs(n))) + 1


def proper_divisors(n: int) -> list[int]:
    if n <= 1:
        return []

    divisors = {1}  # 1 is always a proper divisor

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)  # Add the paired divisor

    return sorted(divisors)


def parse_input(lines: list[str]):
    """Parse the input lines."""
    assert len(lines) == 1
    return [tuple(map(int, s.split("-"))) for s in lines[0].split(",")]


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    input_data = parse_input(lines)
    invalid_sum = 0
    for bounds in input_data:
        for id in range(bounds[0], bounds[1] + 1):
            num_digits = decimal_length(id)
            # Any id with an odd number of digits will always be valid
            if num_digits % 2 != 0:
                continue
            string_id = str(id)
            if string_id[: num_digits // 2] == string_id[num_digits // 2 :]:
                invalid_sum += id
    return invalid_sum


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    input_data = parse_input(lines)
    max_length = decimal_length(max(chain.from_iterable(input_data)))
    all_proper_divisors = {
        n: proper_divisors(n) for n in range(2, max_length + 1)
    }
    invalid_sum = 0
    for bounds in input_data:
        for id in range(bounds[0], bounds[1] + 1):
            idstring = str(id)
            num_digits = decimal_length(id)
            if num_digits < 2:
                continue
            for d in all_proper_divisors[num_digits]:
                if idstring == idstring[:d] * (num_digits // d):
                    invalid_sum += id
                    break
    return invalid_sum


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 02."""
    day = 2
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
