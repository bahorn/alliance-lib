"""
Utils for ILP problems
"""
from typing import Any

from pulp.constants import \
    LpStatus, \
    LpSolutionOptimal, \
    LpSolutionIntegerFeasible


def variable_name(name: Any) -> str:
    """
    Creating names for variables in an ILP problem
    """
    name_ = str(name).replace(' ', '')
    return f'v_{name_}'


def valid_solution(status: LpStatus) -> bool:
    """
    Test if an ILP is solved, even if not optimal
    """
    return status in [LpSolutionIntegerFeasible, LpSolutionOptimal]


__all__ = [
    'variable_name',
    'valid_solution'
]
