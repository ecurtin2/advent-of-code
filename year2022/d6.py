from extra_itertools import nwise
from utils import parse_run
import pytest


def dropwhile(predicate, iterable):
    # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            yield x
            break
    for x in iterable:
        yield x


def find_marker(input: str, size: int) -> int:
    return (
        next(
            dropwhile(
                lambda x: len(set(x[1])) != len(x[1]), enumerate(nwise(size, input))
            )
        )[0]
        + size
    )


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
