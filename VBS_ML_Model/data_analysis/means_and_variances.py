import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from sklearn.feature_selection import VarianceThreshold

#sample = "OS"
sample = "SS"

# Section 1: Data loading

# Directory containing the input numpy arrays
#numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays_with_PF_candidates"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/feature_selection/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/means_and_variances/SS"
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

columns_to_extract = [
    "V0_p_theta", "V0_z_j_leading", "V0_z_j_subleading", 
    "V1_p_theta", "V1_z_j_leading", "V1_z_j_subleading",

    "V0_z_j_subleading_mirrored", "V1_z_j_subleading_mirrored",

    "VV_deta","VV_mVV", "VV_dphi",

    "VV_dphi_mirrored",  
    
    "TagJJ_dphi", "TagJJ_mJJ", "TagJJ_deta", 
    "TagJJ_deta_mirrored",
    
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


# Print the length of each array (column) in each sample file
for sample_file in sample_files:
    print(f"\nLengths for sample: {sample_file}")
    for key in data_dict[sample_file]:
        array = data_dict[sample_file][key]
        print(f"  {key}: {len(array)}")

# Computing means and variances for each feature across all sample files
means = {}
variances = {}

for sample_file in sample_files:
    print(f"Processing sample: {sample_file}")
    for key in data_dict[sample_file]:
        if key in columns_to_extract:
            array = data_dict[sample_file][key]
            if key not in means:
                means[key] = []
                variances[key] = []
            means[key].append(np.mean(array))
            variances[key].append(np.var(array))

# Convert means and variances to DataFrames for better visualization
means_df = pd.DataFrame(means)
variances_df = pd.DataFrame(variances)

# Save means and variances to CSV files
means_file = os.path.join(output_dir, "means.csv")
variances_file = os.path.join(output_dir, "variances.csv")
means_df.to_csv(means_file, index=False)
variances_df.to_csv(variances_file, index=False)