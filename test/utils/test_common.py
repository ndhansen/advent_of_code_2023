from collections.abc import Iterator
from aoc.utils.common import Coord, a_star

import pytest

import math


@pytest.mark.parametrize(
    "start, goal, expected_cost, expected_path",
    [
        (
            Coord(0, 0),
            Coord(2, 2),
            2 * math.sqrt(2),
            [Coord(0, 0), Coord(1, 1), Coord(2, 2)],
        ),
        (Coord(0, 0), Coord(0, 2), 2 * 1, [Coord(0, 0), Coord(0, 1), Coord(0, 2)]),
        (Coord(2, 0), Coord(0, 0), 2 * 1, [Coord(2, 0), Coord(1, 0), Coord(0, 0)]),
    ],
)
def test_a_star(
    start: Coord, goal: Coord, expected_cost: float, expected_path: list[Coord]
) -> None:
    """
    Imagine a map like this:

    A..
    ...
    ..B

    We would expect to walk diagonally from A to B, assuming diagonals are
    faster to walk than straights (kinda).
    """

    def heuristic(current: Coord, goal: Coord) -> float:
        height = abs(current.y - goal.y)
        width = abs(current.x - goal.x)
        return math.sqrt(height**2 + width**2)

    def cost_func(last: Coord, current: Coord) -> float:
        # We can assume they will be points right next to each other
        height = abs(last.y - current.y)
        width = abs(last.x - current.x)
        return math.sqrt(height**2 + width**2)

    def neighbor(current: Coord) -> Iterator[Coord]:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                yield Coord(current.x + x, current.y + y)

    path, cost = a_star(start, goal, heuristic, cost_func, neighbor)

    assert cost == expected_cost
    assert path == expected_path
