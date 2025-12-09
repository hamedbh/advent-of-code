import time

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    """Parse the input lines."""
    fresh_ranges = []
    available = []
    for item in lines:
        if "-" in item:
            fresh_ranges.append(tuple(int(x) for x in item.split("-")))
        elif item:
            available.append(int(item))
    return fresh_ranges, available


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    fresh_ranges, available = parse_input(lines)
    fresh_count = 0
    for item in available:
        for lower, upper in fresh_ranges:
            if lower <= item <= upper:
                fresh_count += 1
                break
    return fresh_count


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    fresh_ranges, _ = parse_input(lines)
    sorted_ranges = sorted(fresh_ranges)
    merged_ranges = []
    current_range = sorted_ranges[0]
    for i in range(1, len(sorted_ranges)):
        lower, upper = sorted_ranges[i]
        if current_range[1] >= lower:
            current_range = (current_range[0], max(current_range[1], upper))
        else:
            merged_ranges.append(current_range)
            current_range = (lower, upper)
    merged_ranges.append(current_range)
    total = 0
    for lower, upper in merged_ranges:
        total += upper - lower + 1
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
    """Solve Advent of Code 2025 Day 05."""
    day = 5
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
