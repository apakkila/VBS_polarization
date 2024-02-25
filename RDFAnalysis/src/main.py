import ROOT
from typing import List
import argparse
import configparser
import json
from VBSAnalysis import VBSAnalyzer

RDataFrame = ROOT.RDataFrame

def read_config_file(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def parse_arguments():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--config', type=str, help='Path to the config file', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    # Initialize
    args = parse_arguments()
    print("Reading config file")
    config = read_config_file(args.config)
    nThreads = int(config["Distributed"]["nThreads"])
    print("Number of threads: ", nThreads)    
    ROOT.EnableImplicitMT(nThreads)
    
    isMC = int(config["General"]["isMC"])
    
    # Load spec and variables
    with open(config["General"]["variableInfo"]) as f:
        json_variables = json.load(f)
    with open(config["General"]["fromSpec"]) as f:
        sample_dict = json.load(f)
        
    sample_names = list(sample_dict["samples"].keys())

    # Create the analyzer and do the analysis
    # Is an object needed? Probably not
    analyzer = VBSAnalyzer(fromSpec=config["General"]["fromSpec"], isMC=isMC, sample_names=sample_names)
    analyzer.do_VBS()
    hists = analyzer.get_histograms()
    ROOT.RDF.RunGraphs(hists)

    # Create the output file
    outfile = ROOT.TFile(config["General"]["outputdir"]+ "/"+config["General"]["sample_name"]+"_output.root", "RECREATE")
    for idx, hist in enumerate(hists):
        # Make a directory based on the first part of the hists name
        # This could use some improving, all of MC goes to same dir.
        if not outfile.Get(hist.GetName().split("_")[0]):
            outfile.mkdir(hist.GetName().split("_")[0])
        outfile.cd(hist.GetName().split("_")[0])
        hist.Write()
        outfile.cd()
    outfile.Close()
    
    print("Done writing histograms to file")
