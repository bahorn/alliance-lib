import click
from solver import solver
from experiments import experiments
from visualization import visualization


@click.group()
def cli():
    pass


cli.add_command(solver)
cli.add_command(experiments)
cli.add_command(visualization)


if __name__ == '__main__':
    cli()
