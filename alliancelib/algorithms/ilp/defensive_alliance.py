# pylint: disable=C0103
"""
ILP solver interface for r-Defensive Alliance
"""
from typing import Optional

from pulp.constants import LpStatus
from pulp.apis import LpSolver as Solver

from alliancelib.ds import \
    Graph, DefensiveAlliance, convert_ta_to_da, defensive_alliance_threshold

from .threshold_alliance import threshold_alliance_solver


def defensive_alliance_solver(graph: Graph,
                              solver: Solver,
                              r: int = -1,
                              solution_range: tuple[
                                  Optional[int], Optional[int]
                              ] = (1, None)
                              ) -> tuple[
                                    LpStatus,
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
        graph, thresholds, solver, solution_range
    )

    converted = None

    if alliance:
        converted = convert_ta_to_da(alliance)

    return (status, converted)


__all__ = [
    'defensive_alliance_solver'
]
