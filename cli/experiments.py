import click

from experiment_base import ilp_da_solver, ilp_vc_da_solver

from alliancelib.experiments.runner import experimental_setup
from alliancelib.experiments.generator import \
    GNPGenerator, \
    GNPBetterGenerator, \
    WaxmanGenerator, \
    WaxmanDegreeGenerator, \
    RegularGenerator, \
    PlantedVertexCoverGenerator, \
    BarabasiAlbertGenerator, \
    FixedGMDAGenerator


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--p-max', default=0.5)
@click.option('--p-min', default=0.01)
@click.option('--timelimit', type=float, default=900)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def gnp_generator_experiment(outfile,
                             n_min,
                             n_max,
                             p_min,
                             p_max,
                             timelimit,
                             samples,
                             axis,
                             jobs,
                             threads
                             ):
    generator = GNPGenerator(
        (n_min, n_max),
        (p_min, p_max),
        axis=axis,
        samples=samples
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--d-max', default=0.5)
@click.option('--d-min', default=0.01)
@click.option('--timelimit', type=float, default=900)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def regular_generator_experiment(outfile,
                                 n_min,
                                 n_max,
                                 d_min,
                                 d_max,
                                 timelimit,
                                 samples,
                                 axis,
                                 jobs,
                                 threads
                                 ):
    generator = RegularGenerator(
        (n_min, n_max),
        (d_min, d_max),
        axis=axis,
        samples=samples
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--b-max', default=0.8)
@click.option('--b-min', default=0.1)
@click.option('--a-max', default=0.2)
@click.option('--a-min', default=0.2)
@click.option('--timelimit', type=float, default=60.0)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--alpha', default=0.15)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def waxman_experiment(outfile,
                      n_min,
                      n_max,
                      b_min,
                      b_max,
                      a_min,
                      a_max,
                      timelimit,
                      samples,
                      axis,
                      alpha,
                      jobs,
                      threads
                      ):
    generator = WaxmanGenerator(
        (n_min, n_max),
        (b_min, b_max),
        (a_min, a_max),
        axis=axis,
        samples=samples
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--b-max', default=0.8)
@click.option('--b-min', default=0.1)
@click.option('--a-max', default=0.2)
@click.option('--a-min', default=0.2)
@click.option('--timelimit', type=float, default=60.0)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--alpha', default=0.15)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def waxman_degree_distribution_experiment(outfile,
                                          n_min,
                                          n_max,
                                          b_min,
                                          b_max,
                                          a_min,
                                          a_max,
                                          timelimit,
                                          samples,
                                          axis,
                                          alpha,
                                          jobs,
                                          threads
                                          ):
    generator = WaxmanDegreeGenerator(
        (n_min, n_max),
        (b_min, b_max),
        (a_min, a_max),
        axis=axis,
        samples=samples
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--timelimit', type=float, default=60.0)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--ni-min', default=5)
@click.option('--ni-max', default=10)
@click.option('--nx-min', default=5)
@click.option('--nx-max', default=10)
@click.option('--pi-min', default=0.5)
@click.option('--pi-max', default=0.5)
@click.option('--px-min', default=0.4)
@click.option('--px-max', default=0.5)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def vertex_cover_planted(outfile,
                         ni_min,
                         ni_max,
                         nx_min,
                         nx_max,
                         pi_min,
                         pi_max,
                         px_min,
                         px_max,
                         timelimit,
                         samples,
                         axis,
                         jobs,
                         threads
                         ):
    generator = PlantedVertexCoverGenerator(
        (ni_min, ni_max),
        (nx_min, nx_max),
        (pi_min, pi_max),
        (px_min, px_max),
        axis=axis,
        samples=samples
    )

    def ilp_vc_da(vc_graph):
        graph = vc_graph
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_vc_da': ilp_vc_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--timelimit', type=float, default=60.0)
@click.option('--axis', default=10)
@click.option('--k-min', default=2)
@click.option('--k-max', default=25)
@click.option('--e-min', default=0)
@click.option('--e-max', default=100)
@click.option('--jobs', default=1)
@click.option('--threads', default=4)
def gmda_planted(outfile,
                 k_min,
                 k_max,
                 e_min,
                 e_max,
                 timelimit,
                 axis,
                 jobs,
                 threads
                 ):
    generator = FixedGMDAGenerator(
        (k_min, k_max),
        (e_min, e_max),
        axis=axis
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.command()
@click.argument('outfile')
@click.option('--n-min', default=25)
@click.option('--n-max', default=100)
@click.option('--m-max', default=2)
@click.option('--m-min', default=15)
@click.option('--timelimit', type=float, default=900)
@click.option('--samples', default=3)
@click.option('--axis', default=10)
@click.option('--jobs', default=8)
@click.option('--threads', default=1)
def ba_generator_experiment(outfile,
                            n_min,
                            n_max,
                            m_min,
                            m_max,
                            timelimit,
                            samples,
                            axis,
                            jobs,
                            threads
                            ):
    generator = BarabasiAlbertGenerator(
        (n_min, n_max),
        (m_min, m_max),
        axis=axis,
        samples=samples
    )

    def ilp_da(graph):
        res = ilp_da_solver(graph, time_limit=timelimit, threads=threads)
        return {'time': res[0], 'size': res[1]}

    algorithms = {'ilp_da': ilp_da}

    results = experimental_setup(generator, algorithms, jobs=jobs)
    results.to_csv(outfile)


@click.group()
def experiments():
    pass


experiments.add_command(gnp_generator_experiment)
experiments.add_command(regular_generator_experiment)
experiments.add_command(waxman_experiment)
experiments.add_command(waxman_degree_distribution_experiment)
experiments.add_command(vertex_cover_planted)
experiments.add_command(ba_generator_experiment)
experiments.add_command(gmda_planted)
