from collections import deque
from time import time
from typing import Dict



def MMKCPP_TEE_TabuSearch(G: Dict[Dict[float]], tours: List[List[int]], maxNOfItsWithoutImprovement: int = 100,
                          maxRunningTime: float = 0, tabuTenure: int = 20) -> List[List[int]]:
    """
    Perform a tabu search metaheuristic optimization on `tour` in the graph `G`.

    Parameters
    ----------
    G : Dict[Dict[float]]
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
    dijkstra = {k: {} for k in G}  # deepcopy
    for start in dijkstra:
        q = deque(((0, start, []),))
        while q:
            length, current, currentpath = q.popleft()
            if current in dijkstra[start]: continue
            dijkstra[start][current] = (length, tuple(currentpath))
            for next_, weight in G[current].items():
                q.append((length+weight, next_, currentpath+[current]))

    # cost function
    def w_max(tours: List[List[int]]) -> float:
        return max(sum(G[tour[i]][tour[i+1]] for i in range(len(tour)-1)) for tour in tours)
    
    def MergeWalkWithTour(tour: List[int], walk: List[int]) -> List[int]:
        # remove edges from walk that are already in tour
        if len(walk) == 1:
            return tour

        tour_edges = set(frozenset((tour[i], tour[i+1])) for i in range(len(tour)-1))

        while frozenset(walk[0], walk[1]) in tour_edges:
            del walk[0]
            if len(walk) == 1:
                return tour

        while frozenset(walk[-1], walk[-2]) in tour_edges:
            del walk[-1]
            if len(walk) == 1:
                return tour
        
        # find node `t` closest to `u` and `v`, the end nodes of `walk`
        min_idx = None
        min_distance = 999999
        min_sp_v = min_sp_u = None

        for i in range(tour):
            sp_u = dijkstra[node][walk[0]]
            sp_v = dijkstra[walk[-1]][node]
            if sp_u[0]+sp_v[0] < min_distance:
                min_distance = sp_v[0]+sp_u[0]
                min_idx = i
                min_sp_u = sp_u[1]
                min_sp_v = sp_v[1]

        # splice SP(t, u), Ĥ, SP(v, t) into Ci at node t
        return tour[:min_idx+1]+min_sp_u+walk+min_sp_v+tour[min_idx:]

    def SeparateWalkFromTour(tour: List[int], walk: List[int]) -> List[int]:
        u, v = walk[0], walk[-1]
        if # TODO
        if 0 in walk:
            return (left := tour.index())



        
        

    
    bestSolution = tours
    currentSolution = tours

    bestSolutionValue = wmax(tours)
    currentSolutionValue = wmax(tours)

    nOfItsWithoutImprovement = 0

    if maxRunningTime:
        startTime = time()

    while (nOfItsWithoutImprovement < maxNOfItsWithoutImprovement and not
           (maxRunningTime and time() > startTime + maxRunningTime)):
        
        nOfItsWithoutImprovement += 1
        
        # Compute a list of neighborhood solutions N(currentSolution) (with parameter improvementProcedure) in decreasing order of their move value.
    
        # Let neighborSolution be the first solution of the list which is either non-tabu or tabu but
        # neighborSolutionValue < bestSolutionValue (if no such solution exists the algorithm terminates).
        # Set currentSolution = neighborSolution and currentSolutionValue = neighborSolutionValue.
        # If currentSolutionValue < bestSolutionValue then bestSolution=currentSolution, bestSolutionValue = currentSolutionValue and nOfItsWithoutImprovement = 0.
        

