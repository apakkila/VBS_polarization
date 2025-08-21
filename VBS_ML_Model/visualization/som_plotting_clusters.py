from minisom import MiniSom
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle
import re

# Directory containing the input numpy arrays
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

#sample = "OS"
sample = "SS"

# Section 1: Data loading

if sample == "OS":
    # Directory to save the trained SOM model weights
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/som/with_PF_candidates/mean_adjusted/OS"
    os.makedirs(cluster_plots_dir, exist_ok=True)

    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weights/with_PF_candidates/mean_adjusted/OS"
    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
elif sample == "SS":
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/som/with_PF_candidates/mirrored_variables/SS"
    feature_importance_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/feature_importance_plots/som/with_PF_candidates/mirrored_variables/SS"

    os.makedirs(cluster_plots_dir, exist_ok=True)
    os.makedirs(feature_importance_plots_dir, exist_ok=True)

    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weights/with_PF_candidates/mirrored_variables/SS"

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}

# features = [
#             "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", "V0_pt",
#             "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", "V1_pt",

#             "VV_deta", "VV_dphi", "log_VV_mVV",

#             "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",

#             "TagJet0_eta", "TagJet0_pt", "TagJet0_mass",
#             "TagJet1_eta", "TagJet1_pt", "TagJet1_mass",

#             "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
#             "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
#         ]

features = [
            "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
            "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",

            "VV_deta", "VV_dphi", "VV_mVV", #"log_VV_mVV",

            # "V0_pt", "V0_eta", "V0_phi", "V0_mass", "V0_area",
            # "V1_pt", "V1_eta", "V1_phi", "V1_mass", "V1_area",

            # "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
            # "V0_SubJet0_eta", "V0_SubJet1_eta", "V1_SubJet0_eta", "V1_SubJet1_eta",
            # "V0_SubJet0_phi", "V0_SubJet1_phi", "V1_SubJet0_phi", "V1_SubJet1_phi",
            # "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
            # "V0_SubJet0_area", "V0_SubJet1_area", "V1_SubJet0_area", "V1_SubJet1_area",

            "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",

            # "TagJet0_eta", "TagJet0_pt", "TagJet0_phi", "TagJet0_mass", "TagJet0_area",
            # "TagJet1_eta", "TagJet1_pt", "TagJet1_phi", "TagJet1_mass", "TagJet1_area"
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

# Find matching weight file
matching_files = [f for f in os.listdir(weight_dir) if run_id in f and f.endswith(".p")]

if not matching_files:
    raise FileNotFoundError(f"No weight file found in {weight_dir} with run_id '{run_id}'")

# If multiple matches, choose the most recent by timestamp in filename (if applicable)
input_weights_file = sorted(matching_files)[-1]

input_file_path = os.path.join(weight_dir, input_weights_file)

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
    missing = [col for col in features if col not in data_dict[sample_file]]
    if missing:
        raise KeyError(f"Missing columns in {sample_file}: {missing}")

# Extract only the specified columns
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in features])
    for sample_file in sample_files
])


# Choose only p_theta, z_j and deta values for both SubJets
#training_data = training_data[:, [0, 1, 2, 3, 4]]

# Initialize labels for the training data
if sample == "OS":
    labels = np.array(['LL'] * number_of_samples_per_file + ['LT'] * number_of_samples_per_file + ['TL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)
    label_names = ['LL', 'LT', 'TL', 'TT']
elif sample == "SS":
    labels = np.array(['LL'] * number_of_samples_per_file + ['LTTL'] * number_of_samples_per_file + ['TT'] * number_of_samples_per_file)
    label_names = ['LL', 'LTTL', 'TT']

# Section 1: Load the weights of the SOM model


print(f"SOM model downloaded from: {input_file_path}")


# Select last 10% of samples for each label
selected_indices = []

for label in np.unique(labels):
    label_indices = np.where(labels == label)[0]
    n_select = max(1, int(len(label_indices) * 0.1))  # at least one
    selected_indices.extend(label_indices[-n_select:])

selected_indices = np.array(sorted(selected_indices))

# Subset the data and labels
training_data_subset = training_data[selected_indices]
labels_subset = labels[selected_indices]

print(f'Quantazation error: {som.quantization_error(training_data)}')

# Compute SOM winners only for the selected subset
w_x, w_y = zip(*[som.winner(d) for d in training_data])
w_x = np.array(w_x)
w_y = np.array(w_y)

colors = ['C0', 'C1', 'C2', 'C3']

# Plotting the U-matrix
plt.figure(figsize=(8, 8))
plt.pcolor(som.distance_map().T, cmap='gist_yarg')
plt.colorbar()

# Plot the winners for each label in the subset
for c in np.unique(labels):
    idx_target = labels == c
    color_index = label_names.index(c)

    plt.scatter(
        w_x[idx_target] + .5 + (np.random.rand(np.sum(idx_target)) - .5) * .8,
        w_y[idx_target] + .5 + (np.random.rand(np.sum(idx_target)) - .5) * .8,
        s=50,
        c=colors[color_index],
        label=c
    )

plt.legend(loc='upper right')
plt.grid()

plot_path = os.path.join(cluster_plots_dir, f"u_matrix_{input_weights_file}_all_points.png")
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")


# Plotting feature importances

X_nodes, Y_nodes, _ = som._weights.shape

W = som.get_weights()
plt.figure(figsize=(10, 10))
for i, f in enumerate(features):
    plt.subplot(3, 4, i+1)
    plt.title(f)
    plt.pcolor(W[:,:,i].T, cmap='coolwarm')
    plt.xticks(np.arange(X_nodes+1))
    plt.yticks(np.arange(Y_nodes+1))
    plt.tight_layout()
    plt.colorbar()
plt.savefig(os.path.join(feature_importance_plots_dir, f"feature_importance_{f}.png"))
