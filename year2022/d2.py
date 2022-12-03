from utils import parse_run
from enum import IntEnum, Enum


class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


DRAW = 3
WIN = 6
LOSE = 0

DECODE_THEM = {"A": Hand.ROCK, "B": Hand.PAPER, "C": Hand.SCISSORS}
DECODE_ME = {"X": Hand.ROCK, "Y": Hand.PAPER, "Z": Hand.SCISSORS}


class Code(str, Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


def score(p1: int, p2: int) -> tuple[int, int]:
    match p1 - p2:
        case 0:
            return p1 + DRAW, p2 + DRAW
        case 1 | -2:
            return p1 + WIN, p2 + LOSE
        case -1 | 2:
            return p1 + LOSE, p2 + WIN
        case _:
            raise ValueError(f"Invalid scores: {p1=} | {p2=}")


def p1(inputs: list[list[str]]):
    scores = [score(DECODE_THEM[them], DECODE_ME[me]) for them, me in inputs]
    return sum(s[1] for s in scores)


def decode_2(them: str, me: str) -> Hand:
    t = DECODE_THEM[them]
    match (t, me):
        case (Hand.ROCK, Code.DRAW) | (Hand.PAPER, Code.LOSE) | (
            Hand.SCISSORS,
            Code.WIN,
        ):
            return Hand.ROCK
        case (Hand.PAPER, Code.DRAW) | (Hand.SCISSORS, Code.LOSE) | (
            Hand.ROCK,
            Code.WIN,
        ):
            return Hand.PAPER
        case (Hand.SCISSORS, Code.DRAW) | (Hand.ROCK, Code.LOSE) | (
            Hand.PAPER,
            Code.WIN,
        ):
            return Hand.SCISSORS
        case _:
            raise ValueError("Not valid")


def p2(inputs: list[list[str]]):
    scores = [score(DECODE_THEM[them], decode_2(them, me)) for them, me in inputs]
    return sum(s[1] for s in scores)


def test_p1():
    assert 15 == parse_run(
        p1,
        inputs="""A Y
B X
C Z""",
    )


def test_p2():
    assert 12 == parse_run(
        p2,
        inputs="""A Y
B X
C Z""",
    )
