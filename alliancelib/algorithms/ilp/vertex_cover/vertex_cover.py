"""
ILP Formulation to compute the Vertex Cover of a graph
"""
from typing import Optional
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from pulp.apis import LpSolver as Solver

from alliancelib.ds.types import Graph
from alliancelib.algorithms.ilp.common import variable_name, valid_solution

from .common import VertexCover


def vertex_cover_ilp_model(graph: Graph) -> LpProblem:
    """
    Generate a ILP model for finding the vertex cover of a graph.
    """
    problem = LpProblem("Vertex Cover", LpMinimize)
    vertices = {}

    for vertex in graph.nodes():
        variable = LpVariable(
            variable_name(vertex),
            lowBound=0,
            upBound=1,
            cat='Integer'
        )
        vertices[vertex] = variable

    # target is to minimize this!
    problem += lpSum([variable for _, variable in vertices.items()])

    for a, b in graph.edges():
        problem += lpSum([vertices[a], vertices[b]]) >= 1

    return problem


def vertex_cover_solver(graph: Graph, solver: Solver) -> Optional[VertexCover]:
    """
    Solve a Vertex Cover with the given solver.
    """
    model = vertex_cover_ilp_model(graph)
    solver.solve(model)
    if not valid_solution(model.status):
        return None
    state = {
        variable.name: variable.varValue
        for variable in model.variables()
    }
    res = []
    for vertex in graph.nodes():
        if state[variable_name(vertex)] == 1.0:
            res.append(vertex)

    return VertexCover(graph, set(res))
