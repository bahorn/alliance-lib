import click
import os
import json
import time
import networkx as nx
from pulp.apis import get_solver
from pulp.constants import LpSolutionOptimal
from alliancelib.algorithms.ilp.direct import defensive_alliance_solver


@click.command()
@click.argument('filename')
@click.option('--r', default=-1)
@click.option('--min_size', default=1)
@click.option('--max_size', default=None)
@click.option('--time_limit', default=None)
@click.option('--json', 'json_output', is_flag=True, default=False)
@click.option('--verbose', is_flag=True, default=False)
def defensive_alliance_ilp(filename, r, min_size, max_size, time_limit,
                           json_output, verbose):
    g = nx.read_graphml(filename)

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

    if not json_output:
        print(alliance)
        print(status == LpSolutionOptimal, len(alliance.vertices()))
        return

    out = {
        'filename': filename,
        'r': r,
        'min_size': min_size,
        'max_size': max_size,
        'alliance': [],
        'time': end - start
    }

    if status == LpSolutionOptimal:
        out['alliance'] = alliance.__dict__()

    print(json.dumps(out))


if __name__ == '__main__':
    defensive_alliance_ilp()
