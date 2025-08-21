import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import dcor

sample = "SS"
# sample = "OS"

numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"
if sample == "OS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/OS/distance_correlations"
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
else:
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/correlation_analysis/SS/distance_correlations"
    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1pPOL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

os.makedirs(output_dir, exist_ok=True)

columns_to_extract = [
            "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
            "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",

            "VV_deta", "VV_dphi", "VV_mVV", 
            
            "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",
]

# Loop over individual files
for fname in sample_files:
    path = os.path.join(numpy_path, fname)
    print(f"\nProcessing: {fname}")
    data = np.load(path)

    # Validate required columns
    missing = [col for col in columns_to_extract if col not in data.files]
    if missing:
        raise KeyError(f"{fname} is missing columns: {missing}")

    # Load into DataFrame
    df = pd.DataFrame({col: data[col] for col in columns_to_extract}).dropna()

    # Compute distance correlation matrix
    n = len(columns_to_extract)
    dcor_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dcor_matrix[i, j] = dcor.distance_correlation(
                df[columns_to_extract[i]].values,
                df[columns_to_extract[j]].values
            )

    dcor_df = pd.DataFrame(dcor_matrix, index=columns_to_extract, columns=columns_to_extract)

    # File-safe name
    short_name = os.path.splitext(fname)[0]

    # Save CSV
    csv_path = os.path.join(output_dir, f"{short_name}_dcor_matrix.csv")
    dcor_df.to_csv(csv_path)
    print(f"Saved matrix to: {csv_path}")

    # Plot heatmap
    plt.figure(figsize=(14, 12))
    sns.heatmap(dcor_df, cmap='coolwarm', annot=True, fmt=".2f", square=True,
                xticklabels=True, yticklabels=True, cbar_kws={'label': 'Distance Correlation'})
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.title(f"Distance Correlation Matrix\n{short_name}", fontsize=14)
    plt.tight_layout()

    heatmap_path = os.path.join(output_dir, f"{short_name}_dcor_heatmap_less_variables.png")
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"Saved heatmap to: {heatmap_path}")
