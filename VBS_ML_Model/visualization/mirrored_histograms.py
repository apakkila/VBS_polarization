import numpy as np
import ROOT
import os
import matplotlib.pyplot as plt


input_dir = "/eos/user/a/apakkila/VBS_ML_project/data/unnormalized_numpy_arrays_with_PF_candidates/with_mirrored_variables"

output_dir = "/eos/user/a/apakkila/VBS_ML_project/histograms/unnormalized_mirrored_histograms"
os.makedirs(output_dir, exist_ok=True)

#sample = "OS"
sample = "SS"

if sample == "OS":
# List of sample files
    sample_list = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]
elif sample == "SS":
    sample_list = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.npz"
    ]

vars_to_plot = [
    "V0_z_j_leading_mirrored",
    "V0_z_j_subleading_mirrored",
    "VV_dphi_mirrored",
    "TagJJ_deta_mirrored"
]

for var in vars_to_plot:
    plt.figure()
    for sample_file in sample_list:
        data = np.load(os.path.join(input_dir, sample_file))
        if var not in data:
            print(f"Variable {var} not found in {sample_file}, skipping.")
            continue

        arr = data[var]
        label = sample_file.split("_Polar")[1].split("_")[0]  # Extract LL, TT, etc.
        plt.hist(arr, bins=100, histtype='step', label=label, linewidth=1.5)

    plt.title(f"{var}")
    plt.xlabel(var)
    plt.ylabel("Entries")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    out_name = os.path.join(output_dir, f"{var}.png")
    plt.savefig(out_name)
    plt.close()

    print(f"Saved histogram for {var}")