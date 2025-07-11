#include <iostream>
#include <vector>
#include <sys/stat.h>
#include "TString.h"
#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"

struct HistogramEntry {
    TString key;
    TH1F* histogram;
};

void plotting_histograms() {

    // Determine which sign the sample W bosons are
    TString sample_sign = "SS";
    //TString sample_sign = "OS";

    TString output_dir = "output_histograms_visualized_" + sample_sign;
    struct stat info;
    if (stat(output_dir.Data(), &info) != 0) {
        mkdir(output_dir.Data(), 0777);
    }

    TString sample_names[26] = {
        "h_V0_p_theta", "h_V0_z_j", "h_V0_pt", "h_V0_eta", "h_V0_phi", "h_V0_mass",
        "h_V1_p_theta", "h_V1_z_j", "h_V1_pt", "h_V1_eta", "h_V1_phi", "h_V1_mass",
        "h_VV_deta", "h_VV_dphi", "h_VV_mVV",
        "h_TagJJ_deta", "h_TagJJ_dphi", "h_TagJJ_mJJ",
        "h_TagJet0_eta", "h_TagJet0_pt", "h_TagJet0_phi", "h_TagJet0_mass",
        "h_TagJet1_eta", "h_TagJet1_pt", "h_TagJet1_phi", "h_TagJet1_mass"
    };

    std::vector<HistogramEntry> histogram_entries;

    TString input_dir;
    TString polarization_states[4];
    int num_polarizations = 0;

    if (sample_sign == "SS") {
        input_dir = "output_histograms_SS";
        polarization_states[0] = "PolarLL";
        polarization_states[1] = "PolarLTTL";
        polarization_states[2] = "PolarTT";
        num_polarizations = 3;
    } else {
        input_dir = "output_histograms_OS";
        polarization_states[0] = "PolarLL";
        polarization_states[1] = "PolarLT";
        polarization_states[2] = "PolarTL";
        polarization_states[3] = "PolarTT";
        num_polarizations = 4;
    }

    // Loop over sample names and polarizations
    for (const auto& sample_name : sample_names) {
        for (int i = 0; i < num_polarizations; ++i) {
            TString polarization = polarization_states[i];
            TString file_name;

            // Build file name
            if (sample_sign == "SS"){
                file_name = input_dir + "/" + sample_name +
                                "_Processed_SampleWPMJJWPMJJjj_EWK_" + polarization +
                                "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";
            } else {
                file_name = input_dir + "/" + sample_name +
                                "_Processed_SampleWPJJWMJJjj_EWK_" + polarization +
                                "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";
            }
            
            // Open file
            TFile *root_file = TFile::Open(file_name);
            if (!root_file || root_file->IsZombie()) {
                std::cout << "Failed to open file: " << file_name << std::endl;
                continue;
            }

            // Get histogram
            auto hist = (TH1F*)root_file->Get(sample_name);
            if (!hist) {
                std::cout << "Histogram " << sample_name << " not found in file: " << file_name << std::endl;
                root_file->Close();
                delete root_file;
                continue;
            }

            // Normalize
            hist->Scale(1.0 / hist->Integral());

            // Store copy
            histogram_entries.push_back({sample_name + "_" + polarization, (TH1F*)hist->Clone()});
            histogram_entries.back().histogram->SetDirectory(0);

            root_file->Close();
        }
    }

    for (const auto& sample_name : sample_names) {
        TCanvas* canvas = new TCanvas("canvas", sample_name, 800, 600);
        TLegend* legend = new TLegend(0.7, 0.7, 0.98, 0.98);
        std::vector<int> color;
        // Determine line colors
        color.push_back(30);
        color.push_back(38);
        color.push_back(41);
        color.push_back(46);

        int color_idx = 0;

        // Loops over the polarization states to draw their histograms to the same plot
        for (const auto& polarization : polarization_states) {
            TString hist_key = sample_name + "_" + polarization;

            for (const auto& entry : histogram_entries) {
                // Truncates "h_" from the beginning of the sample_name
                TString title = sample_name;
                if (title.BeginsWith("h_")) {
                    title.Remove(0, 2);
                }

                if (entry.key.CompareTo(hist_key) == 0) {
                    entry.histogram->GetXaxis()->SetTitle(title);
                    entry.histogram->GetYaxis()->SetTitle("Normalized entires");
                    entry.histogram->SetLineColor(color[color_idx]);
                    entry.histogram->SetLineWidth(2);
                    entry.histogram->Draw(color_idx == 0 ? "hist" : "samehist");
                    legend->AddEntry(entry.histogram, sample_name + "_" + polarization, "l");
                    color_idx++;
                }
            }
        }

        legend->Draw();
        TString output_file = output_dir + "/" + sample_name + "_combined.png";
        canvas->SaveAs(output_file);
        delete canvas;
    }

    std::cout << "Histograms plotted and saved to " << output_dir << std::endl;
}