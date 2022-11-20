#!/bin/bash

BASEDIR=/home/a/dataset

EXACT_TIMEOUT=900
VC_TIMEOUT=600
THREADS=4
REPEAT=3


find $BASEDIR/meta -type f | \
    xargs -I {} echo \
        python3 cli process process-z3 {} $BASEDIR/z3 \
            --threads $THREADS \
            --timelimit $EXACT_TIMEOUT \
            --max-memory 2048 \
            --repeat $REPEAT
