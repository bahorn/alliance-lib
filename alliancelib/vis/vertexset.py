"""
Draw a VertexSet using matplotlib
"""
import matplotlib.pyplot as plt
import networkx as nx
from alliancelib.ds import VertexSet


def display(vs: VertexSet):
    """
    Draw the graph using networkxs default graph drawing utils.
    """
    vertices = vs.graph().nodes()
    colour_map = [
        'red' if vertex in vs.vertices() else 'blue'
        for vertex in vertices
    ]
    nx.draw(vs.graph(), node_color=colour_map)
    plt.show()
