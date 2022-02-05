from typing import List, Type, TypeVar


class CityMap:
    class _Node:
        connected_roads = None
        distance_from_home = None

        def __init__(self):
            self.connected_roads = []
            pass

    class _Road:
        length: int = None
        nodes = None
        cleared = False

        def __init__(self, city_map, node_a, node_b, length):
            print(f'called road init with {node_a=}, {node_b=}, {length=}')
            self.length = length
            self.nodes = [node_a, node_b]
            self.nodes.sort(key=lambda x: float('inf') if x.distance_from_home is None else x.distance_from_home)
            print(f'{[n.distance_from_home for n in self.nodes]=}')
            print(f'{self.nodes=}')
            node_a.connected_roads.append(self)
            node_b.connected_roads.append(self)
            print(f'nodes[0] {self.nodes[0].distance_from_home=}, nodes[1] {self.nodes[1].distance_from_home=}')
            # update distance_from_home for both nodes
            if self.nodes[0].distance_from_home + length < self.nodes[1].distance_from_home:
                self.nodes[1].distance_from_home = self.nodes[0].distance_from_home + length

        def get_weight(self):
            # get weight of road
            pass

    T = TypeVar('T', bound='CityMap')
    nodes = None

    def __init__(self):
        self.nodes: List[CityMap._Node] = []

    @classmethod
    def _from_file_data(cls: Type[T], data: str) -> T:
        print(f'called _from_file_data: {data=}')
        # read data and fill citymap
        lines = data.split('\n')
        n, m = [int(x) for x in lines[0].split()]
        cls = cls()
        for _ in range(n):
            cls.add_node()
        print(cls.nodes)
        for line in lines[1:m]:
            a, b, l = [int(x) for x in line.split()]
            cls.add_road(a, b, l)
        cls.nodes[0].distance_from_home = 0  # make node 0 the home node
        return cls

    def __post_init__(self):
        print(f'called __post_init__')
        pass

    def add_node(self):
        """Add a node (junction) to the citymap."""
        print(f'called add_node')
        self.nodes.append(self._Node())

    def add_road(self, a: int, b: int, l: int):
        """
        Add a road to the citymap.

        Parameters
        ----------
        a : int
            The index of the first node.
        b : int
            The index of the second node.
        l : int
            The length of the road connecting the two.

        """
        print(f'called add_road: {a=}, {b=}, {l=}')
        node_a, node_b = self.nodes[a], self.nodes[b]
        self._Road(self, node_a, node_b, l)

    def call_home(self):
        # apply an additional weigth to every road leading home
        raise NotImplementedError
