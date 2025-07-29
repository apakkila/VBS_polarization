import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from sklearn.feature_selection import VarianceThreshold

sample = "SS"
#sample = "OS"

numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"
if sample == "OS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/feature_selection/OS"
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
    sample_labels = {
        sample_files[0]: "LL",
        sample_files[1]: "LT",
        sample_files[2]: "TL",
        sample_files[3]: "TT"
    }
else:
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/feature_selection/SS"
    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
    sample_labels = {
        sample_files[0]: "LL",
        sample_files[1]: "LTTL",
        sample_files[2]: "TT"
    }

os.makedirs(output_dir, exist_ok=True)

# Dictionary to store loaded data
data_dict = {}

# Load data from each file
for sample_file in sample_files:
    file_path = os.path.join(numpy_path, sample_file)
    print(f"Loading data from {file_path}...")
    data = np.load(file_path)
    data_dict[sample_file] = {key: data[key] for key in data.files}

# Extract only the specified columns
X_list = []
y_list = []

label_map = {'LL': 0, 'LTTL': 1, 'TT': 2}

n_per_sample = 3000
rng = np.random.default_rng(seed=42)

for sample_file in sample_files:
    data = data_dict[sample_file]
    
    # Stack features into (N, F) shape
    X_sample = np.column_stack([data[key] for key in data.keys()])
    
    # Randomly select n_per_sample indices
    total_rows = X_sample.shape[0]
    selected_indices = rng.choice(total_rows, size=n_per_sample, replace=False)
    
    X_sample_sub = X_sample[selected_indices]
    
    # Get label
    label = sample_labels[sample_file]
    y_sample_sub = np.full((n_per_sample,), label_map[label])
    
    X_list.append(X_sample_sub)
    y_list.append(y_sample_sub)

training_data = np.concatenate(X_list, axis=0)
y = np.concatenate(y_list, axis=0)

print("Final data shape:", training_data.shape)
print("Label distribution:", np.unique(y, return_counts=True))


# Check the variances of the features

training_data = training_data.astype(float)
print("Shape:", training_data.shape)

variance_plot_dir = os.path.join(output_dir, "variance_plots")
os.makedirs(variance_plot_dir, exist_ok=True)

variances = np.var(training_data, axis=0)

print(f"Min variance: {np.min(variances)}, max variance: {np.max(variances)}")

plt.hist(variances, bins=50)
plt.xlabel("Feature Variance")
plt.ylabel("Count")
plt.title("Distribution of Feature Variances")
plt.savefig(os.path.join(variance_plot_dir, "feature_variances.png"))
plt.close()

# Sequential forward/backward selection

from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
import time

estimators = [
    LogisticRegression(max_iter=1000),
    RandomForestClassifier(n_estimators=100),
    SVC(kernel='linear'),
    GradientBoostingClassifier(n_estimators=100)
]

for model in estimators:
    print(f"\nEvaluating model: {model.__class__.__name__}")
    
    # Get input feature names
    input_features = np.array(list(data_dict[sample_files[0]].keys()))
    
    # Sequential forward selection
    tic_fwd = time.time()
    sfs_forward = SequentialFeatureSelector(
        model, n_features_to_select=12, direction="forward", cv=3
    ).fit(training_data, y)
    toc_fwd = time.time()

    print("Forward selection features:")
    print(input_features[sfs_forward.get_support()])
    print(f"Done in {toc_fwd - tic_fwd:.2f}s")

    # Sequential backward selection
    tic_bwd = time.time()
    sfs_backward = SequentialFeatureSelector(
        model, n_features_to_select=12, direction="backward", cv=3
    ).fit(training_data, y)
    toc_bwd = time.time()

    print("Backward selection features:")
    print(input_features[sfs_backward.get_support()])
    print(f"Done in {toc_bwd - tic_bwd:.2f}s")