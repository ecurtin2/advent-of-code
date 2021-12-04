from itertools import product

from typing import List, Set, Tuple, Generator


def neighbors(coords: Tuple[int, int, int]) -> Generator[Tuple[int], None, None]:
    for coords2 in product(range(-1, 2), repeat=len(coords)):
        if not all(x == 0 for x in coords2):
            yield tuple(x + x1 for x, x1 in zip(coords, coords2))


def cubes_of_life(start_cubes: Set[Tuple[int, ...]], iterations: int):
    active_cubes = start_cubes
    for _ in range(iterations):
        updates = {}
        for cube in active_cubes:
            for neighbor in neighbors(cube):
                if neighbor in updates:
                    updates[neighbor] += 1
                else:
                    updates[neighbor] = 1

        new_active_cubes = set()
        for loc, val in updates.items():
            if val == 3:
                new_active_cubes.add(loc)
            elif val == 2 and loc in active_cubes:
                new_active_cubes.add(loc)
        active_cubes = new_active_cubes

    return len(active_cubes)


def part1(inp: List[str]) -> int:
    init = {
        (x, y, 0)
        for y, row in enumerate(inp)
        for x, val in enumerate(row)
        if val == "#"
    }
    return cubes_of_life(init, iterations=6)


def part2(inp: List[str]) -> int:
    init = {
        (x, y, 0, 0)
        for y, row in enumerate(inp)
        for x, val in enumerate(row)
        if val == "#"
    }
    return cubes_of_life(init, iterations=6)


def test_part1():
    inp = """.#.
..#
###"""
    assert part1(inp.splitlines()) == 112


def test_part2():
    inp = """.#.
..#
###"""
    assert part2(inp.splitlines()) == 848
