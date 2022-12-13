from utils import parse_run
from extra_itertools import neighbors
from rich.console import Console
from heapq import heappop, heappush

console = Console()


def height(s: str):
    if s == "S":
        return ord("a")
    elif s == "E":
        return ord("z")
    return ord(s)


class Graph:
    def __init__(self, data: list[list[str]], backwards: bool = False):
        self.data = data
        self.connections = dict()
        for node, val in self.nodes():
            for neighbor in neighbors(
                *node, i_max=len(self.data), j_max=len(self.data[1])
            ):
                d = height(val) - height(self.data[neighbor[0]][neighbor[1]])
                if (not backwards) and (d >= -1):
                    self.connections.setdefault(node, set()).add((neighbor, 1))
                elif backwards and (d <= 1):
                    self.connections.setdefault(node, set()).add((neighbor, 1))

    def __getitem__(self, idxs):
        return self.data[idxs[0]][idxs[1]]

    def find_distances(self, start: tuple[int, int]):
        """dijkstra"""
        distances = dict()
        queue = [(0, start)]
        while queue:
            d, node = heappop(queue)
            if node in distances:
                continue
            distances[node] = d
            for n, w in set(self.connections.get(node, {})):
                if n not in distances:
                    heappush(queue, (d + w, n))
        return distances

    def show(self, mask=None):
        if mask is None:
            mask = set()
        for irow in range(len(self.data)):
            for icol in range(len(self.data[0])):
                if (irow, icol) in mask:
                    console.print(self.data[irow][icol], style="magenta", end="")
                else:
                    console.print(self.data[irow][icol], end="")
            print()

    def node_where(self, val):
        try:
            return next(n for n in self.nodes() if n[1] == val)
        except StopIteration:
            raise ValueError(f"No value = {val} found")

    def nodes(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                yield (i, j), self.data[i][j]


def p1(inputs: list[list[str]]) -> int:
    graph = Graph(inputs)
    start = graph.node_where("S")[0]
    end = graph.node_where("E")[0]
    return graph.find_distances(start)[end]


def p2(inputs: list[list[str]]) -> int:
    graph = Graph(inputs, backwards=True)
    end = graph.node_where("E")[0]
    distances = graph.find_distances(end)
    return min(d for n, d in distances.items() if graph[n] == "a")


def test_p1():
    input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    assert parse_run(p1, input) == 31


def test_p2():
    input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    assert parse_run(p2, input) == 29
