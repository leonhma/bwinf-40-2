from itertools import combinations
from queue import PriorityQueue
from typing import FrozenSet, Iterable, List, Mapping, Set, Tuple


class CityGraph:
    """A class representing the city graph."""
    vertices: Mapping[int, Mapping[int, float]]     # {vertex_id: {connected_vertex_id: distance}, ...}
    edgeset: Set[FrozenSet[int]]                    # {{vertex_id, vertex_id}, {vertex_id, vertex_id}, ...}
    max_bfs_depth: int

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

        n, m = [int(s) for s in lines[0].split()]
        return cls(
            list(range(n)),
            [(int(v),
              int(u),
              float(length)) for v, u, length in [line.split() for line in lines[1: m + 1]]])

    def __init__(self, vertices: List[int], edges: List[Tuple[int, int, float]]):
        self.max_bfs_depth = 0

        self.vertices = {v: {} for v in vertices}
        self.edgeset = set()
        self._max_dfs_depth = 0

        for edge in edges:
            self.max_bfs_depth += 1
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

    def get_trash_collection_paths(self, days=5) -> List[Tuple[float, Tuple[int, ...]]]:
        """
        Find the shortest `days` paths that cycle from the depot, so that every road is visited.

        Parameters
        ----------
        days : int
            The number of days to find the paths for.

        Returns
        -------
        List[Tuple[float, Tuple[int, ...]]]
            A list of tuples containing the length of the path and the path itself.

        Raises
        ------
        queue.Empty
            If no path was found.

        """
        paths: List[Tuple[float, Tuple[int, ...]]] = [(0.0, (0,))] * days  # [(distance, [path]), ...]
        queue: PriorityQueue[Tuple[float, List[int]]] = PriorityQueue()   # [(length, [path]), ...]
        queue.put((0.0, [0]))

        while True:  # raises queue.Empty when queue is empty
            current = queue.get()  # get node that is nearest to the 'flooded area'
            if len(current[1]) > self.max_bfs_depth:  # stopping at max feasible bfs depth
                continue
            if current[1][-1] == 0 and len(current[1]) > 1:  # stopping back at the base
                path = tuple(current[1])
                # non-reversed duplicates are dealt with by the 'set' datastructure
                if (current[0], path) not in paths and (current[0], tuple(reversed(path))) not in paths:
                    paths.pop(0)
                    paths.append((current[0], path))
                    # check current path
                    if self._contains_all_edges(map(lambda x: x[1], paths)):
                            return paths
            if current[1][-1] != 0 or current[0] == 0:  # if not back at home or at start of path
                for v_next in self.vertices[current[1][-1]]:
                    if ((v_next == (current[1][-2] if len(current[1]) > 1 else 'a')) and (len(self.vertices[current[1][-1]]) > 1)):
                        continue
                    queue.put((self.vertices[current[1][-1]][v_next] + current[0], current[1]+[v_next]))
