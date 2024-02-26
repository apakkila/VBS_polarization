import ROOT
from collections import OrderedDict

def SetupFatJetGenFlavourLabels(df, isMC_QCD):
  #
  # Skip for QCD. Put these dummy values
  #
  if isMC_QCD:
    df = df.Define("VCand0_isWJet",       "0")
    df = df.Define("VCand0_isZJet",       "0")
    df = df.Define("VCand0_isZbbJet",     "0")
    df = df.Define("VCand0_isZccJet",     "0")
    df = df.Define("VCand0_isHbbJet",     "0")
    df = df.Define("VCand0_isTopJet",     "0")
    df = df.Define("VCand0_isWJetFromTop","0")

    df = df.Define("VCand1_isWJet",       "0")
    df = df.Define("VCand1_isZJet",       "0")
    df = df.Define("VCand1_isZbbJet",     "0")
    df = df.Define("VCand1_isZccJet",     "0")
    df = df.Define("VCand1_isHbbJet",     "0")
    df = df.Define("VCand1_isTopJet",     "0")
    df = df.Define("VCand1_isWJetFromTop","0")
    return df

  df = df.Define("GenPart_motherPDGId",  "GetMotherPDGId(GenPart_genPartIdxMother,GenPart_pdgId)")
  df = df.Define("GenPart_isWBoson",     "abs(GenPart_pdgId)==24")
  df = df.Define("GenPart_isZBoson",     "abs(GenPart_pdgId)==23")
  df = df.Define("GenPart_isHBoson",     "abs(GenPart_pdgId)==25")
  df = df.Define("GenPart_isTop",        "abs(GenPart_pdgId)==6")
  df = df.Define("GenPart_isQuark",      "abs(GenPart_pdgId)>=1 && abs(GenPart_pdgId)<=5")
  df = df.Define("GenPart_isBQuark",     "abs(GenPart_pdgId)==5")
  df = df.Define("GenPart_isCQuark",     "abs(GenPart_pdgId)==4")
  df = df.Define("GenPart_isLepton",     "abs(GenPart_pdgId)==11 || abs(GenPart_pdgId)==13 || abs(GenPart_pdgId)==15")
  # df = df.Define("GenPart_p4",                "return ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass);")
  ############################################
  #
  #
  #
  ############################################
  df = df.Define("GenPart_genPartIdxDaughter",  "GetGenPartIdxDaugther(GenPart_genPartIdxMother)")
  genPartBranchList = [
    "GenPart_eta","GenPart_phi",
    "GenPart_genPartIdxMother", "GenPart_genPartIdxDaughter",
    "GenPart_pdgId","GenPart_motherPDGId", "GenPart_statusFlags",
    "GenPart_isWBoson","GenPart_isZBoson","GenPart_isHBoson","GenPart_isTop",
    "GenPart_isQuark","GenPart_isBQuark","GenPart_isCQuark",
    "GenPart_isLepton",
  ]
  genPartBranch = ','.join(genPartBranchList)
  df = df.Define("VCand_flavLabels_genPartIdx", "FatJetGenFlavourLabelsAndGenPartIndex_V2({VCand0_eta,VCand1_eta},{VCand0_phi,VCand1_phi},"+genPartBranch+")")
  ############################################
  #
  #
  #
  ############################################
  for VIdx in ["0","1"]:
    df = df.Define(f"VCand{VIdx}_isWJet",           f"VCand_flavLabels_genPartIdx[0][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isZJet",           f"VCand_flavLabels_genPartIdx[1][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isZbbJet",         f"VCand_flavLabels_genPartIdx[2][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isZccJet",         f"VCand_flavLabels_genPartIdx[3][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isHbbJet",         f"VCand_flavLabels_genPartIdx[4][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isTopJet",         f"VCand_flavLabels_genPartIdx[5][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_isWJetFromTop",    f"VCand_flavLabels_genPartIdx[6][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W0_q0_idx",        f"VCand_flavLabels_genPartIdx[7][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W0_q1_idx",        f"VCand_flavLabels_genPartIdx[8][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W0_lep_idx",       f"VCand_flavLabels_genPartIdx[9][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W1_q0_idx",        f"VCand_flavLabels_genPartIdx[10][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W1_q1_idx",        f"VCand_flavLabels_genPartIdx[11][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_W1_lep_idx",       f"VCand_flavLabels_genPartIdx[12][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z0_q0_idx",        f"VCand_flavLabels_genPartIdx[13][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z0_q1_idx",        f"VCand_flavLabels_genPartIdx[14][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z0_lep0_idx",      f"VCand_flavLabels_genPartIdx[15][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z0_lep1_idx",      f"VCand_flavLabels_genPartIdx[16][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z1_q0_idx",        f"VCand_flavLabels_genPartIdx[17][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z1_q1_idx",        f"VCand_flavLabels_genPartIdx[18][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z1_lep0_idx",      f"VCand_flavLabels_genPartIdx[19][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Z1_lep1_idx",      f"VCand_flavLabels_genPartIdx[20][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_H0_bquark0_idx",   f"VCand_flavLabels_genPartIdx[21][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_H0_bquark1_idx",   f"VCand_flavLabels_genPartIdx[22][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_H1_bquark0_idx",   f"VCand_flavLabels_genPartIdx[23][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_H1_bquark1_idx",   f"VCand_flavLabels_genPartIdx[24][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top0_bquark_idx",  f"VCand_flavLabels_genPartIdx[25][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top0_W_q0_idx",    f"VCand_flavLabels_genPartIdx[26][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top0_W_q1_idx",    f"VCand_flavLabels_genPartIdx[27][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top0_W_lep_idx",   f"VCand_flavLabels_genPartIdx[28][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top1_bquark_idx",  f"VCand_flavLabels_genPartIdx[29][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top1_W_q0_idx",    f"VCand_flavLabels_genPartIdx[30][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top1_W_q1_idx",    f"VCand_flavLabels_genPartIdx[31][{VIdx}]")
    df = df.Define(f"VCand{VIdx}_Top1_W_lep_idx",   f"VCand_flavLabels_genPartIdx[32][{VIdx}]")
    for itr in ["0","1"]:
      df = df.Define(f"VCand{VIdx}_W{itr}_q0_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_W{itr}_q0_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q0_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_W{itr}_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q0_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_W{itr}_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q0_mass",      f"VCand{VIdx}_W{itr}_q0_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_W{itr}_q0_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_W{itr}_q0_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_W{itr}_q0_idx,0)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q1_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_W{itr}_q1_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q1_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_W{itr}_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q1_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_W{itr}_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_q1_mass",      f"VCand{VIdx}_W{itr}_q1_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_W{itr}_q1_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_W{itr}_q1_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_W{itr}_q1_idx,0)")
      df = df.Define(f"VCand{VIdx}_W{itr}_lep_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_W{itr}_lep_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_lep_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_W{itr}_lep_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_lep_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_W{itr}_lep_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_W{itr}_lep_mass",      f"VCand{VIdx}_W{itr}_lep_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_W{itr}_lep_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_W{itr}_lep_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_W{itr}_lep_idx,0)")
    for itr in ["0","1"]:
      df = df.Define(f"VCand{VIdx}_Z{itr}_q0_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_Z{itr}_q0_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q0_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_Z{itr}_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q0_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_Z{itr}_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q0_mass",      f"VCand{VIdx}_Z{itr}_q0_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Z{itr}_q0_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q0_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Z{itr}_q0_idx,0)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q1_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_Z{itr}_q1_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q1_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_Z{itr}_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q1_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_Z{itr}_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q1_mass",      f"VCand{VIdx}_Z{itr}_q1_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Z{itr}_q1_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Z{itr}_q1_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Z{itr}_q1_idx,0)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep0_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_Z{itr}_lep0_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep0_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_Z{itr}_lep0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep0_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_Z{itr}_lep0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep0_mass",      f"VCand{VIdx}_Z{itr}_q0_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Z{itr}_lep0_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep0_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Z{itr}_lep0_idx,0)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep1_pt",        f"GetFromVec(GenPart_pt,VCand{VIdx}_Z{itr}_lep1_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep1_eta",       f"GetFromVec(GenPart_eta,VCand{VIdx}_Z{itr}_lep1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep1_phi",       f"GetFromVec(GenPart_phi,VCand{VIdx}_Z{itr}_lep1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep1_mass",      f"VCand{VIdx}_Z{itr}_q1_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Z{itr}_lep1_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Z{itr}_lep1_pdgId",     f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Z{itr}_lep1_idx,0)")
    for itr in ["0","1"]:
      df = df.Define(f"VCand{VIdx}_Top{itr}_bquark_pt",     f"GetFromVec(GenPart_pt,VCand{VIdx}_Top{itr}_bquark_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_bquark_eta",    f"GetFromVec(GenPart_eta,VCand{VIdx}_Top{itr}_bquark_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_bquark_phi",    f"GetFromVec(GenPart_phi,VCand{VIdx}_Top{itr}_bquark_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_bquark_mass",   f"VCand{VIdx}_Top{itr}_bquark_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Top{itr}_bquark_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Top{itr}_bquark_pdgId",  f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Top{itr}_bquark_idx,0)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q0_pt",       f"GetFromVec(GenPart_pt,VCand{VIdx}_Top{itr}_W_q0_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q0_eta",      f"GetFromVec(GenPart_eta,VCand{VIdx}_Top{itr}_W_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q0_phi",      f"GetFromVec(GenPart_phi,VCand{VIdx}_Top{itr}_W_q0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q0_mass",     f"VCand{VIdx}_Top{itr}_W_q0_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Top{itr}_W_q0_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q0_pdgId",    f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Top{itr}_W_q0_idx,0)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q1_pt",       f"GetFromVec(GenPart_pt,VCand{VIdx}_Top{itr}_W_q1_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q1_eta",      f"GetFromVec(GenPart_eta,VCand{VIdx}_Top{itr}_W_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q1_phi",      f"GetFromVec(GenPart_phi,VCand{VIdx}_Top{itr}_W_q1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q1_mass",     f"VCand{VIdx}_Top{itr}_W_q1_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Top{itr}_W_q1_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_q1_pdgId",    f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Top{itr}_W_q1_idx,0)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_lep_pt",      f"GetFromVec(GenPart_pt,VCand{VIdx}_Top{itr}_W_lep_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_lep_eta",     f"GetFromVec(GenPart_eta,VCand{VIdx}_Top{itr}_W_lep_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_lep_phi",     f"GetFromVec(GenPart_phi,VCand{VIdx}_Top{itr}_W_lep_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_lep_mass",    f"VCand{VIdx}_Top{itr}_W_lep_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_Top{itr}_W_lep_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_Top{itr}_W_lep_pdgId",   f"GetFromVec(GenPart_pdgId,VCand{VIdx}_Top{itr}_W_lep_idx,0)")
    for itr in ["0","1"]:
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark0_pt",     f"GetFromVec(GenPart_pt,VCand{VIdx}_H{itr}_bquark0_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark0_eta",    f"GetFromVec(GenPart_eta,VCand{VIdx}_H{itr}_bquark0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark0_phi",    f"GetFromVec(GenPart_phi,VCand{VIdx}_H{itr}_bquark0_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark0_mass",   f"VCand{VIdx}_H{itr}_bquark0_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_H{itr}_bquark0_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark0_pdgId",  f"GetFromVec(GenPart_pdgId,VCand{VIdx}_H{itr}_bquark0_idx,0)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark1_pt",     f"GetFromVec(GenPart_pt,VCand{VIdx}_H{itr}_bquark1_idx,-1.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark1_eta",    f"GetFromVec(GenPart_eta,VCand{VIdx}_H{itr}_bquark1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark1_phi",    f"GetFromVec(GenPart_phi,VCand{VIdx}_H{itr}_bquark1_idx,-9.f)")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark1_mass",   f"VCand{VIdx}_H{itr}_bquark1_idx != -1 ? GetQuarkLeptonMass(GenPart_pdgId[VCand{VIdx}_H{itr}_bquark1_idx]) : -1.f")
      df = df.Define(f"VCand{VIdx}_H{itr}_bquark1_pdgId",  f"GetFromVec(GenPart_pdgId,VCand{VIdx}_H{itr}_bquark1_idx,0)")

  return df

def ListOfFatJetGenFlavourLabels(isNominal=True):
  branchList = []

  for VIdx in ["0","1"]:
    branchList += [
      f"VCand{VIdx}_isWJet",f"VCand{VIdx}_isZJet",f"VCand{VIdx}_isZbbJet",f"VCand{VIdx}_isZccJet",f"VCand{VIdx}_isHbbJet",f"VCand{VIdx}_isTopJet",f"VCand{VIdx}_isWJetFromTop"
    ]
    # if isNominal: #TEMP
    #   branchList += [
    #     f"VCand{VIdx}_W0_q0_idx",f"VCand{VIdx}_W0_q1_idx",f"VCand{VIdx}_W0_lep_idx",
    #     f"VCand{VIdx}_W1_q0_idx",f"VCand{VIdx}_W1_q1_idx",f"VCand{VIdx}_W1_lep_idx",
    #     f"VCand{VIdx}_Z0_q0_idx",f"VCand{VIdx}_Z0_q1_idx",f"VCand{VIdx}_Z0_lep0_idx",f"VCand{VIdx}_Z0_lep1_idx",
    #     f"VCand{VIdx}_Z1_q0_idx",f"VCand{VIdx}_Z1_q1_idx",f"VCand{VIdx}_Z1_lep0_idx",f"VCand{VIdx}_Z1_lep1_idx",
    #     f"VCand{VIdx}_H0_bquark0_idx",f"VCand{VIdx}_H0_bquark1_idx",
    #     f"VCand{VIdx}_H1_bquark0_idx",f"VCand{VIdx}_H1_bquark1_idx",
    #     f"VCand{VIdx}_Top0_bquark_idx",f"VCand{VIdx}_Top0_W_q0_idx",f"VCand{VIdx}_Top0_W_q1_idx",f"VCand{VIdx}_Top0_W_lep_idx",
    #     f"VCand{VIdx}_Top1_bquark_idx",f"VCand{VIdx}_Top1_W_q0_idx",f"VCand{VIdx}_Top1_W_q1_idx",f"VCand{VIdx}_Top1_W_lep_idx",
    #   ]
    for itr in ["0","1"]:
      branchList += [
        f"VCand{VIdx}_W{itr}_q0_pt",f"VCand{VIdx}_W{itr}_q0_eta",f"VCand{VIdx}_W{itr}_q0_phi",f"VCand{VIdx}_W{itr}_q0_mass",f"VCand{VIdx}_W{itr}_q0_pdgId",
        f"VCand{VIdx}_W{itr}_q1_pt",f"VCand{VIdx}_W{itr}_q1_eta",f"VCand{VIdx}_W{itr}_q1_phi",f"VCand{VIdx}_W{itr}_q1_mass",f"VCand{VIdx}_W{itr}_q1_pdgId",
        f"VCand{VIdx}_W{itr}_lep_pt",f"VCand{VIdx}_W{itr}_lep_eta",f"VCand{VIdx}_W{itr}_lep_phi",f"VCand{VIdx}_W{itr}_lep_mass",f"VCand{VIdx}_W{itr}_lep_pdgId"
      ]
    for itr in ["0","1"]:
      branchList += [
        f"VCand{VIdx}_Z{itr}_q0_pt",f"VCand{VIdx}_Z{itr}_q0_eta",f"VCand{VIdx}_Z{itr}_q0_phi",f"VCand{VIdx}_Z{itr}_q0_mass",f"VCand{VIdx}_Z{itr}_q0_pdgId",
        f"VCand{VIdx}_Z{itr}_q1_pt",f"VCand{VIdx}_Z{itr}_q1_eta",f"VCand{VIdx}_Z{itr}_q1_phi",f"VCand{VIdx}_Z{itr}_q1_mass",f"VCand{VIdx}_Z{itr}_q1_pdgId",
        f"VCand{VIdx}_Z{itr}_lep0_pt",f"VCand{VIdx}_Z{itr}_lep0_eta",f"VCand{VIdx}_Z{itr}_lep0_phi",f"VCand{VIdx}_Z{itr}_lep0_mass",f"VCand{VIdx}_Z{itr}_lep0_pdgId",
        f"VCand{VIdx}_Z{itr}_lep1_pt",f"VCand{VIdx}_Z{itr}_lep1_eta",f"VCand{VIdx}_Z{itr}_lep1_phi",f"VCand{VIdx}_Z{itr}_lep1_mass",f"VCand{VIdx}_Z{itr}_lep1_pdgId",
      ]
    for itr in ["0","1"]:
      branchList += [
        f"VCand{VIdx}_H{itr}_bquark0_pt",f"VCand{VIdx}_H{itr}_bquark0_eta",f"VCand{VIdx}_H{itr}_bquark0_phi",f"VCand{VIdx}_H{itr}_bquark0_mass",f"VCand{VIdx}_H{itr}_bquark0_pdgId",
        f"VCand{VIdx}_H{itr}_bquark1_pt",f"VCand{VIdx}_H{itr}_bquark1_eta",f"VCand{VIdx}_H{itr}_bquark1_phi",f"VCand{VIdx}_H{itr}_bquark1_mass",f"VCand{VIdx}_H{itr}_bquark1_pdgId"
      ]
    for itr in ["0","1"]:
      branchList += [
        f"VCand{VIdx}_Top{itr}_bquark_pt",  f"VCand{VIdx}_Top{itr}_bquark_eta",  f"VCand{VIdx}_Top{itr}_bquark_phi",  f"VCand{VIdx}_Top{itr}_bquark_mass",  f"VCand{VIdx}_Top{itr}_bquark_pdgId",
        f"VCand{VIdx}_Top{itr}_W_q0_pt",    f"VCand{VIdx}_Top{itr}_W_q0_eta",    f"VCand{VIdx}_Top{itr}_W_q0_phi",    f"VCand{VIdx}_Top{itr}_W_q0_mass",    f"VCand{VIdx}_Top{itr}_W_q0_pdgId",
        f"VCand{VIdx}_Top{itr}_W_q1_pt",    f"VCand{VIdx}_Top{itr}_W_q1_eta",    f"VCand{VIdx}_Top{itr}_W_q1_phi",    f"VCand{VIdx}_Top{itr}_W_q1_mass",    f"VCand{VIdx}_Top{itr}_W_q1_pdgId",
        f"VCand{VIdx}_Top{itr}_W_lep_pt",   f"VCand{VIdx}_Top{itr}_W_lep_eta",   f"VCand{VIdx}_Top{itr}_W_lep_phi",   f"VCand{VIdx}_Top{itr}_W_lep_mass",    f"VCand{VIdx}_Top{itr}_W_lep_pdgId"
      ]

  return branchList