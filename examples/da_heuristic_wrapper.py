"""
Script to be used to find better hyperparameters
"""
import sys
import json
import networkx as nx

from alliancelib.algorithms.heuristics.cost_reduction import \
    defensive_alliance_reduce_cost


def test_function(count, steps, p_add):
    res = 0
    for seed in range(25):
        g = nx.gnp_random_graph(1000, 0.005, seed=seed)
        for i in range(count):
            solution = defensive_alliance_reduce_cost(
                g, -1, steps=steps, p_add=p_add
            )
            if solution:
                res += 1
                break
    return [res, count, steps]


if __name__ == "__main__":
    result = test_function(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
    print(json.dumps(result))
