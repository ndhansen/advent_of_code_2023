from collections.abc import Iterator
import functools
import multiprocessing as mp
from dataclasses import dataclass
from typing import Any, NamedTuple
import itertools
import math

from tqdm import tqdm
from aoc.utils.contents import PuzzleInput


class Vector3D(NamedTuple):
    x: float
    y: float
    z: float

    def xy_dist_square(self, other: "Vector3D") -> float:
        x_diff = other.x - self.x
        y_diff = other.y - self.y
        return x_diff**2 + y_diff**2

    def scale(self, size: int) -> "Vector3D":
        return Vector3D(self.x * size, self.y * size, self.z * size)

    def add(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def sub(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )


@dataclass(frozen=True)
class Hail:
    position: Vector3D
    vector: Vector3D

    def __lt__(self, other: "Hail") -> bool:
        ours = self.position.x**2 + self.position.y**2 + self.position.z**2
        theirs = other.position.x**2 + other.position.y**2 + other.position.z**2
        return ours < theirs

def parse_line(line: str) -> Hail:
    left, right = line.split(" @ ", maxsplit=1)
    px, py, pz = left.split(", ")
    vx, vy, vz = right.split(", ")
    position = Vector3D(float(px), float(py), float(pz))
    vector = Vector3D(float(vx), float(vy), float(vz))
    return Hail(position, vector)


def parse_input(lines: list[str]) -> list[Hail]:
    return list(map(parse_line, lines))


def xy_line_intersect(first: Hail, second: Hail) -> Vector3D | None:
    gradient_first = first.vector.y / first.vector.x
    first_y_intercept = (first.position.x * (-gradient_first)) + first.position.y
    gradient_second = second.vector.y / second.vector.x
    second_y_intercept = (second.position.x * (-gradient_second)) + second.position.y

    if gradient_first == gradient_second and first_y_intercept == second_y_intercept:
        return Vector3D(0.0, first_y_intercept, 0.0)

    if gradient_first == gradient_second:
        return None

    x_intercept = (second_y_intercept - first_y_intercept) / (gradient_first - gradient_second)
    y_intercept = (gradient_first * x_intercept) + first_y_intercept
    return Vector3D(x_intercept, y_intercept, 0.0)


def xy_intercept_in_past(hail: Hail, intersect: Vector3D) -> bool:
    future_hail_pos = Vector3D(hail.position.x + hail.vector.x, hail.position.y + hail.vector.y, hail.position.z + hail.vector.z)
    if hail.position.xy_dist_square(intersect) < future_hail_pos.xy_dist_square(intersect):
        return True
    return False


def part_1(puzzle: PuzzleInput) -> Any:
    hail = parse_input(puzzle.lines)
    min_area = 200000000000000
    max_area = 400000000000000
    total = 0
    for first, second in itertools.combinations(hail, 2):
        if intersect := xy_line_intersect(first, second):
            if xy_intercept_in_past(first, intersect):
                continue
            if xy_intercept_in_past(second, intersect):
                continue
            if intersect.x < min_area:
                continue
            if intersect.y < min_area:
                continue
            if intersect.x > max_area:
                continue
            if intersect.y > max_area:
                continue
            total += 1

    return total


def cross(a: Vector3D, b: Vector3D) -> Vector3D:
    return Vector3D(
        a.y * b.z - b.y * a.z,
        a.z * b.x - b.z * a.x,
        a.x * b.y - b.x * a.y,
    )

def dot(a: Vector3D, b: Vector3D) -> float:
    return a.x * b.x + a.y * b.y + a.z * b.z


def norm(a: Vector3D) -> Vector3D:
    length = math.sqrt(a.x**2 + a.y**2 + a.z**2)
    return Vector3D(
        a.x / length,
        a.y / length,
        a.z / length,
    )


def is_coplanar(hail: Hail, stone: Hail) -> bool:
    between = hail.position.sub(stone.position)
    return dot(between, cross(stone.vector, hail.vector)) == 0.0


def perspective_interception(vector: Vector3D, hail: list[Hail]) -> bool:
    # Attempt at optimization
    for i, j in itertools.pairwise(range(4)):
        first = Hail(hail[i].position, hail[i].vector.add(vector))
        second = Hail(hail[j].position, hail[j].vector.add(vector))
        if not is_coplanar(first, second):
            return False

    return True

    hail_modified = [Hail(h.position, h.vector.add(vector)) for h in hail]
    for left, right in itertools.combinations(hail_modified, 2):
        if not is_coplanar(left, right):
            return False
    return True


def brute_force_vectors(hail: list[Hail], limit: int = 1000) -> Vector3D:
    for x, y, z in tqdm(itertools.product(range(-limit, limit+1), repeat=3), total=(2*limit)**3):
        change = Vector3D(x, y, z)
        if perspective_interception(change, hail):
            return change
    raise ValueError()


def inner(hail: list[Hail], x_low: int, x_high: int, limit: int) -> Vector3D | None:
    for x in range(x_low, x_high):
        for y, z in itertools.product(range(-limit, limit+1), repeat=2):
            change = Vector3D(x, y, z)
            if perspective_interception(change, hail):
                return change

def brute_force_vectors_mp(hail: list[Hail], limit: int = 1000, processors: int = 8) -> Vector3D:
    xs = [i * processors for i in range(processors+1)]
    with mp.Pool(processors) as pool:
        args = []
        for x_low, x_high in itertools.pairwise(xs):
            args.append((hail, x_low, x_high, limit))
        print(pool.starmap(inner, args))
    raise ValueError()


def get_intersection(hail: list[Hail], limit: int = 1000) -> int:
    hail_positions = []
    hail_vectors = []
    hail_simplified: list[tuple[int, int]] = []
    for h in hail:
        pos_sum = int(h.position.x + h.position.y + h.position.z)
        hail_positions.append(pos_sum)
        v_sum = int(h.vector.x + h.vector.y + h.vector.z)
        hail_vectors.append(v_sum)
        hail_simplified.append((pos_sum, v_sum))

    for i in range(-limit, limit+1):
        if i in hail_vectors:
            continue

        n_a = []
        for pos, vec in hail_simplified:
            change = abs(vec-i)
            n_a.append((pos % change, change))

        # Make the set coprime
        n_s = []
        a_s = []
        seen = set()
        for n, a in n_a:
            if a in seen:
                continue
            if len(seen) == 0 or all(math.gcd(a, other) == 1 for other in seen):
                n_s.append(n)
                a_s.append(a)
                seen.add(a)

        origin = chinese_remainder(a_s, n_s)
        for pos, vec in hail_simplified:
            time = (pos-origin) / -(vec-i)
            if time <= 0 or math.floor(time) != time:
                break
        else:
            return origin

    raise ValueError()


def get_intersection_line(first: Hail, second: Hail) -> Iterator[Hail]:
    # for t_1, t_2 in ((5, 3),):
    for t_1, t_2 in tqdm(itertools.permutations(range(1, 10000), 2), total=10000**2):
        p_1 = first.position.add(first.vector.scale(t_1))
        p_2 = second.position.add(second.vector.scale(t_2))
        if t_1 < t_2:
            new_hail = Hail(p_1, p_2.sub(p_1))
        else:
            new_hail = Hail(p_2, p_1.sub(p_2))
        yield new_hail


def chinese_remainder(n: list[int], a: list[int]) -> int:
    """Stolen from Rosetta Code"""
    sum = 0
    prod = functools.reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * _mul_inv(p, n_i) * p
    return sum % prod
 

def _mul_inv(a: int, b: int) -> int:
    """Stolen from Rosetta Code"""
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        div, mod = divmod(a, b)
        a, b = b, mod
        x0, x1 = x1 - div * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part_2(puzzle: PuzzleInput) -> Any:
    hail = parse_input(puzzle.lines)
    return get_intersection(hail, limit=1000)
