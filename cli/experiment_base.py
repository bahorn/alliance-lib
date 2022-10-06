import os
import time
import itertools
import logging
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
import joblib
from pulp.apis import get_solver
from pulp.constants import LpSolutionOptimal
from alliancelib.algorithms.ilp.direct import defensive_alliance_solver

from util import gen_seed, tqdm_joblib


def solve(g, time_limit=900, verbose=False):
    min_size = 1
    max_size = None
    r = -1

    solver = get_solver(
        os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD',
        timeLimit=time_limit,
        msg=verbose
    )

    start = time.time()

    status, alliance = defensive_alliance_solver(
        g, solver, r=r, solution_range=(min_size, max_size)
    )

    end = time.time()

    if status == LpSolutionOptimal:
        return end - start
    else:
        return None


def point(arguments, generator, timelimit, attempts_per_connected=5):
    # do the construction
    for i in range(attempts_per_connected):
        try:
            g = generator(
                    arguments[0],
                    arguments[1],
                    gen_seed(arguments[0], arguments[1], i)
            )
        except Exception as e:
            logging.error(
                f'Exception "{e}" x={arguments[0]} y={arguments[1]}'
            )
            return None
        if nx.is_connected(g):
            return solve(g, timelimit)

    return None


def step(arguments, generator, timelimit):
    p = point(arguments, generator, timelimit)
    return {'x': arguments[0], 'y': arguments[1], 'value': p}


def experiment(name,
               x,
               y,
               generator,
               timelimit=60,
               points_per_axis=10,
               samples_per_point=3
               ):
    x_range = list(
        map(x[0], np.linspace(x[1][0], x[1][1], num=points_per_axis))
    )
    y_range = list(
        map(y[0], np.linspace(y[1][0], y[1][1], num=points_per_axis))
    )

    values = [
        (x, y, s)
        for x, y, s in itertools.product(
            x_range,
            y_range,
            range(samples_per_point)
        )
    ]

    with tqdm_joblib(tqdm(desc=name, total=len(values))) as _:
        data = joblib.Parallel(n_jobs=12)(
            joblib.delayed(step)(value, generator, timelimit)
            for value in values
        )

    df = pd.DataFrame(data)
    return df


def gnp_generator(a, b, seed):
    return nx.gnp_random_graph(a, b, seed=seed)


def main():
    samples_per_point = 3
    points_per_axis = 10

    timelimit = 60
    x = (int, (20, 100))
    y = (float, (0.01, 0.5))
    generator = gnp_generator

    df = experiment(
        x,
        y,
        generator,
        timelimit=timelimit,
        samples_per_point=samples_per_point,
        points_per_axis=points_per_axis
    )

    df.to_csv("out.csv")
    print(df)


if __name__ == "__main__":
    main()
