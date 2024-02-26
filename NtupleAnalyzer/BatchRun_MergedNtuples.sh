#!/bin/bash

cd ${JOBWORKDIR}
source ../../setupROOTWithLCG.sh
python3 -u MakeMergedNtuples.py --option ${1}
