import numpy as np
import os

#sample = "OS"
sample = "SS"

# Section 1: Data loading

# Directory containing the input numpy arrays
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weights/with_PF_candidates/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/weights/with_PF_candidates/mirrored_variables/SS"
    os.makedirs(output_dir, exist_ok=True)

    sample_files = [
        # "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        # "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
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

columns = [
    "V0_PFCand21_jetaxisDeta",
    "V0_PFCand21_jetaxisDphi",
    "V0_PFCand21_logPt",
    "V0_PFCand21_logE",
    "V0_PFCand21_logPtOverV0",
    "V0_PFCand21_logEOverV0",
    "V0_PFCand21_deltaR",
]

# Extract only the specified columns and concatenate the data from different sample files
data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:] for key in columns])
    for sample_file in sample_files
])

# Count NaN, Inf, and length for each column
for i, col in enumerate(columns):
    col_data = data[:, i]
    nan_count = np.isnan(col_data).sum()
    inf_count = np.isinf(col_data).sum()
    total_len = len(col_data)
    print(f"{col}: NaN = {nan_count}, Inf = {inf_count}, Length = {total_len}")