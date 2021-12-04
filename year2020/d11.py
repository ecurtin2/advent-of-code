from copy import deepcopy
from itertools import count, zip_longest
from typing import Any, Generator, List

EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."


def neighborsv1(matrix: List[List[Any]], i: int, j: int) -> Generator[Any, None, None]:
    indices = [
        (i, j + 1),
        (i, j - 1),
        (i + 1, j),
        (i - 1, j),
        (i + 1, j + 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
        (i - 1, j - 1),
    ]
    i_max, j_max = len(matrix), len(matrix[0])
    for i2, j2 in indices:
        if not 0 <= i2 < i_max or not 0 <= j2 < j_max:
            continue
        yield matrix[i2][j2]


def neighborsv2(matrix: List[List[str]], i: int, j: int) -> Generator[Any, None, None]:
    indices = [
        zip_longest([], count(j + 1), fillvalue=i),
        zip_longest([], count(j - 1, -1), fillvalue=i),
        zip_longest(count(i + 1), [], fillvalue=j),
        zip_longest(count(i - 1, -1), [], fillvalue=j),
        zip(count(i + 1), count(j + 1)),
        zip(count(i + 1), count(j - 1, -1)),
        zip(count(i - 1, -1), count(j + 1)),
        zip(count(i - 1, -1), count(j - 1, -1)),
    ]
    i_max, j_max = len(matrix), len(matrix[0])
    for idx_iter in indices:
        for i2, j2 in idx_iter:
            if not 0 <= i2 < i_max or not 0 <= j2 < j_max:
                break
            if matrix[i2][j2] != FLOOR:
                yield matrix[i2][j2]
                break


def advance(matrix: List[List[Any]], get_neighbors, n_occ) -> List[List[Any]]:
    new_matrix = deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == EMPTY and not any(
                n == OCCUPIED for n in get_neighbors(matrix, i, j)
            ):
                new_matrix[i][j] = OCCUPIED
            elif (
                matrix[i][j] == OCCUPIED
                and sum(n == OCCUPIED for n in get_neighbors(matrix, i, j)) >= n_occ
            ):
                new_matrix[i][j] = EMPTY
            else:
                new_matrix[i][j] = matrix[i][j]
    return new_matrix


def solve(inp: List[str], n_occ: int, get_neighbors):
    states = [list(line) for line in inp]
    old_states = [[]]
    while states != old_states:
        old_states = states
        states = advance(old_states, get_neighbors=get_neighbors, n_occ=n_occ)
    return sum(state == OCCUPIED for row in states for state in row)


def part1(inp: List[str]) -> int:
    return solve(inp, get_neighbors=neighborsv1, n_occ=4)


def part2(inp: List[str]) -> int:
    return solve(inp, get_neighbors=neighborsv2, n_occ=5)


def test_part1():
    inp = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    assert part1(inp.splitlines()) == 37


def test_part2():
    inp = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    assert part2(inp.splitlines()) == 26
