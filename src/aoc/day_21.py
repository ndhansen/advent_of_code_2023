import functools
from typing import Any

from aoc.utils.common import Coord
from aoc.utils.contents import PuzzleInput


def parse_input(lines: list[str]) -> Coord:
    start = None
    y = 0
    for line in lines:
        if "S" in line:
            x = line.find("S")
            start = Coord(x, y)
            break
        y += 1

    if not start:
        raise ValueError()

    return start


def get_reachable(steps: int, start: Coord, garden: list[str]) -> int:
    fields_at_step = set()
    frontier: set[tuple[int, Coord]] = {(0, start)}
    while len(frontier) > 0:
        step_count, location = frontier.pop()

        if step_count == steps:
            fields_at_step.add(location)
            continue

        if step_count > steps:
            raise ValueError()

        potential_neighbors: set[Coord] = {
            Coord(location.x + 1, location.y),
            Coord(location.x - 1, location.y),
            Coord(location.x, location.y + 1),
            Coord(location.x, location.y - 1),
        }

        neighbors: set[Coord] = set()

        for neighbor in potential_neighbors:
            if neighbor.x < 0 or neighbor.x >= len(garden[0]):
                continue
            if neighbor.y < 0 or neighbor.y >= len(garden):
                continue
            if garden[neighbor.y][neighbor.x] == "#":
                continue
            neighbors.add(neighbor)

        for neighbor in neighbors:
            frontier.add((step_count + 1, neighbor))

    return len(fields_at_step)


@functools.lru_cache(maxsize=None)
def get_neighbors(coord: Coord, garden: tuple[str, ...]) -> list[Coord]:
    potential_neighbors: list[Coord] = [
        Coord(coord.x + 1, coord.y),
        Coord(coord.x - 1, coord.y),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x, coord.y - 1),
    ]

    neighbors = []
    for neighbor in potential_neighbors:
        if garden[neighbor.y % len(garden)][neighbor.x % len(garden[0])] != "#":
            neighbors.append(neighbor)

    return neighbors


def part_1(puzzle: PuzzleInput) -> Any:
    start = parse_input(puzzle.lines)
    frontier = {start}
    frontier_size = len(frontier)
    seen = {start}
    garden = tuple(puzzle.lines)
    growth = []
    fields_at_step = [len(seen)]

    for _ in range(64):
        frontier = get_next_frontier(frontier, seen, garden)
        seen.update(frontier)
        growth.append(len(frontier) - frontier_size)
        frontier_size = len(frontier)
        fields_at_step.append(len(frontier))

    total = 0
    for i in range(0, 65, 2):
        total += fields_at_step[i]
    return total


def get_reachable_coords(
    start: Coord, steps: int, garden: tuple[str, ...]
) -> dict[Coord, int]:
    frontier: set[Coord] = {start}
    distances: dict[Coord, int] = {start: 0}
    for dist in range(1, steps + 1):
        next_frontier = set()
        while len(frontier) > 0:
            coord = frontier.pop()
            x_offset = (coord.x // len(garden[0])) * len(garden[0])
            y_offset = (coord.y // len(garden)) * len(garden)
            central_neighbors = get_neighbors(
                Coord(coord.x % len(garden[0]), coord.y % len(garden)), garden
            )
            for central_neighbor in central_neighbors:
                neighbor = Coord(
                    central_neighbor.x + x_offset, central_neighbor.y + y_offset
                )
                if neighbor not in distances:
                    next_frontier.add(neighbor)
                    distances[neighbor] = dist
        frontier = next_frontier.copy()

    return distances


def get_fields_up_to(distance: dict[Coord, int], at: int) -> int:
    return len([x for x in distance.values() if x <= at and x % 2 == at % 2])


def get_next_frontier(
    current: set[Coord], seen: set[Coord], garden: tuple[str, ...]
) -> set[Coord]:
    frontier: set[Coord] = set()
    for coord in current:
        x_offset = (coord.x // len(garden[0])) * len(garden[0])
        y_offset = (coord.y // len(garden)) * len(garden)
        central_neighbors = get_neighbors(
            Coord(coord.x % len(garden[0]), coord.y % len(garden)), garden
        )
        for central_neighbor in central_neighbors:
            neighbor = Coord(
                central_neighbor.x + x_offset, central_neighbor.y + y_offset
            )
            if neighbor not in seen:
                frontier.add(neighbor)

    return frontier


def part_2(puzzle: PuzzleInput) -> Any:
    steps = 26501365
    start = parse_input(puzzle.lines)
    garden = tuple(puzzle.lines)

    reachable = get_reachable_coords(start, 65 + (2 * 131), garden)
    x_1 = get_fields_up_to(reachable, 65)
    x_2 = get_fields_up_to(reachable, 65 + 131)
    x_3 = get_fields_up_to(reachable, 65 + (2 * 131))

    # Logic was shamelessly stolen from somewhere on reddit I think.
    # I had my own nice solution with derivitives, but there's a bug in it
    # somewhere and I can't find it now.
    c = x_1
    a = x_3 - 2 * x_2 + x_1
    b = x_2 - x_1 - a
    n = (steps - 65) // 131
    return a * n**2 + b * n + c
