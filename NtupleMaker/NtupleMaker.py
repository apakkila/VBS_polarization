#!/usr/bin/env python3 -u
import os
import sys
import argparse
import subprocess
from collections import OrderedDict
import ROOT
ROOT.gROOT.SetBatch()
import NtupleMaker_Helpers
import NtupleMaker_Helpers_Gen



# Note: Need to do this the first time around to install correctionlib.
# After setupROOT.sh has been sourced. See:
# https://github.com/cms-nanoAOD/correctionlib/discussions/101
# > python3 -m pip install  --user --no-binary=correctionlib correctionlib
import correctionlib
correctionlib.register_pyroot_binding()

#
# Setup optimization level here. FIKRI: Can this make RDF faster by
# increasing JIT optimization or will the optimization make the run-time
# slower overall? Or maybe we're just IO limited with eos LOL.
#
# ROOT.gROOT.ProcessLine(".O 2") # Set optimization level to 2
# ROOT.gROOT.ProcessLine(".O") # Show optimization level

#
# Load the library and link to the header file in ./modules directory
# We have to compile there first  before running this script
#
### ROOT.gSystem.Load("modules/obj/LumiFilterV2_h.so")
ROOT.gSystem.Load("modules/obj/NtupleMaker_Functions_h.so")
ROOT.gSystem.Load("modules/obj/NtupleMaker_Functions_GenLevel_h.so")

code_header = '''
using FourVector = ROOT::Math::PtEtaPhiMVector;
using namespace ROOT::VecOps;
'''
ROOT.gInterpreter.Declare(code_header)

EOSUSER="root://eosuser.cern.ch/"
EOSCMS="root://eoscms.cern.ch/"
TMPDIR=os.getenv("TMPDIR")

prod_tag=""
# prod_tag+="_VCandMassCut"
# prod_tag+="_AddGenPart"

outDirNominalTrees = f"/eos/user/n/nbinnorj/VBSAllHadAna/Ntuples{prod_tag}/"
outDirSystTrees  = f"/eos/user/n/nbinnorj/VBSAllHadAna/NtuplesSyst{prod_tag}/"

disableFilters = False

#
#
#
"""
from distributed import Client
from dask_lxplus import CernCluster
import socket
def create_connection(n_workers):
  n_port = 7892
  cluster = CernCluster(
    n_workers=n_workers,
    processes=True,
    memory='2000MB',
    disk='1000MB',
    death_timeout = '60',
    lcg = True,
    nanny = False,
    container_runtime = "none",
    log_directory = "/afs/cern.ch/user/n/nbinnorj/condor/log",
    scheduler_options={
      'port': n_port,
      'host': socket.gethostname(),
    },
    job_extra={
      '+JobFlavour': '"espresso"',
    },
  extra = ['--worker-port 10000:10100']
  )
  try:
    client = Client(cluster, timeout='5s')
  except TimeoutError:
    pass
  return client, cluster
"""


def main():
  print(f"\n\n")
  print(f"******************************************************************")
  print(f"NtupleMaker::main()::START")
  timerMain = ROOT.TStopwatch()
  timerMain.Start()

  parser = argparse.ArgumentParser("")
  parser.add_argument('-s', '--sample',   type=str,  default="")
  parser.add_argument('-d', '--indir',    type=str,  default="")
  parser.add_argument('-c', '--cores',    type=int,  default=2)
  parser.add_argument('-b', '--batch',    action='store_true', default=False)

  args = parser.parse_args()

  inDir = args.indir
  sampleName = args.sample
  isBatch = args.batch

  ROOT.ROOT.EnableImplicitMT(args.cores)

  #==========================================================================================
  #
  #
  #
  #==========================================================================================
  if not os.path.exists(outDirNominalTrees):
    os.makedirs(outDirNominalTrees)

  # if not os.path.exists(outDirSystTrees):
  #   os.makedirs(outDirSystTrees)

  print(f"{outDirNominalTrees=}")
  # print(f"{outDirSystTrees=}")
  #==========================================================================================
  #
  #
  #
  #==========================================================================================
  # Get Year and isMC
  eraName, triggerYear, corrlibEra, isMC = NtupleMaker_Helpers.GetYears(sampleName)
  #==========================================================================================
  #
  # Nominal
  #
  #==========================================================================================
  doNominal = True
  if doNominal:
    print("")
    print("----------------------------------------------------------------------------")
    print("Nominal")
    print("----------------------------------------------------------------------------")
    outFileTreePathNominalTemp = []
    outFileTreePathNominalTemp += MakeNtuple(inDir, sampleName, isBatch)
    MergeAndTransferNtuplesToEOS(outFileTreePathNominalTemp, sampleName)

  #==========================================================================================
  #
  # Loop over systematics
  #
  #==========================================================================================
  doSystVar = False

  systsList=[]
  systsList+=["SysAK8_Kin_jesTotalUp"]
  systsList+=["SysAK8_Kin_jesTotalDown"]
  systsList+=["SysAK4_Kin_jesTotalUp"]
  systsList+=["SysAK4_Kin_jesTotalDown"]
  systsList+=["SysAK4_Kin_jerUp"]
  systsList+=["SysAK4_Kin_jerDown"]

  if doSystVar and isMC:
    outFileTreePathSystTemp = []
    for systVar in systsList:
      print("")
      print("----------------------------------------------------------------------------")
      print(f"Systematics: {systVar}")
      print("----------------------------------------------------------------------------")
      outFileTreePathSystTemp += MakeNtuple(inDir, sampleName, isBatch, systVar)
    MergeAndTransferNtuplesToEOS(outFileTreePathSystTemp, sampleName, True)

  print(f"******************************************************************")
  timerMain.Stop(); timerMain.Print()
  print(f"NtupleMaker::main()::DONE::{sampleName}")

def MakeNtuple(inDir, sampleName, isBatch, systVar="Nominal"):
  print(f"===================================================================")
  print(f"NtupleMaker::MakeNtuple():Running sample:{sampleName},sys:{systVar}")

  timer = ROOT.TStopwatch()
  timer.Start()

  # Get Year and isMC
  eraName, triggerYear, corrlibEra, isMC = NtupleMaker_Helpers.GetYears(sampleName)

  #
  isMC_QCD  = "QCD" in sampleName
  isMC_TOP  = "TT_" in sampleName or "ST_" in sampleName
  isMC_SMVV = "WW" in sampleName or "WZ" in sampleName or "ZZ" in sampleName and not ("VBS" in sampleName)
  isMC_SMVBS = "VBS" in sampleName

  #
  # Check what kind of dataset is this for real data
  #
  isDatasetJetHT  = 0
  if not isMC:
   if "JetHT" in sampleName: isDatasetJetHT  = 1

  #
  # Check if its Nominal or systVar
  #
  isNominal = "Nominal" in systVar

  #
  # Integrated lumi in inverse picobarns
  #
  lumi_Dict = NtupleMaker_Helpers.lumi_Dict
  lumiUp_Dict = NtupleMaker_Helpers.lumiUp_Dict
  lumiDown_Dict = NtupleMaker_Helpers.lumiDown_Dict
  #
  # XS in picobarns
  #
  xs_Dict   = NtupleMaker_Helpers.xs_Dict
  #########################################
  #
  # Setup modules
  #
  #########################################
  # if not isMC:
  #   ROOT.gInterpreter.ProcessLine('LumiFilterV2 lumiFilt({year})'.format(year=eraName))

  #########################################
  #
  # Setup TChain
  #
  #########################################
  inFileName = f"NanoSkimMerged_{sampleName}.root"
  inFilePath = f"{inDir}/{inFileName}"
  if not(os.path.isfile(inFilePath)):
    raise Exception(f"File not found. Please check. Given path: {inFilePath}")

  if "/eos/user" in inFilePath:
    inFilePath = EOSUSER+inFilePath
  elif "/eos/cms" in inFilePath:
    inFilePath = EOSCMS+inFilePath
  else:
    inFilePath = inFilePath
  print(f"inFilePath: {inFilePath}")

  treeEvents =  ROOT.TChain("Events")
  treeEvents.Add(inFilePath)
  #########################################
  #
  # Setup RDF
  #
  #########################################
  df = None
  df = ROOT.ROOT.RDataFrame(treeEvents)

  # client, cluster = create_connection(4)
  # rdf = ROOT.RDF.Experimental.Distributed.Dask.RDataFrame(treeEvents, dask_client=client)

  if not isBatch:
    ROOT.RDF.Experimental.AddProgressBar(df)
  #########################################
  #
  # Event-level variables and selection
  #
  #########################################
  if isMC:
    df = df.Define("mcXS",f"{xs_Dict[sampleName]}")
    df = df.Define("mcKFactor", "1.f")
    df = df.Define("eventWeightScale",     f"float((mcXS * {lumi_Dict[eraName]})/ genEventSumw)")
    df = df.Define("eventWeightScaleUp",   f"float((mcXS * {lumiUp_Dict[eraName]})/ genEventSumw)")
    df = df.Define("eventWeightScaleDown", f"float((mcXS * {lumiDown_Dict[eraName]})/ genEventSumw)")
    df = df.Define("mcSumOfWeight",             "float(genEventSumw)")
    df = df.Define("mcGenWeight",               "genWeight")
    df = df.Define("evtWeight",                 "mcGenWeight*eventWeightScale")
    df = df.Define("evtWeight_SystLumi_sfUp",   "mcGenWeight*eventWeightScaleUp")
    df = df.Define("evtWeight_SystLumi_sfDown", "mcGenWeight*eventWeightScaleDown")
    #
    df = df.Define("mcPUWeight",                              "puWeight")
    df = df.Define("mcPUWeight_SystPU_sfUp",                  "puWeightUp")
    df = df.Define("mcPUWeight_SystPU_sfDown",                "puWeightDown")
    df = df.Define("L1PreFiringWeight",                       "L1PreFiringWeight_Nom")
    df = df.Define("L1PreFiringWeight_SystL1PreFire_sfUp",    "L1PreFiringWeight_Up")
    df = df.Define("L1PreFiringWeight_SystL1PreFire_sfDown",  "L1PreFiringWeight_Dn")
  else:
    df = df.Define("evtWeight",    "1.f")

  df = df.Define("Count","1")
  #
  # For Data, must pass golden json. NOTE: Not needed here.
  # Already done at NanoSkim level.
  #
  # if not isMC:
  #   df = df.Define("passLumiMask","lumiFilt.eval(run,luminosityBlock)")
  #   df = df.Filter("passLumiMask")

  df = df.Define("isMC", str(isMC))
  df = df.Define("isDatasetJetHT", str(isDatasetJetHT))
  #==================================================
  #
  # Decorate RDF with missing trigger branches
  #
  #==================================================
  listOfBranchInNano = df.GetColumnNames()
  # for b in listOfBranchInNano: print(b)
  trigPathAll  = NtupleMaker_Helpers.GetTriggers(eraName)
  # Get unique elements
  trigPathAllFinal = set(trigPathAll)

  #
  # The missing trigger branches just set to 0.
  #
  for trig in trigPathAllFinal:
    if trig not in(listOfBranchInNano):
      print (f"Missing {trig}. Adding here now.")
      df = df.Define(trig,"0")
  #==================================================
  #
  # First level skim
  #
  #==================================================
  #################
  # Trigger
  #################
  trigPathStr = "||".join(trigPathAllFinal)
  if not disableFilters:
    df = df.Filter(trigPathStr, "Skim_Trigger")

  ########################################################
  # At least two fatjets in the FatJet collection
  #######################################################
  if not disableFilters:
    df = df.Filter("nFatJet>=2","Skim_NFatJet")

  ##################################
  #
  ##################################
  df = df.Define("nPVs",       "PV_npvs")
  df = df.Define("nPVsGood",   "PV_npvsGood")
  df = df.Define("passOneNPV", "nPVsGood>=1")

  if not disableFilters:
    df = df.Filter("passOneNPV", "Cut_NPV>=1")

  #==================================================
  #
  # VCand-VCand selection
  #
  #==================================================
  # Kinematics as in NanoAOD (Deprecated)
  ####fatjet_pt_def   = "FatJet_pt"
  ####fatjet_mass_def = "FatJet_mass"
  #
  fatjet_pt_def   = "FatJet_pt_nom"
  fatjet_mass_def = "FatJet_mass_nom"
  if systVar == "SysAK8_Kin_jesTotalUp":
    fatjet_pt_def   = "FatJet_pt_jesTotalUp"
    fatjet_mass_def = "FatJet_mass_jesTotalUp"
  if systVar == "SysAK8_Kin_jesTotalDown":
    fatjet_pt_def   = "FatJet_pt_jesTotalDown"
    fatjet_mass_def = "FatJet_mass_jesTotalDown"
  print(f"{fatjet_pt_def=}")
  print(f"{fatjet_mass_def=}")

  df = df.Define("FatJet_p4",          f"Construct<FourVector>({fatjet_pt_def}, FatJet_eta, FatJet_phi, {fatjet_mass_def})")
  df = df.Define("FatJet_p4_pt",       "return Map(FatJet_p4,[](const FourVector& v){return float(v.Pt());});")
  df = df.Define("FatJet_p4_eta",      "return Map(FatJet_p4,[](const FourVector& v){return float(v.Eta());});")
  df = df.Define("FatJet_p4_phi",      "return Map(FatJet_p4,[](const FourVector& v){return float(v.Phi());});")
  df = df.Define("FatJet_p4_mass",     "return Map(FatJet_p4,[](const FourVector& v){return float(v.M());});")
  df = df.Define("FatJet_corr_jecNom", "FatJet_pt_nom/FatJet_pt_raw")
  df = df.Define("FatJet_corr_jec",    f"{fatjet_pt_def}/FatJet_pt_raw")

  tau21Def="[](const float t2,const float t1){if(t1>0.) return float(t2/t1); else return -1.f;});"
  df = df.Define("FatJet_tau21",      f"return Map(FatJet_tau2,FatJet_tau1,{tau21Def}")
  df = df.Define("FatJet_passID",     "FatJet_jetId & (1<<1)")
  df = df.Define("FatJet_isSignal",   "(FatJet_p4_pt > 200.f) && (abs(FatJet_p4_eta) < 2.4f) && FatJet_passID")
  #
  #
  #
  fatjet_signal_def = "FatJet_isSignal==1"
  df = df.Define("nSignalFatJet",                 f"Sum({fatjet_signal_def})")
  df = df.Define("SignalFatJet_p4",               f"FatJet_p4[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_p4_pt",            f"FatJet_p4_pt[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_p4_eta",           f"FatJet_p4_eta[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_p4_phi",           f"FatJet_p4_phi[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_p4_mass",          f"FatJet_p4_mass[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_pt_nom",           f"FatJet_pt_nom[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_corr_jecNom",      f"FatJet_corr_jecNom[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_corr_jec",         f"FatJet_corr_jec[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_tau21",            f"FatJet_tau21[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_msoftdrop",        f"FatJet_msoftdrop[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_particleNet_mass", f"FatJet_particleNet_mass[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_subJetIdx1",       f"FatJet_subJetIdx1[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_subJetIdx2",       f"FatJet_subJetIdx2[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_msoftdrop_raw",       "MSoftRaw(SignalFatJet_subJetIdx1,SignalFatJet_subJetIdx2,SubJet_pt,SubJet_eta,SubJet_phi,SubJet_mass,SubJet_rawFactor)")
  df = df.Define("SignalFatJet_msoftdrop_corrAK8JEC","MSoftAK8JEC(SignalFatJet_subJetIdx1,SignalFatJet_subJetIdx2,SignalFatJet_corr_jec,SubJet_pt,SubJet_eta,SubJet_phi,SubJet_mass,SubJet_rawFactor)")
  if isMC:
    df = df.Define("SignalFatJet_nBHadrons",     f"FatJet_nBHadrons[{fatjet_signal_def}]")
    df = df.Define("SignalFatJet_nCHadrons",     f"FatJet_nCHadrons[{fatjet_signal_def}]")
    df = df.Define("SignalFatJet_hadronFlavour", f"FatJet_hadronFlavour[{fatjet_signal_def}]")
    df = df.Define("SignalFatJet_genJetAK8Idx",  f"FatJet_genJetAK8Idx[{fatjet_signal_def}]")
  #
  # Taggers
  #
  df = df.Define("SignalFatJet_particleNetMD_Xqq", f"FatJet_particleNetMD_Xqq[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_particleNetMD_Xbb", f"FatJet_particleNetMD_Xbb[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_particleNetMD_Xcc", f"FatJet_particleNetMD_Xcc[{fatjet_signal_def}]")
  df = df.Define("SignalFatJet_particleNetMD_QCD", f"FatJet_particleNetMD_QCD[{fatjet_signal_def}]")
  denom="SignalFatJet_particleNetMD_Xqq+SignalFatJet_particleNetMD_Xcc+SignalFatJet_particleNetMD_QCD"
  df = df.Define("SignalFatJet_particleNetMD_WvsQCD",f"(SignalFatJet_particleNetMD_Xqq+SignalFatJet_particleNetMD_Xcc)/({denom})")
  denom="SignalFatJet_particleNetMD_Xbb+SignalFatJet_particleNetMD_QCD"
  df = df.Define("SignalFatJet_particleNetMD_XbbvsQCD",f"(SignalFatJet_particleNetMD_Xbb)/({denom})")

  if isMC:
    df = df.Define("GenJetAK8_msoftdrop",   "MSoftGen(GenJetAK8_eta,GenJetAK8_phi,SubGenJetAK8_pt,SubGenJetAK8_eta,SubGenJetAK8_phi,SubGenJetAK8_mass)")

  #
  # Require event has at least two signal fatjets
  #
  df = df.Define("passEventVVCand", "nSignalFatJet>=2")
  if not disableFilters:
    df = df.Filter("passEventVVCand", "Cut_passEventVVCand")
  # df = df.Define("evtWeight_passEventVVCand", "genWeight" if isMC else "1.f")

  #
  # Sort fatjet by pt and take two leading (i.e highest pt) fatjet as VCand candidates
  #
  df = df.Define("VecIdxOfSignalFatJet","CustomArgsort(SignalFatJet_p4_pt, sort_from_highest)")
  df = df.Define("SignalFatJet0Idx",    "GetIdxFromVecIdx(VecIdxOfSignalFatJet, 0)")
  df = df.Define("SignalFatJet1Idx",    "GetIdxFromVecIdx(VecIdxOfSignalFatJet, 1)")

  def ConstructVCand(df, VCandName="VCand0", VCandIdx="SignalFatJet0Idx"):
    df = df.Define(f"{VCandName}_p4",                  f"GetFromVec(SignalFatJet_p4,{VCandIdx},FourVector())")
    df = df.Define(f"{VCandName}_pt",                  f"GetFromVec(SignalFatJet_p4_pt,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_eta",                 f"GetFromVec(SignalFatJet_p4_eta,{VCandIdx},-9.f)")
    df = df.Define(f"{VCandName}_phi",                 f"GetFromVec(SignalFatJet_p4_phi,{VCandIdx},-9.f)")
    df = df.Define(f"{VCandName}_mass",                f"GetFromVec(SignalFatJet_p4_mass,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_pt_nom",              f"GetFromVec(SignalFatJet_pt_nom,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_corr_jecNom",         f"GetFromVec(SignalFatJet_corr_jecNom,{VCandIdx},1.f)")
    df = df.Define(f"{VCandName}_corr_jec",            f"GetFromVec(SignalFatJet_corr_jec,{VCandIdx},1.f)")
    df = df.Define(f"{VCandName}_msoftdrop",           f"GetFromVec(SignalFatJet_msoftdrop,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNet_mass",    f"GetFromVec(SignalFatJet_particleNet_mass,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_msoftdrop_raw",       f"GetFromVec(SignalFatJet_msoftdrop_raw,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_msoftdrop_corrAK8JEC",f"GetFromVec(SignalFatJet_msoftdrop_corrAK8JEC,{VCandIdx},-1.f)")
    #
    #
    #
    if isMC:
      df = df.Define(f"{VCandName}_genJetAK8Idx",    f"GetFromVec(SignalFatJet_genJetAK8Idx,{VCandIdx},-1)")
      df = df.Define(f"{VCandName}_gen_pt",          f"GetFromVec(GenJetAK8_pt,{VCandName}_genJetAK8Idx,-1.f)")
      df = df.Define(f"{VCandName}_gen_eta",         f"GetFromVec(GenJetAK8_eta,{VCandName}_genJetAK8Idx,-9.f)")
      df = df.Define(f"{VCandName}_gen_phi",         f"GetFromVec(GenJetAK8_phi,{VCandName}_genJetAK8Idx,-9.f)")
      df = df.Define(f"{VCandName}_gen_mass",        f"GetFromVec(GenJetAK8_mass,{VCandName}_genJetAK8Idx,-1.f)")
      df = df.Define(f"{VCandName}_gen_msoftdrop",   f"GetFromVec(GenJetAK8_msoftdrop,{VCandName}_genJetAK8Idx,-1.f)")

    #
    # Tagger branches
    #
    df = df.Define(f"{VCandName}_particleNetMD_Xqq",      f"GetFromVec(SignalFatJet_particleNetMD_Xqq,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNetMD_Xbb",      f"GetFromVec(SignalFatJet_particleNetMD_Xbb,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNetMD_Xcc",      f"GetFromVec(SignalFatJet_particleNetMD_Xcc,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNetMD_QCD",      f"GetFromVec(SignalFatJet_particleNetMD_QCD,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNetMD_WvsQCD",   f"GetFromVec(SignalFatJet_particleNetMD_WvsQCD,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_particleNetMD_XbbvsQCD", f"GetFromVec(SignalFatJet_particleNetMD_XbbvsQCD,{VCandIdx},-1.f)")
    df = df.Define(f"{VCandName}_tau21",                  f"GetFromVec(SignalFatJet_tau21,{VCandIdx},-1.f)")


    #
    # ParticleNet WMD
    #
    ParticleNetWvsQCDMDCut = NtupleMaker_Helpers.ParticleNetWvsQCDMDCut
    df = df.Define(f"pass{VCandName}PreTag",        f"passEventVVCand")# Dummy-like flag for pretag
    df = df.Define(f"pass{VCandName}PNetWMD2p5",    f"{VCandName}_particleNetMD_WvsQCD >= {ParticleNetWvsQCDMDCut[eraName]['2p5']}")
    df = df.Define(f"pass{VCandName}PNetWMD1p0",    f"{VCandName}_particleNetMD_WvsQCD >= {ParticleNetWvsQCDMDCut[eraName]['1p0']}")
    df = df.Define(f"pass{VCandName}PNetWMD0p5",    f"{VCandName}_particleNetMD_WvsQCD >= {ParticleNetWvsQCDMDCut[eraName]['0p5']}")
    #
    df = df.Define(f"pass{VCandName}PNetWMD2p5NP",  f"(!pass{VCandName}PNetWMD2p5)")
    df = df.Define(f"pass{VCandName}PNetWMD2p5LP",  f"(pass{VCandName}PNetWMD2p5) &&  (!pass{VCandName}PNetWMD2p5)")
    df = df.Define(f"pass{VCandName}PNetWMD1p0LP",  f"(pass{VCandName}PNetWMD2p5) &&  (!pass{VCandName}PNetWMD1p0)")
    df = df.Define(f"pass{VCandName}PNetWMD0p5LP",  f"(pass{VCandName}PNetWMD2p5) &&  (!pass{VCandName}PNetWMD0p5)")
    df = df.Define(f"pass{VCandName}PNetWMD2p5HP",  f"(pass{VCandName}PNetWMD2p5) &&  (pass{VCandName}PNetWMD2p5)")
    df = df.Define(f"pass{VCandName}PNetWMD1p0HP",  f"(pass{VCandName}PNetWMD2p5) &&  (pass{VCandName}PNetWMD1p0)")
    df = df.Define(f"pass{VCandName}PNetWMD0p5HP",  f"(pass{VCandName}PNetWMD2p5) &&  (pass{VCandName}PNetWMD0p5)")
    #
    # ParticleNet Xbb
    # https://indico.cern.ch/event/1120932/#23-calibration-of-ul20172018-x
    #
    df = df.Define(f"pass{VCandName}PNetXbbMD",    f"{VCandName}_particleNetMD_XbbvsQCD >= 0.95") # Random cut here.
    df = df.Define(f"pass{VCandName}PNetXbbMDNP",  f"(!pass{VCandName}PNetXbbMD)")
    df = df.Define(f"pass{VCandName}PNetXbbMDHP",  f"(pass{VCandName}PNetXbbMD)")
    df = df.Define(f"pass{VCandName}PNetXbbMDLP",  f"(pass{VCandName}PNetXbbMD) && (!pass{VCandName}PNetXbbMD)") # Essentially no LP region for Xbb

    #
    # Check if Xbb tagger score is greater than Xqq and Xcc tagger score. If yes, its a candidate for Xbb
    #
    df = df.Define(f"pass{VCandName}XbbCand", f"{VCandName}_particleNetMD_Xbb > TMath::Max({VCandName}_particleNetMD_Xqq,{VCandName}_particleNetMD_Xcc)")
    df = df.Define(f"pass{VCandName}XqqCand", f"(!pass{VCandName}XbbCand)")

    #
    # Define cut regions whereby we check if the VCand is an Xbb candidate or not first.
    # If yes, apply Xbb tagger cut
    # If no, apply W tagger cuts
    #
    df = df.Define(f"pass{VCandName}XbbCand_passPNetXbbMDNP",  f"pass{VCandName}XbbCand && pass{VCandName}PNetXbbMDNP")
    df = df.Define(f"pass{VCandName}XbbCand_passPNetXbbMDLP",  f"pass{VCandName}XbbCand && pass{VCandName}PNetXbbMDLP")
    df = df.Define(f"pass{VCandName}XbbCand_passPNetXbbMDHP",  f"pass{VCandName}XbbCand && pass{VCandName}PNetXbbMDHP")
    #
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD2p5NP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD2p5NP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD2p5LP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD2p5LP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD1p0LP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD1p0LP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD0p5LP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD0p5LP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD2p5HP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD2p5HP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD1p0HP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD1p0HP")
    df = df.Define(f"pass{VCandName}XqqCand_passPNetWMD0p5HP", f"pass{VCandName}XqqCand && pass{VCandName}PNetWMD0p5HP")
    #
    # Tau21
    #
    df = df.Define(f"pass{VCandName}Tau21HP", f"({VCandName}_tau21 < 0.35f)")
    df = df.Define(f"pass{VCandName}Tau21LP", f"({VCandName}_tau21 > 0.35f) && ({VCandName}_tau21 < 0.75f)")
    df = df.Define(f"pass{VCandName}Tau21NP", f"({VCandName}_tau21 >= 0.75f)")


    df = df.Define(f"{VCandName}_subjet1_Idx",      f"GetFromVec(SignalFatJet_subJetIdx1,{VCandIdx},-1)")
    df = df.Define(f"{VCandName}_subjet1_pt",       f"GetFromVec(SubJet_pt,{VCandName}_subjet1_Idx, -1.f)")
    df = df.Define(f"{VCandName}_subjet1_eta",      f"GetFromVec(SubJet_eta,{VCandName}_subjet1_Idx, -9.f)")
    df = df.Define(f"{VCandName}_subjet1_phi",      f"GetFromVec(SubJet_phi,{VCandName}_subjet1_Idx, -9.f)")
    df = df.Define(f"{VCandName}_subjet1_mass",     f"GetFromVec(SubJet_mass,{VCandName}_subjet1_Idx, -1.f)")
    df = df.Define(f"{VCandName}_subjet1_rawFactor",f"GetFromVec(SubJet_rawFactor,{VCandName}_subjet1_Idx, -1.f)")

    df = df.Define(f"{VCandName}_subjet2_Idx",      f"GetFromVec(SignalFatJet_subJetIdx2,{VCandIdx},-1)")
    df = df.Define(f"{VCandName}_subjet2_pt",       f"GetFromVec(SubJet_pt,{VCandName}_subjet2_Idx, -1.f)")
    df = df.Define(f"{VCandName}_subjet2_eta",      f"GetFromVec(SubJet_eta,{VCandName}_subjet2_Idx, -9.f)")
    df = df.Define(f"{VCandName}_subjet2_phi",      f"GetFromVec(SubJet_phi,{VCandName}_subjet2_Idx, -9.f)")
    df = df.Define(f"{VCandName}_subjet2_mass",     f"GetFromVec(SubJet_mass,{VCandName}_subjet2_Idx, -1.f)")
    df = df.Define(f"{VCandName}_subjet2_rawFactor",f"GetFromVec(SubJet_rawFactor,{VCandName}_subjet2_Idx, -1.f)")

    ##
    ## AK8 Jet Mass Cuts
    ###### OldDef: msoftdrop_def = f"VCand{VCandName}_msoftdrop"
    msoftdrop_def = f"{VCandName}_msoftdrop_corrAK8JEC"
    print(f"{msoftdrop_def=}")
    df = df.Define(f"{VCandName}_msoftdrop_forTag", msoftdrop_def)

    df = df.Define(f"pass{VCandName}Mass30To300", f"({VCandName}_msoftdrop_forTag<300.f) && ({VCandName}_msoftdrop_forTag>=30.f)") # Define loose cut
    df = df.Define(f"pass{VCandName}MassVCand",   f"({VCandName}_msoftdrop_forTag<105.f) && ({VCandName}_msoftdrop_forTag>=65.f)")
    df = df.Define(f"pass{VCandName}MassHCand",   f"({VCandName}_msoftdrop_forTag<135.f) && ({VCandName}_msoftdrop_forTag>=105.f)")
    df = df.Define(f"pass{VCandName}MassSB",      f"({VCandName}_msoftdrop_forTag>=135.f) || ({VCandName}_msoftdrop_forTag<65.f)")
    df = df.Define(f"pass{VCandName}MassSBHCand", f"pass{VCandName}MassSB || pass{VCandName}MassHCand")

    df = df.Define(f"pass{VCandName}PNetMass30To300", f"({VCandName}_particleNet_mass<300.f)  && ({VCandName}_particleNet_mass>=30.f)") # Define loose cut
    df = df.Define(f"pass{VCandName}PNetMassVCand",   f"({VCandName}_particleNet_mass<105.f)  && ({VCandName}_particleNet_mass>=65.f)")
    df = df.Define(f"pass{VCandName}PNetMassHCand",   f"({VCandName}_particleNet_mass<135.f)  && ({VCandName}_particleNet_mass>=105.f)")
    df = df.Define(f"pass{VCandName}PNetMassSB",      f"({VCandName}_particleNet_mass>=135.f) || ({VCandName}_particleNet_mass<65.f)")
    df = df.Define(f"pass{VCandName}PNetMassSBHCand", f"pass{VCandName}PNetMassSB || pass{VCandName}PNetMassHCand")

    if isMC:
      df = df.Define(f"{VCandName}_nBHadrons",     f"GetFromVec(SignalFatJet_nBHadrons,{VCandIdx},static_cast<unsigned char>(0))")
      df = df.Define(f"{VCandName}_nCHadrons",     f"GetFromVec(SignalFatJet_nCHadrons,{VCandIdx},static_cast<unsigned char>(0))")
      df = df.Define(f"{VCandName}_hadronFlavour", f"GetFromVec(SignalFatJet_hadronFlavour,{VCandIdx},-1)")

    return df

  df = ConstructVCand(df, "VCand0", "SignalFatJet0Idx")
  df = ConstructVCand(df, "VCand1", "SignalFatJet1Idx")

  if "VCandMassCut" in prod_tag:
    df = df.Define("passEventVCand0Mass", "passVCand0Mass30To300")
    df = df.Define("passEventVCand1Mass", "passVCand1Mass30To300")
    if not disableFilters:
      df = df.Filter("passEventVCand0Mass", "Cut_passEventVCand0Mass")
      df = df.Filter("passEventVCand1Mass", "Cut_passEventVCand1Mass")
  #==================================================
  #
  # VVCand selection
  #
  #==================================================
  df = df.Define("VVCand_p4", f"VCand0_p4+VCand1_p4")
  df = df.Define("VVCand_mass","float(VVCand_p4.M())")
  df = df.Define("VVCand_pt","float(VVCand_p4.Pt())")
  df = df.Define("VVCand_eta","float(VVCand_p4.Eta())")
  df = df.Define("VVCand_phi","float(VVCand_p4.Phi())")
  df = df.Define("passEventVVCandMass", "VVCand_mass >= 150.f")
  if not disableFilters:
    df = df.Filter("passEventVVCandMass", "Cut_EventVVCand")

  #==================================================
  #
  # Flavour labelling of the selected fatjet
  # Note 1: Do this here after VVCand mass cut.
  # Note 2: Don't do this for QCD samples.
  # Save disk space and computing time
  #
  #==================================================
  if isMC:
    df = NtupleMaker_Helpers_Gen.SetupFatJetGenFlavourLabels(df, isMC_QCD)

  #==================================================
  #
  # AK4 jets for VBF
  #
  #==================================================
  jet_pt_def   = "Jet_pt_nom"
  jet_mass_def = "Jet_mass_nom"
  if systVar == "SysAK4_Kin_jesTotalUp":
    jet_pt_def   = "Jet_pt_jesTotalUp"
    jet_mass_def = "Jet_mass_jesTotalUp"
  if systVar == "SysAK4_Kin_jesTotalDown":
    jet_pt_def   = "Jet_pt_jesTotalDown"
    jet_mass_def = "Jet_mass_jesTotalDown"
  if systVar == "SysAK4_Kin_jerUp":
    jet_pt_def   = "Jet_pt_jerUp"
    jet_mass_def = "Jet_mass_jerUp"
  if systVar == "SysAK4_Kin_jerDown":
    jet_pt_def   = "Jet_pt_jerDown"
    jet_mass_def = "Jet_mass_jerDown"
  print(f"{jet_pt_def=}")
  print(f"{jet_mass_def=}")

  df = df.Define("Jet_p4",                       f"Construct<FourVector>({jet_pt_def}, Jet_eta, Jet_phi, {jet_mass_def})")
  df = df.Define("Jet_p4_pt",                    "return Map(Jet_p4,[](const FourVector& v){return float(v.Pt());});")
  df = df.Define("Jet_p4_eta",                   "return Map(Jet_p4,[](const FourVector& v){return float(v.Eta());});")
  df = df.Define("Jet_p4_phi",                   "return Map(Jet_p4,[](const FourVector& v){return float(v.Phi());});")
  df = df.Define("Jet_p4_mass",                  "return Map(Jet_p4,[](const FourVector& v){return float(v.M());});")
  df = df.Define("Jet_passID",                   "Jet_jetId & (1<<1)") # Tight JetID
  # Note: For ULNanoAODv9 UL2016 APV and nonAPV, there is a bug where Tight and Loose WP cuts were
  # switched (https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_26/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L82-L101)
  # so the bit ordering has to be reversed
  # Use "Loose" PileUp ID WP. Note: Check back the exact pt definition to use.
  puIdBit = "0" if "UL16" in sampleName else "2"
  df = df.Define("Jet_passPUID",                    "return Map(Jet_p4_pt,Jet_puId,[](const float& pt, const int& puId){return pt > 50. ? true : puId&(1<<"+puIdBit+");});")
  df = df.Define("Jet_VCand0Clean",                 "not(IsOverlap(Jet_p4,VCand0_p4,1.0f))")
  df = df.Define("Jet_VCand1Clean",                 "not(IsOverlap(Jet_p4,VCand1_p4,1.0f))")
  df = df.Define("Jet_isCentral",                   "Jet_pt_nom > 30.f && abs(Jet_p4_eta) >= 0.0f && abs(Jet_p4_eta) < 2.4f && Jet_passID")
  df = df.Define("Jet_isForward",                   "Jet_pt_nom > 30.f && abs(Jet_p4_eta) >= 2.4f && abs(Jet_p4_eta) < 4.5f && Jet_passID")
  df = df.Define("Jet_isSignal",                    "(Jet_isCentral || Jet_isForward) && Jet_passPUID")
  df = df.Define("Jet_isPileUp",                    "(Jet_isCentral || Jet_isForward) && (!Jet_passPUID)")
  df = df.Define("Jet_isSignalJetForVBSTag",        "Jet_isSignal && Jet_VCand0Clean && Jet_VCand1Clean")
  df = df.Define("Jet_isPUJetForVBSTag",            "Jet_isPileUp && Jet_VCand0Clean && Jet_VCand1Clean")
  df = df.Define("Jet_isCentralSignalJetForVBSTag", "Jet_isSignalJetForVBSTag && Jet_isCentral")
  df = df.Define("Jet_isForwardSignalJetForVBSTag", "Jet_isSignalJetForVBSTag && Jet_isForward")
  df = df.Define("nCentralSignalJetForVBSTag",      "Sum(Jet_isCentralSignalJetForVBSTag)")
  df = df.Define("nForwardSignalJetForVBSTag",      "Sum(Jet_isForwardSignalJetForVBSTag)")
  if isMC:
    df = df.Define("Jet_gen_pt",   "GetFromAnotherCollection(Jet_genJetIdx,GenJet_pt,-1.f)")
    df = df.Define("Jet_gen_eta",  "GetFromAnotherCollection(Jet_genJetIdx,GenJet_eta,-9.f)")
    df = df.Define("Jet_gen_phi",  "GetFromAnotherCollection(Jet_genJetIdx,GenJet_phi,-9.f)")
    df = df.Define("Jet_gen_mass", "GetFromAnotherCollection(Jet_genJetIdx,GenJet_mass,-1.f)")

  #
  #
  #
  jet_signalforvbf_def = "Jet_isSignalJetForVBSTag==1"
  df = df.Define("nSignalJetForVBSTag",     f"Sum({jet_signalforvbf_def})")
  df = df.Define("SignalJetForVBSTag_p4",   f"Jet_p4[{jet_signalforvbf_def}]")
  df = df.Define("SignalJetForVBSTag_pt",   "return Map(SignalJetForVBSTag_p4,[](const FourVector& v){return float(v.Pt());});")
  df = df.Define("SignalJetForVBSTag_eta",  "return Map(SignalJetForVBSTag_p4,[](const FourVector& v){return float(v.Eta());});")
  df = df.Define("SignalJetForVBSTag_phi",  "return Map(SignalJetForVBSTag_p4,[](const FourVector& v){return float(v.Phi());});")
  df = df.Define("SignalJetForVBSTag_mass", "return Map(SignalJetForVBSTag_p4,[](const FourVector& v){return float(v.M());});")
  if isMC:
    df = df.Define("SignalJetForVBSTag_gen_pt",   f"Jet_gen_pt[{jet_signalforvbf_def}]")
    df = df.Define("SignalJetForVBSTag_gen_eta",  f"Jet_gen_eta[{jet_signalforvbf_def}]")
    df = df.Define("SignalJetForVBSTag_gen_phi",  f"Jet_gen_phi[{jet_signalforvbf_def}]")
    df = df.Define("SignalJetForVBSTag_gen_mass", f"Jet_gen_mass[{jet_signalforvbf_def}]")
  df = df.Define("hasDiJetTagCand",         "nSignalJetForVBSTag>=2")
  df = df.Define("hasJetTagCand",           "nSignalJetForVBSTag==1")

  df = df.Define("DiJetTagCand_comb_idx",             "hasDiJetTagCand ? Combinations(SignalJetForVBSTag_p4, 2) : RVec<RVec<std::size_t>>(); ")
  df = df.Define("DiJetTagCand_comb_j0_idx",          "hasDiJetTagCand ? DiJetTagCand_comb_idx[0] : RVec<std::size_t>();")
  df = df.Define("DiJetTagCand_comb_j1_idx",          "hasDiJetTagCand ? DiJetTagCand_comb_idx[1] : RVec<std::size_t>();")
  df = df.Define("DiJetTagCand_comb_j0_p4",           "hasDiJetTagCand ? Take(SignalJetForVBSTag_p4,DiJetTagCand_comb_j0_idx) : RVec<FourVector>();")
  df = df.Define("DiJetTagCand_comb_j1_p4",           "hasDiJetTagCand ? Take(SignalJetForVBSTag_p4,DiJetTagCand_comb_j1_idx) : RVec<FourVector>();")
  df = df.Define("DiJetTagCand_p4",                   "hasDiJetTagCand ? GeP4SumFromTwoVecsOfP4(DiJetTagCand_comb_j0_p4,DiJetTagCand_comb_j1_p4) : RVec<FourVector>();")
  df = df.Define("DiJetTagCand_p4_pt",                "hasDiJetTagCand ? GetPtFromVecP4(DiJetTagCand_p4) : RVec<float>();")
  df = df.Define("DiJetTagCand_p4_eta",               "hasDiJetTagCand ? GetEtaFromVecP4(DiJetTagCand_p4) : RVec<float>();")
  df = df.Define("DiJetTagCand_p4_phi",               "hasDiJetTagCand ? GetPhiFromVecP4(DiJetTagCand_p4) : RVec<float>();")
  df = df.Define("DiJetTagCand_p4_mass",              "hasDiJetTagCand ? GetMassFromVecP4(DiJetTagCand_p4) : RVec<float>();")
  df = df.Define("DiJetTagCand_deltaR",               "hasDiJetTagCand ? GeDeltaRFromTwoVecsOfP4(DiJetTagCand_comb_j0_p4,DiJetTagCand_comb_j1_p4) : RVec<float>();")
  df = df.Define("DiJetTagCand_deltaEta",             "hasDiJetTagCand ? GeDeltaEtaFromTwoVecsOfP4(DiJetTagCand_comb_j0_p4,DiJetTagCand_comb_j1_p4) : RVec<float>();")
  df = df.Define("VecIdxOfDiJetTagCandSortByMass",    "hasDiJetTagCand ? CustomArgsort(DiJetTagCand_p4_mass, sort_from_highest) : RVec<std::size_t>();")
  df = df.Define("IdxOfDiJetTagHighestMass",          "hasDiJetTagCand ? VecIdxOfDiJetTagCandSortByMass[0] : 0;")

  #
  #
  #
  df = df.Define("DiJetTag_pt",      "hasDiJetTagCand ? DiJetTagCand_p4_pt[IdxOfDiJetTagHighestMass]    : -1.f;")
  df = df.Define("DiJetTag_eta",     "hasDiJetTagCand ? DiJetTagCand_p4_eta[IdxOfDiJetTagHighestMass]   : -9.f;")
  df = df.Define("DiJetTag_phi",     "hasDiJetTagCand ? DiJetTagCand_p4_phi[IdxOfDiJetTagHighestMass]   : -9.f;")
  df = df.Define("DiJetTag_mass",    "hasDiJetTagCand ? DiJetTagCand_p4_mass[IdxOfDiJetTagHighestMass]  : -9.f;")
  df = df.Define("DiJetTag_deltaR",  "hasDiJetTagCand ? DiJetTagCand_deltaR[IdxOfDiJetTagHighestMass]   : -19.f;")
  df = df.Define("DiJetTag_deltaEta","hasDiJetTagCand ? DiJetTagCand_deltaEta[IdxOfDiJetTagHighestMass] : -19.f;")
  df = df.Define("DiJetTag_j0_idx",  "hasDiJetTagCand ? DiJetTagCand_comb_j0_idx[IdxOfDiJetTagHighestMass] : 0;")
  df = df.Define("DiJetTag_j1_idx",  "hasDiJetTagCand ? DiJetTagCand_comb_j1_idx[IdxOfDiJetTagHighestMass] : 0;")
  for j in ["j0","j1"]:
    df = df.Define(f"DiJetTag_{j}_pt",   f"hasDiJetTagCand ? SignalJetForVBSTag_pt[DiJetTag_{j}_idx]   : -1.f")
    df = df.Define(f"DiJetTag_{j}_eta",  f"hasDiJetTagCand ? SignalJetForVBSTag_eta[DiJetTag_{j}_idx]  : -9.f")
    df = df.Define(f"DiJetTag_{j}_phi",  f"hasDiJetTagCand ? SignalJetForVBSTag_phi[DiJetTag_{j}_idx]  : -9.f")
    df = df.Define(f"DiJetTag_{j}_mass", f"hasDiJetTagCand ? SignalJetForVBSTag_mass[DiJetTag_{j}_idx] : -1.f")
    if isMC:
      df = df.Define(f"DiJetTag_{j}_gen_pt",   f"SignalJetForVBSTag_gen_pt[DiJetTag_{j}_idx]")
      df = df.Define(f"DiJetTag_{j}_gen_eta",  f"SignalJetForVBSTag_gen_eta[DiJetTag_{j}_idx]")
      df = df.Define(f"DiJetTag_{j}_gen_phi",  f"SignalJetForVBSTag_gen_phi[DiJetTag_{j}_idx]")
      df = df.Define(f"DiJetTag_{j}_gen_mass", f"SignalJetForVBSTag_gen_mass[DiJetTag_{j}_idx]")
  #
  #
  #
  df = df.Define("JetTag_pt",   "hasJetTagCand ? SignalJetForVBSTag_pt[0]   : -1.f")
  df = df.Define("JetTag_eta",  "hasJetTagCand ? SignalJetForVBSTag_eta[0]  : -9.f")
  df = df.Define("JetTag_phi",  "hasJetTagCand ? SignalJetForVBSTag_phi[0]  : -9.f")
  df = df.Define("JetTag_mass", "hasJetTagCand ? SignalJetForVBSTag_mass[0] : -1.f")
  if isMC:
    df = df.Define("JetTag_gen_pt",   f"SignalJetForVBSTag_gen_pt[0]")
    df = df.Define("JetTag_gen_eta",  f"SignalJetForVBSTag_gen_eta[0]")
    df = df.Define("JetTag_gen_phi",  f"SignalJetForVBSTag_gen_phi[0]")
    df = df.Define("JetTag_gen_mass", f"SignalJetForVBSTag_gen_mass[0]")

  #
  # Define some event weights
  #
  df = df.Define("evtWeight_PU",                      "evtWeight * mcPUWeight" if isMC else "1.f")
  df = df.Define("evtWeight_PU_Prefire",              "evtWeight_PU * L1PreFiringWeight" if isMC else "1.f")
  #
  # Define sampleID. Give each sample a unique large integer number
  #
  sampleID = NtupleMaker_Helpers.MakeSampleID(sampleName)
  print(f"sampleID = {sampleID}")
  df = df.Define("sampleID", sampleID)

  #==================================================
  #
  # LHEScaleWeights
  #
  #==================================================
  # if isMC and isNominal:
  #   df = NtupleMaker_Helpers_Gen.MakeLHEScaleWeightBranches(df, sampleName)
  #   df = NtupleMaker_Helpers_Gen.MakeLHEPDFWeightBranches(df, sampleName)

  #==================================================
  #
  # SignalGenInfo
  #
  #==================================================
  # if isMCSignal:
  #   df = NtupleMaker_Helpers_Gen.SetupSignalGenInfo(df, sigSpin)

  ##########################################################################
  #
  #
  #
  #########################################################################
  #
  #
  #
  branchList = []
  branchList += [
    "sampleID","evtWeight",
  ]
  if isMC:
    branchList += [
      "evtWeight_PU", "evtWeight_PU_Prefire"
    ]
    branchList += [
      "mcXS","mcKFactor","mcGenWeight","mcSumOfWeight","eventWeightScale",
      "evtWeight_SystLumi_sfUp","evtWeight_SystLumi_sfDown",
      "mcPUWeight", "mcPUWeight_SystPU_sfUp", "mcPUWeight_SystPU_sfDown",
      "L1PreFiringWeight", "L1PreFiringWeight_SystL1PreFire_sfUp", "L1PreFiringWeight_SystL1PreFire_sfDown",
      "Pileup_nTrueInt"
    ]
  #
  #
  branchList += [
    "run","luminosityBlock","event", "nPVs","nPVsGood",
  ]
  branchList += trigPathAllFinal

  for VCandName in ["VCand0","VCand1"]:
    branchList += [
      f"{VCandName}_pt",f"{VCandName}_eta",f"{VCandName}_phi",f"{VCandName}_mass",f"{VCandName}_pt_nom",
      f"{VCandName}_msoftdrop", f"{VCandName}_msoftdrop_raw", f"{VCandName}_msoftdrop_corrAK8JEC",f"{VCandName}_particleNet_mass",
      f"{VCandName}_msoftdrop_forTag",f"{VCandName}_corr_jecNom",f"{VCandName}_corr_jec",
    ]
    if isMC:
      branchList += [f"{VCandName}_gen_pt",f"{VCandName}_gen_eta",f"{VCandName}_gen_phi",f"{VCandName}_gen_mass",
        f"{VCandName}_gen_msoftdrop",
      ]
    branchList += [
      f"{VCandName}_particleNetMD_Xqq",f"{VCandName}_particleNetMD_Xbb",f"{VCandName}_particleNetMD_Xcc",f"{VCandName}_particleNetMD_QCD",
      f"{VCandName}_particleNetMD_WvsQCD",f"{VCandName}_particleNetMD_XbbvsQCD",
      f"{VCandName}_tau21",
    ]

    branchList += [
      f"pass{VCandName}PreTag",
      f"pass{VCandName}PNetWMD2p5",f"pass{VCandName}PNetWMD1p0",f"pass{VCandName}PNetWMD0p5",f"pass{VCandName}PNetWMD2p5NP",
      f"pass{VCandName}PNetWMD2p5LP",f"pass{VCandName}PNetWMD1p0LP",f"pass{VCandName}PNetWMD0p5LP",
      f"pass{VCandName}PNetWMD2p5HP",f"pass{VCandName}PNetWMD1p0HP",f"pass{VCandName}PNetWMD0p5HP",
    ]

    branchList += [
      f"pass{VCandName}PNetXbbMD",f"pass{VCandName}PNetXbbMDNP",f"pass{VCandName}PNetXbbMDHP",f"pass{VCandName}PNetXbbMDLP",
      f"pass{VCandName}XbbCand",f"pass{VCandName}XqqCand",
      f"pass{VCandName}XbbCand_passPNetXbbMDNP",f"pass{VCandName}XbbCand_passPNetXbbMDLP",f"pass{VCandName}XbbCand_passPNetXbbMDHP",
      f"pass{VCandName}XqqCand_passPNetWMD2p5NP",
      f"pass{VCandName}XqqCand_passPNetWMD2p5LP",f"pass{VCandName}XqqCand_passPNetWMD1p0LP",f"pass{VCandName}XqqCand_passPNetWMD0p5LP",
      f"pass{VCandName}XqqCand_passPNetWMD2p5HP",f"pass{VCandName}XqqCand_passPNetWMD1p0HP",f"pass{VCandName}XqqCand_passPNetWMD0p5HP",
      f"pass{VCandName}Tau21HP",f"pass{VCandName}Tau21LP",f"pass{VCandName}Tau21NP",
    ]
    branchList += [
      f"{VCandName}_subjet1_pt",f"{VCandName}_subjet1_eta",f"{VCandName}_subjet1_phi",f"{VCandName}_subjet1_mass",
      f"{VCandName}_subjet1_rawFactor",
      f"{VCandName}_subjet2_pt",f"{VCandName}_subjet2_eta",f"{VCandName}_subjet2_phi",f"{VCandName}_subjet2_mass",
      f"{VCandName}_subjet2_rawFactor",
    ]
    branchList += [
      f"pass{VCandName}Mass30To300",f"pass{VCandName}MassVCand",f"pass{VCandName}MassHCand",f"pass{VCandName}MassSB",f"pass{VCandName}MassSBHCand",
      f"pass{VCandName}PNetMass30To300",f"pass{VCandName}PNetMassVCand",f"pass{VCandName}PNetMassHCand",f"pass{VCandName}PNetMassSB",f"pass{VCandName}PNetMassSBHCand",
    ]
    if isMC:
      branchList += [
        f"{VCandName}_nBHadrons",f"{VCandName}_nCHadrons",f"{VCandName}_hadronFlavour",
      ]
  #
  #
  #
  #
  branchList += [
    "VVCand_mass","VVCand_pt","VVCand_eta","VVCand_phi","nSignalJetForVBSTag","IdxOfDiJetTagHighestMass",
  ]
  branchList += [
    "DiJetTag_pt", "DiJetTag_eta","DiJetTag_phi","DiJetTag_mass","DiJetTag_deltaR","DiJetTag_deltaEta",
  ]
  for j in ["j0","j1"]:
    branchList += [
      f"DiJetTag_{j}_idx",f"DiJetTag_{j}_pt",f"DiJetTag_{j}_eta",f"DiJetTag_{j}_phi",f"DiJetTag_{j}_mass",
    ]
    if isMC:
      branchList += [
        f"DiJetTag_{j}_gen_pt",f"DiJetTag_{j}_gen_eta",f"DiJetTag_{j}_gen_phi",f"DiJetTag_{j}_gen_mass",
      ]

  branchList += [
    "JetTag_pt","JetTag_eta","JetTag_phi","JetTag_mass",
  ]
  if isMC:
    branchList += [
      "JetTag_gen_pt","JetTag_gen_eta","JetTag_gen_phi","JetTag_gen_mass",
    ]

  if isMC and not(isMC_QCD):
   branchList +=  NtupleMaker_Helpers_Gen.ListOfFatJetGenFlavourLabels(isNominal=True)

  #### if isMCSignal:
  ####   branchList += NtupleMaker_Helpers_Gen.ListOfSignalGenInfo()

  ##
  ## Uncomment these lines if you want to store the entire GenPart
  ##
  if ("AddGenPart" in prod_tag) and isNominal: # TEMP
    branchList +=[
      "nGenPart","GenPart_pt","GenPart_eta","GenPart_phi","GenPart_mass",
      "GenPart_pdgId","GenPart_status","GenPart_statusFlags",
      "GenPart_genPartIdxMother"
    ]

  branchVec = ROOT.vector('string')()
  for branchName in branchList:
    branchVec.push_back(branchName)

  #========================================================
  #
  # Snapshot each dataframe
  # Things to read with regards to snapshot:
  # https://root-forum.cern.ch/t/some-problem-with-lazy-snapshots-in-rdataframe/46740
  #
  #========================================================
  # Need these  to trigger lazy action
  df_count = df.Count()

  outTreeName = "TreeVVqqqq"
  if not isNominal: outTreeName += f"_{systVar}"

  outFileTreePathTemp = f"{TMPDIR}/"
  outFileTreePathTemp += f"Ntuple_{sampleName}_{outTreeName}"
  outFileTreePathTemp += ".root"

  rdf_opts = ROOT.RDF.RSnapshotOptions(); rdf_opts.fLazy = True
  df = df.Snapshot(outTreeName, outFileTreePathTemp, branchVec, rdf_opts)
  #
  #
  #
  outFileTreePathTempList = [outFileTreePathTemp]
  #========================================================
  #
  # This will trigger lazy actions
  #
  #========================================================
  # cutReport = df.Report();
  print("=========================================================")

  ncount_VVqqqq = df_count.GetValue()
  print("Number of entries for each output tree:")
  print(f"ncount_VVqqqq = {ncount_VVqqqq:d}")

  # cutReport.Print()
  # print(str(df.GetNRuns()))
  ####################################################################
  #
  # Exiting
  #
  ####################################################################
  timer.Stop()
  timer.Print()
  print(f"NtupleMaker::MakeNtuple():Done sample:{sampleName},sys:{systVar}")

  del df
  del timer

  return outFileTreePathTempList

def MergeAndTransferNtuplesToEOS(outFileTreePathTempList, sampleName, doSystVarTrees=False):
  #========================================================
  #
  # Merge the trees by channels (+ systVars) root files.
  #
  #========================================================
  print("=========================================================")
  outFileTreeName = f"Ntuple_{sampleName}"
  if doSystVarTrees:
    outFileTreeName = f"NtupleSyst_{sampleName}"
  outFileTreeName += ".root"

  outFileTreePathTemp = f"{TMPDIR}/{outFileTreeName}"
  print(f"Temporary output Tree file: {outFileTreePathTemp}")

  #
  # hadd the files
  #
  print("Hadd local temporary files:")
  for path in outFileTreePathTempList: print(path)

  command = ["hadd", "-f", outFileTreePathTemp]
  command += outFileTreePathTempList
  subprocess.run(command)

  #
  # Delete the temporary channel root files
  #
  print("=========================================================")
  print(f"Deleting local temporary files:")
  for path in outFileTreePathTempList:print(path)

  command = ["rm", "-fv"]
  command += outFileTreePathTempList
  subprocess.run(command)

  #========================================================
  #
  # Copy the merged root file to EOS and delete in the tmp
  # directory
  #
  #========================================================
  outDirTrees = outDirNominalTrees
  if doSystVarTrees: outDirTrees = outDirSystTrees

  outFileTreePathFinal = None
  if "/eos/user" in outDirTrees:outFileTreePathFinal = EOSUSER+outDirTrees
  elif "/eos/cms" in outDirTrees: outFileTreePathFinal = EOSCMS+outDirTrees
  else: outFileTreePathFinal = outDirTrees
  outFileTreePathFinal += outFileTreeName

  print(f"{outFileTreePathFinal=}")
  print("=========================================================")
  print(f"Copying tree file to final destination directory: {outDirTrees}")
  command = ["xrdcp", "-f", outFileTreePathTemp, outFileTreePathFinal]
  subprocess.run(command)

  print("=========================================================")
  print(f"Deleting local temporary file: {outFileTreePathTemp}")
  command = ["rm", "-fv", outFileTreePathTemp]
  subprocess.run(command)

  print("=========================================================")
  print(f"Test opening tree file : {outFileTreePathFinal}")
  finalFile = ROOT.TFile.Open(outFileTreePathFinal)
  if finalFile:
    print("Tree file okay")
    finalFile.Close()
  else:
    print("Tree file unable to open. Please check!")

if __name__ == "__main__":
  main()