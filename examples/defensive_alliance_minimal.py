import networkx as nx

from alliancelib.algorithms.direct.minimal import \
    find_gmda

g = nx.gnp_random_graph(50, 0.2)
solution = find_gmda(g)

print(solution)
