# pylint: disable=C0103
"""
Vertex Cover Algorithms.
"""
from typing import Any, Dict, Optional
from itertools import combinations

from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from pulp.apis import LpSolver as Solver
from pulp.constants import \
    LpStatus, \
    LpSolutionOptimal, \
    LpSolutionIntegerFeasible

from alliancelib.ds import \
    Graph, \
    NodeSet, \
    ThresholdAlliance, \
    convert_to_da, \
    neighbours_in_set, \
    neighbours_in_set_count, \
    defensive_alliance_threshold

VertexCover = NodeSet


def valid_solution(status: LpStatus) -> bool:
    """
    Test if the ILP was solved, if not optimal.
    """
    return status in [LpSolutionIntegerFeasible, LpSolutionOptimal]


def variable_name(name: Any) -> str:
    """
    Maping sets of vertices to a variable name
    """
    name_ = str(name).replace(" ", '')
    return f'v_{name_}'


def vc_ilp_model(graph: Graph,
                 thresholds: Dict,
                 vc: VertexCover,
                 adjacent: Dict
                 ) -> LpProblem:
    """
    Generate an ILP model for a instance of threshold alliance parameterized by
    vertex cover.
    """
    problem = LpProblem("Vertex_Cover_Threshold_Alliance", LpMinimize)

    # create the variables for each of the 2^vc potential neighbours
    vertices = []
    vc_adjacent: Dict = {i: [] for i in vc}

    for vc_neighours, neighbourhood in adjacent.items():
        variable = LpVariable(
            variable_name(vc_neighours),
            lowBound=0,
            upBound=len(neighbourhood),
            cat='Integer'
        )
        vertices.append(variable)

        for i in vc_neighours:
            vc_adjacent[i].append(variable)

    problem += lpSum(vertices)

    # now for each vertex in the vc, we need to find all the sets of variables
    # it is adjacent to in the vc, and check it is >= its threshold.
    # This has to also subtract the neighbours in the vc from it.
    for vertex in vc:
        # compute the new threshold
        new_threshold = thresholds[vertex] \
                - neighbours_in_set_count(graph, vertex, vc)
        # if new_threshold is negative, the vertex is already protected, we
        # just need to verify the rest are protected so we do need to still
        # solve the ILP.
        # If we hit a case where we already have the full alliance, the ILP
        # solver will find the solution instantly.
        problem += lpSum(vc_adjacent[vertex]) >= new_threshold

    return problem


def neighbour_set(graph: Graph,
                  thresholds: Dict,
                  vc: VertexCover,
                  subset: NodeSet
                  ) -> Dict:
    """
    Discover the vertices that are adjacent to ones in the VC that can possibly
    be protected by it.

    There are at most 2^vc items in res.
    """
    res: Dict = {}
    # We only care about nodes not in the VC, as we have already decided their
    # value.
    possible = filter(lambda x: x not in vc, graph.nodes())

    for vertex in possible:
        # We need to find out if the subset of nodes we have selected from the
        # vertex cover can actually protect this vertex.
        neighbours = neighbours_in_set(graph, vertex, subset)
        if len(neighbours) < thresholds[vertex]:
            continue

        # now we add this to the neighbours of this combination.
        if tuple(neighbours) not in res:
            res[tuple(neighbours)] = set()

        res[tuple(neighbours)] = res[tuple(neighbours)].union({vertex})

    return res


def model_to_alliance(graph: Graph,
                      thresholds: Dict,
                      model: LpProblem,
                      vc: NodeSet,
                      ns: Dict
                      ) -> ThresholdAlliance:
    """
    Converts a solved model into a threshold alliance.
    """
    vertices = vc

    state = {
        variable.name: variable.varValue
        for variable in model.variables()
    }

    for name, neighbours in ns.items():
        count = int(state[variable_name(name)])
        vertices = vertices.union(
            set(list(neighbours)[0:count])
        )

    return ThresholdAlliance(graph, vertices, thresholds)


def threshold_alliance_vertex_cover(
                                    graph: Graph,
                                    thresholds: Dict,
                                    vc: VertexCover,
                                    solver: Solver,
                                    ) -> Optional[ThresholdAlliance]:
    """
    Computes an alliance based of a known vertex cover.
    This has a O(2^vc * ILP), which isn't good!
    """
    # First, detect if we can include any single vertex as a solution on its
    # own.
    # We have do this, else we miss potential solutions.
    # these can be combined with any other alliance that doesn't already
    # include them to produce a new alliance.
    for node, threshold in thresholds.items():
        if threshold > 0:
            continue
        return ThresholdAlliance(graph, {node}, thresholds)

    # Next, branch on every vertex in the VC.
    # Worth noting its hard to bound, so we kinda have to try all combinations.
    # Starting from 2, due to the previous step.
    for i in range(2, len(vc) + 1):
        for selected_vertices in combinations(vc, i):
            # For this combination of vertices we first discover neighbours of
            # the selected subset of the vc.
            ns = neighbour_set(
                graph, thresholds, vc, set(selected_vertices)
            )

            if not ns:
                continue

            model = vc_ilp_model(
                graph, thresholds, set(selected_vertices), ns
            )
            solver.solve(model)

            if not valid_solution(model.status):
                continue

            # now convert the results into a threshold alliance.

            return model_to_alliance(
                graph, thresholds, model, set(selected_vertices), ns
            )

    return None


def defensive_alliance_vertex_cover(
                                    graph: Graph,
                                    vc: VertexCover,
                                    solver: Solver,
                                    r: int = -1
                                    ) -> Optional[ThresholdAlliance]:
    """
    Find an defensive alliance based on vertex cover.
    """
    thresholds = {
        node: defensive_alliance_threshold(graph, node, r)
        for node in graph.nodes()
    }

    alliance = threshold_alliance_vertex_cover(graph, thresholds, vc, solver)

    if alliance:
        return convert_to_da(alliance)

    return None


__all__ = [
    'threshold_alliance_vertex_cover',
    'defensive_alliance_vertex_cover'
]
