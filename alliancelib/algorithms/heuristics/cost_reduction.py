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


class CostReductionAlgo:
    def __init__(self, graph, score_function, accept_function, p_add=0.6):
        self.graph = graph
        self.p_add = p_add
        self.score_function = score_function
        self.accept_function = accept_function
        self.return_value = None
        self.setup()

    def best(self):
        return self.return_value

    def setup(self):
        first_vertex = random.choice(list(self.graph.nodes()))
        self.current = (
            self.score_function(self.graph, set([first_vertex])),
            set([first_vertex])
        )
        self.best_res = (float('inf'), set())

    def run(self, generations: int = 25):
        for _ in range(generations):
            candidates = []
            # decide to either add or remove a vertex
            if random.random() > self.p_add and len(self.current) > 0:
                candidates = [
                    self.current[1] - set([i]) for i in self.current[1]
                ]
            else:
                candidates = list(filter(
                        lambda x: x not in self.current[1],
                        [
                            self.current[1].union(set([i]))
                            for i in self.graph.nodes()
                        ]
                ))

            round_best: tuple[float, NodeSet] = (float('inf'), set())

            # score each candidate
            for candidate in candidates:
                score = self.score_function(self.graph, candidate)
                if score < round_best[0]:
                    round_best = (score, candidate)

            self.current = round_best

            # update if we found anything better
            if round_best[0] < self.best_res[0]:
                self.best_res = round_best

                if self.accept_function(self.graph, self.best_res[1]):
                    self.return_value = self.best_res[1]


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


def DACostReduction(graph, p_add, r=-1):
    def accept_function(graph: Graph, ns: NodeSet) -> bool:
        return is_defensive_alliance(graph, ns, r)

    # Look at the number of vertices we need to add to make it protected.
    def score_function(graph: Graph, ns: NodeSet) -> float:
        return da_score(graph, ns, r)

    return CostReductionAlgo(graph, score_function, accept_function, p_add)


__all__ = [
    'reduce_cost_core',
    'defensive_alliance_reduce_cost',
    'DACostReduction'
]
