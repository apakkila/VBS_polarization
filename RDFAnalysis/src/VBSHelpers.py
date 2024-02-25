import ROOT
import json
import numpy as np
from typing import List

#====================================================
#
# Functions for files and parsing
#
#====================================================

def findFiles(file : str) -> List[str]:
    with open(file) as f:
        return [line.strip() for line in f.readlines() if line.strip().endswith(".root")]

def parseFileName(file : str) -> dict:
    result = {}
    dataset_name = str.split(file, "/")[-1].replace(".root", "")
    name_parts = str.split(dataset_name, "_")
    if "Data" in name_parts[1]:
        result["isMC"] = False
        result["year"] = (name_parts[1].replace("Data", "")[:len(name_parts[1].replace("Data", ""))-1], name_parts[1][-1])
        result["dataset"] = name_parts[2]
        result["full_name"] = "_".join(name_parts[1:])
    else:
        result["isMC"] = True
        result["year"] = (name_parts[1].replace("MC", ""), None)
        result["dataset"] = "_".join(name_parts[2:])
        result["full_name"] = "_".join(name_parts[1:])
    return result

#====================================================
#
# Bins for histograms
#
#====================================================
def get_bins() -> dict:
    bins = {}
    
    # These pt and eta bins are some JEC bins
    bins["pt"] = {}
    bins["pt"]["bins"] = np.array((1, 5, 6, 8, 10, 12, 15, 18, 21, 24, 28, 32, 37, 43, 49, 56, 64, 74, 84, 97, 114, 133,
                    153, 174, 196, 220, 245, 272, 300, 330, 362, 395, 430, 468, 507, 548, 592, 638, 686, 737,
                    790, 846, 905, 967, 1032, 1101, 1172, 1248, 1327, 1410, 1497, 1588, 1684, 1784, 1890, 2000,
                    2116, 2238, 2366, 2500, 2640, 2787, 2941, 3103, 3273, 3450, 3637, 3832, 4037, 4252, 4477, 4713,
                    4961, 5220, 5492, 5777, 6076, 6389, 6717, 7000), dtype=float)
    bins["pt"]["n"] = len(bins["pt"]["bins"]) - 1

    bins["eta"] = {}
    bins["eta"]["bins"] = np.array((-5.191, -4.889, -4.716, -4.538, -4.363, -4.191, -4.013, -3.839, -3.664, -3.489, -3.314,
    -3.139, -2.964, -2.853, -2.65, -2.5, -2.322, -2.172, -2.043, -1.93, -1.83, -1.74, -1.653, -1.566,
    -1.479, -1.392, -1.305, -1.218, -1.131, -1.044, -0.957, -0.879, -0.783, -0.696, -0.609, -0.522,
    -0.435, -0.348, -0.261, -0.174, -0.087, 0, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609,
    0.696, 0.783, 0.879, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479, 1.566, 1.653, 1.74,
    1.83, 1.93, 2.043, 2.172, 2.322, 2.5, 2.65, 2.853, 2.964, 3.139, 3.314, 3.489, 3.664, 3.839,
    4.013, 4.191, 4.363, 4.538, 4.716, 4.889, 5.191), dtype=float)
    bins["eta"]["n"] = len(bins["eta"]["bins"]) - 1
    
    bins["phi"] = {}
    bins["phi"]["bins"] = np.linspace(-3.1416, 3.1416, 100, dtype=float)
    bins["phi"]["n"] = len(bins["phi"]["bins"]) - 1
    
    bins["mjj"] = {}
    bins["mjj"]["bins"] = np.linspace(0, 5000, 200, dtype=float)
    bins["mjj"]["n"] = len(bins["mjj"]["bins"]) - 1
    
    bins["deltaEta"] = {}
    bins["deltaEta"]["bins"] = np.linspace(0, 10, 100, dtype=float)
    bins["deltaEta"]["n"] = len(bins["deltaEta"]["bins"]) - 1
    
    bins["deltaR"] = {}
    bins["deltaR"]["bins"] = np.linspace(0, 10, 100, dtype=float)
    bins["deltaR"]["n"] = len(bins["deltaR"]["bins"]) - 1
    
    return bins

def get_sample_variables() -> dict:
    #====================================================
    #
    # ParticleNetMD cut values
    #
    #====================================================

    ParticleNetWvsQCDMDCut = {
        "UL16APV": {
            "2p5": 0.6400,
            "1p0": 0.8500,
            "0p5": 0.9100,
        },
        "UL16PostAPV": {
            "2p5": 0.6400,
            "1p0": 0.8400,
            "0p5": 0.9100,
        },
        "UL17": {
            "2p5": 0.5800,
            "1p0": 0.8100,
            "0p5": 0.8900,
        },
        "UL18": {
            "2p5": 0.5900,
            "1p0": 0.8200,
            "0p5": 0.9000,
        },
    }

    #====================================================
    #
    # Integrated lumi in inverse picobarns
    # Unit: Inverse Picobarns
    #
    #====================================================

    lumi_Dict = {"UL16APV": 19521.22,
                "UL16PostAPV": 16812.15,
                "UL17": 41479.681,
                "UL18": 59832.47}

    lumiUp_Dict = {"UL16APV": (1. + 0.012)*lumi_Dict["UL16APV"], 
                    "UL16PostAPV": (1. + 0.012)*lumi_Dict["UL16PostAPV"],
                    "UL17": (1. + 0.023)*lumi_Dict["UL17"],
                    "UL18": (1. + 0.025)*lumi_Dict["UL18"]}

    lumiDown_Dict = {"UL16APV": (1. - 0.012)*lumi_Dict["UL16APV"],
                    "UL16PostAPV": (1. - 0.012)*lumi_Dict["UL16PostAPV"],
                    "UL17": (1. - 0.023)*lumi_Dict["UL17"],
                    "UL18": (1. - 0.025)*lumi_Dict["UL18"]}

    #====================================================
    #
    # CROSS-SECTIONS FOR MC SAMPLES
    # Unit: picobarns
    #
    #====================================================
    BR_H_bb = 0.5824
    BR_W_qq = 0.6741
    BR_Z_qq = 0.6991

    eraYears = {"MCUL16APV", "MCUL16PostAPV", "MCUL17", "MCUL18"}
    xs_Dict = {}

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
        xs_Dict[year] = {}
        #
        # VBS WW (EWK, QCD)
        #
        xs_Dict[year]["VBS_WWSSTo4J_EWK"] = 0.1249
        xs_Dict[year]["VBS_WWSSTo4J_QCD"] = 0.1087
        xs_Dict[year]["VBS_WWOSTo4J_EWK"] = 1.8930
        xs_Dict[year]["VBS_WWOSTo4J_QCD"] = 160.1

        #
        # VBS ZW (EWK, QCD)
        #
        xs_Dict[year]["VBS_ZWTo2B2J_EWK"] = 0.123
        xs_Dict[year]["VBS_ZWTo2B2J_QCD"] = 1.261
        xs_Dict[year]["VBS_ZWTo2JnoB2J_QCD"] = 4.733
        xs_Dict[year]["VBS_ZWTo4J_EWK"] = 0.1663
        xs_Dict[year]["VBS_ZWTo4J_QCD"] = 4.2340

        #
        # VBS ZZ (EWK, QCD)
        #
        xs_Dict[year]["VBS_ZZTo4J_QCD"] = 1.0840

        #
        # VBS VV (EWK, QCD)
        #    
        xs_Dict[year]["VBS_WWSSTo4J_EWK_QCD"] = 0.2421
        xs_Dict[year]["VBS_WWOSTo4J_EWK_QCD"] = 161.4
        xs_Dict[year]["VBS_ZWTo2B2J_EWK_QCD"] = 1.385
        xs_Dict[year]["VBS_ZWTo4J_EWK_QCD"] = 4.405
        xs_Dict[year]["VBS_ZZTo4J_EWK_QCD"] = 1.136
        xs_Dict[year]["VBS_ZWTo2JnoB2J_EWK_QCD"] = 5.19
        
        #
        # VBS VV (aQGC)
        #
        xs_Dict[year]["VBS_aQGC_WWOSTo4J"] = 9.701
        xs_Dict[year]["VBS_aQGC_WWSSmTo4J"] = 0.1306
        xs_Dict[year]["VBS_aQGC_WWSSpTo4J"] = 0.9043
        xs_Dict[year]["VBS_aQGC_ZZTo2JnoB2J"] = 0.9258
        xs_Dict[year]["VBS_aQGC_ZZTo4J"] = 2.423

        #************************
        #
        # QCD
        #
        #************************
        xs_Dict[year]["QCD_HT50to100"]    = 185900000.0
        xs_Dict[year]["QCD_HT100to200"]   = 23630000.0
        xs_Dict[year]["QCD_HT200to300"]   = 1551000.0
        xs_Dict[year]["QCD_HT300to500"]   = 324600.0
        xs_Dict[year]["QCD_HT500to700"]   = 30350.0
        xs_Dict[year]["QCD_HT700to1000"]  = 6437.0
        xs_Dict[year]["QCD_HT1000to1500"] = 1118.0
        xs_Dict[year]["QCD_HT1500to2000"] = 108.0
        xs_Dict[year]["QCD_HT2000toInf"]  = 22.04

        #************************
        #
        # V->qq + jets
        #
        #************************
        xs_Dict[year]["WJetsToQQ_HT200to400"] = 2565.0
        xs_Dict[year]["WJetsToQQ_HT400to600"] = 277.2
        xs_Dict[year]["WJetsToQQ_HT600to800"] = 59.1
        xs_Dict[year]["WJetsToQQ_HT800toInf"] = 28.75
        xs_Dict[year]["ZJetsToQQ_HT200to400"] = 1013.0
        xs_Dict[year]["ZJetsToQQ_HT400to600"] = 114.1
        xs_Dict[year]["ZJetsToQQ_HT600to800"] = 25.35
        xs_Dict[year]["ZJetsToQQ_HT800toInf"] = 12.92

        #************************
        #
        # TOP samples
        #
        #************************
        # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO#Top_quark_pair_cross_sections_at
        # //BR for W-boson from PDG(2018)
        xs_Dict[year]["TT_2L"] = 831.76*(3*0.1086)*(3*0.1086)
        xs_Dict[year]["TT_1L"] = 831.76*2*(3*0.1086*0.6741)
        xs_Dict[year]["TT_0L"] = 831.76*(0.6741)*(0.6741)
        # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_t_channel_cross_secti
        xs_Dict[year]["ST_tchan_top"]     = 136.02
        xs_Dict[year]["ST_tchan_antitop"] = 80.95
        # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt_channel_cross_sect
        # 71.7 pb is the total tW cross-section for top+anti-top.
        # xs for (top/antitop) = 35.85
        xs_Dict[year]["ST_tW_top"]     = 35.85
        xs_Dict[year]["ST_tW_antitop"] = 35.85
        # //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_s_channel_cross_secti
        xs_Dict[year]["ST_schan_hadronicDecays"] = 10.32*0.6741

        #************************
        #
        # VV samples
        #
        #************************
        xs_Dict[year]["WWTo4Q"] = 51.54
        xs_Dict[year]["ZZTo4Q"] = 3.306
        xs_Dict[year]["WWTo1L1Nu2Q"] = 50.92
        xs_Dict[year]["WZTo2Q2L"] = 6.331
        xs_Dict[year]["ZZTo2Q2L"] = 3.688

        xs_Dict[year]["WW"] = 75.95
        xs_Dict[year]["WZ"] = 27.59
        xs_Dict[year]["ZZ"] = 12.17

        xs_Dict[year]["WWW"] = 0.2158
        xs_Dict[year]["WWZ"] = 0.1707
        xs_Dict[year]["WZZ"] = 0.05709
        xs_Dict[year]["ZZZ"] = 0.01476

        #************************
        #
        # VBF EWK-W/Z
        #
        #************************
        xs_Dict[year]["EWKWm2Jets_WToQQ"] = 19.19
        xs_Dict[year]["EWKWp2Jets_WToQQ"] = 28.72
        xs_Dict[year]["EWKZ2Jets_ZToQQ"] = 9.792
        
    output_dict = {}
    output_dict["ParticleNetWvsQCDMDCut"] = ParticleNetWvsQCDMDCut
    output_dict["lumi"] = lumi_Dict
    output_dict["lumiUp"] = lumiUp_Dict
    output_dict["lumiDown"] = lumiDown_Dict
    output_dict["xs"] = xs_Dict
    return output_dict

if __name__ == "__main__":    
    with open("inputfiles/variables.json", "w") as f:
        json.dump(get_sample_variables(), f, indent=4)
    print("Created sample based variables")