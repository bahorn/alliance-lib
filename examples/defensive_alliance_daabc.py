import networkx as nx

from alliancelib.algorithms.heuristics.swarm import \
    abc_model, ba_model, sa_model, DAMetaHeuristic

g = nx.gnp_random_graph(250, 0.05)
solver = DAMetaHeuristic(sa_model())
solver.run(g)
