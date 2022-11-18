import networkx as nx
import click
import uuid
import json
import os

from alliancelib.experiments.generator import \
    GNPGenerator, \
    GNPBetterGenerator, \
    RegularGenerator, \
    WaxmanGenerator, \
    PlantedVertexCoverGenerator, \
    FixedGMDAGenerator, \
    BarabasiAlbertGenerator


class UniqueSeed():
    """
    A seed that increases on each call of next()
    """

    def __init__(self, s=0):
        self.s = s

    def next(self):
        self.s += 1
        return self.s


def write_graph_with_meta(outdir, exp, idx, name, g):
    meta, graph = g
    f_uuid = str(uuid.uuid4())
    if not graph:
        print('skipped', exp, idx, name)
        return
    g_filename = f'{outdir}/graphs/{f_uuid}.graphml'
    m_filename = f'{outdir}/meta/{f_uuid}.json'
    nx.write_graphml(graph, g_filename)
    metainfo = {
        'uuid': f_uuid,
        'file': g_filename,
        'idx': idx,
        'experiment': exp,
        'generator': name,
        'meta': meta
    }
    fm = open(m_filename, 'w')
    json.dump(metainfo, fm)
    fm.close()


def experiments():
    """
    Experimental Settings.
    """
    axis = 10
    samples = 3
    seed = UniqueSeed()

    return [
        ( # 300 graphs
            'WaxmanGenerator',
            lambda: WaxmanGenerator(
                (150, 150),
                (0.2, 0.8),
                (0.15, 0.3),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            ),
        ),
        ( # 300 graphs
            'BarabasiAlbert',
            lambda: BarabasiAlbertGenerator(
                (50, 200),
                (2, 25),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        ( # 300 graphs
            'GNP',
            lambda: GNPGenerator(
                (100, 150),
                (0.05, 0.15),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        ( # 75 graphs
            'Regular',
            lambda: RegularGenerator(
                (50, 150),
                (3, 15),
                split='linear',
                axis=5,
                samples=3
            )
        ),
        ( # 75 graphs
            'Fixed VC',
            lambda: PlantedVertexCoverGenerator(
                (3, 30),
                (50, 50),
                (0.8, 0.8),
                (0.5, 0.85),
                split='linear',
                axis=5,
                samples=3
            )
        ),
        ( # 100 graphs
            'FixedGMDA',
            lambda: FixedGMDAGenerator(
                (3, 100),
                (0, 500),
                split='linear',
                axis=10
            )
        )
    ]


def selftest_experiments():
    """
    Experimental Settings.
    """
    axis = 3
    samples = 3
    seed = UniqueSeed()

    return [
        (
            'GNP-n50-75,d2-10',
            lambda: GNPBetterGenerator(
                (50, 75),
                (2, 10),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        )
    ]


@click.command()
@click.argument('outdir')
def dataset_generator(outdir):
    os.makedirs(f'{outdir}/graphs', exist_ok=True)
    os.makedirs(f'{outdir}/meta', exist_ok=True)

    for idx, (name, experiment) in enumerate(experiments()):
        generator = experiment()
        for i in range(generator.count()):
            write_graph_with_meta(
                outdir,
                name,
                idx,
                generator.name(),
                generator.at(i)
            )


@click.command()
@click.argument('outdir')
def selftest_generator(outdir):
    os.makedirs(f'{outdir}/graphs', exist_ok=True)
    os.makedirs(f'{outdir}/meta', exist_ok=True)

    exp = selftest_experiments()

    for idx, (name, experiment) in enumerate(exp):
        generator = experiment()
        for i in range(generator.count()):
            write_graph_with_meta(
                outdir,
                name,
                idx,
                generator.name(),
                generator.at(i)
            )


@click.group()
def generator():
    pass


generator.add_command(dataset_generator)
generator.add_command(selftest_generator)
