"""
Implementation of an ILP solver for Threshold Alliance
"""
from typing import Any, Dict, Optional

from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from pulp.constants import LpStatus
from pulp.apis import LpSolver as Solver

from alliancelib.ds import Graph, ThresholdAlliance


def ilp_solution_to_threshold_alliance() -> Optional[ThresholdAlliance]:
    """
    Converts a ILP solution to a threshold alliance
    """
    return None


def variable_name(name: Any) -> str:
    """
    Maping vertices to variable names
    """
    return f'v_{name}'


def threshold_alliance_problem(graph: Graph,
                               thresholds: Dict,
                               solution_range: tuple[
                                    Optional[int], Optional[int]
                               ]
                               ) -> tuple[Dict, LpProblem]:
    """
    Generate an instance of a threshold alliance problem.
    """
    problem = LpProblem("Threshold Alliance", LpMinimize)

    # Create a boolean variable for each vertex
    vertices = []
    vertices_lookup: Dict = {'forwards': {}, 'backwards': {}}
    for vertex in graph.nodes():
        variable = LpVariable(
            variable_name(vertex), lowBound=0, upBound=1, cat='Integer'
        )
        vertices.append(
            variable
        )
        # assuming these will not clash
        vertices_lookup['forwards'][vertex] = variable
        vertices_lookup['backwards'][variable_name(vertex)] = vertex

    # optimization target
    problem += lpSum(vertices)

    # Add constraints on solution range
    if solution_range[0]:
        problem += lpSum(vertices) >= solution_range[0]
    if solution_range[1]:
        problem += lpSum(vertices) <= solution_range[1]

    # Add constraints for the thresholds
    for vertex in graph.nodes():
        # find the neighbours
        neighbours = [
            vertices_lookup['forwards'][neighbour]
            for neighbour in graph.neighbors(vertex)
        ]
        demand = thresholds[vertex]
        problem += lpSum(neighbours) >= \
            vertices_lookup['forwards'][vertex] * demand

    return (vertices_lookup, problem)


def threshold_alliance_solver(graph: Graph,
                              thresholds: Dict,
                              solver: Solver,
                              solution_range: tuple[
                                Optional[int], Optional[int]
                              ] = (1, None)
                              ) -> tuple[
                                    LpStatus,
                                    Optional[ThresholdAlliance]
                                   ]:
    """
    ILP solver for threshold alliances
    """
    variables, problem = threshold_alliance_problem(
            graph, thresholds, solution_range
    )

    problem.solve(solver)
    solution_indices = []

    for variable in problem.variables():
        if variable.varValue == 1.0:
            solution_indices.append(variables['backwards'][variable.name])

    solution = None
    if len(solution_indices) > 0:
        solution = ThresholdAlliance(graph, solution_indices, thresholds)

    return (problem.status, solution)


__all__ = [
    'threshold_alliance_solver',
    'threshold_alliance_problem'
]
