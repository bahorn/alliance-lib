from alliancelib.algorithms.heuristics.genetic import DAGenetic


class GeneticAlgorithm:
    def __init__(self, graph, population=100, cxpb=0.5, mutpb=0.2):
        self.algo = DAGenetic(
            graph,
            population=population,
            cxpb=cxpb,
            mutpb=mutpb,
            threads=1
        )
        self.best_result = None

    def best(self):
        return self.best_result

    def run(self):
        self.algo.initial_population()
        while True:
            self.algo.loop(1)
            self.best_result = self.algo.best()
