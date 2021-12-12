import pytest
import numpy as np
from extra_itertools import neighbors
from typing import Generator


def simulate(octopi) -> Generator[np.ndarray, None, None]:
    i_max, j_max = octopi.shape
    flash_at = 9
    while True:
        octopi += 1
        flashed = set()
        should_flash = {tuple(x) for x in np.transpose((octopi > flash_at).nonzero())}
        while should_flash:
            flash = should_flash.pop()
            flashed.add(flash)
            for i, j in neighbors(*flash, i_max=i_max, j_max=j_max, diagonals=True):
                octopi[i, j] += 1
                if octopi[i, j] > flash_at and (i, j) not in flashed:
                    should_flash.add((i, j))

        for i, j in flashed:
            octopi[i, j] = 0
        yield octopi


def p1(inputs: str) -> int:
    octopi = np.array([[int(i) for i in row] for row in inputs.splitlines()])
    iterations = simulate(octopi)
    return sum((next(iterations) == 0).sum() for _ in range(100))


def p2(inputs: str) -> int:
    octopi = np.array([[int(i) for i in row] for row in inputs.splitlines()])
    iterations = simulate(octopi)
    for i, octopi in enumerate(iterations):
        if np.all(octopi == 0):
            return i + 1


def animate():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import animation

    fig = plt.figure()
    plt.axis("off")

    np.random.seed(seed=521)
    octopi = np.random.randint(low=1, high=9, size=(100, 100))
    im = plt.imshow(octopi, vmin=0, vmax=1, cmap="afmhot")

    power = 5

    def init():
        im.set_data((octopi / 9) ** power)
        return [im]

    iterations = simulate(octopi)

    def animate(i):
        title = plt.title(f"Step {i+1}")
        plt.setp(title, color="w")
        data = (next(iterations) / 9) ** power
        im.set_array(data)
        return [im]

    anim = animation.FuncAnimation(
        fig, animate, interval=45, init_func=init, frames=500, repeat=False, blit=True
    )
    anim.save("octopi.mp4", savefig_kwargs={"facecolor": "#000000"})


@pytest.fixture()
def example():
    return """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_p1(example):
    assert p1(example) == 1656


def test_p2(example):
    assert p2(example) == 195


if __name__ == "__main__":
    animate()
