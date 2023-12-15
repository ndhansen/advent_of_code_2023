from collections import OrderedDict, defaultdict
from typing import Any

from aoc.utils.contents import PuzzleInput


def aoc_hash(word: str) -> int:
    current_value = 0
    for char in word:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def part_1(puzzle: PuzzleInput) -> Any:
    words = puzzle.lines[0].split(",")
    return sum(map(aoc_hash, words))


def focals(words: list[str]) -> int:
    boxes: defaultdict[int, OrderedDict[str, int]] = defaultdict(OrderedDict)
    for word in words:
        if "-" in word:
            label = word.split("-")[0]
            target = aoc_hash(label)
            if label in boxes[target]:
                del boxes[target][label]
        if "=" in word:
            label, focus = word.split("=")
            target = aoc_hash(label)
            boxes[target][label] = int(focus)

    total = 0
    for box_index, box in boxes.items():
        for slot_index, focus in enumerate(box.values()):
            total += (box_index + 1) * (slot_index + 1) * focus
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    words = puzzle.lines[0].split(",")
    return focals(words)
