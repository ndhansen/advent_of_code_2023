from enum import IntEnum
from typing import Any, Counter

from aoc.utils.contents import PuzzleInput


class Card(IntEnum):
    JOKER = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Hand:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def hand_type(self) -> int:
        c = Counter(self.cards)
        card_counts = list(sorted(c.values()))
        if Card.JOKER in self.cards:
            num_jokers = c[Card.JOKER]
            card_counts.remove(num_jokers)
            if len(card_counts) == 0:
                card_counts = [num_jokers]
            else:
                card_counts[-1] = card_counts[-1] + num_jokers

        if card_counts == [1, 1, 1, 1, 1]:
            return 1
        if card_counts == [1, 1, 1, 2]:
            return 2
        if card_counts == [1, 2, 2]:
            return 3
        if card_counts == [1, 1, 3]:
            return 4
        if card_counts == [2, 3]:
            return 5
        if card_counts == [1, 4]:
            return 6
        if card_counts == [5]:
            return 7
        raise ValueError()

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type() == other.hand_type():
            for our_card, their_card in zip(self.cards, other.cards):
                if our_card == their_card:
                    continue
                return our_card < their_card

        return self.hand_type() < other.hand_type()


def parse_card(card: str) -> Card:
    match card:
        case "2":
            return Card.TWO
        case "3":
            return Card.THREE
        case "4":
            return Card.FOUR
        case "5":
            return Card.FIVE
        case "6":
            return Card.SIX
        case "7":
            return Card.SEVEN
        case "8":
            return Card.EIGHT
        case "9":
            return Card.NINE
        case "T":
            return Card.TEN
        case "J":
            return Card.JACK
        case "Q":
            return Card.QUEEN
        case "K":
            return Card.KING
        case "A":
            return Card.ACE
        case _:
            raise ValueError()


def parse_cards(line: str) -> list[Card]:
    return list(map(parse_card, line.strip()))


def parse_line(line: str) -> tuple[Hand, int]:
    hand_raw, bid_raw = line.strip().split(" ")
    bid = int(bid_raw)
    cards = parse_cards(hand_raw)
    return (Hand(cards), bid)


def part_1(puzzle: PuzzleInput) -> Any:
    hands_unordered = list(map(parse_line, puzzle.lines))
    hands_ordered = sorted(hands_unordered, key=lambda x: x[0])
    total = 0
    i = 1
    for hand, bid in hands_ordered:
        total += i * bid
        i += 1
    return total


def parse_card_2(raw: str) -> Card:
    card = parse_card(raw)
    if card == Card.JACK:
        return Card.JOKER
    return card


def parse_cards_2(line: str) -> list[Card]:
    return list(map(parse_card_2, line.strip()))


def parse_line_2(line: str) -> tuple[Hand, int]:
    hand_raw, bid_raw = line.strip().split(" ")
    bid = int(bid_raw)
    cards = parse_cards_2(hand_raw)
    return (Hand(cards), bid)


def part_2(puzzle: PuzzleInput) -> Any:
    hands_unordered = list(map(parse_line_2, puzzle.lines))
    hands_ordered = sorted(hands_unordered, key=lambda x: x[0])
    total = 0
    i = 1
    for hand, bid in hands_ordered:
        total += i * bid
        i += 1
    return total
