import os
import networkx as nx
from pulp.apis import get_solver
from networkx.algorithms.approximation import min_weighted_vertex_cover
from alliancelib.algorithms.ilp.vertex_cover import defensive_alliance_solver


g = nx.gnp_random_graph(10, 0.5)
vc = min_weighted_vertex_cover(g)
print(vc)

solver = get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD')
alliance = defensive_alliance_solver(g, vc, solver)

print(alliance)
