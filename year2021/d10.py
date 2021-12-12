import pytest
from functools import reduce
from statistics import median


def get_first_line_error(line):
    opens = {"(": ")", "{": "}", "<": ">", "[": "]"}
    closes = {v: k for k, v in opens.items()}
    stack = []
    for char in line:
        if char in opens:
            stack.append(char)
        elif char in closes:
            if stack[-1] == closes[char]:
                stack.pop()
            else:
                return 1, char
    return 0, [opens[c] for c in stack[::-1]]


def p1(inputs: str) -> int:
    results = (get_first_line_error(line) for line in inputs.splitlines())
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(points.get(r, 0) for errcode, r in results if errcode)


def p2(inputs: str) -> int:
    results = (get_first_line_error(line) for line in inputs.splitlines())
    completions = ("".join(r) for err, r in results if err == 0)
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = (reduce(lambda t, c: t * 5 + points[c], s, 0) for s in completions)
    return median(scores)


@pytest.fixture()
def example():
    return """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def test_p1(example):
    assert p1(example) == 26397


def test_p2(example):
    assert p2(example) == 288957
