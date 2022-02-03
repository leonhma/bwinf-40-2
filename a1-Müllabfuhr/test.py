from dijkstra import PathSolver

with open('a1-Müllabfuhr/beispieldaten/muellabfuhr0.txt', 'r') as f:
    data = f.read()

graph = [tuple(int(n) for n in line.split()) for line in data.split('\n')[1:]]

solver = PathSolver(graph)
print(solver.get_shortest_path_length(7, 11))
