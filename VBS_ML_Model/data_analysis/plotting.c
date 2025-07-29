#include <iostream>
#include <vector>
#include <sys/stat.h>
#include "TString.h"
#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

struct HistogramEntry {
    TString key;
    TH1F* histogram;
};

void plotting_histograms() {
    // Use EOS
    TString eos_base = "/eos/user/a/apakkila/VBS_ML_project/data/";

    // Choose sign
    //TString sample_sign = "SS";
    TString sample_sign = "OS";

    // Input EOS folder
    TString input_dir;
    if (sample_sign == "SS") {
        input_dir = eos_base + "output_histograms_SS_all_variables";
    } else {
        input_dir = eos_base + "output_histograms_OS_all_variables";
    }

    // Output EOS folder
    TString output_dir = eos_base + "output_histograms_visualized_all_variables_" + sample_sign;

    // Create EOS output folder if it doesn't exist
    TString check_cmd = "xrdfs root://eosuser.cern.ch stat " + output_dir;
    if (gSystem->Exec(check_cmd) != 0) {
        TString mkdir_cmd = "xrdfs root://eosuser.cern.ch mkdir " + output_dir;
        std::cout << "Creating EOS output folder: " << output_dir << std::endl;
        gSystem->Exec(mkdir_cmd);
    }

    TString sample_names[53] = {
        "h_V0_p_theta", "h_V0_z_j_leading", "h_V0_z_j_subleading", "h_V0_pt", "h_V0_eta", "h_V0_phi", "h_V0_mass", "h_V0_area",
        "h_V1_p_theta", "h_V1_z_j_leading", "h_V1_z_j_subleading", "h_V1_pt", "h_V1_eta", "h_V1_phi", "h_V1_mass", "h_V1_area",

        "h_VV_deta", "h_VV_dphi", "h_VV_mVV", "h_log_VV_mVV",
        
        "h_TagJJ_deta", "h_TagJJ_dphi", "h_TagJJ_mJJ",
        
        "h_TagJet0_eta", "h_TagJet0_pt", "h_TagJet0_phi", "h_TagJet0_mass", "h_TagJet0_area",
        "h_TagJet1_eta", "h_TagJet1_pt", "h_TagJet1_phi", "h_TagJet1_mass", "h_TagJet1_area",
        
        "h_V0_SubJet0_pt", "h_V0_SubJet1_pt", "h_V1_SubJet0_pt", "h_V1_SubJet1_pt",
        "h_V0_SubJet0_eta", "h_V0_SubJet1_eta", "h_V1_SubJet0_eta", "h_V1_SubJet1_eta",
        "h_V0_SubJet0_phi", "h_V0_SubJet1_phi", "h_V1_SubJet0_phi", "h_V1_SubJet1_phi",
        "h_V0_SubJet0_mass", "h_V0_SubJet1_mass", "h_V1_SubJet0_mass", "h_V1_SubJet1_mass",
        "h_V0_SubJet0_area", "h_V0_SubJet1_area", "h_V1_SubJet0_area", "h_V1_SubJet1_area"
    };

    TString polarization_states[4];
    int num_polarizations = 0;
    if (sample_sign == "SS") {
        polarization_states[0] = "PolarLL";
        polarization_states[1] = "PolarLTTL";
        polarization_states[2] = "PolarTT";
        num_polarizations = 3;
    } else {
        polarization_states[0] = "PolarLL";
        polarization_states[1] = "PolarLT";
        polarization_states[2] = "PolarTL";
        polarization_states[3] = "PolarTT";
        num_polarizations = 4;
    }

    std::vector<HistogramEntry> histogram_entries;

    // Loop: read ROOT histos from EOS
    for (const auto& sample_name : sample_names) {
        for (int i = 0; i < num_polarizations; ++i) {
            TString polarization = polarization_states[i];
            TString file_name;

            if (sample_sign == "SS") {
                file_name = input_dir + "/" + sample_name +
                    "_Processed_SampleWPMJJWPMJJjj_EWK_" + polarization +
                    "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";
            } else {
                file_name = input_dir + "/" + sample_name +
                    "_Processed_SampleWPJJWMJJjj_EWK_" + polarization +
                    "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";
            }

            file_name = "root://eosuser.cern.ch/" + file_name;

            TFile *root_file = TFile::Open(file_name);
            if (!root_file || root_file->IsZombie()) {
                std::cout << "Failed to open file: " << file_name << std::endl;
                continue;
            }

            auto hist = (TH1F*)root_file->Get(sample_name);
            if (!hist) {
                std::cout << "Histogram " << sample_name << " not found in file: " << file_name << std::endl;
                root_file->Close();
                delete root_file;
                continue;
            }

            hist->Scale(1.0 / hist->Integral());
            histogram_entries.push_back({sample_name + "_" + polarization, (TH1F*)hist->Clone()});
            histogram_entries.back().histogram->SetDirectory(0);

            root_file->Close();
        }
    }

    // Loop: plot and save PNGs to EOS
    for (const auto& sample_name : sample_names) {
        TString yaxis_name = sample_name;
        if (yaxis_name.BeginsWith("h_")) yaxis_name.Remove(0, 2);
        TString title = yaxis_name + "_" + sample_sign;

        TCanvas* canvas = new TCanvas("canvas", title, 800, 600);
        TLegend* legend = new TLegend(0.75, 0.75, 0.98, 0.98);
        std::vector<int> color = {30, 38, 41, 46};

        double max_y = 0.0;
        for (const auto& polarization : polarization_states) {
            TString hist_key = sample_name + "_" + polarization;
            for (const auto& entry : histogram_entries) {
                if (entry.key.CompareTo(hist_key) == 0) {
                    double local_max = entry.histogram->GetMaximum();
                    if (local_max > max_y) max_y = local_max;
                }
            }
        }
        max_y *= 1.1;

        int color_idx = 0;
        for (const auto& polarization : polarization_states) {
            TString hist_key = sample_name + "_" + polarization;
            for (const auto& entry : histogram_entries) {
                if (entry.key.CompareTo(hist_key) == 0) {
                    entry.histogram->SetTitle(title);
                    entry.histogram->GetXaxis()->SetTitle(yaxis_name);
                    entry.histogram->GetYaxis()->SetTitle("Normalized entries");
                    entry.histogram->SetLineColor(color[color_idx]);
                    entry.histogram->SetLineWidth(2);

                    if (color_idx == 0) {
                        entry.histogram->SetMaximum(max_y);
                        entry.histogram->Draw("hist");
                    } else {
                        entry.histogram->Draw("samehist");
                    }
                    legend->AddEntry(entry.histogram, sample_name + "_" + polarization, "l");
                    color_idx++;
                }
            }
        }

        legend->Draw();
        TString local_png = sample_name + ".png";
        canvas->SaveAs(local_png);

        // Copy to EOS output folder
        TString eos_png = output_dir + "/" + sample_name + ".png";
        TString copy_cmd = "xrdcp -f " + local_png + " root://eosuser.cern.ch/" + eos_png;
        gSystem->Exec(copy_cmd);

        gSystem->Exec("rm " + local_png); // clean local
        delete canvas;
    }

    std::cout << "All plots saved to EOS: " << output_dir << std::endl;
}