# pylint: disable=C0103
"""
Vertex Cover Algorithms.
"""
from typing import Dict, Optional
from itertools import combinations

from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from pulp.apis import LpSolver as Solver

from alliancelib.ds.types import Graph, NodeSet
from alliancelib.ds.alliances.common import \
    neighbours_in_set, \
    neighbours_in_set_count
from alliancelib.ds.alliances.threshold import ThresholdAlliance

from alliancelib.algorithms.ilp.common import variable_name, valid_solution

from .common import VertexCover, VertexCoverSet

import multiprocessing as mp


def vc_ilp_model(graph: Graph,
                 thresholds: Dict,
                 vc: VertexCoverSet,
                 adjacent: Dict,
                 solution_range = (None, None)
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

    if solution_range[0]:
        problem += lpSum(vertices) >= solution_range[0]
    if solution_range[1]:
        problem += lpSum(vertices) <= solution_range[1]

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
                  vc: VertexCoverSet,
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
                      vc: VertexCoverSet,
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


def threshold_alliance_solver(vertex_cover: VertexCover,
                              thresholds: Dict,
                              solver: Solver,
                              solution_range = (1, None),
                              threads=4,
                              ) -> Optional[ThresholdAlliance]:
    """
    Computes an alliance based of a known vertex cover.
    This has a O(2^vc * ILP), which isn't good!
    """
    graph = vertex_cover.graph()
    vc = vertex_cover.vertices()
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

    max_size = len(vc) + 1
    if solution_range[1]:
        if max_size > solution_range[1]:
            max_size = solution_range[1]

    for i in range(1, max_size):
        work_queue = mp.JoinableQueue()

        found_state = mp.Value('b', False)
        manager = mp.Manager()
        state = manager.dict()
        state['alliance'] = []

        def worker(s, q, fs, return_dict):
            while True:
                selected_vertices = q.get()

                if fs.value:
                    q.task_done()
                    continue

                ns = neighbour_set(
                    graph, thresholds, vc, set(selected_vertices)
                )

                if not ns:
                    q.task_done()
                    continue

                new_solution_range = (
                    solution_range[0] - i,
                    solution_range[1] - i
                )

                model = vc_ilp_model(
                    graph,
                    thresholds,
                    set(selected_vertices),
                    ns,
                    solution_range=new_solution_range
                )
                s.solve(model)

                if valid_solution(model.status):
                    fs.value = True
                    alliance = model_to_alliance(
                        graph, thresholds, model, set(selected_vertices), ns
                    )
                    return_dict['alliance'] = alliance.vertices()

                q.task_done()

        processes = []

        for j in range(threads):
            p = mp.Process(
                target=worker,
                daemon=True,
                args=(solver[j], work_queue, found_state, state)
            )
            processes.append(p)
            p.start()

        for selected_vertices in combinations(vc, i):
            # add to queue

            # now convert the results into a threshold alliance.

            # return model_to_alliance(
            #    graph, thresholds, model, set(selected_vertices), ns
            # )
            work_queue.put(selected_vertices)

        work_queue.join()
        if found_state.value:
            return ThresholdAlliance(graph, state['alliance'], thresholds)

    return None


__all__ = [
    'threshold_alliance_solver'
]
