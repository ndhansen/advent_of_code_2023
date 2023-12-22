from dataclasses import dataclass
from typing import Any, NamedTuple

from parse import findall, parse
from tqdm import tqdm

from aoc.utils.contents import PuzzleInput


class Range(NamedTuple):
    dest_start: int
    source_start: int
    length: int


@dataclass
class Allocation:
    id: int
    ranges: list[Range]


def get_allocations(file: str) -> (list[Allocation], list[int]):
    # Get seeds
    chunks = file.strip().split("\n\n")
    seeds = []
    for hit in findall("{:d}", chunks[0]):
        seeds.append(hit.fixed[0])

    allocations = []
    id = 0
    for chunk in chunks[1:]:
        lines = chunk.split("\n")
        ranges = []
        for line in lines[1:]:
            line_nums = parse("{:d} {:d} {:d}", line).fixed
            ranges.append(Range(line_nums[0], line_nums[1], line_nums[2]))

        allocations.append(Allocation(id=id, ranges=ranges))
        id += 1
    return allocations, seeds


def seed_matches_range(seed: int, seed_range: Range) -> int | None:
    if seed >= seed_range.source_start and seed <= (
        seed_range.source_start + seed_range.length
    ):
        position = seed - seed_range.source_start
        return seed_range.dest_start + position


def get_location(seed: int, allocations: list[Allocation]) -> int:
    for allocation in allocations:
        for seed_range in allocation.ranges:
            if new_location := seed_matches_range(seed, seed_range):
                seed = new_location
                break
        pass
    return seed


def part_1(puzzle: PuzzleInput) -> int:
    mappings, seeds = get_allocations(puzzle.raw)
    locations = []
    for seed in seeds:
        locations.append(get_location(seed, mappings))
    return min(locations)


def get_seed_ranges(seeds: list[int]) -> list[tuple[int, int]]:
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append((seeds[i], seeds[i] + seeds[i + 1]))
    return seed_ranges


def precompute(
    smallest: int, largest: int, allocations: list[Allocation]
) -> dict[int, int]:
    seed_map = {}
    for seed in tqdm(range(smallest, largest + 1)):
        seed_map[seed] = get_location(seed, allocations)
    return seed_map


def part_2(puzzle: PuzzleInput) -> Any:
    mappings, raw_seeds = get_allocations(puzzle.raw)
    seeds = get_seed_ranges(raw_seeds)
    # Attempt 1 - brute force
    smallest = 1_000_000_000_000
    for seed_range in tqdm(seeds):
        for seed in tqdm(range(seed_range[0], seed_range[1])):
            loc = get_location(seed, mappings)
            if loc < smallest:
                smallest = loc
    return smallest
