from typing import List, Tuple
# TODO cleanup and integrate with CityMap

class PathSolver:
    nodes = None

    class node:
        def __init__(self, id):
            self.id = id
            self.connected_nodes = {}

    def __init__(self, connections: List[Tuple[int, int, int]]):
        self.nodes = []
        print(f'dji initialise called with {connections=}')
        for id_a, id_b, len_ in connections:
            if max(id_a, id_b) >= len(self.nodes):
                self.nodes += [self.node(i) for i in range(len(self.nodes), max(id_a, id_b) + 1)]
            self.nodes[id_a].connected_nodes[str(id_b)] = len_
            self.nodes[id_b].connected_nodes[str(id_a)] = len_

    def get_shortest_path_length(self, start_id: int, end_id: int) -> float:
        """
        Calculate the shortest path between two nodes using dijkstras algorithm.

        Parameters
        ----------
        start_id : int
            The id of the start node.
        end_id : int
            The id of the end node.

        Returns
        -------
        float
            The length of the shortest path between the two nodes. `-1` if no path exists.

        """
        distances = {str(i): float('inf') for i in range(len(self.nodes))}
        current = str(start_id)
        current_distance = 0.0
        distances[current] = current_distance
        while True:
            for neighbour, distance in self.nodes[int(current)].connected_nodes.items():
                if neighbour not in distances:
                    continue
                new_distance = current_distance + distance
                distances[neighbour] = min(distances[neighbour], new_distance)
                print(f'current: {current}, new distance for neightbour {neighbour} is {distances[neighbour]}')
            print(distances)
            if current == str(end_id):
                return min(distances.items(), key=lambda x: x[1])[1]
            del distances[current]
            
            if not distances:
                return -1
            current, current_distance = min(distances.items(), key=lambda x: x[1])
