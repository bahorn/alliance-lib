"""

"""
import networkx as nx
import random


def planted_vc(n, max_vc, p_internal, p_external, seed=None):
    random.seed = seed
    g = nx.Graph()

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

    return set(range(max_vc)), g
