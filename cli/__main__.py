import click
from solver import solver
from experiments import experiments


@click.group()
def cli():
    pass


cli.add_command(solver)
cli.add_command(experiments)


if __name__ == '__main__':
    cli()
