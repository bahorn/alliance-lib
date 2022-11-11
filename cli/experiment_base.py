import os
import time
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


def ilp_vc_da_solver(g, vc=None, time_limit=900, verbose=False, threads=1):
    r = -1

    vc_ = vc

    if not vc_:
        vc_ = min_weighted_vertex_cover(g)

    vertex_cover = VertexCover(g, vc_)

    solver = get_solver(
        os.getenv('ILP_SOLVER') or 'PULP_CBC_CMD',
        timeLimit=time_limit,
        msg=verbose,
        threads=threads
    )
    alliance = None

    start = time.time()
    try:
        with timelimit(time_limit):
            alliance = vc_solver(
                vertex_cover, solver, r=r
            )
    except TimeoutException:
        pass
    end = time.time()

    if alliance:
        return (end - start, len(alliance), alliance.vertices())

    return (None, None, [])


def z3_da_solver(g, k, time_limit=900, threads=1, verbose=False):
    alliance = None
    set_param("verbose", int(verbose) * 2)
    set_param("parallel.enable", threads > 1)
    set_param("parallel.threads.max", threads)
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

    try:
        with timelimit(time_limit):
            cover = vertex_cover_solver(g, solver)
    except TimeoutException:
        pass

    return cover


def solution_size(g, set, threads=1):
    pass
    #alliance = None
