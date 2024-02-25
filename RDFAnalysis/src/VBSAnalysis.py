import ROOT
from dataclasses import dataclass
from typing import List
from VBSHelpers import get_bins
import numpy as np

RDataFrame = ROOT.RDataFrame
RunGraphs = ROOT.RDF.RunGraphs
RNode = ROOT.RDF.RNode

class VBSAnalyzer:
    def __init__(self, 
                filelist        : List[str] = [],
                json_file       : str = "",
                nFiles          : int = -1,
                nThreads        : int = 1,
                isMC            : int = 0,
                fromSpec        : str = "",
                sample_names    : List[str] = [],
                ):
        
        self.nThreads = nThreads
        self.histograms = {"all" : []}
        self.has_run = False
        self.chain = None
        self.isMC = isMC
        self.bins = get_bins()
        
        # Although sample name is stored in the FromSpec file, you cannot access it outside of RDF
        self.sample_names = sample_names
        
        # This fromSpec vs filelist is a bit of a mess
        # fromSpec assumed default, for now
        print("Loading RDF")
        if fromSpec:
            self.rdf = ROOT.RDF.Experimental.FromSpec(fromSpec)
        else:
            self.rdf = self.__load_RDF(filelist, nFiles = nFiles)

        ROOT.RDF.Experimental.AddProgressBar(self.rdf)
        
        # Initial variables
        # TODO: 
        # 1. Trigger could be more sophisticated
        # 2. FromSpec is assumed, didn't want to do an if else mess
        if self.isMC > 0:
            self.rdf = (self.rdf.DefinePerSample("lumi", 'rdfsampleinfo_.GetD("lumi")')
                        .DefinePerSample("sumOfWeights", 'rdfsampleinfo_.GetD("sumOfWeights")')
                        .DefinePerSample("sampleName", 'rdfsampleinfo_.GetS("sampleName")')
                        .Define("weight", "genWeight*lumi/sumOfWeights")
                        .Filter("HLT_PFHT1050 || HLT_AK8PFJet500 || HLT_PFJet500 || HLT_PFJet550 || HLT_AK8PFJet550", "Trigger")
                        )
        else:
            self.rdf = (self.rdf.DefinePerSample("lumi", 'rdfsampleinfo_.GetD("lumi")')
                            .DefinePerSample("sampleName", 'rdfsampleinfo_.GetS("sampleName")')
                            .Define("weight", "1.")
                            .Filter("HLT_PFHT1050 || HLT_AK8PFJet500 || HLT_PFJet500 || HLT_PFJet550 || HLT_AK8PFJet550", "Trigger")
                        )
        
        # Initialize histograms    
        for sample in self.sample_names:
            self.histograms[sample] = []

    def __cut_Flag(self, rdf : RNode) -> RNode:
        """
        Apply the Flag (prev. MET_flag) cuts to the rdf.
        """
        # TODO: 
        # 1. These should be Run (2 or 3) dependent
        # 2. Are there separate FatJet flags?
        flag = """Flag_goodVertices && 
                    Flag_globalSuperTightHalo2016Filter &&
                    Flag_EcalDeadCellTriggerPrimitiveFilter &&
                    Flag_BadPFMuonFilter &&
                    Flag_BadPFMuonDzFilter && 
                    Flag_hfNoisyHitsFilter &&
                    Flag_eeBadScFilter &&
                    Flag_ecalBadCalibFilter
                    """
        rdf = (rdf.Filter(flag))
        return rdf
        
    def __load_RDF(self,
                   filelist : List[str], 
                   treename : str = "Events", 
                   nFiles   : int = -1
                   ) -> RDataFrame:
        
        if nFiles > 0:
            if len(filelist) < nFiles:
                raise ValueError("The filelist does not contain enough files")
            else:
                filelist = filelist[:nFiles]
        else:
            nFiles = len(filelist)
            filelist = filelist[:nFiles]
        
        # TChain isn't allowed to go out of scope or RDF will segfault (not a problem if an attribute or global scope)
        # See issue:
        # https://github.com/root-project/root/issues/10965#issue-1305124734
        self.chain = ROOT.TChain(treename)
        for file in filelist[:nFiles]:
            self.chain.Add(file)
        
        rdf = RDataFrame(self.chain)
        
        return rdf
            
    def __cut_VBS(self, rdf : RNode) -> RNode:
        dR_to_FatJet = 1.0
        minJetPt = 30
        fatJet_eta = 2.4
        rdf = (rdf.Filter("(nJet >= 4) && (nFatJet > 1)", "At least 4 jets and 2 fatjets")
                .Filter("FatJet_pt[0] > 200 && FatJet_pt[1] > 200", "pT > 200 GeV")
                .Filter(f"FatJet_eta[0] < {fatJet_eta} && FatJet_eta[1] < {fatJet_eta}", f"eta < {fatJet_eta}")
                # FatJet variables. Definitions required for histograms
                .Define("FatJet1_pt", "FatJet_pt[0]").Define("FatJet2_pt", "FatJet_pt[1]")
                .Define("FatJet1_eta", "FatJet_eta[0]").Define("FatJet2_eta", "FatJet_eta[1]")
                .Define("FatJet1_phi", "FatJet_phi[0]").Define("FatJet2_phi", "FatJet_phi[1]")
                .Define("FatJet1_mass", "FatJet_mass[0]").Define("FatJet2_mass", "FatJet_mass[1]")
                .Define("FatJet_invariantMass",
                        "sqrt(2.0 * FatJet1_pt * FatJet2_pt * (cosh(FatJet1_eta - FatJet2_eta) - cos(FatJet1_phi - FatJet2_phi)))")
                .Redefine("FatJet_eta", "ROOT::VecOps::Take(FatJet_eta, 2)")
                .Redefine("FatJet_phi", "ROOT::VecOps::Take(FatJet_phi, 2)")
                .Redefine("FatJet_mass", "ROOT::VecOps::Take(FatJet_mass, 2)")
                .Redefine("FatJet_pt", "ROOT::VecOps::Take(FatJet_pt, 2)")
                .Define("FatJet_dR", "ROOT::VecOps::DeltaR(FatJet1_eta, FatJet2_eta, FatJet1_phi, FatJet2_phi)")
                # FatJet to Jet separation
                .Define("FatJet1ToJet_deltaEta", "abs(Jet_eta - FatJet1_eta)").Define("FatJet2ToJet_deltaEta", "abs(Jet_eta - FatJet2_eta)")
                .Define("FatJet1ToJet_deltaPhi", "abs(Jet_phi - FatJet1_phi)").Define("FatJet2ToJet_deltaPhi", "abs(Jet_phi - FatJet2_phi)")
                .Define("FatJet1ToJet_dR", "ROOT::VecOps::sqrt(FatJet1ToJet_deltaEta*FatJet1ToJet_deltaEta + FatJet1ToJet_deltaPhi*FatJet1ToJet_deltaPhi)")
                .Define("FatJet2ToJet_dR", "ROOT::VecOps::sqrt(FatJet2ToJet_deltaEta*FatJet2ToJet_deltaEta + FatJet2ToJet_deltaPhi*FatJet2ToJet_deltaPhi)")
                .Define("Jet_passesFatJet_dR", f"(FatJet1ToJet_dR > {dR_to_FatJet} && FatJet2ToJet_dR > {dR_to_FatJet})")
                # Jet variables
                .Redefine("Jet_eta", f"Jet_eta[Jet_passesFatJet_dR && Jet_jetId > 4 && Jet_pt > {minJetPt} ]")
                .Redefine("Jet_phi", f"Jet_phi[Jet_passesFatJet_dR && Jet_jetId > 4 && Jet_pt > {minJetPt} ]")
                .Redefine("Jet_mass", f"Jet_mass[Jet_passesFatJet_dR && Jet_jetId > 4 && Jet_pt > {minJetPt} ]")
                .Define("Jet_pt_temp", f"Jet_pt[Jet_passesFatJet_dR && Jet_jetId > 4 && Jet_pt > {minJetPt} ]")
                .Redefine("Jet_jetId", f"Jet_jetId[Jet_passesFatJet_dR && Jet_jetId > 4 && Jet_pt > {minJetPt} ]")
                .Redefine("Jet_pt", "Jet_pt_temp")
                .Filter("Jet_pt.size() >= 2", "At least 2 jets after dR cut") # Ensure that events are good
                # Find TagJets
                .Define("Jet_fourVecs", "ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>(Jet_pt, Jet_eta, Jet_phi, Jet_mass)")
                .Define("TagJet_eta_combinations", "ROOT::VecOps::Combinations(Jet_eta, 2)") # Possibility to do similar max eta choice
                .Define("TagJet_mass_combinations", "ROOT::VecOps::Combinations(Jet_mass, 2)")
                .Define("TagJet_firstMass", "ROOT::VecOps::Take(Jet_mass, TagJet_mass_combinations[0])").Define("TagJet_secondMass", "ROOT::VecOps::Take(Jet_mass, TagJet_mass_combinations[1])")
                .Define("TagJet_firstEta", "ROOT::VecOps::Take(Jet_eta, TagJet_mass_combinations[0])").Define("TagJet_secondEta", "ROOT::VecOps::Take(Jet_eta, TagJet_mass_combinations[1])")
                .Define("TagJet_firstPt", "ROOT::VecOps::Take(Jet_pt, TagJet_mass_combinations[0])").Define("TagJet_secondPt", "ROOT::VecOps::Take(Jet_pt, TagJet_mass_combinations[1])")
                .Define("TagJet_firstPhi", "ROOT::VecOps::Take(Jet_phi, TagJet_mass_combinations[0])").Define("TagJet_secondPhi", "ROOT::VecOps::Take(Jet_phi, TagJet_mass_combinations[1])")
                .Define("TagJet_invariantMasses", "ROOT::VecOps::InvariantMasses(TagJet_firstPt, TagJet_firstEta, TagJet_firstPhi, TagJet_firstMass, TagJet_secondPt, TagJet_secondEta, TagJet_secondPhi, TagJet_secondMass)")
                .Define("TagJet_ids", "ROOT::VecOps::ArgMax(TagJet_invariantMasses)")
                .Define("TagJet_mass", "TagJet_invariantMasses[TagJet_ids]")
                .Filter("TagJet_mass > 200", "m > 200 GeV") 
                .Define("TagJet1_idx", "TagJet_mass_combinations[0][TagJet_ids]").Define("TagJet2_idx", "TagJet_mass_combinations[1][TagJet_ids]")
                # TagJet variables
                .Define("TagJet_deltaEta", "abs(Jet_eta[TagJet1_idx] - Jet_eta[TagJet2_idx])")
                .Define("TagJet_deltaPhi", "abs(Jet_phi[TagJet1_idx] - Jet_phi[TagJet2_idx])")
                .Define("TagJet_dR", "ROOT::VecOps::DeltaR(Jet_eta[TagJet1_idx], Jet_eta[TagJet2_idx], Jet_phi[TagJet1_idx], Jet_phi[TagJet2_idx])")
                .Define("TagJet1_pt", "Jet_pt[TagJet1_idx]").Define("TagJet2_pt", "Jet_pt[TagJet2_idx]")
                .Define("TagJet1_eta", "Jet_eta[TagJet1_idx]").Define("TagJet2_eta", "Jet_eta[TagJet2_idx]")
                .Define("TagJet1_phi", "Jet_phi[TagJet1_idx]").Define("TagJet2_phi", "Jet_phi[TagJet2_idx]")
                .Define("TagJet1_mass", "Jet_mass[TagJet1_idx]").Define("TagJet2_mass", "Jet_mass[TagJet2_idx]")
                # deltaEta and invariantMass are correlated, so this cut can be effectively done with the mass cut
                # .Filter("TagJet_deltaEta > 2.5", "deltaEta > 2.5")
        )
        return rdf
    
    def do_VBS(self) -> None:
        print("Doing VBS histograms")
        for sample in self.sample_names:
            all_rdf = self.rdf
            selected_rdf = self.__cut_Flag((self.__cut_VBS(self.rdf))).Filter(f'sampleName == "{sample}"')
            self.histograms[sample].extend([
                selected_rdf.Histo1D((f"{sample}_TagJet_mass", "TagJet_mass", self.bins["mjj"]["n"], self.bins["mjj"]["bins"]), "TagJet_mass", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet_deltaEta", "TagJet_deltaEta", self.bins["deltaEta"]["n"], self.bins["deltaEta"]["bins"]), "TagJet_deltaEta", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet1_pt", "TagJet1_pt", self.bins["pt"]["n"], self.bins["pt"]["bins"]), "TagJet1_pt", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet2_pt", "TagJet2_pt", self.bins["pt"]["n"], self.bins["pt"]["bins"]), "TagJet2_pt", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet1_eta", "TagJet1_eta", self.bins["eta"]["n"], self.bins["eta"]["bins"]), "TagJet1_eta", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet2_eta", "TagJet2_eta", self.bins["eta"]["n"], self.bins["eta"]["bins"]), "TagJet2_eta", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet1_mass", "TagJet1_mass", 20, 0, 500), "TagJet1_mass", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet2_mass", "TagJet2_mass", 20, 0, 500), "TagJet2_mass", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet1_phi", "TagJet1_phi", self.bins["phi"]["n"], self.bins["phi"]["bins"]), "TagJet1_phi", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet2_phi", "TagJet2_phi", self.bins["phi"]["n"], self.bins["phi"]["bins"]), "TagJet2_phi", "weight"),
                selected_rdf.Histo1D((f"{sample}_TagJet_dR", "TagJet_dR", self.bins["deltaR"]["n"], self.bins["deltaR"]["bins"]), "TagJet_dR", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet1_pt", "FatJet1_pt", self.bins["pt"]["n"], self.bins["pt"]["bins"]), "FatJet1_pt", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet2_pt", "FatJet2_pt", self.bins["pt"]["n"], self.bins["pt"]["bins"]), "FatJet2_pt", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet1_eta", "FatJet1_eta", self.bins["eta"]["n"], self.bins["eta"]["bins"]), "FatJet1_eta", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet2_eta", "FatJet2_eta", self.bins["eta"]["n"], self.bins["eta"]["bins"]), "FatJet2_eta", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet1_mass", "FatJet1_mass", 20, 0, 500), "FatJet1_mass", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet2_mass", "FatJet2_mass", 20, 0, 500), "FatJet2_mass", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet1_phi", "FatJet1_phi", self.bins["phi"]["n"], self.bins["phi"]["bins"]), "FatJet1_phi", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet2_phi", "FatJet2_phi", self.bins["phi"]["n"], self.bins["phi"]["bins"]), "FatJet2_phi", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet_dR", "FatJet_dR", self.bins["deltaR"]["n"], self.bins["deltaR"]["bins"]), "FatJet_dR", "weight"),
                selected_rdf.Histo1D((f"{sample}_FatJet_invariantMass", "FatJet_invariantMass", self.bins["mjj"]["n"], self.bins["mjj"]["bins"]), "FatJet_invariantMass", "weight"),
                selected_rdf.Histo2D((f"{sample}_FatJet1_ptVsFatJet2_pt", "FatJet1_ptVsFatJet2_pt", 
                                      self.bins["pt"]["n"], self.bins["pt"]["bins"], 
                                      self.bins["pt"]["n"], self.bins["pt"]["bins"]), 
                                     "FatJet1_pt", "FatJet2_pt", "weight"),
                selected_rdf.Histo2D((f"{sample}_TagJet_massVsTagJet_deltaEta", "TagJet_massVsTagJet_deltaEta",
                                      self.bins["mjj"]["n"], self.bins["mjj"]["bins"], 
                                      self.bins["deltaEta"]["n"], self.bins["deltaEta"]["bins"]), 
                                     "TagJet_mass", "TagJet_deltaEta", "weight"), 
            ])
        return self
            
    def get_histograms(self) -> dict:
        print("Returning histograms")
        # Make the hists a single list, since RunGraphs takes a list of histograms
        outhists = []
        for sample in self.sample_names:
            outhists.extend(self.histograms[sample])
        return outhists

    def run_histograms(self):
        if not self.has_run:
            # Slower or faster than a single list?
            for sample in self.sample_names:
                print("Running histograms for trigger", sample)
                RunGraphs(self.histograms[sample])
            self.has_run = True
        else:
            print("Histograms have already been run")
        return self