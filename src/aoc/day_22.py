import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Mapping, NamedTuple

from aoc.utils.common import Coord
from aoc.utils.contents import PuzzleInput


class Coord3D(NamedTuple):
    x: int
    y: int
    z: int


class BrickSnapshot(NamedTuple):
    start: Coord3D
    end: Coord3D

    def height(self) -> int:
        return abs(self.end.z - self.start.z) + 1

    def get_shadow(self) -> list[Coord]:
        points = []
        x_dir = 1 if self.start.x < self.end.x else -1
        for x in range(self.start.x, self.end.x + x_dir, x_dir):
            y_dir = 1 if self.start.y < self.end.y else -1
            for y in range(self.start.y, self.end.y + y_dir, y_dir):
                points.append(Coord(x, y))

        return points

    def to_brick(self, z: int) -> "Brick":
        x_dir = 1 if self.start.x < self.end.x else -1
        y_dir = 1 if self.start.y < self.end.y else -1
        z_diff = abs(self.end.z - self.start.z)
        x_range = range(self.start.x, self.end.x + x_dir, x_dir)
        y_range = range(self.start.y, self.end.y + y_dir, y_dir)
        z_range = range(z, z + 1 + z_diff)

        points = []
        for x, y, z in itertools.product(x_range, y_range, z_range):
            points.append(Coord3D(x, y, z))

        return Brick(tuple(points))


@dataclass(frozen=True)
class Brick:
    cubes: tuple[Coord3D, ...]

    def get_above(self) -> tuple[Coord3D, ...]:
        points = []
        for cube in self.cubes:
            points.append(Coord3D(cube.x, cube.y, cube.z + 1))

        return tuple(c for c in points if c not in self.cubes)

    def get_below(self) -> tuple[Coord3D, ...]:
        points = []
        for cube in self.cubes:
            points.append(Coord3D(cube.x, cube.y, cube.z - 1))

        return tuple(c for c in points if c not in self.cubes)


@dataclass(frozen=True)
class Dependency:
    brick: Brick
    supports: set[Brick]
    supported_by: set[Brick]


def parse_line(line: str) -> BrickSnapshot:
    left, right = line.split("~")
    x, y, z = left.split(",")
    start = Coord3D(int(x), int(y), int(z))
    x, y, z = right.split(",")
    end = Coord3D(int(x), int(y), int(z))
    return BrickSnapshot(start, end)


def parse_puzzle(lines: list[str]) -> list[BrickSnapshot]:
    bricks = list(map(parse_line, lines))
    bricks.sort(key=lambda b: b.start.z)
    return bricks


def get_min_height(heightmap: dict[Coord, int], brick: BrickSnapshot) -> int:
    heights = [heightmap[c] for c in brick.get_shadow()]
    return max(heights)


def drop_bricks(bricks: list[BrickSnapshot]) -> list[Brick]:
    heightmap: dict[Coord, int] = defaultdict(lambda: 1)

    fallen = []
    for brick in bricks:
        min_height = get_min_height(heightmap, brick)

        for point in brick.get_shadow():
            heightmap[point] = min_height + brick.height()

        fallen.append(brick.to_brick(min_height))

    return fallen


def get_support_graph(bricks: list[Brick]) -> dict[Brick, Dependency]:
    brickmap: dict[Coord3D, Brick] = {}
    for brick in bricks:
        for cube in brick.cubes:
            brickmap[cube] = brick

    dependency_graph: dict[Brick, Dependency] = {}
    for brick in bricks:
        supports: set[Brick] = set()
        supported_by: set[Brick] = set()
        for above in brick.get_above():
            if above in brickmap:
                supports.add(brickmap[above])
        for below in brick.get_below():
            if below in brickmap:
                supported_by.add(brickmap[below])

        dependency_graph[brick] = Dependency(brick, supports, supported_by)

    return dependency_graph


def to_graphviz(graph: dict[Brick, Dependency]) -> None:
    index = {b: i for i, b in enumerate(graph.keys())}
    number = 0
    for _, dependency in graph.items():
        if len(dependency.supports) == 0:
            print(f"{number};")
        else:
            for dependant in dependency.supports:
                print(f"{number} -> {index[dependant]};")
        number += 1


def part_1(puzzle: PuzzleInput) -> Any:
    bricks_snapshot = parse_puzzle(puzzle.lines)
    bricks = drop_bricks(bricks_snapshot)
    dependencies = get_support_graph(bricks)
    can_be_deleted = set()
    for brick in bricks:
        dependency = dependencies[brick]

        other_bricks = dependency.supports
        can_add = True
        for other in other_bricks:
            assert brick in dependencies[other].supported_by
            if len(dependencies[other].supported_by) == 1:
                can_add = False
                break

        if can_add:
            can_be_deleted.add(brick)

    # to_graphviz(dependencies)
    return len(can_be_deleted)


def bricks_would_fall(brick: Brick, graph: Mapping[Brick, Dependency]) -> int:
    if len(graph[brick].supports) == 0:
        return 0

    toppled = {brick}
    frontier = graph[brick].supports
    while len(frontier) > 0:
        current = frontier.pop()
        if len(graph[current].supported_by - toppled) == 0:
            frontier.update(graph[current].supports)
            toppled.add(current)

    return len(toppled) - 1


def part_2(puzzle: PuzzleInput) -> Any:
    bricks_snapshot = parse_puzzle(puzzle.lines)
    bricks = drop_bricks(bricks_snapshot)
    dependencies = get_support_graph(bricks)

    cant_be_deleted = []
    for brick in bricks:
        dependency = dependencies[brick]

        other_bricks = dependency.supports
        can_add = True
        for other in other_bricks:
            assert brick in dependencies[other].supported_by
            if len(dependencies[other].supported_by) == 1:
                can_add = False
                break

        if not can_add:
            cant_be_deleted.append(brick)

    total = 0
    for brick in cant_be_deleted:
        total += bricks_would_fall(brick, dependencies)
    return total
