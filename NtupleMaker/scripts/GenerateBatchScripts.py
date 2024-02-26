import os
import glob
import re
import collections

runJobsForSystematics = False

def main():

  acceptListUL16APV = []
  acceptListUL16PostAPV = []
  acceptListUL17 = []
  acceptListUL18 = []
  acceptListUL16APV += [
    "^MCUL16APV_*",
    "^DataUL16APV_*",
  ]
  acceptListUL16PostAPV += [
    "^MCUL16PostAPV_*",
    "^DataUL16PostAPV_*",
  ]
  acceptListUL17 += [
    "^MCUL17_*",
    "^DataUL17_*",
  ]
  acceptListUL18 += [
    "^MCUL18_*",
    "^DataUL18_*",
  ]

  vetoListUL16APV = []
  vetoListUL16PostAPV = []
  vetoListUL17 = []
  vetoListUL18 = []

  vetoListUL16APV += [
    # "^MCUL16APV_*",
    "^MCUL16APV_TT_Mtt*",
    "^MCUL16APV_VBS*_EWK_QCD*",
  ]
  vetoListUL16PostAPV += [
    # "^MCUL16PostAPV_*",
    "^MCUL16PostAPV_TT_Mtt*",
    "^MCUL16PostAPV_VBS*_EWK_QCD*",
  ]
  vetoListUL17 += [
    # "^MCUL17_*",
    "^MCUL17_TT_Mtt*",
    "^MCUL17_VBS_.*_EWK_QCD$",
    "^MCUL17_VBS_.*2B.*$",
    "^MCUL17_VBS_.*noB.*$",
    "^MCUL17_VBS_aQGC*",
  ]
  vetoListUL18 += [
    # "^MCUL18_*",
    "^MCUL18_TT_Mtt*",
    "^MCUL18_VBS*_EWK_QCD*",
  ]

  pickyList =  []
  # pickyList += [
  #   "MCUL17_QCD_HT2000toInf",
  #   "MCUL17_TT_2L",
  #   "MCUL17_WZZ",
  # ]
  #######################################################################################
  # Samples directory
  fileDirUL16APV = GetINDIR("UL16APV")
  fileDirUL16PostAPV    = GetINDIR("UL16PostAPV")
  fileDirUL17    = GetINDIR("UL17")
  fileDirUL18    = GetINDIR("UL18")

  #######################################################################################
  # Get samples to run for each year
  samplesUL16APV = GetSampleNames(fileDirUL16APV, vetoListUL16APV, acceptListUL16APV)
  samplesUL16PostAPV    = GetSampleNames(fileDirUL16PostAPV, vetoListUL16PostAPV, acceptListUL16PostAPV)
  samplesUL17    = GetSampleNames(fileDirUL17, vetoListUL17, acceptListUL17)
  samplesUL18    = GetSampleNames(fileDirUL18, vetoListUL18, acceptListUL18)
  # Collect all sample names into one final list
  samplesAll = []
  samplesAll += samplesUL16APV
  samplesAll += samplesUL16PostAPV
  samplesAll += samplesUL17
  samplesAll += samplesUL18
  #######################################################################################
  # Picky list
  if len(pickyList) > 0:
    samplesAll = []
    samplesAll = pickyList
  #######################################################################################
  #
  # Make Bash Script
  #
  fNameBash = CreateBashScript()
  #
  # Make Condor Scripts
  #
  fNameSub  = CreateCondorSubScript(fNameBash,samplesAll)

  #######################################################################################
  ####
  #### Send to batch
  #### 
  #### sendSubScript_command = 'condor_submit %s' % fNameSub
  #### os.system(sendSubScript_command)

def SortSamplesByQueue(samplesAll):
  espressoNCores2 = [
    "WWW","WWZ","WZZ","ZZZ",
    "_WW","_WZ","_ZZ","VBS"
  ]
  espresso = [
    "JetHT","QCD_HT",
    "WJetsToQQ_HT","ZJetsToQQ_HT",
    "EWKWp","EWKWm","EWKZ",
    "TT_2L","ST_schan", "ST_tchan", "ST_tW",
  ]
  microcentury =[
    "TT_0L","TT_1L",
  ]
  longlunch = []
  workday = []
  if runJobsForSystematics:
    espresso = []
    microcentury =[]
    longlunch = []
    workday = []

  samplesByQueue = collections.OrderedDict()
  samplesByQueue["workday"]      = []
  samplesByQueue["longlunch"]    = []
  samplesByQueue["microcentury"] = []
  samplesByQueue["espresso"]     = []
  samplesByQueue["espressoNCores2"]  = []

  for sample in samplesAll:
    # Check if sample should be placed in workday 
    if any(substring in sample for substring in espressoNCores2):
      samplesByQueue["espressoNCores2"].append(sample)
    elif any(substring in sample for substring in espresso):
      samplesByQueue["espresso"].append(sample)
    # Check if sample should be placed in longlunch 
    elif any(substring in sample for substring in microcentury):
      samplesByQueue["microcentury"].append(sample)
    # Check if sample should be placed in microcentury 
    elif any(substring in sample for substring in longlunch):
      samplesByQueue["longlunch"].append(sample)
    # Check if sample should be placed in espresso 
    elif any(substring in sample for substring in workday):
      samplesByQueue["workday"].append(sample)
    # If not sorted in any queue above, chuck it in microcentury
    else:
      if runJobsForSystematics:
        samplesByQueue["longlunch"].append(sample)
      else:
        samplesByQueue["microcentury"].append(sample)


  return samplesByQueue

def GetSampleNames(fileDir, vetoList=[], acceptList=[]):
  # Get All samples name
  samplesAll =  [
    f.split("/")[-1].replace("NanoSkimMerged_", "").replace(".root", "") for f in glob.glob(fileDir+"*.root")
  ]
  # Sort it alphabetically
  samplesAll.sort()
  #
  samples = []
  #
  # Accept samples if any of the strings in acceptList are substrings to the sample's name
  #
  if len(acceptList) > 0:
    combined = "(" + ")|(".join(acceptList) + ")"
    samples += [s for s in samplesAll if re.search(combined, s)]
  #
  # Remove samples if any of the strings in vetoList are substrings to the sample's name
  #
  if len(vetoList) > 0:
    combined = "(" + ")|(".join(vetoList) + ")"
    print(combined)
    samplesToIgnore = [s for s in samplesAll if re.search(combined, s)]
    samples = [s for s in samples if s not in samplesToIgnore]
  # print(samples)
  #
  # TODO: Check for duplicates
  #
  return samples

def GetINDIR(sample):
  BASEDIR="/eos/cms/store/group/phys_b2g/nbinnorj/VBS_TwoFatJetNanoSkim_v0p1/MERGED"
  if "UL16APV" in sample:
    return f"{BASEDIR}/UL16APV/"
  elif "UL16PostAPV" in sample:
    return f"{BASEDIR}/UL16PostAPV/"
  elif "UL17" in sample:
    return f"{BASEDIR}/UL17/"
  elif "UL18" in sample:
    return f"{BASEDIR}/UL18/"

def CreateBashScript():

  fName = "TEMP_BatchRun_VBSNtupleMaker.sh"

  f = open(fName, 'w')
  f.write('#!/bin/bash\n\n')
  f.write('cd %s \n' %(os.getcwd()))
  f.write('source ../setupROOTWithLCG.sh\n')
  f.write('SAMPLENAME=${1}\n')
  f.write('CORES=${2}\n')
  f.write('INDIR=${3}\n')
  f.write('\n')
  f.write('echo \"SAMPLENAME        = \"$SAMPLENAME  \n')
  f.write('echo \"CORES             = \"$CORES \n')
  f.write('echo \"INDIR             = \"$INDIR \n')
  f.write('echo \"Running NtupleMaker.py\" \n')
  f.write('\n')
  # Write the command
  command  = "python3 -u NtupleMaker.py "
  command += "-b "
  command += "-s ${SAMPLENAME} "
  command += "-c ${CORES} "
  command += "-d ${INDIR} \n"
  f.write(command)
  f.write('\n')
  f.close()
  # Change batch script permission
  preliminary_command = 'chmod +x %s' % fName
  os.system(preliminary_command)
  return fName

def CreateCondorSubScript(fNameBash,samplesAll):

  samplesByQueue = SortSamplesByQueue(samplesAll)

  fName = "%s.sub" %(fNameBash)

  f = open(fName, 'w')
  f.write('executable    = %s \n' %(fNameBash))
  f.write('universe      = vanilla\n')
  f.write('output        = BatchLog/Ntuple.$(SAMPLE).$(ClusterId).$(ProcId).out\n')
  f.write('error         = BatchLog/Ntuple.$(SAMPLE).$(ClusterId).$(ProcId).err\n')
  f.write('log           = BatchLog/Ntuple.$(ClusterId).log\n')
  f.write('stream_output = True\n')
  f.write('stream_error  = True\n')
  f.write('\n')
  f.write('arguments = $(SAMPLE) $(NCORES) $(INDIR)\n')
  f.write('\n')
  for queue in samplesByQueue:
    if len(samplesByQueue[queue]) == 0: continue
    NCORES="2"
    if queue == "espressoNCores2":
      NCORES="2"
      f.write('+JobFlavour = \"espresso\"\n')
    else:
      NCORES="4"
      f.write('+JobFlavour = \"%s\"\n' %(queue))
    f.write('NCORES = {} \n'.format(NCORES))
    f.write('request_cpus = $(NCORES) \n')
    f.write('queue SAMPLE INDIR from ( \n')
    for sample in samplesByQueue[queue]:
      f.write('{0:50}{1:50}\n'.format(sample, GetINDIR(sample)))
    f.write(') \n')
    f.write('\n')
  f.close()
  return fName

if __name__ == "__main__":
  main()