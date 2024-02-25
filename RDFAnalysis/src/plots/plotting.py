import ROOT
import uproot
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from hist import Hist

import argparse
import configparser

def read_config_file(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def parse_arguments():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--config', type=str, help='Path to the config file', required=True)
    return parser.parse_args()

if __name__ == "__main__":
   #  args = parse_arguments()
    # config = read_config_file(args.config)
        
    hep.style.use("CMS")
    input_files = {"EWK_QCD" : "output/VBS_EWK_QCD_output.root", "VBS_QCD" : "output/VBS_QCD_output.root", "EWK" : "output/VBS_EWK_output.root",
                   "aQGC" : "output/VBS_aQGC_output.root", "QCD_BCKG" : "output/QCD_BCKG_output.root", "TT_BCKG" : "output/TT_BCKG_output.root"}
    
    # Open the file and load the TagJet1_pt histogram
    files = [uproot.open(file) for file in input_files.values()]
   
    hists = [file["TagJet1_pt"].to_hist() for file in files]

    hep.cms.label(label="Private", data=False, year="2017", loc=0)
    for hist, label in zip(hists, input_files.keys()):
        hep.histplot(hist, label=label, density=True)
    
    ax = plt.gca()
    hep.box_aspect(ax)
    plt.xlabel(r"$p_{T,j1}$ [GeV]")
    plt.xlim(0, 1000)
    plt.ylabel("Events/Histogram area")
    plt.yscale("log")
    # plt.title("TagJet1_pt")
    plt.legend()
    plt.savefig("output/plots/VBS_EWK_QCD_VS_QCD_VS_EWK_TagJet1_pt.png")
    plt.clf()
    
    # TagJet2_pt
    hists = [file["TagJet2_pt"].to_hist() for file in files]

    hep.cms.label(label="Private", data=False, year="2017", loc=0)
    for hist, label in zip(hists, input_files.keys()):
        hep.histplot(hist, label=label, density=True)
    ax = plt.gca()
    hep.box_aspect(ax)
    plt.xlabel(r"$p_{T,j2}$ [GeV]")
    plt.xlim(0, 1000)
    plt.ylabel("Events/Histogram area")
    plt.yscale("log")
    # plt.title("TagJet1_pt")
    plt.legend()
    plt.savefig("output/plots/VBS_EWK_QCD_VS_QCD_VS_EWK_TagJet2_pt.png")
    plt.clf()
    
    # TagJet1_eta
    hists = [file["TagJet1_eta"].to_hist() for file in files]
    
    hep.cms.label(label="Private", data=False, year="2017", loc=0)
    for hist, label in zip(hists, input_files.keys()):
        hep.histplot(hist, label=label, density=True)
    
    ax = plt.gca()
    hep.box_aspect(ax)
    plt.xlabel(r"$\eta_{j1}$")
    plt.xlim(-5, 5)
    plt.ylabel("Events/Histogram area")
    plt.yscale("log")
    plt.legend()
    plt.savefig("output/plots/VBS_EWK_QCD_VS_QCD_VS_EWK_TagJet1_eta.png")
    plt.clf()
    
    #TagJet_mass
    hists = [file["TagJet_mass"].to_hist() for file in files]
    
    hep.cms.label(label="Private", data=False, year="2017", loc=0)
    for hist, label in zip(hists, input_files.keys()):
        hep.histplot(hist, label=label, density=True)
    ax = plt.gca()
    hep.box_aspect(ax)
    plt.xlabel(r"$m_{jj}$ [GeV]")
    plt.xlim(200, 1000)
    plt.ylabel("Events/Histogram area")
    plt.yscale("log")
    plt.legend()
    plt.savefig("output/plots/VBS_EWK_QCD_VS_QCD_VS_EWK_TagJet_mass.png")
    plt.clf()
    
    #TagJet_deltaEta
    hists = [file["TagJet_deltaEta"].to_hist() for file in files]

    hep.cms.label(label="Private", data=False, year="2017", loc=0)
    for hist, label in zip(hists, input_files.keys()):
        hep.histplot(hist, label=label, density=True)
    ax = plt.gca()
    hep.box_aspect(ax)
    plt.xlabel(r"$\Delta\eta_{jj}$")
    plt.xlim(0, 10)
    plt.ylabel("Events/Histogram area")
    plt.yscale("log")
    plt.legend()
    plt.savefig("output/plots/VBS_EWK_QCD_VS_QCD_VS_EWK_TagJet_deltaEta.png")
    
    plt.clf()
    
    
    
