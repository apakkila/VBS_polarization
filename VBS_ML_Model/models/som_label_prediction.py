from minisom import MiniSom
import os
import numpy as np
import pandas as pd
import pickle
import re
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm, colorbar
from matplotlib.lines import Line2D
from itertools import islice
from collections import Counter

#----------------------------------------------------------------------
# 0. Load the training data from the files and import the SOM weights
#----------------------------------------------------------------------


# Directory containing the input numpy arrays
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

#sample = "OS"
sample = "SS"
polarization_fraction_biased = True


if sample == "OS":
    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/parameter_search/OS"
    
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
elif sample == "SS":
    weight_dir  = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/polarization_fraction_biased/SS"

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}


columns_to_extract = [
    "V0_p_theta", "V1_p_theta", "V0_z_j_leading", "V1_z_j_leading", "V0_z_j_subleading", "V1_z_j_subleading", 
    "VV_deta", "VV_dphi", "log_VV_mVV",
    "TagJJ_deta", #"TagJJ_dphi", #"TagJJ_mJJ",
    #"log_TagJJ_mJJ",
    #"log_TagJet0_mass", "log_TagJet1_mass",
    #"log_TagJet0_pt", "log_TagJet1_pt",
]

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
run_id = "run004"

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
        print(f'Polarization fraction biased training dataset for SS with {int(total_number_of_samples*0.1)}, {int(total_number_of_samples*0.29)}, {int(total_number_of_samples*0.61)} events')
    if sample == "OS":
        labels = np.array(['LL'] * int(total_number_of_samples*0.1) + ['LT'] * int(total_number_of_samples*0.145) + ['TL'] * int(total_number_of_samples*0.145) + ['TT'] * int(total_number_of_samples*0.61))
        label_names = ['LL', 'LT', 'TL', 'TT']
    elif sample == "SS":
        labels = np.array(['LL'] * int(total_number_of_samples*0.1) + ['LTTL'] * int(total_number_of_samples*0.29) + ['TT'] * int(total_number_of_samples*0.61))
        label_names = ['LL', 'LTTL', 'TT']
elif polarization_fraction_biased == False:
    number_of_samples_per_file = 100000
    print(f"Number of samples per file: {number_of_samples_per_file}")
    number_of_samples = len(data_dict) * number_of_samples_per_file
    print(number_of_samples)

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

index1 = number_of_samples_per_file+1
index2 = int(1.5*number_of_samples_per_file)

if sample == "SS":
    test_data = np.concatenate([
        np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][100001:115000] for key in columns_to_extract]), 
        np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][100001:143500] for key in columns_to_extract]),
        np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][100001:191500] for key in columns_to_extract]), 
    ])
else:
    test_data = np.concatenate([
        np.column_stack([data_dict[sample_file][key][index1:index2] for key in columns_to_extract])
        for sample_file in sample_files
    ])


# Identify the nodes that have not been activated during training
weights = som.get_weights()
node_activations = som.activation_response(training_data)

# Check the inactive nodes in the network
inactive_nodes = [
    (i, j)
    for i in range(weights.shape[0])
    for j in range(weights.shape[1])
    if node_activations[(i, j)] == 0
]

print("Inactive nodes:", inactive_nodes)
print(len(inactive_nodes))


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))


# Compute the label probabilities from the trained SOM model
label_map = som.labels_map(training_data, labels)
label_map = take(len(label_map), label_map.items())

#print(label_map)

polarization_probabilities = []

# Compute the normalized counts
for coord, counter in label_map:
    total = sum(counter.values())
    if total > 0:
        normalized = Counter({k: v / total for k, v in counter.items()})
    else:
        normalized = Counter()
    polarization_probabilities.append((coord, normalized))

print(len(polarization_probabilities))

# Append the inactive nodes and set their polarization fraction probabilities to zero 
for node in inactive_nodes:
    polarization_probabilities.append((node, Counter()))

#print(polarization_probabilities)


# Compute the winning node for the test_data events and cumulate the polarization probabilities
polarization_probability_dict = dict(polarization_probabilities)
polarization_fractions = Counter()

for x in test_data:
    winner_coord = som.winner(x)
    # polarization_fractions.update({
    #     k: v for k, v in polarization_probability_dict[winner_coord].items() if v > 0.5
    # })
    for pol, v in polarization_probability_dict[winner_coord].items():
        if v > 0.5:
            polarization_fractions[pol] = polarization_fractions.get(pol, 0) + 1

print(polarization_fractions)