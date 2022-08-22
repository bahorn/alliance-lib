import networkx as nx

from alliancelib.algorithms.heuristics.cost_reduction import \
    defensive_alliance_reduce_cost

g = nx.gnp_random_graph(1000, 0.005)
for i in range(100):
    solution = defensive_alliance_reduce_cost(g, -1, steps=100)
    if solution:
        print(solution)
