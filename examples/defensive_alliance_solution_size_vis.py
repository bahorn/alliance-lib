import matplotlib.pyplot as plt
import networkx as nx

from alliancelib.algorithms.direct.solution_size import \
    defensive_alliance

g = nx.gnp_random_graph(15, 0.33)
solution = defensive_alliance(g, 5, -1)


color_map = ['blue' for node in g.nodes()]
for node in solution.vertices():
    color_map[node] = 'red'

nx.draw(g, node_color=color_map)
plt.show()
