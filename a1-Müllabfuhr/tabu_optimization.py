from collections import Counter, deque
from functools import reduce
from operator import add
from random import random
from time import time
from typing import Callable, Dict, Iterable, List, Tuple

from utility import TabuList


def MMKCPP_TEE_TabuSearch(G: Dict[int, Dict[int, float]],
                          k: int = 5, maxNOfItsWithoutImprovement: int = 100, maxRunningTime:
                          float = None, dropout: float = 0.2, dropout_fn: Callable = lambda x: x ** 1.2,
                          tabuTenure: int = 20) -> List[Tuple[int, ...]]:
    """
    Generate a starting path and perform a meta-heuristic optimisation.

    Parameters
    ----------
    G : Dict[int, Dict[int, float]]
        The undirected, non-windy weighted graph to operate on.
    k : int, default=5
        Number of Vehicles.
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
    dijkstra = {k: {} for k in G}  # shallowcopy doesnt work
    for start in dijkstra:
        q = deque(((0, start, []),))
        while q:
            length, current, currentpath = q.popleft()
            if current in dijkstra[start]:
                continue
            dijkstra[start][current] = (length, tuple(currentpath[1:]))
            for next_, weight in G[current].items():
                q.append((length+weight, next_, currentpath+[current]))

    def edges(tour: Tuple[int, ...]) -> Iterable[set]:
        return (set(tour[i:][:2]) for i in range(len(tour)-1))

    def w_tour(tour: Tuple[int, ...]) -> float:
        return sum(G[tour[i]][tour[i+1]] for i in range(len(tour)-1))

    def w_avg_tours(tours: Iterable[Tuple[int, ...]]) -> float:
        return sum(w_tour(tour) for tour in tours)/k

    def w_max_tours(tours: Iterable[Tuple[int, ...]]) -> float:
        return max(w_tour(tour) for tour in tours)

    def cost(tours: Iterable[Tuple[int, ...]], w_avg: float) -> Tuple[float, float, float]:
        return (w_max_tours(tours), sum(abs(w_tour(tour)-w_avg) for tour in tours), random())

    def edgecount_tour(tour: Tuple[int, ...]) -> Counter:
        return Counter(frozenset(x) for x in edges(tour))

    def edgecount_tours(tours: List[Tuple[int, ...]]) -> Counter:
        return reduce(add, (edgecount_tour(tour) for tour in tours))

    def MergeWalkWithTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        # remove edges from walk that are already in tour
        if len(walk) == 1:
            return tour

        walk = list(walk)

        tour_edges = edges(tour)
        if not tour_edges:
            return (((0,) if walk[0] != 0 else ())
                    +dijkstra[0][walk[0]][1]+tuple(walk)+dijkstra[walk[-1]][0][1]
                    +((0,) if walk[-1] != 0 else ()))

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
        return (tour[:min_idx+(1 if tour[min_idx] != walk[0] else 0)]
                +min_sp_u+walk+min_sp_v
                +tour[min_idx+(1 if tour[min_idx] == walk[-1] else 0):])

    # basically shortenPath

    def SeparateWalkFromTour(tour: Tuple[int, ...], walk: Tuple[int, ...]) -> Tuple[int, ...]:
        # assuming walk is a subsegment of tour
        u, v, = walk[0], walk[-1]

        # better lr ri finding
        for i in range(len(tour)-2):
            if walk == tour[i:][:3]:
                li = i
                ri = i+2
                break

        return tour[:li+(1 if u != v else 0)]+dijkstra[u][v][1]+tour[ri:]

    def ReorderToClosedWalk(edgeset: List[set]) -> Tuple[int, ...]:
        newtour = [0]  # depot node

        while edgeset:
            stop = True
            for edge in edgeset:
                if newtour[-1] in edge:
                    edge.remove(newtour[-1])
                    newtour.append(edge.pop())
                    edgeset.remove(edge)
                    stop = False
            if stop:
                break

        while edgeset:  # find walks and append them to the main path
            walk = list(edgeset.pop())
            while True:
                stop = True
                for edge in edgeset:
                    if newtour[-1] in edge:
                        edge.remove(walk[-1])
                        walk.append(edge.pop())
                        edgeset.remove(edge)
                        stop = False
                if stop:
                    break
            newtour = list(MergeWalkWithTour(tuple(newtour), tuple(walk)))

        return tuple(newtour)

    def RemoveEvenRedundantEdges(tour: Tuple[int, ...],
                                 tours: List[Tuple[int, ...]]) -> Tuple[int, ...]:
        edgeset = list(edges(tour))
        for edge in map(frozenset, edgeset):
            ects = edgecount_tours(tours)[edge]
            ect = edgecount_tour(tour)[edge]
            if ects > ect and ect % 2 == 0:
                # check if tour remains connected to node 0 when removing edge 2x
                nodes = {0}
                remaining = set(map(frozenset, edges(tour)))
                remaining.discard(edge)
                if ect > 2:
                    remaining.clear()  # skip to else if no connection is in danger
                while remaining:
                    stop = True
                    to_remove = None
                    for edge_ in remaining:
                        if nodes.intersection(edge_):
                            nodes.update(edge_)
                            to_remove = edge_
                            stop = False
                            break
                    if to_remove:
                        remaining.remove(to_remove)
                    if stop:
                        break
                else:
                    # remove 2 edges
                    edgeset.remove(edge)
                    edgeset.remove(edge)
        return ReorderToClosedWalk(edgeset)

    # first make a starting solution
    # all edges in graph + dijkstra between odd connections
    edges_ = list(map(set, list(set(frozenset((start, end)) for start in G for end in G[start]))))
    odd = [k for k, v in G.items() if len(v) % 2]
    for _ in range(0, len(odd), 2):
        odd1 = odd.pop()
        odd2 = odd.pop()
        edges_ += list(map(set, edges((odd1,)+dijkstra[odd1][odd2][1]+(odd2,))))

    singlePath = ReorderToClosedWalk(edges_)

    bestSolution = [singlePath]+[(0,)]*(k-1)
    currentSolution = bestSolution

    bestSolutionValue = w_max_tours(bestSolution)
    currentSolutionValue = w_max_tours(bestSolution)

    nOfItsWithoutImprovement = 0

    tabuList = TabuList(tabuTenure)

    if maxRunningTime:
        startTime = time()

    while (nOfItsWithoutImprovement < maxNOfItsWithoutImprovement and not
           (maxRunningTime and time() > startTime + maxRunningTime)):
        nOfItsWithoutImprovement += 1
        tabuList.tick()
        currentAvgWeight = w_avg_tours(currentSolution)

        neighborhood: List[Tuple[Tuple[int]]] = []

        # compute neighborhood
        current_max_tour = max(currentSolution, key=w_tour)
        current_max_tour_idx = currentSolution.index(current_max_tour)
        for i in range(len(current_max_tour)-2):
            semilocal_tours = currentSolution.copy()
            walk = current_max_tour[i:i+3]  # 3 nodes, 2 edges
            semilocal_tours[current_max_tour_idx] = SeparateWalkFromTour(current_max_tour, walk)
            semilocal_tours[current_max_tour_idx] = RemoveEvenRedundantEdges(
                semilocal_tours[current_max_tour_idx], semilocal_tours)
            if time() > startTime + maxRunningTime + 120:
                break  # kill program after max_running_time+120 seconds
            for other_tour_idx in range(k):
                if (other_tour_idx == current_max_tour_idx) or (random() < dropout):
                    continue
                local_tours = semilocal_tours.copy()
                other_tour = local_tours[other_tour_idx]

                local_tours[other_tour_idx] = MergeWalkWithTour(other_tour, walk)
                local_tours[other_tour_idx] = RemoveEvenRedundantEdges(
                    local_tours[other_tour_idx], local_tours)

                neighborhood.append(tuple(local_tours))

        # filter tabu, reduce max length
        try:
            currentSolution = min(
                filter(lambda x: not tabuList.get(x),
                       neighborhood),
                key=lambda x: cost(x, currentAvgWeight))
        except ValueError:  # no non-tabu neighbors, were done
            return bestSolution
        tabuList.add(currentSolution)
        currentSolution = list(currentSolution)
        currentSolutionValue = w_max_tours(currentSolution)

        if currentSolutionValue < bestSolutionValue:
            print('.', end='')
            nOfItsWithoutImprovement = 0
            bestSolutionValue = currentSolutionValue
            bestSolution = currentSolution

        dropout = dropout_fn(dropout)

    print()
    return bestSolution
