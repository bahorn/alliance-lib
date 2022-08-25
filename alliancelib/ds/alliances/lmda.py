# pylint: disable=C0103
"""
Locally Minimal Defensive Alliance
"""
from itertools import combinations

from alliancelib.ds.types import Graph, NodeSet
from alliancelib.ds.vertex_set import ConstraintException

from .da import DefensiveAlliance


class NotLocallyMinimal(Exception):
    """
    Exception if an alliance is not Locally Minimal.
    """


class LocallyMinimalDefensiveAlliance(DefensiveAlliance):
    """
    Validated representation of a Locally Minimal Defensive Alliance.

    This is a Defensive Alliance where removing any single vertex won't also
    result in another Defensive Alliance.
    """

    def __init__(self, graph: Graph, indices: NodeSet, r: int = -1):
        # attempt to create a Defensive Alliance based on the combinations of
        # vertices.
        # if one exists, we need to raise an exception
        for indices_set in combinations(indices, len(indices) - 1):
            try:
                DefensiveAlliance(graph, set(indices_set), r)
                raise NotLocallyMinimal()
            except ConstraintException:
                continue
        super().__init__(graph, indices, r)


class NotGloballyMinimal(Exception):
    """
    Exception if an alliance is not Globally Minimal.
    """


__all__ = [
    'LocallyMinimalDefensiveAlliance',
    'NotLocallyMinimal'
]
