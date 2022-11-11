import networkx as nx
import click
import uuid
import json
import os

from alliancelib.experiments.generator import \
    GNPBetterGenerator, \
    RegularGenerator, \
    WaxmanGenerator, \
    PlantedVertexCoverGenerator, \
    FixedGMDAGenerator


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
    samples = 5
    seed = UniqueSeed()

    return [
      (
            'PlantedVertexCover',
            lambda: PlantedVertexCoverGenerator(
                (5, 20),
                (100, 100),
                (0.8, 0.8),
                (0.4, 0.4),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            ),
        ),
    ]

    return [
        (
            'GNP-n100-500,d2-10',
            lambda: GNPBetterGenerator(
                (100, 500),
                (2, 10),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        (
            'GNP-n100-100,d5',
            lambda: GNPBetterGenerator(
                (500, 1000),
                (5, 5),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        (
            'Regular-n25-100,d3-15',
            lambda: RegularGenerator(
                (25, 100),
                (3, 15),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            ),
        ),
        (
            'Waxman-n50-200,b0.1-0.8,a0.15',
            lambda: WaxmanGenerator(
                (100, 200),
                (0.15, 0.8),
                (0.15, 0.15),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            ),
        ),
        (
            'Waxman-n75,b0.05-0.95,a0.05-0.95',
            lambda: WaxmanGenerator(
                (75, 75),
                (0.05, 0.95),
                (0.05, 0.95),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        (
            'Waxman-n100,b0.05-0.95,a0.05-0.95',
            lambda: WaxmanGenerator(
                (100, 100),
                (0.05, 0.95),
                (0.05, 0.95),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            )
        ),
        (
            'PlantedVertexCover',
            lambda: PlantedVertexCoverGenerator(
                (5, 20),
                (100, 100),
                (0.8, 0.8),
                (0.4, 0.4),
                split='linear',
                axis=axis,
                samples=samples,
                seed=seed.next()
            ),
        ),
        (
            'FixedGMDA-n5-100,e0-25',
            lambda: FixedGMDAGenerator(
                (5, 100),
                (0, 50),
                split='linear',
                axis=10
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


@click.group()
def generator():
    pass


generator.add_command(dataset_generator)
