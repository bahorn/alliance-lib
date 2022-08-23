import networkx as nx

from alliancelib.algorithms.heuristics.genetic import \
    defensive_alliance_genetic

g = nx.gnp_random_graph(500, 0.25)
res = defensive_alliance_genetic(g)
print(res)
