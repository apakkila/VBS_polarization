import ROOT
import os
import numpy as np

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data"

# Define the output directory for NumPy arrays
output_dir = "./output_numpy_arrays"
os.makedirs(output_dir, exist_ok=True)

def normalize_data(data):
    """
    Normalizes the data using standard normalization (mean = 0, std = 1).

    Args:
        data (np.ndarray): Input data array.

    Returns:
        np.ndarray: Normalized data array.
    """
    return (data - np.mean(data)) / np.std(data)


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

        # Define z_j values for both of the subjets
        df_root = df_root.Define("V0_z_j", "V0_SubJet0_pt / V0_pt")
        df_root = df_root.Define("V1_z_j", "V1_SubJet0_pt / V1_pt")

        # Convert specific columns to NumPy arrays
        columns_to_extract = ["V0_p_theta", "V1_p_theta", "V0_z_j", "V1_z_j", "VV_deta", "VV_dphi", "VV_mVV"]
        numpy_data = df_root.AsNumpy(columns_to_extract)

         # Normalize each column
        normalized_data = {column_name: normalize_data(array) for column_name, array in numpy_data.items()}

        # Save all columns into a single NumPy file
        output_file = f"{output_dir}/{sample_name}.npz"
        np.savez(output_file, **normalized_data)
        print(f"Saved all columns to {output_file}")

# List of sample files
sample_list = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL"
]

# Call the function
process_samples(sample_list, data_path, output_dir)