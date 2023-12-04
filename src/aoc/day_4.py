from dataclasses import dataclass
from typing import Any

from aoc.utils.contents import PuzzleInput


@dataclass
class Card:
    id: int
    winning: list[int]
    numbers: list[int]
    copies: int = 1


def parse_line(line: str) -> Card:
    card_raw, nums_raw = line.strip().split(": ")
    card_raw = " ".join(card_raw.split())
    nums_raw = " ".join(nums_raw.split())
    card_id = int(card_raw.split(" ")[1])
    winning_nums, present_nums = nums_raw.split(" | ")
    present_numbers = []
    for raw_present_num in present_nums.split(" "):
        pres_num = raw_present_num.strip()
        present_numbers.append(int(pres_num))

    winning_numbers = []
    for raw_winning_num in winning_nums.split(" "):
        raw_winning_num_clean = raw_winning_num.strip()
        winning_numbers.append(int(raw_winning_num_clean))

    return Card(card_id, winning_numbers, present_numbers)


def card_score(card: Card) -> int:
    winning_nums = len(set(card.winning).intersection(card.numbers))
    if winning_nums == 0:
        return 0
    return 2 ** (winning_nums - 1)


def card_winners(card: Card) -> int:
    winning_nums = len(set(card.winning).intersection(card.numbers))
    return winning_nums


def part_1(puzzle: PuzzleInput) -> Any:
    cards: list[Card] = []
    for line in puzzle.lines:
        cards.append(parse_line(line))

    total = 0
    for card in cards:
        total += card_score(card)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    cards: list[Card] = []
    for line in puzzle.lines:
        cards.append(parse_line(line))

    for card in cards:
        winners = card_winners(card)
        for i in range(card.id, card.id + winners):
            copies = card.copies
            cards[i].copies += copies

    total = sum(map(lambda card: card.copies, cards))
    return total
