"""
Implementation of a Mealpy solver using ABC for Defensive Alliance
"""
from alliancelib.ds.alliances.da import DefensiveAlliance
from mealpy.swarm_based.ABC import OriginalABC
from .cost_functions import da_score


def clean_solution(solution):
    res = []
    for i in range(len(solution)):
        if solution[i] >= 0.5:
            res.append(i)
    return res


class DAABC:
    """
    Artificial Bee Colony for Defensive Alliance
    """

    def __init__(self, pop_size=50, n_elites=16, n_others=4, patch_size=5.0,
                 patch_reduction=0.985, n_sites=3, n_elite_sites=1):
        self.pop_size = pop_size
        self.n_elites = n_elites
        self.n_others = n_others
        self.patch_size = patch_size
        self.patch_reduction = patch_reduction
        self.n_sites = n_sites
        self.n_elite_sites = n_elite_sites

    def run(self, graph, generations=1000, r=-1):
        model = OriginalABC(
            generations,
            self.pop_size,
            self.n_elites,
            self.n_others,
            self.patch_size,
            self.patch_reduction,
            self.n_sites,
            self.n_elite_sites
        )

        def fitness_function(solution):
            new_solution = clean_solution(solution)
            score = da_score(graph, new_solution, r=r)
            size = len(new_solution)/len(graph.nodes())
            return (score, size)

        problem = {
            "fit_func": fitness_function,
            "lb": [0 for i in graph.nodes()],
            "ub": [1 for i in graph.nodes()],
            "minmax": "min",
            "obj_weights": [1.0, 0.1]
        }

        term_dict = {}

        best_position, best_fitness = model.solve(
            problem,
            n_workers=8,
            termination=term_dict
        )

        da = DefensiveAlliance(graph, clean_solution(best_position), r=r)
        print(f"Solution: {da}, Fitness: {best_fitness}")

        return da
