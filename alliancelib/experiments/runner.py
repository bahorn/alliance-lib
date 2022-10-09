import pandas as pd
from tqdm import tqdm
import joblib

from util import tqdm_joblib


def algorithm_wrapper(name, algorithm, properties, graph):
    res = algorithm(graph)
    res['algorithm'] = name
    res.update(properties)
    return res


def step(name, algorithm, generator, idx):
    properties, graph = generator.at(idx)

    if not graph:
        return joblib.delayed(lambda: None)()

    res = joblib.delayed(algorithm_wrapper)(
        name, algorithm, properties, graph
    )

    return res


def experimental_setup(generator, algorithms, jobs=8):
    """
    Run an experiment with a graph generator and a set of algorithms.
    """
    graph_count = generator.count()
    results = []
    # Setup the queue for each algorithms
    for name, algorithm in algorithms.items():
        data = []
        with tqdm_joblib(tqdm(desc=name, total=graph_count)) as _:
            data = joblib.Parallel(n_jobs=jobs)(
                step(
                    name, algorithm, generator, idx
                )
                for idx in range(graph_count)
            )
        results += list(filter(lambda x: x is not None, data))

    return pd.DataFrame(results)
