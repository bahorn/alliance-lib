"""

"""
import networkx as nx
from alliancelib.ds.alliances.da import DefensiveAlliance


def fixed_gmda(k, extra=0):
    start_range = 2*k + 1 + extra
    g = nx.complete_graph(start_range)
    core_path = [start_range + i for i in range(k)]
    p = nx.cycle_graph(core_path)

    n = nx.compose(g, p)

    for idx, node in enumerate(core_path):
        n.add_edge(node, idx*2)
        n.add_edge(node, idx*2 + 1)

    DefensiveAlliance(n, range(start_range, start_range+k), r=-1)

    return n
