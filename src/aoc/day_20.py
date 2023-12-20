from dataclasses import dataclass, field
from typing import Any
from enum import Enum
from collections import defaultdict

from aoc.utils.contents import PuzzleInput


# True is HIGH, False is LOW


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
        return FlipFlop(name=identifier[1:], kind=ModuleType.FLIP_FLOP, outputs=tuple(outputs))
    elif identifier[0] == "&":
        return Conjunction(name=identifier[1:], kind=ModuleType.FLIP_FLOP, outputs=tuple(outputs), memory={})
    else:
        return Broadcast(name=identifier, kind=ModuleType.FLIP_FLOP, outputs=tuple(outputs))


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


def push_button(modules: dict[str, Module]) -> tuple[int, int, bool]:
    lows = 1  # 1 for the button push
    highs = 0
    done = False
    frontier: list[tuple[bool, str, str]] = [(False, "button", "broadcaster")]

    while len(frontier) > 0:
        signal, source, name = frontier.pop(0)
        module = modules[name]

        if isinstance(module, Broadcast):
            for output in module.outputs:
                frontier.append((False, module.name, output))
                lows += 1
        elif isinstance(module, FlipFlop):
            if signal == False:
                if module.state == False:
                    module.state = True
                    for output in module.outputs:
                        highs += 1
                        frontier.append((True, module.name, output))
                elif module.state == True:
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
            if signal == False:
                done = True
        else:
            raise ValueError()

    return lows, highs, done


def part_1(puzzle: PuzzleInput) -> Any:
    modules = parse_input(puzzle.lines)
    lows, highs = 0, 0
    for _ in range(1000):
        low, high, _ = push_button(modules)
        lows += low
        highs += high
    return lows * highs


def part_2(puzzle: PuzzleInput) -> Any:
    modules = parse_input(puzzle.lines)
    pushes = 0
    while True:
        pushes += 1
        _, __, done = push_button(modules)
        if done:
            break
    return pushes

# %a -> %b -> %c
# To get c to send a high: 4 (2^2)
# TO get c to send a low: 8 (2^3)
#
# %a -> %b, &c
# %b -> &c
# %a -> %b -> &c
# %a -> &c
# 1 low: a on, b off, c[a=high,b=low]
# 2 low: a off, b on, c[a=low,b=high]
# 3 low: a on, b on, c[a=high,b=high]
#
# %a -> %b, %c, &d
# %b -> %c, &d
# %c -> &d
# a on every 1st, 3rd, 5th cycle etc
# a off every 2st, 4rd, 6th cycle etc
# b on every 2nd, 6th, 10th cycle etc
# b off every 4nd, 8th, 12th cycle etc
# c on every 4th, 12th, 20th cycle etc
# c off every 8th, 16th, 24th cycle etc
# 01010101010101010101
# 00110011001100110011
# 00001111000011110000
