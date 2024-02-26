#!/usr/bin/env python3 -u
import sys
import os
import glob
import argparse
import subprocess
import ROOT

ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro("./SamplesInfo.h")

EOSUSER = "root://eosuser.cern.ch/"
TMPDIR  = os.getenv("TMPDIR")

def main():

  parser = argparse.ArgumentParser("")
  parser.add_argument('-o', '--option', type=str, default="Nominal")
  args = parser.parse_args()
  option = args.option
  #
  #
  #
  if "Nominal" in option:
    INDIR   = "/eos/user/n/nbinnorj/VBSAllHadAna/Ntuples/"
    OUTDIR  = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuples/"
    # INDIR   = "/eos/user/n/nbinnorj/VBSAllHadAna/Ntuples_VCandMassCut/"
    # OUTDIR  = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuples_VCandMassCut/"
    # INDIR   = "/eos/user/n/nbinnorj/VBSAllHadAna/Ntuples_VCandMassCut_AddGenPart/"
    # OUTDIR  = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuples_VCandMassCut_AddGenPart/"
    RunMergeNtuples(INDIR,OUTDIR)
  #
  #
  #
  # if "Syst" in option:
  #   INDIR   = "/eos/user/n/nbinnorj/VBSAllHadAna/NtuplesSyst/"
  #   OUTDIR  = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuplesSyst/"
  #   # INDIR   = "/eos/user/n/nbinnorj/VBSAllHadAna/NtuplesSyst_VCandMassCut/"
  #   # OUTDIR  = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuplesSyst_VCandMassCut/"
  #   RunMergeNtuples(INDIR,OUTDIR,True)

def RunMergeNtuples(INDIR,OUTDIR,mergeSyst=False):
  print(f"INDIR: {INDIR}")
  print(f"OUTDIR: {OUTDIR}")

  #
  # Make output directory
  #
  if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

  #
  # Get SamplesInfo map
  #
  samplesMap = ROOT.GetMapOfSamples()

  #
  # List of samples to merge
  #
  samplesToMerge = []
  if not(mergeSyst):
    samplesToMerge += [
      "DataUL17",
    ]
  samplesToMerge += [
    "MCUL17_QCD_HT",
    "MCUL17_VJetsToQQ",
    "MCUL17_TOP",
    "MCUL17_VV_LO",
    "MCUL17_VV_NLO",
    "MCUL17_VVV_NLO",
    "MCUL17_VBF",
    "MCUL17_VBS_WW_EWK",
    "MCUL17_VBS_WW_QCD",
    "MCUL17_VBS_WZ",
    "MCUL17_VBS_ZZ",
  ]


  #
  # Run over this sample
  #
  for sampleName in samplesToMerge:
    print("************************************************************")
    print(f"Merge sample: {sampleName}")
    #
    #
    #
    sampleInfo = None
    if sampleName in samplesMap:
      print (f"{sampleName} is defined in ../SamplesInfo.h")
      sampleInfo = samplesMap[sampleName]
    else:
      raise Exception(f"{sampleName} is NOT defined in ../SamplesInfo.h. Please check!!!")
    #
    #
    #
    MergeNtuples(sampleInfo, INDIR, OUTDIR, sampleName, mergeSyst)
    print("************************************************************")
    print("\n")

def MergeNtuples(sampleInfo, INDIR, OUTDIR,  sampleName="", mergeSyst=False):
  #
  #
  #
  inFileListTemp = []
  for subSample in sampleInfo.subsamples:
    if mergeSyst:
      inFileListTemp += [f for f in glob.glob(INDIR+"NtupleSyst_"+str(subSample)+".root")]
    else:
      inFileListTemp += [f for f in glob.glob(INDIR+"Ntuple_"+str(subSample)+".root")]
  #
  #
  #
  print("List of subsamples files to be merged")
  inFileList=[]
  for f in inFileListTemp:
    if not(os.path.isfile(f)):
      raise Exception(f"File not found. Please check. Given path: {f}")
    else:
      print(f"Found file: {f}")
      inFileList += [EOSUSER+f]

  print("=========================================================")
  outFileName = f"MergedNtuple_{sampleName}.root"
  if mergeSyst:
    outFileName = f"MergedNtupleSyst_{sampleName}.root"

  outFilePathTemp = f"{TMPDIR}/{outFileName}"
  print(f"Temporary merged ntuple file: {outFilePathTemp}")
  #========================================================
  #
  # hadd the mumu and elel root files into a single file
  #
  #========================================================
  print("Hadd subsamples")
  command = ["hadd", "-f", outFilePathTemp]
  command += inFileList
  subprocess.run(command)

  print("Checking size of merged file")
  command = ["du", "-cskh", outFilePathTemp]
  subprocess.run(command)
  #========================================================
  #
  # Copy the merged root file to EOS and delete in the tmp
  # directory
  #
  #========================================================
  outFilePathFinal = None
  if "/eos/user" in OUTDIR:
    outFilePathFinal = EOSUSER+OUTDIR
  else:
    outFilePathFinal = OUTDIR
  outFilePathFinal += outFileName

  print("=========================================================")
  print(f"Copying merged ntuple file to final destination: {outFilePathFinal}")
  command = ["xrdcp", "-f", outFilePathTemp, outFilePathFinal]
  subprocess.run(command)

  print("=========================================================")
  print(f"Deleting temporary ntuple file: {outFilePathTemp}")
  command = ["rm", "-fv", outFilePathTemp]
  subprocess.run(command)

if __name__== "__main__":
  main()