from collections.abc import Iterator
from collections import defaultdict
from typing import NamedTuple, Protocol, TypeVar
import heapq


class Coord(NamedTuple):
    x: int
    y: int


T = TypeVar("T")


class Heuristic(Protocol):
    def __call__(self, current: T, goal: T) -> float:
        ...


class Cost(Protocol):
    def __call__(self, last: T, current: T) -> float:
        ...


class Neighbors(Protocol):
    def __call__(self, current: T) -> Iterator[T]:
        ...


def _reconstruct_path(paths: dict[T, T], goal: T) -> list[T]:
    path = [goal]
    current = goal
    while current in paths.keys():
        path.insert(0, paths[current])
        current = paths[current]
    return path


def a_star(
    start: T, goal: T, heuristic: Heuristic, cost_func: Cost, next_func: Neighbors
) -> tuple[list[T], float]:
    frontier: list[tuple[float, T]] = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    paths: dict[T, T] = {}
    cheapest_path: dict[T, float] = defaultdict(lambda: float("inf"))
    cheapest_path[start] = 0.0

    while len(frontier) > 0:
        _, current = heapq.heappop(frontier)
        if current == goal:
            path = _reconstruct_path(paths, goal)
            return path, cheapest_path[current]

        for neighbor in next_func(current):
            new_cost = cheapest_path[current] + cost_func(current, neighbor)

            if new_cost < cheapest_path[neighbor]:
                paths[neighbor] = current
                cheapest_path[neighbor] = new_cost
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    raise ValueError("Could not find a path.")
