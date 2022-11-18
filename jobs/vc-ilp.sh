#!/bin/bash

BASEDIR=$1

EXACT_TIMEOUT=900
VC_TIMEOUT=600
THREADS=4
REPEAT=3


find $BASEDIR/meta -type f | \
    xargs -I {} echo \
        python3 cli process process-ilp-vc {} $BASEDIR/vc \
            --threads $THREADS \
            --timelimit $EXACT_TIMEOUT \
            --repeat $REPEAT \

