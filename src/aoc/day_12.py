import re
from typing import Any, NamedTuple
import itertools

from aoc.utils.contents import PuzzleInput

from tqdm import tqdm


class Spring(NamedTuple):
    placement: str
    spring_count: list[int]


def parse_input(puzzle: list[str]) -> list[Spring]:
    lines = []
    for row in puzzle:
        springs, raw_count = row.split(" ")
        springs = springs.strip(".")
        springs = ".".join(x for x in springs.split(".") if len(x) > 0)
        count_nums_raw = raw_count.split(",")
        numbers = [int(x) for x in count_nums_raw]
        lines.append(Spring(springs, numbers))
    return lines


def split_to_valid_groups(spring: Spring) -> list[str]:
    line = spring.placement.strip(".")
    line = ".".join(x for x in line.split(".") if len(x) > 0)


def find(line: str, character: str):
    return [i for i, letter in enumerate(line) if letter == character]


def get_all_placements(spring: str, num: int) -> list[tuple[str, str]]:
    all = []

    # Brute force for now
    # to_replace = num - spring.count("#")
    # for indexes in itertools.combinations(find(spring, "?"), to_replace):
    #     current = list(spring.replace("?", "."))
    #     for index in indexes:
    #         current[index] = "#"
    #     all.append()
    wiped = spring.replace("?", "#")
    for hit in re.finditer("#" * num, wiped):
        all.append((spring[: hit.start()] + "#" * num, spring[hit.end() :]))
    return all


def count_placements(spring: Spring) -> int:
    constelations = [("", spring.placement)]
    for i in range(len(spring.spring_count)):
        # Restrict our range to the possible places we could put the number
        sum_leftover_numbers = sum(spring.spring_count[i + 1 :])
        if sum_leftover_numbers > 0:
            sum_leftover_numbers += len(spring.spring_count[i + 1 :])

        # Take each constelation and try putting the current number in
        new_constellations = []
        for accounted, usable in constelations:
            free = usable[: len(usable) - sum_leftover_numbers]
            reserved = usable[len(usable) - sum_leftover_numbers :]
            for placement, remaining in get_all_placements(
                free, spring.spring_count[i]
            ):
                new_constellations.append((accounted + placement, remaining + reserved))

        constelations = new_constellations

    return len(constelations)


def is_valid(spring: Spring) -> bool:
    if spring.placement.count("#") != sum(spring.spring_count):
        return False

    line = spring.placement.strip(".")
    line = ".".join(x for x in line.split(".") if len(x) > 0)
    chunks = line.split(".")
    spring_counts = [len(x) for x in chunks]
    return spring_counts == spring.spring_count


def brute_force(spring: Spring) -> int:
    total = 0

    questionmarks = find(spring.placement, "?")
    for i in range(len(questionmarks) + 1):
        for indexes in itertools.combinations(questionmarks, i):
            cleaned = list(spring.placement.replace("?", "."))
            for index in indexes:
                cleaned[index] = "#"
            if is_valid(Spring("".join(cleaned), spring.spring_count)):
                total += 1

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    springs = parse_input(puzzle.lines)
    # return sum(map(count_placements, springs))
    return sum(map(brute_force, springs))


def parse_input_2(puzzle: list[str]) -> list[Spring]:
    lines = []
    for row in puzzle:
        springs, raw_count = row.split(" ")
        springs = (springs + "?") * 5
        springs = springs[:-1]
        springs = springs.strip(".")
        springs = ".".join(x for x in springs.split(".") if len(x) > 0)
        count_nums_raw = raw_count.split(",")
        numbers = [int(x) for x in count_nums_raw] * 5
        lines.append(Spring(springs, numbers))
    return lines


def generate_regex(nums: list[int]) -> str:
    chunks = [r"([#\?]{" + str(x) + "})" for x in nums]
    return r"[\.\?]+".join(chunks)


def actual_match(hit: re.Match, line: str) -> str:
    new_possibility = list(line.replace("?", "."))
    for start, end in hit.regs[1:]:
        for i in range(start, end):
            new_possibility[i] = "#"
    return "".join(new_possibility)


def possible_matches(spring: Spring) -> int:
    pattern = re.compile(generate_regex(spring.spring_count))
    seen = set()
    test = set()
    possibilities = {spring.placement}
    while len(possibilities) > 0:
        possibility = possibilities.pop()
        for hit in re.finditer(pattern, possibility):
            seen.add(possibility)
            test.add(actual_match(hit, possibility))
            for start, end in hit.regs[1:]:
                new_possibility = list(possibility)
                all = []
                for i in range(start, end):
                    if new_possibility[i] == "?":
                        x = new_possibility.copy()
                        x[i] = "."
                        all.append(x)
                for x in all:
                    if "".join(x) not in seen:
                        possibilities.add("".join(x))

    print(len(test))
    return len(test)


def part_2(puzzle: PuzzleInput) -> Any:
    # springs = parse_input_2(puzzle.lines)
    import pudb

    pudb.set_trace()
    springs = parse_input(puzzle.lines)
    possible_matches(springs[-1])
    return sum(map(possible_matches, springs))
    # total = 0
    # for spring in tqdm(springs):
    #     total += brute_force(spring)
    # return total
