"""
Implementation of a Mealpy solver using ABC for Defensive Alliance
"""
from alliancelib.ds.alliances.da import DefensiveAlliance
from alliancelib.ds.vertex_set import ConstraintException
from mealpy.swarm_based.ABC import OriginalABC
from mealpy.swarm_based.BA import OriginalBA
from mealpy.physics_based.SA import OriginalSA
from mealpy.utils.problem import Problem
from .cost_functions import da_score


def clean_solution(solution):
    res = []
    for i in range(len(solution)):
        if solution[i] >= 0.5:
            res.append(i)
    return res


def abc_model(pop_size=50, n_elites=16, n_others=4,
              patch_size=5.0, patch_reduction=0.985, n_sites=3,
              n_elite_sites=1):
    def model(generations):
        return OriginalABC(
            generations,
            pop_size,
            n_elites,
            n_others,
            patch_size,
            patch_reduction,
            n_sites,
            n_elite_sites
        )
    return model


def ba_model(pop_size=50, loudness=0.8, pulse_rate=0.95, pf_min=0, pf_max=10):
    def model(generations):
        return OriginalBA(
            generations,
            pop_size,
            loudness,
            pulse_rate,
            pf_min,
            pf_max
        )
    return model


def sa_model(pop_size=50, max_sub_iter=5, t0=1000, t1=1, move_count=5,
             mutation_rate=0.1, mutation_step_size=0.1,
             mutation_step_size_damp=0.99):
    def model(generations):
        return OriginalSA(
            generations,
            pop_size,
            max_sub_iter,
            t0,
            t1,
            move_count,
            mutation_rate,
            mutation_step_size,
            mutation_step_size_damp
        )
    return model


class DefensiveAllianceProblem(Problem):
    """
    MealPy formulation of DefensiveAlliance
    """

    def __init__(self, graph, r=-1, name="DefensiveAlliance", **kwargs):
        self.g = graph
        self.r = r
        self.vertex_count = len(self.g.nodes())
        lb = [0 for i in range(self.vertex_count)]
        ub = [1 for i in range(self.vertex_count)]
        super().__init__(lb, ub, 'min', **kwargs)
        self.name = name

    def fit_func(self, solution):
        new_solution = clean_solution(solution)
        score = da_score(self.g, new_solution, r=self.r)
        size = len(new_solution)/self.vertex_count
        return (score, size)


class DAMetaHeuristic:
    """
    Wrapper mealpy for solving Defensive Alliance
    """

    def __init__(self, model):
        self.model = model

    def run(self, graph, generations=1000, r=-1, threads=8, time_limit=60):
        model = self.model(generations)

        problem = DefensiveAllianceProblem(graph, obj_weights=[1.0, 0.1])

        term_dict = {
            "mode": "TB",
            "quantity": time_limit
        }

        best_position, best_fitness = model.solve(
            problem,
            n_workers=threads,
            termination=term_dict
        )

        try:
            da = DefensiveAlliance(graph, clean_solution(best_position), r=r)
            print(f"Solution: {da}, Fitness: {best_fitness}")
        except ConstraintException:
            return None
