import argparse
from importlib.resources import files

from aoc import (
    day_1,
    day_2,
    day_3,
    day_4,
    day_5,
    day_6,
    day_7,
    day_8,
    day_9,
    day_10,
    day_11,
)
from aoc.utils import contents

parser = argparse.ArgumentParser(prog="AOC", description="Advent of Code")
parser.add_argument("day", help="The day to run.")
parser.add_argument(
    "-t", "--test", action="store_true", help="Whether to use the test or real input."
)

args = parser.parse_args()

# Get the file contents
filename = "test.txt" if args.test else "input.txt"
path = files("aoc.inputs") / args.day / filename
puzzle = contents.get_puzzle_input(path)

match args.day:
    case "day_1":
        part_1 = day_1.part_1(puzzle)
        part_2 = day_1.part_2(puzzle)
    case "day_2":
        part_1 = day_2.part_1(puzzle)
        part_2 = day_2.part_2(puzzle)
    case "day_3":
        part_1 = day_3.part_1(puzzle)
        part_2 = day_3.part_2(puzzle)
    case "day_4":
        part_1 = day_4.part_1(puzzle)
        part_2 = day_4.part_2(puzzle)
    case "day_5":
        part_1 = day_5.part_1(puzzle)
        part_2 = day_5.part_2(puzzle)
    case "day_6":
        part_1 = day_6.part_1(puzzle)
        part_2 = day_6.part_2(puzzle)
    case "day_7":
        part_1 = day_7.part_1(puzzle)
        part_2 = day_7.part_2(puzzle)
    case "day_8":
        part_1 = day_8.part_1(puzzle)
        part_2 = day_8.part_2(puzzle)
    case "day_9":
        part_1 = day_9.part_1(puzzle)
        part_2 = day_9.part_2(puzzle)
    case "day_10":
        part_1 = day_10.part_1(puzzle)
        part_2 = day_10.part_2(puzzle)
    case "day_11":
        part_1 = day_11.part_1(puzzle)
        part_2 = day_11.part_2(puzzle)
    case _:
        raise ValueError("Unknown day!")

print("Part 1:")
print(part_1)
print("Part 2:")
print(part_2)
