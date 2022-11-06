import networkx as nx

from alliancelib.algorithms.heuristics.swarm import \
    DAABC

g = nx.gnp_random_graph(100, 0.25)
solver = DAABC()
solver.run(g)
