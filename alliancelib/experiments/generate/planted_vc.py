"""
Planted VertexCover
"""
import networkx as nx
import random
from alliancelib.algorithms.ilp.vertex_cover.common import VertexCover


def planted_vc(n, max_vc, p_internal, p_external, seed=None):
    random.seed = seed
    g = nx.Graph()

    print(n, max_vc, p_internal, p_external)

    g.add_nodes_from(range(n))

    # Create the base graph
    for vertex in range(max_vc):
        for target in range(max_vc):
            if random.random() < p_internal and target != vertex:
                g.add_edge(vertex, target)

    # Join the extra to the base graph at k random points
    for vertex in range(max_vc, n):
        for target in range(max_vc):
            if random.random() < p_external:
                g.add_edge(vertex, target)

    vc = VertexCover(g, set(range(max_vc)))
    print(vc)
    return (set(range(max_vc)), g)
