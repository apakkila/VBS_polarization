#!/bin/bash

SAMPLE=${1}
NFILES=${2}

export X509_USER_PROXY=/afs/cern.ch/user/a/apakkila/myProxy

cd ${JOBWORKDIR}
source ../setupROOTWithLCG.sh
python3 -u ProcessNano.py --sample ${SAMPLE} --nfiles ${NFILES}
