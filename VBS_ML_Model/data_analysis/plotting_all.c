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
    TString output_dir = "output_histograms_visualized_OS";
    struct stat info;
    if (stat(output_dir.Data(), &info) != 0) {
        mkdir(output_dir.Data(), 0777);
    }

    TString sample_names[26] = {
        "h_V0_p_theta", "h_V0_z_j", "h_V0_pt", "h_V0_eta", "h_V0_phi", "h_V0_mass",
        "h_V1_p_theta", "h_V1_z_j", "h_V1_pt", "h_V1_eta", "h_V1_phi", "h_V1_mass",
        "h_VV_deta", "h_VV_dphi", "h_VV_mVV",
        "h_TagJJ_deta", "h_TagJJ_dphi", "h_TagJJ_mJJ",
        "h_Tagjet0_eta", "h_Tagjet0_pt", "h_Tagjet0_phi", "h_Tagjet0_mass",
        "h_Tagjet1_eta", "h_Tagjet1_pt", "h_Tagjet1_phi", "h_Tagjet1_mass"
    };

    TString polarization_states[4] = {"PolarLL", "PolarLT", "PolarTL", "PolarTT"};

    std::vector<HistogramEntry> histogram_entries;

    TString input_dir = "output_histograms_OS";

    for (const auto& sample_name : sample_names) {
        for (const auto& polarization : polarization_states) {

            // Specifies the file that is opened
            TString file_name = input_dir + "/" + sample_name +
                                "_Processed_SampleWPJJWMJJjj_EWK_" + polarization +
                                "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";

            // Opens the root_file
            TFile *root_file = TFile::Open(file_name, "READ");

            // Checks if the file is opened correctly
            if (!root_file || root_file->IsZombie()) {
                std::cout << "Failed to open file: " << file_name << std::endl;
                continue;
            }

            // Extracts the histogram data from the root_file
            auto hist = (TH1F*)root_file->Get(sample_name);

            // Checks if the root_file is read correctly
            if (!hist) {
                std::cout << "Histogram " << sample_name << " not found in file: " << file_name << std::endl;
                root_file->Close();
                delete root_file;
                continue;
            }

            // Normalized the histogram data
            hist->Scale(1.0 / hist->Integral());

            // Adds the histogram data to the storage vector
            histogram_entries.push_back({sample_name + "_" + polarization, (TH1F*)hist->Clone()});
            histogram_entries.back().histogram->SetDirectory(0);

            root_file->Close();
        }
    }

    // Loops over the sample_names and for each sample_name plots the histograms with different polarization states to the same plot
    for (const auto& sample_name : sample_names) {
        TCanvas* canvas = new TCanvas("canvas", sample_name, 800, 600);
        TLegend* legend = new TLegend(0.7, 0.7, 0.9, 0.9);
        int color = 1;

        // Loops over the polarization states to draw their histograms to the same plot
        for (const auto& polarization : polarization_states) {
            TString hist_key = sample_name + "_" + polarization;

            for (const auto& entry : histogram_entries) {
                if (entry.key.CompareTo(hist_key) == 0) {
                    entry.histogram->SetLineColor(color++);
                    entry.histogram->SetLineWidth(2);
                    entry.histogram->Draw(color == 2 ? "hist" : "samehist");
                    legend->AddEntry(entry.histogram, sample_name + "_" + polarization, "l");
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
