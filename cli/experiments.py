import networkx as nx
import click

from experiment_base import experiment


def gnp_generator(a, b, seed):
    return nx.gnp_random_graph(a, b, seed=seed)


def waxman_generator(alpha):
    def generator(a, b, seed):
        return nx.waxman_graph(a, beta=b, alpha=alpha, seed=seed)
    return generator


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--p-max', default=0.5)
@click.option('--p-min', default=0.01)
@click.option('--timelimit', default=60)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
def gnp_generator_experiment(outfile,
                             n_min,
                             n_max,
                             p_min,
                             p_max,
                             timelimit,
                             samples,
                             axis
                             ):

    x = (int, (n_min, n_max))
    y = (float, (p_min, p_max))
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

    df = df.rename(columns={'x': 'n', 'y': 'p', 'value': 'time (s)'})
    df.to_csv(outfile)

    print(df)


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--b-max', default=0.8)
@click.option('--b-min', default=0.1)
@click.option('--timelimit', default=60)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--alpha', default=0.15)
def waxman_experiment(outfile,
                      n_min,
                      n_max,
                      b_min,
                      b_max,
                      timelimit,
                      samples,
                      axis,
                      alpha
                      ):

    x = (int, (n_min, n_max))
    y = (float, (b_min, b_max))
    generator = waxman_generator(alpha)

    df = experiment(
        "waxman-experiment",
        x,
        y,
        generator,
        timelimit=timelimit,
        samples_per_point=samples,
        points_per_axis=axis
    )

    df = df.rename(columns={'x': 'n', 'y': 'beta', 'value': 'time (s)'})
    df.to_csv(outfile)
    print(df)


@click.group()
def experiments():
    pass


experiments.add_command(gnp_generator_experiment)
experiments.add_command(waxman_experiment)
