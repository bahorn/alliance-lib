import signal
import click

import networkx as nx
import ga
import cost_reduction as cr

from testcase import TestCase


class Wrapper:
    """
    Wrapper class, printing the best alliance found.
    """

    def __init__(self, internal):
        self.internal = internal

    def run(self):
        self.internal.run()

    def best(self):
        res = self.internal.best()
        if res:
            print(len(res))


def experiment(wrapper):
    def handler(signum, frame):
        wrapper.best()
        exit(1)

    signal.signal(signal.SIGINT, handler)

    wrapper.run()


@click.command()
@click.argument('job')
@click.argument('population', type=int)
@click.argument('cxpb', type=float)
@click.argument('mutpb', type=float)
def ga_exp(job, population, cxpb, mutpb):
    tc = TestCase(job)

    conf = tc.data()
    g_f = conf['file']
    graph = nx.read_graphml(g_f)

    wrapper = Wrapper(
            ga.GeneticAlgorithm(
                graph,
                population=population,
                cxpb=cxpb,
                mutpb=mutpb
            )
    )
    experiment(wrapper)


@click.command()
@click.argument('job')
@click.argument('population', type=int)
@click.argument('p_add', type=float)
def cost_reduction(job, population, p_add):
    tc = TestCase(job)

    conf = tc.data()
    g_f = conf['file']
    graph = nx.read_graphml(g_f)

    wrapper = Wrapper(
            cr.CostReduction(
                graph,
                population=population,
                p_add=p_add
            )
    )
    experiment(wrapper)


@click.group()
def heuristic():
    pass


heuristic.add_command(ga_exp)
heuristic.add_command(cost_reduction)


if __name__ == "__main__":
    heuristic()
