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
