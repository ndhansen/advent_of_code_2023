from typing import Any

from aoc.utils.contents import PuzzleInput


def parse_input(contents: str) -> list[list[str]]:
    chunks = contents.split("\n\n")
    patterns = []
    for chunk in chunks:
        patterns.append([line.strip() for line in chunk.strip().split("\n")])
    return patterns


def mirror(left: str, right: str) -> bool:
    for left, right in zip(left[::-1], right, strict=False):
        if left != right:
            return False
    return True


def smudged_mirror(left: str, right: str) -> int:
    errors = 0
    for left, right in zip(left[::-1], right, strict=False):
        if left != right:
            errors += 1
    return errors


def find_reflection(pattern: list[str]) -> int:
    # Vertical
    for i in range(1, len(pattern[0])):
        works = True
        for line in pattern:
            if not mirror(line[:i], line[i:]):
                works = False
                break
        if works:
            return i

    # horizontal
    flipped = list(zip(*pattern))
    for i in range(1, len(pattern)):
        works = True
        for chars in flipped:
            line = "".join(chars)
            if not mirror(line[:i], line[i:]):
                works = False
                break
        if works:
            return 100 * i
    raise ValueError()


def part_1(puzzle: PuzzleInput) -> Any:
    patterns = parse_input(puzzle.raw)
    return sum(map(find_reflection, patterns))


def find_reflection_2(pattern: list[str]) -> int:
    # Vertical
    for i in range(1, len(pattern[0])):
        errors = 0
        for line in pattern:
            errors += smudged_mirror(line[:i], line[i:])
        if errors == 1:
            return i

    # horizontal
    flipped = list(zip(*pattern))
    for i in range(1, len(pattern)):
        errors = 0
        for chars in flipped:
            line = "".join(chars)
            errors += smudged_mirror(line[:i], line[i:])
        if errors == 1:
            return 100 * i
    raise ValueError()


def part_2(puzzle: PuzzleInput) -> Any:
    patterns = parse_input(puzzle.raw)
    return sum(map(find_reflection_2, patterns))
