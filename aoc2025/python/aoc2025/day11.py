import time
from collections.abc import Callable
from functools import cache

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]) -> dict[str, set[str]]:
    """Parse the input lines."""
    return {
        k: set(v.split(" ")) for line in lines for k, v in [line.split(": ")]
    }


def make_path_counter(graph: dict[str, set[str]]) -> Callable[[str, str], int]:
    @cache
    def count_paths(current: str, target: str) -> int:
        # Base case: reached the target
        if current == target:
            return 1
        return sum(
            count_paths(next_node, target)
            for next_node in graph.get(current, [])
        )

    return count_paths


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    graph = parse_input(lines)
    count_paths = make_path_counter(graph)
    return count_paths("you", "out")


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    graph = parse_input(lines)
    count_paths = make_path_counter(graph)
    dac_fft = count_paths("dac", "fft")
    if dac_fft:
        return (
            count_paths("svr", "dac")
            * count_paths("dac", "fft")
            * count_paths("fft", "out")
        )
    else:
        return (
            count_paths("svr", "fft")
            * count_paths("fft", "dac")
            * count_paths("dac", "out")
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
    """Solve Advent of Code 2025 Day 11."""
    day = 11
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
