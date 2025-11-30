import click

from aoc2024.utils import load_lines, save_answer


def parse_input(lines: list[str]) -> tuple[list[int], list[int]]:
    """Parse the input lines into two lists of integers."""
    left_list = []
    right_list = []

    for line in lines:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

    return left_list, right_list


def solve_part1(lines: list[str]) -> int:
    """Solve part 1: total distance between sorted lists."""
    left_list, right_list = parse_input(lines)

    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    total_distance = sum(
        abs(left - right)
        for left, right in zip(left_sorted, right_sorted, strict=True)
    )
    return total_distance


def solve_part2(lines: list[str]) -> int:
    """Solve part 2: similarity score."""
    left_list, right_list = parse_input(lines)

    # Count occurrences in right list
    right_counts = {}
    for num in right_list:
        right_counts[num] = right_counts.get(num, 0) + 1

    # Calculate similarity score
    similarity_score = sum(num * right_counts.get(num, 0) for num in left_list)
    return similarity_score


@click.command()
@click.option(
    "--test", is_flag=True, help="Run on example data instead of real input"
)
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2024 Day 1."""
    day = 1
    lines = load_lines(day, use_example=test)

    if part in ("1", "both"):
        answer1 = solve_part1(lines)
        print(f"Part 1: {answer1}")
        save_answer(day, 1, answer1, use_example=test)

    if part in ("2", "both"):
        answer2 = solve_part2(lines)
        print(f"Part 2: {answer2}")
        save_answer(day, 2, answer2, use_example=test)


if __name__ == "__main__":
    main()
