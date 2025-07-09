import ROOT
import os

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# List of sample files
sample_list = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
]

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data"

# Ensure the output directory exists
output_dir = "./output_deta_dphi_mVV_zj"
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

    # Define z_j values for both of the subjets
    df_root = df_root.Define("V0_z_j", "V0_SubJet0_pt / V0_pt")
    df_root = df_root.Define("V1_z_j", "V1_SubJet0_pt / V1_pt")

    # Dictionary for histrograms from multiple files
    histosDict = {}

    # Create histograms
    histosDict["h_VV_deta_" + sample_name] = df_root.Histo1D(("h_VV_deta", "deta distribution", 100, 0, 5), "VV_deta")
    histosDict["h_VV_dphi_" + sample_name] = df_root.Histo1D(("h_VV_dphi", "dphi distribution", 50, 2, 3.2), "VV_dphi")
    histosDict["h_VV_mVV_" + sample_name] = df_root.Histo1D(("h_VV_mVV", "mVV distribution", 200, 400, 3500), "VV_mVV")

    # Data for z_j from both of the subjest
    histosDict["h_V0_z_j_" + sample_name] = df_root.Histo1D(("h_V0_z_j", "z_j", 100, 0.4, 1), "V0_z_j")
    histosDict["h_V1_z_j_" + sample_name] = df_root.Histo1D(("h_V1_z_j", "z_j", 100, 0.4, 1), "V1_z_j")

    # Save histograms to a ROOT file
    for hName in histosDict:
        outFile = f"{output_dir}/Histo_{hName}.root"
        print(f"Saving histograms in {outFile}")
        outHisto = ROOT.TFile(outFile, "RECREATE")
        histosDict[hName].Write()
        outHisto.Close()

print("All histograms saved successfully!")