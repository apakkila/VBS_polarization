#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sys/stat.h>
#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"

void plotting_histograms() {
    // Create the output directory if it doesn't exist
    const char* output_dir = "output_histograms_visualized";
    struct stat info;
    if (stat(output_dir, &info) != 0) {
        mkdir(output_dir, 0777);
    }

    // Define sample names
    const char* sample_names[24] = {
        "Histo_h_V0_p_theta", "Histo_h_V0_z_j", "Histo_h_V0_pt", "Histo_h_V0_eta", "Histo_h_V0_phi", "Histo_h_V0_mass",
        "Histo_h_V1_p_theta", "Histo_h_V1_z_j", "Histo_h_V1_pt", "Histo_h_V1_eta", "Histo_h_V1_phi", "Histo_h_V1_mass",
        "Histo_h_VV_deta", "Histo_h_VV_dphi", "Histo_h_VV_mVV",
        "Histo_h_TagJJ_deta", "Histo_h_TagJJ_dphi", "Histo_h_TagJJ_mJJ",
        "Histo_h_Tagjet0_eta", "Histo_h_Tagjet0_pt", "Histo_h_Tagjet0_phi", "Histo_h_Tagjet0_mass",
        "Histo_h_Tagjet1_eta", "Histo_h_Tagjet1_pt", "Histo_h_Tagjet1_phi", "Histo_h_Tagjet1_mass"
    };

    // Define polarization states
    const char* polarization_states[4] = {"PolarLL", "PolarLT", "PolarTL", "PolarTT"};

    // Map to store histograms
    std::map<std::string, TH1F*> histogram_map;

    // Input directory containing the .root files
    const char* input_dir = "output_histograms_OS";

    // Loop through sample names and polarization states
    for (const auto& sample_name : sample_names) {  
        // Initialize an empty histogram for the combined plot
        TH1F* combined_histogram = nullptr;

        // Loop through each polarization state
        for (const auto& polarization : polarization_states) {
            // Construct the file name
            std::string file_name = std::string(input_dir) + "/" + sample_name + "_Processed_SampleWPJJWMJJjj_EWK_" + polarization + "_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root";

            // Open the ROOT file
            TFile* root_file = TFile::Open(file_name, "READ");
            if (!root_file || root_file->IsZombie()) {
                std::cout << "Failed to open file: " << file_name << std::endl;
                continue;
            }

            // Extract the histogram
            TH1F* hist = (TH1F*)root_file->Get(sample_name);
            if (!hist) {
                std::cout << "Histogram " << sample_name << " not found in file: " << file_name << std::endl;
                root_file->Close();
                delete root_file;
                continue;
            }

            // Normalize the histogram
            hist->Scale(1.0 / hist->Integral());

            // Add the histogram to the map
            std::string hist_key = std::string(sample_name) + "_" + polarization;
            histogram_map[hist_key] = (TH1F*)hist->Clone();
            histogram_map[hist_key]->SetDirectory(0);  // Detach from the file

            root_file->Close();
            delete root_file;
        }
    }

    // Check if all histograms were extracted correctly
    std::cout << "Extracted histograms:" << std::endl;
    for (const auto& pair : histogram_map) {
        std::cout << "Key: " << pair.first << ", Histogram: " << pair.second->GetName() << std::endl;
    }

    // Plot histograms grouped by sample_name
    for (const auto& sample_name : sample_names) {
        TCanvas* canvas = new TCanvas("canvas", sample_name, 800, 600);

        TLegend* legend = new TLegend(0.7, 0.7, 0.9, 0.9);
        int color = 1;  // Start with color index 1

        for (const auto& polarization : polarization_states) {
            std::string hist_key = std::string(sample_name) + "_" + polarization;

            if (histogram_map.find(hist_key) != histogram_map.end()) {
                TH1F* hist = histogram_map[hist_key];
                hist->SetLineColor(color++);
                hist->SetLineWidth(2);
                hist->Draw(color == 2 ? "hist" : "hist same");  // Draw the first histogram normally, others on the same canvas
                legend->AddEntry(hist, polarization, "l");
            }
        }

        legend->Draw();

        // Save the canvas as an image
        std::string output_file = std::string(output_dir) + "/" + sample_name + "_combined.png";
        canvas->SaveAs(output_file.c_str());

        delete canvas;
    }

    std::cout << "Histograms plotted and saved to " << output_dir << std::endl;
}