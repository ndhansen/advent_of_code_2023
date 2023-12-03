from collections import defaultdict
from typing import Any
import re
from aoc.utils.common import Coord

from aoc.utils.contents import PuzzleInput


def number_adjacent_to_symbol(left: Coord, right: Coord, puzzle: list[str]) -> bool:
    if (
        puzzle[left.y][left.x - 1] != "."
        or puzzle[left.y - 1][left.x - 1] != "."
        or puzzle[left.y + 1][left.x - 1] != "."
        or puzzle[left.y][right.x + 1] != "."
        or puzzle[left.y - 1][right.x + 1] != "."
        or puzzle[left.y + 1][right.x + 1] != "."
    ):
        return True

    for x in range(left.x, right.x + 1):
        if puzzle[left.y - 1][x] != "." or puzzle[left.y + 1][x] != ".":
            return True

    return False


def get_number_indexes(lines: list[str]) -> list[tuple[Coord, Coord, int]]:
    number_positions = []
    y = 0
    for line in lines:
        for num_match in re.finditer(r"\d+", line):
            pos = num_match.span()
            first = Coord(pos[0], y)
            second = Coord(pos[1] - 1, y)
            number_positions.append((first, second, int(num_match.group())))
        y += 1

    return number_positions


def pad(puzzle: PuzzleInput) -> list[str]:
    lines = puzzle.lines
    i = 0
    for i in range(len(lines)):
        lines[i] = "." + lines[i] + "."
    lines.insert(0, "." * len(lines[0]))
    lines.append("." * len(lines[1]))
    return lines


def part_1(puzzle: PuzzleInput) -> Any:
    # Pad the puzzle with a border
    lines = pad(puzzle)

    numbers = get_number_indexes(lines)
    total = 0
    for left, right, value in numbers:
        if number_adjacent_to_symbol(left, right, lines):
            total += value

    return total


def number_adjacent_to_star(
    left: Coord, right: Coord, puzzle: list[str]
) -> Coord | None:
    if puzzle[left.y][left.x - 1] == "*":
        return Coord(left.x - 1, left.y)
    if puzzle[left.y - 1][left.x - 1] == "*":
        return Coord(left.x - 1, left.y - 1)
    if puzzle[left.y + 1][left.x - 1] == "*":
        return Coord(left.x - 1, left.y + 1)
    if puzzle[left.y][right.x + 1] == "*":
        return Coord(right.x + 1, left.y)
    if puzzle[left.y - 1][right.x + 1] == "*":
        return Coord(right.x + 1, left.y - 1)
    if puzzle[left.y + 1][right.x + 1] == "*":
        return Coord(right.x + 1, left.y + 1)

    for x in range(left.x, right.x + 1):
        if puzzle[left.y - 1][x] != ".":
            return Coord(x, left.y - 1)
        if puzzle[left.y + 1][x] != ".":
            return Coord(x, left.y + 1)


def part_2(puzzle: PuzzleInput) -> Any:
    lines = pad(puzzle)
    gears = defaultdict(list)
    numbers = get_number_indexes(lines)
    for left, right, value in numbers:
        gear = number_adjacent_to_star(left, right, lines)
        if gear is None:
            continue
        gears[gear].append(value)

    total = 0
    for gear_nums in gears.values():
        if len(gear_nums) == 2:
            total += gear_nums[0] * gear_nums[1]
    return total
