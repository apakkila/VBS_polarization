import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import os

plt.style.use(hep.style.CMS)

#sample = "OS"
sample = "SS"

if sample == "SS":
    file_path = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/grid_search/SS/run001som_training_log.txt"
elif sample == "OS":
    file_path = "/eos/user/a/apakkila/VBS_ML_project/models/som_model/final_weights/gaussian_euclidean/regular_variables/grid_search/OS/run001som_training_log.txt"

if sample == "SS":
    error_log = pd.read_csv(
        file_path,
        sep=",",  # Comma-separated file
        header=None,  # No header in the file
        names=["datetime", "run_id", "number_of_samples", "lr", "sigma", 
        "weight_init_elapsed_time", "elapsed_time", "quantization_error", 
        "topographic_error", "features"],
        usecols=["quantization_error", "topographic_error"]
    )
elif sample == "OS":
    error_log = pd.read_csv(
        file_path,
        sep=",",  # Comma-separated file
        header=None,  # No header in the file
        names=["datetime", "run_id", "number_of_samples", "som_shape", "lr", "sigma", 
            "weight_init_elapsed_time", "elapsed_time", "quantization_error", 
            "topographic_error", "features"],
        usecols=["quantization_error", "topographic_error"]
    )

df_plot = pd.DataFrame(error_log)
print(df_plot)
df_plot = df_plot[1:]
print(df_plot)
df_plot['quantization_error'] = df_plot['quantization_error'].astype(float)
df_plot['topographic_error'] = df_plot['topographic_error'].astype(float)

if sample == "SS":
    plot_path = "/eos/user/a/apakkila/VBS_ML_project/plots/som_training_errors/grid_search/SS"
elif sample == "OS":
    plot_path = "/eos/user/a/apakkila/VBS_ML_project/plots/som_training_errors/grid_search/OS"

os.makedirs(plot_path, exist_ok=True)

# Create learning rate and sigma pairs for x-axis labels
sigmas = [1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
lrs = [0.05, 0.1, 0.2, 0.5, 0.8, 1.0]
lr_sigma_pairs = []
for sigma in sigmas:
    for lr in lrs:
        lr_sigma_pairs.append(f"({lr}, {sigma})")

indices = np.arange(len(df_plot))

# Plot quantization error
plt.figure(figsize=(18, 10))

plt.plot(
        indices,
        df_plot['quantization_error'], 
         marker='o', linestyle='-', color='steelblue', 
         label="Quantization error", markersize=6)
plt.xticks(range(len(lr_sigma_pairs)), 
           lr_sigma_pairs[:54], 
           rotation=90, ha='center')
plt.xlabel("Learning rate and sigma pairs")
plt.ylabel("Quantization Error")
plt.title(f"SOM model quantization error for {sample} sample")
#plt.ylim(0, 0.6)  # Dynamic y-limit based on data
plt.grid(True, alpha=0.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(plot_path, "quantization_error.png"), dpi=300, bbox_inches='tight')
plt.show()  # Show the plot for debugging


# Plot topographic error
plt.figure(figsize=(18, 10))

# Plot the topographic error values
plt.plot(
        indices,
        df_plot['topographic_error'], 
         marker='o', linestyle='-', color='steelblue', 
         label="Topographic error", markersize=6)
plt.xticks(range(len(lr_sigma_pairs)), 
           lr_sigma_pairs[:54], 
           rotation=90, ha='center')
plt.xlabel("Learning rate and sigma pairs")
plt.ylabel("Topographic Error")
plt.title(f"SOM model topographic error for {sample} sample")
plt.ylim(0, 0.6)  # Dynamic y-limit based on data
plt.grid(True, alpha=0.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig(os.path.join(plot_path, "topographic_error.png"), dpi=300, bbox_inches='tight')
plt.show()  # Show the plot for debugging

print("Plot saved successfully!")