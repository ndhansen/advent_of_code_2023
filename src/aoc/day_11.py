from itertools import combinations
from typing import Any, NamedTuple

from aoc.utils.common import Coord
from aoc.utils.contents import PuzzleInput


class LongGalaxy(NamedTuple):
    xs: set[int]
    ys: set[int]


def parse_input(puzzle: list[str]) -> list[list[str]]:
    return [list(line) for line in puzzle]


def expand_galaxy(galaxy: list[list[str]]) -> list[list[str]]:
    expanded_horizontal = []
    for line in galaxy:
        if set(line) == {"."}:
            expanded_horizontal.append(line)
        expanded_horizontal.append(line)

    expanded_vertical = []
    for line in zip(*expanded_horizontal):
        if set(line) == {"."}:
            expanded_vertical.append(list(line))
        expanded_vertical.append(list(line))

    flipped_galaxy = zip(*expanded_vertical)
    final_galaxy = []
    for flipped in flipped_galaxy:
        final_galaxy.append(list(flipped))

    return final_galaxy


def get_stars(galaxy: list[list[str]]) -> list[Coord]:
    stars = []
    for y in range(len(galaxy)):
        for x in range(len(galaxy[0])):
            if galaxy[y][x] == "#":
                stars.append(Coord(x, y))
    return stars


def dist_between_star_pairs(stars: list[Coord]) -> int:
    total = 0
    for star_1, star_2 in combinations(stars, 2):
        dist = abs(star_1.x - star_2.x) + abs(star_1.y - star_2.y)
        total += dist
    return total


def get_expands(galaxy: list[list[str]]) -> LongGalaxy:
    long_xs = set()
    x = 0
    for line in zip(*galaxy):
        if set(line) == {"."}:
            long_xs.add(x)
        x += 1

    long_ys = set()
    y = 0
    for line in galaxy:
        if set(line) == {"."}:
            long_ys.add(y)
        y += 1

    return LongGalaxy(long_xs, long_ys)


def part_1(puzzle: PuzzleInput) -> Any:
    galaxy = parse_input(puzzle.lines)
    expanded_galaxy = expand_galaxy(galaxy)
    stars = get_stars(expanded_galaxy)
    dist = dist_between_star_pairs(stars)
    return dist


def long_dist_between_star_pairs(stars: list[Coord], long_space: LongGalaxy) -> int:
    empty_space_len = 1_000_000
    total = 0
    for star_1, star_2 in combinations(stars, 2):
        dist = abs(star_1.x - star_2.x) + abs(star_1.y - star_2.y)

        x_dir = 1 if star_2.x > star_1.x else -1
        for x in range(star_1.x, star_2.x, x_dir):
            if x in long_space.xs:
                dist += empty_space_len - 1

        y_dir = 1 if star_2.y > star_1.y else -1
        for y in range(star_1.y, star_2.y, y_dir):
            if y in long_space.ys:
                dist += empty_space_len - 1

        total += dist
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    galaxy = parse_input(puzzle.lines)
    long_galaxy = get_expands(galaxy)
    stars = get_stars(galaxy)
    dist = long_dist_between_star_pairs(stars, long_galaxy)
    return dist
