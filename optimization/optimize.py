"""
Script to use a genetic algorithm to optimize a set of hyperparameters.

You pass in a json file describing a target problem.

Randomly generates new values in mutation, which might not be ideal for a
speciifc problem.

Mating may also not be ideal.
"""
import logging
import json
import multiprocessing
import subprocess
import sys
import random

from deap import base
from deap import creator
from deap import tools

logging.basicConfig(level=logging.INFO)


initialization_lookup = {
    "float": random.uniform,
    "int": random.randint
}


def evaluate_solution(instance, command, order):
    """
    Return a function that can evaluate this instance.
    """
    lookup = {key: value for key, value in zip(order, instance)}
    new_command = list(map(lambda x: x.format(**lookup), command))
    output = subprocess.run(new_command, capture_output=True)
    return tuple(json.loads(output.stdout))


def mate_function():
    """
    return a function that can mate two instances.
    """
    return tools.cxTwoPoint


def mutation_function(variables):
    """
    Return a function that can mutate an instance according to the variable
    specifications.
    """
    def mutation(individual, indpb):
        for idx, value in enumerate(individual):
            if random.random() < indpb:
                individual[idx] = initialization_lookup[variables[idx][0]](
                    variables[idx][1][0], variables[idx][1][1]
                )
        return individual

    return mutation


class HyperparameterShell:
    """
    Given a problem description, search using a genetic algorithm for the
    optimal case.
    """

    def __init__(self, problem):
        self.parameters = problem['parameters']

        creator.create(
            "Objective", base.Fitness, weights=problem['objective']
        )
        creator.create("Individual", list, fitness=creator.Objective)
        toolbox = base.Toolbox()

        # Parallel Computation
        pool = multiprocessing.Pool()
        toolbox.register("map", pool.map)

        # Define the attributes
        attributes = []
        order = []
        for variable, (type, (t_min, t_max)) in problem['variables'].items():
            toolbox.register(
                f'attr_{variable}', initialization_lookup[type], t_min, t_max
            )
            attributes.append(toolbox.__dict__[f'attr_{variable}'])
            order.append(variable)

        # What a solution can look like.
        toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            tuple(attributes),
            n=1
        )

        toolbox.register(
            "population", tools.initRepeat, list, toolbox.individual
        )

        toolbox.register(
            "evaluate",
            evaluate_solution,
            command=problem['command'],
            order=order
        )
        toolbox.register("mate",  mate_function())
        toolbox.register(
            "mutate", mutation_function(list(problem['variables'].values())),
            indpb=self.parameters['indpb']
        )
        toolbox.register(
            "select", tools.selTournament,
            tournsize=self.parameters['tournsize']
        )
        self.toolbox = toolbox

    def run(self):
        """
        Perform a search.
        """
        pop = self.toolbox.population(n=self.parameters['population'])

        for i in range(self.parameters['iterations']):
            # A new generation
            logging.info(f'Generation {i}')

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(self.toolbox.map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                # cross two individuals with probability CXPB
                if random.random() < self.parameters['cxpb']:
                    self.toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                # mutate an individual with probability MUTPB
                if random.random() < self.parameters['mutpb']:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            logging.info(f'Evaluated {len(invalid_ind)} individuals')

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            fits = [ind.fitness.values[0] for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean ** 2) ** 0.5

            logging.info(
                f'Min {min(fits)} / '
                f'Max {max(fits)} / '
                f'Avg {mean} / '
                f'Std {std}'
            )

        return tools.selBest(pop, 1)[0]


def main():
    """
    Entrypoint.
    """
    with open(sys.argv[1], 'r') as f:
        problem = json.load(f)
        target = HyperparameterShell(problem)
        res = target.run()
        print(res, res.fitness)


if __name__ == "__main__":
    main()
