def display(points: list[tuple[int, int]]):
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    for row in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            if (col, row) in points:
                print("█", end="")
            else:
                print(" ", end="")
        print()


def fold(point: tuple[int, int], dir: str, val: int):
    if dir == "x" and point[0] > val:
        return 2 * val - point[0], point[1]
    elif dir == "y" and point[1] > val:
        return point[0], 2 * val - point[1]
    return point


def apply_folds(inputs, only_first: bool = False) -> set[tuple[int, int]]:
    # parse
    lines = iter(inputs.splitlines())
    points = set()
    for l in lines:
        if not l.strip():
            break
        points.add(tuple(int(i) for i in l.split(",")))
    folds = [l.split()[-1].split("=") for l in lines]

    # do folds
    for d, v in folds:
        points = {fold(p, d, int(v)) for p in points}
        if only_first:
            break
    return points


def p1(inputs: str) -> int:
    return len(apply_folds(inputs, only_first=True))


def p2(inputs: str):
    print()
    display(apply_folds(inputs))
    print()


def test_p1(example):
    assert p1(example) == 17
