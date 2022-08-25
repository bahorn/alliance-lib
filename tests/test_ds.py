import pytest
import networkx as nx
from alliancelib.ds.alliances.da import DefensiveAlliance
from alliancelib.ds.vertex_set import ConstraintException


def iterative_threshold(n, r):
    for i in range(0, n + 1):
        if i >= ((n - i) + r):
            return i


def base_test_da_complete(n, r):
    g = nx.complete_graph(n)
    possible_set = [i for i in range(0, n)]

    # subtract one to avoid include a vertex twice
    threshold = iterative_threshold(n - 1, r)

    if not threshold:
        return

    # print(threshold, set(possible_set[0:threshold]))

    # +1 is added to the threshold, as we need threshold + 1 vertices in the
    # set, as each vertex needs threshold neighbours.

    for i in range(0, threshold + 1):
        with pytest.raises(ConstraintException):
            DefensiveAlliance(g, set(possible_set[0:i]), r=r)

    for i in range(threshold + 1, n):
        DefensiveAlliance(g, set(possible_set[0:i]), r=r)


def test_da_complete():
    for i in range(5,  50):
        for r in range(-3, 3):
            print(i, r)
            base_test_da_complete(i, r)
