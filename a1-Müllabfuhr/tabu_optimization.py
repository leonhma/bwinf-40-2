from collections import Counter, deque
from functools import reduce
from operator import add
from time import time
from typing import Dict, List, Tuple, Iterable

from utility import TabuList

def MMKCPP_TEE_TabuSearch(G: Dict[int, Dict[int, float]], tours: List[Tuple[int, ...]], /, maxNOfItsWithoutImprovement: int = 100,
                          maxRunningTime: float = 0, tabuTenure: int = 20) -> List[Tuple[int, ...]]:
    """
    Perform a tabu search metaheuristic optimization on `tours` in the graph `G`.

    Parameters
    ----------
    G : Dict[int, Dict[int, float]]
        The undirected, non-windy weighted graph to operate on.
    tours : List[List[int]]
        List of `k` tours to start with.
    maxNOfItsWithoutImprovement : int, default=100
        Maximum number of iterations without improvement to stop early.
    maxRunningTime : float, optional
        The maximum running time to stop early (seconds).
    tabuTenure : int, default=20
        The number of iterations to 'tabu' a neighbor.

    Returns
    -------
    List[List[int]]
        An optimized List of k paths

    """
    # precompute shortest paths O(|V|²)
    print('computing dijstra')
    dijkstra = {k: {} for k in G}  # shallowcopy doesnt work
    for start in dijkstra:
        q = deque(((0, start, []),))
        while q:
            length, current, currentpath = q.popleft()
            if current in dijkstra[start]: continue
            dijkstra[start][current] = (length, tuple(currentpath[1:]))
            for next_, weight in G[current].items():
                q.append((length+weight, next_, currentpath+[current]))
        
    def edges(tour: Tuple[int, ...]) -> Iterable[set]:
        return (set(tour[i:][:2]) for i in range(len(tour)-1) if None not in tour[i:][:2])

    def w_tour(tour: Tuple[int, ...]) -> float:
        return sum(G[tour[i]][tour[i+1]] for i in range(len(tour)-1))

    # cost function
    def w_max_tours(tours: Iterable[Tuple[int, ...]]) -> float:
        return max(w_tour(tour) for tour in tours)

    def edgecount_tour(tour: Tuple[int, ...]) -> Counter:
        return Counter(frozenset(x) for x in edges(tour))

    def edgecount_tours(tours: List[Tuple[int, ...]]) -> Counter:
        return reduce(add, (edgecount_tour(tour) for tour in tours))
    
    def MergeWalkWithTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        # remove edges from walk that are already in tour
        if len(walk) == 1:
            return tour

        tour_edges = edges(tour)
        if not tour_edges:
            return walk

        while frozenset((walk[0], walk[1])) in tour_edges:
            del walk[0]
            if len(walk) == 1:
                return tour

        while frozenset((walk[-1], walk[-2])) in tour_edges:
            del walk[-1]
            if len(walk) == 1:
                return tour
        
        # find node `t` closest to `u` and `v`, the end nodes of `walk`
        min_idx = None
        min_distance = 999999
        min_sp_v = min_sp_u = None

        for node in tour:
            sp_u = dijkstra[node][walk[0]]
            sp_v = dijkstra[walk[-1]][node]
            if sp_u[0]+sp_v[0] < min_distance:
                min_distance = sp_v[0]+sp_u[0]
                min_idx = i
                min_sp_u = sp_u[1]
                min_sp_v = sp_v[1]

        # splice
        return tour[:min_idx+(1 if min_idx > 0 else 0)]+('|')+min_sp_u+('|')+walk+('|')+min_sp_v+('|')+tour[min_idx:]

    # fix this
    def SeparateWalkFromTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        u, v = walk[0], walk[-1]
        if u not in tour or v not in tour or u == v:
            return tour
        li, ri = min(tour.index(u), tour.index(v)), max(tour.index(u), tour.index(v))
        

        if li == 0:
            return ((0,) if v != 0 else ())+dijkstra[0][v][1]+tour[ri:]+dijkstra[tour[-1]][0][1]+((0,) if tour[-1] != 0 else ())
        if ri == len(tour)-1:
            return ((0,) if tour[0] != 0 else ())+dijkstra[0][tour[0]][1]+tour[:ri+1]+dijkstra[u][0][1]+((0,) if tour[ri] != 0 else ())
        return ((0,) if tour[0] != 0 else ())+dijkstra[0][tour[0]][1]+tour[:li+1]+dijkstra[u][v][1]+tour[ri:]+dijkstra[tour[-1]][0][1]+((0,) if tour[-1] != 0 else ())
    
    def _ReorderToClosedWalk(edgeset: List[set]) -> Tuple[int, ...]:
        print(f'debug in _ReorderToClosedWalk {edgeset=}')
        newtour = [0]  # depot node

        while edgeset:
            for edge in edgeset:
                if newtour[-1] in edge:
                    edge.remove(newtour[-1])
                    newtour.append(edge.pop())
                    edgeset.remove(edge)
        
        if newtour[-1] != 0:
            raise ValueError(f'something went wrong! newtour was {newtour}')
        
        return tuple(newtour)

    def RemoveEvenRedundantEdges(tour: Tuple[int, ...], tours: List[Tuple[int, ...]]) -> Tuple[int, ...]:
        print(f'called RemoveEvenRedundantEdges with {tour=}')
        edgeset = list(edges(tour))
        for edge in edgeset:
            print(f'evaluating {edge}')
            edge = frozenset(edge)  # 🥶
            ects = edgecount_tours(tours)[edge]
            ect = edgecount_tour(tour)[edge]
            print(f'{ects=}, {ect=}')
            if ects > ect and ect % 2 == 0:
                print(f'{edgecount_tours(tours)[edge]=}, {edgecount_tour(tour)[edge]=}')
                # check if tour remains connected to node 0
                nodes = set((0,))
                remaining = set(map(frozenset, edges(tour))).discard(edge)
                while remaining:
                    stop = True
                    for edge in remaining:
                        if nodes.intersection(edge):
                            nodes.update(edge)
                            remaining.remove(edge)
                            stop = False
                    if stop:
                        break
                else:
                    # remove edges
                    edgeset = list(filter(lambda x: x != edge, edgeset))
        print(f'{edgeset=}')
        return _ReorderToClosedWalk(edgeset)

    bestSolution = tours
    currentSolution = tours

    bestSolutionValue = w_max_tours(tours)
    currentSolutionValue = w_max_tours(tours)

    nOfItsWithoutImprovement = 0

    tabuList = TabuList(tabuTenure)

    if maxRunningTime:
        startTime = time()

    print('starting algorithm')
    while (nOfItsWithoutImprovement < maxNOfItsWithoutImprovement and not
           (maxRunningTime and time() > startTime + maxRunningTime)):
        
        nOfItsWithoutImprovement += 1
        tabuList.tick()
        
        neighborhood: List[Tuple[Tuple[int]]] = []

        # compute neighborhood
        print('starting compute neighborhood')
        current_max_tour = max(currentSolution, key=w_tour)
        current_max_tour_idx = currentSolution.index(current_max_tour)

        for other_tour_idx in range(len(tours)):
            if other_tour_idx == current_max_tour_idx:
                continue
            other_tour = currentSolution[other_tour_idx]
            print(f'changing between {current_max_tour} and {other_tour}')
            for i in range(len(current_max_tour)-2):
                walk = current_max_tour[i:i+3]  # 3 nodes, 2 edges
                local_tours = currentSolution.copy()
                print(f'seperating walk {walk} from max')
                current = SeparateWalkFromTour(current_max_tour, walk)
                local_tours[current_max_tour_idx] = current
                print(f'optimizing max={current}')
                current = RemoveEvenRedundantEdges(current, local_tours)
                print(f'max is now {current}')
                local_tours[current_max_tour_idx] = current
                print(f'merging walk with other')
                other = MergeWalkWithTour(other_tour, walk)
                local_tours[other_tour_idx] = other
                print(f'optimizing other')
                other = RemoveEvenRedundantEdges(other, local_tours)
                print(f'other is now {other}')
                local_tours[other_tour_idx] = other
                print(f'neighbor {local_tours}')

                neighborhood.append(tuple(local_tours))

        print(f'{neighborhood=}')
        # select max neighbor
        currentSolution = min(neighborhood, key=lambda x: (tabuList.get(x), w_max_tours(x)))
        tabuList.add(currentSolution)
        currentSolution = list(currentSolution)
        currentSolutionValue = w_max_tours(currentSolution)

        if currentSolutionValue < bestSolutionValue:
            bestSolutionValue = currentSolutionValue
            bestSolution = currentSolution
            nOfItsWithoutImprovement = 0

    return bestSolution

        

