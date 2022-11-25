#!/bin/bash
JOB=$1
JOBNAME=`basename $1`
TIMEOUT=300
KILL_TIME=330
OUTDIR=~/out/cr/
echo "timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py cost-reduction $JOB 711 0.44 0.67 > $OUTDIR/$JOBNAME.1.txt"
echo "timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py cost-reduction $JOB 711 0.44 0.67 > $OUTDIR/$JOBNAME.2.txt"
echo "timeout -k $KILL_TIME -s SIGINT $TIMEOUT python3 heuristic/wrapper.py cost-reduction $JOB 711 0.44 0.67 > $OUTDIR/$JOBNAME.3.txt"
