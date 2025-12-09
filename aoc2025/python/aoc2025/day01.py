import time
from itertools import accumulate

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def count_zero_clicks(start_position: int, turn_size: int) -> int:
    start_position %= 100
    distance = abs(turn_size)
    full_cycles = distance // 100

    if turn_size >= 0:
        end = (start_position + distance) % 100
        if end < start_position:
            full_cycles += 1
    else:
        end = (start_position - distance) % 100
        if end > start_position:
            full_cycles += 1
    return full_cycles


def parse_input(lines: list[str]):
    """Parse the input lines."""
    return [(1 if s[0] == "R" else -1) * int(s[1:]) for s in lines]


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    input_data = parse_input(lines)
    mod_positions = accumulate([50] + input_data, lambda x, y: (x + y) % 100)
    return sum(position == 0 for position in mod_positions)


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    input_data = parse_input(lines)
    positions = list(accumulate([50] + input_data))
    return sum(
        count_zero_clicks(start, turn)
        for start, turn in zip(positions, input_data, strict=False)
    )


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 01."""
    day = 1
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
