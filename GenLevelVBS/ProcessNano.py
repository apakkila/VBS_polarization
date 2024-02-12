#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import glob
import ROOT
ROOT.gROOT.SetBatch(True)

sys.path.append(os.path.abspath("../nanoAODTools"))
from treeReaderArrayTools import InputTree
from datamodel import Collection
from datamodel import Event
from branchselection import BranchSelection
from tools import matchObjectCollection
from GenPartDumper import GenPartDumper, getdecaychain, hasAncestor, hasMother, getFinalCopy

time_start = datetime.datetime.now()
print(f"{str(sys.argv[0])}::START::Time({str(time_start)})")

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sample", type=str, required=True)
args = parser.parse_args()
sample_name = args.sample

sampleBaseDir="/media/Duo/VBSAllHadAnalysis_NANO/store/mc/RunIISummer20UL17NanoAODv9/"
samplePathDict = {}
samplePathDict["VBS_WW_SS_EWK"] = f"{sampleBaseDir}/WplusminusTo2JWplusminusTo2JJJ_EWK_LO_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*/*.root"
samplePathDict["VBS_WW_SS_QCD"] = f"{sampleBaseDir}/WplusminusTo2JWplusminusTo2JJJ_QCD_LO_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*/*.root"
samplePathDict["VBS_WW_SS_EWKQCD"] = f"{sampleBaseDir}/WplusminusTo2JWplusminusTo2Jjj_EWK_QCD_LO_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*/*.root"

samplePathDict["VBS_WW_OS_EWK"] = f"{sampleBaseDir}/WplusTo2JWminusTo2JJJ_EWK_LO_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*/*.root"
samplePathDict["VBS_WW_OS_QCD"] = f"{sampleBaseDir}/WplusTo2JWminusTo2Jjj_EWK_QCD_LO_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*/*.root"


#
# Glob path to files
#
fileList = [f for f in glob.glob(samplePathDict[sample_name])]
# fileList = fileList[0:1]

#
#
#
treeEvents = ROOT.TChain("Events")
for f in fileList:
  print(f)
  treeEvents.Add(f)

#
#
#
inTree  = InputTree(treeEvents)
nEntries = inTree.GetEntries()
#### nEntries = 10000
print(f"nEntries={nEntries}")

#
# Enable certain branches in Events tree.
# Consider only branches that you really need for your analysis
inTree.SetBranchStatus("*",0)
inTree.SetBranchStatus("event",1)
inTree.SetBranchStatus("nGenPart",1)
inTree.SetBranchStatus("GenPart_*",1)


#================================================================
#
# Event Loop START
#
#================================================================

def createHisto(hDict,name,nbins,xmin,xmax):
  hDict[name] = ROOT.TH1D(name, name, nbins, xmin, xmax)
  return hDict

def createHisto2D(hDict,name,nbinsx,xmin,xmax,nbinsy,ymin,ymax):
  hDict[name] = ROOT.TH2D(name, name, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
  return hDict


histosDict = {}

histosDict = createHisto(histosDict, "h_genW0_pt",   100, 0., 2000.)
histosDict = createHisto(histosDict, "h_genW0_eta",  120, -6.,   6.)
histosDict = createHisto(histosDict, "h_genW0_phi",  120, -6.,   6.)
histosDict = createHisto(histosDict, "h_genW0_mass",  25,  0.,  250.)

histosDict = createHisto(histosDict, "h_genW1_pt",   100, 0., 2000.)
histosDict = createHisto(histosDict, "h_genW1_eta",  120, -6.,   6.)
histosDict = createHisto(histosDict, "h_genW1_phi",  120, -6.,   6.)
histosDict = createHisto(histosDict, "h_genW1_mass",  25,  0.,  250.)

histosDict = createHisto2D(histosDict, "h2_genW1_pt_vs_genW0_pt",  100, 0., 2000., 100, 0., 2000.)


#================================================================
#
# Event Loop START
#
#================================================================
genPartDumper = GenPartDumper()

nEventsWPt200 = 0
nEventsWPt250 = 0

for iEntry in range(0, nEntries):
  if iEntry%500 == 0:
    print(f"{iEntry} / {nEntries}")

  #------------------------------------
  # Load the event from the tree
  #------------------------------------
  event = Event(inTree, iEntry)

  #--------------------------------
  # Add more variables to GenParts
  #--------------------------------
  GenPartAll = Collection(event,'GenPart')
  genPartDumper.setupGenParts(GenPartAll)

  #------------------------
  # Dump GenParts info
  #------------------------
  # genPartDumper.analyze(GenPartAll)

  #----------------------------------------
  # Loop over gen parts and get the two
  # (last copies) of the W-bosons
  #----------------------------------------
  genWbosons = []

  for i,gp in enumerate(GenPartAll):
    if abs(gp.pdgId) == 24 and gp.statusflag('isLastCopy') and gp.statusflag('isPrompt'):
      genWbosons.append(gp)
      print(len(gp.daughters))

  #----------------------------------------------
  # Skip event if we have less than two.
  # In principle, we should always have exactly
  # two W-bosons. If we don't have exactly two,
  # we should investigate why.
  #
  #-----------------------------------------------
  if len(genWbosons) < 2: continue
  #
  # Sort W-bosons by pt
  #
  genWbosons.sort(key=lambda x: x.pt, reverse=True)

  genW0_p4 = genWbosons[0].p4()
  genW1_p4 = genWbosons[1].p4()

  histosDict["h_genW0_pt"].Fill(genW0_p4.Pt())
  histosDict["h_genW0_eta"].Fill(genW0_p4.Eta())
  histosDict["h_genW0_phi"].Fill(genW0_p4.Phi())
  histosDict["h_genW0_mass"].Fill(genW0_p4.M())
  histosDict["h_genW1_pt"].Fill(genW1_p4.Pt())
  histosDict["h_genW1_eta"].Fill(genW1_p4.Eta())
  histosDict["h_genW1_phi"].Fill(genW1_p4.Phi())
  histosDict["h_genW1_mass"].Fill(genW1_p4.M())

  histosDict["h2_genW1_pt_vs_genW0_pt"].Fill(genW0_p4.Pt(),genW1_p4.Pt())

  if genW0_p4.Pt() >=200 and genW1_p4.Pt() >=200.: nEventsWPt200+= 1
  if genW0_p4.Pt() >=250 and genW1_p4.Pt() >=250.: nEventsWPt250+= 1

#================================================================
#
# Event Loop END
#
#================================================================
print(nEventsWPt200/nEntries)
print(nEventsWPt250/nEntries)

outFile = f"./Histo_{sample_name}.root"
print(f"Saving histograms in {outFile}")
outHisto = ROOT.TFile(outFile,"RECREATE")
for hName in histosDict:
  histosDict[hName].Write()
outHisto.Close()

time_end = datetime.datetime.now()
elapsed = time_end - time_start
elapsed_str = str(datetime.timedelta(seconds=elapsed.seconds))
print(f"{str(sys.argv[0])}::DONE::Time({str(time_start)},{str(time_end)})::Elapsed({elapsed_str})")
