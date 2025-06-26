void stacked_histogram()
{
    // Create the output directory if it doesn't exist
    const char* output_dir = "output_histograms";
    struct stat info;
    if (stat(output_dir, &info) != 0) {
        mkdir(output_dir, 0777);  // Create the directory with read/write/execute permissions
    }

    // Open the .root files
    TFile *file_V0_LL = TFile::Open("output/Histo_h_V0_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V1_LL = TFile::Open("output/Histo_h_V1_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V0_TT = TFile::Open("output/Histo_h_V0_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V1_TT = TFile::Open("output/Histo_h_V1_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");

    // Check if files are opened successfully
    if (!file_V0_LL || file_V0_LL->IsZombie() || !file_V1_LL || file_V1_LL->IsZombie() ||
        !file_V0_TT || file_V0_TT->IsZombie() || !file_V1_TT || file_V1_TT->IsZombie()) {
        std::cout << "Failed to open one or more files!" << std::endl;
        return;
    }

    // Extract histograms from the files
    auto hist_V0_LL = (TH1F*)file_V0_LL->Get("h_V0_p_theta");
    auto hist_V1_LL = (TH1F*)file_V1_LL->Get("h_V1_p_theta");
    auto hist_V0_TT = (TH1F*)file_V0_TT->Get("h_V0_p_theta");
    auto hist_V1_TT = (TH1F*)file_V1_TT->Get("h_V1_p_theta");

    // Check if histograms are retrieved successfully
    if (!hist_V0_LL || !hist_V1_LL || !hist_V0_TT || !hist_V1_TT) {
        std::cout << "Failed to retrieve histograms!" << std::endl;
        return;
    }

    // Combine histograms
    hist_V0_LL->Add(hist_V1_LL);  // Add contents of V1_LL to V0_LL
    hist_V0_TT->Add(hist_V1_TT);  // Add contents of V1_TT to V0_TT

    // Customize the appearance of the histograms
    hist_V0_LL->SetLineColor(kRed);
    hist_V0_LL->SetLineWidth(2);

    hist_V0_TT->SetLineColor(kBlue);
    hist_V0_TT->SetLineWidth(2);

    hist_V0_LL->GetXaxis()->SetTitle("p_theta");
    hist_V0_LL->GetYaxis()->SetTitle("Entries");

    // Normalize histograms
    hist_V0_LL->Scale(1. / hist_V0_LL->Integral());
    hist_V0_TT->Scale(1. / hist_V0_TT->Integral());

    // Create a canvas to draw the histograms
    auto canvas = new TCanvas("canvas", "Combined Histogram", 800, 600);
    hist_V0_LL->Draw("hist");
    hist_V0_TT->Draw("samehist");

    // Add a legend
    auto legend = new TLegend(0.7, 0.7, 0.9, 0.9);
    legend->AddEntry(hist_V0_LL, "Polarized LL (combined)", "l");
    legend->AddEntry(hist_V0_TT, "Polarized TT (combined)", "l");
    legend->Draw();

    // Save the canvas as an image in the output_histograms folder
    std::string output_file = std::string(output_dir) + "/p_theta_V0_V1_combined_histogram.png";
    canvas->SaveAs(output_file.c_str());

    // Close the files
    file_V0_LL->Close();
    file_V1_LL->Close();
    file_V0_TT->Close();
    file_V1_TT->Close();
}