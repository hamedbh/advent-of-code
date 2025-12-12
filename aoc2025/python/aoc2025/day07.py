import time

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]):
    """Parse the input lines."""
    return lines


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    input_data = parse_input(lines)
    beams = {i for i, s in enumerate(input_data[0]) if s == "S"}
    max_index = len(input_data[0]) - 1
    split_count = 0
    for i in range(1, len(input_data)):
        below_positions = [input_data[i][j] for j in beams]
        new_beams = []
        for beam_col, char_below in zip(beams, below_positions, strict=True):
            if char_below == "^":
                split_count += 1
                new_beams.append(beam_col - 1)
                new_beams.append(beam_col + 1)
            if char_below == ".":
                new_beams.append(beam_col)
        beams = {beam for beam in new_beams if 0 <= beam <= max_index}
    return split_count


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    input_data = parse_input(lines)
    beams = {i: 1 for i, s in enumerate(input_data[0]) if s == "S"}
    max_index = len(input_data[0]) - 1
    for i in range(1, len(input_data)):
        below_positions = [input_data[i][j] for j in beams.keys()]
        new_beams = {}
        for beam_col, char_below in zip(
            beams.keys(), below_positions, strict=True
        ):
            if char_below == "^":
                if beam_col - 1 >= 0:
                    new_beams[beam_col - 1] = (
                        new_beams.get(beam_col - 1, 0) + beams[beam_col]
                    )
                if beam_col + 1 <= max_index:
                    new_beams[beam_col + 1] = (
                        new_beams.get(beam_col + 1, 0) + beams[beam_col]
                    )
            if char_below == ".":
                new_beams[beam_col] = (
                    new_beams.get(beam_col, 0) + beams[beam_col]
                )
        beams = new_beams
    return sum(v for v in beams.values())


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 07."""
    day = 7
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
