import os
import networkx as nx
from pulp.apis import get_solver
from alliancelib.algorithms.ilp.vertex_cover import \
        defensive_alliance_solver, \
        vertex_cover_solver

threads = 16

solver = [
    get_solver(os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD', msg=False, threads=1)
    for i in range(threads)
]

g = nx.gnp_random_graph(35, 0.2)
vc = vertex_cover_solver(g, solver[0])

alliance = defensive_alliance_solver(
    vc,
    solver,
    solution_range=(1, 10),
    threads=threads
)

print(alliance)
