"""
Encapulate a generator for a specific graph type.
"""
import itertools
import numpy as np
import networkx as nx

from alliancelib.experiments.generate import planted_vc
from alliancelib.experiments.cleaning import min_degree_add
from .util import gen_seed


class GraphGenerator:
    """
    Base class to represent a graph generator.
    """

    def __init__(self):
        pass

    def count(self):
        return 0

    def at(self):
        raise IndexError


class PreGeneratedGenerator(GraphGenerator):
    """
    Base class for storing a bunch of graphs that are generated on
    construction.
    """

    def __init__(self, generated={}):
        self.generated = generated

        super().__init__()

    def count(self):
        return len(self.generated)

    def at(self, idx):
        res = self.generated[idx]
        return res


class GNPBetterGenerator(PreGeneratedGenerator):
    """
    GNP Generator, but with a fixed degree
    """

    def __init__(self, n_range, d_range, split='geom', axis=10, samples=3,
                 seed=0, min_degree=2):
        splitter = np.linspace
        if split == 'geom':
            splitter = np.geomspace

        nr = list(
            map(int, splitter(n_range[0], n_range[1], num=axis))
        )
        dr = list(
            map(float, splitter(d_range[0], d_range[1], num=axis))
        )

        self.potential = [
            (x, y, s)
            for x, y, s in itertools.product(nr, dr, range(samples))
        ]

        self.axis = axis
        self.samples = samples
        self.seed = seed
        self.split = split
        self.min_degree = min_degree

        super().__init__(
            {idx: self.generate(idx) for idx in range(len(self.potential))}
        )

    def generate(self, idx, attempts=5):
        """
        Generate a graph, and its properties for a specific index
        """
        x, y, s = self.potential[idx]
        p = y/x
        res1 = {'n': x, 'd': y, 'iteration': s}
        for i in range(attempts):
            seed = gen_seed([self.seed, x, y, i, s])
            g = nx.gnp_random_graph(x, p, seed)
            g = min_degree_add(g, self.min_degree)
            if nx.is_connected(g):
                return (res1, g)

        return (res1, None)


def range_to_list(t, r, split, axis):
    splitter = np.linspace
    if split == 'geom':
        splitter = np.geomspace

    if isinstance(r, tuple):
        if r[0] == r[1]:
            return [r[0]]

        return list(map(t, splitter(r[0], r[1], num=axis)))

    return [r]


class WaxmanGenerator(PreGeneratedGenerator):
    """
    Waxman Generator, but with a fixed degree
    """

    def __init__(self, n_range, b_range, a_range, split='geom',
                 axis=10, samples=3, seed=0):
        nr = range_to_list(int, n_range, split, axis)
        br = range_to_list(float, b_range, split, axis)
        ar = range_to_list(float, a_range, split, axis)

        self.potential = [
            (n, b, a, s)
            for n, b, a, s in itertools.product(nr, br, ar, range(samples))
        ]

        self.axis = axis
        self.samples = samples
        self.seed = seed
        self.split = split

        super().__init__(
            {idx: self.generate(idx) for idx in range(len(self.potential))}
        )

    def generate(self, idx, attempts=5):
        """
        Generate a graph, and its properties for a specific index
        """
        n, b, a, s = self.potential[idx]
        res1 = {'n': n, 'b': b, 'a': a, 'iteration': s}
        for i in range(attempts):
            seed = gen_seed([self.seed, n, b, a, s, i])
            g = nx.waxman_graph(n, beta=b, alpha=a, seed=seed)
            if nx.is_connected(g):
                return (res1, g)

        return (res1, None)


class PlantedVertexCoverGenerator(PreGeneratedGenerator):
    """
    Planted Vertex Cover Generator
    """

    def __init__(self, ni_range, nx_range, pi_range, px_range, split='geom',
                 axis=10, samples=3, seed=0):
        n_i = range_to_list(int, ni_range, split, axis)
        n_x = range_to_list(int, nx_range, split, axis)
        p_i = range_to_list(float, pi_range, split, axis)
        p_x = range_to_list(float, px_range, split, axis)

        self.potential = [
            (ni, nx, pi, px, s)
            for ni, nx, pi, px, s in itertools.product(
                n_i, n_x, p_i, p_x, range(samples)
            )
        ]

        self.axis = axis
        self.samples = samples
        self.seed = seed
        self.split = split

        super().__init__(
            {idx: self.generate(idx) for idx in range(len(self.potential))}
        )

    def generate(self, idx, attempts=5):
        """
        Generate a graph, and its properties for a specific index
        """
        n_i, n_x, p_i, p_x, s = self.potential[idx]
        res1 = {'n_i': n_i, 'n_x': n_x, 'p_i': p_i, 'p_x': p_x, 'iteration': s}
        for i in range(attempts):
            seed = gen_seed([self.seed, n_i, n_x, p_i, p_x, s, i])
            vc, g = planted_vc(n_i + n_x, n_i, p_i, p_x, seed=seed)
            if nx.is_connected(g):
                return (res1, (vc, g))

        return (res1, None)
