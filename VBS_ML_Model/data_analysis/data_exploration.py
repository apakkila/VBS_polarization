import ROOT
import os

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# List of sample files
sample_list = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
]

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data"

# Ensure the output directory exists
output_dir = "./output_histograms"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over each sample in the sample list
for sample_name in sample_list:
    print(f"Processing sample: {sample_name}")

    # File path for the current sample
    file_path = f"{data_path}/{sample_name}.root"

    # Load the ROOT file into RDataFrame
    tree = "Events"
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

    # Define z_j values for both of the subjets
    df_root = df_root.Define("V0_z_j", "V0_SubJet0_pt / V0_pt")
    df_root = df_root.Define("V1_z_j", "V1_SubJet0_pt / V1_pt")

    # Dictionary for histrograms from multiple files
    histosDict = {}

    # Create histograms

    # V0 and V1
    histosDict["h_V0_p_theta_" + sample_name] = df_root.Histo1D(("h_V0_p_theta", "p_theta distribution", 100, 0, 1), "V0_p_theta")
    histosDict["h_V1_p_theta_" + sample_name] = df_root.Histo1D(("h_V1_p_theta", "p_theta distribution", 100, 0, 1), "V1_p_theta")

    histosDict["h_V0_z_j_" + sample_name] = df_root.Histo1D(("h_V0_z_j", "z_j", 100, 0.4, 1), "V0_z_j")
    histosDict["h_V1_z_j_" + sample_name] = df_root.Histo1D(("h_V1_z_j", "z_j", 100, 0.4, 1), "V1_z_j")

    histosDict["h_V0_pt_" + sample_name] = df_root.Histo1D(("h_V0_pt", "V0_pt", 100, 0.4, 1), "V0_pt")
    histosDict["h_V1_pt_" + sample_name] = df_root.Histo1D(("h_V1_pt", "V1_pt", 100, 0.4, 1), "V1_pt")

    histosDict["h_V0_eta_" + sample_name] = df_root.Histo1D(("h_V0_eta", "V0_eta", 100, 0.4, 1), "V0_eta")
    histosDict["h_V1_eta_" + sample_name] = df_root.Histo1D(("h_V1_eta", "V1_eta", 100, 0.4, 1), "V1_eta")
    
    histosDict["h_V0_phi_" + sample_name] = df_root.Histo1D(("h_V0_phi", "V0_phi", 100, 0.4, 1), "V0_phi")
    histosDict["h_V1_phi_" + sample_name] = df_root.Histo1D(("h_V1_phi", "V1_phi", 100, 0.4, 1), "V1_phi")
    
    histosDict["h_V0_mass_" + sample_name] = df_root.Histo1D(("h_V0_mass", "V0_mass", 100, 0.4, 1), "V0_mass")
    histosDict["h_V1_mass_" + sample_name] = df_root.Histo1D(("h_V1_mass", "V1_mass", 100, 0.4, 1), "V1_mass")

    # VV
    histosDict["h_VV_deta_" + sample_name] = df_root.Histo1D(("h_VV_deta", "deta distribution", 100, 0, 5), "VV_deta")
    histosDict["h_VV_dphi_" + sample_name] = df_root.Histo1D(("h_VV_dphi", "dphi distribution", 50, 2, 3.2), "VV_dphi")
    histosDict["h_VV_mVV_" + sample_name] = df_root.Histo1D(("h_VV_mVV", "mVV distribution", 200, 400, 3500), "VV_mVV")

    # TagJJ
    histosDict["h_TagJJ_deta_" + sample_name] = df_root.Histo1D(("h_TagJJ_deta", "TagJJ deta distribution", 100, 0, 5), "TagJJ_deta")
    histosDict["h_TagJJ_dphi_" + sample_name] = df_root.Histo1D(("h_TagJJ_dphi", "TagJJ dphi distribution", 50, 2, 3.2), "TagJJ_dphi")
    histosDict["h_TagJJ_mJJ_" + sample_name] = df_root.Histo1D(("h_TagJJ_mJJ", "TagJJ mJJ distribution", 200, 400, 3500), "TagJJ_mJJ")

    # TagJet pair
    histosDict["h_TagJet0_pt_" + sample_name] = df_root.Histo1D(("h_TagJet0_pt", "TagJet0_pt", 100, 0.4, 1), "TagJet0_pt")
    histosDict["h_TagJet1_pt_" + sample_name] = df_root.Histo1D(("h_TagJet1_pt", "TagJet1_pt", 100, 0.4, 1), "TagJet1_pt")

    histosDict["h_TagJet0_eta_" + sample_name] = df_root.Histo1D(("h_TagJet0_eta", "TagJet0_eta", 100, 0.4, 1), "TagJet0_eta")
    histosDict["h_TagJet1_eta_" + sample_name] = df_root.Histo1D(("h_TagJet1_eta", "TagJet1_eta", 100, 0.4, 1), "TagJet1_eta")

    histosDict["h_TagJet0_phi_" + sample_name] = df_root.Histo1D(("h_TagJet0_phi", "TagJet0_phi", 100, 0.4, 1), "TagJet0_phi")
    histosDict["h_TagJet1_phi_" + sample_name] = df_root.Histo1D(("h_TagJet1_phi", "TagJet1_phi", 100, 0.4, 1), "TagJet1_phi")

    histosDict["h_TagJet0_mass_" + sample_name] = df_root.Histo1D(("h_TagJet0_mass", "TagJet0_mass", 100, 0.4, 1), "TagJet0_mass")
    histosDict["h_TagJet1_mass_" + sample_name] = df_root.Histo1D(("h_TagJet1_mass", "TagJet1_mass", 100, 0.4, 1), "TagJet1_mass")


    # Save histograms to a ROOT file
    for hName in histosDict:
        outFile = f"{output_dir}/Histo_{hName}.root"
        print(f"Saving histograms in {outFile}")
        outHisto = ROOT.TFile(outFile, "RECREATE")
        histosDict[hName].Write()
        outHisto.Close()

print("All histograms saved successfully!")