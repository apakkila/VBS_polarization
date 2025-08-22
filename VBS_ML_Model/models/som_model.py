# Polarization state analysis for Vector Boson Scattering

# This document contains the implementation for a Self-Organizing Map (SOM) model
# for analyzing polarization states in Vector Boson Scattering (VBS) processes.

# Importing required libraries
from minisom import MiniSom
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.utils import resample
import time
import re
from datetime import datetime

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
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/parameter_search/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/with_PF_candidates/SS"
    os.makedirs(output_dir, exist_ok=True)

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

features = [
    "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
    "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",

#     # "V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

    "VV_deta", "VV_dphi", "log_VV_mVV",
    # "VV_mVV",
#     # "VV_dphi_mirrored",  
    "TagJJ_deta", 
#     "TagJJ_dphi", "TagJJ_mJJ",
#     # "TagJJ_deta_mirrored",
    
    "V0_PFCand10_jetaxisDeta", "V0_PFCand10_jetaxisDphi", "V0_PFCand10_logPt", "V0_PFCand10_logE", "V0_PFCand10_logPtOverV0", "V0_PFCand10_logEOverV0", "V0_PFCand10_deltaR",
    "V0_PFCand11_jetaxisDeta", "V0_PFCand11_jetaxisDphi", "V0_PFCand11_logPt", "V0_PFCand11_logE", "V0_PFCand11_logPtOverV0", "V0_PFCand11_logEOverV0", "V0_PFCand11_deltaR",
    "V0_PFCand12_jetaxisDeta", "V0_PFCand12_jetaxisDphi", "V0_PFCand12_logPt", "V0_PFCand12_logE", "V0_PFCand12_logPtOverV0", "V0_PFCand12_logEOverV0", "V0_PFCand12_deltaR",
    "V0_PFCand13_jetaxisDeta", "V0_PFCand13_jetaxisDphi", "V0_PFCand13_logPt", "V0_PFCand13_logE", "V0_PFCand13_logPtOverV0", "V0_PFCand13_logEOverV0", "V0_PFCand13_deltaR",
    "V0_PFCand14_jetaxisDeta", "V0_PFCand14_jetaxisDphi", "V0_PFCand14_logPt", "V0_PFCand14_logE", "V0_PFCand14_logPtOverV0", "V0_PFCand14_logEOverV0", "V0_PFCand14_deltaR",
    "V0_PFCand15_jetaxisDeta", "V0_PFCand15_jetaxisDphi", "V0_PFCand15_logPt", "V0_PFCand15_logE", "V0_PFCand15_logPtOverV0", "V0_PFCand15_logEOverV0", "V0_PFCand15_deltaR",
    "V0_PFCand16_jetaxisDeta", "V0_PFCand16_jetaxisDphi", "V0_PFCand16_logPt", "V0_PFCand16_logE", "V0_PFCand16_logPtOverV0", "V0_PFCand16_logEOverV0", "V0_PFCand16_deltaR",
    "V0_PFCand17_jetaxisDeta", "V0_PFCand17_jetaxisDphi", "V0_PFCand17_logPt", "V0_PFCand17_logE", "V0_PFCand17_logPtOverV0", "V0_PFCand17_logEOverV0", "V0_PFCand17_deltaR",
    "V0_PFCand18_jetaxisDeta", "V0_PFCand18_jetaxisDphi", "V0_PFCand18_logPt", "V0_PFCand18_logE", "V0_PFCand18_logPtOverV0", "V0_PFCand18_logEOverV0", "V0_PFCand18_deltaR",
    "V0_PFCand19_jetaxisDeta", "V0_PFCand19_jetaxisDphi", "V0_PFCand19_logPt", "V0_PFCand19_logE", "V0_PFCand19_logPtOverV0", "V0_PFCand19_logEOverV0", "V0_PFCand19_deltaR",


    "V1_PFCand10_jetaxisDeta", "V1_PFCand10_jetaxisDphi", "V1_PFCand10_logPt", "V1_PFCand10_logE", "V1_PFCand10_logPtOverV1", "V1_PFCand10_logEOverV1", "V1_PFCand10_deltaR",
    "V1_PFCand11_jetaxisDeta", "V1_PFCand11_jetaxisDphi", "V1_PFCand11_logPt", "V1_PFCand11_logE", "V1_PFCand11_logPtOverV1", "V1_PFCand11_logEOverV1", "V1_PFCand11_deltaR",
    "V1_PFCand12_jetaxisDeta", "V1_PFCand12_jetaxisDphi", "V1_PFCand12_logPt", "V1_PFCand12_logE", "V1_PFCand12_logPtOverV1", "V1_PFCand12_logEOverV1", "V1_PFCand12_deltaR",
    "V1_PFCand13_jetaxisDeta", "V1_PFCand13_jetaxisDphi", "V1_PFCand13_logPt", "V1_PFCand13_logE", "V1_PFCand13_logPtOverV1", "V1_PFCand13_logEOverV1", "V1_PFCand13_deltaR",
    "V1_PFCand14_jetaxisDeta", "V1_PFCand14_jetaxisDphi", "V1_PFCand14_logPt", "V1_PFCand14_logE", "V1_PFCand14_logPtOverV1", "V1_PFCand14_logEOverV1", "V1_PFCand14_deltaR",
    "V1_PFCand15_jetaxisDeta", "V1_PFCand15_jetaxisDphi", "V1_PFCand15_logPt", "V1_PFCand15_logE", "V1_PFCand15_logPtOverV1", "V1_PFCand15_logEOverV1", "V1_PFCand15_deltaR",
    "V1_PFCand16_jetaxisDeta", "V1_PFCand16_jetaxisDphi", "V1_PFCand16_logPt", "V1_PFCand16_logE", "V1_PFCand16_logPtOverV1", "V1_PFCand16_logEOverV1", "V1_PFCand16_deltaR",
    "V1_PFCand17_jetaxisDeta", "V1_PFCand17_jetaxisDphi", "V1_PFCand17_logPt", "V1_PFCand17_logE", "V1_PFCand17_logPtOverV1", "V1_PFCand17_logEOverV1", "V1_PFCand17_deltaR",
    "V1_PFCand18_jetaxisDeta", "V1_PFCand18_jetaxisDphi", "V1_PFCand18_logPt", "V1_PFCand18_logE", "V1_PFCand18_logPtOverV1", "V1_PFCand18_logEOverV1", "V1_PFCand18_deltaR",
    "V1_PFCand19_jetaxisDeta", "V1_PFCand19_jetaxisDphi", "V1_PFCand19_logPt", "V1_PFCand19_logE", "V1_PFCand19_logPtOverV1", "V1_PFCand19_logEOverV1", "V1_PFCand19_deltaR",
]

# features = [
#     "V0_p_theta", "V1_p_theta", "V0_z_j_leading", "V1_z_j_leading", "V0_z_j_subleading", "V1_z_j_subleading", 
#     "VV_deta", "VV_dphi", "log_VV_mVV",
#     "TagJJ_deta", #"TagJJ_dphi", #"TagJJ_mJJ",
#     #"log_TagJJ_mJJ",
#     #"log_TagJet0_mass", "log_TagJet1_mass",
#     #"log_TagJet0_pt", "log_TagJet1_pt",
# ]


# Print the length of each array (column) in each sample file
for sample_file in sample_files:
    print(f"\nLengths for sample: {sample_file}")
    for key in data_dict[sample_file]:
        array = data_dict[sample_file][key]
        print(f"  {key}: {len(array)}")


if polarization_fraction_biased:
    total_number_of_samples = 300000
    if sample == "SS":
        training_data = np.concatenate([
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.1)] for key in features]),
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.29)] for key in features]),
            np.column_stack([data_dict["Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.61)] for key in features])
        ])
        print("Polarization fraction biased training dataset for SS")
    elif sample == "OS":
        training_data = np.concatenate([
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.1)] for key in features]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.145)] for key in features]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.145)] for key in features]),
            np.column_stack([data_dict["Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"][key][:int(total_number_of_samples*0.61)] for key in features]),
        ])
        print("Polarization fraction biased training dataset for OS")
elif polarization_fraction_biased == False:
    number_of_samples_per_file = 5000
    print(f"Number of samples per file: {number_of_samples_per_file}")
    number_of_samples = len(data_dict) * number_of_samples_per_file
    print(number_of_samples)

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


# training_data = np.concatenate([
#     np.column_stack([data_dict[sample_file][key] for key in features])
#     for sample_file in sample_files
# ])

print(f"Training data shape: {training_data.shape}")

#----------------------------------------------------------------------
# 1. Defining the model paramters for the SOM
#----------------------------------------------------------------------

# Define the dimensions of the SOM grid computed as sqrt(5*sqrt(number of samples))
som_shape = (int(np.floor(np.sqrt(5 * np.sqrt(len(training_data))))), int(np.floor(np.sqrt(5 * np.sqrt(len(training_data))))))
#som_shape = (80,80)

# # Grid search for hyperparameters

# # # For gaussian, euclidean
# sigmas = [1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
# lrs = [0.05, 0.1, 0.2, 0.5, 0.8, 1.0]

# For triangle, cosine
# sigmas = [1, 2, 3, 4, 5]
# lrs = [0.01, 0.1, 0.2, 0.5, 1.0]


sigmas = [4.5]
lrs = [0.05]

topology = 'hexagonal'  # 'rectangular' or 'hexagonal'
neighborhood_function = 'gaussian'
activation_distance = 'euclidean'

quantization_errors = []
topographic_errors = []

# Path for logging all runs into one file
log_file_path = os.path.join(output_dir, f'{get_next_run_id(output_dir)}som_training_log.txt')

# If log file doesn't exist, write header
if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as log_file:
        log_file.write("datetime,run_id,number_of_samples,som_shape,lr,sigma,weight_init_elapsed_time,elapsed_time,quantization_error, topographic_error, features\n")


#----------------------------------------------------------------------
# 2. Training the SOM and saving the model weights
#----------------------------------------------------------------------

for sigma in sigmas:
    for lr in lrs:
        print(f"Training SOM with sigma: {sigma}, learning rate: {lr}")

        som = MiniSom(
            x=som_shape[0], 
            y=som_shape[1], 
            input_len=training_data.shape[1], 
            sigma=sigma, 
            learning_rate=lr, 
            neighborhood_function=neighborhood_function,
            activation_distance=activation_distance,
            decay_function='asymptotic_decay',
            topology=topology,
            sigma_decay_function='asymptotic_decay'
        )

        subset = resample(training_data, n_samples=int(0.05 * len(training_data)), random_state=42)

        weight_init_start_time = time.time()
        som.pca_weights_init(subset)
        weight_init_end_time = time.time()
        weight_init_elapsed_time = weight_init_end_time - weight_init_start_time
        print(f"SOM weights initialized in ({weight_init_elapsed_time/60:.2f} minutes).")

        start_time = time.time()
        som.train(
            data=training_data, 
            num_iteration=100,
            verbose=True,
            use_epochs=True,
            random_order=True
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        qe = som.quantization_error(training_data)
        te = som.topographic_error(training_data)
        print(f"SOM training completed in {elapsed_time:.2f} seconds "
            f"({elapsed_time/60:.2f} minutes) with QE {qe} and TE {te}.")

        quantization_errors.append(qe)
        topographic_errors.append(te)

        # Generate run_id
        run_id = get_next_run_id(output_dir)

        if polarization_fraction_biased:
            # Append results to log file
            with open(log_file_path, "a") as log_file:
                log_file.write(
                    f"{datetime.now()},{run_id},{total_number_of_samples},{som_shape},{lr},{sigma},{weight_init_elapsed_time:.4f},{elapsed_time:.4f},{qe:.6f},{te:.6f}, {features}\n"
                )
        else:
            # Append results to log file
            with open(log_file_path, "a") as log_file:
                log_file.write(
                    f"{datetime.now()},{run_id},{number_of_samples},{som_shape},{lr},{sigma},{weight_init_elapsed_time:.4f},{elapsed_time:.4f},{qe:.6f},{te:.6f}, {features}\n"
                )

        # Save the trained SOM model
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if polarization_fraction_biased == True:
            output_file_path = os.path.join(
                output_dir,
                f'som_weights_{sample}_{run_id}_{timestamp}_lr_{lr:.2f}_sigma_{sigma:.2f}_samples_{total_number_of_samples}_{topology}_{neighborhood_function}_{activation_distance}.p'
            )
        else:
            output_file_path = os.path.join(
            output_dir,
            f'som_weights_{sample}_{run_id}_{timestamp}_lr_{lr:.2f}_sigma_{sigma:.2f}_samples_{number_of_samples}_{topology}_{neighborhood_function}_{activation_distance}.p'
        )
        with open(output_file_path, 'wb') as outfile:
            pickle.dump(som, outfile)
        print(f"SOM model saved to: {output_file_path}")


print(f'Quantization errors for different configurations: {quantization_errors}')
print(f'Topographic errors for different configurations: {topographic_errors}')
