import argparse
from importlib.resources import files
from timeit import default_timer as timer

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
    day_12,
    day_13,
    day_14,
    day_15,
    day_16,
    day_17,
    day_18,
    day_19,
    day_20,
    day_21,
    day_22,
    day_23,
    day_24,
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
start_time = timer()

match args.day:
    case "day_1":
        part_1 = day_1.part_1(puzzle)
        middle_time = timer()
        part_2 = day_1.part_2(puzzle)
    case "day_2":
        part_1 = day_2.part_1(puzzle)
        middle_time = timer()
        part_2 = day_2.part_2(puzzle)
    case "day_3":
        part_1 = day_3.part_1(puzzle)
        middle_time = timer()
        part_2 = day_3.part_2(puzzle)
    case "day_4":
        part_1 = day_4.part_1(puzzle)
        middle_time = timer()
        part_2 = day_4.part_2(puzzle)
    case "day_5":
        part_1 = day_5.part_1(puzzle)
        middle_time = timer()
        part_2 = day_5.part_2(puzzle)
    case "day_6":
        part_1 = day_6.part_1(puzzle)
        middle_time = timer()
        part_2 = day_6.part_2(puzzle)
    case "day_7":
        part_1 = day_7.part_1(puzzle)
        middle_time = timer()
        part_2 = day_7.part_2(puzzle)
    case "day_8":
        part_1 = day_8.part_1(puzzle)
        middle_time = timer()
        part_2 = day_8.part_2(puzzle)
    case "day_9":
        part_1 = day_9.part_1(puzzle)
        middle_time = timer()
        part_2 = day_9.part_2(puzzle)
    case "day_10":
        part_1 = day_10.part_1(puzzle)
        middle_time = timer()
        part_2 = day_10.part_2(puzzle)
    case "day_11":
        part_1 = day_11.part_1(puzzle)
        middle_time = timer()
        part_2 = day_11.part_2(puzzle)
    case "day_12":
        part_1 = day_12.part_1(puzzle)
        middle_time = timer()
        part_2 = day_12.part_2(puzzle)
    case "day_13":
        part_1 = day_13.part_1(puzzle)
        middle_time = timer()
        part_2 = day_13.part_2(puzzle)
    case "day_14":
        part_1 = day_14.part_1(puzzle)
        middle_time = timer()
        part_2 = day_14.part_2(puzzle)
    case "day_15":
        part_1 = day_15.part_1(puzzle)
        middle_time = timer()
        part_2 = day_15.part_2(puzzle)
    case "day_16":
        part_1 = day_16.part_1(puzzle)
        middle_time = timer()
        part_2 = day_16.part_2(puzzle)
    case "day_17":
        part_1 = day_17.part_1(puzzle)
        middle_time = timer()
        part_2 = day_17.part_2(puzzle)
    case "day_18":
        part_1 = day_18.part_1(puzzle)
        middle_time = timer()
        part_2 = day_18.part_2(puzzle)
    case "day_19":
        part_1 = day_19.part_1(puzzle)
        middle_time = timer()
        part_2 = day_19.part_2(puzzle)
    case "day_20":
        part_1 = day_20.part_1(puzzle)
        middle_time = timer()
        part_2 = day_20.part_2(puzzle)
    case "day_21":
        part_1 = day_21.part_1(puzzle)
        middle_time = timer()
        part_2 = day_21.part_2(puzzle)
    case "day_22":
        part_1 = day_22.part_1(puzzle)
        middle_time = timer()
        part_2 = day_22.part_2(puzzle)
    case "day_23":
        part_1 = day_23.part_1(puzzle)
        middle_time = timer()
        part_2 = day_23.part_2(puzzle)
    case "day_24":
        part_1 = day_24.part_1(puzzle)
        middle_time = timer()
        part_2 = day_24.part_2(puzzle)
    case _:
        raise ValueError("Unknown day!")

end_time = timer()

print("Part 1:")
print(part_1)
print("Time taken:", round(middle_time - start_time, 3), "seconds")
print()
print("Part 2:")
print(part_2)
print("Time taken:", round(end_time - middle_time, 3), "seconds")
