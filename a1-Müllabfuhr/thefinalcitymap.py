from typing import List, Mapping


class CityMap:
    _nodes: List['CityMap.node'] = None
    _compiled = False

    class node:
        connected_roads: List['CityMap.road']
        distance_to: Mapping['CityMap.node', float]

        def __init__(self, id: int):
            self.id = id
            self.adjacent_nodes = []

        def get_adjacent_nodes(self) -> Mapping['CityMap.node', float]:
            pass

    class edge:
        nodes: List['CityMap.node']

        def __init__(self, a: 'CityMap.node', b: 'CityMap.node', len_: float):
            self.nodes = [a, b]
            a.distance_to[b] = len_
            b.distance_to[a] = len_

        def get_other_node(self, current: 'CityMap.node') -> 'CityMap.node':
            return [node for node in self.nodes if node != current][0]

    def __init__(self):
        self._nodes = []

    def add_node(self):
        assert not self._compiled, "CityMap is already compiled!"
        self._nodes.append(self.node(len(self._nodes)))

    def add_edge(self, a: int, b: int, len_: float):
        assert not self._compiled, "CityMap is already compiled!"
        a, b = [self._nodes[str(n)] for n in [a, b]]    # convert indices to node objects
        road = self.edge(a, a, len_)
        a.connected_roads.append(road)
        b.connected_roads.append(road)

    def _get_distances_dijkstra(self, start_node: 'CityMap.node'):
        distances = {str(n.id): float('inf') for n in range(len(self._nodes))}
        current = str(start_node.id)
        current_distance = 0.0
        distances[current] = current_distance
        while True:
            for neighbour, distance in self._nodes[int(current)].connected_nodes.items():
                if neighbour not in distances:
                    continue
                new_distance = current_distance + distance
                distances[neighbour] = min(distances[neighbour], new_distance)
             distances[current] = current_distance
            del distances[current]

            if not distances:
                break
            current, current_distance = min(distances.items(), key=lambda x: x[1])
        return {self._nodes[int(k)]: v for k, v in distances}

    def compile(self):
        for node in self._nodes:
            node.distance_to = self._get_distances_dijkstra(node)
        self._compiled = True

    def get_unseen_nodes(self) -> List['CityMap.node']:
        unseen = []
        for node in self._nodes:
            if(sum([0 if road.]))
