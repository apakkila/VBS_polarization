import ROOT
import os
import numpy as np

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data/processed_samples_with_PF_candidates"

output_dir = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates/mean_adjusted"
#output_dir = "/eos/user/a/apakkila/VBS_ML_project/data/standard_normalized_numpy_arrays"
os.makedirs(output_dir, exist_ok=True)

# Uncomment the normalization function you want to use

# # Min-Max normalization function
# def normalize_data(data):
#     """
#     Normalizes the data using Min-Max scaling to [0, 1].

#     Args:
#         data (np.ndarray): Input data array.

#     Returns:
#         np.ndarray: Min-Max scaled data array.
#     """
#     min_val = np.min(data)
#     max_val = np.max(data)
#     if max_val - min_val == 0:
#         return np.zeros_like(data)
#     return (data - min_val) / (max_val - min_val)

# StandardScaler normalization function
def normalize_data(data, mean_deviation):
    """
    Standardizes the data to have zero mean and unit variance.

    Args:
        data (np.ndarray): Input data array.

    Returns:
        np.ndarray: Standardized data array.
    """
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    
    # Avoid division by zero
    std_replaced = np.where(std == 0, 1, std)
    
    return (data - mean) / std_replaced + mean_deviation


def process_samples(sample_list, data_path, output_dir):
    """
    Processes ROOT samples, extracts columns, and saves them as a single NumPy file.

    Args:
        sample_list (list): List of sample names.
        data_path (str): Path to the ROOT files.
        output_dir (str): Directory to save the NumPy arrays.
    """
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

        # z_j for the leading subjet (the subjet with higher transverse momentum)
        df_root = df_root.Define("V0_z_j_leading", "TMath::Max(V0_SubJet0_p4.Pt(), V0_SubJet1_p4.Pt()) / V0_SubJets_p4.Pt()")
        df_root = df_root.Define("V1_z_j_leading", "TMath::Max(V1_SubJet0_p4.Pt(), V1_SubJet1_p4.Pt()) / V1_SubJets_p4.Pt()")

        # z_j for the subleading subjet (the subjet with lower transverse momentum)
        df_root = df_root.Define("V0_z_j_subleading", "TMath::Min(V0_SubJet0_p4.Pt(), V0_SubJet1_p4.Pt()) / V0_SubJets_p4.Pt()")
        df_root = df_root.Define("V1_z_j_subleading", "TMath::Min(V1_SubJet0_p4.Pt(), V1_SubJet1_p4.Pt()) / V1_SubJets_p4.Pt()")

        # Transforming mVV to log(mVV)
        df_root = df_root.Define("log_VV_mVV", "TMath::Log(VV_mVV)")

        # Convert specific columns to NumPy arrays
        columns_to_extract = [
            "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", "V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
            "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", "V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",

            "VV_deta", "VV_dphi", "VV_mVV", "log_VV_mVV",

            "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",

            "TagJet0_eta", "TagJet0_pt", "TagJet0_phi", "TagJet0_mass", "TagJet0_area",
            "TagJet1_eta", "TagJet1_pt", "TagJet1_phi", "TagJet1_mass", "TagJet1_area",

            "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
            "V0_SubJet0_eta", "V0_SubJet1_eta", "V1_SubJet0_eta", "V1_SubJet1_eta",
            "V0_SubJet0_phi", "V0_SubJet1_phi", "V1_SubJet0_phi", "V1_SubJet1_phi",
            "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
            "V0_SubJet0_area", "V0_SubJet1_area", "V1_SubJet0_area", "V1_SubJet1_area"
        ]
        
        numpy_data = df_root.AsNumpy(columns_to_extract)

        if sample == "SS":
            if sample_name == "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, 0) for column_name, array in numpy_data.items()}
            elif sample_name == "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, -5) for column_name, array in numpy_data.items()}
            elif sample_name == "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, 5) for column_name, array in numpy_data.items()}
        elif sample == "OS":
            if sample_name == "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, 0) for column_name, array in numpy_data.items()}
            elif sample_name == "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, -5) for column_name, array in numpy_data.items()}
            elif sample_name == "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, 5) for column_name, array in numpy_data.items()}
            elif sample_name == "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL":
                normalized_data = {column_name: normalize_data(array, 10) for column_name, array in numpy_data.items()}

        # Save all columns into a single NumPy file
        output_file = f"{output_dir}/{sample_name}.npz"
        np.savez(output_file, **normalized_data)
        print(f"Saved all columns to {output_file}")


# Choose which sample will be processed
sample = "OS"
#sample = "SS"


# if sample == "OS":
# # List of sample files
#     sample_list = [
#         "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
#         "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
#         "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
#         "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
#     ]
# elif sample == "SS":
#     sample_list = [
#         "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
#         "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
#         "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
#     ]

if sample == "OS":
# List of sample files
    sample_list = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL"
    ]
elif sample == "SS":
    sample_list = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL"
    ]

# Call the function
process_samples(sample_list, data_path, output_dir)