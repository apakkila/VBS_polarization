#include <iostream>
#include <vector>
#include <sys/stat.h>
#include "TString.h"
#include "TFile.h"
#include "TH2F.h"
#include "TCanvas.h"
#include "TSystem.h"

struct Histogram2DEntry {
    TString key;
    TH2F* histogram2D;
};

void plotting_histograms() {
    // Base EOS directory
    TString eos_base = "/eos/user/a/apakkila/VBS_ML_project/data/";

    // Choose sign
    //TString sample_sign = "SS";
    TString sample_sign = "OS";

    // Input EOS folder
    TString input_dir;
    if (sample_sign == "SS") {
        input_dir = eos_base + "output_histograms_SS";
    } else {
        input_dir = eos_base + "output_histograms_OS";
    }
    TString output_dir = eos_base + "output_2d_histograms_visualized_" + sample_sign;

    // Create EOS output folder if needed
    TString check_cmd = "xrdfs root://eosuser.cern.ch stat " + output_dir;
    if (gSystem->Exec(check_cmd) != 0) {
        TString mkdir_cmd = "xrdfs root://eosuser.cern.ch mkdir " + output_dir;
        std::cout << "Creating EOS output folder: " << output_dir << std::endl;
        gSystem->Exec(mkdir_cmd);
    }

    // Histogram base names (without sample suffix)
    TString sample_names[] = {
        "h2_V0_p_theta_vs_z_j",
        "h2_V1_p_theta_vs_z_j"
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

    std::vector<Histogram2DEntry> histogram2D_entries;

    // Loop over histograms and polarizations to load them from file
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

            TFile* root_file = TFile::Open(file_name);
            if (!root_file || root_file->IsZombie()) {
                std::cout << "Failed to open file: " << file_name << std::endl;
                continue;
            }

            TString hist_key = sample_name + "_" + polarization;
            auto hist2D = (TH2F*)root_file->Get(sample_name);
            if (!hist2D) {
                std::cout << "Histogram " << hist_key << " not found in file: " << file_name << std::endl;
                root_file->Close();
                delete root_file;
                continue;
            }

            // Normalize if needed
            hist2D->Scale(1.0 / hist2D->Integral());
            histogram2D_entries.push_back({hist_key, (TH2F*)hist2D->Clone()});
            histogram2D_entries.back().histogram2D->SetDirectory(0);

            root_file->Close();
        }
    }

    // Plot and save
    for (const auto& entry2D : histogram2D_entries) {
        TCanvas* c2 = new TCanvas("c2", entry2D.key, 800, 600);
        c2->SetRightMargin(0.15);
        entry2D.histogram2D->GetXaxis()->SetTitle("p_{#theta}");
        entry2D.histogram2D->GetYaxis()->SetTitle("z_{j}");
        entry2D.histogram2D->Draw("COLZ");

        TString filename = entry2D.key + ".png";
        c2->SaveAs(filename);

        TString eos_png = output_dir + "/" + filename;
        TString copy_cmd = "xrdcp -f " + filename + " root://eosuser.cern.ch/" + eos_png;
        gSystem->Exec(copy_cmd);
        gSystem->Exec("rm " + filename);
        delete c2;
    }

    std::cout << "2D histogram plots saved to EOS: " << output_dir << std::endl;
}
