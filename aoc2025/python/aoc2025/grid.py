from itertools import product


def find_neighbours(i: int, j: int, m: int, n: int) -> list[tuple[int, int]]:
    all_indices = product(
        range(max(0, i - 1), min(m - 1, i + 1) + 1),
        range(max(0, j - 1), min(n - 1, j + 1) + 1),
    )
    return [
        (row, col) for row, col in all_indices if not (row == i and col == j)
    ]
