import click
from solver import solver
from experiments import experiments
from visualization import visualization
from dataset import generator
from process import process


@click.group()
def cli():
    pass


cli.add_command(solver)
cli.add_command(experiments)
cli.add_command(visualization)
cli.add_command(generator)
cli.add_command(process)

if __name__ == '__main__':
    cli()
