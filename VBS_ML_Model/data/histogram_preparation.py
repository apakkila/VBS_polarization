import ROOT
import os

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data/processed_samples_with_PF_candidates"
output_path = "/eos/user/a/apakkila/VBS_ML_project/data"

# List of sample files, comment out either SS or OS
sample_list = "SS"
#sample_list = "OS"

if sample_list=="SS":
    samples = [
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL"
    ]
    # Ensure the output directory exists
    output_dir = os.path.join(output_path, "output_histograms_SS_all_variables_with_PF_candidates")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
elif sample_list=="OS":
    samples = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL"
    ]

    # Ensure the output directory exists
    output_dir = os.path.join(output_path, "output_histograms_OS_all_variables_with_PF_candidates")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# Loop over each sample in the sample list
for sample_name in samples:
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
    df_root = df_root.Define("V0_z_j_leading", "TMath::Max(V0_SubJet0_p4.Pt(), V0_SubJet1_p4.Pt()) / V0_SubJets_p4.Pt()")
    df_root = df_root.Define("V1_z_j_leading", "TMath::Max(V1_SubJet0_p4.Pt(), V1_SubJet1_p4.Pt()) / V1_SubJets_p4.Pt()")

    df_root = df_root.Define("V0_z_j_subleading", "TMath::Min(V0_SubJet0_p4.Pt(), V0_SubJet1_p4.Pt()) / V0_SubJets_p4.Pt()")
    df_root = df_root.Define("V1_z_j_subleading", "TMath::Min(V1_SubJet0_p4.Pt(), V1_SubJet1_p4.Pt()) / V1_SubJets_p4.Pt()")

    # Transforming mVV to log(mVV)
    df_root = df_root.Define("VV_log_mVV", "TMath::Log(VV_mVV)")

    df_root = df_root.Define("TagJJ_log_mJJ", "TMath::Log(TagJJ_mJJ)")

    # Dictionary for histrograms from multiple files
    histosDict = {}

    # Create histograms

    # V0 and V1

    min_V0_p_theta = df_root.Min("V0_p_theta").GetValue()
    max_V0_p_theta = df_root.Max("V0_p_theta").GetValue()
    min_V1_p_theta = df_root.Min("V1_p_theta").GetValue()
    max_V1_p_theta = df_root.Max("V1_p_theta").GetValue()

    histosDict["h_V0_p_theta_" + sample_name] = df_root.Histo1D(("h_V0_p_theta", "p_theta distribution for V0", 120, 0, 0.95), "V0_p_theta")
    histosDict["h_V1_p_theta_" + sample_name] = df_root.Histo1D(("h_V1_p_theta", "p_theta distribution for V1", 120, 0, 0.95), "V1_p_theta")

    min_V0_z_j_leading = df_root.Min("V0_z_j_leading").GetValue()
    min_V0_z_j_subleading = df_root.Min("V0_z_j_subleading").GetValue()
    max_V0_z_j_leading = df_root.Max("V0_z_j_leading").GetValue()
    max_V0_z_j_subleading = df_root.Max("V0_z_j_subleading").GetValue()

    min_V1_z_j_leading = df_root.Min("V1_z_j_leading").GetValue()
    min_V1_z_j_subleading = df_root.Min("V1_z_j_subleading").GetValue()
    max_V1_z_j_leading = df_root.Max("V1_z_j_leading").GetValue()
    max_V1_z_j_subleading = df_root.Max("V1_z_j_subleading").GetValue()

    histosDict["h_V0_z_j_leading_" + sample_name] = df_root.Histo1D(("h_V0_z_j_leading", "V0_z_j_leading", 100, 0.45, 0.94), "V0_z_j_leading")
    histosDict["h_V0_z_j_subleading_" + sample_name] = df_root.Histo1D(("h_V0_z_j_subleading", "V0_z_j_subleading", 100, 0, 0.6), "V0_z_j_subleading")

    histosDict["h_V1_z_j_leading_" + sample_name] = df_root.Histo1D(("h_V1_z_j_leading", "V1_z_j_leading", 100, 0.45, 0.94), "V1_z_j_leading")
    histosDict["h_V1_z_j_subleading_" + sample_name] = df_root.Histo1D(("h_V1_z_j_subleading", "V1_z_j_subleading", 100, 0, 0.6), "V1_z_j_subleading")

    histosDict["h2_V0_p_theta_vs_z_j_" + sample_name] =  df_root.Histo2D(("h2_V0_p_theta_vs_z_j_leading", "p_{#theta} vs z_{j} for leading subjet of jet V0", 100, min_V0_p_theta, max_V0_p_theta, 100, min_V0_z_j_leading, max_V0_z_j_leading), "V0_p_theta", "V0_z_j_leading")
    histosDict["h2_V0_p_theta_vs_z_j_" + sample_name] =  df_root.Histo2D(("h2_V0_p_theta_vs_z_j_subleading", "p_{#theta} vs z_{j} for subleading subjet of jet V0", 100, min_V0_p_theta, max_V0_p_theta, 100, min_V0_z_j_subleading, max_V0_z_j_subleading), "V0_p_theta", "V0_z_j_subleading")
    histosDict["h2_V1_p_theta_vs_z_j_" + sample_name] =  df_root.Histo2D(("h2_V1_p_theta_vs_z_j_leading", "p_{#theta} vs z_{j} for leading subjet of jet V1", 100, min_V1_p_theta, max_V1_p_theta, 100, min_V1_z_j_leading, max_V1_z_j_leading), "V1_p_theta", "V1_z_j_leading")
    histosDict["h2_V1_p_theta_vs_z_j_" + sample_name] =  df_root.Histo2D(("h2_V1_p_theta_vs_z_j_subleading", "p_{#theta} vs z_{j} for subleading subjet of jet V1", 100, min_V1_p_theta, max_V1_p_theta, 100, min_V1_z_j_subleading, max_V1_z_j_subleading), "V1_p_theta", "V1_z_j_subleading")

    histosDict["h_V0_pt_" + sample_name] = df_root.Histo1D(("h_V0_pt", "V0_pt", 100, 390, 1300), "V0_pt")
    histosDict["h_V1_pt_" + sample_name] = df_root.Histo1D(("h_V1_pt", "V1_pt", 100, 390, 1300), "V1_pt")

    histosDict["h_V0_eta_" + sample_name] = df_root.Histo1D(("h_V0_eta", "V0_eta", 100, -2.5, 2.5), "V0_eta")
    histosDict["h_V1_eta_" + sample_name] = df_root.Histo1D(("h_V1_eta", "V1_eta", 100, -2.5, 2.5), "V1_eta")
    
    histosDict["h_V0_phi_" + sample_name] = df_root.Histo1D(("h_V0_phi", "V0_phi", 100, -3.2, 3.2), "V0_phi")
    histosDict["h_V1_phi_" + sample_name] = df_root.Histo1D(("h_V1_phi", "V1_phi", 100, -3.2, 3.2), "V1_phi")
    
    histosDict["h_V0_mass_" + sample_name] = df_root.Histo1D(("h_V0_mass", "V0_mass", 150, 60, 200), "V0_mass")
    histosDict["h_V1_mass_" + sample_name] = df_root.Histo1D(("h_V1_mass", "V1_mass", 150, 60, 180), "V1_mass")

    min_V0_area = df_root.Min("V0_area").GetValue()
    max_V0_area = df_root.Max("V0_area").GetValue()
    min_V1_area = df_root.Min("V1_area").GetValue()
    max_V1_area = df_root.Max("V1_area").GetValue()
    
    histosDict["h_V0_area_" + sample_name] = df_root.Histo1D(("h_V0_area", "V0_area", 150, min_V0_area, max_V0_area), "V0_area")
    histosDict["h_V1_area_" + sample_name] = df_root.Histo1D(("h_V1_area", "V1_area", 150, min_V1_area, max_V1_area), "V1_area")    

    # VV
    min_VV_log_mVV = df_root.Min("VV_log_mVV").GetValue() - 0.1
    max_VV_log_mVV = df_root.Max("VV_log_mVV").GetValue() + 0.1

    histosDict["h_VV_deta_" + sample_name] = df_root.Histo1D(("h_VV_deta", "deta distribution", 100, -0.1, 4.5), "VV_deta")
    histosDict["h_VV_dphi_" + sample_name] = df_root.Histo1D(("h_VV_dphi", "dphi distribution", 100, 1.95, 3.16), "VV_dphi")
    histosDict["h_VV_mVV_" + sample_name] = df_root.Histo1D(("h_VV_mVV", "mVV distribution", 150, 500, 3800), "VV_mVV")
    histosDict["h_VV_log_mVV_" + sample_name] = df_root.Histo1D(("h_VV_log_mVV", "log(m_VV) distribution", 150, 6, 9), "VV_log_mVV")

    min_TagJJ_log_mJJ = df_root.Min("TagJJ_log_mJJ").GetValue() - 0.1
    max_TagJJ_log_mJJ = df_root.Max("TagJJ_log_mJJ").GetValue() + 0.1

    # TagJJ
    histosDict["h_TagJJ_deta_" + sample_name] = df_root.Histo1D(("h_TagJJ_deta", "TagJJ deta distribution", 120, 2.0, 10), "TagJJ_deta")
    histosDict["h_TagJJ_dphi_" + sample_name] = df_root.Histo1D(("h_TagJJ_dphi", "TagJJ dphi distribution", 70, -0.1, 3.25), "TagJJ_dphi")
    histosDict["h_TagJJ_mJJ_" + sample_name] = df_root.Histo1D(("h_TagJJ_mJJ", "TagJJ mJJ distribution", 200, 400, 6000), "TagJJ_mJJ")
    histosDict["h_TagJJ_log_mJJ_" + sample_name] = df_root.Histo1D(("h_TagJJ_log_mJJ", "TagJJ log_mJJ distribution", 200, 6, 9.5), "TagJJ_log_mJJ")

    # TagJet pair
    histosDict["h_TagJet0_pt_" + sample_name] = df_root.Histo1D(("h_TagJet0_pt", "TagJet0_pt", 120, 50, 800), "TagJet0_pt")
    histosDict["h_TagJet1_pt_" + sample_name] = df_root.Histo1D(("h_TagJet1_pt", "TagJet1_pt", 120, 50, 500), "TagJet1_pt")

    histosDict["h_TagJet0_eta_" + sample_name] = df_root.Histo1D(("h_TagJet0_eta", "TagJet0_eta", 120, -5.1, 5.1), "TagJet0_eta")
    histosDict["h_TagJet1_eta_" + sample_name] = df_root.Histo1D(("h_TagJet1_eta", "TagJet1_eta", 120, -5.1, 5.1), "TagJet1_eta")

    histosDict["h_TagJet0_phi_" + sample_name] = df_root.Histo1D(("h_TagJet0_phi", "TagJet0_phi", 120, -3.2, 3.2), "TagJet0_phi")
    histosDict["h_TagJet1_phi_" + sample_name] = df_root.Histo1D(("h_TagJet1_phi", "TagJet1_phi", 120, -3.2, 3.2), "TagJet1_phi")

    histosDict["h_TagJet0_mass_" + sample_name] = df_root.Histo1D(("h_TagJet0_mass", "TagJet0_mass", 150, 0, 125), "TagJet0_mass")
    histosDict["h_TagJet1_mass_" + sample_name] = df_root.Histo1D(("h_TagJet1_mass", "TagJet1_mass", 150, 0, 80), "TagJet1_mass")

    min_TagJet0_area = df_root.Min("TagJet0_area").GetValue()
    max_TagJet0_area = df_root.Max("TagJet0_area").GetValue()
    min_TagJet1_area = df_root.Min("TagJet1_area").GetValue()
    max_TagJet1_area = df_root.Max("TagJet1_area").GetValue()

    histosDict["h_TagJet0_area_" + sample_name] = df_root.Histo1D(("h_TagJet0_area", "TagJet0_area", 150, min_TagJet0_area, max_TagJet0_area), "TagJet0_area")
    histosDict["h_TagJet1_area_" + sample_name] = df_root.Histo1D(("h_TagJet1_area", "TagJet1_area", 150, min_TagJet1_area, max_TagJet1_area), "TagJet1_area")

    # Min and max range values for the subjets

    # V0_SubJet0
    min_V0_SubJet0_pt   = df_root.Min("V0_SubJet0_pt").GetValue() - 5
    max_V0_SubJet0_pt   = df_root.Max("V0_SubJet0_pt").GetValue() + 5
    min_V0_SubJet0_eta  = df_root.Min("V0_SubJet0_eta").GetValue()
    max_V0_SubJet0_eta  = df_root.Max("V0_SubJet0_eta").GetValue()
    min_V0_SubJet0_phi  = df_root.Min("V0_SubJet0_phi").GetValue()
    max_V0_SubJet0_phi  = df_root.Max("V0_SubJet0_phi").GetValue()
    min_V0_SubJet0_mass = df_root.Min("V0_SubJet0_mass").GetValue() - 1
    max_V0_SubJet0_mass = df_root.Max("V0_SubJet0_mass").GetValue() + 1
    min_V0_SubJet0_area = df_root.Min("V0_SubJet0_area").GetValue()
    max_V0_SubJet0_area = df_root.Max("V0_SubJet0_area").GetValue()

    # V0_SubJet1
    min_V0_SubJet1_pt   = df_root.Min("V0_SubJet1_pt").GetValue() - 5
    max_V0_SubJet1_pt   = df_root.Max("V0_SubJet1_pt").GetValue() + 5
    min_V0_SubJet1_eta  = df_root.Min("V0_SubJet1_eta").GetValue()
    max_V0_SubJet1_eta  = df_root.Max("V0_SubJet1_eta").GetValue()
    min_V0_SubJet1_phi  = df_root.Min("V0_SubJet1_phi").GetValue()
    max_V0_SubJet1_phi  = df_root.Max("V0_SubJet1_phi").GetValue()
    min_V0_SubJet1_mass = df_root.Min("V0_SubJet1_mass").GetValue() - 1
    max_V0_SubJet1_mass = df_root.Max("V0_SubJet1_mass").GetValue() + 1
    min_V0_SubJet1_area = df_root.Min("V0_SubJet1_area").GetValue()
    max_V0_SubJet1_area = df_root.Max("V0_SubJet1_area").GetValue()

    # V1_SubJet0
    min_V1_SubJet0_pt   = df_root.Min("V1_SubJet0_pt").GetValue() - 5
    max_V1_SubJet0_pt   = df_root.Max("V1_SubJet0_pt").GetValue() + 5
    min_V1_SubJet0_eta  = df_root.Min("V1_SubJet0_eta").GetValue()
    max_V1_SubJet0_eta  = df_root.Max("V1_SubJet0_eta").GetValue()
    min_V1_SubJet0_phi  = df_root.Min("V1_SubJet0_phi").GetValue()
    max_V1_SubJet0_phi  = df_root.Max("V1_SubJet0_phi").GetValue()
    min_V1_SubJet0_mass = df_root.Min("V1_SubJet0_mass").GetValue() - 1
    max_V1_SubJet0_mass = df_root.Max("V1_SubJet0_mass").GetValue() + 1
    min_V1_SubJet0_area = df_root.Min("V1_SubJet0_area").GetValue()
    max_V1_SubJet0_area = df_root.Max("V1_SubJet0_area").GetValue()

    # V1_SubJet1
    min_V1_SubJet1_pt   = df_root.Min("V1_SubJet1_pt").GetValue() - 5
    max_V1_SubJet1_pt   = df_root.Max("V1_SubJet1_pt").GetValue()  + 5
    min_V1_SubJet1_eta  = df_root.Min("V1_SubJet1_eta").GetValue()
    max_V1_SubJet1_eta  = df_root.Max("V1_SubJet1_eta").GetValue()
    min_V1_SubJet1_phi  = df_root.Min("V1_SubJet1_phi").GetValue()
    max_V1_SubJet1_phi  = df_root.Max("V1_SubJet1_phi").GetValue()
    min_V1_SubJet1_mass = df_root.Min("V1_SubJet1_mass").GetValue() - 1
    max_V1_SubJet1_mass = df_root.Max("V1_SubJet1_mass").GetValue() + 1
    min_V1_SubJet1_area = df_root.Min("V1_SubJet1_area").GetValue()
    max_V1_SubJet1_area = df_root.Max("V1_SubJet1_area").GetValue()


    # V0_SubJet0
    
    histosDict["h_V0_SubJet0_pt_" + sample_name] = df_root.Histo1D(("h_V0_SubJet0_pt", "V0_SubJet0_pt", 120, 0, 1200), "V0_SubJet0_pt")
    histosDict["h_V0_SubJet0_eta_" + sample_name] = df_root.Histo1D(("h_V0_SubJet0_eta", "V0_SubJet0_eta", 120, min_V0_SubJet0_eta, max_V0_SubJet0_eta), "V0_SubJet0_eta")
    histosDict["h_V0_SubJet0_phi_" + sample_name] = df_root.Histo1D(("h_V0_SubJet0_phi", "V0_SubJet0_phi", 120, min_V0_SubJet0_phi, max_V0_SubJet0_phi), "V0_SubJet0_phi")
    histosDict["h_V0_SubJet0_mass_" + sample_name] = df_root.Histo1D(("h_V0_SubJet0_mass", "V0_SubJet0_mass", 150, 0, 80), "V0_SubJet0_mass")
    histosDict["h_V0_SubJet0_area_" + sample_name] = df_root.Histo1D(("h_V0_SubJet0_area", "V0_SubJet0_area", 100, min_V0_SubJet0_area, max_V0_SubJet0_area), "V0_SubJet0_area")

    # V0_SubJet1
    histosDict["h_V0_SubJet1_pt_" + sample_name] = df_root.Histo1D(("h_V0_SubJet1_pt", "V0_SubJet1_pt", 120, 0, 800), "V0_SubJet1_pt")
    histosDict["h_V0_SubJet1_eta_" + sample_name] = df_root.Histo1D(("h_V0_SubJet1_eta", "V0_SubJet1_eta", 120, min_V0_SubJet1_eta, max_V0_SubJet1_eta), "V0_SubJet1_eta")
    histosDict["h_V0_SubJet1_phi_" + sample_name] = df_root.Histo1D(("h_V0_SubJet1_phi", "V0_SubJet1_phi", 120, min_V0_SubJet1_phi, max_V0_SubJet1_phi), "V0_SubJet1_phi")
    histosDict["h_V0_SubJet1_mass_" + sample_name] = df_root.Histo1D(("h_V0_SubJet1_mass", "V0_SubJet1_mass", 150, 0, 80), "V0_SubJet1_mass")
    histosDict["h_V0_SubJet1_area_" + sample_name] = df_root.Histo1D(("h_V0_SubJet1_area", "V0_SubJet1_area", 100, min_V0_SubJet1_area, max_V0_SubJet1_area), "V0_SubJet1_area")

    # V1_SubJet0
    histosDict["h_V1_SubJet0_pt_" + sample_name] = df_root.Histo1D(("h_V1_SubJet0_pt", "V1_SubJet0_pt", 120, 0, 1200), "V1_SubJet0_pt")
    histosDict["h_V1_SubJet0_eta_" + sample_name] = df_root.Histo1D(("h_V1_SubJet0_eta", "V1_SubJet0_eta", 120, min_V1_SubJet0_eta, max_V1_SubJet0_eta), "V1_SubJet0_eta")
    histosDict["h_V1_SubJet0_phi_" + sample_name] = df_root.Histo1D(("h_V1_SubJet0_phi", "V1_SubJet0_phi", 120, min_V1_SubJet0_phi, max_V1_SubJet0_phi), "V1_SubJet0_phi")
    histosDict["h_V1_SubJet0_mass_" + sample_name] = df_root.Histo1D(("h_V1_SubJet0_mass", "V1_SubJet0_mass", 150, 0, 80), "V1_SubJet0_mass")
    histosDict["h_V1_SubJet0_area_" + sample_name] = df_root.Histo1D(("h_V1_SubJet0_area", "V1_SubJet0_area", 100, min_V1_SubJet0_area, max_V1_SubJet0_area), "V1_SubJet0_area")

    # V1_SubJet1
    histosDict["h_V1_SubJet1_pt_" + sample_name] = df_root.Histo1D(("h_V1_SubJet1_pt", "V1_SubJet1_pt", 120, 0, 800), "V1_SubJet1_pt")
    histosDict["h_V1_SubJet1_eta_" + sample_name] = df_root.Histo1D(("h_V1_SubJet1_eta", "V1_SubJet1_eta", 120, min_V1_SubJet1_eta, max_V1_SubJet1_eta), "V1_SubJet1_eta")
    histosDict["h_V1_SubJet1_phi_" + sample_name] = df_root.Histo1D(("h_V1_SubJet1_phi", "V1_SubJet1_phi", 120, min_V1_SubJet1_phi, max_V1_SubJet1_phi), "V1_SubJet1_phi")
    histosDict["h_V1_SubJet1_mass_" + sample_name] = df_root.Histo1D(("h_V1_SubJet1_mass", "V1_SubJet1_mass", 150, 0, 80), "V1_SubJet1_mass")
    histosDict["h_V1_SubJet1_area_" + sample_name] = df_root.Histo1D(("h_V1_SubJet1_area", "V1_SubJet1_area", 100, min_V1_SubJet1_area, max_V1_SubJet1_area), "V1_SubJet1_area")


    # Save histograms to a ROOT file
    for hName in histosDict:
        outFile = f"{output_dir}/{hName}.root"
        print(f"Saving histograms in {outFile}")
        outHisto = ROOT.TFile(outFile, "RECREATE")
        histosDict[hName].Write()
        outHisto.Close()

print("All histograms saved successfully!")