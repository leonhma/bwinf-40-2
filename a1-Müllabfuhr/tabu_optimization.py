from collections import Counter, deque
from functools import reduce
from operator import add
from time import time
from typing import Dict, List, Tuple, Iterable

from utility import TabuList

def MMKCPP_TEE_TabuSearch(G: Dict[int, Dict[int, float]], tours: List[Tuple[int, ...]], /,
                          maxNOfItsWithoutImprovement: int = 100, maxRunningTime: float = 0,
                          tabuTenure: int = 20) -> List[Tuple[int, ...]]:
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
    print('computing dijkstra')
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

    def w_tours(tours: Iterable[Tuple[int, ...]]) -> float:
        return sum(w_tour(tour) for tour in tours)

    # cost function
    def w_max_tours(tours: Iterable[Tuple[int, ...]]) -> float:
        return max(w_tour(tour) for tour in tours)

    def edgecount_tour(tour: Tuple[int, ...]) -> Counter:
        return Counter(frozenset(x) for x in edges(tour))

    def edgecount_tours(tours: List[Tuple[int, ...]]) -> Counter:
        return reduce(add, (edgecount_tour(tour) for tour in tours))
    
    def MergeWalkWithTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        print(f'merging {walk=} with {tour=}')
        # remove edges from walk that are already in tour
        if len(walk) == 1:
            return tour

        walk = list(walk)

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
        
        walk = tuple(walk)
        
        # find node `t` closest to `u` and `v`, the end nodes of `walk`
        min_idx = None
        min_distance = 999999
        min_sp_v = min_sp_u = None

        for i, node in enumerate(tour):
            sp_u = dijkstra[node][walk[0]]
            sp_v = dijkstra[walk[-1]][node]
            if sp_u[0]+sp_v[0] < min_distance:
                min_distance = sp_v[0]+sp_u[0]
                min_idx = i
                min_sp_u = sp_u[1]
                min_sp_v = sp_v[1]

        # splice
        return tour[:min_idx+(1 if tour[min_idx] != walk[0] else 0)]+min_sp_u+walk+min_sp_v+tour[min_idx+(1 if tour[min_idx] == walk[-1] else 0):]

        

    def SeparateWalkFromTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        print(f'seperating {walk=} from {tour=}')
        u, v = walk[0], walk[-1]
        if u not in tour or v not in tour or u == v:
            return tour
        li, ri = min(tour.index(u), tour.index(v)), max(tour.index(u), tour.index(v))
        
        return ((0,) if tour[0] != 0 else ())+tour[:li+1]+dijkstra[u][v][1]+tour[ri:]+((0,) if tour[-1] != 0 else ())
    
    def _ReorderToClosedWalk(edgeset: List[set]) -> Tuple[int, ...]:
        print(f'reordering {edgeset=}')
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
        print(f'optimizing {tour=}')
        edgeset = list(edges(tour))
        for edge in edgeset:
            edge = frozenset(edge)  # 🥶
            ects = edgecount_tours(tours)[edge]
            ect = edgecount_tour(tour)[edge]
            if ects > ect and ect % 2 == 0:
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
        print('starting compute neighborhood\n-------------------')
        current_max_tour = max(currentSolution, key=w_tour)
        current_max_tour_idx = currentSolution.index(current_max_tour)

        for i in range(len(current_max_tour)-2):
            semilocal_tours = currentSolution.copy()
            walk = current_max_tour[i:i+3]  # 3 nodes, 2 edges
            print(f'checking {walk=}')
            semilocal_tours[current_max_tour_idx] = SeparateWalkFromTour(current_max_tour, walk)
            semilocal_tours[current_max_tour_idx] = RemoveEvenRedundantEdges(current_max_tour, walk)
            print(f'max is now {semilocal_tours[current_max_tour_idx]}')


            for other_tour_idx in range(len(tours)):
                if other_tour_idx == current_max_tour_idx:
                    continue
                other_tour = currentSolution[other_tour_idx]
                local_tours = semilocal_tours.copy()

                local_tours[other_tour_idx] = MergeWalkWithTour(other_tour, walk)
                local_tours[other_tour_idx] = RemoveEvenRedundantEdges(other, local_tours)
                print(f'other is now {local_tours[other_tour_idx]}')
                print(f'> neighbor {local_tours}')

                neighborhood.append(tuple(local_tours))

        print(f'{neighborhood=}')
        # filter tabu, prioritise overall length, then reduce max length
        currentSolution = min(filter(lambda x: not tabuList.get(x), neighborhood), key=lambda x: (w_tours(x), w_max_tours(x)))
        tabuList.add(currentSolution)
        currentSolution = list(currentSolution)
        currentSolutionValue = w_max_tours(currentSolution)

        if currentSolutionValue < bestSolutionValue:
            bestSolutionValue = currentSolutionValue
            bestSolution = currentSolution
            nOfItsWithoutImprovement = 0

    return bestSolution

        

