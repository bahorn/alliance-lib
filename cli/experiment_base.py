import os
import time
import multiprocessing
from z3 import SolverFor, set_param
from pulp.apis import get_solver
from pulp.constants import LpSolutionOptimal
from networkx.algorithms.approximation import min_weighted_vertex_cover

from alliancelib.algorithms.ilp.direct import defensive_alliance_solver
from alliancelib.algorithms.ilp.vertex_cover import \
    defensive_alliance_solver as vc_solver, \
    VertexCover, \
    vertex_cover_solver

from alliancelib.algorithms.z3 import \
        defensive_alliance_solver as z3_defensive_alliance_solver

from alliancelib.algorithms.heuristics.genetic import \
        defensive_alliance_genetic

from alliancelib.algorithms.direct.solution_size import \
        defensive_alliance as da_solution_size

from alliancelib.experiments.util import TimeoutException, timelimit


def ilp_da_solver(g, time_limit=900, verbose=False, threads=1):
    min_size = 1
    max_size = None
    r = -1

    solver = get_solver(
        os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD',
        timeLimit=time_limit,
        msg=verbose,
        threads=threads
    )

    alliance = None
    status = None

    start = time.time()
    try:
        with timelimit(time_limit):
            status, alliance = defensive_alliance_solver(
                g, solver, r=r, solution_range=(min_size, max_size)
            )
    except TimeoutException:
        pass
    end = time.time()

    if status == LpSolutionOptimal:
        return (end - start, len(alliance), alliance.vertices())

    return (None, None, [])


def ilp_vc_da_solver(g, vc=None, k=None, time_limit=900, verbose=False,
                     threads=1):
    r = -1

    vc_ = vc

    if not vc_:
        vc_ = min_weighted_vertex_cover(g)

    vertex_cover = VertexCover(g, vc_)

    solver = [
        get_solver(
            os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD',
            timeLimit=time_limit,
            msg=verbose,
            threads=1
        )
        for i in range(threads)
    ]
    alliance = None

    start = time.time()
    try:
        with timelimit(time_limit):
            alliance = vc_solver(
                vertex_cover,
                solver,
                r=r,
                solution_range=(1, k),
                threads=threads
            )
    except TimeoutException:
        for child in multiprocessing.active_children():
            print('kill')
            child.terminate()
        print('killed')
        pass
    end = time.time()

    if alliance:
        return (end - start, len(alliance), alliance.vertices())

    return (None, None, [])


def z3_da_solver(g, k, time_limit=900, max_memory=1024, threads=1,
                 verbose=False):
    alliance = None
    set_param("verbose", int(verbose) * 10)
    set_param("parallel.enable", threads > 1)
    set_param("parallel.threads.max", threads)
    set_param("memory_max_size", max_memory)
    solver = SolverFor('QF_FD')
    solver.set("timeout", int(time_limit)*1000)

    start = time.time()
    try:
        with timelimit(time_limit):
            status, alliance = z3_defensive_alliance_solver(
                    solver,
                    g,
                    solution_range=(1, k)
            )
    except TimeoutException:
        pass
    end = time.time()

    if alliance:
        return (end - start, len(alliance), alliance.vertices())

    return (None, None, [])


def ilp_vc_solver(g, time_limit=900, threads=1, verbose=False):
    solver = get_solver(
        os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD',
        timeLimit=time_limit,
        msg=verbose,
        threads=threads
    )

    cover = None

    try:
        with timelimit(time_limit):
            cover = vertex_cover_solver(g, solver)
    except TimeoutException:
        pass

    return cover


class Carrier(Exception):
    def __init__(self, value):
        self.value = value


def worker(data):
    g, k, i = data
    res = da_solution_size(g, k, initial=[str(i)])
    if res:
        raise Carrier(res.vertices())
    return None


def solution_size_solver(g, initial, k, threads=1, time_limit=900):
    data = zip(
        [g for _ in range(len(initial))],
        [k for _ in range(len(initial))],
        initial
    )
    res = None


    start = time.time()
    with multiprocessing.Pool(processes=threads) as pool:
        try:
            with timelimit(time_limit):
                list(pool.imap_unordered(worker, data))
        except Carrier as c:
            res = c.value
            pool.close()
        except TimeoutException:
            pool.close()
    end = time.time()

    if res:
        return (end - start, len(res), res)

    return (None, None, [])

def ga_da_solver(g, time_limit=900, verbose=False):
    cover = defensive_alliance_genetic(g, generations=200)
    print(cover)
    return (0.0, len(cover), cover.vertices())
