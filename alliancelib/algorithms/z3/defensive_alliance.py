# pylint: disable=C0103
"""
Z3 solver interface for r-Defensive Alliance
"""
from typing import Optional


from alliancelib.ds.types import Graph
from alliancelib.ds.alliances.da import \
    DefensiveAlliance, \
    defensive_alliance_threshold
from alliancelib.ds.alliances.conversion import convert_to_da

from .threshold_alliance import threshold_alliance_solver


def defensive_alliance_solver(graph: Graph,
                              r: int = -1,
                              solution_range: tuple[
                                  Optional[int], Optional[int]
                              ] = (1, None)
                              ) -> tuple[
                                    bool,
                                    Optional[DefensiveAlliance]
                                   ]:
    """
    Find a defensive alliance in a graph.
    """

    thresholds = {
        node: defensive_alliance_threshold(graph, node, r)
        for node in graph.nodes()
    }

    status, alliance = threshold_alliance_solver(
        graph, thresholds, solution_range
    )

    converted = None

    if alliance:
        converted = convert_to_da(alliance)

    return (status, converted)


__all__ = [
    'defensive_alliance_solver'
]
