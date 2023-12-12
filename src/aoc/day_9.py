from typing import Any

from aoc.utils.contents import PuzzleInput


def parse_line(line: str) -> list[int]:
    return [int(num) for num in line.strip().split(" ")]


def get_change(numbers: list[int]) -> list[int]:
    changes = []
    for i in range(1, len(numbers)):
        changes.append(numbers[i] - numbers[i - 1])
    return changes


def get_changes(numbers: list[int]) -> list[list[int]]:
    predict_lines = [numbers]
    while True:
        changes = get_change(predict_lines[-1])
        if set(changes) == {0}:
            break
        predict_lines.append(changes)
    return predict_lines


def predict_next(numbers: list[int]) -> int:
    predict_lines = get_changes(numbers)

    total = 0
    for line in predict_lines:
        total += line[-1]
    return total


def predict_last(numbers: list[int]) -> int:
    predict_lines = get_changes(numbers)

    total = 0
    for i in range(len(predict_lines) - 1, -1, -1):
        total = predict_lines[i][0] - total
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    increases = list(map(parse_line, puzzle.lines))
    next_nums = list(map(predict_next, increases))
    return sum(next_nums)


def part_2(puzzle: PuzzleInput) -> Any:
    increases = list(map(parse_line, puzzle.lines))
    last_nums = list(map(predict_last, increases))
    return sum(last_nums)
