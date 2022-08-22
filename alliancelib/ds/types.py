"""
Common types
"""
from typing import Any, Set
from networkx import Graph as NXGraph

Graph = NXGraph

# Defining this as its unclear what types NetworkX supports for indexing nodes.
NodeId = Any
NodeSet = Set[NodeId]
