from minisom import MiniSom
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"

#sample = "OS"
sample = "SS"

# Section 1: Data loading

if sample == "OS":
    # Directory to save the trained SOM model weights
    plots_dir = "/eos/user/a/apakkila/VBS_ML_project/cluster_plots/som/OS"
    os.makedirs(plots_dir, exist_ok=True)

    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weight/OS"
    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
elif sample == "SS":
    plots_dir = "/eos/user/a/apakkila/VBS_ML_project/cluster_plots/som/SS"
    os.makedirs(plots_dir, exist_ok=True)

    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weights/SS"

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

number_of_samples_per_file = len(data_dict[sample_files[1]]['V0_p_theta'])

# Prepare the training data by concenating the different sample files
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in data_dict[sample_file].keys()])
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
input_weights_file = "som_weights_SS_with_lr_0.7000_sigma_2.0000_input_data_samples_223953.p"
input_file_path = os.path.join(weight_dir, input_weights_file)

with open(input_file_path, 'rb') as infile:
    som = pickle.load(infile)

print(f"SOM model downloaded from: {input_file_path}")


w_x, w_y = zip(*[som.winner(d) for d in training_data])
w_x = np.array(w_x)
w_y = np.array(w_y)

colors = ['C0', 'C1', 'C2', 'C3']

# Plotting the U-matrix, i.e., the distance between neighboring neurons
plt.figure(figsize=(8, 8))
plt.pcolor(som.distance_map().T, cmap='gist_yarg') 
plt.colorbar()

# for c in np.unique(labels):
#     idx_target = labels == c
#     color_index = label_names.index(c)

#     plt.scatter(
#         w_x[idx_target] + .5 + (np.random.rand(np.sum(idx_target)) - .5) * .8,
#         w_y[idx_target] + .5 + (np.random.rand(np.sum(idx_target)) - .5) * .8,
#         s=50,
#         c=colors[color_index],
#         label=c
#     )
# plt.legend(loc='upper right')
# plt.grid()

plot_path = os.path.join(plots_dir, f"u_matrix_{input_weights_file}.png")
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")