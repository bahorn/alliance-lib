import os
import json
import click
import networkx as nx
import pandas as pd

from experiment_base import \
    ilp_da_solver, \
    ilp_vc_da_solver, \
    z3_da_solver, \
    ilp_vc_solver


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

    f = open(infile)
    conf = json.load(f)
    f_uuid = conf['uuid']
    g_f = conf['file']
    g = nx.read_graphml(g_f)
    res = []
    for i in range(repeat):
        res1 = ilp_da(g)
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
@click.option('--threads', default=4)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_ilp_vc(infile, outdir, timelimit, threads, repeat, verbose):
    def ilp_da_vc(graph, vc):
        res = ilp_vc_da_solver(
            graph,
            vc,
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

    f = open(infile)
    conf = json.load(f)
    f_uuid = conf['uuid']
    g_f = conf['file']
    vertex_cover = conf['vertex_cover']
    g = nx.read_graphml(g_f)
    res = []
    for i in range(repeat):
        res1 = ilp_da_vc(g, vc=vertex_cover)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.argument('k')
@click.option('--timelimit', type=float, default=900)
@click.option('--threads', default=4)
@click.option('--repeat', default=3)
@click.option('--verbose', is_flag=True, default=False)
def process_z3(infile, outdir, k, timelimit, threads, repeat, verbose):
    def z3_da(graph):
        res = z3_da_solver(
            graph,
            k=k,
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

    f = open(infile)
    conf = json.load(f)
    f_uuid = conf['uuid']
    g_f = conf['file']
    g = nx.read_graphml(g_f)
    res = []
    for i in range(repeat):
        res1 = z3_da(g)
        print(res1)
        res.append(res1)
        if not res1['time']:
            break

    df = pd.DataFrame(res)
    df.to_csv(f'{outdir}/{f_uuid}.csv')


@click.command()
@click.argument('infile')
def add_vertex_cover(infile):
    f = open(infile, 'r')
    conf = json.load(f)
    f.close()

    print(conf)
    g_f = conf['file']
    g = nx.read_graphml(g_f)
    res = ilp_vc_solver(g)
    conf['vertex_cover'] = list(res.vertices())

    f = open(infile, 'w')
    json.dump(conf, f)
    f.close()


@click.group()
def process():
    pass


process.add_command(process_ilp)
process.add_command(process_ilp_vc)
process.add_command(process_z3)
process.add_command(add_vertex_cover)
