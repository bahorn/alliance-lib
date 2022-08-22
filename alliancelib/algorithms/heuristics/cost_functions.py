# pylint: disable=C0103
"""
Collection of cost functions to use for evaluating an Alliance
"""
from collections.abc import Callable
from alliancelib.ds import \
    Graph, \
    NodeSet, \
    neighbours_in_set, \
    defensive_alliance_threshold


# Type definitions for functions that guide towards an acceptable solution
AcceptFunction = Callable[[Graph, NodeSet], bool]
ScoreFunction = Callable[[Graph, NodeSet], float]


def da_score(graph: Graph, ns: NodeSet, r: int = -1) -> float:
    """
    Compute a score on the quality of a Defensive Alliance.

    Currently just the number of vertices away from being fully protected.
    """
    score = 0.0
    for vertex in ns:
        threshold = defensive_alliance_threshold(graph, vertex, r)
        count = neighbours_in_set(graph, vertex, ns)
        score += (threshold - count) if (count < threshold) else 0

    return score
