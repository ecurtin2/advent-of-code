from dataclasses import dataclass
from typing import List, Optional


@dataclass
class State:
    last_seen: int
    count: int = 1
    second_last_seen: Optional[int] = None

    def update(self, idx: int):
        self.second_last_seen = self.last_seen
        self.last_seen = idx
        self.count += 1

    @property
    def diff(self):
        return self.last_seen - self.second_last_seen


def solve(inp: List[int], N: int):
    memory = {v: State(i) for i, v in enumerate(inp)}
    current = inp[-1]

    for i in range(len(inp), N):
        if current in memory:
            if memory[current].count == 1:
                current = 0
            elif memory[current].count > 1:
                current = memory[current].diff

        if current in memory:
            memory[current].update(i)
        else:
            memory[current] = State(i)
    return current


def part1(inp: List[int]) -> int:
    return solve(inp, 2020)


def part2(inp: List[int]) -> int:
    return solve(inp, 30_000_000)


def test_part1():
    inp = """0,3,6"""
    assert part1([int(i) for i in inp.split(",")]) == 436


def test_part2():
    inp = """0,3,6"""
    assert part2([int(i) for i in inp.split(",")]) == 175594
