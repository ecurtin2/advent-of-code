from collections import deque
from typing import TypeVar, Iterable, Generator

T = TypeVar("T")


def nwise(n, iterable: Iterable[T]) -> Generator[tuple[T, ...], None, None]:
    d: deque[T] = deque(maxlen=n)
    it = iter(iterable)
    for _ in range(n):
        d.append(next(it))

    yield tuple(d)
    for val in it:
        d.append(val)
        yield tuple(d)


def neighbors(i: int, j: int, i_max: int, j_max: int, diagonals: bool = False):
    points = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    if diagonals:
        points += [(i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]
    for p in points:
        if 0 <= p[0] < i_max and 0 <= p[1] < j_max:
            yield p
