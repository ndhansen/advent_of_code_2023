from collections import defaultdict
import itertools
from typing import Any, NamedTuple
from aoc.utils.common import Coord, Direction

from aoc.utils.contents import PuzzleInput

from tqdm import tqdm


class Instruction(NamedTuple):
    direction: Direction
    distance: int
    color: str


class Line(NamedTuple):
    start: Coord
    end: Coord


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
    return Coord(current.x - x, current.y - y)


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


def dist_between_points(last: Coord, current: Coord) -> int:
    if last.x == current.x:
        return abs(last.y - current.y)
    if last.y == current.y:
        return abs(last.x - current.x)
    raise ValueError()


def get_crossing_points(y: int, lines: list[Line]) -> list[int]:
    points = []
    for line in lines:
        if y == line.start.y and y == line.end.y:
            points.extend([line.start.x, line.end.x])
            continue
        line_smallest = min(line.start.y, line.end.y)
        line_biggest = max(line.start.y, line.end.y)
        if y > line_smallest and y < line_biggest:
            points.extend([line.start.x, line.start.x])
    return sorted(points)


def interior_size(points: list[int]) -> int:
    inside = 0
    for point_group in itertools.batched(points, 4):
        assert len(point_group) % 2 == 0
        if len(point_group) == 2:
            inside += (point_group[1] - point_group[0]) + 1
            continue
        inside += (point_group[3] - point_group[0]) + 1
        # if len(point_group) != 4:
        #     continue
        # inside += (point_group[2] - point_group[1]) - 1

    return inside


def interior_2(instructions: list[Instruction]) -> int:
    lines: list[Line] = []
    last = Coord(0, 0)
    perimiter_length = 0

    for instruction in instructions:
        next_coord = next_point(last, instruction)
        lines.append(Line(last, next_coord))
        perimiter_length += dist_between_points(last, next_coord)
        last = next_coord

    largest_y, smallest_y = 0, 0
    for line in lines:
        line_smallest = min(line.start.y, line.end.y)
        line_biggest = max(line.start.y, line.end.y)
        if line_smallest < smallest_y:
            smallest_y = line_smallest
        if line_biggest > largest_y:
            largest_y = line_biggest

    import pudb

    pudb.set_trace()
    inside_size = 0
    for y in tqdm(range(smallest_y, largest_y + 1)):
        points = get_crossing_points(y, lines)
        inside_size += interior_size(points)

    # return inside_size + perimiter_length
    return inside_size


def part_2(puzzle: PuzzleInput) -> Any:
    instructions = list(map(parse_input, puzzle.lines))
    return interior_2(instructions)
