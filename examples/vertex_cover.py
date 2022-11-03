import os
import networkx as nx
from pulp.apis import get_solver
from alliancelib.algorithms.ilp.vertex_cover.vertex_cover import \
        vertex_cover_solver


g = nx.gnp_random_graph(100, 0.2)
solver = get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD')
result = vertex_cover_solver(g, solver)
print(result)
