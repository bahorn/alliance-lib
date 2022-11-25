#!/bin/bash
JOB=$1
JOBNAME=`basename $1`
TIMEOUT=300
KILL_TIME=330
OUTDIR=~/out/ga/
echo timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py ga-exp $JOB 507 0.84 0.42 > $OUTDIR/$JOBNAME.1.txt
echo timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py ga-exp $JOB 507 0.84 0.42 > $OUTDIR/$JOBNAME.2.txt
echo timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py ga-exp $JOB 507 0.84 0.42 > $OUTDIR/$JOBNAME.3.txt
