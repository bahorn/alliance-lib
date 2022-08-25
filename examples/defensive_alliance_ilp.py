import os
import networkx as nx
from pulp.apis import get_solver
from pulp.constants import LpSolutionOptimal
from alliancelib.algorithms.ilp.direct import defensive_alliance_solver

g = nx.gnp_random_graph(100, 0.08)
solver = get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD')
status, alliance = defensive_alliance_solver(g, solver)

print(alliance)
print(status == LpSolutionOptimal, len(alliance.vertices()))
