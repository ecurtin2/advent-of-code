from collections import deque
from itertools import islice
from typing import List


def solve_p1(inp: List[int], preamble_len: int) -> int:
    it = iter(inp)
    window = deque(islice(it, preamble_len), maxlen=preamble_len)
    while True:
        next_num = next(it)
        if any((next_num - n) in (set(window) - {n}) for n in window):
            window.append(next_num)
            continue
        else:
            return next_num


def part1(inp: List[int]) -> int:
    return solve_p1(inp, preamble_len=25)


def solve_p2(inp: List[int], preamble_len: int) -> int:
    p1_solution = solve_p1(inp, preamble_len)
    start = 0
    end = 2

    for start in range(len(inp)):
        for end in range(start + 2, len(inp)):
            nums = inp[start:end]
            total = sum(nums)
            if total == p1_solution:
                return min(nums) + max(nums)
            elif total > p1_solution:
                break


def part2(inp: List[int]) -> int:
    return solve_p2(inp, preamble_len=25)


def test_part1():
    inp = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    assert solve_p1(list(map(int, inp.splitlines())), 5) == 127


def test_part2():
    inp = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    assert solve_p2(list(map(int, inp.splitlines())), 5) == 62
