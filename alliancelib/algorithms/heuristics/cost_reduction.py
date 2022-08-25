# pylint: disable=C0103
"""
Heuristic Algorithm based around reducing the number of external vertices
needed.
"""
import random
from typing import Optional
from alliancelib.ds.types import Graph, NodeSet
from alliancelib.ds.vertex_set import VertexSet
from alliancelib.ds.alliances.da import \
    DefensiveAlliance, \
    is_defensive_alliance
from alliancelib.ds.alliances.conversion import convert_to_da

from .cost_functions import da_score, AcceptFunction, ScoreFunction


def reduce_cost_core(
                     graph: Graph,
                     score_function: ScoreFunction,
                     accept_function: AcceptFunction,
                     steps: int = 1024,
                     p_add: float = 0.60
                     ) -> Optional[VertexSet]:
    """
    Base of the algorithm.
    """
    # Setup
    first_vertex = random.choice(list(graph.nodes()))
    current: tuple[float, NodeSet] = (
        score_function(graph, set([first_vertex])), set([first_vertex])
    )
    best: tuple[float, NodeSet] = (float('inf'), set())

    # pick best node for reducing the cost
    for _ in range(steps):
        candidates = []
        # decide to either add or remove a vertex
        if random.random() > p_add and len(current) > 0:
            candidates = [current[1] - set([i]) for i in current[1]]
        else:
            candidates = list(filter(
                    lambda x: x not in current[1],
                    [current[1].union(set([i])) for i in graph.nodes()]
            ))

        round_best: tuple[float, NodeSet] = (float('inf'), set())

        # score each candidate
        for candidate in candidates:
            score = score_function(graph, candidate)
            if score < round_best[0]:
                round_best = (score, candidate)

        current = round_best

        # update if we found anything better
        if round_best[0] < best[0]:
            best = round_best

    if accept_function(graph, best[1]):
        return VertexSet(graph, best[1])

    return None


def defensive_alliance_reduce_cost(
                                   graph: Graph,
                                   r: int = -1,
                                   steps: int = 1024,
                                   p_add: float = 0.9
                                   ) -> Optional[DefensiveAlliance]:
    """
    Heuristic to find Defensive Alliances
    """
    # Just check if its a DA.
    def accept_function(graph: Graph, ns: NodeSet) -> bool:
        return is_defensive_alliance(graph, ns, r)

    # Look at the number of vertices we need to add to make it protected.
    def score_function(graph: Graph, ns: NodeSet) -> float:
        return da_score(graph, ns, r)

    res = reduce_cost_core(
        graph, score_function, accept_function, steps, p_add
    )

    if res:
        return convert_to_da(res, r)

    return None


__all__ = [
    'reduce_cost_core',
    'defensive_alliance_reduce_cost'
]
