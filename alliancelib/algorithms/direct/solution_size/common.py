"""
Common for Soltion Size algorithms
"""
from typing import Any
from collections.abc import Callable
from alliancelib.ds import \
    Graph, \
    NodeId, \
    NodeSet

VertexPredicate = Callable[[Graph, NodeId, Any], bool]
SolutionPredicate = Callable[[Graph, NodeSet], bool]


__all__ = [
    'VertexPredicate',
    'SolutionPredicate'
]
