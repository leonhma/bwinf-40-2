from typing import (FrozenSet, Iterable, List, Mapping, Set,
                    Tuple)

from utility import ilist, remove_by_exp


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
        self.max_bfs_depth = 0

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

    def get_paths(self, days: int = 5) -> List[Tuple[float, Tuple[int, ...]]]:
        print('getting cycles')
        # get paths using bfs-type algorithm
        visited: Mapping[int, Tuple[float, List[int]]] = {}  # {visited_node_id: (length, path)}
        paths: List[Tuple[float, Tuple[int, ...]]] = []  # [(length, (path)), ...]
        queue: List[Tuple[float, Tuple[int, ...]]] = [(0.0, [0])]  # [(distance, path), ...]

        try:
            while not self._contains_all_edges(map(lambda x: x[1], paths)):
                queue.sort()
                current_length, current_path = queue.pop(0)
                if current_path[-1] in visited:  # check if path meets another path TODO make path not meet with itself
                    paths.append((current_length+visited[current_path[-1]][0],
                                 (*visited[current_path[-1]][1], *reversed(current_path[:-1]))))
                    visited[current_path[-1]] = (current_length, current_path)

                    # remove the path merging into the current path
                    remove_by_exp(lambda x: x[1][-1] == current_path[-2], queue)
                    continue
                if len(self.vertices[current_path[-1]]) == 1:  # check if it's a dead end
                    paths.append((current_length*2, (*current_path, *reversed(current_path[:-1]))))
                    continue
                visited[current_path[-1]] = (current_length, current_path)
                for next_node_id in self.vertices[current_path[-1]]:
                    if next_node_id == (current_path[-2] if len(current_path) > 1 else None):  # skip going backwards
                        continue
                    queue.append((self.vertices[current_path[-1]][next_node_id] + current_length,
                                  current_path + [next_node_id]))
        except IndexError as e:
            print(f'Keine Pfade gefunden! (Mehrere unverbundene Straßennetze). ({e})')
            return []

        print(f'{paths=}')

        # remove all paths that are subsets of other paths
        paths.sort(key=lambda x: len(x[1]), reverse=True)
        to_remove = []
        edgesets: List[FrozenSet[FrozenSet[int]]] = ilist()
        for i, path in enumerate(paths):
            edgesets[i] = frozenset(tuple(frozenset((path[1][i], path[1][i+1])) for i in range(len(path[1])-1)))

        for i, edgeset in enumerate(edgesets):
            if any(edgeset.issubset(edgeset2) for edgeset2 in edgesets[:i]):
                to_remove.append(i)

        shift = 0
        for i in to_remove:
            del paths[i-shift]
            shift += 1
        
        # merge paths while they are > target_n_days
        while len(paths) > days:
            paths.sort()
            first = paths.pop(0)
            second = paths[0]
            paths[0] = (first[0] + second[0], (*first[1], *second[1]))

        # pad to length of target_n_days
        while len(paths) < days:
            paths.append((0.0, (0,)))
        
        return paths

