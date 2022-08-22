"""
Common types
"""
from typing import Any
from networkx import Graph as NXGraph

Graph = NXGraph

# Defining this as its unclear what types NetworkX supports for indexing nodes.
NodeId = Any
