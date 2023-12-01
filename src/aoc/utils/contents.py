from dataclasses import dataclass


@dataclass(frozen=True)
class PuzzleInput:
    raw: str
    lines: list[str]


def get_puzzle_input(filepath: str) -> PuzzleInput:
    with open(filepath) as file:
        raw = file.read()
    with open(filepath) as file:
        lines = file.readlines()
        lines = list(map(lambda line: line.strip(), lines))
    return PuzzleInput(raw=raw, lines=lines)
