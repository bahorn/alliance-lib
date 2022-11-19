import os
import sys
import signal
import json
import random
import click
import networkx as nx
import pandas as pd

from experiment_base import \
    ilp_da_solver, \
    ilp_vc_da_solver, \
    z3_da_solver, \
    ilp_vc_solver, \
    ga_da_solver, \
    solution_size_solver


class TestCase:
    def __init__(self, file):
        self.filename = file
        f = open(file, 'r')
        self._data = json.load(f)
        f.close()

    def data(self):
        return self._data

    def save(self):
        f = open(self.filename, 'w')
        json.dump(self._data, f)
        f.close()

    def add_key(self, key, value):
        self._data[key] = value


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--timelimit', type=float, default=900)
@click.option('--threads', default=4)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_ilp(infile, outdir, timelimit, threads, repeat, verbose):
    def ilp_da(graph):
        res = ilp_da_solver(
            graph,
            time_limit=timelimit,
            threads=threads,
            verbose=verbose
        )
        return {
            'time': res[0],
            'size': res[1],
            'alliance': res[2]
        }

    os.makedirs(outdir, exist_ok=True)
    alliance = []

    tc = TestCase(infile)
    conf = tc.data()
    f_uuid = conf['uuid']
    g_f = conf['file']
    g = nx.read_graphml(g_f)
    res = []
    for i in range(repeat):
        res1 = ilp_da(g)
        res.append(res1)
        if not res1['time']:
            break
        alliance = res1['alliance']

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')

    print(list(alliance))
    tc.add_key('alliance', list(alliance))
    tc.save()


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--timelimit', type=float, default=900)
@click.option('--threads', default=4)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_ilp_vc(infile, outdir, timelimit, threads, repeat, verbose):
    def ilp_da_vc(graph, vc, k):
        res = ilp_vc_da_solver(
            graph,
            vc,
            k,
            time_limit=timelimit,
            threads=threads,
            verbose=verbose
        )
        return {
            'time': res[0],
            'size': res[1],
            'alliance': res[2]
        }

    os.makedirs(outdir, exist_ok=True)

    tc = TestCase(infile)
    conf = tc.data()
    f_uuid = conf['uuid']
    g_f = conf['file']
    vertex_cover = None
    if 'vertex_cover' in conf:
        vertex_cover = conf['vertex_cover']
    else:
        return

    if not 'alliance' in conf:
        return

    size = len(conf['alliance'])
    print(size, infile)

    if size == 0:
        return

    g = nx.read_graphml(g_f)
    res = []
    for i in range(repeat):
        k = len(conf['alliance'])
        res1 = ilp_da_vc(g, vc=vertex_cover, k=k)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')
    os.kill(os.getpid(),signal.SIGKILL)


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--timelimit', type=float, default=900)
@click.option('--max-memory', default=8192)
@click.option('--threads', default=4)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_z3(infile, outdir, timelimit, threads, repeat, verbose,
               max_memory):
    def z3_da(graph, k):
        res = z3_da_solver(
            graph,
            k=k,
            max_memory=max_memory,
            time_limit=timelimit,
            threads=threads,
            verbose=verbose
        )
        return {
            'time': res[0],
            'size': res[1],
            'alliance': res[2]
        }

    os.makedirs(outdir, exist_ok=True)

    tc = TestCase(infile)
    conf = tc.data()

    f_uuid = conf['uuid']
    g_f = conf['file']

    g = nx.read_graphml(g_f)
    res = []

    if not 'alliance' in conf:
        return

    size = len(conf['alliance'])
    print(size, infile)

    if size == 0:
        return

    for i in range(repeat):
        res1 = z3_da(g, size)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--timelimit', type=float, default=900)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_ga(infile, outdir, timelimit, threads, repeat, verbose):
    def ga_da(graph):
        res = ga_da_solver(
            graph,
            time_limit=timelimit,
            verbose=verbose
        )
        return {
            'time': res[0],
            'size': res[1],
            'alliance': res[2]
        }

    os.makedirs(outdir, exist_ok=True)

    tc = TestCase(infile)
    conf = tc.data()

    f_uuid = conf['uuid']
    g_f = conf['file']

    g = nx.read_graphml(g_f)
    res = []

    for i in range(repeat):
        res1 = ga_da(g)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--threads', default=4)
@click.option('--max-size', default=30)
@click.option('--repeat', default=3)
@click.option('--timelimit', type=float, default=900)
@click.option('--seed', default=0)
def process_solution_size(infile, outdir, threads, max_size, timelimit, repeat, seed):
    def ss_da(graph, alliance, alliance_size):
        res = solution_size_solver(
            g,
            alliance,
            alliance_size,
            threads=threads,
            time_limit=timelimit
        )

        return {
            'time': res[0],
            'size': res[1],
            'alliance': res[2]
        }

    os.makedirs(outdir, exist_ok=True)

    tc = TestCase(infile)
    conf = tc.data()
    f_uuid = conf['uuid']
    g_f = conf['file']
    g = nx.read_graphml(g_f)

    if not 'alliance' in conf:
        return

    s = len(conf['alliance'])
    print(s, infile)

    if s == 0:
        return

    alliance = []
    size = max_size
    if 'alliance' in conf:
        existing = conf['alliance']
        # wasting cycles to try and find alliances if we know the optimal
        # is larger than the max-size.
        if len(existing) > max_size:
            return
        alliance = conf['alliance']
        size = len(alliance)

    if not alliance:
        return

    print(size, infile)
    random.seed(seed)
    res = []
    for i in range(repeat):
        alliance = []

        if size < max_size:
            alliance = conf['alliance']
            if (max_size - size) < len(g.nodes()):
                alliance += random.sample(g.nodes(), max_size - size)
            else:
                alliance += random.sample(g.nodes(), len(g.nodes()))

        if not alliance:
            return

        res1 = ss_da(g, alliance, size)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')


@click.command()
@click.argument('infile')
@click.option('--verbose', is_flag=True, default=False)
@click.option('--threads', default=4)
@click.option('--timelimit', default=600)
def add_vertex_cover(infile, verbose, threads, timelimit):
    print(infile)
    tc = TestCase(infile)
    g_f = tc.data()['file']
    g = nx.read_graphml(g_f)
    res = ilp_vc_solver(g, threads=threads, verbose=verbose, time_limit=timelimit)
    if res:
        tc.add_key('vertex_cover', list(res.vertices()))
        tc.save()
    else:
        print(f'{infile} - could not find optimal vc!')


@click.group()
def process():
    pass


process.add_command(process_ilp)
process.add_command(process_ilp_vc)
process.add_command(process_z3)
process.add_command(add_vertex_cover)
process.add_command(process_ga)
process.add_command(process_solution_size)
