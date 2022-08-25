import networkx as nx

from alliancelib.algorithms.direct.solution_size import \
    defensive_alliance

g = nx.gnp_random_graph(50, 0.10)
solution = defensive_alliance(g, 5, -1)

print(solution)
