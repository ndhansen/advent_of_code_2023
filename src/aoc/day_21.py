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
    seen = {start}
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
            Coord(location.x+1, location.y),
            Coord(location.x-1, location.y),
            Coord(location.x, location.y+1),
            Coord(location.x, location.y-1),
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
            frontier.add((step_count+1, neighbor))

    return len(fields_at_step)


def part_1(puzzle: PuzzleInput) -> Any:
    start = parse_input(puzzle.lines)
    return get_reachable(64, start, puzzle.lines)


def part_2(puzzle: PuzzleInput) -> Any:
    return 0
