import ROOT
import os
import numpy as np

# Enable multi-threading for ROOT
ROOT.EnableImplicitMT(4)

# Define the path to the data files
data_path = "/eos/user/a/apakkila/VBS_ML_project/data/processed_samples_with_PF_candidates"

output_dir = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

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
def normalize_data(data):
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
    
    return (data - mean) / std_replaced

def min_max_normalize_data(data):
    """
    Normalizes the data using Min-Max scaling to [0, 1].

    Args:
        data (np.ndarray): Input data array.

    Returns:
        np.ndarray: Min-Max scaled data array.
    """
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val - min_val == 0:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)


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
    
        max_V0_z_j_leading = df_root.Max("V0_z_j_leading").GetValue()
        min_V0_z_j_leading = df_root.Min("V0_z_j_leading").GetValue()
        max_V1_z_j_leading = df_root.Max("V1_z_j_leading").GetValue()
        min_V1_z_j_leading = df_root.Min("V1_z_j_leading").GetValue()

        df_root = df_root.Define("V0_z_j_leading_mirrored", f"{max_V0_z_j_leading} + {min_V0_z_j_leading} - V0_z_j_leading")
        df_root = df_root.Define("V1_z_j_leading_mirrored", f"{max_V1_z_j_leading} + {min_V1_z_j_leading} - V1_z_j_leading")

        # z_j for the subleading subjet (the subjet with lower transverse momentum)
        df_root = df_root.Define("V0_z_j_subleading", "TMath::Min(V0_SubJet0_p4.Pt(), V0_SubJet1_p4.Pt()) / V0_SubJets_p4.Pt()")
        df_root = df_root.Define("V1_z_j_subleading", "TMath::Min(V1_SubJet0_p4.Pt(), V1_SubJet1_p4.Pt()) / V1_SubJets_p4.Pt()")

        max_V0_z_j_subleading = df_root.Max("V0_z_j_subleading").GetValue()
        min_V0_z_j_subleading = df_root.Min("V0_z_j_subleading").GetValue()
        max_V1_z_j_subleading = df_root.Max("V1_z_j_subleading").GetValue()
        min_V1_z_j_subleading = df_root.Min("V1_z_j_subleading").GetValue()

        df_root = df_root.Define("V0_z_j_subleading_mirrored", f"{max_V0_z_j_subleading} + {min_V0_z_j_subleading} - V0_z_j_subleading")
        df_root = df_root.Define("V1_z_j_subleading_mirrored", f"{max_V1_z_j_subleading} + {min_V1_z_j_subleading} - V1_z_j_subleading")

        min_VV_phi = df_root.Min("VV_dphi").GetValue()
        max_VV_phi = df_root.Max("VV_dphi").GetValue()

        df_root = df_root.Define("VV_dphi_mirrored", f"{min_VV_phi} + {max_VV_phi} - VV_dphi")

        min_TagJJ_deta = df_root.Min("TagJJ_deta").GetValue()
        max_TagJJ_deta = df_root.Max("TagJJ_deta").GetValue()

        df_root = df_root.Define("TagJJ_deta_mirrored", f"{min_TagJJ_deta} + {max_TagJJ_deta} - TagJJ_deta")

        # Transforming mVV to log(mVV)
        df_root = df_root.Define("log_VV_mVV", "TMath::Log(VV_mVV)")

        df_root = df_root.Define("log_TagJJ_mJJ", "TMath::Log(TagJJ_mJJ)")
        
        df_root = df_root.Define("log_TagJet0_mass", "TMath::Log(TagJet0_mass)")
        df_root = df_root.Define("log_TagJet1_mass", "TMath::Log(TagJet1_mass)")
        df_root = df_root.Define("log_TagJet0_pt", "TMath::Log(TagJet0_pt)")
        df_root = df_root.Define("log_TagJet1_pt", "TMath::Log(TagJet1_pt)")


        # Convert specific columns to NumPy arrays
        columns_to_extract = [
            "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", #"V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
            "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", #"V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",

            "VV_deta", "VV_dphi", "VV_mVV", "log_VV_mVV",

            "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ", "log_TagJJ_mJJ",

            # "TagJet0_eta", "TagJet0_pt", "TagJet0_phi", "TagJet0_mass", "TagJet0_area",
            # "TagJet1_eta", "TagJet1_pt", "TagJet1_phi", "TagJet1_mass", "TagJet1_area",
            # "log_TagJet0_mass", "log_TagJet1_mass", "log_TagJet0_pt", "log_TagJet1_pt",

            # "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
            # "V0_SubJet0_eta", "V0_SubJet1_eta", "V1_SubJet0_eta", "V1_SubJet1_eta",
            # "V0_SubJet0_phi", "V0_SubJet1_phi", "V1_SubJet0_phi", "V1_SubJet1_phi",
            # "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
            # "V0_SubJet0_area", "V0_SubJet1_area", "V1_SubJet0_area", "V1_SubJet1_area",
            # "V0_z_j_leading_mirrored", "V0_z_j_subleading_mirrored",
            # "V1_z_j_leading_mirrored", "V1_z_j_subleading_mirrored",
            # "VV_dphi_mirrored", "TagJJ_deta_mirrored",

            "V0_PFCand10_jetaxisDeta", "V0_PFCand10_jetaxisDphi", "V0_PFCand10_logPt", "V0_PFCand10_logE", "V0_PFCand10_logPtOverV0", "V0_PFCand10_logEOverV0", "V0_PFCand10_deltaR",
            "V0_PFCand11_jetaxisDeta", "V0_PFCand11_jetaxisDphi", "V0_PFCand11_logPt", "V0_PFCand11_logE", "V0_PFCand11_logPtOverV0", "V0_PFCand11_logEOverV0", "V0_PFCand11_deltaR",
            "V0_PFCand12_jetaxisDeta", "V0_PFCand12_jetaxisDphi", "V0_PFCand12_logPt", "V0_PFCand12_logE", "V0_PFCand12_logPtOverV0", "V0_PFCand12_logEOverV0", "V0_PFCand12_deltaR",
            "V0_PFCand13_jetaxisDeta", "V0_PFCand13_jetaxisDphi", "V0_PFCand13_logPt", "V0_PFCand13_logE", "V0_PFCand13_logPtOverV0", "V0_PFCand13_logEOverV0", "V0_PFCand13_deltaR",
            "V0_PFCand14_jetaxisDeta", "V0_PFCand14_jetaxisDphi", "V0_PFCand14_logPt", "V0_PFCand14_logE", "V0_PFCand14_logPtOverV0", "V0_PFCand14_logEOverV0", "V0_PFCand14_deltaR",
            "V0_PFCand15_jetaxisDeta", "V0_PFCand15_jetaxisDphi", "V0_PFCand15_logPt", "V0_PFCand15_logE", "V0_PFCand15_logPtOverV0", "V0_PFCand15_logEOverV0", "V0_PFCand15_deltaR",
            "V0_PFCand16_jetaxisDeta", "V0_PFCand16_jetaxisDphi", "V0_PFCand16_logPt", "V0_PFCand16_logE", "V0_PFCand16_logPtOverV0", "V0_PFCand16_logEOverV0", "V0_PFCand16_deltaR",
            "V0_PFCand17_jetaxisDeta", "V0_PFCand17_jetaxisDphi", "V0_PFCand17_logPt", "V0_PFCand17_logE", "V0_PFCand17_logPtOverV0", "V0_PFCand17_logEOverV0", "V0_PFCand17_deltaR",
            "V0_PFCand18_jetaxisDeta", "V0_PFCand18_jetaxisDphi", "V0_PFCand18_logPt", "V0_PFCand18_logE", "V0_PFCand18_logPtOverV0", "V0_PFCand18_logEOverV0", "V0_PFCand18_deltaR",
            "V0_PFCand19_jetaxisDeta", "V0_PFCand19_jetaxisDphi", "V0_PFCand19_logPt", "V0_PFCand19_logE", "V0_PFCand19_logPtOverV0", "V0_PFCand19_logEOverV0", "V0_PFCand19_deltaR",


            "V1_PFCand10_jetaxisDeta", "V1_PFCand10_jetaxisDphi", "V1_PFCand10_logPt", "V1_PFCand10_logE", "V1_PFCand10_logPtOverV1", "V1_PFCand10_logEOverV1", "V1_PFCand10_deltaR",
            "V1_PFCand11_jetaxisDeta", "V1_PFCand11_jetaxisDphi", "V1_PFCand11_logPt", "V1_PFCand11_logE", "V1_PFCand11_logPtOverV1", "V1_PFCand11_logEOverV1", "V1_PFCand11_deltaR",
            "V1_PFCand12_jetaxisDeta", "V1_PFCand12_jetaxisDphi", "V1_PFCand12_logPt", "V1_PFCand12_logE", "V1_PFCand12_logPtOverV1", "V1_PFCand12_logEOverV1", "V1_PFCand12_deltaR",
            "V1_PFCand13_jetaxisDeta", "V1_PFCand13_jetaxisDphi", "V1_PFCand13_logPt", "V1_PFCand13_logE", "V1_PFCand13_logPtOverV1", "V1_PFCand13_logEOverV1", "V1_PFCand13_deltaR",
            "V1_PFCand14_jetaxisDeta", "V1_PFCand14_jetaxisDphi", "V1_PFCand14_logPt", "V1_PFCand14_logE", "V1_PFCand14_logPtOverV1", "V1_PFCand14_logEOverV1", "V1_PFCand14_deltaR",
            "V1_PFCand15_jetaxisDeta", "V1_PFCand15_jetaxisDphi", "V1_PFCand15_logPt", "V1_PFCand15_logE", "V1_PFCand15_logPtOverV1", "V1_PFCand15_logEOverV1", "V1_PFCand15_deltaR",
            "V1_PFCand16_jetaxisDeta", "V1_PFCand16_jetaxisDphi", "V1_PFCand16_logPt", "V1_PFCand16_logE", "V1_PFCand16_logPtOverV1", "V1_PFCand16_logEOverV1", "V1_PFCand16_deltaR",
            "V1_PFCand17_jetaxisDeta", "V1_PFCand17_jetaxisDphi", "V1_PFCand17_logPt", "V1_PFCand17_logE", "V1_PFCand17_logPtOverV1", "V1_PFCand17_logEOverV1", "V1_PFCand17_deltaR",
            "V1_PFCand18_jetaxisDeta", "V1_PFCand18_jetaxisDphi", "V1_PFCand18_logPt", "V1_PFCand18_logE", "V1_PFCand18_logPtOverV1", "V1_PFCand18_logEOverV1", "V1_PFCand18_deltaR",
            "V1_PFCand19_jetaxisDeta", "V1_PFCand19_jetaxisDphi", "V1_PFCand19_logPt", "V1_PFCand19_logE", "V1_PFCand19_logPtOverV1", "V1_PFCand19_logEOverV1", "V1_PFCand19_deltaR",
        ]


        
        numpy_data = df_root.AsNumpy(columns_to_extract)


        from collections import defaultdict
        import numpy as np

        # Group vector features based on prefix (e.g. V0_PFCand10)
        def extract_vector_groups(numpy_data):
            grouped = defaultdict(list)
            for name in numpy_data.keys():
                prefix = "_".join(name.split("_")[:3])
                grouped[prefix].append(name)
            return grouped

        vector_groups = extract_vector_groups(numpy_data)
        n_events = next(iter(numpy_data.values())).shape[0]

        # Initialize keep mask to all True
        keep_mask = np.ones(n_events, dtype=bool)

        # Track removal reasons
        removed_due_to_neg999 = np.zeros(n_events, dtype=bool)
        removed_due_to_inf    = np.zeros(n_events, dtype=bool)
        removed_due_to_nan    = np.zeros(n_events, dtype=bool)

        # Step 1: Check vector groups
        for group_columns in vector_groups.values():
            group_data = np.stack([numpy_data[col] for col in group_columns], axis=1)

            removed_due_to_neg999 |= np.any(group_data == -999, axis=1)
            removed_due_to_inf    |= np.any(~np.isfinite(group_data), axis=1)  # catches +inf, -inf
            removed_due_to_nan    |= np.any(np.isnan(group_data), axis=1)

        # Step 2: Check all scalar columns (not part of vector groups)
        scalar_columns = set(numpy_data.keys()) - {col for group in vector_groups.values() for col in group}

        for col in scalar_columns:
            array = numpy_data[col]
            removed_due_to_neg999 |= (array == -999)
            removed_due_to_inf    |= ~np.isfinite(array)
            removed_due_to_nan    |= np.isnan(array)

        # Final mask: only keep events clean in all respects
        keep_mask &= ~(removed_due_to_neg999 | removed_due_to_inf | removed_due_to_nan)

        # Apply mask to data
        for key in numpy_data:
            numpy_data[key] = numpy_data[key][keep_mask]

        # Print summary
        print(f"Total events:                        {n_events}")
        print(f"Removed due to -999:                 {np.sum(removed_due_to_neg999)}")
        print(f"Removed due to inf or -inf:          {np.sum(removed_due_to_inf)}")
        print(f"Removed due to NaN:                  {np.sum(removed_due_to_nan)}")
        print(f"Remaining after full cleaning:       {np.sum(keep_mask)}")


        # Normalize each column
        normalized_data = {column_name: normalize_data(array) for column_name, array in numpy_data.items()}

        # Save all columns into a single NumPy file
        output_file = f"{output_dir}/{sample_name}.npz"
        np.savez(output_file, **numpy_data)
        print(f"Saved all columns to {output_file}")


# Choose which sample will be processed
#sample = "OS"
sample = "SS"

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