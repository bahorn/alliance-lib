"""

"""
import networkx as nx


def fixed_gmda(k):
    g = nx.complete_graph(2*k + 1)
    core_path = [(2*k + 1) + i for i in range(k)]
    p = nx.cycle_graph(core_path)

    n = nx.compose(g, p)

    for idx, node in enumerate(core_path):
        n.add_edge(node, idx*2)
        n.add_edge(node, idx*2 + 1)

    return g
