# pylint: disable=E0401,C0103
"""
Genetic Algorithm to find Alliances.

Multiobjective fitness function:
* number of vertices needed to make the alliance protected
* if it possible to chisel it down to a valid alliance.
"""
import random
from typing import Any, List, Dict, Optional

from deap import base
from deap import creator
from deap import tools

from alliancelib.ds.types import Graph, NodeSet
from alliancelib.ds.alliances.da import DefensiveAlliance

from .cost_functions import da_score


def bits_to_nodeset(mapping: Dict, alliance: List[bool]) -> NodeSet:
    """
    Convert a bitmap produced by the GA into a NodeSet for evaluation.
    """
    raw: NodeSet = set()
    for idx, value in enumerate(alliance):
        if value:
            raw = raw.union({mapping[idx]})
    return raw


class DAGenetic:
    """
    Class representing an instance of a GA algorithm to find a DA.
    """
    CXPB, MUTPB = 0.5, 0.2

    def __init__(self, graph: Graph, r: int = -1):
        self.r = r
        self.graph = graph

        self.pop: List = []
        self.fitnesses: Any = None
        self.fits: List = []

        self.nodeset_map = {}
        for idx, node in enumerate(graph.nodes()):
            self.nodeset_map[idx] = node

        self.setup()

    def setup(self):
        """
        Setup the toolbox.
        """
        creator.create("FitnessAlliance", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessAlliance)

        toolbox = base.Toolbox()
        # Boolean attributes are all we use.
        toolbox.register("attr_bool", random.randint, 0, 1)
        # Define our individual
        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attr_bool,
            self.graph.number_of_nodes()
        )
        toolbox.register(
            "population",
            tools.initRepeat,
            list,
            toolbox.individual
        )

        # evaluation function
        def evaluate_alliance(alliance):
            return (
                da_score(
                    self.graph,
                    bits_to_nodeset(self.nodeset_map, alliance),
                    self.r
                ),
                sum(alliance)
            )

        toolbox.register("evaluate", evaluate_alliance)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        self.toolbox = toolbox

    def run(self, generations: int = 25):
        """
        Start the algorithm.
        """
        self.initial_population()
        self.loop(generations)

    def best(self) -> Optional[DefensiveAlliance]:
        """
        Find the best alliance if one exists.
        """
        best_ind = tools.selBest(self.pop, 1)[0]

        if best_ind.fitness.values[0] == 0.0:
            return DefensiveAlliance(
                self.graph,
                bits_to_nodeset(self.nodeset_map, best_ind),
            )

        return None

    def initial_population(self) -> None:
        """
        Setup the initial population
        """
        self.pop = self.toolbox.population(n=100)
        self.fitnesses = map(self.toolbox.evaluate, self.pop)
        for ind, fit in zip(self.pop, self.fitnesses):
            ind.fitness.values = fit

        self.fits = [ind.fitness.values[0] for ind in self.pop]

    def loop(self, generations: int = 25):
        """
        Main GA Loop
        """
        for idx in range(generations):
            print(f'-- Generation {idx} --')
            self.step()

    def step(self):
        """
        Single generation
        """
        # Select the next generation individuals
        offspring = self.toolbox.select(self.pop, len(self.pop))
        # Clone the selected individuals
        offspring = list(map(self.toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.CXPB:
                self.toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < self.MUTPB:
                self.toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        self.pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in self.pop]

        length = len(self.pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')


def defensive_alliance_genetic(
                               graph: Graph,
                               r: int = -1,
                               generations: int = 25
                               ) -> Optional[DefensiveAlliance]:
    """
    Genetic algorithm for finding Defensive Alliances
    """
    dag = DAGenetic(graph, r)
    dag.run(generations)
    return dag.best()


__all__ = [
    'defensive_alliance_genetic'
]
