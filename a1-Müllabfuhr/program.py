from citygraph import CityGraph

cg = CityGraph()

# load CityGraph from file
path = path.join(
    path.dirname(path.realpath(__file__)), 'beispieldaten', f'muellabfuhr{0}.txt'
)

with open(path, 'r') as f:
    lines = f.read.split('\n')

n, m = [int(s) for s in lines[0].split()]
for _ in range(n):
    cg.add_node()
for line in lines[1:m+1]:
    fields = line.split()
    a, b = [int(s) for s in fields[:2]]
    len_ = float(fields[2])
    cg.add_edge(a, b, len_)
cg.compile()



# loop through the days, pathfind, and record the journey
days = {'Montag': [], 'Dienstag': [], 'Mittwoch': [], 'Donnerstag': [], 'Freitag': []}
for day in days:
    center = cg.get_center_node()
    current = center
    not_back_home = True
    distance_travelled = 0
    while not_back_home:
        # pathfinding function
        def get_next() -> 'CityGraph.node':
            """
            Do a step in the pathfinding calculation.

            Returns
            -------
            CityGraph.node
                The next node.

            """
            unseen = cg.get_unseen_nodes()
            if current in unseen: unseen.remove(current)
            weights = {edge: 0 for edge in current.connections.keys()}
            for edge in weights:
                # calculate weigth
                node = edge.get_other_node(current)
                if distance_travelled > cg.avg_daily_length/2:
                    weights[edge] = 2*node.distance_to[center]  # going home is more important than being efficient
                weigths[edge] += get_closest_node_list(node, unseen)
                if edge.seen:
                    weight += 1
                # seen edges should be discouraged
                # edges whould be emphasised based on how far they are from unseen nodes
                # if distance > avg_daily_distance/2 nodes leading home should be encouraged
            return min(weights.items(), key=weights.get)[0]
            # 
            # return the next node
        next_ = get_next()
        days[day] += [next_.index]   # TODO figure out if append works
        if next_.index == 0:
            not_back_home = False
        current = next_

print(days)
        

