import networkx as nx

from alliancelib.algorithms.direct.minimal import \
    find_gmda

g = nx.gnp_random_graph(250, 0.05)
solution = find_gmda(g)

print(solution)
