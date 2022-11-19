#!/bin/bash

BASEDIR=/home/a/dataset

EXACT_TIMEOUT=900
VC_TIMEOUT=600
THREADS=4
REPEAT=3

find $BASEDIR/meta -type f | \
    xargs -I {} echo \
        python3 cli process process-solution-size {} $BASEDIR/ss \
            --threads $THREADS \
            --timelimit $EXACT_TIMEOUT \
            --repeat $REPEAT
