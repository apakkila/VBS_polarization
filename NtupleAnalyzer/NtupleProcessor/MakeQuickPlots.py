#!/usr/bin/env python
import os
import glob
import collections
import copy
import itertools
import argparse
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gROOT.LoadMacro("./tdrStyle.C")
ROOT.gROOT.ProcessLine("setTDRStyle();")
from helpers import *

class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

EOSURL     = "root://eosuser.cern.ch/"
# path_inDir = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuples/"
path_inDir = "/eos/user/n/nbinnorj/VBSAllHadAna/MergedNtuples_VCandMassCut/"

ncores=4
ROOT.ROOT.EnableImplicitMT(ncores)

####################################################
#
#
#
######################################################
def main():

  parser = argparse.ArgumentParser("")
  parser.add_argument('--era', dest='era', type=str, required=True)
  args = parser.parse_args()
  era = args.era

  if era  == "UL17":
    yearStr = "UL2017" 
    lumiStr = "41.5"
  elif era  == "UL18":
    yearStr = "UL2018"
    lumiStr = "59.8"
  elif era  == "UL16NonAPV":
    yearStr = "UL2016late"
    lumiStr = "16.8"
  elif era  == "UL16APV":
    yearStr = "UL2016early"
    lumiStr = "19.5"
  else:
    raise Exception(f"Unrecognized era: {era}. Please check!")

  MakeValidation(era,yearStr,lumiStr)

def MakeValidation(era,yearStr,lumiStr):

  samples = MyDict()
  samples["QCD"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_QCD_HT.root",
    ],
  }
  samples["VJets"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_VJetsToQQ.root"
    ],
  }
  samples["TOP"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_TOP.root"
    ],
  }
  samples["VBF"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_VBF.root"
    ],
  }
  samples["MultiV"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_VV_NLO.root",
      path_inDir+"MergedNtuple_MCUL17_VVV_NLO.root",
    ],
  }
  samples["VBS"] = {
    "files" : [
      path_inDir+"MergedNtuple_MCUL17_VBS_WW_EWK.root",
      path_inDir+"MergedNtuple_MCUL17_VBS_WW_QCD.root",
      path_inDir+"MergedNtuple_MCUL17_VBS_WZ.root",
      path_inDir+"MergedNtuple_MCUL17_VBS_ZZ.root",
    ],
  }
  samples["Data"] = {
    "files": [path_inDir+"MergedNtuple_DataUL17.root"],
  }

  colorsDict = {
    "QCD"   : ROOT.kGreen,
    "VJets" : ROOT.kViolet,
    "TOP"   : ROOT.kOrange,
    "VBF"   : ROOT.kBlue,
    "MultiV": ROOT.kMagenta,
    "VBS"   : ROOT.kRed,
    "Data"  : ROOT.kBlack
  }

  sampleNames = samples.keys()

  mcList = ["QCD","VJets","TOP","VBF","MultiV"]
  mcListFinal = ["QCD","VJets","TOP","VBF","MultiV"]


  ####################################################
  #
  #
  #
  ######################################################
  histoInfos = MyDict()
  histoInfos["VVCand_mass"] = {
    "branch": "VVCand_mass",
    "model": ROOT.RDF.TH1DModel("h_VVCand_mass", "", 100, 0., 10000.),
    "doLogy": True,
    "xaxistitle": "mVV [GeV]",
  }
  histoInfos["VCand0_pt"] = {
    "branch": "VCand0_pt",
    "model": ROOT.RDF.TH1DModel("h_VCand0_pt", "",   60, 0., 6000.),
    "doLogy": True,
    "xaxistitle": "VCand0 pT [GeV]",
  }
  histoInfos["VCand0_eta"] = {
    "branch": "VCand0_eta",
    "model": ROOT.RDF.TH1DModel("h_VCand0_eta", "",   120, -3., 3.),
    "doLogy": False,
    "xaxistitle": "VCand0 #eta",
  }
  histoInfos["VCand0_msoftdrop_forTag"] = {
    "branch": "VCand0_msoftdrop_forTag",
    "model": ROOT.RDF.TH1DModel("h_VCand0_msoftdrop_forTag", "",  40, 0., 400.),
    "doLogy": True,
    "xaxistitle": "VCand0 softdrop mass [GeV]",
  }
  histoInfos["VCand0_particleNetMD_WvsQCD"] = {
    "branch": "VCand0_particleNetMD_WvsQCD",
    "model": ROOT.RDF.TH1DModel("h_VCand0_particleNetMD_WvsQCD", "",  50, 0., 1.),
    "doLogy": True,
    "xaxistitle": "VCand0 ParticleNetMD WvsQCD",
  }
  histoInfos["VCand1_pt"] = {
    "branch": "VCand1_pt",
    "model": ROOT.RDF.TH1DModel("h_VCand1_pt", "",   60, 0., 6000.),
    "doLogy": True,
    "xaxistitle": "VCand1 pT [GeV]",
  }
  histoInfos["VCand1_eta"] = {
    "branch": "VCand1_eta",
    "model": ROOT.RDF.TH1DModel("h_VCand1_eta", "",   120, -3., 3.),
    "doLogy": False,
    "xaxistitle": "VCand1 #eta",
  }
  histoInfos["VCand1_msoftdrop_forTag"] = {
    "branch": "VCand1_msoftdrop_forTag",
    "model": ROOT.RDF.TH1DModel("h_VCand1_msoftdrop_forTag", "",  40, 0., 400.),
    "doLogy": True,
    "xaxistitle": "VCand1 softdrop mass [GeV]",
  }
  histoInfos["VCand1_particleNetMD_WvsQCD"] = {
    "branch": "VCand1_particleNetMD_WvsQCD",
    "model": ROOT.RDF.TH1DModel("h_VCand1_particleNetMD_WvsQCD", "",  50, 0., 1.),
    "doLogy": True,
    "xaxistitle": "VCand1 ParticleNetMD WvsQCD",
  }

  histoInfos["DiJetTag_mass"] = {
    "branch": "DiJetTag_mass",
    "model": ROOT.RDF.TH1DModel("h_DiJetTag_mass", "",  100, 0., 10000.),
    "doLogy": True,
    "xaxistitle": "DiJetTag_mass",
  }
  histoInfos["DiJetTag_absdeltaEta"] = {
    "branch": "DiJetTag_absdeltaEta",
    "model": ROOT.RDF.TH1DModel("h_DiJetTag_absdeltaEta", "",  100, 0., 10.),
    "doLogy": True,
    "xaxistitle": "DiJetTag_absdeltaEta",
  }


  ####################################################
  #
  #
  #
  ######################################################
  inTrees = MyDict()

  for sample in samples:
    inTrees[sample] = ROOT.TChain("TreeVVqqqq")
    for file in samples[sample]["files"]:
      print(file)
      inTrees[sample].Add(EOSURL+file)

  # inTrees["TotalMC"] = ROOT.TChain("TreeVVqqqq")
  # for mc in mcList:
  #   inTrees["TotalMC"].Add(inTrees[mc])

  def ApplyBaselineSelection(df, era, isMC=True):
    df = df.Filter("nSignalJetForVBSTag>=2 && passVCand0MassSBHCand && passVCand1MassSBHCand")
    df = df.Define("DiJetTag_absdeltaEta","TMath::Abs(DiJetTag_deltaEta)")
    return df

  def ApplyWeights(df, selLevel="Baseline", isMC=True):
    if isMC:
      if "Baseline" in selLevel and not(df.HasColumn("evtWeight_Baseline")):
        df = df.Define("evtWeight_Baseline", "evtWeight")
    elif not(isMC) and not(df.HasColumn("evtWeight")):
      df = df.Define("evtWeight", "1.")

    return df

  ####################################################
  #
  #
  #
  ######################################################
  df = MyDict()
  df_counts = MyDict()

  #====================================
  #
  # Data
  #
  #====================================
  df["Data"]["Initial"]        = ROOT.RDataFrame(inTrees["Data"])
  ROOT.RDF.Experimental.AddProgressBar(df["Data"]["Initial"])

  df["Data"]["Baseline"]        = ApplyBaselineSelection(df["Data"]["Initial"], era, isMC=False)
  df_counts["Data"]["Baseline"] = df["Data"]["Baseline"].Count()
  #====================================
  #
  # MC
  #
  #====================================

  for sample in mcList:
    df[sample]["Initial"] = ROOT.RDataFrame(inTrees[sample])
    ROOT.RDF.Experimental.AddProgressBar(df[sample]["Initial"])
    #
    #
    #
    df[sample]["Baseline"] = ApplyBaselineSelection(df[sample]["Initial"], era, isMC=True)
    df[sample]["Baseline"] = ApplyWeights(df[sample]["Baseline"], selLevel="Baseline", isMC=True)
    df_counts[sample]["Baseline"] = df[sample]["Baseline"].Sum("evtWeight_Baseline")

  cutNames = [
    "Baseline",
  ]

  histograms = MyDict()
  histo1D = MyDict()
  for sample in mcListFinal+["Data"]:
    for cut in cutNames:
      for hist in histoInfos:
        hModelTemp = copy.copy(histoInfos[hist]["model"])
        hModelTemp.fName = f"{sample}_{cut}_{histoInfos[hist]['model'].fName}"
        if "Data" in sample:
          histo1D[sample][cut][hist] = df[sample][cut].Histo1D(hModelTemp,histoInfos[hist]["branch"])
        else:
          if "Baseline" in cut: weightName = "evtWeight_Baseline"
          histo1D[sample][cut][hist] = df[sample][cut].Histo1D(hModelTemp,histoInfos[hist]["branch"], weightName)

  #
  # Print out Baseline yields
  #
  print("Baseline")
  for sample in mcListFinal+["Data"]:
    print(f"Trigger Lazy Action for sample = {sample}")
    nevts = df_counts[sample]["Baseline"].GetValue()
    print(f"{sample}:{nevts}")

  #
  # Get histograms
  #
  for sample in mcListFinal+["Data"]:
    for cut in cutNames:
      for hist in histoInfos:
        histograms[sample][cut][hist] = histo1D[sample][cut][hist].GetValue()

  ######################################################
  #
  # Make the plots
  #
  ######################################################
  outDir="./plots_VBSAllHad/"

  def MakePlot(histograms, histoInfos, cutName="", histoName="", dataName="", mcList=[], year="", lumi="", outDir=""):
    mcListTemp = list(mcList)
    #
    #
    xLat,yLat = 0.25, 0.91
    xLeg,yLeg = xLat + 0.30, yLat
    leg_h =  0.03 * len(mcListTemp)
    leg = ROOT.TLegend( xLeg, yLeg - leg_h, xLeg + 0.35, yLeg )
    leg.SetNColumns( 2 )
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetTextFont( 43 )
    leg.SetTextSize( 18 )
    #
    #
    #
    h_data  = histograms[dataName][cutName][histoName]
    h_dataC = h_data.Clone(dataName+"_"+cutName+"_"+h_data.GetName())
    h_dataC.SetMarkerColor(ROOT.kBlack)
    h_dataC.SetBinErrorOption(ROOT.TH1.kPoisson)
    #
    #
    #
    histosTemp = {}
    stack_mc = ROOT.THStack("stack_"+histoName+"_"+cutName, histoName+"_"+cutName)
    for mc in mcListTemp:
      h  = histograms[mc][cutName][histoName]
      hC = h.Clone(f"{mc}_{cutName}_{h.GetName()}")
      hC.SetLineColor(ROOT.kBlack)
      hC.SetLineWidth(2)
      hC.SetFillColor(colorsDict[mc])
      stack_mc.Add(hC)
      histosTemp[mc] = hC
    h_mc_totalC = stack_mc.GetStack().Last().Clone(f"{histoName}_{cutName}_TotalMC")
    #
    #
    #
    leg.AddEntry(h_dataC,"Data","p")
    mcListTemp.reverse()
    for mc in mcListTemp:
      leg.AddEntry(histosTemp[mc],mc,"f")

    xaxistitle = histoInfos[histoName]["xaxistitle"]
    yaxistitle = "Events"

    if not os.path.exists(outDir):
      os.makedirs(outDir)
    pdfName= f"{outDir}h_{year}_{cutName}_{histoName}"
    PlotDataMC(f"h_{cutName}_{histoName}", stack_mc, h_dataC, h_mc_totalC, leg, xaxistitle, yaxistitle, year, lumi, histoInfos[histoName]["doLogy"],pdfName)

  #
  #
  #
  mcListFinalReverse = mcListFinal.copy()
  mcListFinalReverse.reverse()
  for cutName in cutNames:
    for hInfo in histoInfos:
      MakePlot(histograms, histoInfos, cutName, hInfo, "Data", mcListFinalReverse, yearStr, lumiStr, outDir)

if __name__ == '__main__':
  main()