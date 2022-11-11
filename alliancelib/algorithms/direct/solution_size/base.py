# pylint: disable=C0103,R0913
"""
Searches for alliances up to a certain solution size.

This is in FPT for many cases, include Defensive Alliance.
This is because you can ignore vertices that would add too many neighbours,
caping the total number of vertices to consider.
"""
import multiprocessing as mp
from typing import Optional, List
from alliancelib.ds import \
    Graph, \
    NodeSet, \
    VertexSet
from .common import VertexPredicate, SolutionPredicate


def traverse(graph: Graph,
             initial_set: NodeSet,
             possible_vertices: NodeSet,
             vertex_predicate: VertexPredicate,
             solution_predicate: SolutionPredicate,
             depth: int
             ) -> Optional[VertexSet]:
    """
    Recursive function, as thats the cleanest way of writing this, and you'll
    never actually hit the python stack limit of ~1000.
    """
    if solution_predicate(graph, initial_set):
        return VertexSet(graph, initial_set)

    if depth <= 0:
        return None

    # compute the potential set of neighbours.
    neighbours: NodeSet = set()
    for vertex in initial_set:
        neighbours = neighbours.union(set(graph.neighbors(vertex)))
    neighbours -= initial_set

    if len(initial_set) == 0:
        neighbours = possible_vertices
    else:
        pass

    neighbours_ = filter(
        lambda v: vertex_predicate(graph, v, depth),
        neighbours
    )

    for vertex in neighbours_:
        vs = {vertex}
        res = traverse(
            graph,
            initial_set.union(vs),
            possible_vertices - vs,
            vertex_predicate,
            solution_predicate,
            depth - 1
        )
        if res:
            return res

    return None


def alliance_solution_size(graph: Graph,
                           vertex_predicate: VertexPredicate,
                           solution_predicate: SolutionPredicate,
                           k: int
                           ) -> Optional[VertexSet]:
    """
    Finds a connected alliance, up to a certain size.
    """
    # first, find the vertices that satify the predicate.
    possible_vertices = set(
        filter(lambda v: vertex_predicate(graph, v, k), graph.nodes())
    )

    return traverse(
        graph,
        set(),
        possible_vertices,
        vertex_predicate,
        solution_predicate,
        k
    )


def new_sets(graph: Graph, base: List, k: int,
             vertex_predicate: VertexPredicate):
    """
    Compute a list of adjacent sets for a given list.
    """
    neighbours: NodeSet = set()
    for vertex in base:
        neighbours = neighbours.union(set(graph.neighbors(vertex)))
    neighbours -= set(base)

    depth = k-len(base)

    neighbours_ = filter(
        lambda v: vertex_predicate(graph, v, depth),
        neighbours
    )

    res = []
    for neighbour in neighbours_:
        res.append(base + [neighbour])

    return res


def alliance_solution_size_parallel(graph: Graph,
                                    initial: List,
                                    vertex_predicate: VertexPredicate,
                                    solution_predicate: SolutionPredicate,
                                    k: int,
                                    threads: int = 1
                                    ) -> Optional[VertexSet]:
    work_queue = mp.JoinableQueue()

    manager = mp.Manager()
    state = manager.dict()
    state['found'] = False
    state['size'] = len(graph.nodes())
    state['solution'] = graph.nodes()

    # using shared memory for this, so make it faster.
    found_state = mp.Value('b', False)

    def worker(q, fs, idx, return_dict):
        while True:
            item = q.get()

            # just clear the queue if we are done
            if fs.value:
                q.task_done()
                continue

            if solution_predicate(graph, item):
                fs.value = True
                return_dict['found'] = True
                return_dict['solution'] = item
                return_dict['size'] = len(item)

            if len(item) < k:
                neighbours = new_sets(graph, item, k, vertex_predicate)
                for neighbour in neighbours:
                    q.put(neighbour)

            q.task_done()

    processes = []
    for i in range(threads):
        p = mp.Process(target=worker, daemon=True, args=(
            work_queue, found_state, i, state
        ))
        processes.append(p)
        p.start()

    for item in initial:
        work_queue.put([item])

    work_queue.join()

    if state['found']:
        return VertexSet(graph, state['solution'])

    return None


__all__ = [
    'alliance_solution_size',
    'alliance_solution_size_parallel'
]
