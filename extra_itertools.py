from collections import deque
from typing import TypeVar, Iterable, Generator, Callable, List

T = TypeVar("T")


def nwise(
    n, iterable: Iterable[T], step: int = 1
) -> Generator[tuple[T, ...], None, None]:
    """Yield length-n chunks of iterable advancing by step"""
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


def split(
    iterable: Iterable,
    on: Callable = lambda s: s.strip() == "",
    include_edges: bool = False,
) -> Generator[List, None, None]:
    result = []
    for thing in iterable:
        if on(thing):
            if include_edges:
                result.append(thing)
            yield result
            result = []
        else:
            result.append(thing)

    # last chunk if exists
    if result:
        yield result


def take_until(pred, iterable):
    """Yield until the predicate is true"""
    for val in iterable:
        yield val
        if pred(val):
            break


def last(iterable, default=0):
    """Return the last value in iterable, or default"""
    val = default
    for val in iterable:
        pass
    return val