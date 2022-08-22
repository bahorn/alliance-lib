# AllianceLib

Library for working with problems similar to Defensive Alliance.

Written to help with experiments for my Masters Thesis.

## Overview

The library is fairly functional in design.
You pass graphs with parameters into solvers, and get an `Optional[Alliance]`
out.

Based on NetworkX.

### Data Structures

The core Alliance classes are based on a VertexSet, which represents a set of
nodes in a graph, and extended with constraints that get tested on construction.
If an Alliance is constructed that doesn't meet the constraints, an exception is
thrown.

### Algorithms

Algorithms are split into three categories:

* ILP Solvers - Often the best choice for your problems.
* Z3 based Solvers - SMT based solutions often perform well, but not as good as
  ILP.
* Direct Approaches - More direct algorithms.
* Heuristics - Experimental heuristics, not bounded.

Some variants require specific solvers to represent.

## Performance

This isn't overly focused on performance, as these algorithms being implemented
are exponential in some cases.
(As the focus of my thesis is parameterized complexity.)

## Usage

Setup a virtual environment, and use poetry to install the dependencies

### Testing

There is a `makefile` setup with some useful tests (type checking, linting,
tests):
Run `make` to set those up.

### Examples

Check `examples/` for some sample scripts.

## License

MIT
