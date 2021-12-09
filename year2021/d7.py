from typing import Callable
import numpy as np


def solve(inputs: str, fuel_cost: Callable[[np.array], np.array]) -> int:
    crabs = np.array(inputs.split(",")).astype(np.int32)
    mean = int(np.mean(crabs))
    med = np.median(crabs)
    min_ = min(mean, med) - 2
    max_ = max(mean, med) + 2
    xs = np.arange(min_, max_)
    distances = np.abs(crabs - xs[:, np.newaxis])
    return fuel_cost(distances).min()


def p1(inputs: str) -> int:
    return solve(inputs, fuel_cost=lambda d: d.sum(axis=1).astype(np.int32))


def p2(inputs: str) -> int:
    # fuel cost in p2 is the d'th triangular number
    return solve(
        inputs, fuel_cost=lambda d: (d * (d + 1) / 2).astype(np.int32).sum(axis=1)
    )


def test_p1():
    assert p1("16,1,2,0,4,2,7,1,2,14") == 37


def test_p2():
    assert p2("16,1,2,0,4,2,7,1,2,14") == 168
