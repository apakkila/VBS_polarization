# Polarization state analysis for Vector Boson Scattering

# This document contains the implementation for a Gaussian Mixture Model (GMM) model
# for analyzing polarization states in Vector Boson Scattering (VBS) processes.

# Importing required libraries
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.utils import resample
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score

# Choose which sample the model is trained on
sample = "OS"
#sample = "SS"

# Section 1: Data loading

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/gmm/weights/OS"
    os.makedirs(output_dir, exist_ok=True)

    plots_dir = "/eos/user/a/apakkila/VBS_ML_project/cluster_plots/gmm/OS"
    os.makedirs(plots_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/gmm/weights/SS"
    os.makedirs(output_dir, exist_ok=True)

    plots_dir = "/eos/user/a/apakkila/VBS_ML_project/cluster_plots/gmm/SS"
    os.makedirs(plots_dir, exist_ok=True)

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}

# Load data from each file
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}

# Print the length of each array (column) in each sample file
for sample_file in sample_files:
    print(f"\nLengths for sample: {sample_file}")
    for key in data_dict[sample_file]:
        array = data_dict[sample_file][key]
        print(f"  {key}: {len(array)}")

number_of_samples_per_file = data_dict[sample_files[2]]['V0_p_theta'].shape[0]
print(f"Number of samples per file: {number_of_samples_per_file}") # total of 75177 samples in each file
number_of_samples = len(data_dict) * number_of_samples_per_file
print(number_of_samples)

# Prepare the training data by concenating the different sample files
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in data_dict[sample_file].keys()])
    for sample_file in sample_files
])

training_data = training_data[:, [0, 1, 2, 3]]

# Initialize labels for the training data
if sample == "OS":
    labels = np.array(['LL'] * number_of_samples_per_file + ['LT'] * number_of_samples_per_file + ['TL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)
elif sample == "SS":
    labels = np.array(['LL'] * number_of_samples_per_file + ['LTTL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)


# Section 2: defining the GMM

gmm = GaussianMixture(n_components=4)
gmm.fit(training_data)

cluster_labels = gmm.predict(training_data)

score = adjusted_rand_score(labels, cluster_labels)
print(f"Adjusted Rand Index: {score:.3f}")

plt.scatter(training_data[:, 0], training_data[:, 2], c=cluster_labels, cmap='viridis')
plt.xlabel('V0_p_theta')
plt.ylabel('V0_z_j')
plt.title('Gaussian Mixture Model Clustering')

plot_path = os.path.join(plots_dir, f"scatter_plot.png")
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")