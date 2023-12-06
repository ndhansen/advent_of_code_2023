from typing import Any, NamedTuple

from parse import findall

from aoc.utils.contents import PuzzleInput


class Race(NamedTuple):
    time: int
    distance: int


def get_races(lines: list[str]) -> list[Race]:
    times = []
    for hit in findall("{:d}", lines[0]):
        times.append(hit.fixed[0])
    distances = []
    for hit in findall("{:d}", lines[1]):
        distances.append(hit.fixed[0])

    races = []
    for time, distance in zip(times, distances):
        races.append(Race(time, distance))

    return races


def get_time(race: Race, seconds: int) -> int:
    move_time = race.time - seconds
    return move_time * seconds


def get_valid_times(race: Race) -> int:
    total = 0
    for i in range(1, race.time):
        if get_time(race, i) > race.distance:
            total += 1
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    races = get_races(puzzle.lines)
    possible_wins = []
    for race in races:
        possible_wins.append(get_valid_times(race))

    total = 1
    for possible_win in possible_wins:
        total *= possible_win

    return total


def get_race(lines: list[str]) -> Race:
    times = []
    for hit in findall("{:d}", lines[0]):
        times.append(hit.fixed[0])
    distances = []
    for hit in findall("{:d}", lines[1]):
        distances.append(hit.fixed[0])

    time = int("".join(str(x) for x in times))
    distance = int("".join(str(x) for x in distances))
    return Race(time, distance)


def part_2(puzzle: PuzzleInput) -> Any:
    race = get_race(puzzle.lines)
    possible_wins = []
    possible_wins.append(get_valid_times(race))

    total = 1
    for possible_win in possible_wins:
        total *= possible_win

    return total
