from dataclasses import dataclass
from typing import Any, NamedTuple

import parse

from aoc.utils.contents import PuzzleInput


class Pull(NamedTuple):
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    pulls: list[Pull]


def parse_game(line: str) -> Game:
    game_raw, pulls_raw = line.split(":", maxsplit=1)
    game_id = int(game_raw.split(" ", maxsplit=1)[1])
    pulls = []
    for pull_raw in pulls_raw.split("; "):
        red_result = parse.search("{:d} red", pull_raw)
        if red_result is None:
            red = 0
        else:
            red = red_result.fixed[0]

        blue_result = parse.search("{:d} blue", pull_raw)
        if blue_result is None:
            blue = 0
        else:
            blue = blue_result.fixed[0]

        green_result = parse.search("{:d} green", pull_raw)
        if green_result is None:
            green = 0
        else:
            green = green_result.fixed[0]

        pulls.append(Pull(red, green, blue))
    return Game(id=game_id, pulls=pulls)


def possible_game(game: Game) -> int:
    for pull in game.pulls:
        if pull.red > 12 or pull.green > 13 or pull.blue > 14:
            return 0
    return game.id


def part_1(puzzle: PuzzleInput) -> Any:
    games = list(map(parse_game, puzzle.lines))
    possible = sum(map(possible_game, games))
    return possible


def min_balls(game: Game) -> int:
    red, green, blue = 0, 0, 0
    for pull in game.pulls:
        if pull.red > red:
            red = pull.red
        if pull.green > green:
            green = pull.green
        if pull.blue > blue:
            blue = pull.blue
    return red * green * blue


def part_2(puzzle: PuzzleInput) -> Any:
    games = list(map(parse_game, puzzle.lines))
    power_set = list(map(min_balls, games))
    total = sum(power_set)
    return total
    return 0
