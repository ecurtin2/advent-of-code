from typing import List

from utils import diff


def get_seat_id(s: str) -> int:
    row = int(s[:7].replace("B", "1").replace("F", "0"), 2)
    col = int(s[7:].replace("L", "0").replace("R", "1"), 2)
    return row * 8 + col


def part1(inp: List[str]) -> int:
    return max(map(get_seat_id, inp))


def part2(inp: List[str]) -> int:
    seat_ids = sorted(map(get_seat_id, inp))
    for val, d in zip(seat_ids, diff(seat_ids)):
        if d != 1:
            return val + 1


def test_get_seat_id():
    assert get_seat_id("BFFFBBFRRR") == 567
    assert get_seat_id("FFFBBBFRRR") == 119
    assert get_seat_id("BBFFBBFRLL") == 820
