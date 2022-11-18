#!/bin/bash
export ILP_SOLVER=GUROBI_CMD
source .gurobi_src
parallel --progress --bar --jobs 4 < $2
