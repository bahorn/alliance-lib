import os
import sys
import networkx as nx
from pulp.apis import get_solver
from pulp.constants import LpSolutionOptimal
from alliancelib.algorithms.ilp.direct import defensive_alliance_solver

g = nx.read_graphml(sys.argv[1])

solver = get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD')
status, alliance = defensive_alliance_solver(g, solver,
        solution_range=(int(sys.argv[2]), None))

print(alliance)
print(status == LpSolutionOptimal, len(alliance.vertices()))
