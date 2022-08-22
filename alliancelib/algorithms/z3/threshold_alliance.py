"""
Implementation of an Z3 solver for Threshold Alliance
"""
from typing import Any, Dict, Optional

from z3 import Bool, Int, If, Sum, Solver, sat

from alliancelib.ds import Graph, ThresholdAlliance


def variable_name(name: Any) -> str:
    """
    Maping vertices to variable names
    """
    return f'v_{name}'


def bool_to_int(inp: Bool) -> Int:
    return If(inp, 1, 0)


def threshold_alliance_problem(graph: Graph,
                               thresholds: Dict,
                               solution_range: tuple[
                                    Optional[int], Optional[int]
                               ],
                               ) -> tuple[Dict, Solver]:
    """
    Generate an instance of a threshold alliance problem.
    """
    problem = Solver()

    # Create a boolean variable for each vertex
    vertices = []
    vertices_lookup: Dict = {'forwards': {}, 'backwards': {}}
    for vertex in graph.nodes():
        variable = Bool(variable_name(vertex))
        vertices.append(
            variable
        )
        # assuming these will not clash
        vertices_lookup['forwards'][vertex] = variable
        vertices_lookup['backwards'][variable] = vertex

    # Add constraints on solution range
    if solution_range[0]:
        problem += Sum(list(map(bool_to_int, vertices))) >= solution_range[0]
    if solution_range[1]:
        problem += Sum(list(map(bool_to_int, vertices))) <= solution_range[1]

    # Add constraints for the thresholds
    for vertex in graph.nodes():
        # find the neighbours
        neighbours = [
            vertices_lookup['forwards'][neighbour]
            for neighbour in graph.neighbors(vertex)
        ]
        demand = thresholds[vertex]
        problem += Sum(list(map(bool_to_int, neighbours))) >= \
            vertices_lookup['forwards'][vertex] * demand

    return (vertices_lookup, problem)


def threshold_alliance_solver(graph: Graph,
                              thresholds: Dict,
                              solution_range: tuple[
                                Optional[int], Optional[int]
                              ] = (1, None)
                              ) -> tuple[
                                    bool,
                                    Optional[ThresholdAlliance]
                                   ]:
    """
    ILP solver for threshold alliances
    """
    variables, problem = threshold_alliance_problem(
            graph, thresholds, solution_range
    )

    if problem.check() != sat:
        return (False, None)

    solution_indices = []

    m = problem.model()
    for variable in variables['backwards']:
        print(variable, m)
        if m.evaluate(variable):
            solution_indices.append(variables['backwards'][variable])

    solution = None
    if len(solution_indices) > 0:
        solution = ThresholdAlliance(graph, set(solution_indices), thresholds)

    return (True, solution)


__all__ = [
    'threshold_alliance_solver',
    'threshold_alliance_problem'
]
