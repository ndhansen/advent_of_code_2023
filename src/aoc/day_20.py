import math
from dataclasses import dataclass
from enum import Enum
from typing import Any

from aoc.utils.contents import PuzzleInput


class ModuleType(Enum):
    BROADCASTER = "broadcast"
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    OUTPUT = "output"


@dataclass
class Module:
    name: str
    kind: ModuleType
    outputs: tuple[str, ...]


@dataclass
class Broadcast(Module):
    pass


@dataclass
class Output(Module):
    pass


@dataclass
class FlipFlop(Module):
    state: bool = False


@dataclass
class Conjunction(Module):
    memory: dict[str, bool]


def parse_line(line: str) -> Module:
    identifier, raw_outputs = line.split(" -> ")
    outputs = raw_outputs.strip().split(", ")
    if identifier[0] == "%":
        return FlipFlop(
            name=identifier[1:], kind=ModuleType.FLIP_FLOP, outputs=tuple(outputs)
        )
    elif identifier[0] == "&":
        return Conjunction(
            name=identifier[1:],
            kind=ModuleType.FLIP_FLOP,
            outputs=tuple(outputs),
            memory={},
        )
    else:
        return Broadcast(
            name=identifier, kind=ModuleType.FLIP_FLOP, outputs=tuple(outputs)
        )


def parse_input(lines: list[str]) -> dict[str, Module]:
    modules = list(map(parse_line, lines))
    modules_map = {m.name: m for m in modules}

    output_modules = []
    for module in modules_map.values():
        for output in module.outputs:
            if output not in modules_map:
                output_modules.append(Output(output, ModuleType.OUTPUT, ()))
    for module in output_modules:
        modules_map[module.name] = module

    for module in modules_map.values():
        for output in module.outputs:
            target = modules_map[output]
            if isinstance(target, Conjunction):
                target.memory[module.name] = False

    return modules_map


def push_button(modules: dict[str, Module]) -> tuple[int, int]:
    lows = 1  # 1 for the button push
    highs = 0
    frontier: list[tuple[bool, str, str]] = [(False, "button", "broadcaster")]

    while len(frontier) > 0:
        signal, source, name = frontier.pop(0)
        module = modules[name]

        if isinstance(module, Broadcast):
            for output in module.outputs:
                frontier.append((False, module.name, output))
                lows += 1
        elif isinstance(module, FlipFlop):
            if signal is False:
                if module.state is False:
                    module.state = True
                    for output in module.outputs:
                        highs += 1
                        frontier.append((True, module.name, output))
                elif module.state is True:
                    module.state = False
                    for output in module.outputs:
                        lows += 1
                        frontier.append((False, module.name, output))
        elif isinstance(module, Conjunction):
            module.memory[source] = signal
            if all(module.memory.values()):
                for output in module.outputs:
                    lows += 1
                    frontier.append((False, module.name, output))
            else:
                for output in module.outputs:
                    highs += 1
                    frontier.append((True, module.name, output))
        elif isinstance(module, Output):
            pass
        else:
            raise ValueError()

    return lows, highs


def cycle(modules: dict[str, Module], observed: set[str]) -> set[str]:
    frontier: list[tuple[bool, str, str]] = [(False, "button", "broadcaster")]

    cycle_detected = set()

    while len(frontier) > 0:
        signal, source, name = frontier.pop(0)
        module = modules[name]

        if isinstance(module, Broadcast):
            for output in module.outputs:
                frontier.append((False, module.name, output))
        elif isinstance(module, FlipFlop):
            if signal is False:
                if module.state is False:
                    module.state = True
                    for output in module.outputs:
                        frontier.append((True, module.name, output))
                elif module.state is True:
                    module.state = False
                    for output in module.outputs:
                        frontier.append((False, module.name, output))
        elif isinstance(module, Conjunction):
            module.memory[source] = signal
            if all(module.memory.values()):
                if module.name in observed:
                    cycle_detected.add(module.name)
                for output in module.outputs:
                    frontier.append((False, module.name, output))
            else:
                for output in module.outputs:
                    frontier.append((True, module.name, output))
        elif isinstance(module, Output):
            pass
        else:
            raise ValueError()

    return cycle_detected


def part_1(puzzle: PuzzleInput) -> Any:
    modules = parse_input(puzzle.lines)
    lows, highs = 0, 0
    for _ in range(1000):
        low, high = push_button(modules)
        lows += low
        highs += high
    return lows * highs


def part_2(puzzle: PuzzleInput) -> Any:
    modules = parse_input(puzzle.lines)
    observed: dict[str, int | None] = {"rb": None, "gp": None, "ml": None, "bt": None}
    observed_names = set(observed.keys())
    pushes = 0
    cycles: list[int] = []
    while True:
        pushes += 1
        detected = cycle(modules, observed_names)
        for name in detected:
            if not observed[name]:
                observed[name] = pushes
        if all(observed.values()):
            cycles = list(v for v in observed.values() if v)
            break
    return math.lcm(*cycles)
