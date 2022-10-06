import networkx as nx
import click

from experiment_base import experiment


def gnp_generator(a, b, seed):
    return nx.gnp_random_graph(a, b, seed=seed)


@click.command()
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--p-max', default=0.5)
@click.option('--p-min', default=0.01)
@click.option('--timelimit', default=60)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
def gnp_generator_experiment(n_min,
                       n_max,
                       p_min,
                       p_max,
                       timelimit,
                       samples,
                       axis
                       ):

    x = (int, (20, 100))
    y = (float, (0.01, 0.5))
    generator = gnp_generator

    df = experiment(
        "gnp-experiment",
        x,
        y,
        generator,
        timelimit=timelimit,
        samples_per_point=samples,
        points_per_axis=axis
    )

    df.to_csv("out.csv")
    print(df)


@click.group()
def experiments():
    pass

experiments.add_command(gnp_generator_experiment)
