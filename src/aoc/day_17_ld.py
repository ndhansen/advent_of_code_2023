from collections.abc import Iterator
from typing import Any, NamedTuple
from aoc.utils.common import Coord, a_star

from aoc.utils.contents import PuzzleInput


def heuristic_old(current: Coord, goal: Coord) -> float:
    # Manhattan distance where each step is cost 1
    height = abs(current.y - goal.y)
    width = abs(current.x - goal.x)
    return height + width


def straight(paths: dict[Coord, Coord], current: Coord, last: Coord) -> int:
    # Test x's
    xs = abs(current.x - last.x)
    if xs > 0:
        token = last
        while True:
            token = paths.get(token)
            if not token:
                break
            if token.y != current.y:
                break

            xs += 1

    # Test y's
    ys = abs(current.y - last.y)
    if ys > 0:
        token = last
        while True:
            token = paths.get(token)
            if not token:
                break
            if token.x != current.x:
                break

            ys += 1

    return max(xs, ys) - 1


class CostFunctionOld:
    def __init__(self, lava_map: list[list[int]]) -> None:
        self.lava_map = lava_map

    def __call__(self, paths: dict[Coord, Coord], current: Coord, last: Coord) -> float:
        straights = straight(paths, current, last)
        return float(self.lava_map[current.y][current.x]) + (straights / 100)


class NeighborFunctionOld:
    def __init__(self, lava_map: list[list[int]]) -> None:
        self.lava_map = lava_map

    def disallowed_next(
        self, current: Coord, paths: dict[Coord, Coord], lookback=3
    ) -> Coord | None:
        path = [current]
        token = current
        while True:
            token = paths.get(token)
            if token is None:
                break
            path.append(token)

        if len(path) >= lookback + 1:
            possible_straight = set(path[: lookback + 1])
            xs = {coord.x for coord in possible_straight}
            ys = {coord.y for coord in possible_straight}
            lengths = {len(xs), len(ys)}
            if lengths == {1, lookback + 1}:
                x_diff = current.x - path[1].x
                y_diff = current.y - path[1].y
                return Coord(current.x + x_diff, current.y + y_diff)

    def __call__(self, current: Coord, paths: dict[Coord, Coord]) -> Iterator[Coord]:
        all_neighbors = {
            Coord(current.x + 1, current.y),
            Coord(current.x - 1, current.y),
            Coord(current.x, current.y + 1),
            Coord(current.x, current.y - 1),
        }

        if paths.get(current):
            all_neighbors.remove(paths[current])

        straight = self.disallowed_next(current, paths)
        if straight:
            all_neighbors.remove(straight)

        for neighbor in all_neighbors:
            if neighbor.x < 0 or neighbor.x >= len(self.lava_map[0]):
                continue
            if neighbor.y < 0 or neighbor.y >= len(self.lava_map):
                continue
            yield neighbor


class Step(NamedTuple):
    coord: Coord
    straight: int


def heuristic(current: Step, goal: Step) -> float:
    # Manhattan distance where each step is cost 1
    height = abs(current.coord.y - goal.coord.y)
    width = abs(current.coord.x - goal.coord.x)
    return height + width


class CostFunction:
    def __init__(self, lava_map: list[list[int]]) -> None:
        self.lava_map = lava_map

    def __call__(self, paths: dict[Step, Step], current: Step, last: Step) -> float:
        return float(self.lava_map[current.coord.y][current.coord.x])


class NeighborFunction:
    def __init__(self, lava_map: list[list[int]]) -> None:
        self.lava_map = lava_map

    def __call__(self, current: Step, paths: dict[Step, Step]) -> Iterator[Step]:
        last = paths.get(current)
        if last is None:
            all_neighbors = {
                Step(Coord(current.coord.x + 1, current.coord.y), 1),
                Step(Coord(current.coord.x - 1, current.coord.y), 1),
                Step(Coord(current.coord.x, current.coord.y + 1), 1),
                Step(Coord(current.coord.x, current.coord.y - 1), 1),
            }
        else:
            all_neighbors = set()
            if last.coord.x == current.coord.x:
                y_diff = current.coord.y - last.coord.y
                all_neighbors.add(Step(Coord(current.coord.x - 1, current.coord.y), 1))
                all_neighbors.add(Step(Coord(current.coord.x + 1, current.coord.y), 1))
                if current.straight < 3:
                    all_neighbors.add(
                        Step(
                            Coord(current.coord.x, current.coord.y + y_diff),
                            current.straight + 1,
                        )
                    )
            elif last.coord.y == current.coord.y:
                x_diff = current.coord.x - last.coord.x
                all_neighbors.add(Step(Coord(current.coord.x, current.coord.y - 1), 1))
                all_neighbors.add(Step(Coord(current.coord.x, current.coord.y + 1), 1))
                if current.straight < 3:
                    all_neighbors.add(
                        Step(
                            Coord(current.coord.x + x_diff, current.coord.y),
                            current.straight + 1,
                        )
                    )
            else:
                raise ValueError()

        for neighbor in all_neighbors:
            if neighbor.coord.x < 0 or neighbor.coord.x >= len(self.lava_map[0]):
                continue
            if neighbor.coord.y < 0 or neighbor.coord.y >= len(self.lava_map):
                continue
            yield neighbor


def part_1(puzzle: PuzzleInput) -> Any:
    lava_map: list[list[int]] = []
    for line in puzzle.lines:
        lava_map.append([int(x) for x in line])

    start = Step(Coord(0, 0), straight=0)
    goal = Step(Coord(len(lava_map[0]) - 1, len(lava_map) - 1), straight=1)
    _, cost = a_star(
        start, goal, heuristic, CostFunction(lava_map), NeighborFunction(lava_map)
    )
    # Lower than 1020
    return cost


def part_2(puzzle: PuzzleInput) -> Any:
    return 0
