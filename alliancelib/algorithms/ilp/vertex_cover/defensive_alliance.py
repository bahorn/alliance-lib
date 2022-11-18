# pylint: disable=C0103
"""
Vertex Cover Algorithms.
"""
from typing import Optional

from pulp.apis import LpSolver as Solver

from alliancelib.ds.types import Graph
from alliancelib.ds.alliances.da import \
    DefensiveAlliance, \
    defensive_alliance_threshold
from alliancelib.ds.alliances.conversion import convert_to_da

from .common import VertexCover
from .threshold_alliance import threshold_alliance_solver


def defensive_alliance_solver(vertex_cover: VertexCover,
                              solver: Solver,
                              r: int = -1,
                              solution_range = (1, None)
                              ) -> Optional[DefensiveAlliance]:
    """
    Find an defensive alliance based on vertex cover.
    """
    graph = vertex_cover.graph()

    thresholds = {
        node: defensive_alliance_threshold(graph, node, r)
        for node in graph.nodes()
    }

    alliance = threshold_alliance_solver(vertex_cover, thresholds, solver, solution_range)

    if alliance:
        return convert_to_da(alliance)

    return None


__all__ = [
    'defensive_alliance_solver'
]
