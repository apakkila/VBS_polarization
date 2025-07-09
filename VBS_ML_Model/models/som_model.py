# Polarization state analysis for Vector Boson Scattering

# This document contains the implementation for a Self-Organizing Map (SOM) model
# for analyzing polarization states in Vector Boson Scattering (VBS) processes.

# Importing required libraries
import ROOT
from minisom import MiniSom
import numpy as np
import pandas as pd
import os

# Enable multi-threading for ROOT (optional, improves performance)
ROOT.EnableImplicitMT(4)


# Section 1: Data loading

# Directory containing the numpy arrays
numpy_dir = "/afs/cern.ch/user/a/apakkila/VBS_polarization/VBS_ML_Model/data/output_numpy_arrays"

# List of sample files to load
sample_files = [
    "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
    "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
]

# Dictionary to store loaded data
data_dict = {}

# Load data from each file
for sample_file in sample_files:
    file_path = f"{numpy_dir}/{sample_file}"
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}


# Section 2: Defining the model parameters for the SOM

# Define the dimensions of the SOM grid computed as sqrt(5*sqrt(number of samples))
som_shape = (20, 20) 

# Define the input data dimensions
input_len = len(data_dict[sample_files[0]].keys())  # Number of features (columns) in the input data

# Initialize the MiniSom model
som = MiniSom(
    x=som_shape[0], 
    y=som_shape[1], 
    input_len=input_len, 
    sigma=1.0, 
    learning_rate=0.5, 
    decay_function='asymptotic_decay',  # Decay function for learning rate
    neighborhood_function='gaussian',        # Neighborhood function
    topology='hexagonal',                     # Topology of the SOM grid
    sigma_decay_function='asymptotic_decay'
)

# Prepare the training data (take only 500 samples from each file)
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:500] for key in data_dict[sample_file].keys()])
    for sample_file in sample_files
])

# Initialize the SOM weights using PCA
som.pca_weights_init(training_data)
print("SOM weights initialized.")


# Section 3: Training the SOM

print("Training the SOM...")
som.train(
    data=training_data, 
    num_iteration=1000,  # Number of iterations
    verbose=True,       # Verbose output for training progress
)
print("SOM training completed.")


# Section 4: Evaluation

# Evaluate the trained SOM (e.g., map input data to SOM nodes)
mapped_nodes = [som.winner(x) for x in training_data]
print("Mapped nodes:", mapped_nodes)


# Section 5: Visualization

# Each neuron represents a cluster
winner_coordinates = np.array([som.winner(x) for x in training_data]).T

# With np.ravel_multi_index we convert the bidimensional coordinates to a monodimensional index
cluster_index = np.ravel_multi_index(winner_coordinates, som_shape)

import matplotlib.pyplot as plt

# Ensure the "./plots" folder exists
plots_dir = "./plots"
os.makedirs(plots_dir, exist_ok=True)

# Plotting the clusters using the first 2 dimensions of the data
plt.figure(figsize=(1, 1))
for c in np.unique(cluster_index):
    plt.scatter(training_data[cluster_index == c, 0],
                training_data[cluster_index == c, 1], label='Cluster ' + str(c), alpha=0.7)

# Plotting centroids
for centroid in som.get_weights():
    plt.scatter(centroid[:, 0], centroid[:, 1], marker='.', 
                s=5, linewidths=35, color='k', label='centroid')

# Add labels, title, and legend
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("SOM Clusters and Centroids")


# Save the plot to the "./plots" folder
plot_path = os.path.join(plots_dir, "som_clusters.png")
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")