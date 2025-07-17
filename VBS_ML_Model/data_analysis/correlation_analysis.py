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
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/correlations_between_samples"
    os.makedirs(output_dir, exist_ok=True)
    
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
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/correlations_between_samples"
    os.makedirs(output_dir, exist_ok=True)

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

# Cross-sample correlation between variables
for source_file in sample_files:
    source_matrix = sample_matrices[source_file]
    source_label = sample_labels[source_file]

    for target_file in sample_files:
        if source_file == target_file:
            continue  # skip self-correlations

        target_matrix = sample_matrices[target_file]
        target_label = sample_labels[target_file]

        corr_matrix = np.zeros((len(variable_names), len(variable_names)))

        for i, var_src in enumerate(variable_names):
            for j, var_tgt in enumerate(variable_names):
                x = source_matrix[:, i]
                y = target_matrix[:, j]
                corr_matrix[i, j] = np.corrcoef(x, y)[0, 1]

        # Convert to DataFrame
        df_cross = pd.DataFrame(corr_matrix, index=variable_names, columns=variable_names)

        # Plot heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(df_cross, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1,
            xticklabels=variable_names, yticklabels=variable_names, square=True)
        plt.title(f"Cross-Sample Correlation\n{sample}: {source_label} → {target_label}")
        plt.tight_layout()

        # Save heatmap
        heatmap_path = os.path.join(output_dir, f"cross_corr_{source_label}_vs_{target_label}.png")
        plt.savefig(heatmap_path)
        plt.close()
        print(f"Saved cross-correlation heatmap: {heatmap_path}")
