from collections import Counter
from os.path import dirname, join
from typing import (FrozenSet, Iterable, List, Mapping, Set,
                    Tuple)

from tabu_optimization import MMKCPP_TEE_TabuSearch
from utility import remove_by_exp


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

    def _contains_all_edges(self, paths: Iterable[Iterable[int]]) -> bool:
        # convert all paths into an edgesets
        flattened = tuple(j for path in paths for j in path)
        edges = set(frozenset((flattened[i], flattened[i+1])) for i in range(len(flattened)-1))
        # check if all edges are contained in the resulting edgeset
        for edge in self.edgeset:
            if edge not in edges:
                return False
        return True
    

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
        # get paths using bfs-type algorithm
        visited: Mapping[int, Tuple[float, List[int]]] = {}  # {visited_node_id: (length, path)}
        paths: List[Tuple[int, ...]] = []  # [(path), ...]
        queue: List[Tuple[float, Tuple[int, ...]]] = [(0.0, [0])]  # [(distance, path), ...]

        try:
            while not self._contains_all_edges(paths):
                queue.sort()
                current_length, current_path = queue.pop(0)
                if current_path[-1] in visited:  # check if path meets another path
                    paths.append((*visited[current_path[-1]], *reversed(current_path[:-1])))
                    visited[current_path[-1]] = current_path

                    # remove the path merging into the current path
                    remove_by_exp(lambda x: x[1][-1] == current_path[-2], queue)
                    continue
                if len(self.vertices[current_path[-1]]) == 1:  # check if it's a dead end
                    paths.append((*current_path, *reversed(current_path[:-1])))
                    continue
                visited[current_path[-1]] = current_path
                for next_node_id in self.vertices[current_path[-1]]:
                    if next_node_id == (current_path[-2] if len(current_path) > 1 else None):  # skip going backwards
                        continue
                    queue.append((self.vertices[current_path[-1]][next_node_id] + current_length,
                                  current_path + [next_node_id]))
        except IndexError as e:
            raise ValueError(f'Keine Pfade gefunden! (Mehrere unverbundene Straßennetze). ({e})')

        # remove unneeded paths
        paths.sort(key=lambda path: sum(self.vertices[path[i]][path[i+1]] for i in range(len(path)-1)), reverse=True)
        edgecounts = Counter(frozenset((path[i], path[i+1])) for path in paths for i in range(len(path)-1))
        keys = edgecounts.keys()
        for path in paths:
            edgecount = Counter(frozenset((path[i], path[i+1])) for i in range(len(path)-1))
            tmp = edgecounts-edgecount
            if not any(v < 1 for v in tmp.values()) and tmp.keys() == keys:
                paths.remove(path)
                edgecounts.subtract(edgecount)

        # merge paths while they are > target_n_days
        while len(paths) > days:
            paths.sort(key=lambda path: sum(self.vertices[path[i]][path[i+1]] for i in range(len(path)-1)))
            first = paths.pop(0)
            second = paths[0]
            paths[0] = (*first, *second[1:])

        # pad to length of target_n_days
        while len(paths) < days:
            paths.append((0,))
        
        return map(lambda x: (self.w_tour(x), x), MMKCPP_TEE_TabuSearch(self.vertices, paths, maxRunningTime=10))


# repl
while True:
    try:
        pth = join(dirname(__file__),
                        f'beispieldaten/muellabfuhr{input("Bitte die Nummer des Beispiels eingeben [0-9]: ")}.txt')
        cg = CityGraph._from_bwinf_file(pth)
        n_days = int(input('Für wieviele Tage soll geplant werden? (5):') or 5)
        print(f'cityGraph is {"strongly" if cg.is_connected else "not"} connected!')
        maxlen = 0
        iterable = zip(range(1, n_days+1), cg.get_paths(n_days))
        for i, (len_, p) in iterable:
            print(f'Tag {i}: {" -> ".join(map(str, p))}, Gesamtlaenge: {len_}')
            maxlen = max(maxlen, len_)
        print(f'Maximale Lange einer Tagestour: {maxlen}')
    except Exception as e:
        print(e)
