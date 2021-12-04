from itertools import product
from typing import List


def set_bits(value, updates: dict):
    for idx, val in updates.items():
        if val == 0:
            value = value & ~(1 << idx)
        elif val == 1:
            value |= 1 << idx
    return value


def part1(inp: List[str]) -> int:
    lines = iter(inp)
    memory = {}
    for line in lines:
        if val := line.split("mask = ")[1:]:
            mask = {i: int(v) for i, v in enumerate(reversed(val[0])) if v != "X"}
            continue
        idx, val = [int(i) for i in line.split("mem[")[1].split("] = ")]
        memory[idx] = set_bits(val, mask)
    return sum(memory.values())


def get_addresses(idx: int, mask: dict) -> List[int]:
    new_idx = idx
    ones = [i for i, v in mask.items() if v == "1"]
    xs = [i for i, v in mask.items() if v == "X"]
    for i in ones:
        new_idx |= 1 << i

    for i in product([0, 1], repeat=len(xs)):
        ret_val = new_idx
        for j, position in enumerate(xs):
            if i[j] == 1:
                ret_val &= ~(1 << position)
            elif i[j] == 0:
                ret_val |= 1 << position
        yield ret_val


def part2(inp: List[str]) -> int:
    lines = iter(inp)
    memory = {}
    for line in lines:
        if val := line.split("mask = ")[1:]:
            mask = {i: v for i, v in enumerate(reversed(val[0])) if v != "0"}
            continue
        idx, val = [int(i) for i in line.split("mem[")[1].split("] = ")]
        for i in get_addresses(idx, mask):
            # print(f"mem[{i}] = {val}")
            memory[i] = val
    return sum(memory.values())


def test_part1():
    inp = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    assert part1(inp.splitlines()) == 165


def test_part2():
    inp = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    assert part2(inp.splitlines()) == 208
