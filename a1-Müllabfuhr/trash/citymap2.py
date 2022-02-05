from typing import List


class CityMap:
    class _Node:
        connected_roads = None
        distance_from_home = None
        id = None

        def __init__(self, id: int):
            self.connected_roads = []
            self.id = id

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

    nodes = None
    gravity_towards_home = False
    weekly_way = 0

    def __init__(self, data: List[str]):
        self.nodes = []
        n, m = [int(x) for x in data[0].split()]
        self.center_node = self._Node(0)
        for i in range(n):
            self.nodes.append(self._Node(i))
        self.nodes[0].distance_from_home = 0  # make node 0 the home node
        for edge in data[1:m+1]:  # this currently only works if all edges are added from the home node outwards
            a, b, l = [int(x) for x in edge.split()]
            self.weekly_way += l
            self._Road(self.nodes[a], self.nodes[b], l)


    def set_gravity_towards_home(self, val: bool = True):
        # apply an additional weigth to roads leading home
        self.gravity_towards_home = val
    
    def get_average_daily_way(self):
        return self.weekly_way/5

    def get_distance_to_full_road(self, node: 'CityMap._Node') -> int:
        print(f'getting distance to full road for node {node.id}')
        d = 99999
        for r in node.connected_roads:
            if not r.cleared:
                d = 0
            d = min(d, self.get_distance_to_full_road(self.get_other_node(node, r)))
        return d   
            
    def get_next_road(self, current_node: 'CityMap._Node') -> 'CityMap._Road':
        # weight all roads by wether theyve been, cleared or not, and if gravity_to_home is enabled, by the distance to home
        weights = {r: None for r in current_node.connected_roads}
        for r in weights:
            road_weight = r.length
            road_weight += 0.5 if r.cleared else 0
            road_weight += self.get_other_node(current_node, r).distance_from_home if self.gravity_towards_home else 0
            road_weight += 0.2*self.get_distance_to_full_road(self.get_other_node(current_node, r))
            weights[r] = road_weight
        return min(weights, key=weights.get)

    def get_other_node(self, current_node: 'CityMap._Node', road: 'CityMap._Road') -> 'CityMap._Node':
        # get the other node of the road
        return [n for n in road.nodes if n != current_node][0]

    def go_down_road(self, current_node: 'CityMap._Node', road: 'CityMap._Road') -> 'CityMap._Node':
        # go down the road
        road.cleared = True
        return self.get_other_node(current_node, road)
