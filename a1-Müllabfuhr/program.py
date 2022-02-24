from citygraph import CityGraph
from os import path

cg = CityGraph()

# load CityGraph from file
path = path.join(
    path.dirname(path.realpath(__file__)), 'beispieldaten', f'muellabfuhr{1}.txt'
)

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, m = [int(s) for s in lines[0].split()]
for _ in range(n):
    cg.add_node()
for line in lines[1:m+1]:
    fields = line.split()
    a, b = [int(s) for s in fields[:2]]
    len_ = float(fields[2])
    cg.add_edge(a, b, len_)
cg.compile()


center = cg.get_center_node()

# loop through the days, pathfind, and record the journey
days = {'Montag': [0], 'Dienstag': [0], 'Mittwoch': [0], 'Donnerstag': [0], 'Freitag': [0]}
lengths = {'Montag': 0, 'Dienstag': 0, 'Mittwoch': 0, 'Donnerstag': 0, 'Freitag': 0}
for day in days:
    current = center
    not_back_home = True
    distance_travelled = 0
    while not_back_home:
        # pathfinding function
        def get_next() -> 'CityGraph.node':  # sourcery skip: use-dict-items
            """
            Do a step in the pathfinding calculation.

            Returns
            -------
            CityGraph.node
                The next node.

            """
            # TODO handle unconnected graphs
            unseen = cg.get_unseen_nodes()
            if current in unseen: unseen.remove(current)
            weights = {edge: 0 for edge in current.connections.keys()}
            for edge in weights:
                # calculate weigth
                other = edge.get_other_node(current)
                if distance_travelled > cg.avg_daily_length:
                    weights[edge] += 2*other.distance_to[center]
                try:
                    weights[edge] += cg.get_closest_node_list(other, unseen).distance_to[other] # distance from other node to node with unseen edges
                except ValueError:
                    pass
                if edge.seen:
                    weights[edge] += 1
                    # seen edges should be discouraged
                    # edges whould be emphasised based on how far they are from unseen nodes
                    # if distance > avg_daily_distance/2 nodes leading home should be encouraged
            edge = min(weights.items(), key=lambda x: x[1])[0]
            edge.seen = True
            return edge.length, edge.get_other_node(current)
            # 
            # return the next node
        len_, next_ = get_next()
        distance_travelled += len_
        days[day] += [next_.index]   # TODO figure out if append works
        if next_.index == 0:
            not_back_home = False
        current = next_
    lengths[day] = distance_travelled

print(f'average daily length: {cg.avg_daily_length}')
print(days)
print(lengths)
        

