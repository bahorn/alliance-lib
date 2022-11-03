import os
import networkx as nx
from pulp.apis import get_solver
from alliancelib.algorithms.ilp.vertex_cover import \
        defensive_alliance_solver, \
        vertex_cover_solver


solver = get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD')

g = nx.gnp_random_graph(25, 0.2)
vc = vertex_cover_solver(g, solver)

alliance = defensive_alliance_solver(vc, solver)

print(alliance)
