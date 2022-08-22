import networkx as nx

from alliancelib.algorithms.direct.solution_size import \
    defensive_alliance_solution_size

g = nx.gnp_random_graph(50, 0.10)
solution = defensive_alliance_solution_size(g, 5, -1)

print(solution)
