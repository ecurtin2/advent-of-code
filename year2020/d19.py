from typing import List, Union, Dict
from utils import split
import re


def part1(inp: List[str]) -> int:
    rules_str, messages = split(inp)
    rules: Dict[int, Union[str, List[List[int]]]] = {}
    for line in rules_str:
        k, rest = line.split(":")
        if '"' in rest:
            rules[int(k)] = rest.replace('"', "").strip()
        else:
            rules[int(k)] = [
                [int(i) for i in line.split(" ") if i] for line in rest.split("|")
            ]

    while True:
        resolved_rules = {k: v for k, v in rules.items() if isinstance(v, str)}
        unresolved_rules = {k: v for k, v in rules.items() if not isinstance(v, str)}
        if not unresolved_rules:
            break

        rules = {
            k: [[resolved_rules.get(v, v) for v in sr] for sr in v]
            for k, v in unresolved_rules.items()
        }
        for k, v in rules.items():
            if all(isinstance(val, str) for sr in v for val in sr):
                rules[k] = "(" + "|".join(("".join(s for s in sr) for sr in v)) + ")"

    return sum(
        (match := re.match(rules[0], m)) is not None and (match.span(0) == (0, len(m)))
        for m in messages
    )


def part2(inp: List[str]) -> int:
    raise NotImplementedError


def test_part1():
    inp = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    assert part1(inp.splitlines()) == 2


def test_part2():
    inp = """"""
    assert part2(inp.splitlines()) == 1
