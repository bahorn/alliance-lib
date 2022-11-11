import networkx as nx

from alliancelib.algorithms.direct.solution_size import \
    defensive_alliance_parallel

g = nx.gnp_random_graph(100, 0.05)
print(nx.is_connected(g))
solution = defensive_alliance_parallel(g, 5, -1, threads=16)
print(solution)
