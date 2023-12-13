import functools
from typing import Any, NamedTuple

from aoc.utils.contents import PuzzleInput

from tqdm import tqdm


class Spring(NamedTuple):
    placement: str
    spring_count: tuple[int, ...]


def parse_input(puzzle: list[str], repeats: int = 1) -> list[Spring]:
    lines = []
    for row in puzzle:
        springs, raw_count = row.split(" ")
        springs = "?".join([springs] * repeats)

        # Basically worthless optimisations
        springs = springs.strip(".")
        springs = ".".join(x for x in springs.split(".") if len(x) > 0)

        count_nums_raw = raw_count.split(",")
        numbers = tuple(int(x) for x in count_nums_raw) * repeats
        lines.append(Spring(springs, numbers))
    return lines


@functools.lru_cache(maxsize=None)
def placements(spring: Spring, next_must_work: bool) -> int:
    if sum(spring.spring_count) > len(spring.placement):
        # Significant optimisation
        return 0
    if sum(spring.spring_count) == 0:
        if "#" in spring.placement:
            return 0
        else:
            return 1
    if len(spring.placement) == 0:
        return 0
    if spring.spring_count[0] == 0:
        if spring.placement[0] not in {"?", "."}:
            return 0
        return placements(Spring(spring.placement[1:], spring.spring_count[1:]), False)
    if next_must_work or spring.placement[0] == "#":
        if spring.placement[0] not in {"?", "#"}:
            return 0
        cur_count, *rest = spring.spring_count
        new_count = tuple([cur_count - 1] + rest)
        return placements(Spring(spring.placement[1:], new_count), True)
    if spring.placement[0] == ".":
        return placements(Spring(spring.placement[1:], spring.spring_count), False)
    if spring.placement[0] == "?":
        cur_count, *rest = spring.spring_count
        new_count = tuple([cur_count - 1] + rest)
        place = placements(Spring(spring.placement[1:], new_count), True)
        no_place = placements(Spring(spring.placement[1:], spring.spring_count), False)
        return place + no_place
    raise ValueError("Huh?")


def part_1(puzzle: PuzzleInput) -> Any:
    springs = parse_input(puzzle.lines)
    return sum(placements(spring, False) for spring in springs)


def part_2(puzzle: PuzzleInput) -> Any:
    springs = parse_input(puzzle.lines, repeats=5)
    return sum(placements(spring, False) for spring in springs)
