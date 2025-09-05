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

# Functions for initializing the Chebyshev distance metric and the corresponding SOM
def chebyshev_distance(a, b):
    return np.max(np.abs(a - b))

class ChebyshevSOM(MiniSom):
    def _find_bmu(self, x):
        min_dist = np.inf
        bmu = None
        for i in range(self._weights.shape[0]):
            for j in range(self._weights.shape[1]):
                w = self._weights[i, j, :]
                dist = chebyshev_distance(x, w)
                if dist < min_dist:
                    min_dist = dist
                    bmu = np.array([i, j])
        return bmu



#----------------------------------------------------------------------
# 0. Load the training data from the files and import the SOM weights
#----------------------------------------------------------------------


# Directory containing the input numpy arrays
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
# numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates_filtered"

sample = "OS"
#sample = "SS"
#sample = "both"
polarization_fraction_biased = False


if sample == "OS":
    # Directory to save the trained SOM model weights
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/som/final_plots/guassian_euclidean/regular_variables/parameter_search/OS"
    feature_importance_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/feature_importance/som/final_plots/guassian_euclidean/regular_variables/parameter_search/OS"
    
    os.makedirs(cluster_plots_dir, exist_ok=True)
    os.makedirs(feature_importance_plots_dir, exist_ok=True)

    weight_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/parameter_search/OS"
    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
elif sample == "SS":
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/som/final_plots/guassian_euclidean/regular_variables/100k/SS"
    feature_importance_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/feature_importance/som/final_plots/guassian_euclidean/regular_variables/100k/SS"

    os.makedirs(cluster_plots_dir, exist_ok=True)
    os.makedirs(feature_importance_plots_dir, exist_ok=True)

    weight_dir  = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/100k/SS"

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
elif sample == "both":
    cluster_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/cluster_plots/som/final_plots/guassian_euclidean/regular_variables/grid_search/both"
    feature_importance_plots_dir = "/eos/user/a/apakkila/VBS_ML_project/plots/feature_importance/som/final_plots/guassian_euclidean/regular_variables/grid_search/both"

    os.makedirs(cluster_plots_dir, exist_ok=True)
    os.makedirs(feature_importance_plots_dir, exist_ok=True)

    weight_dir  = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/grid_search/both"

    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

# Dictionary to store loaded data
data_dict = {}

# columns_to_extract = [
#             "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", "V0_pt",
#             "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading", "V1_pt",

#             "VV_deta", "VV_dphi", "log_VV_mVV",

#             "TagJJ_deta", "TagJJ_dphi", "TagJJ_mJJ",

#             "TagJet0_eta", "TagJet0_pt", "TagJet0_mass",
#             "TagJet1_eta", "TagJet1_pt", "TagJet1_mass",

#             "V0_SubJet0_pt", "V0_SubJet1_pt", "V1_SubJet0_pt", "V1_SubJet1_pt",
#             "V0_SubJet0_mass", "V0_SubJet1_mass", "V1_SubJet0_mass", "V1_SubJet1_mass",
#         ]


## Columns including the first 20 PF candidates

# columns_to_extract = [
#     "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
#     "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",

#     #"V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

    # "VV_deta", "log_VV_mVV", "VV_dphi",

#     #"VV_dphi_mirrored",  
    
    # "TagJJ_deta", 
    
#     "TagJJ_dphi", "TagJJ_mJJ",

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
# ]

## Columns with variables with mirrored values

# columns_to_extract = [
#     "V0_p_theta", "V0_z_j_leading", #"V0_z_j_subleading", 
#     "V1_p_theta", "V1_z_j_leading", #"V1_z_j_subleading",

#     "V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

#     "VV_deta",#"VV_mVV",
#     "log_VV_mVV",
#     "VV_dphi_mirrored", 
    
#     "TagJJ_dphi", "TagJJ_mJJ",
#     "TagJJ_deta_mirrored", 
# ]

columns_to_extract = [
    # "V0_p_theta", "V1_p_theta", "V0_z_j_leading", "V1_z_j_leading", "V0_z_j_subleading", "V1_z_j_subleading", 
    # "VV_deta", "log_VV_mVV", "VV_dphi",
    # "TagJJ_deta",#"TagJJ_dphi", #"TagJJ_mJJ",

    'V0_p_theta', 'V1_p_theta', 'V0_z_j_leading', 'V1_z_j_leading', 'V0_z_j_subleading', 'V1_z_j_subleading', 'VV_deta', 'VV_dphi', 'TagJJ_deta' # OS

#     #"log_TagJJ_mJJ",
#     #"log_TagJet0_mass", "log_TagJet1_mass",
#     #"log_TagJet0_pt", "log_TagJet1_pt",
]

feature_names = [
    r"$p_{\theta}$ of V0", r"$p_{\theta}$ of V1", r"$z^{leading}_{j}$ of V0", r"$z^{leading}_{j}$ of V1", r"$z^{subleading}_{j}$ of V0", r"$z^{subleading}_{j}$ of V1", 
    r"$\Delta\eta$ of VV", r"$\Delta\phi$ of VV", #r"log($m_{VV}$) of VV", 
    r"$\Delta\eta$ of TagJJ", #r"$\Delta\phi$ of TagJJ", #r"log($m_{JJ})$ of TagJJ",
]

# columns_to_extract = [
#     "V0_p_theta", "V1_p_theta", "V0_z_j_leading", "V1_z_j_leading", "V0_z_j_subleading", "V1_z_j_subleading", 
#     "VV_deta", "log_VV_mVV", 
#     "VV_dphi_mirrored",
#     "TagJJ_deta_mirrored", #"TagJJ_dphi", "TagJJ_mJJ"
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
run_id = "run006"

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
# 1. Plot the distance map of the trained SOM
#----------------------------------------------------------------------


print(f"SOM model downloaded from: {input_file_path}")

xx, yy = som.get_euclidean_coordinates()
umatrix = som.distance_map()
weights = som.get_weights()

f = plt.figure(figsize=(10,10))
ax = f.add_subplot(111)

ax.set_aspect('equal')

# iteratively add hexagons
for i in range(weights.shape[0]):
    for j in range(weights.shape[1]):
        wy = yy[(i, j)] * np.sqrt(3) / 2
        hex = RegularPolygon((xx[(i, j)], wy), 
                             numVertices=6, 
                             radius=.95 / np.sqrt(3),
                             facecolor=cm.Blues(umatrix[i, j]), 
                             alpha=.4, 
                             edgecolor='gray')
        ax.add_patch(hex)

xrange = np.arange(weights.shape[0])
yrange = np.arange(weights.shape[1])
plt.xticks(xrange-.5, xrange)
plt.yticks(yrange * np.sqrt(3) / 2, yrange)

divider = make_axes_locatable(plt.gca())
ax_cb = divider.new_horizontal(size="5%", pad=0.05)    
cb1 = colorbar.ColorbarBase(ax_cb, cmap=cm.Blues, 
                            orientation='vertical', alpha=.4)
cb1.ax.get_yaxis().labelpad = 16
cb1.ax.set_ylabel('Distance from nodes in the neighbourhood',
                  rotation=270, fontsize=16)
plt.gcf().add_axes(ax_cb)
if sample == "SS":
    plt.title("Distance map of the trained SOM for same-sign sample")
else:
    plt.title("Distance map of the trained SOM for opposite-sign sample")

plot_path = os.path.join(cluster_plots_dir, f"{run_id}_u_matrix_{input_weights_file}.png")
plt.savefig(plot_path)
plt.show()



#----------------------------------------------------------------------
# 2. Plot density maps for each polarization sample
#----------------------------------------------------------------------


polarizations = ['LL', 'LT', 'TL', 'TT'] if sample == "OS" else ['LL', 'LTTL', 'TT']

fractions_SS = [0.1, 0.29, 0.61]
fractions_OS = [0.1, 0.145, 0.145, 0.61]

# Step 1: Loop through each sample file separately to create density map for each polarization
for sf_idx, sample_file in enumerate(sample_files):

    # Extract the training data for this specific file
    if polarization_fraction_biased:
        if sample == "SS":
            data_this_file = np.column_stack([
                data_dict[sample_file][key][:int(total_number_of_samples*fractions_SS[sf_idx])] for key in columns_to_extract
            ])
            print(f'{int(total_number_of_samples*fractions_SS[sf_idx])} loaded from {sample_file}')
        elif sample == "OS":
            data_this_file = np.column_stack([
                data_dict[sample_file][key][:int(total_number_of_samples*fractions_OS[sf_idx])] for key in columns_to_extract
            ])
    else:
        data_this_file = np.column_stack([
            data_dict[sample_file][key][:number_of_samples_per_file] for key in columns_to_extract
        ])

    # Select which part of the data to use for density map
    part_of_data = max(1, int(1 * len(data_this_file)))
    data_last = data_this_file[-part_of_data:]

    # Step 2: Count points assigned to each neuron
    point_counts = np.zeros((weights.shape[0], weights.shape[1]), dtype=int)
    for x in data_last:
        w = som.winner(x)  # (i, j)
        point_counts[w] += 1

    # Step 3: Normalize to [0,1] for colormap
    max_count = point_counts.max()
    #max_count = np.sum(point_counts)  # Normalize by total number of points
    print(max_count)
    density_map = point_counts / max_count if max_count > 0 else point_counts

    # Step 4: Plot density map for this file
    f = plt.figure(figsize=(10, 10))
    ax = f.add_subplot(111)
    ax.set_aspect('equal')

    # Add hexagons colored by density
    for i in range(weights.shape[0]):
        for j in range(weights.shape[1]):
            wy = yy[(i, j)] * np.sqrt(3) / 2
            hex = RegularPolygon(
                (xx[(i, j)], wy),
                numVertices=6,
                radius=.95 / np.sqrt(3),
                facecolor=cm.Blues(density_map[i, j]),
                alpha=.8,
                edgecolor='gray'
            )
            ax.add_patch(hex)

    # Step 5: Set ticks
    xrange = np.arange(weights.shape[0])
    yrange = np.arange(weights.shape[1])
    plt.xticks(xrange - .5, xrange)
    plt.yticks(yrange * np.sqrt(3) / 2, yrange)
    if sample == "SS":
        plt.title(f"Density map for {polarizations[sf_idx]} polarized samples for same-sign sample")
    else:
        plt.title(f"Density map for {polarizations[sf_idx]} polarized samples for opposite-sign sample")

    # Step 6: Colorbar
    divider = make_axes_locatable(plt.gca())
    ax_cb = divider.new_horizontal(size="5%", pad=0.05)
    cb1 = colorbar.ColorbarBase(ax_cb, cmap=cm.Blues, orientation='vertical', alpha=.8)
    cb1.ax.get_yaxis().labelpad = 16
    cb1.ax.set_ylabel('Density of events per node', rotation=270, fontsize=16)
    plt.gcf().add_axes(ax_cb)

    # Step 7: Save plot
    plot_path = os.path.join(
        cluster_plots_dir,
        f"{run_id}_u_matrix_{input_weights_file}_density_map_last1pct_{os.path.splitext(sample_file)[0]}_last5pct.png"
    )
    plt.savefig(plot_path)
    plt.close()

    print(f"Saved density map for {sample_file} (last 1%) at {plot_path}")



#----------------------------------------------------------------------
# 3. Plot the value distributions (feature importance planes)
#    of the trained SOM model variables
#----------------------------------------------------------------------


# Hexagonal feature planes
xx, yy = som.get_euclidean_coordinates()
weights = som.get_weights()  # shape: (X_nodes, Y_nodes, num_features)

plt.figure(figsize=(10, 15))
for i, f in enumerate(columns_to_extract):
    ax = plt.subplot(9, 3, i+1)
    ax.set_aspect('equal')
    ax.set_title(feature_names[i])

    # Plot each neuron as a hexagon colored by feature value
    for xi in range(weights.shape[0]):
        for yi in range(weights.shape[1]):
            wy = yy[(xi, yi)] * np.sqrt(3) / 2
            color_val = weights[xi, yi, i]
            hexagon = RegularPolygon(
                (xx[(xi, yi)], wy),
                numVertices=6,
                radius=.95 / np.sqrt(3),
                facecolor=cm.coolwarm(
                    (color_val - weights[:, :, i].min()) /
                    (weights[:, :, i].max() - weights[:, :, i].min())
                ),
                edgecolor='gray'
            )
            ax.add_patch(hexagon)

    # Axis ticks for hex layout
    #ax.set_xticks(np.arange(weights.shape[0]) - .5)
    #ax.set_yticks(np.arange(weights.shape[1]) * np.sqrt(3) / 2)
    ax.set_xlim(-1, weights.shape[0])
    ax.set_ylim(-1, weights.shape[1] * np.sqrt(3) / 2 + 1)

    # Add colorbar
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="5%", pad=0.05)
    cb = colorbar.ColorbarBase(
        ax_cb,
        cmap=cm.coolwarm,
        norm=plt.Normalize(vmin=weights[:, :, i].min(),
                           vmax=weights[:, :, i].max()),
        orientation='vertical'
    )
    plt.gcf().add_axes(ax_cb)

plt.tight_layout()
plt.savefig(os.path.join(feature_importance_plots_dir,
                         f'{run_id}_feature_importances_hexagonal.png'))



#----------------------------------------------------------------------
# 4. Compute the overlaps between the polarizations
#----------------------------------------------------------------------


from itertools import combinations
import numpy as np

density_maps = {}

for sf_idx, sample_file in enumerate(sample_files):
    if polarization_fraction_biased:
        if sample == "SS":
            data = np.column_stack([
                data_dict[sample_file][key][:int(total_number_of_samples*fractions_SS[sf_idx])] for key in columns_to_extract
            ])
        elif sample == "OS":
            data = np.column_stack([
                data_dict[sample_file][key][:int(total_number_of_samples*fractions_OS[sf_idx])] for key in columns_to_extract
            ])
    else:
        data = np.column_stack([
            data_dict[sample_file][key][:number_of_samples_per_file] for key in columns_to_extract
        ])
    
    # Take only the last 1% of events
    n_last = max(1, int(len(data) * 0.5))
    data_last = data[-n_last:]
    
    point_counts = np.zeros((weights.shape[0], weights.shape[1]), dtype=int)
    for x in data_last:
        w = som.winner(x)
        point_counts[w] += 1
    
    density_maps[sample_file] = point_counts / point_counts.max() if point_counts.max() > 0 else point_counts

# Compare overlaps
for (f1, f2) in combinations(sample_files, 2):
    D1, D2 = density_maps[f1], density_maps[f2]
    
    # Min-overlap fraction
    overlap_fraction = np.sum(np.minimum(D1, D2)) / np.sum(D1)
    
    # Symmetric overlap fraction
    overlap_symmetric = (np.sum(np.minimum(D1, D2)) /
                         np.sum(np.maximum(D1, D2)))
    
    # Correlation
    correlation = np.corrcoef(D1.flatten(), D2.flatten())[0,1]
    
    print(f"{f1} vs {f2}:")
    print(f"  Overlap fraction (D1 perspective): {overlap_fraction:.3f}")
    print(f"  Symmetric overlap fraction: {overlap_symmetric:.3f}")
    print(f"  Pearson correlation: {correlation:.3f}")

if sample == "SS":
    D_LL = density_maps[sample_files[0]]
    D_LTTL = density_maps[sample_files[1]]
    D_TT = density_maps[sample_files[2]]

    overlap_LL_LTTL = (np.sum(np.minimum(D_LL, D_LTTL)) /
                         np.sum(np.maximum(D_LL, D_LTTL)))
    
    overlap_LL_TT = (np.sum(np.minimum(D_LL, D_TT)) /
                         np.sum(np.maximum(D_LL, D_TT)))

    overlap_LL_LTTL_TT = (np.sum(np.minimum(D_LL, D_LTTL, D_TT)) /
                         np.sum(np.maximum(D_LL, D_LTTL, D_TT)))

    print(f"Overlap fraction LL vs LL: {overlap_LL_LTTL:.3f}")
    print(f"Overlap fraction LL vs LT: {overlap_LL_TT:.3f}")
    print(f"Overlap fraction LL vs TL: {overlap_LL_LTTL_TT:.3f}")
else:
    D_LL = density_maps[sample_files[0]]
    D_LT = density_maps[sample_files[1]]
    D_TL = density_maps[sample_files[2]]
    D_TT = density_maps[sample_files[3]]

    # LL vs LL
    intersection_LL_LL = np.where((D_LL > 0) & (D_LL > 0), np.minimum(D_LL, D_LL), 0)
    overlap_fraction_LL_LL = np.sum(intersection_LL_LL) / np.sum(D_LL)

    # LL vs LT
    intersection_LL_LT = np.where((D_LL > 0) & (D_LT > 0), np.minimum(D_LL, D_LT), 0)
    overlap_fraction_LL_LT = np.sum(intersection_LL_LT) / np.sum(D_LL)

    # LL vs TL
    intersection_LL_TL = np.where((D_LL > 0) & (D_TL > 0), np.minimum(D_LL, D_TL), 0)
    overlap_fraction_LL_TL = np.sum(intersection_LL_TL) / np.sum(D_LL)

    # LL vs TT
    intersection_LL_TT = np.where((D_LL > 0) & (D_TT > 0), np.minimum(D_LL, D_TT), 0)
    overlap_fraction_LL_TT = np.sum(intersection_LL_TT) / np.sum(D_LL)

    # LL vs LT, TL
    intersection_LL_LT_TL = np.where((D_LL > 0) & (D_LT > 0) & (D_TL > 0), np.minimum.reduce([D_LL, D_LT, D_TL]), 0)
    overlap_fraction_LL_LT_TL = np.sum(intersection_LL_LT_TL) / np.sum(D_LL)

    # LL vs LT, TT
    intersection_LL_LT_TT = np.where((D_LL > 0) & (D_LT > 0) & (D_TT > 0), np.minimum.reduce([D_LL, D_LT, D_TT]), 0)
    overlap_fraction_LL_LT_TT = np.sum(intersection_LL_LT_TT) / np.sum(D_LL)

    # LL vs TL, TT
    intersection_LL_TL_TT = np.where((D_LL > 0) & (D_TL > 0) & (D_TT > 0), np.minimum.reduce([D_LL, D_TL, D_TT]), 0)
    overlap_fraction_LL_TL_TT = np.sum(intersection_LL_TL_TT) / np.sum(D_LL)

    # LT vs LT, TL, TT
    intersection_LL_LT_TL_TT = np.where((D_LL > 0) & (D_LT > 0) & (D_TL > 0) & (D_TT > 0), np.minimum.reduce([D_LL, D_LT, D_TL, D_TT]), 0)
    overlap_fraction_LL_LT_TL_TT = np.sum(intersection_LL_LT_TL_TT) / np.sum(D_LL)

    # Print overlap fractions
    print(f"Overlap fraction LL vs LL: {overlap_fraction_LL_LL:.3f}")
    print(f"Overlap fraction LL vs LT: {overlap_fraction_LL_LT:.3f}")
    print(f"Overlap fraction LL vs TL: {overlap_fraction_LL_TL:.3f}")
    print(f"Overlap fraction LL vs TT: {overlap_fraction_LL_TT:.3f}")
    print(f"Overlap fraction LL vs LT, TL: {overlap_fraction_LL_LT_TL:.3f}")
    print(f"Overlap fraction LL vs LT, TT: {overlap_fraction_LL_LT_TT:.3f}")
    print(f"Overlap fraction LL vs TL, TT: {overlap_fraction_LL_TL_TT:.3f}")
    print(f"Overlap fraction LL vs LT, TL, TT: {overlap_fraction_LL_LT_TL_TT:.3f}")



#----------------------------------------------------------------------
# 5. Cluster the nodes SOM using Agglomerative clustering
#----------------------------------------------------------------------


from sklearn.cluster import AgglomerativeClustering

# Step 1: Get SOM neuron weights as (num_neurons, num_features)

weights = som.get_weights()  # shape: (x, y, features)
num_x, num_y, num_features = weights.shape
flat_weights = weights.reshape(num_x * num_y, num_features)

# Step 2: Choose number of meta-clusters
n_clusters = 3

# Step 3: Fit hierarchical clustering on neuron weights
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
cluster_labels = clustering.fit_predict(flat_weights)

# Step 4: Reshape back to SOM grid
cluster_grid = cluster_labels.reshape(num_x, num_y)

# Step 5: Plot clusters on top of the U-matrix
f = plt.figure(figsize=(10, 10))
ax = f.add_subplot(111)
ax.set_aspect('equal')

colors = cm.tab10(np.linspace(0, 1, n_clusters))

for i in range(num_x):
    for j in range(num_y):
        wy = yy[(i, j)] * np.sqrt(3) / 2
        hex = RegularPolygon(
            (xx[(i, j)], wy),
            numVertices=6,
            radius=.95 / np.sqrt(3),
            facecolor=colors[cluster_grid[i, j]],
            alpha=0.6,
            edgecolor='k'
        )
        ax.add_patch(hex)

# Optional: overlay sample markers
label_to_marker = {'LL': 'o', 'LTTL': '+', 'TT': 'x'} if sample == "SS" else {'LL': 'o', 'LT': '+', 'TL': 'x', 'TT': 's'}
label_to_color  = {'LL': 'C0', 'LTTL': 'C1', 'TT': 'C2'} if sample == "SS" else {'LL': 'C0', 'LT': 'C1', 'TL': 'C2', 'TT': 'C3'}

for cnt, x in enumerate(training_data):
    w = som.winner(x)
    wx, wy = som.convert_map_to_euclidean(w)
    wy = wy * np.sqrt(3) / 2
    lbl = labels[cnt]
    plt.plot(
        wx, wy,
        label_to_marker[lbl],
        markerfacecolor='None',
        markeredgecolor=label_to_color[lbl],
        markersize=8,
        markeredgewidth=1.5
    )

# Legend for meta-clusters
legend_elements = [Line2D([0], [0], marker='h', color='w', label=f'Cluster {k}',
                          markerfacecolor=colors[k], markersize=12, linestyle='None') 
                   for k in range(n_clusters)]
ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xticks(np.arange(num_x) - .5, np.arange(num_x))
plt.yticks(np.arange(num_y) * np.sqrt(3) / 2, np.arange(num_y))


plot_path = os.path.join(cluster_plots_dir, f"u_matrix_{input_weights_file}_meta_clusters.png")
plt.savefig(plot_path, bbox_inches='tight')
plt.close()