from collections import Counter
from typing import Callable, TypeVar
import pytest

T = TypeVar("T")
Splitter = Callable[[T, list[T]], int]


class Decoder:
    """Decoder to translate from one basis to another

    The decoder is initialized in a given basis, then when .fit is called,
    it will generate a mapping from the basis in .fit to the basis in __init__.
    Then the transform method will transform new input from the .fit basis to the
    __init__ basis.

    The splitter functions must be independent of basis and the tuple of results of applying
    them to each value must uniquely identify that value.
    """

    def __init__(self, reference: list[T], splitters: list[Splitter]):
        self.ref = reference
        self.splitters = splitters

        self.table = dict()
        self.decoder = None

        # Create a lookup table based on output of splitter functions
        for i, val in enumerate(self.ref):
            k = tuple(splitter(val, self.ref) for splitter in self.splitters)
            self.table[k] = i

        # If results of splitters are non unique (to fix, add more splitters!)
        if len(self.ref) != len(self.table):
            raise ValueError(f"Splitters not sufficient to split")

    def fit(self, values: list[T]):
        self.decoder = {}
        for val in values:
            k = tuple(splitter(val, values) for splitter in self.splitters)
            self.decoder["".join(sorted(val))] = self.table[k]
        return self

    def transform(self, values: list[T]):
        if self.decoder is None:
            raise ValueError(f"Need to fit on values before transform!")
        return [self.decoder["".join(sorted(v))] for v in values]


def join_digits(x: list[int]) -> int:
    return int("".join(map(str, x)))


def split_strip(s: str) -> list[str]:
    return [chunk.strip() for chunk in s.split()]


decoder = Decoder(
    reference=[
        "abcefg",
        "cf",
        "acdeg",
        "acdfg",
        "bcdf",
        "abdfg",
        "abdefg",
        "acf",
        "abcdefg",
        "abcdfg",
    ],
    splitters=[
        lambda val, rest: len(val),
        lambda val, rest: sum(set(val).issubset(set(r)) for r in rest),
        lambda val, rest: sum(set(val).issuperset(set(r)) for r in rest),
    ],
)


def p1(inputs: str) -> int:
    in_out = [l.split("|") for l in inputs.splitlines()]
    counts = Counter(
        digit
        for i, o in in_out
        for digit in decoder.fit(split_strip(i)).transform(split_strip(o))
    )
    return counts[1] + counts[4] + counts[7] + counts[8]


def p2(inputs: str) -> int:
    in_out = [l.split("|") for l in inputs.splitlines()]
    return sum(
        join_digits(decoder.fit(split_strip(i)).transform(split_strip(o)))
        for i, o in in_out
    )


@pytest.fixture()
def example():
    return """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def test_p1(example):
    assert p1(example) == 26


def test_p2_1():
    assert (
        p2(
            """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""
        )
        == 5353
    )


def test_p2(example):
    assert p2(example) == 61229
