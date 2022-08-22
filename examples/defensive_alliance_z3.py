import os
import networkx as nx

from alliancelib.algorithms.z3 import defensive_alliance_solver

g = nx.gnp_random_graph(50, 0.10)
status, alliance = defensive_alliance_solver(g, solution_range=(1, 10))

print(alliance)
#print(status == LpSolutionOptimal, len(alliance.vertices()))
