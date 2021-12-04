from typing import List

from utils import product


def solve(inp: List[str], dx: int, dy: int) -> int:
    x, y = 0, 0
    ymax = len(inp)
    xmax = len(inp[0])

    count = 0
    while y < ymax - 1:
        x, y = (x + dx) % xmax, y + dy
        if inp[y][x] == "#":
            count += 1
    return count


def part1(inp: List[str]) -> int:
    return solve(inp, dx=3, dy=1)


def part2(inp: List[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = (solve(inp, dx=s[0], dy=s[1]) for s in slopes)
    return product(counts)


def test_part1():
    inp = [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]
    assert part1(inp) == 7


def test_part2():
    inp = [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]
    assert part2(inp) == 336
