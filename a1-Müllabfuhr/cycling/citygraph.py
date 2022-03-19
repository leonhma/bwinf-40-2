from typing import List, Mapping, Set, Tuple


class CityGraph:
    """A class representing the city graph."""
    vertices: Mapping[int, Mapping[int, float]]     # {vertex_id: {connected_vertex_id: distance}, ...}
    edgeset: List[Set[int]]                         # [{vertex_id, vertex_id}, {vertex_id, vertex_id}, ...]
    _max_dfs_depth: int

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
            self._max_dfs_depth += 1
            self.edgeset.append({v, u})
            self.vertices[v][u] = len_
            self.vertices[u][v] = len_

    def _cycles_dfs(self, _current_path: List[int],
                    _traversed_edges: List[Set[int]],
                    _current_depth: int) -> set[tuple[tuple[int],
                                                      float]]:
        connected = self.vertices[_current_path[-1]]
        cycles = set()
        for v_next in connected:
            if len(_current_path) > self._max_dfs_depth:
                break
            if (((v_next == (_current_path[-2] if len(_current_path) > 1 else 'asdafsdfsd')) and len(connected) == 2)
                or (_traversed_edges.count({_current_path[-1], v_next}) == 2)):
                continue
            if v_next == 0:
                cycles.add((tuple(_current_path+[0]), _current_depth+connected[0]))
            else:
                cycles.update(
                    self._cycles_dfs(
                        _current_path + [v_next],
                        _traversed_edges + [{_current_path[-1],
                                            v_next}],
                        _current_depth + connected[v_next]))
        return cycles

    def find_cycles(self) -> set[tuple[tuple[int], float]]:
        """
        Find all cycles, that
        - can use an edge up to two times
        - don't turn around when there's only two edges connected to a vertice

        """
        cycles = self._cycles_dfs([0], [], 0)
        cycles.add(((0,), 0))  # also consider staying home possibility
        # clean duplicates
        to_check = cycles.copy()
        while to_check:
            cycle = to_check.pop()
            if cycle[0] != cycle[0][::-1] and (cycle[0][::-1], cycle[1]) in to_check:
                cycles.discard((cycle[0][::-1], cycle[1]))
        return cycles
