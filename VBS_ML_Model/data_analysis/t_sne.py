import os
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sample = "OS"
#sample = "SS"

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/t_sne/deta_and_mVV/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/t_sne/SS"
    os.makedirs(output_dir, exist_ok=True)

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}

number_of_samples_per_file = 10000

# Load data from each file
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}

# Take only the selected keys for t-SNE
selected_keys = ["VV_deta", "VV_mVV"]

# Concatenate data from all sample files
data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in selected_keys])
    for sample_file in sample_files
])

# # Concatenate data from all sample files
# data = np.concatenate([
#     np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in data_dict[sample_file].keys()])
#     for sample_file in sample_files
# ])

labels = np.array(['LL'] * number_of_samples_per_file + ['LT'] * number_of_samples_per_file + ['TL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)


# Apply t-SNE to the data
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, n_iter=1000, random_state=42)
data_tsne = tsne.fit_transform(data)

# Create a DataFrame for easy plotting
tsne_df = pd.DataFrame(data_tsne, columns=['tSNE1', 'tSNE2'])
tsne_df['label'] = labels

# Plot the t-SNE result
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tsne_df, x='tSNE1', y='tSNE2', hue='label', palette='deep', alpha=0.7, s=30)
plt.title(f"t-SNE of W Polarization Samples ({sample})")
plt.grid(True)
plt.tight_layout()

# Save to file
plt.savefig(os.path.join(output_dir, f"tSNE_{sample}.png"))


# Plot each polarization state separately
unique_labels = tsne_df['label'].unique()

for label in unique_labels:
    plt.figure(figsize=(6, 5))
    subset = tsne_df[tsne_df['label'] == label]
    
    sns.scatterplot(data=subset, x='tSNE1', y='tSNE2', alpha=0.7, s=30)
    plt.title(f"t-SNE of {label} Polarization ({sample})")
    plt.grid(True)
    plt.tight_layout()
    
    # Save each plot
    filename = f"tSNE_{sample}_{label}.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.show()
