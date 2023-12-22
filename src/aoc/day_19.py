import re
from enum import Enum
from typing import Any, Literal, NamedTuple

from aoc.utils.contents import PuzzleInput


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Evaluation(NamedTuple):
    i: int
    direction: Literal["<", ">"]
    value: int
    target: str


class Condition(NamedTuple):
    name: str
    cond: list[Evaluation]
    final: str


def parse_input(contents: str) -> tuple[dict[str, Condition], list[Part]]:
    raw_conditions, raw_parts = contents.split("\n\n")

    conditions: dict[str, Condition] = {}
    for raw_condition in raw_conditions.strip().split("\n"):
        name, rest = raw_condition.split("{")
        rest = rest.strip().strip("}")
        cond_eval: list[Evaluation] = []
        evals = rest.split(",")

        for part in evals[:-1]:
            cond, dest = part.split(":")
            index: int
            match cond[0]:
                case "x":
                    index = 0
                case "m":
                    index = 1
                case "a":
                    index = 2
                case "s":
                    index = 3
                case _:
                    raise ValueError()

            cond_eval.append(Evaluation(index, cond[1], int(cond[2:]), dest))

        conditions[name] = Condition(name, cond_eval, evals[-1])

    parts: list[Part] = []
    for raw_part in raw_parts.strip().split("\n"):
        raw_components = re.findall(r"\d+", raw_part)
        parts.append(
            Part(
                x=int(raw_components[0]),
                m=int(raw_components[1]),
                a=int(raw_components[2]),
                s=int(raw_components[3]),
            )
        )

    return conditions, parts


def run_evaluation(part, evaluation: Evaluation) -> str | None:
    match evaluation.direction:
        case "<":
            return evaluation.target if part[evaluation.i] < evaluation.value else None
        case ">":
            return evaluation.target if part[evaluation.i] > evaluation.value else None


def next_condition(part: Part, condition: Condition) -> str:
    for cond in condition.cond:
        next_name = run_evaluation(part, cond)
        if next_name:
            return next_name

    return condition.final


def accepted_value(parts: list[Part], conditions: dict[str, Condition]) -> int:
    total = 0
    for part in parts:
        current = "in"
        while True:
            current = next_condition(part, conditions[current])
            if current == "R":
                break
            if current == "A":
                total += part.x + part.m + part.s + part.a
                break

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    conditions, parts = parse_input(puzzle.raw)
    return accepted_value(parts, conditions)


class TreeCondition(NamedTuple):
    rating: str
    direction: Literal["<", ">"]
    value: int

    @staticmethod
    def from_evaluation(evaluation: "Evaluation") -> "TreeCondition":
        rating: str
        match evaluation.i:
            case 0:
                rating = "x"
            case 1:
                rating = "m"
            case 2:
                rating = "a"
            case 3:
                rating = "s"
            case _:
                raise ValueError()
        return TreeCondition(rating, evaluation.direction, evaluation.value)

    def flip(self) -> "TreeCondition":
        if self.direction == "<":
            return TreeCondition(self.rating, ">", self.value - 1)
        if self.direction == ">":
            return TreeCondition(self.rating, "<", self.value + 1)
        raise ValueError()

    def __str__(self) -> str:
        return f"{self.rating}{self.direction}{self.value}"


class Tail(Enum):
    ACCEPTED = "A"
    REJECTED = "R"


class Tree(NamedTuple):
    cond: TreeCondition
    yes: "Tree | Tail"
    no: "Tree | Tail"


def build_tree(conditions: dict[str, Condition], current: str = "in") -> Tree | Tail:
    if len(conditions[current].cond) == 0:
        if conditions[current].final == "A":
            return Tail.ACCEPTED
        elif conditions[current].final == "R":
            return Tail.REJECTED
        else:
            return build_tree(conditions, current=conditions[current].final)

    cond = conditions[current].cond.pop(0)
    tree_cond = TreeCondition.from_evaluation(cond)
    if cond.target == "A":
        yes = Tail.ACCEPTED
    elif cond.target == "R":
        yes = Tail.REJECTED
    else:
        yes = build_tree(conditions, current=cond.target)

    no = build_tree(conditions, current=current)
    return Tree(tree_cond, yes, no)


def simplify_tree(tree: Tree) -> Tree | Tail:
    if tree.yes == Tail.ACCEPTED and tree.no == Tail.ACCEPTED:
        return Tail.ACCEPTED
    if tree.yes == Tail.REJECTED and tree.no == Tail.REJECTED:
        return Tail.REJECTED
    yes = tree.yes
    if isinstance(yes, Tree):
        yes = simplify_tree(yes)
    no = tree.no
    if isinstance(no, Tree):
        no = simplify_tree(no)
    return Tree(tree.cond, yes, no)


def accepted_tree_conditions(tree: Tree) -> list[tuple[TreeCondition, ...]]:
    accepted_conditions: list[tuple[TreeCondition, ...]] = []
    frontier: list[tuple[Tree, tuple[TreeCondition, ...]]] = [(tree, ())]
    while len(frontier) > 0:
        branch, cur_conditions = frontier.pop(0)
        if branch.yes == Tail.ACCEPTED:
            accepted_conditions.append((*cur_conditions, branch.cond))
        elif branch.yes == Tail.REJECTED:
            pass
        else:
            frontier.append((branch.yes, (*cur_conditions, branch.cond)))

        if branch.no == Tail.ACCEPTED:
            accepted_conditions.append((*cur_conditions, branch.cond.flip()))
        elif branch.no == Tail.REJECTED:
            pass
        else:
            frontier.append((branch.no, (*cur_conditions, branch.cond.flip())))

    return accepted_conditions


def get_rating_range(
    rating: str, conditions: tuple[TreeCondition, ...]
) -> tuple[int, int]:
    conditions = tuple(c for c in conditions if c.rating == rating)

    lower_bound = tuple(c.value for c in conditions if c.direction == ">")
    smallest = 0
    if len(lower_bound) > 0:
        smallest = max(lower_bound)

    upper_bound = tuple(c.value for c in conditions if c.direction == "<")
    biggest = 4000
    if len(upper_bound) > 0:
        biggest = min(upper_bound) - 1

    return smallest, biggest


def get_total_combinations(conditions: list[tuple[TreeCondition, ...]]) -> int:
    total = 0
    for condition in conditions:
        current = 1
        for rating in ("x", "m", "a", "s"):
            lower, upper = get_rating_range(rating, condition)
            assert lower < upper
            current *= max((upper - lower), 0)
        total += current
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    conditions, _ = parse_input(puzzle.raw)
    import pudb

    pudb.set_trace()
    tree = build_tree(conditions)
    assert isinstance(tree, Tree)
    tree = simplify_tree(tree)
    assert isinstance(tree, Tree)
    accept_conds = accepted_tree_conditions(tree)
    return get_total_combinations(accept_conds)
