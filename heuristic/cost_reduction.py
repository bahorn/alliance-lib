from alliancelib.algorithms.heuristics.cost_reduction import \
        DACostReduction


class CostReduction:
    def __init__(self, graph, population=100, p_add=0.5):
        self.population = population
        self.best_result = None
        self.graph = graph
        self.p_add = p_add

    def best(self):
        return self.best_result

    def run(self):
        instances = [
            DACostReduction(self.graph, self.population, self.p_add)
            for _ in range(self.population)
        ]
        while True:
            for instance in instances:
                instance.run(1)
                best = instance.best()
                if not self.best_result or \
                        len(self.best_result) < len(best):
                    self.best_result = instance.best()
