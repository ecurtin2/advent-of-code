from dataclasses import dataclass
from enum import Enum
from math import cos, radians, sin
from typing import List, Tuple


def rotate(point: Tuple[int, int], angle: int) -> Tuple[int, int]:
    theta = radians(angle)
    new_x = point[0] * cos(theta) - point[1] * sin(theta)
    new_y = point[0] * sin(theta) + point[1] * cos(theta)
    return int(round(new_x)), int(round(new_y))


class Action(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    L = 4
    R = 5
    F = 6


@dataclass
class Ship:
    loc: Tuple[int, int]
    waypoint: Tuple[int, int]

    def update(self, action: Action, value: int):
        if action == Action.L:
            self.waypoint = rotate(self.waypoint, value)
            return
        elif action == Action.R:
            self.waypoint = rotate(self.waypoint, -value)
            return
        elif action == Action.N:
            self.loc = self.loc[0], self.loc[1] + value
        elif action == Action.S:
            self.loc = self.loc[0], self.loc[1] - value
        elif action == Action.E:
            self.loc = self.loc[0] + value, self.loc[1]
        elif action == Action.W:
            self.loc = self.loc[0] - value, self.loc[1]
        elif action == Action.F:
            self.loc = (
                self.loc[0] + self.waypoint[0] * value,
                self.loc[1] + self.waypoint[1] * value,
            )

    def update_2(self, action: Action, value: int):
        if action == Action.L:
            self.waypoint = rotate(self.waypoint, value)
            return
        elif action == Action.R:
            self.waypoint = rotate(self.waypoint, -value)
            return
        elif action == Action.N:
            self.waypoint = self.waypoint[0], self.waypoint[1] + value
        elif action == Action.S:
            self.waypoint = self.waypoint[0], self.waypoint[1] - value
        elif action == Action.E:
            self.waypoint = self.waypoint[0] + value, self.waypoint[1]
        elif action == Action.W:
            self.waypoint = self.waypoint[0] - value, self.waypoint[1]
        elif action == Action.F:
            self.loc = (
                self.loc[0] + self.waypoint[0] * value,
                self.loc[1] + self.waypoint[1] * value,
            )


def part1(inp: List[str]) -> int:
    inputs = [(Action[s[0]], int(s[1:])) for s in inp]
    ship = Ship(loc=(0, 0), waypoint=(1, 0))
    for action, value in inputs:
        ship.update(action, value)
    return abs(ship.loc[0]) + abs(ship.loc[1])


def part2(inp: List[str]) -> int:
    inputs = [(Action[s[0]], int(s[1:])) for s in inp]
    ship = Ship(loc=(0, 0), waypoint=(10, 1))
    for action, value in inputs:
        ship.update_2(action, value)
    return abs(ship.loc[0]) + abs(ship.loc[1])


def test_part1():
    inp = """F10
N3
F7
R90
F11"""
    assert part1(inp.splitlines()) == 25


def test_part2():
    inp = """F10
N3
F7
R90
F11"""
    assert part2(inp.splitlines()) == 286


def test_rotate():
    assert rotate((1, 0), 90) == (0, 1)
    assert rotate((10, 0), 90) == (0, 10)
    assert rotate((0, 1), 90) == (-1, 0)
    assert rotate((1, 1), 90) == (-1, 1)
    assert rotate((0, 1), -90) == (1, 0)
    assert rotate((10, 30), 360) == (10, 30)
