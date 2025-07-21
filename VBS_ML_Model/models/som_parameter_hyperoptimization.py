import ROOT
from minisom import MiniSom
import numpy as np
import pandas as pd
import os
import pickle
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK

sample = "OS"
#sample = "SS"

# Section 1: Data loading

# Directory containing the input numpy arrays
numpy_path = "/eos/user/a/apakkila/VBS_ML_project/data/normalized_numpy_arrays"

if sample == "OS":
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.npz"
    ]
elif sample == "SS":
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

number_of_samples_per_file = 10000

# Prepare the training data by concenating the different sample files
training_data = np.concatenate([
    np.column_stack([data_dict[sample_file][key][:number_of_samples_per_file] for key in data_dict[sample_file].keys()])
    for sample_file in sample_files
])

# Choose only p_theta, z_j and deta values for both SubJets
#training_data = training_data[:, [0, 1, 2, 3, 4]]

# Section 2: Hyperparameter optimization for SOM

# Define the dimensions of the SOM grid computed as sqrt(5*sqrt(number of samples))
som_shape = (int(np.floor(np.sqrt(5 * np.sqrt(len(training_data))))), int(np.floor(np.sqrt(5 * np.sqrt(len(training_data))))))

space = {
    'sig': hp.uniform('sigma', 1, 3.5),
    'lr': hp.uniform('learning_rate', 0.2, 1),
}

def som_fn(space):
    sig = space['sig']
    lr = space['lr']
    som = MiniSom(
        x=som_shape[0], 
        y=som_shape[1],
        input_len=training_data.shape[1],
        sigma = sig,
        learning_rate = lr,
        decay_function='asymptotic_decay',
        activation_distance='cosine'
        )

    # Initialize weights
    som.random_weights_init(training_data)
    # Train the SOM — you can adjust the number of iterations as needed
    som.train(training_data, num_iteration=5000)
    
    val = som.quantization_error(training_data)
    print(f"Sigma: {sig}, LR: {lr}, QE: {val}")
    return {'loss': val, 'status': STATUS_OK}

trials = Trials()
best = fmin(
    fn=som_fn,
    space=space,
    algo=tpe.suggest,
    max_evals=500,
    trials=trials)
print("Best hyperparameters found:", best)

for i, trial in enumerate(trials.trials[:2]):
    print(i,trial)