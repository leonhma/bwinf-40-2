from typing import List, Mapping, Set, Tuple


class CityGraph:
    """A class representing the city graph."""
    vertices: Mapping[int, Mapping[int, float]]     # {vertex_id: {connected_vertex_id: distance}}
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

    # TODO also consider staying at 0 a cycle
    def find_cycles(self, v_start: int = 0, _current_path: List[int] = None, _traversed_edges: List[Set[int]] = None) -> List[List[int]]:
        """
        Find all cycles starting at v_start, that
        - can use an edge up to two times
        - don't turn around when there's only two edges connected to a vertice

        """
        print(f'find_cycles ({v_start=}, {_current_path=}, {_traversed_edges=})')
        if not _current_path:
            _current_path = [0]
        if not _traversed_edges:
            _traversed_edges = []
        connected = self.vertices[v_start]
        cycles = []
        for v_next in connected:
            if len(_current_path) > self._max_dfs_depth:
                print('length axceeded')
                break
            if (v_next == _current_path[-1] and len(connected) == 2) or (_traversed_edges.count({v_start, v_next}) == 2):
                continue
            if v_next == 0:
                cycles.append(_current_path+[0])
                print('equals 0 adding')
            else:
                cycles += (self.find_cycles(v_next, _current_path + [v_next], _traversed_edges + [{v_start, v_next}]))
        return cycles
