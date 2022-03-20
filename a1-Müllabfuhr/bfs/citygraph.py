from itertools import combinations_with_replacement
from time import time
from typing import List, Mapping, Set, Tuple


class CityGraph:
    """A class representing the city graph."""
    vertices: Mapping[int, Mapping[int, float]]     # {vertex_id: {connected_vertex_id: distance}, ...}
    edgeset: List[Set[int]]                         # [{vertex_id, vertex_id}, {vertex_id, vertex_id}, ...]

    @classmethod
    def _from_bwinf_file(cls, path: str) -> 'CityGraph':
        with open(path, 'r') as f:
            lines = f.read().split('\n')

        n, m = [int(s) for s in lines[0].split()]
        return cls(
            list(range(n)),
            [(int(v),
              int(u),
              float(length)) for v, u, length in [line.split() for line in lines[1: m + 1]]])

    def __init__(self, vertices: List[int], edges: List[Tuple[int, int, float]]):
        self.vertices = {v: {} for v in vertices}
        self.edgeset = []
        self._max_dfs_depth = 0

        for edge in edges:
            v, u, len_ = edge
            self.edgeset.append({v, u})
            self.vertices[v][u] = len_
            self.vertices[u][v] = len_

    def path_contains_all_edges(self, paths: List[List[int]]) -> bool:
        # convert all paths into edgesets
        flattened = [j for sub in paths for j in sub]
        edgesets = [{flattened[i], flattened[i+1]} for i in range(len(flattened)-1)]
        # check if all edges are contained in the resulting edgeset
        for edge in self.edgeset:
            if edge not in edgesets:
                return False
        return True

    def get_bfs_trash_collection_paths(self, days=5) -> Tuple[Tuple[int], float]:
        paths = set()
        queue: List[Tuple[List[int], float]] = [([0], 0.0)]  # [(path, length), ...]

        while True:
            if len(queue) == 0:
                raise Exception('no paths found. bfs queue empty')
            current = sorted(queue, key=lambda x: x[1]).pop(0)  # get node that is nearest to the 'flooded area'
            queue.remove(current)
            if current[0][-1] == 0:
                path = tuple(current[0])
                # non-reversed duplicates are dealt with by the 'set' datastructure
                if (tuple(reversed(path)), current[1]) not in paths:
                    paths.add((path, current[1]))
                    # check current path
                    print(f'{time()} starting checking for combinations')
                    for comb in combinations_with_replacement(paths, days):
                        if self.path_contains_all_edges([x[0] for x in comb]):
                            return comb
                    print(f'{time()} done checking for combinations')
            if current[0][-1] != 0 or len(current[0]) == 1:
                for v_next in self.vertices[current[0][-1]]:
                    if ((v_next == (current[0][-2] if len(current[0]) > 1 else 'a')) and (len(self.vertices[current[0][-1]]) > 1)):
                        continue
                    queue.append((current[0]+[v_next], self.vertices[current[0][-1]][v_next] + current[1]))
