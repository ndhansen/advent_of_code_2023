from typing import Any

from aoc.utils.common import Coord
from aoc.utils.contents import PuzzleInput


def get_start(puzzle: list[str]) -> Coord:
    y = 0
    for line in puzzle:
        if line.find("S") != -1:
            return Coord(line.find("S"), y)
        y += 1
    raise ValueError()


def get_start_neightbors(start: Coord, puzzle: list[str]) -> tuple[Coord, Coord]:
    neighbors: list[Coord] = []
    left_coord = Coord(start.x - 1, start.y)
    left = puzzle[start.y][start.x - 1]
    if left in "-LF":
        neighbors.append(left_coord)
    right_coord = Coord(start.x + 1, start.y)
    right = puzzle[start.y][start.x + 1]
    if right in "-J7":
        neighbors.append(right_coord)
    top_coord = Coord(start.x, start.y - 1)
    top = puzzle[start.y - 1][start.x]
    if top in "|F7":
        neighbors.append(top_coord)
    bottom_coord = Coord(start.x, start.y + 1)
    bottom = puzzle[start.y + 1][start.x]
    if bottom in "|JL":
        neighbors.append(bottom_coord)

    assert len(neighbors) == 2
    return (neighbors[0], neighbors[1])


def next_pipe(current: Coord, previous: Coord, puzzle: list[str]) -> Coord:
    neighbors: list[Coord]
    match puzzle[current.y][current.x]:
        case "|":
            neighbors = [
                Coord(current.x, current.y - 1),
                Coord(current.x, current.y + 1),
            ]
        case "-":
            neighbors = [
                Coord(current.x - 1, current.y),
                Coord(current.x + 1, current.y),
            ]
        case "L":
            neighbors = [
                Coord(current.x, current.y - 1),
                Coord(current.x + 1, current.y),
            ]
        case "J":
            neighbors = [
                Coord(current.x, current.y - 1),
                Coord(current.x - 1, current.y),
            ]
        case "7":
            neighbors = [
                Coord(current.x, current.y + 1),
                Coord(current.x - 1, current.y),
            ]
        case "F":
            neighbors = [
                Coord(current.x, current.y + 1),
                Coord(current.x + 1, current.y),
            ]
        case _:
            raise ValueError()

    neighbors.remove(previous)
    assert len(neighbors) == 1
    return neighbors[0]


def get_path(start: Coord, puzzle: list[str]) -> list[Coord]:
    neighbors = get_start_neightbors(start, puzzle)
    cur_pipe = neighbors[0]
    last_pipe = start
    path: list[Coord] = [start, cur_pipe]
    while True:
        following_pipe = next_pipe(cur_pipe, last_pipe, puzzle)
        if following_pipe == start:
            return path
        path.append(following_pipe)

        cur_pipe = path[-1]
        last_pipe = path[-2]


def part_1(puzzle: PuzzleInput) -> Any:
    start = get_start(puzzle.lines)
    steps = len(get_path(start, puzzle.lines))
    return (steps + 1) // 2


def neighbor_fields(loc: Coord, pipe: set[Coord], puzzle: list[str]) -> set[Coord]:
    seen = set()
    to_explore = [loc]
    while len(to_explore) > 0:
        current = to_explore.pop()
        seen.add(current)
        for x in range(-1, 2):
            for y in range(-1, 2):
                neighbor = Coord(current.x + x, current.y + y)
                if neighbor.x < 0 or neighbor.x >= len(puzzle[0]):
                    continue
                if neighbor.y < 0 or neighbor.y >= len(puzzle):
                    continue
                if neighbor in pipe:
                    continue
                if neighbor in seen:
                    continue
                to_explore.append(neighbor)
    return seen


def touches_edge(fields: set[Coord], puzzle: list[str]) -> bool:
    for field in fields:
        if field.x == 0 or field.x == len(puzzle[0]) - 1:
            return True
        if field.y == 0 or field.y == len(puzzle) - 1:
            return True
    return False


def not_working(puzzle: PuzzleInput) -> Any:
    start = get_start(puzzle.lines)
    pipe = set(get_path(start, puzzle.lines))
    enclosed = set()
    exposed = set()
    for y in range(len(puzzle.lines)):
        for x in range(len(puzzle.lines[0])):
            current = Coord(x, y)
            if current in exposed:
                continue
            if current in enclosed:
                continue
            if current in pipe:
                continue

            fields = neighbor_fields(current, pipe, puzzle.lines)
            if touches_edge(fields, puzzle.lines):
                exposed.update(fields)
            else:
                enclosed.update(fields)

    for x in enclosed:
        print(x)
    return len(enclosed)


def get_sides(
    pipe: list[Coord], index: int, puzzle: list[str]
) -> tuple[list[Coord], list[Coord]]:
    # Return type is "outside/inside", when going clockwise
    last_index = (index - 1) % len(pipe)
    next_index = (index + 1) % len(pipe)
    # Straight
    if puzzle[pipe[index].y][pipe[index].x] == "-":
        up = Coord(pipe[index].x, pipe[index].y - 1)
        down = Coord(pipe[index].x, pipe[index].y + 1)
        # left to right
        if pipe[last_index].x < pipe[next_index].x:
            return ([up], [down])
        # right to left
        else:
            return ([down], [up])

    if puzzle[pipe[index].y][pipe[index].x] == "|":
        right = Coord(pipe[index].x + 1, pipe[index].y)
        left = Coord(pipe[index].x - 1, pipe[index].y)
        # top to bottom
        if pipe[last_index].y < pipe[next_index].y:
            return ([right], [left])
        # bottom to top
        else:
            return ([left], [right])

    if puzzle[pipe[index].y][pipe[index].x] == "J":
        nook = []
        edge = [
            Coord(pipe[index].x + 1, pipe[index].y),
            Coord(pipe[index].x + 1, pipe[index].y + 1),
            Coord(pipe[index].x, pipe[index].y + 1),
        ]
        # top to left
        if pipe[last_index].y < pipe[next_index].y:
            return (edge, nook)
        # left to top
        else:
            return (nook, edge)

    if puzzle[pipe[index].y][pipe[index].x] == "L":
        nook = []
        edge = [
            Coord(pipe[index].x - 1, pipe[index].y),
            Coord(pipe[index].x - 1, pipe[index].y + 1),
            Coord(pipe[index].x, pipe[index].y + 1),
        ]
        # top to right
        if pipe[last_index].y < pipe[next_index].y:
            return (nook, edge)
        # right to top
        else:
            return (edge, nook)

    if puzzle[pipe[index].y][pipe[index].x] == "F":
        nook = []
        edge = [
            Coord(pipe[index].x - 1, pipe[index].y),
            Coord(pipe[index].x - 1, pipe[index].y - 1),
            Coord(pipe[index].x, pipe[index].y - 1),
        ]
        # bottom to right
        if pipe[last_index].y > pipe[next_index].y:
            return (edge, nook)
        # right to bottom
        else:
            return (nook, edge)

    if puzzle[pipe[index].y][pipe[index].x] == "7":
        nook = []
        edge = [
            Coord(pipe[index].x + 1, pipe[index].y),
            Coord(pipe[index].x + 1, pipe[index].y - 1),
            Coord(pipe[index].x, pipe[index].y - 1),
        ]
        # left to bottom
        if pipe[last_index].y < pipe[next_index].y:
            return (edge, nook)
        # bottom to left
        else:
            return (nook, edge)

    raise ValueError()


def part_2(puzzle: PuzzleInput) -> Any:
    start = get_start(puzzle.lines)
    pipe = get_path(start, puzzle.lines)
    first_side = set()
    second_side = set()
    for i in range(1, len(pipe)):
        second_sides, first_sides = get_sides(pipe, i, puzzle.lines)
        first_side.update(first_sides)
        second_side.update(second_sides)

    inner_sides = first_side if len(first_side) < len(second_side) else second_side

    for inside_field in inner_sides.copy():
        if inside_field in pipe:
            inner_sides.remove(inside_field)

    all_inside = set()
    for inside_field in inner_sides:
        all_inside.update(neighbor_fields(inside_field, set(pipe), puzzle.lines))

    return len(all_inside)
