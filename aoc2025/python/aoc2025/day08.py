import time
from collections import Counter
from math import prod

import click
import numpy as np

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]):
    """Parse the input lines."""
    return np.array([tuple(int(s) for s in line.split(",")) for line in lines])


def find_root(x: int, parents: list[int]) -> int:
    current = x
    while True:
        if parents[current] == current:
            return current
        else:
            current = parents[current]


def connect_boxes(x: int, y: int, parents: list[int]) -> int:
    root_x = find_root(x, parents)
    root_y = find_root(y, parents)
    if root_x != root_y:
        parents[root_x] = root_y
        return -1
    else:
        return 0


def solve_part1(lines: list[str], test: bool) -> int:
    """Solve part 1."""
    boxes = parse_input(lines)
    diffs = boxes[:, np.newaxis, :] - boxes[np.newaxis, :, :]
    distances = np.sqrt((diffs**2).sum(axis=2))
    rows, cols = np.triu_indices(len(boxes), k=1)
    pairwise_distances = distances[rows, cols]
    n_connections = 10 if test else 1000
    indices = np.argsort(pairwise_distances)[:n_connections]
    box_pairs = [
        (int(r), int(c))
        for r, c in zip(rows[indices], cols[indices], strict=True)
    ]
    parents = list(range(len(boxes)))
    for row, col in box_pairs:
        connect_boxes(row, col, parents)
    roots = [find_root(i, parents) for i in range(len(boxes))]
    circuit_sizes = Counter(roots)
    return prod(v for _, v in circuit_sizes.most_common(3))


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    boxes = parse_input(lines)
    diffs = boxes[:, np.newaxis, :] - boxes[np.newaxis, :, :]
    distances = np.sqrt((diffs**2).sum(axis=2))
    rows, cols = np.triu_indices(len(boxes), k=1)
    pairwise_distances = distances[rows, cols]
    indices = np.argsort(pairwise_distances)
    box_pairs = [
        (int(r), int(c))
        for r, c in zip(rows[indices], cols[indices], strict=True)
    ]
    parents = list(range(len(boxes)))
    n_circuits = len(boxes)
    for row, col in box_pairs:
        n_circuits += connect_boxes(row, col, parents)
        if n_circuits == 1:
            return int(boxes[row, 0] * boxes[col, 0])


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 08."""
    day = 8
    lines = load_lines(day, use_example=test)

    if part in ("1", "both"):
        start = time.perf_counter()
        answer1 = solve_part1(lines, test)
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
