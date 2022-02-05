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

# 


