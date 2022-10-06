import click
import plotly.graph_objects as go
import pandas as pd


@click.command()
@click.argument('filename')
def vis_experiment(filename):
    df = pd.read_csv(filename)
    df = df.drop(columns=['Unnamed: 0'])
    columns = list(df.columns[:2])
    selection = df.groupby(columns).mean()
    df = selection.reset_index()
    x = df.values[:, 0]
    y = df.values[:, 1]
    z = df.values[:, 2]

    # Plotly 3D Surface
    fig = go.Figure(
        go.Mesh3d(x=x, y=y, z=z,  intensity=z, colorscale='Viridis')
    )

    fig.update_layout(
        title='',
        autosize=False,
        width=1000,
        height=720,
        scene=dict(
            xaxis_title=df.columns[0],
            yaxis_title=df.columns[1],
            zaxis_title=df.columns[2]
        ),
        margin=dict(l=65, r=50, b=65, t=90)
    )

    fig.show()


@click.group()
def visualization():
    pass


visualization.add_command(vis_experiment)
