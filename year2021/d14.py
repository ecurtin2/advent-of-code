from collections import Counter
import numpy as np
from numpy.linalg import matrix_power

import pytest


def solve(inputs: str, n: int) -> int:
    polymer, _, *lines = inputs.splitlines()
    lines = [line.split("->") for line in lines if line.strip()]

    conversions = {l.strip(): r.strip() for l, r in lines}
    i_to_pair = dict(enumerate(conversions))
    pair_to_i = {v: k for k, v in i_to_pair.items()}
    n_pairs = len(conversions)

    transition_matrix = np.zeros((n_pairs, n_pairs), dtype=np.int64)
    for in_pair, out in conversions.items():
        transition_matrix[pair_to_i[out + in_pair[1]], pair_to_i[in_pair]] = 1
        transition_matrix[pair_to_i[in_pair[0] + out], pair_to_i[in_pair]] = 1

    # Setup initial state
    initial_state = np.zeros(n_pairs, dtype=np.int64)
    counts = Counter(''.join(p) for p in zip(polymer, polymer[1:]))
    for pair, count in counts.items():
        initial_state[pair_to_i[pair]] = count

    # Apply transition matrix n times
    final_state = matrix_power(transition_matrix, n) @ initial_state

    # Counting: use the first part of pair and add in the last element
    elem_counts = sum(
        (Counter({i_to_pair[i][0]: v}) for i, v in enumerate(final_state)),
        start=Counter({polymer[-1]: 1}),
    )
    return elem_counts.most_common()[0][1] - elem_counts.most_common()[-1][1]


def p1(inputs: str) -> int:
    return solve(inputs, n=10)


def p2(inputs: str):
    return solve(inputs, n=40)


@pytest.fixture()
def example():
    return """NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
    """


def test_p1(example):
    assert p1(example) == 1588


def test_p2(example):
    assert p2(example) == 2188189693529
