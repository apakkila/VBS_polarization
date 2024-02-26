#!/bin/bash
if [ ! -z $CMSSW_BASE ]; then 
  echo "Unset CMSSW runtime environment"
  eval `scram unsetenv -sh`
fi

########################################################################
### Note: Setup the following LCG stack.
########################################################################
echo "Setup LCG_105a stack built for x86_64-el9-gcc12-opt which has gcc12 and ROOT 6.30.04"
source /cvmfs/sft.cern.ch/lcg/views/LCG_105a/x86_64-el9-gcc12-opt/setup.sh

