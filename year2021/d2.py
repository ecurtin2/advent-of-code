from enum import Enum


class Direction(Enum):
    forward = "forward"
    down = "down"
    up = "up"


def p1(data: list[tuple[Direction, int]]) -> int:
    pos = 0, 0
    for dir, amt in data:
        if dir == Direction.up:
            pos = pos[0], pos[1] - amt
        elif dir == Direction.down:
            pos = pos[0], pos[1] + amt
        elif dir == Direction.forward:
            pos = pos[0] + amt, pos[1]
    return pos[0] * pos[1]


def p2(data: list[tuple[Direction, int]]) -> int:
    pos = 0, 0
    aim = 0
    for dir, amt in data:
        if dir == Direction.up:
            aim -= amt
        elif dir == Direction.down:
            aim += amt
        elif dir == Direction.forward:
            pos = pos[0] + amt, pos[1] + aim * amt
    return pos[0] * pos[1]
