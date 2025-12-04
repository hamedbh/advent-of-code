import time

import click

from aoc2024.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]):
    """Parse the input lines."""
    # TODO: Implement input parsing
    return lines


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    # input_data = parse_input(lines)
    # TODO: Implement part 1 solution
    return 0


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    # input_data = parse_input(lines)
    # TODO: Implement part 2 solution
    return 0


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2024 Day 03."""
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
