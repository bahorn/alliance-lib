# pylint: disable=C0103
"""
Conversion utilities
"""
from alliancelib.ds.vertex_set import VertexSet

from .da import DefensiveAlliance
from .gmda import GloballyMinimalDefensiveAlliance


# Conversion functions

def convert_to_da(vs: VertexSet, r: int = -1) -> DefensiveAlliance:
    """
    Convert a VertexSet to a DefensiveAlliance
    """
    return DefensiveAlliance(vs.graph(), vs.vertices(), r)


def convert_to_gmda(vs: VertexSet,
                    r: int = -1
                    ) -> GloballyMinimalDefensiveAlliance:
    """
    Convert a VertexSet to a DefensiveAlliance
    """
    return GloballyMinimalDefensiveAlliance(vs.graph(), vs.vertices(), r)


__all__ = [
    'convert_to_da',
    'convert_to_gmda',
]
