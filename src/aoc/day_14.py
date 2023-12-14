import functools
from typing import Any

from aoc.utils.contents import PuzzleInput


def tilt_line(line: str) -> str:
    parts = line.split("#")
    new_line = []
    for part in parts:
        new_line.append("O" * part.count("O") + "." * part.count("."))
    return "#".join(new_line)


def tilt_line_right(line: str) -> str:
    parts = line.split("#")
    new_line = []
    for part in parts:
        new_line.append("." * part.count(".") + "O" * part.count("O"))
    return "#".join(new_line)


def total_weight(puzzle: list[str]) -> int:
    total = 0
    for i, weight in enumerate(range(len(puzzle), 0, -1)):
        total += puzzle[i].count("O") * weight

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    rotated: list[str] = ["".join(x) for x in zip(*puzzle.lines)]
    tilted = list(map(tilt_line, rotated))
    normal: list[str] = ["".join(x) for x in zip(*tilted)]
    return total_weight(normal)


@functools.lru_cache(maxsize=None)
def cycle(puzzle: tuple[str, ...]) -> tuple[str, ...]:
    # North
    tilted: list[str] = ["".join(x) for x in zip(*puzzle)]
    tilted = list(map(tilt_line, tilted))
    tilted: list[str] = ["".join(x) for x in zip(*tilted)]

    # West
    tilted = list(map(tilt_line, tilted))

    # South
    tilted: list[str] = ["".join(x) for x in zip(*tilted)]
    tilted = list(map(tilt_line_right, tilted))
    tilted: list[str] = ["".join(x) for x in zip(*tilted)]

    # East
    tilted = list(map(tilt_line_right, tilted))

    return tuple(tilted)


def part_2(puzzle: PuzzleInput) -> Any:
    layout = tuple(puzzle.lines)
    for _ in range(1000):
        layout = cycle(layout)

    weights = []
    cycles = 999
    while len(weights) < 4 or weights[:2] != weights[-2:]:
        layout = cycle(layout)
        weights.append(total_weight(list(layout)))
        cycles += 1

    repeating_weights = weights[4:]
    index = (1000000000 - cycles) % len(repeating_weights)
    return repeating_weights[index]
