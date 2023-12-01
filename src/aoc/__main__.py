import argparse
from importlib.resources import files

from aoc import day_1
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
    case _:
        raise ValueError("Unknown day!")

print("Part 1:")
print(part_1)
print("Part 2:")
print(part_2)
