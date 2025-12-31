"""Advent of Code 2025, Day 9

This puzzle was a real PITA. Ended up having to look for help online,
which led me to an amazing breakdown of the problem on Reddit:

https://www.reddit.com/r/adventofcode/comments/1pichj2/comment/nt5guy3/

Someone had then ported that person's TypeScript code into Python:

https://github.com/euporphium/pyaoc/blob/main/aoc/2025/solutions/day09_part2.py

Overall this one was _hard_. When I first saw the puzzle I had thought
that maybe I needed to create the polygon for the boundaries, but that
seemed so impossible I just forgot about it.

The lesson here was really about understanding the size of the problem,
and that cool trick for 2d compression. Once it became possible to just
lookup elements from a relatively small grid (i.e. a `list[list[str]]`)
then the problem can complete v fast.
"""

import time
from itertools import product

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]) -> list[tuple[int, int]]:
    """Parse the input lines."""
    return [tuple(map(int, line.split(","))) for line in lines]  # ty:ignore[invalid-return-type]


def calculate_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    red_tiles = parse_input(lines)
    all_pairs = product(red_tiles, red_tiles)
    all_areas = [calculate_area(first, second) for first, second in all_pairs]
    return max(all_areas)


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    red_tiles = parse_input(lines)
    all_x, all_y = zip(*red_tiles, strict=True)
    sorted_x = sorted(set(all_x))
    sorted_y = sorted(set(all_y))
    # Start by compressing the 2d space
    map_x = {coord: i for i, coord in enumerate(sorted_x)}
    map_y = {coord: i for i, coord in enumerate(sorted_y)}
    compressed_red = [(map_x[x], map_y[y]) for x, y in red_tiles]

    # Create the grid
    width = len(sorted_x)
    height = len(sorted_y)
    grid = [["." for _ in range(width)] for _ in range(height)]

    # Now mark the red tiles
    for x, y in compressed_red:
        grid[y][x] = "#"

    # Now we 'rasterise' the edges of the polygon, i.e. connect them
    for i in range(len(compressed_red)):
        x1, y1 = compressed_red[i]
        x2, y2 = compressed_red[(i + 1) % len(compressed_red)]

        # If the line is vertical fill along that y-axis, otheriwse
        # fill along x-axis
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = "#"
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = "#"

    # Now we find some point on the inside of the polygon with
    # with raycasting
    inside_point = None
    for y in range(height):
        for x in range(width):
            if grid[y][x] != ".":
                continue

            # Count transitions from this point to the left.
            transitions = 0
            prev = "."
            for i in range(x, -1, -1):
                cur = grid[y][i]
                # This tests whether we have hit a polygon edge
                if cur != prev:
                    transitions += 1
                prev = cur

            # Odd number of transitions means we started inside
            if transitions % 2 == 1:
                inside_point = (x, y)
                break
        if inside_point:
            break

    # Now we flood fill from the inside point
    if inside_point:
        stack = [inside_point]
        while stack:
            x, y = stack.pop()
            if 0 <= x < width and 0 <= y < height and grid[y][x] == ".":
                grid[y][x] = "X"
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    # Find the largest rectangle that is entirely inside the polygon
    max_area = 0

    for i, first in enumerate(red_tiles[:-1]):
        x1, y1 = first
        cx1, cy1 = map_x[x1], map_y[y1]
        for second in red_tiles[i + 1 :]:
            x2, y2 = second
            cx2, cy2 = map_x[x2], map_y[y2]

            # Calculate the actual area, ignore if it is smaller than
            # current best
            area = calculate_area(first, second)
            if area <= max_area:
                continue

            # Check if the edges of the rectangle are entirely inside
            # the polygon
            min_cx = min(cx1, cx2)
            max_cx = max(cx1, cx2)
            min_cy = min(cy1, cy2)
            max_cy = max(cy1, cy2)

            enclosed = True

            # First check top and bottom edges
            for cx in range(min_cx, max_cx + 1):
                if grid[min_cy][cx] == "." or grid[max_cy][cx] == ".":
                    enclosed = False
                    break

            # Then the left and right
            if enclosed:
                for cy in range(min_cy, max_cy + 1):
                    if grid[cy][min_cx] == "." or grid[cy][max_cx] == ".":
                        enclosed = False
                        break

            if enclosed:
                max_area = area

    return max_area


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day 09."""
    day = 9
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
    # red_tiles = parse_input(lines)
    # all_polygon_edges = tuple(
    #     (red_tiles[i], red_tiles[(i + 1) % len(red_tiles)])
    #     for i in range(len(red_tiles))
    # )
    # all_pairs = product(red_tiles, red_tiles)
    # max_area = 0
    # for first, second in all_pairs:
    #     if first == second:
    #         continue
    #     area = calculate_area(first, second)
    #     if area <= max_area:
    #         continue
    #     if is_rectangle_valid(first, second, all_polygon_edges):
    #         max_area = area
    # return max_area
    # # Everything below this point is the old code, will remove it once I
    # # have the new logic sorted.
    # # all_bounded_points = product(
    # #     range(min_x, max_x + 1), range(min_y, max_y + 1)
    # # )
    # # all_green_points = {
    # #     point
    # #     for point in all_bounded_points
    # #     if is_green_tile(point[0], point[1], red_tiles)
    # # }

    # # # Code below is left over from before
    # all_pairs = product(red_tiles, red_tiles)
    # max_area = 0
    # for first, second in all_pairs:
    #     # Generate all points inside the rectangle
    #     all_points = product(
    #         range(min(first[0], second[0]), max(first[0], second[0]) + 1),
    #         range(min(first[1], second[1]), max(first[1], second[1]) + 1),
    #     )
    #     # Only calculate the area of the rectangle if all points are
    #     # in the legal area
    #     if all(point in all_green_points for point in all_points):
    #         max_area = max(max_area, calculate_area(first, second))
    # return max_area
