from extra_itertools import nwise
from utils import parse_run
from typing import Callable, TypeVar, Iterable
import pytest


T = TypeVar("T")


def first_false(predicate: Callable[[T], bool], iterable: Iterable[T], default: T) -> tuple[int, T]:
    for i, val in enumerate(iterable):
        if not predicate(val):
            return i, val
    return -1, default


def find_marker(input: str, size: int) -> int:
    return first_false(lambda x: len(set(x)) != len(x), nwise(size, input), default=())[0] + size


def p1(inputs: str) -> int:
    return find_marker(inputs, 4)


def p2(inputs: str) -> int:
    return find_marker(inputs, 14)


@pytest.mark.parametrize(
    ("input", "expect"),
    [
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
    ],
)
def test_p1(input, expect):
    assert parse_run(p1, input) == expect


@pytest.mark.parametrize(
    ("input", "expect"),
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
    ],
)
def test_p2(input, expect):
    assert parse_run(p2, input) == expect
