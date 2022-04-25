from collections import deque
from os.path import dirname, join
from typing import (FrozenSet, List, Mapping, Set,
                    Tuple)

from tabu_optimization import MMKCPP_TEE_TabuSearch


class CityGraph:
    """A class representing the city graph."""
    vertices: Mapping[int, Mapping[int, float]]     # {vertex_id: {connected_vertex_id: distance}, ...}
    edgeset: Set[FrozenSet[int]]                    # {{vertex_id, vertex_id}, {vertex_id, vertex_id}, ...}

    @classmethod
    def _from_bwinf_file(cls, path: str) -> 'CityGraph':
        """
        Load the CityGraph from an bwinf example file.

        Parameters
        ----------
        path : str
            The path to the bwinf file.

        """
        with open(path, 'r') as f:
            lines = f.read().split('\n')

        n, m = map(int, lines[0].split())
        return cls(
            list(range(n)),
            [(int(v), int(u), float(length)) for v, u, length in
             [line.split() for line in lines[1: m + 1]]])

    def __init__(self, vertices: List[int], edges: List[Tuple[int, int, float]]):
        self.vertices = {v: {} for v in vertices}
        self.edgeset = set()

        for edge in edges:
            v, u, len_ = edge
            self.edgeset.add(frozenset((v, u)))
            self.vertices[v][u] = len_
            self.vertices[u][v] = len_

    def w_tour(self, tour: Tuple[int, ...]) -> float:
        return sum(self.vertices[tour[i]][tour[i+1]] for i in range(len(tour)-1))

    def is_connected(self) -> bool:
        unseen = set(self.vertices.keys())
        q = deque((0,))
        while q:
            current = q.popleft()
            if current not in unseen:
                continue
            unseen.remove(current)
            for next_ in self.vertices[current]:
                q.append(next_)
        return not unseen

    def get_paths(self, days: int = 5) -> List[Tuple[float, Tuple[int, ...]]]:
        return map(lambda x: (self.w_tour(x), x), MMKCPP_TEE_TabuSearch(self.vertices, days, 100, 600, 0))


# repl
while True:
    pth = join(dirname(__file__),
                    f'beispieldaten/muellabfuhr{input("Bitte die Nummer des Beispiels eingeben [0-9]: ")}.txt')
    cg = CityGraph._from_bwinf_file(pth)
    n_days = int(input('Für wieviele Tage soll geplant werden? (5): ') or 5)
    maxlen = 0
    iterable = zip(range(1, n_days+1), cg.get_paths(n_days))
    for i, (len_, p) in iterable:
        print(f'Tag {i}: {" -> ".join(map(str, p))}, Gesamtlaenge: {len_}')
        maxlen = max(maxlen, len_)
    print(f'Maximale Lange einer Tagestour: {maxlen}')
