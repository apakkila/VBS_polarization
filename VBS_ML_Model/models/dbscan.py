# Polarization state analysis for Vector Boson Scattering

# This document contains the implementation for a DBSCAN model
# for analyzing polarization states in Vector Boson Scattering (VBS) processes.

# Importing required libraries
import ROOT
from minisom import MiniSom
import numpy as np
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


# Section 1: Data loading

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"

# Directory to save the trained SOM model weights
output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/dbscan_model/weights"
os.makedirs(output_dir, exist_ok=True)

neighbor_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/models/dbscan_model/neighbor_plots"
os.makedirs(neighbor_plots_dir, exist_ok=True)

plots_dir = "/eos/user/a/apakkila/VBS_ML_project/cluster_plots/dbscan"
os.makedirs(plots_dir, exist_ok=True)

# List of sample files to load
sample_files = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
]

# Dictionary to store loaded data
data_dict = {}

# Load data from each file
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}

number_of_samples_per_file = 1000

# Prepare the training data by concenating the different sample files
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in data_dict[sample_file].keys()])
    for sample_file in sample_files
])

# Section 2: Computing the epsilon and min_samples parameters for DBSCAN
from sklearn.neighbors import NearestNeighbors

# Function to plot k-distance graph
def plot_k_distance_graph(X, k, title):
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(training_data)
    distances, _ = neigh.kneighbors(training_data)
    distances = np.sort(distances[:, k-1])
    plt.figure(figsize=(10, 6))
    plt.plot(distances)
    plt.xlabel('Points')
    plt.ylabel(f'{k}-th nearest neighbor distance')
    plt.title('K-distance Graph')
    plt.grid()
    print(f"Saving k-distance graph for k={k}...")
    plt.savefig(os.path.join(neighbor_plots_dir, f'k_distance_k_{k}_{title}.png'))
    plt.close()


plot_k_distance_graph(training_data, k=5, title="entire_dataset")



# Section 3: Training the DBSCAN model

epsilon = 0.18  # Chosen based on k-distance graph
min_samples = 8  # 2 * num_features (2D data)
dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
clusters = dbscan.fit_predict(training_data)

# Visualize the results
plt.figure(figsize=(10, 6))
scatter = plt.scatter(training_data[:, 4], training_data[:, 5], c=clusters, cmap='viridis')
plt.colorbar(scatter)
plt.title('DBSCAN Clustering Results')
plt.xlabel('V0_p_theta')
plt.ylabel('V0_z_j')
plt.savefig(os.path.join(plots_dir, 'dbscan_clustering_results.png'))
plt.close()