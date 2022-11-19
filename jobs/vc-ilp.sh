#!/bin/bash

BASEDIR=/home/a/dataset

EXACT_TIMEOUT=900
VC_TIMEOUT=600
THREADS=4
REPEAT=3
FINAL_TIMEOUT=2800

find $BASEDIR/meta -type f | \
    xargs -I {} echo \
        timeout $FINAL_TIMEOUT python3 cli process process-ilp-vc {} $BASEDIR/vc \
            --threads $THREADS \
            --timelimit $EXACT_TIMEOUT \
            --repeat $REPEAT \

