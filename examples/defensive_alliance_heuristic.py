import networkx as nx

from alliancelib.algorithms.heuristics.cost_reduction import \
    DACostReduction

g = nx.gnp_random_graph(1000, 0.005)
p_add = 0.8
p_best = 0.9
solver = DACostReduction(g, p_add, p_best, r=-1)
solver.run(100)
print(solver.best())
