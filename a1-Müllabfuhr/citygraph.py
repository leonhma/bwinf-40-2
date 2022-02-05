from typing import List, Mapping


class CityGraph:
    """
    Class representing a graph of a city with roads & nodes.
    
    Attributes
    ----------
    avg_daily_length : float
        The average length of a daily journey

    """
    _nodes: List['CityGraph.node'] = None
    _compiled = False
    avg_daily_length = 0

    class node:
        """
        Nested class representing a node.

        Attributes
        ----------
        connections : Mapping[CityMap.edge, float]
            The edges connected to the node and their length
        distance_to : Mapping[CityMap.node, float]
            The distance from this node to `other_node` is `distance_to[other_node]`

        """
        connections: Mapping['CityGraph.edge', float]
        distance_to: Mapping['CityGraph.node', float]

        def __init__(self, index: int):
            self.index = index
            self.connections = {}
            # distance_to is initialized by CityGraph.compile()

    class edge:
        """
        Nested class representing the connection between two nodes.

        Attributes
        ----------
        seen : bool
            whether the edge has been seen by the garbage truck.

        """
        _nodes: List['CityGraph.node']
        seen = False

        def __init__(self, a: 'CityGraph.node', b: 'CityGraph.node', len_: float):
            self._nodes = [a, b]
            for n in self._nodes:
                n.connections[self] = len_

        def get_other_node(self, current: 'CityGraph.node') -> 'CityGraph.node':
            """
            Return the other connected node.

            Parameters
            ----------
            current : CityMap.node
                The currrent node

            Returns
            -------
            CityMap.node
                The other node

            """
            return [node for node in self._nodes if node != current][0]

    def __init__(self):
        self._nodes = []

    def add_node(self):
        """Add a node to the CityGraph.""" 
        assert not self._compiled, "CityGraph is already compiled!"
        self._nodes.append(self.node(len(self._nodes)))

    def add_edge(self, a: int, b: int, len_: float):
        """
        Add an edge to the CityGraph.

        Parameters
        ----------
        a, b : int
            The index of the first/second node to connect. Make sure enough nodes have been added using `add_node()`
        len_ : float
            The length of the connection

        """
        assert not self._compiled, "CityGraph is already compiled!"
        self.edge(*[self._nodes[n] for n in [a, b]], len_)  # convert node indices into node objects and connect them
        self.avg_daily_length += len_

    def _get_distances_dijkstra(self, start_node: 'CityGraph.node'):
        unvisited = {n: float('inf') for n in self._nodes}  # mapping of node -> temporary distance
        visited = {}    # mapping of node -> final distance
        current = start_node
        current_distance = 0.0
        unvisited[current] = current_distance
        while True:
            for neighbour, distance in [(edge.get_other_node(current), len_) for edge, len_ in current.connections.items()]:
                if neighbour not in unvisited:
                    continue
                new_distance = current_distance + distance
                unvisited[neighbour] = min(unvisited[neighbour], new_distance)
            visited[current] = current_distance
            del unvisited[current]
            if not unvisited:
                break
            current, current_distance = min(unvisited.items(), key=lambda x: x[1])
        return visited

    def compile(self):
        """Calculate the distance between every node and freeze the CityGraph."""
        for node in self._nodes:
            node.distance_to = self._get_distances_dijkstra(node)
        self._compiled = True
        self.avg_daily_length /= 5

    # utility methods

    def get_center_node(self) -> 'CityGraph.node':
        """Get the center (home) node.

        Returns
        -------
        CityGraph.node
            The home node

        """
        return self._nodes[0]

    def get_unseen_nodes(self) -> List['CityGraph.node']:
        """
        Get a list of every node with unseen edges connected to it.

        Returns
        -------
        List[CityGraph.node]
            The list of unseen nodes

        """
        unseen = []
        for node in self._nodes:
            if(sum([0 if edge.seen else 1 for edge in node.connections.keys()]) > 0):
                unseen.append(node)
        return unseen
    
    def get_closest_node_list(self, current: 'CityGraph.node', nodes: List['CityGraph.node']) -> 'CityGraph.node':
        """
        Get the node out of `nodes`, that's closest to `current`

        Parameters
        ----------
        current : CityGraph.node
            The current node
        nodes : List[CityGraph.node]
            The nodes to compare for distance

        Returns
        -------
        CityGraph.node
            The node out of `nodes` that's closest to `current`

        """
        assert self._compiled, "CityGraph has to be compiled first!"
        return min(nodes, key=current.distance_to.get)

