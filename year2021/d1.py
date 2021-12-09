from extra_itertools import nwise


def p1(data: list[int]):
    return sum(y > x for x, y in nwise(2, data))


def p2(data: list[int]):
    window_sums = [sum(w) for w in nwise(3, data)]
    return sum(y > x for x, y in nwise(2, window_sums))


def test_p1():
    assert p1(
        [
            199,
            200,
            208,
            210,
            200,
            207,
            240,
            269,
            260,
            263,
        ]
    )


def test_p2():
    assert (
        p2(
            [
                199,
                200,
                208,
                210,
                200,
                207,
                240,
                269,
                260,
                263,
            ]
        )
        == 5
    )
