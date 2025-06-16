import ROOT

def createHisto(hDict,name,title,nbins,xmin,xmax):
  hDict[name] = ROOT.TH1D(name,title, nbins, xmin, xmax)
  return hDict

def createHisto2D(hDict,name,title,nbinsx,xmin,xmax,nbinsy,ymin,ymax):
  hDict[name] = ROOT.TH2D(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
  return hDict

def SetupHistos_VBSQuarks(histosDict):

  histosDict = createHisto(histosDict, "h_genQuarkVBS0_pt",   ";VBS-tag q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS0_eta",  ";VBS-tag q0 #eta", 120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS0_phi",  ";VBS-tag q0 #phi", 120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS0_mass", ";VBS-tag q0 mass [GeV]", 250,  0.,   250.)

  histosDict = createHisto(histosDict, "h_genQuarkVBS1_pt",  ";VBS-tag q1 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS1_eta", ";VBS-tag q1 #eta", 120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS1_phi", ";VBS-tag q1 #phi", 120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genQuarkVBS1_mass", ";VBS-tag q1 mass [GeV]", 250,  0.,   250.)

  histosDict = createHisto(histosDict, "h_genqqVBS_pt",   ";VBS-tag qq pT [GeV]",200,  0., 2000.)
  histosDict = createHisto(histosDict, "h_genqqVBS_eta",  ";VBS-tag qq #eta",120, -6.,    6.)
  histosDict = createHisto(histosDict, "h_genqqVBS_phi",  ";VBS-tag qq #phi",120, -6.,    6.)

  histosDict = createHisto(histosDict, "h_genqqVBS_mass",    ";VBS-tag qq mass [GeV]", 150,  0.,   3000.)
  histosDict = createHisto(histosDict, "h_genqqVBS_mass_v2", ";VBS-tag qq mass [GeV]",1000,  0.,   1000.)#zoomed and finer bins

  histosDict = createHisto(histosDict, "h_genqqVBS_deltaEta",      ";VBS-tag qq #Delta #eta", 150, -15., 15.)
  histosDict = createHisto(histosDict, "h_genqqVBS_deltaEtaAbs",   ";VBS-tag qq |#Delta #eta|", 150,  0.,  15.)
  histosDict = createHisto(histosDict, "h_genqqVBS_eta0timeseta1", ";VBS-tag qq #eta_{0} #times #eta_{1}", 210, -21., 21.)
  histosDict = createHisto(histosDict, "h_genqqVBS_deltaPhi",      ";VBS-tag qq #Delta #phi", 160,  -8,   8.)

  histosDict = createHisto2D(histosDict, "h2_genqqVBS_eta_vs_genQuarkVBS0_eta",      "",120, -6., 6., 120, -6., 6.)
  histosDict = createHisto2D(histosDict, "h2_genqqVBS_eta_vs_genQuarkVBS1_eta",      "",120, -6., 6., 120, -6., 6.)
  histosDict = createHisto2D(histosDict, "h2_genQuarkVBS0_eta_vs_genQuarkVBS1_eta",  "",120, -6., 6., 120, -6., 6.)

  histosDict = createHisto2D(histosDict, "h2_genqqVBS_deltaEtaAbs_vs_genqqVBS_mass",  "", 150,  0.,  15., 40,  0., 2000.)
  histosDict = createHisto2D(histosDict, "h2_genqqVBS_eta0timeseta1_vs_genqqVBS_deltaEtaAbs","",  210, -21., 21., 150,  0.,  15.)

  return histosDict

def SetupHistos_WW4q(histosDict):

  histosDict = createHisto(histosDict, "h_genW2_pt",   "", 20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW2_eta",  "", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW2_phi",  "", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW2_mass", "", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW0_init_pt",   ";W0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW0_init_eta",  ";W0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_init_phi",  ";W0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_init_mass", ";W0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1_init_pt",   ";W1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW1_init_eta",  ";W1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_init_phi",  ";W1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_init_mass", ";W1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWW_init_pt",      ";WW pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_init_eta",     ";WW #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_init_phi",     ";WW #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_init_mass",    ";WW mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_init_mass_v2", ";WW mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genW0_pt",   ";W0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW0_eta",  ";W0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_phi",  ";W0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_mass", ";W0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1_pt",   ";W1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW1_eta",  ";W1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_phi",  ";W1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_mass", ";W1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWW_pt",   ";WW pT [GeV]",      20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_eta",  ";WW #eta",          120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_phi",  ";WW #phi",          120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_mass", ";WW mass [GeV]",     20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_mass_v2", ";WW mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genW0_costheta", "", 240,  -1.2,  1.2)
  histosDict = createHisto(histosDict, "h_genW1_costheta", "", 240,  -1.2,  1.2)

  histosDict = createHisto(histosDict, "h_genW0_costheta_v2", "", 240,  -1.2,  1.2)
  histosDict = createHisto(histosDict, "h_genW1_costheta_v2", "", 240,  -1.2,  1.2)

  histosDict = createHisto(histosDict, "h_genW0_costheta_v3", "", 240,  -1.2,  1.2)
  histosDict = createHisto(histosDict, "h_genW1_costheta_v3", "", 240,  -1.2,  1.2)

  histosDict = createHisto(histosDict, "h_genW0_zg_q0", "", 150,  0.,  1.5)
  histosDict = createHisto(histosDict, "h_genW1_zg_q0", "", 150,  0.,  1.5)

  histosDict = createHisto(histosDict, "h_genW0_zg_probeq", "", 150,  0.,  1.5)
  histosDict = createHisto(histosDict, "h_genW1_zg_probeq", "", 150,  0.,  1.5)

  histosDict = createHisto(histosDict, "h_genW0q0_pt",   ";W0 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genW0q0_eta",  ";W0 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0q0_phi",  ";W0 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0q0_mass", ";W0 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW0q1_pt",   ";W0 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genW0q1_eta",  ";W0 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0q1_phi",  ";W0 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0q1_mass", ";W0 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1q0_pt",   ";W1 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genW1q0_eta",  ";W1 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1q0_phi",  ";W1 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1q0_mass", ";W1 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1q1_pt",   ";W1 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genW1q1_eta",  ";W1 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1q1_phi",  ";W1 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1q1_mass", ";W1 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW0_qq_pt",  ";(W0) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW0_qq_eta", ";(W0) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_qq_phi", ";(W0) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_qq_mass",";(W0) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1_qq_pt",  ";(W1) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW1_qq_eta", ";(W1) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_qq_phi", ";(W1) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_qq_mass",";(W1) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWW_qqqq_pt",  ";(W0,W1) qqqq pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_qqqq_eta", ";(W0,W1) qqqq #eta",       120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_qqqq_phi", ";(W0,W1) qqqq #phi",       120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_qqqq_mass",";(W0,W1) qqqq mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_final_genW0q0_pt",   ";W0 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genW0q0_eta",  ";W0 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW0q0_phi",  ";W0 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW0q0_mass", ";W0 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genW0q1_pt",   ";W0 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genW0q1_eta",  ";W0 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW0q1_phi",  ";W0 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW0q1_mass", ";W0 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genW1q0_pt",   ";W1 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genW1q0_eta",  ";W1 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW1q0_phi",  ";W1 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW1q0_mass", ";W1 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genW1q1_pt",   ";W1 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genW1q1_eta",  ";W1 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW1q1_phi",  ";W1 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genW1q1_mass", ";W1 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW0_final_qq_pt",  ";(W0) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW0_final_qq_eta", ";(W0) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_final_qq_phi", ";(W0) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW0_final_qq_mass",";(W0) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW1_final_qq_pt",  ";(W1) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW1_final_qq_eta", ";(W1) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_final_qq_phi", ";(W1) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW1_final_qq_mass",";(W1) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWW_final_qqqq_pt",  ";(W0,W1) qqqq pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWW_final_qqqq_eta", ";(W0,W1) qqqq #eta",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_final_qqqq_phi", ";(W0,W1) qqqq #phi",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWW_final_qqqq_mass",";(W0,W1) qqqq mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_genW0q0_initVsFinal_pt",   "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q0_initVsFinal_eta",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q0_initVsFinal_phi",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q0_initVsFinal_mass", "", 200, -1., 1.)

  histosDict = createHisto(histosDict, "h_genW0q1_initVsFinal_pt",   "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q1_initVsFinal_eta",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q1_initVsFinal_phi",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW0q1_initVsFinal_mass", "", 200, -1., 1.)

  histosDict = createHisto(histosDict, "h_genW1q0_initVsFinal_pt",   "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q0_initVsFinal_eta",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q0_initVsFinal_phi",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q0_initVsFinal_mass", "", 200, -1., 1.)

  histosDict = createHisto(histosDict, "h_genW1q1_initVsFinal_pt",   "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q1_initVsFinal_eta",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q1_initVsFinal_phi",  "", 200, -1., 1.)
  histosDict = createHisto(histosDict, "h_genW1q1_initVsFinal_mass", "", 200, -1., 1.)

  histosDict = createHisto2D(histosDict, "h2_genW0_pt_vs_genW1_pt",       "", 20, 0., 2000., 20, 0., 2000.)
  histosDict = createHisto2D(histosDict, "h2_genW0_pt_vs_genW0W1_mass",   "", 20, 0., 2000., 20, 0., 2000.)
  histosDict = createHisto2D(histosDict, "h2_genW1_pt_vs_genW0W1_mass",   "", 20, 0., 2000., 20, 0., 2000.)

  histosDict = createHisto2D(histosDict, "h2_genW0_pt_vs_genW0_costheta", "",  20, 0., 2000., 24, -1.2,  1.2)
  histosDict = createHisto2D(histosDict, "h2_genW1_pt_vs_genW1_costheta", "",  20, 0., 2000., 24, -1.2,  1.2)

  return  histosDict

def SetupHistos_ZW4q(histosDict):

  histosDict = createHisto(histosDict, "h_genZ_init_pt",      ";Z pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_init_eta",     ";Z #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_init_phi",     ";Z #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_init_mass",    ";Z mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_init_pt",      ";W pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_init_eta",     ";W #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_init_phi",     ";W #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_init_mass",    ";W mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_init_pt",     ";WZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_init_eta",    ";WZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_init_phi",    ";WZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_init_mass",   ";WZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_init_mass_v2",";WZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZ_pt",   ";Z pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_eta",  ";Z #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_phi",  ";Z #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_mass", ";Z mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_pt",    ";W pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_eta",   ";W #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_phi",   ";W #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_mass",  ";W mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_pt",     ";WZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_eta",    ";WZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_phi",    ";WZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_mass",   ";WZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_mass_v2",";WZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genWq0_pt",    ";W q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genWq0_eta",   ";W q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq0_phi",   ";W q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq0_mass",  ";W q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWq1_pt",    ";W q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genWq1_eta",   ";W q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq1_phi",   ";W q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq1_mass",  ";W q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZq0_pt",    ";Z q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZq0_eta",   ";Z q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZq0_phi",   ";Z q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZq0_mass",  ";Z q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZq1_pt",    ";Z q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZq1_eta",   ";Z q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZq1_phi",   ";Z q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZq1_mass",  ";Z q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_qq_pt",   ";(W) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_qq_eta",  ";(W) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_qq_phi",  ";(W) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_qq_mass", ";(W) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_qq_pt",   ";(Z) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_qq_eta",  ";(Z) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_qq_phi",  ";(Z) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_qq_mass", ";(Z) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_qqqq_pt",  ";(W,Z) qqqq pT [GeV]",  20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_qqqq_eta", ";(W,Z) qqqq #eta",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_qqqq_phi", ";(W,Z) qqqq #phi",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_qqqq_mass",";(W,Z) qqqq mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_final_genWq0_pt",    ";W q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genWq0_eta",   ";W q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq0_phi",   ";W q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq0_mass",  ";W q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genWq1_pt",    ";W q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genWq1_eta",   ";W q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq1_phi",   ";W q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq1_mass",  ";W q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZq0_pt",    ";Z q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZq0_eta",   ";Z q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZq0_phi",   ";Z q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZq0_mass",  ";Z q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZq1_pt",    ";Z q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZq1_eta",   ";Z q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZq1_phi",   ";Z q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZq1_mass",  ";Z q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_final_qq_pt",  ";(W) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_eta", ";(W) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_phi", ";(W) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_mass",";(W) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_final_qq_pt",  ";(Z) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_eta", ";(Z) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_phi", ";(Z) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_mass",";(Z) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_final_qqqq_pt",  ";(W,Z) qqqq pT [GeV]",  20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqqq_eta", ";(W,Z) qqqq #eta",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqqq_phi", ";(W,Z) qqqq #phi",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqqq_mass",";(W,Z) qqqq mass [GeV]", 20,  0.,  2000.)

  return  histosDict

def SetupHistos_ZZ4q(histosDict):


  histosDict = createHisto(histosDict, "h_genZ0_init_pt",     ";Z0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ0_init_eta",    ";Z0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_init_phi",    ";Z0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_init_mass",   ";Z0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1_init_pt",     ";Z1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ1_init_eta",    ";Z1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_init_phi",    ";Z1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_init_mass",   ";Z1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_init_pt",     ";ZZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_init_eta",    ";ZZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_init_phi",    ";ZZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_init_mass",   ";ZZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_init_mass_v2",";ZZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZ0_pt",     ";Z0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ0_eta",    ";Z0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_phi",    ";Z0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_mass",   ";Z0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1_pt",     ";Z1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ1_eta",    ";Z1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_phi",    ";Z1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_mass",   ";Z1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_pt",     ";ZZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_eta",    ";ZZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_phi",    ";ZZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_mass",   ";ZZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_mass_v2",";ZZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZ0q0_pt",   ";Z0 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZ0q0_eta",  ";Z0 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0q0_phi",  ";Z0 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0q0_mass", ";Z0 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ0q1_pt",   ";Z0 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZ0q1_eta",  ";Z0 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0q1_phi",  ";Z0 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0q1_mass", ";Z0 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1q0_pt",   ";Z1 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZ1q0_eta",  ";Z1 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1q0_phi",  ";Z1 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1q0_mass", ";Z1 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1q1_pt",   ";Z1 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZ1q1_eta",  ";Z1 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1q1_phi",  ";Z1 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1q1_mass", ";Z1 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ0_qq_pt",  ";(Z0) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ0_qq_eta", ";(Z0) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_qq_phi", ";(Z0) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_qq_mass",";(Z0) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1_qq_pt",  ";(Z1) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ1_qq_eta", ";(Z1) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_qq_phi", ";(Z1) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_qq_mass",";(Z1) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_qqqq_pt",  ";(Z0,Z1) qqqq pT [GeV]",  20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_qqqq_eta", ";(Z0,Z1) qqqq #eta",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_qqqq_phi", ";(Z0,Z1) qqqq #phi",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_qqqq_mass",";(Z0,Z1) qqqq mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_final_genZ0q0_pt",   ";Z0 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZ0q0_eta",  ";Z0 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ0q0_phi",  ";Z0 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ0q0_mass", ";Z0 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZ0q1_pt",   ";Z0 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZ0q1_eta",  ";Z0 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ0q1_phi",  ";Z0 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ0q1_mass", ";Z0 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZ1q0_pt",   ";Z1 q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZ1q0_eta",  ";Z1 q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ1q0_phi",  ";Z1 q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ1q0_mass", ";Z1 q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZ1q1_pt",   ";Z1 q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZ1q1_eta",  ";Z1 q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ1q1_phi",  ";Z1 q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZ1q1_mass", ";Z1 q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ0_final_qq_pt",  ";(Z0) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ0_final_qq_eta", ";(Z0) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_final_qq_phi", ";(Z0) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ0_final_qq_mass",";(Z0) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ1_final_qq_pt",  ";(Z1) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ1_final_qq_eta", ";(Z1) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_final_qq_phi", ";(Z1) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ1_final_qq_mass",";(Z1) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_final_qqqq_pt",  ";(Z0,Z1) qqqq pT [GeV]",  20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqqq_eta", ";(Z0,Z1) qqqq #eta",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqqq_phi", ";(Z0,Z1) qqqq #phi",     120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqqq_mass",";(Z0,Z1) qqqq mass [GeV]", 20,  0.,  2000.)


  return  histosDict

def SetupHistos_ZWvvqq(histosDict):

  histosDict = createHisto(histosDict, "h_genZ_init_pt",      ";Z pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_init_eta",     ";Z #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_init_phi",     ";Z #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_init_mass",    ";Z mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_init_pt",      ";W pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_init_eta",     ";W #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_init_phi",     ";W #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_init_mass",    ";W mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_init_pt",     ";WZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_init_eta",    ";WZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_init_phi",    ";WZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_init_mass",   ";WZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_init_mass_v2",";WZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZ_pt",       ";Z pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_eta",      ";Z #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_phi",      ";Z #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_mass",     ";Z mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_pt",       ";W pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_eta",      ";W #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_phi",      ";W #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_mass",     ";W mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_pt",      ";WZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_eta",     ";WZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_phi",     ";WZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_mass",    ";WZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_mass_v2", ";WZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genWq0_pt",   ";W q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genWq0_eta",  ";W q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq0_phi",  ";W q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq0_mass", ";W q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWq1_pt",   ";W q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genWq1_eta",  ";W q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq1_phi",  ";W q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genWq1_mass", ";W q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZv0_pt",   ";Z v0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZv0_eta",  ";Z v0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZv0_phi",  ";Z v0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZv0_mass", ";Z v0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZv1_pt",   ";Z v1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZv1_eta",  ";Z v1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZv1_phi",  ";Z v1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZv1_mass", ";Z v1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_qq_pt",  ";(W) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_qq_eta", ";(W) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_qq_phi", ";(W) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_qq_mass",";(W) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_vv_pt",  ";(Z) vv pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_vv_eta", ";(Z) vv #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_vv_phi", ";(Z) vv #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_vv_mass",";(Z) vv mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_qqvv_pt",  ";(W,Z) qqvv pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_qqvv_eta", ";(W,Z) qqvv #eta",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_qqvv_phi", ";(W,Z) qqvv #phi",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_qqvv_mass",";(W,Z) qqvv mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_final_genWq0_pt",   ";W q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genWq0_eta",  ";W q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq0_phi",  ";W q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq0_mass", ";W q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genWq1_pt",   ";W q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genWq1_eta",  ";W q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq1_phi",  ";W q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genWq1_mass", ";W q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZv0_pt",   ";Z v0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZv0_eta",  ";Z v0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZv0_phi",  ";Z v0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZv0_mass", ";Z v0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_final_genZv1_pt",   ";Z v1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_final_genZv1_eta",  ";Z v1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZv1_phi",  ";Z v1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_final_genZv1_mass", ";Z v1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genW_final_qq_pt",  ";(W) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_eta", ";(W) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_phi", ";(W) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genW_final_qq_mass",";(W) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_final_vv_pt",  ";(Z) vv pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_eta", ";(Z) vv #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_phi", ";(Z) vv #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_mass",";(Z) vv mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genWZ_final_qqvv_pt",  ";(W,Z) qqvv pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqvv_eta", ";(W,Z) qqvv #eta",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqvv_phi", ";(W,Z) qqvv #phi",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genWZ_final_qqvv_mass",";(W,Z) qqvv mass [GeV]", 20,  0.,  2000.)

  return  histosDict

def SetupHistos_ZZvvqq(histosDict):

  histosDict = createHisto(histosDict, "h_genZvv_init_pt",     ";Z0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZvv_init_eta",    ";Z0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_init_phi",    ";Z0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_init_mass",   ";Z0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_init_pt",     ";Z1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZqq_init_eta",    ";Z1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_init_phi",    ";Z1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_init_mass",   ";Z1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_init_pt",      ";ZZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_init_eta",     ";ZZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_init_phi",     ";ZZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_init_mass",    ";ZZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_init_mass_v2", ";ZZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZqq_pt",    ";Z0 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZqq_eta",   ";Z0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_phi",   ";Z0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_mass",  ";Z0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZvv_pt",    ";Z1 pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZvv_eta",   ";Z1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_phi",   ";Z1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_mass",  ";Z1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_pt",     ";ZZ pT [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_eta",    ";ZZ #eta",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_phi",    ";ZZ #phi",120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_mass",   ";ZZ mass [GeV]", 20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_mass_v2",";ZZ mass [GeV]", 1000,  0.,  1000.)

  histosDict = createHisto(histosDict, "h_genZvv_v0_pt",    ";Zvv v0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZvv_v0_eta",   ";Zvv v0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_v0_phi",   ";Zvv v0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_v0_mass",  ";Zvv v0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZvv_v1_pt",    ";Zvv v1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZvv_v1_eta",   ";Zvv v1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_v1_phi",   ";Zvv v1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_v1_mass",  ";Zvv v1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_q0_pt",    ";Zqq q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZqq_q0_eta",   ";Zqq q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_q0_phi",   ";Zqq q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_q0_mass",  ";Zqq q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_q1_pt",    ";Zqq q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZqq_q1_eta",   ";Zqq q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_q1_phi",   ";Zqq q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_q1_mass",  ";Zqq q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZvv_vv_pt",    ";(Z) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZvv_vv_eta",   ";(Z) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_vv_phi",   ";(Z) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_vv_mass",  ";(Z) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_qq_pt",    ";(Z) qq pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZqq_qq_eta",   ";(Z) qq #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_qq_phi",   ";(Z) qq #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_qq_mass",  ";(Z) qq mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_qqvv_pt",  ";(Z,Z) qqvv pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_qqvv_eta", ";(Z,Z) qqvv #eta",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_qqvv_phi", ";(Z,Z) qqvv #phi",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_qqvv_mass",";(Z,Z) qqvv mass [GeV]", 20,  0.,  2000.)

  histosDict = createHisto(histosDict, "h_genZvv_final_v0_pt",    ";Zvv v0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v0_eta",   ";Zvv v0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v0_phi",   ";Zvv v0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v0_mass",  ";Zvv v0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZvv_final_v1_pt",    ";Zvv v1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v1_eta",   ";Zvv v1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v1_phi",   ";Zvv v1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZvv_final_v1_mass",  ";Zvv v1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_final_q0_pt",    ";Zqq q0 pT [GeV]",  50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q0_eta",   ";Zqq q0 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q0_phi",   ";Zqq q0 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q0_mass",  ";Zqq q0 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZqq_final_q1_pt",    ";Zqq q1 pT [GeV]", 50,  0.,   500.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q1_eta",   ";Zqq q1 #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q1_phi",   ";Zqq q1 #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZqq_final_q1_mass",  ";Zqq q1 mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_final_qq_pt",  ";(Z) qq pT [GeV]",   20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_eta", ";(Z) qq #eta",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_phi", ";(Z) qq #phi",  120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_qq_mass",";(Z) qq mass [GeV]",  250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZ_final_vv_pt",  ";(Z) vv pT [GeV]",  20, 0., 1000.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_eta", ";(Z) vv #eta", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_phi", ";(Z) vv #phi", 120, -6.,   6.)
  histosDict = createHisto(histosDict, "h_genZ_final_vv_mass",";(Z) vv mass [GeV]", 250,  0.,  250.)

  histosDict = createHisto(histosDict, "h_genZZ_final_qqvv_pt",  ";(Z,Z) qqvv pT [GeV]",   20,  0.,  2000.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqvv_eta", ";(Z,Z) qqvv #eta",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqvv_phi", ";(Z,Z) qqvv #phi",      120, -6.,     6.)
  histosDict = createHisto(histosDict, "h_genZZ_final_qqvv_mass",";(Z,Z) qqvv mass [GeV]", 20,  0.,  2000.)

  return  histosDict
