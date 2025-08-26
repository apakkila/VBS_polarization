import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

sample = "SS"
#sample = "OS"

numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"
if sample == "OS":
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/correlations_all_variables"
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
    sample_labels = {
        sample_files[0]: "LL",
        sample_files[1]: "LT",
        sample_files[2]: "TL",
        sample_files[3]: "TT"
    }
else:
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/PF_candidates/combined"
    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
    sample_labels = [
        "LL", "LTTL", "TT"
    ]

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

group7_V0_PF_candidates = [
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
]

group8_V1_PF_candidates = [
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

variable_groups = {
    # "group1_V0_V1": group1_vars,
    # "group2_tag_jets": group2_vars,
    # "group3_subjets": group3_vars,
    # "group4_TagJJ_V0": group4_vars,
    # "group5_TagJJ_V1": group5_vars,
    # "group6_TagJJ_VV": group6_vars
    "group1_V0_PF_candidates": group7_V0_PF_candidates,
    "group2_V1_PF_candidates": group8_V1_PF_candidates,
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


for matrix in sample_matrices.values():
    print(matrix.shape)

sample_matrices_list = list(sample_matrices.values())

variables_V0 = ["jetaxisDeta", "jetaxisDphi", "logPt", "logE", "logPtOverV0", "logEOverV0", "deltaR"]
variables_V1 = ["jetaxisDeta", "jetaxisDphi", "logPt", "logE", "logPtOverV1", "logEOverV1", "deltaR"]

# Map variable names to column indices
name_to_index = {name: idx for idx, name in enumerate(variable_names)}

# Collect stats per variable
new_statistics_V0 = [{var: [] for var in variables_V0} for _ in range(len(sample_matrices))]

for i, (sample_file, sample_matrix) in enumerate(sample_matrices.items()):
    for candidate_variable in group7_V0_PF_candidates:
        for variable in variables_V0:
            if candidate_variable.endswith(variable):
                col_idx = name_to_index[candidate_variable]
                new_statistics_V0[i][variable].append(sample_matrix[:, col_idx])

# Convert lists to arrays
for i in range(len(new_statistics_V0)):
    for var in new_statistics_V0[i]:
        print(len(new_statistics_V0[i][var]))
        new_statistics_V0[i][var] = np.concatenate(new_statistics_V0[i][var])

print(type(new_statistics_V0))


for i, variable_list in enumerate(new_statistics_V0):
    # combine the arrays from variables list into a pd.DataFrame
    df_all = pd.DataFrame()
    for j, (key, value) in enumerate(variable_list.items()):
        df_all.insert(j, key, value)

    label = sample_labels[i]
    corr = df_all.corr()
    plt.figure(figsize=(15, 15))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title(f"Correlation Matrix: {label}")
    plt.tight_layout()
    corr_path = os.path.join(output_dir_within_sample, f"corr_{label}.png")
    plt.savefig(corr_path)
    plt.close()
    print(f"Saved correlation matrix: {corr_path}")

    # Covariance
    cov = df_all.cov()
    plt.figure(figsize=(15, 15))
    sns.heatmap(cov, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title(f"Covariance Matrix: {label})")
    plt.tight_layout()
    cov_path = os.path.join(output_dir_within_sample, f"cov_{label}.png")
    plt.savefig(cov_path)
    plt.close()
    print(f"Saved covariance matrix: {cov_path}")