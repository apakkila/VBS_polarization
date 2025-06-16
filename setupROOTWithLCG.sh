#!/bin/bash
if [ ! -z $CMSSW_BASE ]; then 
  echo "Unset CMSSW runtime environment"
  eval `scram unsetenv -sh`
fi

########################################################################
### Note: Setup the following LCG stack.
########################################################################
if [[ !  ${CPLUS_INCLUDE_PATH} =~ LCG_106c/x86_64-el9-gcc13-opt ]]; then
  echo "Setup LCG_106c stack built for x86_64-el9-gcc13-opt which has gcc13 and ROOT 6.32.10"
  source /cvmfs/sft.cern.ch/lcg/views/LCG_106c/x86_64-el9-gcc13-opt/setup.sh
fi


###if [[ !  ${CPLUS_INCLUDE_PATH} =~ LCG_105c/x86_64-el9-gcc12-opt ]]; then
###  echo "Setup LCG_105c stack built for x86_64-el9-gcc12-opt which has gcc12 and ROOT 6.30.08"
###  source /cvmfs/sft.cern.ch/lcg/views/LCG_105c/x86_64-el9-gcc12-opt/setup.sh
###fi
