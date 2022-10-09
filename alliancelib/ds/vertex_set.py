"""
Various classes that represent VertexSets.

These are used to build the representation of alliances.
"""
from collections.abc import Callable
from .types import Graph, NodeId, NodeSet
import networkx as nx

class VertexSet:
    """
    Base representation of a set of vertices.
    """

    def __init__(self, graph: Graph, indices: NodeSet):
        self._graph = graph
        self._indices = indices

    def graph(self) -> Graph:
        """
        Return the graph.
        """
        return self._graph

    def vertices(self) -> NodeSet:
        """
        return the vertices.
        """
        return self._indices

    def __str__(self) -> str:
        return type(self).__name__ + str(self._indices)

    def __dict__(self):
        return list(self._indices)

    def __len__(self):
        return len(self._indices)


class ConstraintException(Exception):
    """
    Thrown when a constraint can't be satisified in the construction of a
    ConstrainedVertexSet.
    """


VertexConstraint = Callable[[Graph, NodeId, NodeSet], bool]


class ConstrainedVertexSet(VertexSet):
    """
    An VertexSet that runs a function to validate it.
    """

    def __init__(self,
                 graph: Graph,
                 indices: NodeSet,
                 constraint: VertexConstraint):
        super().__init__(graph, indices)

        # Check if each vertex satisifies the constraint
        for vertex in self._indices:
            if constraint(graph, vertex, self._indices):
                continue
            raise ConstraintException()


__all__ = [
    'VertexSet',
    'ConstrainedVertexSet',
    'VertexConstraint',
    'ConstraintException'
]
