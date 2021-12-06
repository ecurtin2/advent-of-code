from collections import Counter, deque


def simulate(inputs: str, doubling_time: int, n_days: int, days_to_sexual_maturity: int):
    counts = Counter(int(i) for i in inputs.split(","))
    state = deque((counts[i] for i in range(doubling_time + 1)), maxlen=doubling_time + 1)
    for _ in range(n_days):
        state[-days_to_sexual_maturity] += state[0]
        state.rotate(-1)
    return sum(state)


def p1(inputs: str) -> int:
    return simulate(inputs, doubling_time=8, n_days=80, days_to_sexual_maturity=2)


def p2(inputs: str) -> int:
    return simulate(inputs, doubling_time=8, n_days=256, days_to_sexual_maturity=2)


def test_p1():
    assert p1("3,4,3,1,2") == 5934


def test_p2():
    assert p2("3,4,3,1,2") == 26984457539