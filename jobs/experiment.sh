#!/bin/bash
export ILP_SOLVER=GUROBI_CMD
source jobs/.gurobi_src
export CMD=$1
echo "parallel --progress --bar --jobs 4 < $CMD"
