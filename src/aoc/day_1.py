from aoc.utils.contents import PuzzleInput


def get_input(filename: str = "input.txt") -> list[str]:
    with open(filename) as file:
        return file.readlines()


def part_1(puzzle: PuzzleInput) -> int:
    contents = puzzle.lines
    rolling_sum = 0
    for line in contents:
        line = line.strip()
        digits = [x for x in line if x.isdigit()]
        numbers = "".join([digits[0], digits[-1]])
        num = int(numbers)
        rolling_sum += num
    return rolling_sum


NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def replace(line: str) -> str:
    low_index = {}
    for n, number in enumerate(NUMBERS):
        cur_index = line.find(number)
        if cur_index != -1:
            low_index[cur_index] = (n, number)

    high_index = {}
    for n, number in enumerate(NUMBERS):
        cur_index = line.rfind(number)
        if cur_index != -1:
            high_index[cur_index] = (n, number)

    if len(low_index) > 0:
        lowest = min(low_index.keys())
        line = line[:lowest] + str(low_index[lowest][0]) + line[lowest:]

    if len(high_index) > 0:
        highest = max(high_index.keys())
        line = line[: highest + 1] + str(high_index[highest][0]) + line[highest + 1 :]

    return line


def part_2(puzzle: PuzzleInput) -> int:
    contents = puzzle.lines
    rolling_sum = 0
    for line in contents:
        line = line.strip()
        line = replace(line)
        digits = [x for x in line if x.isdigit()]
        numbers = "".join([digits[0], digits[-1]])
        num = int(numbers)
        rolling_sum += num
    return rolling_sum
