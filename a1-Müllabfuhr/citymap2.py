from typing import List


class CityMap:
    class _Node:
        connected_roads = None
        distance_from_home = None

        def __init__(self):
            self.connected_roads = []

    class _Road:
        length: int = None
        nodes = None
        cleared = False

        def __init__(self, node_a, node_b, length):
            self.length = length
            self.nodes = [node_a, node_b]
            self.nodes.sort(key=lambda x: float('inf') if x.distance_from_home is None else x.distance_from_home)
            node_a.connected_roads.append(self)
            node_b.connected_roads.append(self)
            # update distance_from_home for both nodes
            if self.nodes[0].distance_from_home + length < (self.nodes[1].distance_from_home or 99999):
                self.nodes[1].distance_from_home = self.nodes[0].distance_from_home + length

        def get_weight(self):
            # get the weight of the road
            pass

    center_node = None
    gravity_towards_home = False

    def __init__(self, data: List[str]):
        n, m = [int(x) for x in data[0].split()]
        self.center_node = self._Node()
        nodes = [self.center_node]
        for _ in range(n):
            nodes.append(self._Node())
        self.nodes[0].distance_from_home = 0  # make node 0 the home node
        for edge in data[1:m]:  # this currently only works if all edges are added from the home node outwards
            a, b, l = [int(x) for x in edge.split()]
            self._Road(nodes[a], nodes[b], l)

    def set_gravity_towards_home(self, val: bool = True):
        # apply an additional weigth to roads leading home
        self.gravity_towards_home = val

    def go_down_road(self, current_node: 'CityMap._Node', road: 'CityMap._Road') -> 'CityMap._Node':
        # go down the road
        road.cleared = True
        return [n for n in road.nodes if n != current_node][0]  # return the other node
