from typing import Any
import math

from parse import parse

from aoc.utils.contents import PuzzleInput


def get_instructions(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions = lines[0].strip()
    desert_map: dict[str, tuple[str, str]] = {}
    for line in lines[2:]:
        node, left, right = parse("{} = ({}, {})", line).fixed
        desert_map[node] = (left, right)

    return instructions, desert_map


def steps(
    start: str, end: str, instructions: str, desert_map: dict[str, tuple[str, str]]
) -> int:
    i = 0
    cur_node = start
    while cur_node != end:
        direction = instructions[i % len(instructions)]
        match direction:
            case "L":
                cur_node = desert_map[cur_node][0]
            case "R":
                cur_node = desert_map[cur_node][1]
            case _:
                raise ValueError()
        i += 1
    return i


def get_start_nodes(desert_map: dict[str, tuple[str, str]]) -> list[str]:
    start_nodes = []
    for key in desert_map.keys():
        if key[-1] == "A":
            start_nodes.append(key)
    return start_nodes


def part_1(puzzle: PuzzleInput) -> Any:
    instructions, desert_map = get_instructions(puzzle.lines)
    return steps("AAA", "ZZZ", instructions, desert_map)


def ghost_steps(
    start: str, instructions: str, desert_map: dict[str, tuple[str, str]]
) -> int:
    i = 0
    cur_node = start
    while cur_node[-1] != "Z":
        direction = instructions[i % len(instructions)]
        match direction:
            case "L":
                cur_node = desert_map[cur_node][0]
            case "R":
                cur_node = desert_map[cur_node][1]
            case _:
                raise ValueError()
        i += 1
    return i


def simultaneous_steps(
    instructions: str, desert_map: dict[str, tuple[str, str]]
) -> int:
    starts = get_start_nodes(desert_map)
    times = []
    for start in starts:
        times.append(ghost_steps(start, instructions, desert_map))

    return math.lcm(*times)


def part_2(puzzle: PuzzleInput) -> Any:
    instructions, desert_map = get_instructions(puzzle.lines)
    return simultaneous_steps(instructions, desert_map)
