from typing import Any
from enum import Enum, auto

from aoc.utils.contents import PuzzleInput
from aoc.utils.common import Coord, Direction


class Mirror(Enum):
    DIAG_TL_BR = auto()
    DIAG_BL_TR = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()


def parse_input(puzzle: list[str]) -> dict[Coord, Mirror]:
    positions = {}
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            match char:
                case "\\":
                    positions[Coord(x, y)] = Mirror.DIAG_TL_BR
                case "/":
                    positions[Coord(x, y)] = Mirror.DIAG_BL_TR
                case "-":
                    positions[Coord(x, y)] = Mirror.HORIZONTAL
                case "|":
                    positions[Coord(x, y)] = Mirror.VERTICAL
    return positions


def get_energized(
    puzzle: list[str],
    mirrors: dict[Coord, Mirror],
    start: tuple[Coord, Direction] = (Coord(0, 0), Direction.EAST),
):
    path: set[tuple[Coord, Direction]] = set()
    energized: set[Coord] = set()
    to_explore: list[tuple[Coord, Direction]] = [start]
    while len(to_explore) > 0:
        place, direction = to_explore.pop()
        # Check if it's out of bounds
        if place.x < 0 or place.x >= len(puzzle[0]):
            continue
        if place.y < 0 or place.y >= len(puzzle[0]):
            continue

        # Check if we've already been here before
        if (place, direction) in path:
            continue

        # Add it to the path / energized set
        energized.add(place)
        path.add((place, direction))

        # Check what the next place to go is
        if place not in mirrors:
            to_explore.append((place.add(direction.value), direction))
            continue

        match mirrors[place]:
            case Mirror.DIAG_TL_BR:
                new_direction: Direction
                match direction:
                    case Direction.EAST:
                        new_direction = Direction.SOUTH
                    case Direction.NORTH:
                        new_direction = Direction.WEST
                    case Direction.WEST:
                        new_direction = Direction.NORTH
                    case Direction.SOUTH:
                        new_direction = Direction.EAST
                to_explore.append((place.add(new_direction.value), new_direction))
            case Mirror.DIAG_BL_TR:
                new_direction: Direction
                match direction:
                    case Direction.EAST:
                        new_direction = Direction.NORTH
                    case Direction.NORTH:
                        new_direction = Direction.EAST
                    case Direction.WEST:
                        new_direction = Direction.SOUTH
                    case Direction.SOUTH:
                        new_direction = Direction.WEST
                to_explore.append((place.add(new_direction.value), new_direction))
            case Mirror.HORIZONTAL:
                if direction in {Direction.EAST, Direction.WEST}:
                    to_explore.append((place.add(direction.value), direction))
                else:
                    to_explore.append((place.add(Direction.WEST.value), Direction.WEST))
                    to_explore.append((place.add(Direction.EAST.value), Direction.EAST))
            case Mirror.VERTICAL:
                if direction in {Direction.NORTH, Direction.SOUTH}:
                    to_explore.append((place.add(direction.value), direction))
                else:
                    to_explore.append(
                        (place.add(Direction.NORTH.value), Direction.NORTH)
                    )
                    to_explore.append(
                        (place.add(Direction.SOUTH.value), Direction.SOUTH)
                    )
            case _:
                raise ValueError()

    return len(energized)


def part_1(puzzle: PuzzleInput) -> Any:
    mirrors = parse_input(puzzle.lines)
    return get_energized(puzzle.lines, mirrors)


def get_max_energized(puzzle: list[str], mirrors: dict[Coord, Mirror]):
    starts = []
    for y in range(len(puzzle)):
        starts.append((Coord(0, y), Direction.EAST))
        starts.append((Coord(len(puzzle[0]) - 1, y), Direction.WEST))
    for x in range(len(puzzle[0])):
        starts.append((Coord(x, 0), Direction.SOUTH))
        starts.append((Coord(x, len(puzzle) - 1), Direction.NORTH))

    energized = []
    for start in starts:
        energized.append(get_energized(puzzle, mirrors, start))
    return max(energized)


def part_2(puzzle: PuzzleInput) -> Any:
    mirrors = parse_input(puzzle.lines)
    return get_max_energized(puzzle.lines, mirrors)
