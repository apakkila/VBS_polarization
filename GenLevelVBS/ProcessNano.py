#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import glob
import copy
import ROOT
ROOT.gROOT.SetBatch(True)

sys.path.append(os.path.abspath("../nanoAODTools"))
from treeReaderArrayTools import InputTree
from datamodel import Collection
from datamodel import Event
from branchselection import BranchSelection
from tools import matchObjectCollection
from GenPartDumper import GenPartDumper, getdecaychain, hasAncestor, hasMother, getFinalCopy, getFirstCopy

import Helpers

time_start = datetime.datetime.now()
print(f"{str(sys.argv[0])}::START::Time({str(time_start)})")

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sample", type=str, required=True)
parser.add_argument("-n", "--nfiles", type=int, default=-1)
args = parser.parse_args()
sample_name = args.sample
nfiles = args.nfiles

#
#
#
txtFilePath=f"./samples/{sample_name}.txt"

fileList = []
with open(txtFilePath) as f:
  files = f.read().splitlines()
  fileList += files

if len(fileList) == 0:
  raise Exception(f"No files in the list. Please CHECK!")
else:
  print(f"We have {len(fileList)} files")

#
#
#
fileListFinal = []
for f in fileList:
  if "/store/user/nbinnorj/" in f:
    fileListFinal.append(f"root://hip-cms-se.csc.fi/{f}")
  else:
    fileListFinal.append(f)

if nfiles > 0 and (len(fileListFinal) > nfiles):
  fileListFinal = fileListFinal[0:nfiles]
  print(f"Process only {nfiles} files")

#
#
#
treeEvents = ROOT.TChain("Events")
for f in fileListFinal:
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

# GenPartBranchName="GenPart"
GenPartBranchName="NanoGenPart"

inTree.SetBranchStatus("event",1)
inTree.SetBranchStatus(f"n{GenPartBranchName}",1)
inTree.SetBranchStatus(f"{GenPartBranchName}_*",1)

#================================================================
#
# 
#
#================================================================
isOSWW4q = False
isSSWW4q = False
isWZ4q = False
isZZ4q = False
isZWvvqq = False
isZZvvqq = False

if "WPJJWMJJjj" in sample_name: isOSWW4q = True
if "WPMJJWPMJJjj" in sample_name: isSSWW4q = True
if "ZJJWPMJJjj" in sample_name: isWZ4q = True
if "ZJJZJJjj" in sample_name: isZZ4q = True
if "ZNuNuWPMJJjj" in sample_name: isZWvvqq = True
if "ZNuNuZJJjj" in sample_name: isZZvvqq = True


#================================================================
#
# Event Loop START
#
#================================================================
histosDict = {}
if isOSWW4q or isSSWW4q:
  histosDict = Helpers.SetupHistos_WW4q(histosDict)
if isWZ4q:
  histosDict = Helpers.SetupHistos_ZW4q(histosDict)
if isZZ4q:
  histosDict = Helpers.SetupHistos_ZZ4q(histosDict)
if isZWvvqq:
  histosDict = Helpers.SetupHistos_ZWvvqq(histosDict)
if isZZvvqq:
  histosDict = Helpers.SetupHistos_ZZvvqq(histosDict)

histosDict = Helpers.SetupHistos_VBSQuarks(histosDict)

#================================================================
#
# Event Loop START
#
#================================================================
genPartDumper = GenPartDumper()

nEventsLessThanTwoVBosons = 0
nEventsVPt200 = 0
nEventsVPt250 = 0

maxEvents = -1
# maxEvents = 2500

for iEntry in range(0, nEntries):
  if iEntry%500 == 0:
    print(f"{iEntry} / {nEntries}")

    if maxEvents > -1 and iEntry > maxEvents:
      break

  #------------------------------------
  # Load the event from the tree
  #------------------------------------
  event = Event(inTree, iEntry)

  #--------------------------------
  # Add more variables to GenParts
  #--------------------------------
  GenPartAll = Collection(event,GenPartBranchName)
  genPartDumper.setupGenParts(GenPartAll)

  #------------------------
  # Dump GenParts info
  #------------------------
  # genPartDumper.analyze(event, GenPartAll)

  #----------------------------------------
  # Loop over gen parts and get the two
  # (last copies) of the W-bosons
  #----------------------------------------
  genWbosons = []
  genZbosons = []
  genQuarksVBS = []

  for i,gp in enumerate(GenPartAll):
    if abs(gp.pdgId) == 24 and gp.statusflag('isLastCopy') and gp.statusflag('isPrompt'):
      genWbosons.append(gp)
    if abs(gp.pdgId) == 23 and gp.statusflag('isLastCopy') and gp.statusflag('isPrompt'):
      genZbosons.append(gp)
      # print(len(gp.daughters))
    if (abs(gp.pdgId) >= 1  and abs(gp.pdgId) <= 5) and (gp.genPartIdxMother == 0 or gp.genPartIdxMother == 1):
      genQuarksVBS.append(gp)

  ######################################################
  #
  # WW -> 4q
  #
  ######################################################
  if isSSWW4q or isOSWW4q:
    #----------------------------------------------
    # Skip event if we have less than two.
    # In principle, we should always have exactly
    # two W-bosons. If we don't have exactly two,
    # we should investigate why.
    #
    #-----------------------------------------------
    if len(genWbosons) < 2:
      nEventsLessThanTwoVBosons += 1
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Skip.")
      continue
    if len(genWbosons) > 2:
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Take the first two leading.")
      print(f"Warning! has {len(genQuarksVBS)} quarkVBS.")

    # genPartDumper.analyze(event, GenPartAll)
    genWbosons.sort(key=lambda x: x.pt, reverse=True)

    if len(genWbosons) == 2:

      genW0 = genWbosons[0]
      genW1 = genWbosons[1]

      genW0_p4 = genW0.p4()
      genW1_p4 = genW1.p4()

      if genW0_p4.Pt() >= 200. and genW1_p4.Pt() >= 200.: nEventsVPt200 += 1
      if genW0_p4.Pt() >= 250. and genW1_p4.Pt() >= 250.: nEventsVPt250 += 1

      genW0W1_p4 = genW0_p4 + genW1_p4

      genW0_init = getFirstCopy(genW0)
      genW1_init = getFirstCopy(genW1)

      genW0_init_p4 = genW0_init.p4()
      genW1_init_p4 = genW1_init.p4()

      genWW_init_p4 = genW0_init_p4 + genW1_init_p4

      histosDict["h_genW0_init_pt"].Fill(genW0_init_p4.Pt())
      histosDict["h_genW0_init_eta"].Fill(genW0_init_p4.Eta())
      histosDict["h_genW0_init_phi"].Fill(genW0_init_p4.Phi())
      histosDict["h_genW0_init_mass"].Fill(genW0_init_p4.M())

      histosDict["h_genW1_init_pt"].Fill(genW1_init_p4.Pt())
      histosDict["h_genW1_init_eta"].Fill(genW1_init_p4.Eta())
      histosDict["h_genW1_init_phi"].Fill(genW1_init_p4.Phi())
      histosDict["h_genW1_init_mass"].Fill(genW1_init_p4.M())

      histosDict["h_genWW_init_pt"].Fill(genWW_init_p4.Pt())
      histosDict["h_genWW_init_eta"].Fill(genWW_init_p4.Eta())
      histosDict["h_genWW_init_phi"].Fill(genWW_init_p4.Phi())
      histosDict["h_genWW_init_mass"].Fill(genWW_init_p4.M())
      histosDict["h_genWW_init_mass_v2"].Fill(genWW_init_p4.M())

      histosDict["h_genW0_pt"].Fill(genW0_p4.Pt())
      histosDict["h_genW0_eta"].Fill(genW0_p4.Eta())
      histosDict["h_genW0_phi"].Fill(genW0_p4.Phi())
      histosDict["h_genW0_mass"].Fill(genW0_p4.M())

      histosDict["h_genW1_pt"].Fill(genW1_p4.Pt())
      histosDict["h_genW1_eta"].Fill(genW1_p4.Eta())
      histosDict["h_genW1_phi"].Fill(genW1_p4.Phi())
      histosDict["h_genW1_mass"].Fill(genW1_p4.M())

      histosDict["h_genWW_pt"].Fill(genW0W1_p4.Pt())
      histosDict["h_genWW_eta"].Fill(genW0W1_p4.Eta())
      histosDict["h_genWW_phi"].Fill(genW0W1_p4.Phi())
      histosDict["h_genWW_mass"].Fill(genW0W1_p4.M())
      histosDict["h_genWW_mass_v2"].Fill(genW0W1_p4.M())

      #
      # Quarks from leading W
      #
      genW0q0 = genWbosons[0].daughters[0]
      genW0q1 = genWbosons[0].daughters[1]
      if genW0q0.pt < genW0q1.pt:
        genW0q0 = genWbosons[0].daughters[1]
        genW0q1 = genWbosons[0].daughters[0]

      genW0q0_init = genW0q0
      genW0q1_init = genW0q1

      genW0q_probe = None
      genW0q_other = None

      genW0q_uptype = None
      genW0q_downtype = None

      #
      # 24 is W+
      # u-dbar
      # c-sbar
      #
      if genW0.pdgId == 24:
        #
        #
        #
        if genW0q0.pdgId > 0 and genW0q1.pdgId < 0:
          genW0q_probe = genW0q0
          genW0q_other = genW0q1
        if genW0q0.pdgId < 0 and genW0q1.pdgId > 0:
          genW0q_probe = genW0q1
          genW0q_other = genW0q0
      #
      # -24 is W-
      # ubar-d
      # cbar-s
      #
      elif genW0.pdgId == -24:
        if genW0q0.pdgId < 0 and genW0q1.pdgId > 0:
          genW0q_probe = genW0q0
          genW0q_other = genW0q1
        if genW0q0.pdgId > 0 and genW0q1.pdgId < 0:
          genW0q_probe = genW0q1
          genW0q_other = genW0q0
        # if genW0q0.pdgId > 0 and genW0q1.pdgId < 0:
        #   genW0q_probe = genW0q0
        #   genW0q_other = genW0q1
        # if genW0q0.pdgId < 0 and genW0q1.pdgId > 0:
        #   genW0q_probe = genW0q1
        #   genW0q_other = genW0q0

      #
      #
      #
      if abs(genW0q0.pdgId) in [2,4] and abs(genW0q1.pdgId) in [1,3,5]:
        genW0q_uptype = genW0q0
        genW0q_downtype = genW0q1
      elif abs(genW0q0.pdgId) in [1,3,5] and abs(genW0q1.pdgId) in [2,4]:
        genW0q_uptype = genW0q1
        genW0q_downtype = genW0q0


      #
      # Quarks from sub-leading W
      #
      genW1q0 = genWbosons[1].daughters[0]
      genW1q1 = genWbosons[1].daughters[1]
      if genW1q0.pt < genW1q1.pt:
        genW1q0 = genWbosons[1].daughters[1]
        genW1q1 = genWbosons[1].daughters[0]

      genW1q0_init = genW0q0
      genW1q1_init = genW0q1

      genW1q_probe = None
      genW1q_other = None

      genW1q_uptype = None
      genW1q_downtype = None

      #
      # 24 is W+
      # u-dbar
      # c-sbar
      #
      if genW1.pdgId == 24:
        if genW1q0.pdgId > 0 and genW1q1.pdgId < 0:
          genW1q_probe = genW1q0
          genW1q_other = genW1q1
        if genW1q0.pdgId < 0 and genW1q1.pdgId > 0:
          genW1q_probe = genW1q1
          genW1q_other = genW1q0
      #
      # -24 is W-
      # ubar-d
      # cbar-s
      #
      elif genW1.pdgId == -24:
        if genW1q0.pdgId < 0 and genW1q1.pdgId > 0:
          genW1q_probe = genW1q0
          genW1q_other = genW1q1
        if genW1q0.pdgId > 0 and genW1q1.pdgId < 0:
          genW1q_probe = genW1q1
          genW1q_other = genW1q0
        # if genW1q0.pdgId > 0 and genW1q1.pdgId < 0:
        #   genW1q_probe = genW1q0
        #   genW1q_other = genW1q1
        # if genW1q0.pdgId < 0 and genW1q1.pdgId > 0:
        #   genW1q_probe = genW1q1
        #   genW1q_other = genW1q0

      if abs(genW1q0.pdgId) in [2,4] and abs(genW1q1.pdgId) in [1,3,5]:
        genW1q_uptype = genW1q0
        genW1q_downtype = genW1q1
      elif abs(genW1q0.pdgId) in [1,3,5] and abs(genW1q1.pdgId) in [2,4]:
        genW1q_uptype = genW1q1
        genW1q_downtype = genW1q0

      histosDict["h2_genW0_pt_vs_genW1_pt"].Fill(genW0_p4.Pt(),genW1_p4.Pt())
      histosDict["h2_genW0_pt_vs_genW0W1_mass"].Fill(genW0_p4.Pt(),genW0W1_p4.M())
      histosDict["h2_genW1_pt_vs_genW0W1_mass"].Fill(genW1_p4.Pt(),genW0W1_p4.M())

      #
      #
      #
      # genW0W1_p4lab = copy.copy(genW0W1_p4)
      # genW0_p4hel = copy.copy(genW0_p4)
      # genW0_p4hel.Boost(-1. * genW0W1_p4lab.BoostVector())

      #
      #
      #
      genW0q_probe_p4 = genW0q_probe.p4(usePDGIdMass=True)
      genW0q_other_p4 = genW0q_other.p4(usePDGIdMass=True)
      genW0_qq_p4 = genW0q_probe_p4 + genW0q_other_p4
      genW0_qq_p4_boost = genW0_qq_p4.BoostVector()

      genW0q_probe_p4_boost = copy.deepcopy(genW0q_probe_p4)
      genW0q_probe_p4_boost.Boost(-genW0_qq_p4_boost)


      genW0q_downtype_p4 = genW0q_downtype.p4(usePDGIdMass=True)
      genW0q_uptype_p4   = genW0q_uptype.p4(usePDGIdMass=True)
      genW0_qq_v2_p4 = genW0q_downtype_p4 + genW0q_uptype_p4
      genW0_qq_v2_p4_boost = genW0_qq_v2_p4.BoostVector()

      genW0q_downtype_p4_boost = copy.deepcopy(genW0q_downtype_p4)
      genW0q_downtype_p4_boost.Boost(-genW0_qq_v2_p4_boost)

      #
      #
      #
      genW1q_probe_p4 = genW1q_probe.p4(usePDGIdMass=True)
      genW1q_other_p4 = genW1q_other.p4(usePDGIdMass=True)
      genW1_qq_p4 = genW1q_probe_p4 + genW1q_other_p4
      genW1_qq_p4_boost = genW1_qq_p4.BoostVector()

      genW1q_probe_p4_boost = copy.deepcopy(genW1q_probe_p4)
      genW1q_probe_p4_boost.Boost(-genW1_qq_p4_boost)

      genW1q_downtype_p4 = genW1q_downtype.p4(usePDGIdMass=True)
      genW1q_uptype_p4   = genW1q_uptype.p4(usePDGIdMass=True)
      genW1_qq_v2_p4 = genW1q_downtype_p4 + genW1q_uptype_p4
      genW1_qq_v2_p4_boost = genW1_qq_v2_p4.BoostVector()

      genW1q_downtype_p4_boost = copy.deepcopy(genW1q_downtype_p4)
      genW1q_downtype_p4_boost.Boost(-genW1_qq_v2_p4_boost)

      #
      #
      #

      genW0q_costheta = genW0q_probe_p4_boost.Vect().Unit().Dot(genW0_qq_p4.Vect().Unit())
      genW1q_costheta = genW1q_probe_p4_boost.Vect().Unit().Dot(genW1_qq_p4.Vect().Unit())

      genW0q_costheta_v2 = ROOT.TMath.Cos(genW0q_probe_p4_boost.Vect().Angle(genW0_qq_p4_boost))
      genW1q_costheta_v2 = ROOT.TMath.Cos(genW1q_probe_p4_boost.Vect().Angle(genW1_qq_p4_boost))

      genW0q_costheta_v3 = ROOT.TMath.Cos(genW0q_downtype_p4_boost.Vect().Angle(genW0_qq_v2_p4_boost))
      genW1q_costheta_v3 = ROOT.TMath.Cos(genW1q_downtype_p4_boost.Vect().Angle(genW1_qq_v2_p4_boost))

      histosDict["h_genW0_costheta"].Fill(genW0q_costheta)
      histosDict["h_genW1_costheta"].Fill(genW1q_costheta)


      histosDict["h2_genW0_pt_vs_genW0_costheta"].Fill(genW0_p4.Pt(), genW0q_costheta)
      histosDict["h2_genW1_pt_vs_genW1_costheta"].Fill(genW1_p4.Pt(), genW1q_costheta)

      histosDict["h_genW0_costheta_v2"].Fill(genW0q_costheta_v2)
      histosDict["h_genW1_costheta_v2"].Fill(genW1q_costheta_v2)

      histosDict["h_genW0_costheta_v3"].Fill(genW0q_costheta_v3)
      histosDict["h_genW1_costheta_v3"].Fill(genW1q_costheta_v3)

      #
      #
      #
      genW0q0_p4 = genW0q0.p4(usePDGIdMass=True)
      genW0q1_p4 = genW0q1.p4(usePDGIdMass=True)

      genW1q0_p4 = genW1q0.p4(usePDGIdMass=True)
      genW1q1_p4 = genW1q1.p4(usePDGIdMass=True)

      genW0_qq_p4 = genW0q0_p4 + genW0q1_p4
      genW1_qq_p4 = genW1q0_p4 + genW1q1_p4

      histosDict["h_genW0q0_pt"].Fill(genW0q0_p4.Pt())
      histosDict["h_genW0q0_eta"].Fill(genW0q0_p4.Eta())
      histosDict["h_genW0q0_phi"].Fill(genW0q0_p4.Phi())
      histosDict["h_genW0q0_mass"].Fill(genW0q0_p4.M())

      histosDict["h_genW0q1_pt"].Fill(genW0q1_p4.Pt())
      histosDict["h_genW0q1_eta"].Fill(genW0q1_p4.Eta())
      histosDict["h_genW0q1_phi"].Fill(genW0q1_p4.Phi())
      histosDict["h_genW0q1_mass"].Fill(genW0q1_p4.M())

      histosDict["h_genW1q0_pt"].Fill(genW1q0_p4.Pt())
      histosDict["h_genW1q0_eta"].Fill(genW1q0_p4.Eta())
      histosDict["h_genW1q0_phi"].Fill(genW1q0_p4.Phi())
      histosDict["h_genW1q0_mass"].Fill(genW1q0_p4.M())

      histosDict["h_genW1q1_pt"].Fill(genW1q1_p4.Pt())
      histosDict["h_genW1q1_eta"].Fill(genW1q1_p4.Eta())
      histosDict["h_genW1q1_phi"].Fill(genW1q1_p4.Phi())
      histosDict["h_genW1q1_mass"].Fill(genW1q1_p4.M())

      histosDict["h_genW0_qq_pt"].Fill(genW0_qq_p4.Pt())
      histosDict["h_genW0_qq_eta"].Fill(genW0_qq_p4.Eta())
      histosDict["h_genW0_qq_phi"].Fill(genW0_qq_p4.Phi())
      histosDict["h_genW0_qq_mass"].Fill(genW0_qq_p4.M())

      histosDict["h_genW1_qq_pt"].Fill(genW1_qq_p4.Pt())
      histosDict["h_genW1_qq_eta"].Fill(genW1_qq_p4.Eta())
      histosDict["h_genW1_qq_phi"].Fill(genW1_qq_p4.Phi())
      histosDict["h_genW1_qq_mass"].Fill(genW1_qq_p4.M())

      genWW_qqqq_p4  = genW0_qq_p4 + genW1_qq_p4

      histosDict["h_genWW_qqqq_pt"].Fill(genWW_qqqq_p4.Pt())
      histosDict["h_genWW_qqqq_eta"].Fill(genWW_qqqq_p4.Eta())
      histosDict["h_genWW_qqqq_phi"].Fill(genWW_qqqq_p4.Phi())
      histosDict["h_genWW_qqqq_mass"].Fill(genWW_qqqq_p4.M())

      histosDict["h_genW0_zg_q0"].Fill(genW0q0_p4.Pt()/genW0_qq_p4.Pt())
      histosDict["h_genW1_zg_q0"].Fill(genW1q0_p4.Pt()/genW1_qq_p4.Pt())

      histosDict["h_genW0_zg_probeq"].Fill(genW0q_probe_p4_boost.Pt()/genW0_qq_p4.Pt())
      histosDict["h_genW1_zg_probeq"].Fill(genW1q_probe_p4_boost.Pt()/genW1_qq_p4.Pt())

      genW0q0_final = getFinalCopy(genW0q0)
      genW0q1_final = getFinalCopy(genW0q1)

      genW1q0_final = getFinalCopy(genW1q0)
      genW1q1_final = getFinalCopy(genW1q1)

      genW0q0_final_p4 = genW0q0_final.p4(usePDGIdMass=True)
      genW0q1_final_p4 = genW0q1_final.p4(usePDGIdMass=True)
      genW1q0_final_p4 = genW1q0_final.p4(usePDGIdMass=True)
      genW1q1_final_p4 = genW1q1_final.p4(usePDGIdMass=True)

      genW0_final_qq_p4 = genW0q0_final_p4 + genW0q1_final_p4
      genW1_final_qq_p4 = genW1q0_final_p4 + genW1q1_final_p4

      genWW_final_qqqq_p4  = genW0_final_qq_p4 + genW1_final_qq_p4

      histosDict["h_final_genW0q0_pt"].Fill(genW0q0_final_p4.Pt())
      histosDict["h_final_genW0q0_eta"].Fill(genW0q0_final_p4.Eta())
      histosDict["h_final_genW0q0_phi"].Fill(genW0q0_final_p4.Phi())
      histosDict["h_final_genW0q0_mass"].Fill(genW0q0_final_p4.M())

      histosDict["h_final_genW0q1_pt"].Fill(genW0q1_final_p4.Pt())
      histosDict["h_final_genW0q1_eta"].Fill(genW0q1_final_p4.Eta())
      histosDict["h_final_genW0q1_phi"].Fill(genW0q1_final_p4.Phi())
      histosDict["h_final_genW0q1_mass"].Fill(genW0q1_final_p4.M())

      histosDict["h_final_genW1q0_pt"].Fill(genW1q0_final_p4.Pt())
      histosDict["h_final_genW1q0_eta"].Fill(genW1q0_final_p4.Eta())
      histosDict["h_final_genW1q0_phi"].Fill(genW1q0_final_p4.Phi())
      histosDict["h_final_genW1q0_mass"].Fill(genW1q0_final_p4.M())

      histosDict["h_final_genW1q1_pt"].Fill(genW1q1_final_p4.Pt())
      histosDict["h_final_genW1q1_eta"].Fill(genW1q1_final_p4.Eta())
      histosDict["h_final_genW1q1_phi"].Fill(genW1q1_final_p4.Phi())
      histosDict["h_final_genW1q1_mass"].Fill(genW1q1_final_p4.M())

      histosDict["h_genW0_final_qq_pt"].Fill(genW0_final_qq_p4.Pt())
      histosDict["h_genW0_final_qq_eta"].Fill(genW0_final_qq_p4.Eta())
      histosDict["h_genW0_final_qq_phi"].Fill(genW0_final_qq_p4.Phi())
      histosDict["h_genW0_final_qq_mass"].Fill(genW0_final_qq_p4.M())

      histosDict["h_genW1_final_qq_pt"].Fill(genW1_final_qq_p4.Pt())
      histosDict["h_genW1_final_qq_eta"].Fill(genW1_final_qq_p4.Eta())
      histosDict["h_genW1_final_qq_phi"].Fill(genW1_final_qq_p4.Phi())
      histosDict["h_genW1_final_qq_mass"].Fill(genW1_final_qq_p4.M())

      histosDict["h_genWW_final_qqqq_pt"].Fill(genWW_final_qqqq_p4.Pt())
      histosDict["h_genWW_final_qqqq_eta"].Fill(genWW_final_qqqq_p4.Eta())
      histosDict["h_genWW_final_qqqq_phi"].Fill(genWW_final_qqqq_p4.Phi())
      histosDict["h_genWW_final_qqqq_mass"].Fill(genWW_final_qqqq_p4.M())

      histosDict["h_genW0q0_initVsFinal_pt"].Fill((genW0q0_final_p4.Pt()-genW0q0_p4.Pt())/genW0q0_p4.Pt())
      histosDict["h_genW0q0_initVsFinal_eta"].Fill((genW0q0_final_p4.Eta()-genW0q0_p4.Eta())/genW0q0_p4.Eta())
      histosDict["h_genW0q0_initVsFinal_phi"].Fill((genW0q0_final_p4.Phi()-genW0q0_p4.Phi())/genW0q0_p4.Phi())
      histosDict["h_genW0q0_initVsFinal_mass"].Fill((genW0q0_final_p4.M()-genW0q0_p4.M())/genW0q0_p4.M())
      histosDict["h_genW0q1_initVsFinal_pt"].Fill((genW0q1_final_p4.Pt()-genW0q1_p4.Pt())/genW0q1_p4.Pt())
      histosDict["h_genW0q1_initVsFinal_eta"].Fill((genW0q1_final_p4.Eta()-genW0q1_p4.Eta())/genW0q1_p4.Eta())
      histosDict["h_genW0q1_initVsFinal_phi"].Fill((genW0q1_final_p4.Phi()-genW0q1_p4.Phi())/genW0q1_p4.Phi())
      histosDict["h_genW0q1_initVsFinal_mass"].Fill((genW0q1_final_p4.M()-genW0q1_p4.M())/genW0q1_p4.M())
      histosDict["h_genW1q0_initVsFinal_pt"].Fill((genW1q0_final_p4.Pt()-genW1q0_p4.Pt())/genW1q0_p4.Pt())
      histosDict["h_genW1q0_initVsFinal_eta"].Fill((genW1q0_final_p4.Eta()-genW1q0_p4.Eta())/genW1q0_p4.Eta())
      histosDict["h_genW1q0_initVsFinal_phi"].Fill((genW1q0_final_p4.Phi()-genW1q0_p4.Phi())/genW1q0_p4.Phi())
      histosDict["h_genW1q0_initVsFinal_mass"].Fill((genW1q0_final_p4.M()-genW1q0_p4.M())/genW1q0_p4.M())
      histosDict["h_genW1q1_initVsFinal_pt"].Fill((genW1q1_final_p4.Pt()-genW1q1_p4.Pt())/genW1q1_p4.Pt())
      histosDict["h_genW1q1_initVsFinal_eta"].Fill((genW1q1_final_p4.Eta()-genW1q1_p4.Eta())/genW1q1_p4.Eta())
      histosDict["h_genW1q1_initVsFinal_phi"].Fill((genW1q1_final_p4.Phi()-genW1q1_p4.Phi())/genW1q1_p4.Phi())
      histosDict["h_genW1q1_initVsFinal_mass"].Fill((genW1q1_final_p4.M()-genW1q1_p4.M())/genW1q1_p4.M())
    elif len(genWbosons) >= 3:
      genW2_p4 = genWbosons[2].p4()
      histosDict["h_genW2_pt"].Fill(genW2_p4.Pt())
      histosDict["h_genW2_eta"].Fill(genW2_p4.Eta())
      histosDict["h_genW2_phi"].Fill(genW2_p4.Phi())
      histosDict["h_genW2_mass"].Fill(genW2_p4.M())

  ######################################################
  #
  # WZ -> 4q
  #
  ######################################################
  if isWZ4q:
    #----------------------------------------------
    # Skip event if we have less than two.
    # In principle, we should always have exactly
    # two W-bosons. If we don't have exactly two,
    # we should investigate why.
    #
    #-----------------------------------------------
    if len(genWbosons) < 1:
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Skip.")
      continue
    if len(genZbosons) < 1:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Skip.")
      continue
    if len(genWbosons) > 1:
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Take the leading.")
    if len(genZbosons) > 1:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Take the leading.")

    # genPartDumper.analyze(event, GenPartAll)

    #
    # Sort W-bosons by pt
    #
    genWbosons.sort(key=lambda x: x.pt, reverse=True)
    genZbosons.sort(key=lambda x: x.pt, reverse=True)

    if len(genWbosons) == 1 and len(genZbosons) == 1:
      genW = genWbosons[0]
      genZ = genZbosons[0]

      genW_p4 = genW.p4()
      genZ_p4 = genZ.p4()

      if genW_p4.Pt() >= 200. and genZ_p4.Pt() >= 200.: nEventsVPt200 += 1
      if genW_p4.Pt() >= 250. and genZ_p4.Pt() >= 250.: nEventsVPt250 += 1

      genWZ_p4 = genW_p4 + genZ_p4

      genW_init = getFirstCopy(genW)
      genZ_init = getFirstCopy(genZ)

      genW_init_p4 = genW_init.p4()
      genZ_init_p4 = genZ_init.p4()

      genWZ_init_p4 = genW_init_p4+genZ_init_p4

      histosDict["h_genW_init_pt"].Fill(genW_init_p4.Pt())
      histosDict["h_genW_init_eta"].Fill(genW_init_p4.Eta())
      histosDict["h_genW_init_phi"].Fill(genW_init_p4.Phi())
      histosDict["h_genW_init_mass"].Fill(genW_init_p4.M())

      histosDict["h_genZ_init_pt"].Fill(genZ_init_p4.Pt())
      histosDict["h_genZ_init_eta"].Fill(genZ_init_p4.Eta())
      histosDict["h_genZ_init_phi"].Fill(genZ_init_p4.Phi())
      histosDict["h_genZ_init_mass"].Fill(genZ_init_p4.M())

      histosDict["h_genWZ_init_pt"].Fill(genWZ_init_p4.Pt())
      histosDict["h_genWZ_init_eta"].Fill(genWZ_init_p4.Eta())
      histosDict["h_genWZ_init_phi"].Fill(genWZ_init_p4.Phi())
      histosDict["h_genWZ_init_mass"].Fill(genWZ_init_p4.M())
      histosDict["h_genWZ_init_mass_v2"].Fill(genWZ_init_p4.M())

      histosDict["h_genW_pt"].Fill(genW_p4.Pt())
      histosDict["h_genW_eta"].Fill(genW_p4.Eta())
      histosDict["h_genW_phi"].Fill(genW_p4.Phi())
      histosDict["h_genW_mass"].Fill(genW_p4.M())

      histosDict["h_genZ_pt"].Fill(genZ_p4.Pt())
      histosDict["h_genZ_eta"].Fill(genZ_p4.Eta())
      histosDict["h_genZ_phi"].Fill(genZ_p4.Phi())
      histosDict["h_genZ_mass"].Fill(genZ_p4.M())

      histosDict["h_genWZ_pt"].Fill(genWZ_p4.Pt())
      histosDict["h_genWZ_eta"].Fill(genWZ_p4.Eta())
      histosDict["h_genWZ_phi"].Fill(genWZ_p4.Phi())
      histosDict["h_genWZ_mass"].Fill(genWZ_p4.M())
      histosDict["h_genWZ_mass_v2"].Fill(genWZ_p4.M())

      #
      # Quarks from W
      #
      genWq0 = genWbosons[0].daughters[0]
      genWq1 = genWbosons[0].daughters[1]
      if genWq0.pt < genWq1.pt:
        genWq0 = genWbosons[0].daughters[1]
        genWq1 = genWbosons[0].daughters[0]

      genWq0_init = genWq0
      genWq1_init = genWq1

      #
      # Quarks from Z
      #
      genZq0 = genZbosons[0].daughters[0]
      genZq1 = genZbosons[0].daughters[1]
      if genZq0.pt < genZq1.pt:
        genZq0 = genZbosons[0].daughters[1]
        genZq1 = genZbosons[0].daughters[0]

      genZq0_init = genZq0
      genZq1_init = genZq1

      genWq0_p4 = genWq0.p4(usePDGIdMass=True)
      genWq1_p4 = genWq1.p4(usePDGIdMass=True)

      genZq0_p4 = genZq0.p4(usePDGIdMass=True)
      genZq1_p4 = genZq1.p4(usePDGIdMass=True)

      genW_qq_p4 = genWq0_p4 + genWq1_p4
      genZ_qq_p4 = genZq0_p4 + genZq1_p4

      genWZ_qqqq_p4 = genW_qq_p4 + genZ_qq_p4

      histosDict["h_genWq0_pt"].Fill(genWq0_p4.Pt())
      histosDict["h_genWq0_eta"].Fill(genWq0_p4.Eta())
      histosDict["h_genWq0_phi"].Fill(genWq0_p4.Phi())
      histosDict["h_genWq0_mass"].Fill(genWq0_p4.M())

      histosDict["h_genWq1_pt"].Fill(genWq1_p4.Pt())
      histosDict["h_genWq1_eta"].Fill(genWq1_p4.Eta())
      histosDict["h_genWq1_phi"].Fill(genWq1_p4.Phi())
      histosDict["h_genWq1_mass"].Fill(genWq1_p4.M())

      histosDict["h_genZq0_pt"].Fill(genZq0_p4.Pt())
      histosDict["h_genZq0_eta"].Fill(genZq0_p4.Eta())
      histosDict["h_genZq0_phi"].Fill(genZq0_p4.Phi())
      histosDict["h_genZq0_mass"].Fill(genZq0_p4.M())

      histosDict["h_genZq1_pt"].Fill(genZq1_p4.Pt())
      histosDict["h_genZq1_eta"].Fill(genZq1_p4.Eta())
      histosDict["h_genZq1_phi"].Fill(genZq1_p4.Phi())
      histosDict["h_genZq1_mass"].Fill(genZq1_p4.M())

      histosDict["h_genW_qq_pt"].Fill(genW_qq_p4.Pt())
      histosDict["h_genW_qq_eta"].Fill(genW_qq_p4.Eta())
      histosDict["h_genW_qq_phi"].Fill(genW_qq_p4.Phi())
      histosDict["h_genW_qq_mass"].Fill(genW_qq_p4.M())

      histosDict["h_genZ_qq_pt"].Fill(genZ_qq_p4.Pt())
      histosDict["h_genZ_qq_eta"].Fill(genZ_qq_p4.Eta())
      histosDict["h_genZ_qq_phi"].Fill(genZ_qq_p4.Phi())
      histosDict["h_genZ_qq_mass"].Fill(genZ_qq_p4.M())

      histosDict["h_genWZ_qqqq_pt"].Fill(genWZ_qqqq_p4.Pt())
      histosDict["h_genWZ_qqqq_eta"].Fill(genWZ_qqqq_p4.Eta())
      histosDict["h_genWZ_qqqq_phi"].Fill(genWZ_qqqq_p4.Phi())
      histosDict["h_genWZ_qqqq_mass"].Fill(genWZ_qqqq_p4.M())

      genWq0_final = getFinalCopy(genWq0)
      genWq1_final = getFinalCopy(genWq1)

      genZq0_final = getFinalCopy(genZq0)
      genZq1_final = getFinalCopy(genZq1)

      genWq0_final_p4 = genWq0_final.p4(usePDGIdMass=True)
      genWq1_final_p4 = genWq1_final.p4(usePDGIdMass=True)
      genZq0_final_p4 = genZq0_final.p4(usePDGIdMass=True)
      genZq1_final_p4 = genZq1_final.p4(usePDGIdMass=True)

      genW_final_qq_p4 = genWq0_final_p4 + genWq1_final_p4
      genZ_final_qq_p4 = genZq0_final_p4 + genZq1_final_p4

      genWZ_final_qqqq_p4  = genW_final_qq_p4 + genZ_final_qq_p4

      histosDict["h_final_genWq0_pt"].Fill(genWq0_final_p4.Pt())
      histosDict["h_final_genWq0_eta"].Fill(genWq0_final_p4.Eta())
      histosDict["h_final_genWq0_phi"].Fill(genWq0_final_p4.Phi())
      histosDict["h_final_genWq0_mass"].Fill(genWq0_final_p4.M())

      histosDict["h_final_genWq1_pt"].Fill(genWq1_final_p4.Pt())
      histosDict["h_final_genWq1_eta"].Fill(genWq1_final_p4.Eta())
      histosDict["h_final_genWq1_phi"].Fill(genWq1_final_p4.Phi())
      histosDict["h_final_genWq1_mass"].Fill(genWq1_final_p4.M())

      histosDict["h_final_genZq0_pt"].Fill(genZq0_final_p4.Pt())
      histosDict["h_final_genZq0_eta"].Fill(genZq0_final_p4.Eta())
      histosDict["h_final_genZq0_phi"].Fill(genZq0_final_p4.Phi())
      histosDict["h_final_genZq0_mass"].Fill(genZq0_final_p4.M())

      histosDict["h_final_genZq1_pt"].Fill(genZq1_final_p4.Pt())
      histosDict["h_final_genZq1_eta"].Fill(genZq1_final_p4.Eta())
      histosDict["h_final_genZq1_phi"].Fill(genZq1_final_p4.Phi())
      histosDict["h_final_genZq1_mass"].Fill(genZq1_final_p4.M())

      histosDict["h_genW_final_qq_pt"].Fill(genW_final_qq_p4.Pt())
      histosDict["h_genW_final_qq_eta"].Fill(genW_final_qq_p4.Eta())
      histosDict["h_genW_final_qq_phi"].Fill(genW_final_qq_p4.Phi())
      histosDict["h_genW_final_qq_mass"].Fill(genW_final_qq_p4.M())

      histosDict["h_genZ_final_qq_pt"].Fill(genZ_final_qq_p4.Pt())
      histosDict["h_genZ_final_qq_eta"].Fill(genZ_final_qq_p4.Eta())
      histosDict["h_genZ_final_qq_phi"].Fill(genZ_final_qq_p4.Phi())
      histosDict["h_genZ_final_qq_mass"].Fill(genZ_final_qq_p4.M())

      histosDict["h_genWZ_final_qqqq_pt"].Fill(genWZ_final_qqqq_p4.Pt())
      histosDict["h_genWZ_final_qqqq_eta"].Fill(genWZ_final_qqqq_p4.Eta())
      histosDict["h_genWZ_final_qqqq_phi"].Fill(genWZ_final_qqqq_p4.Phi())
      histosDict["h_genWZ_final_qqqq_mass"].Fill(genWZ_final_qqqq_p4.M())

  ######################################################
  #
  # ZZ -> 4q
  #
  ######################################################
  if isZZ4q:
    #----------------------------------------------
    # Skip event if we have less than two.
    # In principle, we should always have exactly
    # two W-bosons. If we don't have exactly two,
    # we should investigate why.
    #
    #-----------------------------------------------
    if len(genZbosons) < 2:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Skip.")
      continue
    if len(genZbosons) > 2:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Take the leading two.")

    # genPartDumper.analyze(event, GenPartAll)

    #
    # Sort Z-bosons by pt
    #
    genZbosons.sort(key=lambda x: x.pt, reverse=True)

    if len(genZbosons) == 2:
      genZ0 = genZbosons[0]
      genZ1 = genZbosons[1]

      genZ0_p4 = genZ0.p4()
      genZ1_p4 = genZ1.p4()

      genZZ_p4 = genZ0_p4 + genZ1_p4

      if genZ0_p4.Pt() >= 200. and genZ1_p4.Pt() >= 200.: nEventsVPt200 += 1
      if genZ0_p4.Pt() >= 250. and genZ1_p4.Pt() >= 250.: nEventsVPt250 += 1

      genZ0_init = getFirstCopy(genZ0)
      genZ1_init = getFirstCopy(genZ1)

      genZ0_init_p4 = genZ0_init.p4()
      genZ1_init_p4 = genZ1_init.p4()

      genZZ_init_p4 = genZ0_init_p4 + genZ1_init_p4

      histosDict["h_genZ0_pt"].Fill(genZ0_p4.Pt())
      histosDict["h_genZ0_eta"].Fill(genZ0_p4.Eta())
      histosDict["h_genZ0_phi"].Fill(genZ0_p4.Phi())
      histosDict["h_genZ0_mass"].Fill(genZ0_p4.M())

      histosDict["h_genZ1_pt"].Fill(genZ1_p4.Pt())
      histosDict["h_genZ1_eta"].Fill(genZ1_p4.Eta())
      histosDict["h_genZ1_phi"].Fill(genZ1_p4.Phi())
      histosDict["h_genZ1_mass"].Fill(genZ1_p4.M())

      histosDict["h_genZZ_pt"].Fill(genZZ_p4.Pt())
      histosDict["h_genZZ_eta"].Fill(genZZ_p4.Eta())
      histosDict["h_genZZ_phi"].Fill(genZZ_p4.Phi())
      histosDict["h_genZZ_mass"].Fill(genZZ_p4.M())
      histosDict["h_genZZ_mass_v2"].Fill(genZZ_p4.M())

      histosDict["h_genZ0_init_pt"].Fill(genZ0_init_p4.Pt())
      histosDict["h_genZ0_init_eta"].Fill(genZ0_init_p4.Eta())
      histosDict["h_genZ0_init_phi"].Fill(genZ0_init_p4.Phi())
      histosDict["h_genZ0_init_mass"].Fill(genZ0_init_p4.M())

      histosDict["h_genZ1_init_pt"].Fill(genZ1_init_p4.Pt())
      histosDict["h_genZ1_init_eta"].Fill(genZ1_init_p4.Eta())
      histosDict["h_genZ1_init_phi"].Fill(genZ1_init_p4.Phi())
      histosDict["h_genZ1_init_mass"].Fill(genZ1_init_p4.M())

      histosDict["h_genZZ_init_pt"].Fill(genZZ_init_p4.Pt())
      histosDict["h_genZZ_init_eta"].Fill(genZZ_init_p4.Eta())
      histosDict["h_genZZ_init_phi"].Fill(genZZ_init_p4.Phi())
      histosDict["h_genZZ_init_mass"].Fill(genZZ_init_p4.M())
      histosDict["h_genZZ_init_mass_v2"].Fill(genZZ_init_p4.M())

      #
      # Quarks from Z
      #
      genZ0q0 = genZbosons[0].daughters[0]
      genZ0q1 = genZbosons[0].daughters[1]
      if genZ0q0.pt < genZ0q1.pt:
        genZ0q0 = genZbosons[0].daughters[1]
        genZ0q1 = genZbosons[0].daughters[0]

      genZ0q0_init = genZ0q0
      genZ0q1_init = genZ0q1
      #
      # Quarks from W
      #
      genZ1q0 = genZbosons[1].daughters[0]
      genZ1q1 = genZbosons[1].daughters[1]
      if genZ1q0.pt < genZ1q1.pt:
        genZ1q0 = genZbosons[1].daughters[1]
        genZ1q1 = genZbosons[1].daughters[0]

      genZ1q0_init = genZ1q0
      genZ1q1_init = genZ1q1

      genZ0q0_p4 = genZ0q0.p4(usePDGIdMass=True)
      genZ0q1_p4 = genZ0q1.p4(usePDGIdMass=True)

      genZ1q0_p4 = genZ1q0.p4(usePDGIdMass=True)
      genZ1q1_p4 = genZ1q1.p4(usePDGIdMass=True)

      genZ0_qq_p4 = genZ0q0_p4 + genZ0q1_p4
      genZ1_qq_p4 = genZ1q0_p4 + genZ1q1_p4

      genZZ_qqqq_p4 = genZ0_qq_p4 + genZ1_qq_p4

      histosDict["h_genZ0q0_pt"].Fill(genZ0q0_p4.Pt())
      histosDict["h_genZ0q0_eta"].Fill(genZ0q0_p4.Eta())
      histosDict["h_genZ0q0_phi"].Fill(genZ0q0_p4.Phi())
      histosDict["h_genZ0q0_mass"].Fill(genZ0q0_p4.M())

      histosDict["h_genZ0q1_pt"].Fill(genZ0q1_p4.Pt())
      histosDict["h_genZ0q1_eta"].Fill(genZ0q1_p4.Eta())
      histosDict["h_genZ0q1_phi"].Fill(genZ0q1_p4.Phi())
      histosDict["h_genZ0q1_mass"].Fill(genZ0q1_p4.M())

      histosDict["h_genZ1q0_pt"].Fill(genZ1q0_p4.Pt())
      histosDict["h_genZ1q0_eta"].Fill(genZ1q0_p4.Eta())
      histosDict["h_genZ1q0_phi"].Fill(genZ1q0_p4.Phi())
      histosDict["h_genZ1q0_mass"].Fill(genZ1q0_p4.M())

      histosDict["h_genZ1q1_pt"].Fill(genZ1q1_p4.Pt())
      histosDict["h_genZ1q1_eta"].Fill(genZ1q1_p4.Eta())
      histosDict["h_genZ1q1_phi"].Fill(genZ1q1_p4.Phi())
      histosDict["h_genZ1q1_mass"].Fill(genZ1q1_p4.M())

      histosDict["h_genZ0_qq_pt"].Fill(genZ0_qq_p4.Pt())
      histosDict["h_genZ0_qq_eta"].Fill(genZ0_qq_p4.Eta())
      histosDict["h_genZ0_qq_phi"].Fill(genZ0_qq_p4.Phi())
      histosDict["h_genZ0_qq_mass"].Fill(genZ0_qq_p4.M())

      histosDict["h_genZ1_qq_pt"].Fill(genZ1_qq_p4.Pt())
      histosDict["h_genZ1_qq_eta"].Fill(genZ1_qq_p4.Eta())
      histosDict["h_genZ1_qq_phi"].Fill(genZ1_qq_p4.Phi())
      histosDict["h_genZ1_qq_mass"].Fill(genZ1_qq_p4.M())

      histosDict["h_genZZ_qqqq_pt"].Fill(genZZ_qqqq_p4.Pt())
      histosDict["h_genZZ_qqqq_eta"].Fill(genZZ_qqqq_p4.Eta())
      histosDict["h_genZZ_qqqq_phi"].Fill(genZZ_qqqq_p4.Phi())
      histosDict["h_genZZ_qqqq_mass"].Fill(genZZ_qqqq_p4.M())

      genZ0q0_final = getFinalCopy(genZ0q0)
      genZ0q1_final = getFinalCopy(genZ0q1)

      genZ1q0_final = getFinalCopy(genZ1q0)
      genZ1q1_final = getFinalCopy(genZ1q1)

      genZ0q0_final_p4 = genZ0q0_final.p4(usePDGIdMass=True)
      genZ0q1_final_p4 = genZ0q1_final.p4(usePDGIdMass=True)
      genZ1q0_final_p4 = genZ1q0_final.p4(usePDGIdMass=True)
      genZ1q1_final_p4 = genZ1q1_final.p4(usePDGIdMass=True)

      genZ0_final_qq_p4 = genZ0q0_final_p4 + genZ0q1_final_p4
      genZ1_final_qq_p4 = genZ1q0_final_p4 + genZ1q1_final_p4

      genZZ_final_qqqq_p4 = genZ0_final_qq_p4 + genZ1_final_qq_p4

      histosDict["h_final_genZ0q0_pt"].Fill(genZ0q0_final_p4.Pt())
      histosDict["h_final_genZ0q0_eta"].Fill(genZ0q0_final_p4.Eta())
      histosDict["h_final_genZ0q0_phi"].Fill(genZ0q0_final_p4.Phi())
      histosDict["h_final_genZ0q0_mass"].Fill(genZ0q0_final_p4.M())

      histosDict["h_final_genZ0q1_pt"].Fill(genZ0q1_final_p4.Pt())
      histosDict["h_final_genZ0q1_eta"].Fill(genZ0q1_final_p4.Eta())
      histosDict["h_final_genZ0q1_phi"].Fill(genZ0q1_final_p4.Phi())
      histosDict["h_final_genZ0q1_mass"].Fill(genZ0q1_final_p4.M())

      histosDict["h_final_genZ1q0_pt"].Fill(genZ1q0_final_p4.Pt())
      histosDict["h_final_genZ1q0_eta"].Fill(genZ1q0_final_p4.Eta())
      histosDict["h_final_genZ1q0_phi"].Fill(genZ1q0_final_p4.Phi())
      histosDict["h_final_genZ1q0_mass"].Fill(genZ1q0_final_p4.M())

      histosDict["h_final_genZ1q1_pt"].Fill(genZ1q1_final_p4.Pt())
      histosDict["h_final_genZ1q1_eta"].Fill(genZ1q1_final_p4.Eta())
      histosDict["h_final_genZ1q1_phi"].Fill(genZ1q1_final_p4.Phi())
      histosDict["h_final_genZ1q1_mass"].Fill(genZ1q1_final_p4.M())

      histosDict["h_genZ0_final_qq_pt"].Fill(genZ0_final_qq_p4.Pt())
      histosDict["h_genZ0_final_qq_eta"].Fill(genZ0_final_qq_p4.Eta())
      histosDict["h_genZ0_final_qq_phi"].Fill(genZ0_final_qq_p4.Phi())
      histosDict["h_genZ0_final_qq_mass"].Fill(genZ0_final_qq_p4.M())

      histosDict["h_genZ1_final_qq_pt"].Fill(genZ1_final_qq_p4.Pt())
      histosDict["h_genZ1_final_qq_eta"].Fill(genZ1_final_qq_p4.Eta())
      histosDict["h_genZ1_final_qq_phi"].Fill(genZ1_final_qq_p4.Phi())
      histosDict["h_genZ1_final_qq_mass"].Fill(genZ1_final_qq_p4.M())

      histosDict["h_genZZ_final_qqqq_pt"].Fill(genZZ_final_qqqq_p4.Pt())
      histosDict["h_genZZ_final_qqqq_eta"].Fill(genZZ_final_qqqq_p4.Eta())
      histosDict["h_genZZ_final_qqqq_phi"].Fill(genZZ_final_qqqq_p4.Phi())
      histosDict["h_genZZ_final_qqqq_mass"].Fill(genZZ_final_qqqq_p4.M())

  ######################################################
  #
  # ZW -> vvqq
  #
  ######################################################
  if isZWvvqq:
    #----------------------------------------------
    #
    #
    #-----------------------------------------------
    if len(genWbosons) < 1:
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Skip.")
      continue
    if len(genZbosons) < 1:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Skip.")
      continue
    if len(genWbosons) > 1:
      print(f"Warning! Event {iEntry} has {len(genWbosons)} W-bosons. Take the leading.")
    if len(genZbosons) > 1:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Take the leading.")

    # genPartDumper.analyze(event, GenPartAll)

    #
    # Sort W-bosons by pt
    #
    genWbosons.sort(key=lambda x: x.pt, reverse=True)
    genZbosons.sort(key=lambda x: x.pt, reverse=True)

    if len(genWbosons) == 1 and len(genZbosons) == 1:

      genW = genWbosons[0]
      genZ = genZbosons[0]

      genW_p4 = genW.p4()
      genZ_p4 = genZ.p4()

      genWZ_p4 = genW_p4 + genZ_p4

      if genW_p4.Pt() >= 200. and genZ_p4.Pt() >= 200.: nEventsVPt200 += 1
      if genW_p4.Pt() >= 250. and genZ_p4.Pt() >= 250.: nEventsVPt250 += 1

      genW_init = getFirstCopy(genW)
      genZ_init = getFirstCopy(genZ)

      genW_init_p4 = genW_init.p4()
      genZ_init_p4 = genZ_init.p4()

      genWZ_init_p4 = genW_init_p4 + genZ_init_p4

      histosDict["h_genW_init_pt"].Fill(genW_init_p4.Pt())
      histosDict["h_genW_init_eta"].Fill(genW_init_p4.Eta())
      histosDict["h_genW_init_phi"].Fill(genW_init_p4.Phi())
      histosDict["h_genW_init_mass"].Fill(genW_init_p4.M())

      histosDict["h_genZ_init_pt"].Fill(genZ_init_p4.Pt())
      histosDict["h_genZ_init_eta"].Fill(genZ_init_p4.Eta())
      histosDict["h_genZ_init_phi"].Fill(genZ_init_p4.Phi())
      histosDict["h_genZ_init_mass"].Fill(genZ_init_p4.M())

      histosDict["h_genWZ_init_pt"].Fill(genWZ_init_p4.Pt())
      histosDict["h_genWZ_init_eta"].Fill(genWZ_init_p4.Eta())
      histosDict["h_genWZ_init_phi"].Fill(genWZ_init_p4.Phi())
      histosDict["h_genWZ_init_mass"].Fill(genWZ_init_p4.M())
      histosDict["h_genWZ_init_mass_v2"].Fill(genWZ_init_p4.M())

      histosDict["h_genW_pt"].Fill(genW_p4.Pt())
      histosDict["h_genW_eta"].Fill(genW_p4.Eta())
      histosDict["h_genW_phi"].Fill(genW_p4.Phi())
      histosDict["h_genW_mass"].Fill(genW_p4.M())

      histosDict["h_genZ_pt"].Fill(genZ_p4.Pt())
      histosDict["h_genZ_eta"].Fill(genZ_p4.Eta())
      histosDict["h_genZ_phi"].Fill(genZ_p4.Phi())
      histosDict["h_genZ_mass"].Fill(genZ_p4.M())

      histosDict["h_genWZ_pt"].Fill(genWZ_p4.Pt())
      histosDict["h_genWZ_eta"].Fill(genWZ_p4.Eta())
      histosDict["h_genWZ_phi"].Fill(genWZ_p4.Phi())
      histosDict["h_genWZ_mass"].Fill(genWZ_p4.M())
      histosDict["h_genWZ_mass_v2"].Fill(genWZ_p4.M())

      #
      # Quarks from W
      #
      genWq0 = genWbosons[0].daughters[0]
      genWq1 = genWbosons[0].daughters[1]
      if genWq0.pt < genWq1.pt:
        genWq0 = genWbosons[0].daughters[1]
        genWq1 = genWbosons[0].daughters[0]

      genWq0_init = genWq0
      genWq1_init = genWq1

      #
      # Neutrinos from Z
      #
      genZv0 = genZbosons[0].daughters[0]
      genZv1 = genZbosons[0].daughters[1]
      if genZv0.pt < genZv1.pt:
        genZv0 = genZbosons[0].daughters[1]
        genZv1 = genZbosons[0].daughters[0]

      genZv0_init = genZv0
      genZv1_init = genZv1

      genWq0_p4 = genWq0.p4(usePDGIdMass=True)
      genWq1_p4 = genWq1.p4(usePDGIdMass=True)

      genZv0_p4 = genZv0.p4(usePDGIdMass=True)
      genZv1_p4 = genZv1.p4(usePDGIdMass=True)

      genW_qq_p4 = genWq0_p4 + genWq1_p4
      genZ_vv_p4 = genZv0_p4 + genZv1_p4

      genWZ_qqvv_p4 = genW_qq_p4 + genZ_vv_p4

      histosDict["h_genWq0_pt"].Fill(genWq0_p4.Pt())
      histosDict["h_genWq0_eta"].Fill(genWq0_p4.Eta())
      histosDict["h_genWq0_phi"].Fill(genWq0_p4.Phi())
      histosDict["h_genWq0_mass"].Fill(genWq0_p4.M())

      histosDict["h_genWq1_pt"].Fill(genWq1_p4.Pt())
      histosDict["h_genWq1_eta"].Fill(genWq1_p4.Eta())
      histosDict["h_genWq1_phi"].Fill(genWq1_p4.Phi())
      histosDict["h_genWq1_mass"].Fill(genWq1_p4.M())

      histosDict["h_genZv0_pt"].Fill(genZv0_p4.Pt())
      histosDict["h_genZv0_eta"].Fill(genZv0_p4.Eta())
      histosDict["h_genZv0_phi"].Fill(genZv0_p4.Phi())
      histosDict["h_genZv0_mass"].Fill(genZv0_p4.M())

      histosDict["h_genZv1_pt"].Fill(genZv1_p4.Pt())
      histosDict["h_genZv1_eta"].Fill(genZv1_p4.Eta())
      histosDict["h_genZv1_phi"].Fill(genZv1_p4.Phi())
      histosDict["h_genZv1_mass"].Fill(genZv1_p4.M())

      histosDict["h_genW_qq_pt"].Fill(genW_qq_p4.Pt())
      histosDict["h_genW_qq_eta"].Fill(genW_qq_p4.Eta())
      histosDict["h_genW_qq_phi"].Fill(genW_qq_p4.Phi())
      histosDict["h_genW_qq_mass"].Fill(genW_qq_p4.M())

      histosDict["h_genZ_vv_pt"].Fill(genZ_vv_p4.Pt())
      histosDict["h_genZ_vv_eta"].Fill(genZ_vv_p4.Eta())
      histosDict["h_genZ_vv_phi"].Fill(genZ_vv_p4.Phi())
      histosDict["h_genZ_vv_mass"].Fill(genZ_vv_p4.M())

      histosDict["h_genWZ_qqvv_pt"].Fill(genWZ_qqvv_p4.Pt())
      histosDict["h_genWZ_qqvv_eta"].Fill(genWZ_qqvv_p4.Eta())
      histosDict["h_genWZ_qqvv_phi"].Fill(genWZ_qqvv_p4.Phi())
      histosDict["h_genWZ_qqvv_mass"].Fill(genWZ_qqvv_p4.M())

      genWq0_final = getFinalCopy(genWq0)
      genWq1_final = getFinalCopy(genWq1)

      genZv0_final = getFinalCopy(genZv0)
      genZv1_final = getFinalCopy(genZv1)

      genWq0_final_p4 = genWq0_final.p4(usePDGIdMass=True)
      genWq1_final_p4 = genWq1_final.p4(usePDGIdMass=True)
      genZv0_final_p4 = genZv0_final.p4(usePDGIdMass=True)
      genZv1_final_p4 = genZv1_final.p4(usePDGIdMass=True)

      genW_final_qq_p4 = genWq0_final_p4 + genWq1_final_p4
      genZ_final_vv_p4 = genZv0_final_p4 + genZv1_final_p4

      genWZ_final_qqvv_p4  = genW_final_qq_p4 + genZ_final_vv_p4

      histosDict["h_final_genWq0_pt"].Fill(genWq0_final_p4.Pt())
      histosDict["h_final_genWq0_eta"].Fill(genWq0_final_p4.Eta())
      histosDict["h_final_genWq0_phi"].Fill(genWq0_final_p4.Phi())
      histosDict["h_final_genWq0_mass"].Fill(genWq0_final_p4.M())

      histosDict["h_final_genWq1_pt"].Fill(genWq1_final_p4.Pt())
      histosDict["h_final_genWq1_eta"].Fill(genWq1_final_p4.Eta())
      histosDict["h_final_genWq1_phi"].Fill(genWq1_final_p4.Phi())
      histosDict["h_final_genWq1_mass"].Fill(genWq1_final_p4.M())

      histosDict["h_final_genZv0_pt"].Fill(genZv0_final_p4.Pt())
      histosDict["h_final_genZv0_eta"].Fill(genZv0_final_p4.Eta())
      histosDict["h_final_genZv0_phi"].Fill(genZv0_final_p4.Phi())
      histosDict["h_final_genZv0_mass"].Fill(genZv0_final_p4.M())

      histosDict["h_final_genZv1_pt"].Fill(genZv1_final_p4.Pt())
      histosDict["h_final_genZv1_eta"].Fill(genZv1_final_p4.Eta())
      histosDict["h_final_genZv1_phi"].Fill(genZv1_final_p4.Phi())
      histosDict["h_final_genZv1_mass"].Fill(genZv1_final_p4.M())

      histosDict["h_genW_final_qq_pt"].Fill(genW_final_qq_p4.Pt())
      histosDict["h_genW_final_qq_eta"].Fill(genW_final_qq_p4.Eta())
      histosDict["h_genW_final_qq_phi"].Fill(genW_final_qq_p4.Phi())
      histosDict["h_genW_final_qq_mass"].Fill(genW_final_qq_p4.M())

      histosDict["h_genZ_final_vv_pt"].Fill(genZ_final_vv_p4.Pt())
      histosDict["h_genZ_final_vv_eta"].Fill(genZ_final_vv_p4.Eta())
      histosDict["h_genZ_final_vv_phi"].Fill(genZ_final_vv_p4.Phi())
      histosDict["h_genZ_final_vv_mass"].Fill(genZ_final_vv_p4.M())

      histosDict["h_genWZ_final_qqvv_pt"].Fill(genWZ_final_qqvv_p4.Pt())
      histosDict["h_genWZ_final_qqvv_eta"].Fill(genWZ_final_qqvv_p4.Eta())
      histosDict["h_genWZ_final_qqvv_phi"].Fill(genWZ_final_qqvv_p4.Phi())
      histosDict["h_genWZ_final_qqvv_mass"].Fill(genWZ_final_qqvv_p4.M())

  ######################################################
  #
  # ZZ -> vvqq
  #
  ######################################################
  if isZZvvqq:
    #----------------------------------------------
    # Skip event if we have less than two.
    # In principle, we should always have exactly
    # two W-bosons. If we don't have exactly two,
    # we should investigate why.
    #
    #-----------------------------------------------
    if len(genZbosons) < 2:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Skip.")
      continue
    if len(genZbosons) > 2:
      print(f"Warning! Event {iEntry} has {len(genZbosons)} Z-bosons. Take the leading two.")

    # genPartDumper.analyze(event, GenPartAll)

    #
    # Sort Z-bosons by pt
    #
    genZbosons.sort(key=lambda x: x.pt, reverse=True)

    if len(genZbosons) == 2:

      genZ0_temp = genZbosons[0]
      genZ1_temp = genZbosons[1]

      genZvv=None
      genZqq=None

      if abs(genZ0_temp.daughters[0].pdgId) in [12,14,16] and abs(genZ1_temp.daughters[0].pdgId) in [12,14,16]:
        print("Warning! Both Z decays to vv")
        continue
      elif abs(genZ0_temp.daughters[0].pdgId) in [1,2,3,4,5] and abs(genZ1_temp.daughters[0].pdgId) in [1,2,3,4,5]:
        print("Warning! Both Z decays to qq")
        continue

      if abs(genZ0_temp.daughters[0].pdgId) in [12,14,16] and abs(genZ1_temp.daughters[0].pdgId) in [1,2,3,4,5]:
        genZvv = genZ0_temp
        genZqq = genZ1_temp
      elif abs(genZ1_temp.daughters[0].pdgId) in [12,14,16] and abs(genZ0_temp.daughters[0].pdgId) in [1,2,3,4,5]:
        genZvv = genZ1_temp
        genZqq = genZ0_temp
      else:
        print("Warning! Unable to identify Z->vv and Z->qq")
        continue

      genZvv_p4 = genZvv.p4()
      genZqq_p4 = genZqq.p4()

      genZZ_p4 = genZvv_p4 + genZqq_p4

      if genZvv_p4.Pt() >= 200. and genZqq_p4.Pt() >= 200.: nEventsVPt200 += 1
      if genZvv_p4.Pt() >= 250. and genZqq_p4.Pt() >= 250.: nEventsVPt250 += 1

      genZvv_init = getFirstCopy(genZvv)
      genZqq_init = getFirstCopy(genZqq)

      genZvv_init_p4 = genZvv_init.p4()
      genZqq_init_p4 = genZqq_init.p4()

      genZZ_init_p4 = genZvv_init_p4 + genZqq_init_p4

      histosDict["h_genZvv_init_pt"].Fill(genZvv_init_p4.Pt())
      histosDict["h_genZvv_init_eta"].Fill(genZvv_init_p4.Eta())
      histosDict["h_genZvv_init_phi"].Fill(genZvv_init_p4.Phi())
      histosDict["h_genZvv_init_mass"].Fill(genZvv_init_p4.M())

      histosDict["h_genZqq_init_pt"].Fill(genZqq_init_p4.Pt())
      histosDict["h_genZqq_init_eta"].Fill(genZqq_init_p4.Eta())
      histosDict["h_genZqq_init_phi"].Fill(genZqq_init_p4.Phi())
      histosDict["h_genZqq_init_mass"].Fill(genZqq_init_p4.M())

      histosDict["h_genZZ_init_pt"].Fill(genZZ_init_p4.Pt())
      histosDict["h_genZZ_init_eta"].Fill(genZZ_init_p4.Eta())
      histosDict["h_genZZ_init_phi"].Fill(genZZ_init_p4.Phi())
      histosDict["h_genZZ_init_mass"].Fill(genZZ_init_p4.M())
      histosDict["h_genZZ_init_mass_v2"].Fill(genZZ_init_p4.M())

      histosDict["h_genZqq_pt"].Fill(genZqq_p4.Pt())
      histosDict["h_genZqq_eta"].Fill(genZqq_p4.Eta())
      histosDict["h_genZqq_phi"].Fill(genZqq_p4.Phi())
      histosDict["h_genZqq_mass"].Fill(genZqq_p4.M())

      histosDict["h_genZvv_pt"].Fill(genZvv_p4.Pt())
      histosDict["h_genZvv_eta"].Fill(genZvv_p4.Eta())
      histosDict["h_genZvv_phi"].Fill(genZvv_p4.Phi())
      histosDict["h_genZvv_mass"].Fill(genZvv_p4.M())

      histosDict["h_genZZ_pt"].Fill(genZZ_p4.Pt())
      histosDict["h_genZZ_eta"].Fill(genZZ_p4.Eta())
      histosDict["h_genZZ_phi"].Fill(genZZ_p4.Phi())
      histosDict["h_genZZ_mass"].Fill(genZZ_p4.M())
      histosDict["h_genZZ_mass_v2"].Fill(genZZ_p4.M())

      #
      # Quarks from Z
      #
      genZqq_q0 = genZqq.daughters[0]
      genZqq_q1 = genZqq.daughters[1]
      if genZqq_q0.pt < genZqq_q1.pt:
        genZqq_q0 = genZqq.daughters[1]
        genZqq_q1 = genZqq.daughters[0]

      genZqq_q0_init = genZqq_q0
      genZqq_q1_init = genZqq_q1

      #
      # Neutrinos from Z
      #
      genZvv_v0 = genZvv.daughters[0]
      genZvv_v1 = genZvv.daughters[1]
      if genZvv_v0.pt < genZvv_v1.pt:
        genZvv_v0 = genZvv.daughters[1]
        genZvv_v1 = genZvv.daughters[0]

      genZvv_v0_init = genZvv_v0
      genZvv_v1_init = genZvv_v1


      genZvv_v0_p4 = genZvv_v0.p4(usePDGIdMass=True)
      genZvv_v1_p4 = genZvv_v1.p4(usePDGIdMass=True)

      genZqq_q0_p4 = genZqq_q0.p4(usePDGIdMass=True)
      genZqq_q1_p4 = genZqq_q1.p4(usePDGIdMass=True)

      genZvv_vv_p4 = genZvv_v0_p4 + genZvv_v1_p4
      genZqq_qq_p4 = genZqq_q0_p4 + genZqq_q1_p4

      genZZ_qqvv_p4 = genZvv_vv_p4 + genZqq_qq_p4

      histosDict["h_genZvv_v0_pt"].Fill(genZvv_v0_p4.Pt())
      histosDict["h_genZvv_v0_eta"].Fill(genZvv_v0_p4.Eta())
      histosDict["h_genZvv_v0_phi"].Fill(genZvv_v0_p4.Phi())
      histosDict["h_genZvv_v0_mass"].Fill(genZvv_v0_p4.M())

      histosDict["h_genZvv_v1_pt"].Fill(genZvv_v1_p4.Pt())
      histosDict["h_genZvv_v1_eta"].Fill(genZvv_v1_p4.Eta())
      histosDict["h_genZvv_v1_phi"].Fill(genZvv_v1_p4.Phi())
      histosDict["h_genZvv_v1_mass"].Fill(genZvv_v1_p4.M())

      histosDict["h_genZqq_q0_pt"].Fill(genZqq_q0_p4.Pt())
      histosDict["h_genZqq_q0_eta"].Fill(genZqq_q0_p4.Eta())
      histosDict["h_genZqq_q0_phi"].Fill(genZqq_q0_p4.Phi())
      histosDict["h_genZqq_q0_mass"].Fill(genZqq_q0_p4.M())

      histosDict["h_genZqq_q1_pt"].Fill(genZqq_q1_p4.Pt())
      histosDict["h_genZqq_q1_eta"].Fill(genZqq_q1_p4.Eta())
      histosDict["h_genZqq_q1_phi"].Fill(genZqq_q1_p4.Phi())
      histosDict["h_genZqq_q1_mass"].Fill(genZqq_q1_p4.M())

      histosDict["h_genZvv_vv_pt"].Fill(genZvv_vv_p4.Pt())
      histosDict["h_genZvv_vv_eta"].Fill(genZvv_vv_p4.Eta())
      histosDict["h_genZvv_vv_phi"].Fill(genZvv_vv_p4.Phi())
      histosDict["h_genZvv_vv_mass"].Fill(genZvv_vv_p4.M())

      histosDict["h_genZqq_qq_pt"].Fill(genZqq_qq_p4.Pt())
      histosDict["h_genZqq_qq_eta"].Fill(genZqq_qq_p4.Eta())
      histosDict["h_genZqq_qq_phi"].Fill(genZqq_qq_p4.Phi())
      histosDict["h_genZqq_qq_mass"].Fill(genZqq_qq_p4.M())

      histosDict["h_genZZ_qqvv_pt"].Fill(genZZ_qqvv_p4.Pt())
      histosDict["h_genZZ_qqvv_eta"].Fill(genZZ_qqvv_p4.Eta())
      histosDict["h_genZZ_qqvv_phi"].Fill(genZZ_qqvv_p4.Phi())
      histosDict["h_genZZ_qqvv_mass"].Fill(genZZ_qqvv_p4.M())

      genZvv_v0_final = getFinalCopy(genZvv_v0)
      genZvv_v1_final = getFinalCopy(genZvv_v1)

      genZqq_q0_final = getFinalCopy(genZqq_q0)
      genZqq_q1_final = getFinalCopy(genZqq_q1)

      genZvv_v0_final_p4 = genZvv_v0_final.p4(usePDGIdMass=True)
      genZvv_v1_final_p4 = genZvv_v1_final.p4(usePDGIdMass=True)
      genZqq_q0_final_p4 = genZqq_q0_final.p4(usePDGIdMass=True)
      genZqq_q1_final_p4 = genZqq_q1_final.p4(usePDGIdMass=True)

      genZ_final_qq_p4 = genZqq_q0_final_p4 + genZqq_q1_final_p4
      genZ_final_vv_p4 = genZvv_v0_final_p4 + genZvv_v1_final_p4

      genZZ_final_qqvv_p4  = genZ_final_vv_p4 + genZ_final_qq_p4

      histosDict["h_genZvv_final_v0_pt"].Fill(genZvv_v0_final_p4.Pt())
      histosDict["h_genZvv_final_v0_eta"].Fill(genZvv_v0_final_p4.Eta())
      histosDict["h_genZvv_final_v0_phi"].Fill(genZvv_v0_final_p4.Phi())
      histosDict["h_genZvv_final_v0_mass"].Fill(genZvv_v0_final_p4.M())

      histosDict["h_genZvv_final_v1_pt"].Fill(genZvv_v1_final_p4.Pt())
      histosDict["h_genZvv_final_v1_eta"].Fill(genZvv_v1_final_p4.Eta())
      histosDict["h_genZvv_final_v1_phi"].Fill(genZvv_v1_final_p4.Phi())
      histosDict["h_genZvv_final_v1_mass"].Fill(genZvv_v1_final_p4.M())

      histosDict["h_genZqq_final_q0_pt"].Fill(genZqq_q0_final_p4.Pt())
      histosDict["h_genZqq_final_q0_eta"].Fill(genZqq_q0_final_p4.Eta())
      histosDict["h_genZqq_final_q0_phi"].Fill(genZqq_q0_final_p4.Phi())
      histosDict["h_genZqq_final_q0_mass"].Fill(genZqq_q0_final_p4.M())

      histosDict["h_genZqq_final_q1_pt"].Fill(genZqq_q1_final_p4.Pt())
      histosDict["h_genZqq_final_q1_eta"].Fill(genZqq_q1_final_p4.Eta())
      histosDict["h_genZqq_final_q1_phi"].Fill(genZqq_q1_final_p4.Phi())
      histosDict["h_genZqq_final_q1_mass"].Fill(genZqq_q1_final_p4.M())

      histosDict["h_genZ_final_qq_pt"].Fill(genZ_final_qq_p4.Pt())
      histosDict["h_genZ_final_qq_eta"].Fill(genZ_final_qq_p4.Eta())
      histosDict["h_genZ_final_qq_phi"].Fill(genZ_final_qq_p4.Phi())
      histosDict["h_genZ_final_qq_mass"].Fill(genZ_final_qq_p4.M())

      histosDict["h_genZ_final_vv_pt"].Fill(genZ_final_vv_p4.Pt())
      histosDict["h_genZ_final_vv_eta"].Fill(genZ_final_vv_p4.Eta())
      histosDict["h_genZ_final_vv_phi"].Fill(genZ_final_vv_p4.Phi())
      histosDict["h_genZ_final_vv_mass"].Fill(genZ_final_vv_p4.M())

      histosDict["h_genZZ_final_qqvv_pt"].Fill(genZZ_final_qqvv_p4.Pt())
      histosDict["h_genZZ_final_qqvv_eta"].Fill(genZZ_final_qqvv_p4.Eta())
      histosDict["h_genZZ_final_qqvv_phi"].Fill(genZZ_final_qqvv_p4.Phi())
      histosDict["h_genZZ_final_qqvv_mass"].Fill(genZZ_final_qqvv_p4.M())

  ######################################################
  #
  # VBS quarks
  #
  ######################################################
  if len(genQuarksVBS) >= 2:
    genQuarkVBS0 = genQuarksVBS[0]
    genQuarkVBS1 = genQuarksVBS[1]
    if genQuarkVBS0.pt < genQuarkVBS1.pt:
      genQuarkVBS0 = genQuarksVBS[1]
      genQuarkVBS1 = genQuarksVBS[0]

    genQuarkVBS0_p4 = genQuarkVBS0.p4(usePDGIdMass=True)
    genQuarkVBS1_p4 = genQuarkVBS1.p4(usePDGIdMass=True)

    gen_qqVBS_p4 = genQuarkVBS0_p4+genQuarkVBS1_p4

    histosDict["h_genQuarkVBS0_pt"].Fill(genQuarkVBS0_p4.Pt())
    histosDict["h_genQuarkVBS0_eta"].Fill(genQuarkVBS0_p4.Eta())
    histosDict["h_genQuarkVBS0_phi"].Fill(genQuarkVBS0_p4.Phi())
    histosDict["h_genQuarkVBS0_mass"].Fill(genQuarkVBS0_p4.M())
    histosDict["h_genQuarkVBS1_pt"].Fill(genQuarkVBS1_p4.Pt())
    histosDict["h_genQuarkVBS1_eta"].Fill(genQuarkVBS1_p4.Eta())
    histosDict["h_genQuarkVBS1_phi"].Fill(genQuarkVBS1_p4.Phi())
    histosDict["h_genQuarkVBS1_mass"].Fill(genQuarkVBS1_p4.M())
    histosDict["h_genqqVBS_pt"].Fill(gen_qqVBS_p4.Pt())
    histosDict["h_genqqVBS_eta"].Fill(gen_qqVBS_p4.Eta())
    histosDict["h_genqqVBS_phi"].Fill(gen_qqVBS_p4.Phi())
    histosDict["h_genqqVBS_mass"].Fill(gen_qqVBS_p4.M())
    histosDict["h_genqqVBS_mass_v2"].Fill(gen_qqVBS_p4.M())

    histosDict["h_genqqVBS_deltaEta"].Fill(genQuarkVBS0_p4.Eta()-genQuarkVBS1_p4.Eta())
    histosDict["h_genqqVBS_deltaEtaAbs"].Fill(ROOT.TMath.Abs(genQuarkVBS0_p4.Eta()-genQuarkVBS1_p4.Eta()))
    histosDict["h_genqqVBS_eta0timeseta1"].Fill(genQuarkVBS0_p4.Eta() * genQuarkVBS1_p4.Eta())
    histosDict["h_genqqVBS_deltaPhi"].Fill(genQuarkVBS0_p4.Phi()-genQuarkVBS1_p4.Phi())

    histosDict["h2_genqqVBS_eta_vs_genQuarkVBS0_eta"].Fill(gen_qqVBS_p4.Eta(),genQuarkVBS0_p4.Eta())
    histosDict["h2_genqqVBS_eta_vs_genQuarkVBS1_eta"].Fill(gen_qqVBS_p4.Eta(),genQuarkVBS1_p4.Eta())
    histosDict["h2_genQuarkVBS0_eta_vs_genQuarkVBS1_eta"].Fill(genQuarkVBS0_p4.Eta(),genQuarkVBS1_p4.Eta())

    histosDict["h2_genqqVBS_deltaEtaAbs_vs_genqqVBS_mass"].Fill(ROOT.TMath.Abs(genQuarkVBS0_p4.Eta()-genQuarkVBS1_p4.Eta()),gen_qqVBS_p4.M())
    histosDict["h2_genqqVBS_eta0timeseta1_vs_genqqVBS_deltaEtaAbs"].Fill(genQuarkVBS0_p4.Eta() * genQuarkVBS1_p4.Eta(),ROOT.TMath.Abs(genQuarkVBS0_p4.Eta()-genQuarkVBS1_p4.Eta()))

#================================================================
#
# Event Loop END
#
#================================================================
print(f"frac_nEventsVPt200 = {nEventsVPt200/nEntries}")
print(f"frac_nEventsVPt250 = {nEventsVPt250/nEntries}")
print(f"frac_nEventsLessThanTwoVBosons = {nEventsLessThanTwoVBosons/nEntries}")

outFile = f"./output/Histo_{sample_name}.root"
print(f"Saving histograms in {outFile}")
outHisto = ROOT.TFile(outFile,"RECREATE")
for hName in histosDict:
  histosDict[hName].Write()
outHisto.Close()

time_end = datetime.datetime.now()
elapsed = time_end - time_start
elapsed_str = str(datetime.timedelta(seconds=elapsed.seconds))
print(f"{str(sys.argv[0])}::DONE::Time({str(time_start)},{str(time_end)})::Elapsed({elapsed_str})")
