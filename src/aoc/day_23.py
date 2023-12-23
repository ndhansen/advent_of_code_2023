import functools
import itertools
from collections import defaultdict
from typing import Any

from aoc.utils.common import Coord
from aoc.utils.contents import PuzzleInput


class CostFunc:
    def __call__(self, current: Coord, last: Coord) -> int:
        x_diff = abs(current.x - last.x)
        y_diff = abs(current.y - last.y)
        return x_diff + y_diff


class NeighborFunc:
    def __init__(self, trails: tuple[str, ...], slippery: bool = True) -> None:
        self.trails = trails
        self.slippery = slippery

    @functools.lru_cache(maxsize=None)
    def __call__(self, current: Coord, paths: tuple[Coord, ...]) -> list[Coord]:
        neighbors = []
        for x, y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_loc = Coord(current.x + x, current.y + y)
            if new_loc in paths:
                continue
            if new_loc.y < 0 or new_loc.y > len(self.trails) - 1:
                continue
            if self.trails[new_loc.y][new_loc.x] == ".":
                neighbors.append(new_loc)
            elif (
                self.trails[new_loc.y][new_loc.x] == ">"
                and x == 1
                or self.trails[new_loc.y][new_loc.x] == "<"
                and x == -1
                or self.trails[new_loc.y][new_loc.x] == "v"
                and y == 1
            ):
                if self.slippery:
                    neighbors.append(Coord(new_loc.x + x, new_loc.y + y))
                else:
                    neighbors.append(new_loc)
            else:
                continue
        return neighbors


def _path_cost(trails: tuple[str, ...], paths: list[Coord]) -> int:
    cost = CostFunc()
    total = 0
    for first, second in itertools.pairwise(paths):
        total += cost(first, second)

    return total


@functools.lru_cache(maxsize=None)
def get_neighbors(
    junction: Coord,
    current: Coord,
    trails: tuple[str, ...],
    neighbor_func: NeighborFunc,
) -> tuple[Coord, int]:
    path = [junction, current]
    while True:
        if current.y == 0:
            return Coord(1, 0), _path_cost(trails, path)
        next_locs = neighbor_func(current, tuple(path))
        if len(next_locs) == 0:
            raise ValueError()
        if len(next_locs) == 1:
            path.append(next_locs[0])
            current = next_locs[0]

            if current.y == len(trails) - 1:
                return next_locs[0], _path_cost(trails, path)

            continue
        else:
            return current, _path_cost(trails, path)


def get_start_end(lines: list[str]) -> tuple[Coord, Coord]:
    start = Coord(lines[0].index("."), 0)
    end = Coord(lines[-1].index("."), len(lines) - 1)
    return start, end


def part_1(puzzle: PuzzleInput) -> Any:
    start, end = get_start_end(puzzle.lines)
    graph, connections = get_junctions(start, end, tuple(puzzle.lines))
    cost = dfs(graph, connections, 0, 0, start, end, set())
    return cost


def get_junctions(
    start: Coord, end: Coord, trails: tuple[str, ...]
) -> tuple[dict[tuple[Coord, Coord], int], dict[Coord, set[Coord]]]:
    neighbor = NeighborFunc(trails, True)
    frontier = {start}
    seen = set()
    paths = {}
    connections = defaultdict(set)
    while len(frontier) > 0:
        current = frontier.pop()
        if current in seen:
            continue
        for next_loc in neighbor(current, ()):
            junction, steps = get_neighbors(current, next_loc, trails, neighbor)
            connections[current].add(junction)
            paths[(current, junction)] = steps
            paths[(junction, current)] = steps
            if junction not in seen:
                if junction != end:
                    frontier.add(junction)
        seen.add(current)

    return paths, connections


def dfs(
    graph: dict[tuple[Coord, Coord], int],
    connections: dict[Coord, set[Coord]],
    dist: int,
    best: int,
    start: Coord,
    end: Coord,
    seen: set[Coord],
) -> int:
    if start == end:
        return dist
    if start in seen:
        return best
    highest = []
    seen.add(start)
    for connection in connections[start]:
        to_connection = graph[(start, connection)]
        highest.append(
            dfs(
                graph,
                connections,
                to_connection + dist,
                best,
                connection,
                end,
                seen.copy(),
            )
        )

    return max(highest)


def part_2(puzzle: PuzzleInput) -> Any:
    start, end = get_start_end(puzzle.lines)
    test = puzzle.lines
    test_2 = []
    for line in test:
        test_2.append(line.replace(">", ".").replace("v", ".").replace("<", "."))

    graph, connections = get_junctions(start, end, tuple(test_2))
    cost = dfs(graph, connections, 0, 0, start, end, set())
    return cost
