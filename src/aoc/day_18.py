from collections import defaultdict
from enum import Enum, IntEnum, auto
import itertools
from typing import Any, NamedTuple
from aoc.utils.common import Coord, Direction

from aoc.utils.contents import PuzzleInput

from tqdm import tqdm


class Instruction(NamedTuple):
    direction: Direction
    distance: int
    color: str


class Side(IntEnum):
    INSIDE = auto()
    OUTSIDE = auto()


class Line(NamedTuple):
    start: Coord
    end: Coord
    side: Side


def parse_input(puzzle: str) -> Instruction:
    direction: Direction
    dir_raw, dist_raw, color = puzzle.split(" ")
    match dir_raw:
        case "R":
            direction = Direction.EAST
        case "L":
            direction = Direction.WEST
        case "U":
            direction = Direction.NORTH
        case "D":
            direction = Direction.SOUTH
        case _:
            raise ValueError()

    return Instruction(direction, int(dist_raw), color)


def points_in_between(last: Coord, current: Coord) -> list[Coord]:
    if last.x == current.x:
        step = 1 if last.y < current.y else -1
        points = []
        for y in range(last.y, current.y, step):
            points.append(Coord(current.x, y))
        return points
    if last.y == current.y:
        step = 1 if last.x < current.x else -1
        points = []
        for x in range(last.x, current.x, step):
            points.append(Coord(x, current.y))
        return points
    raise ValueError()


def next_point(current: Coord, instruction: Instruction) -> Coord:
    x, y = 0, 0
    match instruction.direction:
        case Direction.NORTH:
            y = -instruction.distance
        case Direction.SOUTH:
            y = instruction.distance
        case Direction.EAST:
            x = instruction.distance
        case Direction.WEST:
            x = -instruction.distance
    return Coord(current.x + x, current.y + y)


def get_inside_perimiter(
    start: Coord, perimiter: set[Coord], limit=1000
) -> set[Coord] | None:
    frontier = [start]
    seen = {start}
    while len(frontier) > 0:
        current = frontier.pop()
        neighbors = {
            Coord(current.x, current.y + 1),
            Coord(current.x, current.y - 1),
            Coord(current.x - 1, current.y),
            Coord(current.x + 1, current.y),
        }
        unseen = neighbors - seen
        unseen -= perimiter
        frontier.extend(unseen)
        seen.update(unseen)
        if len(seen) > limit:
            return None
    return seen


def interior(instructions: list[Instruction]) -> int:
    last = Coord(0, 0)
    loop = {last}

    for instruction in instructions:
        next_coord = next_point(last, instruction)
        loop.update(points_in_between(last, next_coord))
        last = next_coord

    possibly_inside = [Coord(-1, -1), Coord(1, 1), Coord(-1, 1), Coord(1, -1)]
    interior = None
    for coord in possibly_inside:
        maybe_interior = get_inside_perimiter(coord, loop, limit=100000)
        if maybe_interior:
            interior = maybe_interior

    if not interior:
        raise ValueError()

    return len(interior) + len(loop)


def part_1(puzzle: PuzzleInput) -> Any:
    instructions = list(map(parse_input, puzzle.lines))
    return interior(instructions)


def parse_input_2(line: str) -> Instruction:
    _, __, color = line.split(" ")
    color = color.strip("(#)")
    dist_raw, dir_raw = color[:-1], color[-1]
    distance = int(dist_raw, base=16)
    direction: Direction
    match dir_raw:
        case "0":
            direction = Direction.EAST
        case "1":
            direction = Direction.SOUTH
        case "2":
            direction = Direction.WEST
        case "3":
            direction = Direction.NORTH
        case _:
            raise ValueError()
    return Instruction(direction, distance, "")


def coordinates_from_instructions(instructions: list[Instruction]) -> list[Coord]:
    coords = [Coord(0, 0)]
    for instruction in instructions:
        x_diff, y_diff = 0, 0
        match instruction.direction:
            case Direction.NORTH:
                y_diff = -instruction.distance
            case Direction.SOUTH:
                y_diff = instruction.distance
            case Direction.WEST:
                x_diff = -instruction.distance
            case Direction.EAST:
                x_diff = instruction.distance
            case _:
                raise ValueError()

        x = coords[-1].x + x_diff
        y = coords[-1].y + y_diff
        coords.append(Coord(x, y))

    assert coords[-1] == Coord(0, 0)
    return coords


def determinant(one: Coord, two: Coord) -> int:
    return (one.x * two.y) - (one.y * two.x)


def shoelace(coords: list[Coord]) -> int:
    total = 0
    for left, right in itertools.pairwise(coords):
        total += determinant(left, right)

    return total


def perimiter(instructions: list[Instruction]) -> int:
    return sum(instruction.distance for instruction in instructions)


def part_1(puzzle: PuzzleInput) -> Any:
    instructions = list(map(parse_input, puzzle.lines))
    coordinates = coordinates_from_instructions(instructions)
    interior_size = shoelace(coordinates) // 2
    perimiter_size = perimiter(instructions)
    return interior_size + (perimiter_size // 2) + 1


def part_2(puzzle: PuzzleInput) -> Any:
    instructions = list(map(parse_input_2, puzzle.lines))
    coordinates = coordinates_from_instructions(instructions)
    interior_size = shoelace(coordinates) // 2
    perimiter_size = perimiter(instructions)
    return interior_size + (perimiter_size // 2) + 1
