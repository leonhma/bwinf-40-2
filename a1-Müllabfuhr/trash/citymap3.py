from ast import List

# create a spatial map of the nodes
# use a* to find the shortest path between the nodes


class CityMap:
    nodes = None
    avg_daily_way = 0

    # a node (junction)
    class _Node:
        connected_roads = None

        def __init__(self, cmap: 'CityMap', id: int):
            cmap.nodes.append(self)
            cmap.nodes[id].connected_roads = {}

    # proxy for the _Node class
    def Node(self, id) -> _Node:
        return self._Node(self, id)

    def __init__(self, data: List[str]):
        self.nodes = []
        n, m = [int(x) for x in data[0].split()]
        for i in range(n):
            self.nodes.append(self.Node(i))
        for edge in data[1:m+1]:
            a, b, len_ = [int(x) for x in edge.split()]
            self.avg_daily_way += len_
            self.nodes[a].connected_roads[self.nodes[b]] = len_
            self.nodes[b].conencted_roads[self.nodes[a]] = len_
        self.avg_daily_way /= 5

    


# add all nodes and connections
# freeze citymap and calculate spatial coordinates
# get_distance_to_node(node) uses a* to find the shortest path and return it's length
# get_distance_to_full_road(node) uses a* to find the shortest path and return it's length
