import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

sample = "OS"
#sample = "SS"

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"
if sample == "OS":
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/correlations_within_sample"
    output_dir_between_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/correlations_between_samples"
    os.makedirs(output_dir_between_sample, exist_ok=True)
    
    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]

    # Short sample name mapping
    sample_labels = {
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "LL",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "LT",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "TL",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "TT"
    }
elif sample == "SS":
    output_dir_within_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/correlations_within_sample"
    output_dir_between_sample = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/correlations_between_samples"
    os.makedirs(output_dir_between_sample, exist_ok=True)

    sample_files = [
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]

    sample_labels = {
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "LL",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "LTTL",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz": "TT"
    }


# Dictionary to store data matrices per sample
sample_matrices = {}
variable_names = None  # Will capture the order of variables

# Load data and build sample matrices
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)

    if variable_names is None:
        variable_names = list(data.files)

    matrix = np.column_stack([data[key] for key in variable_names])
    sample_matrices[sample_file] = matrix

# Align all sample matrices to the same number of rows
min_length = min(matrix.shape[0] for matrix in sample_matrices.values())
for sample_file in sample_matrices:
    sample_matrices[sample_file] = sample_matrices[sample_file][:min_length, :]


# Compute and save within-sample covariance matrices
os.makedirs(output_dir_within_sample, exist_ok=True)

for sample_file in sample_files:
    matrix = sample_matrices[sample_file]
    label = sample_labels[sample_file]

    # Compute covariance matrix for the sample (variables vs variables)
    corr_matrix = np.corrcoef(matrix, rowvar=False)

    # Convert to DataFrame for plotting
    df_corr = pd.DataFrame(corr_matrix, index=variable_names, columns=variable_names)

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_corr, annot=True, fmt=".2f", cmap="coolwarm",
                xticklabels=variable_names, yticklabels=variable_names, square=True)
    plt.title(f"Within-Sample Correlation\n{sample}: {label}")
    plt.tight_layout()

    # Save heatmap
    heatmap_path = os.path.join(output_dir_within_sample, f"within_corr_{label}.png")
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Saved within-sample correlation heatmap: {heatmap_path}")