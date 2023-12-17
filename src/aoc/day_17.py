from collections.abc import Iterator
from enum import IntEnum, auto
from typing import Any, NamedTuple

from aoc.utils.common import a_star

from aoc.utils.contents import PuzzleInput


class Direction(IntEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Coord(NamedTuple):
    x: int
    y: int
    direction: Direction


def heuristic(current: Coord, goal: Coord) -> float:
    # Manhattan distance where each step is cost 1
    height = abs(current.y - goal.y)
    width = abs(current.x - goal.x)
    return height + width


class CostFunction:
    def __init__(self, lava_map: list[list[int]]) -> None:
        self.lava_map = lava_map

    def __call__(self, paths: dict[Coord, Coord], current: Coord, last: Coord) -> float:
        total = 0
        if last.x == current.x:
            if last.y < current.y:
                for y in range(last.y + 1, current.y + 1):
                    total += self.lava_map[y][current.x]
            else:
                for y in range(last.y - 1, current.y - 1, -1):
                    total += self.lava_map[y][current.x]
        elif last.y == current.y:
            if last.x < current.x:
                for x in range(last.x + 1, current.x + 1):
                    total += self.lava_map[current.y][x]
            else:
                for x in range(last.x - 1, current.x - 1, -1):
                    total += self.lava_map[current.y][x]
        else:
            raise ValueError()
        return float(total)


class NeighborFunction:
    def __init__(
        self, lava_map: list[list[int]], min_straight: int, max_straight: int
    ) -> None:
        self.lava_map = lava_map
        self.min_straight = min_straight
        self.max_straight = max_straight

    def __call__(self, current: Coord, paths: dict[Coord, Coord]) -> Iterator[Coord]:
        last = paths.get(current)
        all_neighbors = set()
        if last:
            if last.x == current.x:
                for i in range(self.min_straight, self.max_straight + 1):
                    all_neighbors.add(
                        Coord(current.x + i, current.y, Direction.HORIZONTAL)
                    )
                    all_neighbors.add(
                        Coord(current.x - i, current.y, Direction.HORIZONTAL)
                    )
            elif last.y == current.y:
                for i in range(self.min_straight, self.max_straight + 1):
                    all_neighbors.add(
                        Coord(current.x, current.y + i, Direction.VERTICAL)
                    )
                    all_neighbors.add(
                        Coord(current.x, current.y - i, Direction.VERTICAL)
                    )
            else:
                raise ValueError()
        else:
            for i in range(self.min_straight, self.max_straight + 1):
                all_neighbors.add(Coord(current.x + i, current.y, Direction.HORIZONTAL))
                all_neighbors.add(Coord(current.x - i, current.y, Direction.HORIZONTAL))
                all_neighbors.add(Coord(current.x, current.y + i, Direction.VERTICAL))
                all_neighbors.add(Coord(current.x, current.y - i, Direction.VERTICAL))

        for neighbor in all_neighbors:
            if neighbor.x < 0 or neighbor.x >= len(self.lava_map[0]):
                continue
            if neighbor.y < 0 or neighbor.y >= len(self.lava_map):
                continue
            yield neighbor


def part_1(puzzle: PuzzleInput) -> Any:
    lava_map: list[list[int]] = []
    for line in puzzle.lines:
        lava_map.append([int(x) for x in line])

    start = Coord(0, 0, Direction.HORIZONTAL)
    goals = [
        Coord(len(lava_map[0]) - 1, len(lava_map) - 1, Direction.HORIZONTAL),
        Coord(len(lava_map[0]) - 1, len(lava_map) - 1, Direction.VERTICAL),
    ]
    costs = []
    for goal in goals:
        _, cost = a_star(
            start,
            goal,
            heuristic,
            CostFunction(lava_map),
            NeighborFunction(lava_map, 1, 3),
        )
        costs.append(cost)
    return min(costs)


def part_2(puzzle: PuzzleInput) -> Any:
    lava_map: list[list[int]] = []
    for line in puzzle.lines:
        lava_map.append([int(x) for x in line])

    start = Coord(0, 0, Direction.HORIZONTAL)
    goals = [
        Coord(len(lava_map[0]) - 1, len(lava_map) - 1, Direction.HORIZONTAL),
        Coord(len(lava_map[0]) - 1, len(lava_map) - 1, Direction.VERTICAL),
    ]
    costs = []
    for goal in goals:
        _, cost = a_star(
            start,
            goal,
            heuristic,
            CostFunction(lava_map),
            NeighborFunction(lava_map, 4, 10),
        )
        costs.append(cost)
    return min(costs)
