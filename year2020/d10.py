from collections import Counter
from functools import lru_cache
from typing import List, Tuple

from utils import diff


def part1(inp: List[int]) -> int:
    c = Counter(diff([0] + sorted(inp) + [max(inp) + 3]))
    return c[1] * c[3]


@lru_cache
def solve_part2(choices: Tuple[int], curr_idx: int = 0) -> int:
    if not choices:
        return 0
    if curr_idx == len(choices) - 1:
        return 1
    return sum(
        solve_part2(choices, i + curr_idx)
        for i, val in enumerate(choices[curr_idx:])
        if 1 <= val - choices[curr_idx] <= 3
    )


def part2(inp: List[int]) -> int:
    return solve_part2(tuple([0] + sorted(inp) + [max(inp) + 3]))


def test_part1():
    inp = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    assert part1([int(i) for i in inp.splitlines()]) == 220


def test_part2():
    inp = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    assert part2([int(i) for i in inp.splitlines()]) == 19208
