import ROOT
ROOT.gROOT.SetBatch()

def GetYears(sampleName):
  eraName = ""
  triggerYear = ""
  corrlibEra = ""
  isMC = 1 if "MC" in sampleName else 0
  if "MCUL16APV" in sampleName or "DataUL16APV" in sampleName:
    eraName     = "UL16APV"
    triggerYear = "2016"
    corrlibEra  = "2016preVFP_UL"
  elif "MCUL16PostAPV" in sampleName or "DataUL16PostAPV" in sampleName:
    eraName     = "UL16PostAPV"
    triggerYear = "2016"
    corrlibEra  = "2016postVFP_UL"
  elif "MCUL17" in sampleName or "DataUL17" in sampleName:
    eraName     = "UL17"
    triggerYear = "2017"
    corrlibEra  = "2017_UL"
  elif "MCUL18" in sampleName or "DataUL18" in sampleName:
    eraName     = "UL18"
    triggerYear = "2018"
    corrlibEra  = "2018_UL"
  else:
    raise Exception(f"Cannot figure out eraName for sample: {sampleName}")

  return eraName, triggerYear, corrlibEra, isMC

def SetupCorrectionLibForAK8Tagging(corrlibEra):

  ak8_jmar_json=f"\"/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/{corrlibEra}/jmar.json.gz\""
  ROOT.gInterpreter.Declare(f'std::unique_ptr<correction::CorrectionSet> cset_ak8_jmar = correction::CorrectionSet::from_file({ak8_jmar_json});')
  ROOT.gInterpreter.Declare('auto cset_ak8_PNetWMD_SF = cset_ak8_jmar->at("ParticleNet_W_MD");')

  code_header = '''
RVec<RVec<RVec<float>>> GetAK8PNetWMDSFsSysts(const RVec<float>& pt, const RVec<float>& eta){
  int nSF = 2; int nSyst = 3;
  RVec<RVec<RVec<float>>> rvec_rvec_rvec_sf(nSF, RVec<RVec<float>>(pt.size(), RVec<float>(nSyst, 1.f)));
  for (size_t i = 0; i < pt.size(); i++) {
    if (pt[i] < 200.f or pt[i] >= 800.f) continue;
    rvec_rvec_rvec_sf[0][i][0] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"nom\",  \"2p5\"});
    rvec_rvec_rvec_sf[0][i][1] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"up\",   \"2p5\"});
    rvec_rvec_rvec_sf[0][i][2] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"down\", \"2p5\"});
    //
    //
    //
    rvec_rvec_rvec_sf[1][i][0] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"nom\",  \"0p5\"});
    rvec_rvec_rvec_sf[1][i][1] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"up\",   \"0p5\"});
    rvec_rvec_rvec_sf[1][i][2] = cset_ak8_PNetWMD_SF->evaluate({eta[i], pt[i], \"down\", \"0p5\"});
  }
  return rvec_rvec_rvec_sf;
}
'''
  ROOT.gInterpreter.Declare(code_header)

#====================================================
#
# ParticleNetMD cut values
#
#====================================================
ParticleNetWvsQCDMDCut = dict()
# https://indico.cern.ch/event/1152827/#4-particlenet-sf-ul
# https://twiki.cern.ch/twiki/bin/view/CMS/ParticleNetSFs
ParticleNetWvsQCDMDCut["UL16APV"] = {
  "2p5": "0.6400f",
  "1p0": "0.8500f",
  "0p5": "0.9100f",
}
ParticleNetWvsQCDMDCut["UL16PostAPV"] = {
  "2p5": "0.6400f",
  "1p0": "0.8400f",
  "0p5": "0.9100f",
}
ParticleNetWvsQCDMDCut["UL17"] = {
  "2p5": "0.5800f",
  "1p0": "0.8100f",
  "0p5": "0.8900f",
}
ParticleNetWvsQCDMDCut["UL18"] = {
  "2p5": "0.5900f",
  "1p0": "0.8200f",
  "0p5": "0.9000f",
}

#====================================================
#
# Integrated lumi in inverse picobarns
# Unit: Inverse Picobarns
#
#====================================================
lumi_Dict = dict()
lumi_Dict["UL16APV"] = "19521.22f"
lumi_Dict["UL16PostAPV"] = "16812.15f"
lumi_Dict["UL17"] = "41479.681f"
lumi_Dict["UL18"] = "59832.47f"

lumiUp_Dict = dict()
lumiUp_Dict["UL16APV"] = "(1.f + 0.012f)*"+lumi_Dict["UL16APV"]
lumiUp_Dict["UL16PostAPV"] = "(1.f + 0.012f)*"+lumi_Dict["UL16PostAPV"]
lumiUp_Dict["UL17"] = "(1.f + 0.023f)*"+lumi_Dict["UL17"]
lumiUp_Dict["UL18"] = "(1.f + 0.025f)*"+lumi_Dict["UL18"]

lumiDown_Dict = dict()
lumiDown_Dict["UL16APV"] = "(1.f - 0.012f)*"+lumi_Dict["UL16APV"]
lumiDown_Dict["UL16PostAPV"]    = "(1.f - 0.012f)*"+lumi_Dict["UL16PostAPV"]
lumiDown_Dict["UL17"] = "(1.f - 0.023f)*"+lumi_Dict["UL17"]
lumiDown_Dict["UL18"] = "(1.f - 0.025f)*"+lumi_Dict["UL18"]
#====================================================
#
# CROSS-SECTIONS FOR MC SAMPLES
# Unit: picobarns
#
#====================================================
xs_Dict = dict()

BR_H_bb = 0.5824
BR_W_qq = 0.6741
BR_Z_qq = 0.6991

eraYears =[
  "MCUL16APV",
  "MCUL16PostAPV",
  "MCUL17",
  "MCUL18",
]

for year in eraYears:
  #************************
  #
  # VBS samples
  #
  # From SMP-21-012 (Run2 SM VBS All-hadronic):
  # https://cms.cern.ch/iCMS/analysisadmin/cadilines?id=2486&ancode=SMP-21-012&tp=an&line=SMP-21-012
  # AnaNote: AN2020_083_v4.pdf
  #
  #************************
  #
  # VBS WW (EWK, QCD)
  #
  xs_Dict[year+"_VBS_WWSSTo4J_EWK"] = 0.1249
  xs_Dict[year+"_VBS_WWSSTo4J_QCD"] = 0.1087
  xs_Dict[year+"_VBS_WWOSTo4J_EWK"] = 1.8930
  xs_Dict[year+"_VBS_WWOSTo4J_QCD"] = 160.1
  #
  # VBS ZW (EWK, QCD)
  #
  xs_Dict[year+"_VBS_ZWTo4J_EWK"] = 0.1663
  xs_Dict[year+"_VBS_ZWTo4J_QCD"] = 4.2340
  xs_Dict[year+"_VBS_ZWTo2B2J_EWK"] = 0.123
  xs_Dict[year+"_VBS_ZWTo2B2J_QCD"] = 1.261
  xs_Dict[year+"_VBS_ZWTo2JnoB2J_QCD"] = 4.733
  #
  # VBS ZZ (EWK, QCD)
  #
  xs_Dict[year+"_VBS_ZZTo4J_QCD"] = 1.0840
  #
  # VBS VV (EWK+QCD)
  #
  xs_Dict[year+"_VBS_WWSSTo4J_EWK_QCD"] = 0.2421
  xs_Dict[year+"_VBS_WWOSTo4J_EWK_QCD"] = 161.4
  xs_Dict[year+"_VBS_ZWTo2B2J_EWK_QCD"] = 1.385
  xs_Dict[year+"_VBS_ZWTo4J_EWK_QCD"] = 4.405
  xs_Dict[year+"_VBS_ZZTo4J_EWK_QCD"] = 1.136
  xs_Dict[year+"_VBS_ZWTo2JnoB2J_EWK_QCD"] = 5.19
  #
  # VBS VV (aQGC)
  #
  xs_Dict[year+"_VBS_aQGC_WWOSTo4J"] = 9.701
  xs_Dict[year+"_VBS_aQGC_WWSSmTo4J"] = 0.1306
  xs_Dict[year+"_VBS_aQGC_WWSSpTo4J"] = 0.9043
  xs_Dict[year+"_VBS_aQGC_ZZTo2JnoB2J"] = 0.9258
  xs_Dict[year+"_VBS_aQGC_ZZTo4J"] = 2.423

  #************************
  #
  # QCD
  #
  #************************
  xs_Dict[year+"_QCD_HT50to100"]    = 185900000.0
  xs_Dict[year+"_QCD_HT100to200"]   = 23630000.0
  xs_Dict[year+"_QCD_HT200to300"]   = 1551000.0
  xs_Dict[year+"_QCD_HT300to500"]   = 324600.0
  xs_Dict[year+"_QCD_HT500to700"]   = 30350.0
  xs_Dict[year+"_QCD_HT700to1000"]  = 6437.0
  xs_Dict[year+"_QCD_HT1000to1500"] = 1118.0
  xs_Dict[year+"_QCD_HT1500to2000"] = 108.0
  xs_Dict[year+"_QCD_HT2000toInf"]  = 22.04

  #************************
  #
  # V->qq + jets
  #
  #************************
  xs_Dict[year+"_WJetsToQQ_HT-200to400"] = 2565.0
  xs_Dict[year+"_WJetsToQQ_HT-400to600"] = 277.2
  xs_Dict[year+"_WJetsToQQ_HT-600to800"] = 59.1
  xs_Dict[year+"_WJetsToQQ_HT-800toInf"] = 28.75
  xs_Dict[year+"_ZJetsToQQ_HT-200to400"] = 1013.0
  xs_Dict[year+"_ZJetsToQQ_HT-400to600"] = 114.1
  xs_Dict[year+"_ZJetsToQQ_HT-600to800"] = 25.35
  xs_Dict[year+"_ZJetsToQQ_HT-800toInf"] = 12.92

  #************************
  #
  # TOP samples
  #
  #************************
  # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO#Top_quark_pair_cross_sections_at
  # //BR for W-boson from PDG(2018)
  xs_Dict[year+"_TT_2L"] = 831.76*(3*0.1086)*(3*0.1086)
  xs_Dict[year+"_TT_1L"] = 831.76*2*(3*0.1086*0.6741)
  xs_Dict[year+"_TT_0L"] = 831.76*(0.6741)*(0.6741)
  # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_t_channel_cross_secti
  xs_Dict[year+"_ST_tchan_top"]     = 136.02
  xs_Dict[year+"_ST_tchan_antitop"] = 80.95
  # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt_channel_cross_sect
  # 71.7 pb is the total tW cross-section for top+anti-top.
  # xs for (top/antitop) = 35.85
  xs_Dict[year+"_ST_tW_top"]     = 35.85
  xs_Dict[year+"_ST_tW_antitop"] = 35.85
  # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_s_channel_cross_secti
  xs_Dict[year+"_ST_schan_hadronicDecays"] = 10.32*0.6741

  #************************
  #
  # VV samples
  #
  #************************
  xs_Dict[year+"_WWTo4Q"] = 51.54
  xs_Dict[year+"_ZZTo4Q"] = 3.306
  xs_Dict[year+"_WWTo1L1Nu2Q"] = 50.92
  xs_Dict[year+"_WZTo2Q2L"] = 6.331
  xs_Dict[year+"_ZZTo2Q2L"] = 3.688

  xs_Dict[year+"_WW"] = 75.95
  xs_Dict[year+"_WZ"] = 27.59
  xs_Dict[year+"_ZZ"] = 12.17

  xs_Dict[year+"_WWW"] = 0.2158
  xs_Dict[year+"_WWZ"] = 0.1707
  xs_Dict[year+"_WZZ"] = 0.05709
  xs_Dict[year+"_ZZZ"] = 0.01476

  #************************
  #
  # VBF EWK-W/Z
  #
  #************************
  xs_Dict[year+"_EWKWminus2Jets_WToQQ"] = 19.19
  xs_Dict[year+"_EWKWplus2Jets_WToQQ"] = 28.72
  xs_Dict[year+"_EWKWminus2Jets_WToQQ"] = 9.792

def GetSampleEventSumOfWeights(sampleRunsFiles):
  #########################################
  #
  # Get sample sum of event weights from
  # Runs TTree. Using a simple pyroot
  # event looping. Should be quick
  #
  #########################################
  genEventCount = 0
  genEventSumw = 0
  treeRuns = ROOT.TChain("Runs")
  for file in sampleRunsFiles: treeRuns.Add(file)
  nEventsRuns = treeRuns.GetEntries()

  for i in range(0, nEventsRuns):
    event = treeRuns.GetEntry(i)
    genEventCount += treeRuns.genEventCount
    genEventSumw  += treeRuns.genEventSumw

  print (f"genEventCount: {genEventCount}")
  print (f"genEventSumw: {genEventSumw}")

  return genEventSumw, genEventCount

def MakeSampleID(sampleName):
  year="2000"
  ID="000"
  #
  # For DATA
  #
  if "DataUL" in sampleName:
    if   "DataUL16APVB" in sampleName: year = "21501"
    elif "DataUL16APVC" in sampleName: year = "21502"
    elif "DataUL16APVD" in sampleName: year = "21503"
    elif "DataUL16APVE" in sampleName: year = "21504"
    elif "DataUL16APVF" in sampleName: year = "21505"
    elif "DataUL16PostAPVF" in sampleName: year = "21601"
    elif "DataUL16PostAPVG" in sampleName: year = "21602"
    elif "DataUL16PostAPVH" in sampleName: year = "21603"
    #
    elif "DataUL17B" in sampleName: year = "21701"
    elif "DataUL17C" in sampleName: year = "21702"
    elif "DataUL17D" in sampleName: year = "21703"
    elif "DataUL17E" in sampleName: year = "21704"
    elif "DataUL17F" in sampleName: year = "21705"
    #
    elif "DataUL18A" in sampleName: year = "21801"
    elif "DataUL18B" in sampleName: year = "21802"
    elif "DataUL18C" in sampleName: year = "21803"
    elif "DataUL18D" in sampleName: year = "21804"
    #
    if "JetHT" in sampleName: ID = "01"
    elif "MET" in sampleName: ID = "02"
  elif "Data" in sampleName:
    #
    #
    if   "Data22C" in sampleName: year = "22201"
    elif "Data22D" in sampleName: year = "22202"
    elif "Data22E" in sampleName: year = "22203"
    elif "Data22F" in sampleName: year = "22204"
    elif "Data22G" in sampleName: year = "22205"
    #
    elif "Data23Cv1" in sampleName: year = "22301"
    elif "Data23Cv2" in sampleName: year = "22302"
    elif "Data23Cv3" in sampleName: year = "22303"
    elif "Data23Cv4" in sampleName: year = "22304"
    elif "Data23Dv1" in sampleName: year = "22305"
    elif "Data23Dv2" in sampleName: year = "22306"
    #
    if "JetMET" in sampleName: ID = "01"
  #
  # For MC
  #
  elif "MCUL" in sampleName:
    if   "MCUL16APV"  in sampleName: year = "415"
    elif "MCUL16PostAPV"     in sampleName: year = "416"
    elif "MCUL17"     in sampleName: year = "417"
    elif "MCUL18"     in sampleName: year = "418"
    #
    if   "QCD_HT50to100"              in sampleName: ID = "0100"
    elif "QCD_HT100to200"             in sampleName: ID = "0101"
    elif "QCD_HT200to300"             in sampleName: ID = "0102"
    elif "QCD_HT300to500"             in sampleName: ID = "0103"
    elif "QCD_HT500to700"             in sampleName: ID = "0104"
    elif "QCD_HT700to1000"            in sampleName: ID = "0105"
    elif "QCD_HT1000to1500"           in sampleName: ID = "0106"
    elif "QCD_HT1500to2000"           in sampleName: ID = "0107"
    elif "QCD_HT2000toInf"            in sampleName: ID = "0108"
    elif "TT_0L"                      in sampleName: ID = "0200"
    elif "TT_1L"                      in sampleName: ID = "0201"
    elif "TT_2L"                      in sampleName: ID = "0202"
    elif "ST_tW_top"                  in sampleName: ID = "0300"
    elif "ST_tW_antitop"              in sampleName: ID = "0301"
    elif "ST_t-chan_antitop"          in sampleName: ID = "0302"
    elif "ST_t-chan_top"              in sampleName: ID = "0303"
    elif "ST_schan_hadronicDecays"    in sampleName: ID = "0304"
    elif "WWTo4Q"                     in sampleName: ID = "0400"
    elif "WZTo4Q"                     in sampleName: ID = "0401"
    elif "ZZTo4Q"                     in sampleName: ID = "0402"
    elif "WWTo1L1Nu2Q"                in sampleName: ID = "0403"
    elif "WZTo2Q2L"                   in sampleName: ID = "0404"
    elif "ZZTo2Q2L"                   in sampleName: ID = "0405"
    elif "WW"                         in sampleName: ID = "0406"
    elif "WZ"                         in sampleName: ID = "0407"
    elif "ZZ"                         in sampleName: ID = "0408"
    elif "WWW"                        in sampleName: ID = "0501"
    elif "WWZ"                        in sampleName: ID = "0502"
    elif "WZZ"                        in sampleName: ID = "0503"
    elif "ZZZ"                        in sampleName: ID = "0504"
    elif "EWKWminus2Jets_WToQQ"       in sampleName: ID = "0600"
    elif "EWKWplus2Jets_WToQQ"        in sampleName: ID = "0601"
    elif "EWKWminus2Jets_WToQQ"       in sampleName: ID = "0602"
    elif "VBS_WWSSTo4J_EWK"           in sampleName: ID = "0700"
    elif "VBS_WWSSTo4J_QCD"           in sampleName: ID = "0700"
    elif "VBS_WWOSTo4J_EWK"           in sampleName: ID = "0700"
    elif "VBS_ZWTo2B2J_EWK"           in sampleName: ID = "0800"
    elif "VBS_ZWTo2B2J_QCD"           in sampleName: ID = "0800"
    elif "VBS_ZWTo2JnoB2J_QCD"        in sampleName: ID = "0800"
    elif "VBS_ZWTo4J_EWK"             in sampleName: ID = "0800"
    elif "VBS_ZWTo4J_QCD"             in sampleName: ID = "0800"
    elif "VBS_ZZTo4J_QCD"             in sampleName: ID = "0900"
    elif "VBS_aQGC_WWOSTo4J"          in sampleName: ID = "1000"
    elif "VBS_aQGC_WWSSmTo4J"         in sampleName: ID = "1000"
    elif "VBS_aQGC_WWSSpTo4J"         in sampleName: ID = "1000"
    elif "VBS_aQGC_ZZTo2JnoB2J"       in sampleName: ID = "1100"
    elif "VBS_aQGC_ZZTo4J"            in sampleName: ID = "1100"
    elif "VBS_WWOSTo4J_EWK_QCD"       in sampleName: ID = "1200"
    elif "VBS_WWSSTo4J_EWK_QCD"       in sampleName: ID = "1200"
    elif "VBS_ZWTo2B2J_EWK_QCD"       in sampleName: ID = "1300"
    elif "VBS_ZWTo2JnoB2J_EWK_QCD"    in sampleName: ID = "1300"
    elif "VBS_ZZTo4J_EWK_QCD"         in sampleName: ID = "1400"
    elif "VBS_ZWTo4J_EWK_QCD"         in sampleName: ID = "1400"
  return year+ID