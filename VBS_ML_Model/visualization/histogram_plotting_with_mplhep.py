import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot
from pathlib import Path
from typing import Dict, List, Tuple

plt.style.use(hep.style.CMS)

class HistogramEntry:
    def __init__(self, key: str, histogram_data: Tuple[np.ndarray, np.ndarray]):
        self.key = key
        self.values, self.edges = histogram_data
        total = np.sum(self.values)
        if total > 0:
            self.values = self.values / total

def plotting_histograms():
    eos_base = "/eos/user/a/apakkila/VBS_ML_project/data/"
    
    sample_sign = "SS"
    #sample_sign = "OS"
    
    if sample_sign == "SS":
        input_dir = eos_base + "output_histograms_SS_all_variables_with_PF_candidates"
    else:
        input_dir = eos_base + "output_histograms_OS_all_variables_with_PF_candidates"
    
    output_dir = f"/eos/user/a/apakkila/VBS_ML_project/histograms/output_histograms_visualized_all_variables_{sample_sign}"
    
    check_cmd = f"xrdfs root://eosuser.cern.ch stat {output_dir}"
    result = subprocess.run(check_cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        mkdir_cmd = f"xrdfs root://eosuser.cern.ch mkdir {output_dir}"
        print(f"Creating EOS output folder: {output_dir}")
        subprocess.run(mkdir_cmd, shell=True)
    
    sample_names = [
        "h_V0_p_theta", "h_V0_z_j_leading", "h_V0_z_j_subleading", "h_V0_pt", "h_V0_eta", "h_V0_phi", "h_V0_mass", "h_V0_area",
        "h_V1_p_theta", "h_V1_z_j_leading", "h_V1_z_j_subleading", "h_V1_pt", "h_V1_eta", "h_V1_phi", "h_V1_mass", "h_V1_area",
        "h_VV_deta", "h_VV_dphi", "h_VV_mVV", "h_VV_log_mVV",
        "h_TagJJ_deta", "h_TagJJ_dphi", "h_TagJJ_mJJ", "h_TagJJ_log_mJJ",
        "h_TagJet0_eta", "h_TagJet0_pt", "h_TagJet0_phi", "h_TagJet0_mass", "h_TagJet0_area",
        "h_TagJet1_eta", "h_TagJet1_pt", "h_TagJet1_phi", "h_TagJet1_mass", "h_TagJet1_area",
        "h_V0_SubJet0_pt", "h_V0_SubJet1_pt", "h_V1_SubJet0_pt", "h_V1_SubJet1_pt",
        "h_V0_SubJet0_eta", "h_V0_SubJet1_eta", "h_V1_SubJet0_eta", "h_V1_SubJet1_eta",
        "h_V0_SubJet0_phi", "h_V0_SubJet1_phi", "h_V1_SubJet0_phi", "h_V1_SubJet1_phi",
        "h_V0_SubJet0_mass", "h_V0_SubJet1_mass", "h_V1_SubJet0_mass", "h_V1_SubJet1_mass",
        "h_V0_SubJet0_area", "h_V0_SubJet1_area", "h_V1_SubJet0_area", "h_V1_SubJet1_area"
    ]

    y_axis_names = [
        r"$p_{\theta}$", r"$z_j$", r"$z_j$", r"$p_T$", r"$\eta$", r"$\phi$", r"$m$", r"$\mathrm{area}$",
        r"$p_{\theta}$", r"$z_j$", r"$z_j$", r"$p_T$", r"$\eta$", r"$\phi$", r"$m$", r"$\mathrm{area}$",
        r"$\Delta\eta$", r"$\Delta\phi$", r"$m_{VV}$", r"$\log(m_{VV})$",
        r"$\Delta\eta$", r"$\Delta\phi$", r"$m_{JJ}$", r"$\log(m_{JJ})$",
        r"$\eta$", r"$p_T$", r"$\phi$", r"$m$", r"$\mathrm{area}$",
        r"$\eta$", r"$p_T$", r"$\phi$", r"$m$", r"$\mathrm{area}$",
        r"$p_T$", r"$p_T$", r"$p_T$", r"$p_T$",
        r"$\eta$", r"$\eta$", r"$\eta$", r"$\eta$",
        r"$\phi$", r"$\phi$", r"$\phi$", r"$\phi$",
        r"$m$", r"$m$", r"$m$", r"$m$",
        r"$\mathrm{area}$", r"$\mathrm{area}$", r"$\mathrm{area}$", r"$\mathrm{area}$"
    ]

    title_names = [
        r"$p_{\theta}$ of V0", r"$z_j$ for leading subjet of V0", r"$z_j$ for subleading subjet of V0", r"$p_T$ of V0", r"$\eta$ of V0", r"$\phi$ of V0", r"$m$ of V0", r"$\mathrm{area}$ of V0",
        r"$p_{\theta}$ of V1", r"$z_j$ for leading subjet of V1", r"$z_j$ for subleading subjet of V1", r"$p_T$ of V1", r"$\eta$ of V1", r"$\phi$ of V1", r"$m$ of V1", r"$\mathrm{area}$ of V1",
        r"$\Delta\eta$ of VV", r"$\Delta\phi$ of VV", r"$m_{VV}$ of VV", r"$\log(m_{VV})$ of VV",
        r"$\Delta\eta$ of TagJJ", r"$\Delta\phi$ of TagJJ", r"$m_{JJ}$ of TagJJ", r"$\log(m_{JJ})$ of TagJJ",
        r"$\eta$ of TagJet0", r"$p_T$ of TagJet0", r"$\phi$ of TagJet0", r"$m$ of TagJet0", r"$\mathrm{area}$ of TagJet0",
        r"$\eta$ of TagJet1", r"$p_T$ of TagJet1", r"$\phi$ of TagJet1", r"$m$ of TagJet1", r"$\mathrm{area}$ of TagJet1",
        r"$p_T$ of SubJet0 of V0", r"$p_T$ of SubJet1 of V0", r"$p_T$ of SubJet0 of V1", r"$p_T$ of SubJet1 of V1",
        r"$\eta$ of SubJet0 of V0", r"$\eta$ of SubJet1 of V0", r"$\eta$ of SubJet0 of V1", r"$\eta$ of SubJet1 of V1",
        r"$\phi$ of SubJet0 of V0", r"$\phi$ of SubJet1 of V0", r"$\phi$ of SubJet0 of V1", r"$\phi$ of SubJet1 of V1",
        r"$m$ of SubJet0 of V0", r"$m$ of SubJet1 of V0", r"$m$ of SubJet0 of V1", r"$m$ of SubJet1 of V1",
        r"$\mathrm{area}$ of SubJet0 of V0", r"$\mathrm{area}$ of SubJet1 of V0", r"$\mathrm{area}$ of SubJet0 of V1", r"$\mathrm{area}$ of SubJet1 of V1"
    ]

    if sample_sign == "SS":
        polarization_states = ["PolarLL", "PolarLTTL", "PolarTT"]
    else:
        polarization_states = ["PolarLL", "PolarLT", "PolarTL", "PolarTT"]
    
    histogram_entries: List[HistogramEntry] = []

    for sample_name in sample_names:
        for polarization in polarization_states:
            if sample_sign == "SS":
                file_name = (f"{input_dir}/{sample_name}_Processed_SampleWPMJJWPMJJjj_EWK_"
                             f"{polarization}_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_"
                             f"Modulereco_Tagv1p5POL.root")
            else:
                file_name = (f"{input_dir}/{sample_name}_Processed_SampleWPJJWMJJjj_EWK_"
                             f"{polarization}_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_"
                             f"Modulereco_Tagv1p5POL.root")
            
            file_name = f"root://eosuser.cern.ch/" + file_name
            
            try:
                with uproot.open(file_name) as root_file:
                    if sample_name not in root_file:
                        print(f"Histogram {sample_name} not found in file: {file_name}")
                        continue
                    hist = root_file[sample_name]
                    values, edges = hist.to_numpy()
                    hist_entry = HistogramEntry(f"{sample_name}_{polarization}", (values, edges))
                    histogram_entries.append(hist_entry)
            except Exception as e:
                print(f"Failed to open file: {file_name}")
                print(f"Error: {e}")
                continue

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']


    for i, sample_name in enumerate(sample_names):
        yaxis_name = sample_name[2:] if sample_name.startswith("h_") else sample_name
        title = f"{yaxis_name}_{sample_sign}"
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        max_y = 0.0
        plot_data = []

        for j, polarization in enumerate(polarization_states):
            hist_key = f"{sample_name}_{polarization}"
            for entry in histogram_entries:
                if entry.key == hist_key:
                    plot_data.append((entry, colors[j], polarization))
                    local_max = np.max(entry.values)
                    if local_max > max_y:
                        max_y = local_max
        
        max_y *= 1.1

        for entry, color, polarization in plot_data:
            ax.step(entry.edges[:-1], entry.values, where='post',
                    color=color, linewidth=2, label=polarization.replace("Polar", ""))
        
        ax.set_xlabel(y_axis_names[i], fontsize=20)
        ax.set_ylabel("Normalized entries", fontsize=20)
        ax.set_title(f'{title_names[i]} for {sample_sign}', fontsize=24)
        
        
        # Calculate min_x and max_x for the current sample_name
        sample_min_x = min(entry.edges[0] for entry in histogram_entries if entry.key.startswith(sample_name))
        sample_max_x = max(entry.edges[-1] for entry in histogram_entries if entry.key.startswith(sample_name))

        ax.set_xlim(sample_min_x, sample_max_x)
        ax.set_ylim(0, max_y)
        
        ax.legend(loc='upper right', fontsize=20)
        ax.grid(True, alpha=0.3)

        local_png = f"{sample_name}.png"
        plt.savefig(local_png, dpi=300, bbox_inches='tight')
        plt.close()

        eos_png = f"{output_dir}/{sample_name}.png"
        copy_cmd = f"xrdcp -f {local_png} root://eosuser.cern.ch/{eos_png}"
        subprocess.run(copy_cmd, shell=True)
        os.remove(local_png)

        print(f"Saved plot: {sample_name}")

    print(f"All plots saved to EOS: {output_dir}")

if __name__ == "__main__":
    plotting_histograms()
