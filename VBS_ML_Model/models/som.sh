#!/bin/bash
# som.sh: Wrapper script for running SOM training

# Arguments
SAMPLE=$1
RUNID=$2
LR=$3
SIGMA=$4
NSAMPLES=$5

echo "Starting SOM training job..."
echo "Sample: $SAMPLE"
echo "RunID: $RUNID"
echo "Learning Rate: $LR"
echo "Sigma: $SIGMA"
echo "Number of Samples: $NSAMPLES"

# Load CMSSW / Python environment (adjust if needed)
source /cvmfs/cms.cern.ch/cmsset_default.sh
# conda or venv activation can go here if used

# Run the Python training script
python3 som_model.py \
    --sample $SAMPLE \
    --runID $RUNID \
    --learning_rate $LR \
    --sigma $SIGMA \
    --num_samples $NSAMPLES
