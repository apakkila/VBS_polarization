import ROOT
import os
import sys

ROOT.EnableImplicitMT(4)

input_dir = "/eos/user/a/apakkila/VBS_ML_project/data/processed_samples_with_PF_candidates"

sample = "OS" 
#sample = "SS"

if sample == "OS":
    # Directory to save the trained SOM model weights
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/PF_candidate_exploration/OS"
    os.makedirs(output_dir, exist_ok=True)

    # List of sample files to load
    sample_files = [
        "Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root",
        "Processed_SampleWPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root",
        "Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root"
    ]
elif sample == "SS":
    output_dir = "/eos/user/a/apakkila/VBS_ML_project/data_analysis/PF_candidate_exploration/SS"
    os.makedirs(output_dir, exist_ok=True)

    sample_files = [
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root",
        "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root"
    ]

tree = "Events"
sample_file = "Processed_SampleWPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p5POL.root"
file_path = os.path.join(input_dir, sample_file)

df_root = ROOT.RDataFrame(tree, file_path)

# Redirect the output to a text file
with open("tree_description.txt", "w") as f:
    original_stdout = sys.stdout  # Save the original stdout
    sys.stdout = f  # Redirect stdout to the file

    # Get column names
    column_names = df_root.GetColumnNames()

    # Print column names and their types
    print("Column Names and Types:")
    for column in column_names:
        column_type = df_root.GetColumnType(column)
        print(f"{column}: {column_type}")

    sys.stdout = original_stdout  # Restore original stdout

print("Column names and types written to tree_description.txt")