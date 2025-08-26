import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

sample = "SS"
#sample = "OS"

numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"
if sample == "OS":
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/correlations_all_variables"
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
    sample_labels = {
        sample_files[0]: "LL",
        sample_files[1]: "LT",
        sample_files[2]: "TL",
        sample_files[3]: "TT"
    }
else:
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/correlations_all_variables"
    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
    sample_labels = {
        sample_files[0]: "LL",
        sample_files[1]: "LTTL",
        sample_files[2]: "TT"
    }

os.makedirs(output_dir_within_sample, exist_ok=True)

# Variable groups
group1_vars = [
    "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", "V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
    "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", "V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",
    "VV_deta", "VV_dphi", "VV_mVV", "log_VV_mVV"
]

group2_vars = [
    "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",
    "TagJet0_eta", "TagJet0_pt", "TagJet0_phi", "TagJet0_mass", "TagJet0_area",
    "TagJet1_eta", "TagJet1_pt", "TagJet1_phi", "TagJet1_mass", "TagJet1_area"
]

group3_vars = [
    "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
    "V0_SubJet0_eta", "V0_SubJet1_eta", "V1_SubJet0_eta", "V1_SubJet1_eta",
    "V0_SubJet0_phi", "V0_SubJet1_phi", "V1_SubJet0_phi", "V1_SubJet1_phi",
    "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
    "V0_SubJet0_area", "V0_SubJet1_area", "V1_SubJet0_area", "V1_SubJet1_area"
]

group4_vars = [
    "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",
    "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", "V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
]

group5_vars = [
    "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",
    "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", "V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",
]

group6_vars = [
    "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",
    "VV_deta", "VV_dphi", "VV_mVV", "log_VV_mVV"
]

variable_groups = {
    "group1_V0_V1": group1_vars,
    "group2_tag_jets": group2_vars,
    "group3_subjets": group3_vars,
    "group4_TagJJ_V0": group4_vars,
    "group5_TagJJ_V1": group5_vars,
    "group6_TagJJ_VV": group6_vars
}

# Load data
sample_matrices = {}
variable_names = None

for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)

    if variable_names is None:
        variable_names = list(data.files)

    matrix = np.column_stack([data[key] for key in variable_names])
    sample_matrices[sample_file] = matrix

# Correlations and covariances
for sample_file in sample_files:
    matrix = sample_matrices[sample_file]
    label = sample_labels[sample_file]
    df_all = pd.DataFrame(matrix, columns=variable_names)

    for group_name, group_vars in variable_groups.items():
        if not all(var in df_all.columns for var in group_vars):
            print(f"Missing variables in {group_name}, skipping...")
            continue

        df_group = df_all[group_vars]

        # Correlation
        corr = df_group.corr()
        plt.figure(figsize=(len(group_vars) * 0.6, len(group_vars) * 0.6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        plt.title(f"Correlation Matrix: {group_name} ({sample}: {label})")
        plt.tight_layout()
        corr_path = os.path.join(output_dir_within_sample, f"corr_{group_name}_{label}.png")
        plt.savefig(corr_path)
        plt.close()
        print(f"Saved correlation matrix: {corr_path}")

        # Covariance
        cov = df_group.cov()
        plt.figure(figsize=(len(group_vars) * 0.6, len(group_vars) * 0.6))
        sns.heatmap(cov, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        plt.title(f"Covariance Matrix: {group_name} ({sample}: {label})")
        plt.tight_layout()
        cov_path = os.path.join(output_dir_within_sample, f"cov_{group_name}_{label}.png")
        plt.savefig(cov_path)
        plt.close()
        print(f"Saved covariance matrix: {cov_path}")