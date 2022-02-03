from typing import List, Tuple


class PathSolver:
    nodes = None
    class node:
        def __init__(self, id):
            self.id = id
            self.connected_nodes = {}
            self.coordinates = None

    def __init__(self, connections: List[Tuple[int, int, int]]):
        self.nodes = []
        for id_a, id_b, l in connections:
            if max(id_a, id_b) >= len(self.nodes):
                self.nodes.append([self.node(i) for i in range(len(self.nodes), max(id_a, id_b) + 1)])
            self.nodes[id_a-1].connected_nodes[id_b-1] = l
            self.nodes[id_b-1].connected_nodes[id_a-1] = l
        # calculate coordinates for each node ((-1, 0) means 1km west of the home node)
        self.nodes[0].coordinates = (0, 0)
        for node

    def get_shortest_path_length(self, start_id: int, end_id: int) -> float:
        # get the shortest path length between two nodes
        # start_id and end_id are 1-indexed
        # return -1 if no path exists
        if start_id == end_id:
            return 0
        stack = [(node_id, None, float('inf')) for node_id in range(len(self.nodes))]  # node_id, from, weigth
        stack[start_id-1] = (start_id-1, None, 0)
        stack.sort(key=lambda x: x[2])  # sort by weight


