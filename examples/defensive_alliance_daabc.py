import networkx as nx

from alliancelib.algorithms.heuristics.swarm import \
    abc_model, ba_model, sa_model, DAMetaHeuristic

g = nx.gnp_random_graph(1000, 0.25)
solver = DAMetaHeuristic(abc_model())
solver.run(g, time_limit=300)
