"""
Common
"""
from alliancelib.ds import \
    Graph, \
    NodeSet, \
    VertexSet, \
    ConstraintException


class VertexCover(VertexSet):
    """
    Vertex Cover
    """

    def __init__(self, graph: Graph, indices: NodeSet):
        if len(indices) == 0:
            raise ConstraintException

        for a, b in graph.edges():
            if a not in indices and b not in indices:
                raise ConstraintException

        super().__init__(graph, indices)


# To simplify some algorithms.
VertexCoverSet = NodeSet
