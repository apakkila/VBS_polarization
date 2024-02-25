# RDFAnalysis

## TODO
1. Plots
2. Distributed computing (might have to move away from RDF.FromSpec)

## How-to
0. Setup your environment
   - Lxplus:
     ```
     source /cvmfs/sft.cern.ch/lcg/views/LCG_105a/x86_64-el9-gcc13-opt/setup.sh
     ```
   - Vulcan:
     ```
     source /cvmfs/sft.cern.ch/lcg/views/LCG_105a/x86_64-ubuntu2004-gcc9-opt/setup.sh
     ```
1. Setup the file list to be used
   ```
   cd inputfiles
   find pathToMyFiles -path "*.root" > filelist.txt
   cd ..
   ```
2. Create a variables and a specifications files which contain information such as lumi, xs and how to setup the RDataFrame. This _could_ be done in one part such that the specifications file contains all the information (as it kind of already does). **NOTE** you might need to modify the first few lines of `VBSCreateSpec.py` to take into account your file list and the environment you're running in (Lxplus vs Vulcan)
   ```
   python3 src/VBSHelpers.py
   python3 src/VBSCreateSpec.py
   ```
3. Create a config file. Minimal example is provided in the `config` directory
4. Run with (DT and MC separately):
   ```
   python3 src/main.py --config myConfig.txt
   ```
   
