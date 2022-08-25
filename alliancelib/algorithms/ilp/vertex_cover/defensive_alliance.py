# pylint: disable=C0103
"""
Vertex Cover Algorithms.
"""
from typing import Optional

from pulp.apis import LpSolver as Solver

from alliancelib.ds import \
    Graph, \
    DefensiveAlliance, \
    convert_to_da, \
    defensive_alliance_threshold

from .common import VertexCover
from .threshold_alliance import threshold_alliance_solver


def defensive_alliance_solver(graph: Graph,
                              vc: VertexCover,
                              solver: Solver,
                              r: int = -1
                              ) -> Optional[DefensiveAlliance]:
    """
    Find an defensive alliance based on vertex cover.
    """
    thresholds = {
        node: defensive_alliance_threshold(graph, node, r)
        for node in graph.nodes()
    }

    alliance = threshold_alliance_solver(graph, thresholds, vc, solver)

    if alliance:
        return convert_to_da(alliance)

    return None


__all__ = [
    'defensive_alliance_solver'
]
