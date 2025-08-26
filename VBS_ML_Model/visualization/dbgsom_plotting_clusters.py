import numpy as np
import pandas as pd
import os
import pickle
from sklearn.utils import resample
import time
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

from dbgsom.dbgsom_ import DBGSOM

# Function to get the next run ID based on existing weight files
def get_next_run_id(output_dir, prefix="run"):
    existing_files = [f for f in os.listdir(output_dir) if f.startswith(f"som_weights_{sample}_{prefix}")]
    run_nums = []
    for f in existing_files:
        match = re.search(rf"{prefix}(\d+)", f)
        if match:
            run_nums.append(int(match.group(1)))
    next_run = max(run_nums, default=0) + 1
    return f"{prefix}{next_run:03d}"

#----------------------------------------------------------------------
# 0. Load the training data from the files
#----------------------------------------------------------------------

#sample = "OS"
sample = "SS"

polarization_fraction_biased = False

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/dbgsom/gaussian_euclidean/regular_variables/tests/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

elif sample == "SS":
    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/dbgsom/gaussian_euclidean/regular_variables/tests/SS"
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/dbgsom/gaussian_euclidean/regular_variables/tests/SS"

    os.makedirs(cluster_plots_dir, exist_ok=True)

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}

# Load data from each file
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}

# features = [
#             "V0_p_theta", "V0_z_j_leading", #"V0_z_j_subleading", 
#             "V1_p_theta", "V1_z_j_leading", #"V1_z_j_subleading",

#             "V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

#             "VV_deta", "VV_mVV", #"VV_dphi",

#             "VV_dphi_mirrored",  
            
#             "TagJJ_dphi", "TagJJ_mJJ", #"TagJJ_deta", 

#             "TagJJ_deta_mirrored",

#             #"log_VV_mVV",

#             # "V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
#             # "V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",

#             # "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
#             # "V0_SubJet0_eta", "V0_SubJet1_eta", "V1_SubJet0_eta", "V1_SubJet1_eta",
#             # "V0_SubJet0_phi", "V0_SubJet1_phi", "V1_SubJet0_phi", "V1_SubJet1_phi",
#             # "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
#             # "V0_SubJet0_area", "V0_SubJet1_area", "V1_SubJet0_area", "V1_SubJet1_area",

#             # "TagJet0_eta", "TagJet0_pt", "TagJet0_phi", "TagJet0_mass", "TagJet0_area",
#             # "TagJet1_eta", "TagJet1_pt", "TagJet1_phi", "TagJet1_mass", "TagJet1_area"
#         ]

columns_to_extract = [
    "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
    "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",
    "VV_deta", "VV_dphi", "log_VV_mVV",
    "TagJJ_deta", 

#     # "V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

    # "VV_mVV",
#     # "VV_dphi_mirrored",  
#     "TagJJ_dphi", "TagJJ_mJJ",
#     # "TagJJ_deta_mirrored",
    
    # "V0_PFCand10_jetaxisDeta", "V0_PFCand10_jetaxisDphi", "V0_PFCand10_logPt", "V0_PFCand10_logE", "V0_PFCand10_logPtOverV0", "V0_PFCand10_logEOverV0", "V0_PFCand10_deltaR",
    # "V0_PFCand11_jetaxisDeta", "V0_PFCand11_jetaxisDphi", "V0_PFCand11_logPt", "V0_PFCand11_logE", "V0_PFCand11_logPtOverV0", "V0_PFCand11_logEOverV0", "V0_PFCand11_deltaR",
    # "V0_PFCand12_jetaxisDeta", "V0_PFCand12_jetaxisDphi", "V0_PFCand12_logPt", "V0_PFCand12_logE", "V0_PFCand12_logPtOverV0", "V0_PFCand12_logEOverV0", "V0_PFCand12_deltaR",
    # "V0_PFCand13_jetaxisDeta", "V0_PFCand13_jetaxisDphi", "V0_PFCand13_logPt", "V0_PFCand13_logE", "V0_PFCand13_logPtOverV0", "V0_PFCand13_logEOverV0", "V0_PFCand13_deltaR",
    # "V0_PFCand14_jetaxisDeta", "V0_PFCand14_jetaxisDphi", "V0_PFCand14_logPt", "V0_PFCand14_logE", "V0_PFCand14_logPtOverV0", "V0_PFCand14_logEOverV0", "V0_PFCand14_deltaR",
    # "V0_PFCand15_jetaxisDeta", "V0_PFCand15_jetaxisDphi", "V0_PFCand15_logPt", "V0_PFCand15_logE", "V0_PFCand15_logPtOverV0", "V0_PFCand15_logEOverV0", "V0_PFCand15_deltaR",
    # "V0_PFCand16_jetaxisDeta", "V0_PFCand16_jetaxisDphi", "V0_PFCand16_logPt", "V0_PFCand16_logE", "V0_PFCand16_logPtOverV0", "V0_PFCand16_logEOverV0", "V0_PFCand16_deltaR",
    # "V0_PFCand17_jetaxisDeta", "V0_PFCand17_jetaxisDphi", "V0_PFCand17_logPt", "V0_PFCand17_logE", "V0_PFCand17_logPtOverV0", "V0_PFCand17_logEOverV0", "V0_PFCand17_deltaR",
    # "V0_PFCand18_jetaxisDeta", "V0_PFCand18_jetaxisDphi", "V0_PFCand18_logPt", "V0_PFCand18_logE", "V0_PFCand18_logPtOverV0", "V0_PFCand18_logEOverV0", "V0_PFCand18_deltaR",
    # "V0_PFCand19_jetaxisDeta", "V0_PFCand19_jetaxisDphi", "V0_PFCand19_logPt", "V0_PFCand19_logE", "V0_PFCand19_logPtOverV0", "V0_PFCand19_logEOverV0", "V0_PFCand19_deltaR",


    # "V1_PFCand10_jetaxisDeta", "V1_PFCand10_jetaxisDphi", "V1_PFCand10_logPt", "V1_PFCand10_logE", "V1_PFCand10_logPtOverV1", "V1_PFCand10_logEOverV1", "V1_PFCand10_deltaR",
    # "V1_PFCand11_jetaxisDeta", "V1_PFCand11_jetaxisDphi", "V1_PFCand11_logPt", "V1_PFCand11_logE", "V1_PFCand11_logPtOverV1", "V1_PFCand11_logEOverV1", "V1_PFCand11_deltaR",
    # "V1_PFCand12_jetaxisDeta", "V1_PFCand12_jetaxisDphi", "V1_PFCand12_logPt", "V1_PFCand12_logE", "V1_PFCand12_logPtOverV1", "V1_PFCand12_logEOverV1", "V1_PFCand12_deltaR",
    # "V1_PFCand13_jetaxisDeta", "V1_PFCand13_jetaxisDphi", "V1_PFCand13_logPt", "V1_PFCand13_logE", "V1_PFCand13_logPtOverV1", "V1_PFCand13_logEOverV1", "V1_PFCand13_deltaR",
    # "V1_PFCand14_jetaxisDeta", "V1_PFCand14_jetaxisDphi", "V1_PFCand14_logPt", "V1_PFCand14_logE", "V1_PFCand14_logPtOverV1", "V1_PFCand14_logEOverV1", "V1_PFCand14_deltaR",
    # "V1_PFCand15_jetaxisDeta", "V1_PFCand15_jetaxisDphi", "V1_PFCand15_logPt", "V1_PFCand15_logE", "V1_PFCand15_logPtOverV1", "V1_PFCand15_logEOverV1", "V1_PFCand15_deltaR",
    # "V1_PFCand16_jetaxisDeta", "V1_PFCand16_jetaxisDphi", "V1_PFCand16_logPt", "V1_PFCand16_logE", "V1_PFCand16_logPtOverV1", "V1_PFCand16_logEOverV1", "V1_PFCand16_deltaR",
    # "V1_PFCand17_jetaxisDeta", "V1_PFCand17_jetaxisDphi", "V1_PFCand17_logPt", "V1_PFCand17_logE", "V1_PFCand17_logPtOverV1", "V1_PFCand17_logEOverV1", "V1_PFCand17_deltaR",
    # "V1_PFCand18_jetaxisDeta", "V1_PFCand18_jetaxisDphi", "V1_PFCand18_logPt", "V1_PFCand18_logE", "V1_PFCand18_logPtOverV1", "V1_PFCand18_logEOverV1", "V1_PFCand18_deltaR",
    # "V1_PFCand19_jetaxisDeta", "V1_PFCand19_jetaxisDphi", "V1_PFCand19_logPt", "V1_PFCand19_logE", "V1_PFCand19_logPtOverV1", "V1_PFCand19_logEOverV1", "V1_PFCand19_deltaR",
]

# features = [
#     "V0_p_theta", "V1_p_theta", "V0_z_j_leading", "V1_z_j_leading", "V0_z_j_subleading", "V1_z_j_subleading", 
#     "VV_deta", "VV_dphi", "log_VV_mVV",
#     "TagJJ_deta", #"TagJJ_dphi", #"TagJJ_mJJ",
#     #"log_TagJJ_mJJ",
#     #"log_TagJet0_mass", "log_TagJet1_mass",
#     #"log_TagJet0_pt", "log_TagJet1_pt",
# ]


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

# Define run_id
run_id = "run001"

# Find matching weight file with the corresponding run_id
matching_files = [f for f in os.listdir(weight_dir) if run_id in f and f.endswith(".p")]

if not matching_files:
    raise FileNotFoundError(f"No weight file found in {weight_dir} with run_id '{run_id}'")

# If multiple matches, choose the most recent by timestamp in filename (if applicable)
input_weights_file = sorted(matching_files)[-1]

input_file_path = os.path.join(weight_dir, input_weights_file)

# Read the SOM weights from the file
with open(input_file_path, 'rb') as infile:
    som = pickle.load(infile)

# Try to extract number_of_samples from filename
match = re.search(r"samples_(\d+)", input_weights_file)
if match:
    total_samples = int(match.group(1))
    number_of_samples_per_file = total_samples // len(sample_files)
    print(f"Extracted number_of_samples_per_file: {number_of_samples_per_file}")
else:
    raise ValueError(f"Could not extract number_of_samples from filename: {input_weights_file}")

# Ensure all requested columns are present in each file
for sample_file in sample_files:
    missing = [col for col in columns_to_extract if col not in data_dict[sample_file]]
    if missing:
        raise KeyError(f"Missing columns in {sample_file}: {missing}")


if polarization_fraction_biased:
    total_number_of_samples = 300000
    if sample == "SS":
        training_data = np.concatenate([
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.1)] for key in columns_to_extract]),
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.29)] for key in columns_to_extract]),
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.61)] for key in columns_to_extract])
        ])
        print(f'Polarization fraction biased training dataset for SS with {int(total_number_of_samples*0.1)}, {int(total_number_of_samples*0.29)}, {int(total_number_of_samples*0.61)} events')
    elif sample == "OS":
        training_data = np.concatenate([
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.1)] for key in columns_to_extract]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.145)] for key in columns_to_extract]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.145)] for key in columns_to_extract]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.61)] for key in columns_to_extract]),
        ])
        print("Polarization fraction biased training dataset for OS")

            # Initialize labels for the training data
    if sample == "OS":
        labels = np.array(['LL'] * int(total_number_of_samples*0.1) + ['LT'] * int(total_number_of_samples*0.145) + ['TL'] * int(total_number_of_samples*0.145) + ['TT'] * int(total_number_of_samples*0.61))
        label_names = ['LL', 'LT', 'TL', 'TT']
    elif sample == "SS":
        labels = np.array(['LL'] * int(total_number_of_samples*0.1) + ['LTTL'] * int(total_number_of_samples*0.29) + ['TT'] * int(total_number_of_samples*0.61))
        label_names = ['LL', 'LTTL', 'TT']
elif polarization_fraction_biased == False:


    # Ensure all requested columns are present in each file
    for sample_file in sample_files:
        missing = [col for col in columns_to_extract if col not in data_dict[sample_file]]
        if missing:
            raise KeyError(f"Missing columns in {sample_file}: {missing}")

    # Extract only the specified columns
    training_data = np.concatenate([
        np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in columns_to_extract])
        for sample_file in sample_files
    ])

    # Initialize labels for the training data
    if sample == "OS":
        labels = np.array(['LL'] * number_of_samples_per_file + ['LT'] * number_of_samples_per_file + ['TL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)
        label_names = ['LL', 'LT', 'TL', 'TT']
    elif sample == "SS":
        labels = np.array(['LL'] * number_of_samples_per_file + ['LTTL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)
        label_names = ['LL', 'LTTL', 'TT']
    print("Non-biased training dataset loaded")



#----------------------------------------------------------------------
# 1. Plot the cluster plots for the trained DBGSOM model
#----------------------------------------------------------------------

counts_for_overlaps = []

for sf_idx, sample_file in enumerate(sample_files):
    
    print(f"Processing sample file: {sample_file}")
    data_this_file = np.column_stack([
            data_dict[sample_file][key][:number_of_samples_per_file] for key in columns_to_extract
        ])

    # Compute point counts for each neuron in the trained model
    winning_nodes = som._get_winning_neurons(data_this_file, n_bmu=1)
    unique, counts = np.unique(winning_nodes, axis=0, return_counts=True)
    counts_for_overlaps.append(counts)
    coordinates = np.array(som.neurons_)
    
    print(f"Coordinate ranges - X: {coordinates[:, 0].min()}-{coordinates[:, 0].max()}, Y: {coordinates[:, 1].min()}-{coordinates[:, 1].max()}")
    print(f"Number of neurons: {len(coordinates)}")
    
    # Determine the actual SOM grid dimensions and offsets from the coordinates
    min_x, max_x = int(coordinates[:, 0].min()), int(coordinates[:, 0].max())
    min_y, max_y = int(coordinates[:, 1].min()), int(coordinates[:, 1].max())
    
    # Calculate grid dimensions (add 1 because we need to include both min and max)
    grid_width = max_x - min_x + 1
    grid_height = max_y - min_y + 1
    
    print(f"Creating density map with dimensions: {grid_width} x {grid_height}")
    print(f"Coordinate offsets - X offset: {-min_x}, Y offset: {-min_y}")
    
    # Create density map with correct dimensions
    density_map = np.zeros((grid_width, grid_height), dtype=int)
    
    # Fill the density map (shift coordinates to start from 0)
    for coordinate, count in zip(coordinates, counts):
        x = int(coordinate[0]) - min_x
        y = int(coordinate[1]) - min_y
        density_map[x, y] = count

    # Normalize the counts to [0, 1] range for better visualization
    if np.max(density_map) > 0:
        density_map = density_map.astype(float) / np.max(density_map)

    # Plot the density map for this sample file
    plt.figure(figsize=(12, 12), dpi=300)
    plt.imshow(density_map.T, cmap='viridis', origin='lower')
    plt.colorbar(label='Normalized Count')
    plt.title(f'Density Map of Winning Neurons for {sample_file}')
    plt.xlabel('SOM X')
    plt.ylabel('SOM Y')
    plt.savefig(f"{cluster_plots_dir}/dbgsom_density_map_{sample}_sf{sf_idx+1}_{run_id}_samples_{total_samples}.png", dpi=300, bbox_inches="tight")
    plt.close()


# Compute overlaps between sample distributions

LL_counts = counts_for_overlaps[0]
LTTL_counts = counts_for_overlaps[1]
TT_counts = counts_for_overlaps[2]

overlap_LL_LTTL = np.sum(np.minimum(LL_counts, LTTL_counts))
overlap_LL_TT = np.sum(np.minimum(LL_counts, TT_counts))

overlap_fraction_LL_LTTL = overlap_LL_LTTL / np.sum(LL_counts) if np.sum(LL_counts) > 0 else 0
overlap_fraction_LL_TT = overlap_LL_TT / np.sum(LL_counts) if np.sum(LL_counts) > 0 else 0

print(f"Overlap LL-LTTL: {overlap_LL_LTTL}/{np.sum(LL_counts)} ({overlap_fraction_LL_LTTL:.2%} of LL)")
print(f"Overlap LL-TT: {overlap_LL_TT}/{np.sum(LL_counts)} ({overlap_fraction_LL_TT:.2%} of LL)")


# # f = plt.figure(figsize=(5, 5), dpi=300)
# labels = list(dict(som.som_.nodes.data("label")).values())
# coordinates = np.array(som.neurons_)
# print(labels)
# print(type(labels))

# p = (
#     so.Plot(x=coordinates[:, 0], y=coordinates[:, 1], color=labels)
#     .add(so.Dot())
#     .scale(color="Set1")
# )

# p.save(f"{cluster_plots_dir}/dbgsom_cluster_plot_{sample}_{run_id}_samples_{total_samples}.png", dpi=300, bbox_inches="tight")
