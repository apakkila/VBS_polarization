import ROOT
import os

# Enable multi-threading for ROOT (optional, improves performance)
ROOT.EnableImplicitMT(4)

# List of sample files
sample_list = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
]

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data"

# Ensure the output directory exists
output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over each sample in the sample list
for sample_name in sample_list:
    print(f"Processing sample: {sample_name}")

    # File path for the current sample
    file_path = f"{data_path}/{sample_name}.root"

    # Load the ROOT file into RDataFrame
    tree = "Events"  # Replace with the actual tree name
    df_root = ROOT.RDataFrame(tree, file_path)

    # Define 4-vectors for the subjets
    df_root = df_root.Define("V0_SubJet0_p4", "ROOT::Math::PtEtaPhiMVector(V0_SubJet0_pt, V0_SubJet0_eta, V0_SubJet0_phi, V0_SubJet0_mass)")
    df_root = df_root.Define("V0_SubJet1_p4", "ROOT::Math::PtEtaPhiMVector(V0_SubJet1_pt, V0_SubJet1_eta, V0_SubJet1_phi, V0_SubJet1_mass)")
    df_root = df_root.Define("V1_SubJet0_p4", "ROOT::Math::PtEtaPhiMVector(V1_SubJet0_pt, V1_SubJet0_eta, V1_SubJet0_phi, V1_SubJet0_mass)")
    df_root = df_root.Define("V1_SubJet1_p4", "ROOT::Math::PtEtaPhiMVector(V1_SubJet1_pt, V1_SubJet1_eta, V1_SubJet1_phi, V1_SubJet1_mass)")

    # Define energies and momenta
    df_root = df_root.Define("V0_SubJets_p4", "V0_SubJet0_p4 + V0_SubJet1_p4")
    df_root = df_root.Define("V1_SubJets_p4", "V1_SubJet0_p4 + V1_SubJet1_p4")

    # Compute p_theta
    df_root = df_root.Define("V0_p_theta", "abs(V0_SubJet0_p4.E() - V0_SubJet1_p4.E()) / abs(V0_SubJets_p4.P())")
    df_root = df_root.Define("V1_p_theta", "abs(V1_SubJet0_p4.E() - V1_SubJet1_p4.E()) / abs(V1_SubJets_p4.P())")

    # Dictionary for histrograms from multiple files
    histosDict = {}

    # Create histograms
    histosDict["h_V0_p_theta_" + sample_name] = df_root.Histo1D(("h_V0_p_theta", "p_theta distribution", 100, 0, 1), "V0_p_theta")
    histosDict["h_V1_p_theta_" + sample_name] = df_root.Histo1D(("h_V1_p_theta", "p_theta distribution", 100, 0, 1), "V1_p_theta")

    # Save histograms to a ROOT file
    for hName in histosDict:
        outFile = f"{output_dir}/Histo_{hName}.root"
        print(f"Saving histograms in {outFile}")
        outHisto = ROOT.TFile(outFile, "RECREATE")
        histosDict[hName].Write()
        outHisto.Close()

print("All histograms saved successfully!")