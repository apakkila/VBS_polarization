void stacked_histogram()
{
    // Create the output directory if it doesn't exist
    const char* output_dir = "output_histograms";
    struct stat info;
    if (stat(output_dir, &info) != 0) {
        mkdir(output_dir, 0777);
    }

    // Open the .root files
    TFile *file_V0_LL = TFile::Open("output/Histo_h_V0_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V0_TT = TFile::Open("output/Histo_h_V0_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    
    TFile *file_V1_LL = TFile::Open("output/Histo_h_V1_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V1_TT = TFile::Open("output/Histo_h_V1_p_theta_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");

    TFile *file_VV_deta_LL = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_deta_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_VV_deta_TT = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_deta_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");

    TFile *file_VV_dphi_LL = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_dphi_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_VV_dphi_TT = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_dphi_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    
    TFile *file_VV_mVV_LL = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_mVV_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_VV_mVV_TT = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_VV_mVV_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");

    TFile *file_V0_z_j_LL = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_V0_z_j_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V1_z_j_LL = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_V1_z_j_Processed_SampleWPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V0_z_j_TT = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_V0_z_j_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");
    TFile *file_V1_z_j_TT = TFile::Open("output_deta_dphi_mVV_zj/Histo_h_V1_z_j_Processed_SampleWPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_CategoryBB_Modulereco_Tagv1p2POL.root");

    // Check if files for p_theta are opened successfully
    if (!file_V0_LL || file_V0_LL->IsZombie() || !file_V1_LL || file_V1_LL->IsZombie() ||
        !file_V0_TT || file_V0_TT->IsZombie() || !file_V1_TT || file_V1_TT->IsZombie()) {
        std::cout << "Failed to open one or more files!" << std::endl;
        return;
    }

    // Check if files deta, dphi and dmVV are opened successfully
    if (!file_VV_deta_LL || file_VV_deta_LL->IsZombie() || !file_VV_deta_TT || file_VV_deta_TT->IsZombie() ||
        !file_VV_dphi_LL || file_VV_dphi_LL->IsZombie() || !file_VV_dphi_TT || file_VV_dphi_TT->IsZombie() ||
        !file_VV_mVV_LL || file_VV_mVV_LL->IsZombie() || !file_VV_mVV_TT || file_VV_mVV_TT->IsZombie()) {
        std::cout << "Failed to open one or more files!" << std::endl;
        return;
    }

    // Check if files for z_j are opened successfully
    if (!file_V0_z_j_LL || file_V0_z_j_LL->IsZombie() || !file_V1_z_j_LL || file_V1_z_j_LL->IsZombie() ||
        !file_V0_z_j_TT || file_V0_z_j_TT->IsZombie() || !file_V1_z_j_TT || file_V1_z_j_TT->IsZombie()) {
        std::cout << "Failed to open one or more files for z_j!" << std::endl;
        return;
    }

    // Extract histograms from the files
    auto hist_V0_LL = (TH1F*)file_V0_LL->Get("h_V0_p_theta");
    auto hist_V0_TT = (TH1F*)file_V0_TT->Get("h_V0_p_theta");

    auto hist_V1_LL = (TH1F*)file_V1_LL->Get("h_V1_p_theta");
    auto hist_V1_TT = (TH1F*)file_V1_TT->Get("h_V1_p_theta");

    auto hist_VV_deta_LL = (TH1F*)file_VV_deta_LL->Get("h_VV_deta");
    auto hist_VV_deta_TT = (TH1F*)file_VV_deta_TT->Get("h_VV_deta");

    auto hist_VV_dphi_LL = (TH1F*)file_VV_dphi_LL->Get("h_VV_dphi");
    auto hist_VV_dphi_TT = (TH1F*)file_VV_dphi_TT->Get("h_VV_dphi");

    auto hist_VV_mVV_LL = (TH1F*)file_VV_mVV_LL->Get("h_VV_mVV");
    auto hist_VV_mVV_TT = (TH1F*)file_VV_mVV_TT->Get("h_VV_mVV");

    auto hist_V0_z_j_LL = (TH1F*)file_V0_z_j_LL->Get("h_V0_z_j");
    auto hist_V1_z_j_LL = (TH1F*)file_V1_z_j_LL->Get("h_V1_z_j");

    auto hist_V0_z_j_TT = (TH1F*)file_V0_z_j_TT->Get("h_V0_z_j");
    auto hist_V1_z_j_TT = (TH1F*)file_V1_z_j_TT->Get("h_V1_z_j");

    // Check if histograms are retrieved successfully
    if (!hist_V0_LL || !hist_V1_LL || !hist_V0_TT || !hist_V1_TT) {
        std::cout << "Failed to retrieve histograms for p_theta!" << std::endl;
        return;
    }

    if (!hist_VV_deta_LL || !hist_VV_deta_TT) {
        std::cout << "Failed to retrieve histograms for deta!" << std::endl;
        return;
    }

    if (!hist_VV_dphi_LL || !hist_VV_dphi_TT) {
        std::cout << "Failed to retrieve histograms for dphi!" << std::endl;
        return;
    }

    if (!hist_VV_mVV_LL || !hist_VV_mVV_TT) {
        std::cout << "Failed to retrieve histograms for mVV!" << std::endl;
        return;
    }

    if (!hist_V0_z_j_LL || !hist_V1_z_j_LL || !hist_V0_z_j_TT || !hist_V1_z_j_TT) {
        std::cout << "Failed to retrieve histograms for z_j!" << std::endl;
        return;
    }

    // Combine histograms
    hist_V0_LL->Add(hist_V1_LL);  // Add contents of V1_LL to V0_LL
    hist_V0_TT->Add(hist_V1_TT);  // Add contents of V1_TT to V0_TT

    hist_V0_z_j_LL->Add(hist_V1_z_j_LL);  // Add contents of V1_z_j_LL to V0_z_j_LL
    hist_V0_z_j_TT->Add(hist_V1_z_j_TT);  // Add contents of V1_z_j_TT to V0_z_j_TT

    // Customize the appearance of the histograms

    // Set color lines for the plots
    hist_V0_LL->SetLineColor(kRed);
    hist_V0_TT->SetLineColor(kBlue);

    hist_VV_deta_LL->SetLineColor(kRed);
    hist_VV_deta_TT->SetLineColor(kBlue);

    hist_VV_dphi_LL->SetLineColor(kRed);
    hist_VV_dphi_TT->SetLineColor(kBlue);
    
    hist_VV_mVV_LL->SetLineColor(kRed);
    hist_VV_mVV_TT->SetLineColor(kBlue);

    hist_V0_z_j_LL->SetLineColor(kRed);
    hist_V0_z_j_TT->SetLineColor(kBlue);


    // Set line widths for the plots
    hist_V0_LL->SetLineWidth(2);
    hist_V0_TT->SetLineWidth(2);
    
    hist_VV_deta_LL->SetLineWidth(2);
    hist_VV_deta_TT->SetLineWidth(2);

    hist_VV_dphi_LL->SetLineWidth(2);
    hist_VV_dphi_TT->SetLineWidth(2);
    
    hist_VV_mVV_LL->SetLineWidth(2);
    hist_VV_mVV_TT->SetLineWidth(2);

    hist_V0_z_j_LL->SetLineWidth(2);
    hist_V0_z_j_TT->SetLineWidth(2);

    // Name the axis of the plots
    hist_V0_LL->GetXaxis()->SetTitle("p_theta");
    hist_V0_LL->GetYaxis()->SetTitle("Entries");

    hist_VV_deta_LL->GetXaxis()->SetTitle("deta");
    hist_VV_deta_TT->GetYaxis()->SetTitle("Entries");

    hist_VV_dphi_LL->GetXaxis()->SetTitle("dphi");
    hist_VV_dphi_TT->GetYaxis()->SetTitle("Entries");

    hist_VV_mVV_LL->GetXaxis()->SetTitle("mVV");
    hist_VV_mVV_TT->GetYaxis()->SetTitle("Entries");

    hist_V0_z_j_LL->GetXaxis()->SetTitle("z_j");
    hist_V0_z_j_TT->GetYaxis()->SetTitle("Entries");

    /*
    
        Plottings for p_theta histogram

    */

    // Normalize histograms
    hist_V0_LL->Scale(1. / hist_V0_LL->Integral());
    hist_V0_TT->Scale(1. / hist_V0_TT->Integral());

    // Create a canvas to draw the histograms
    auto canvas = new TCanvas("canvas", "Combined Histogram", 800, 600);
    hist_V0_LL->Draw("hist");
    hist_V0_TT->Draw("samehist");

    // Add a legend
    auto legend = new TLegend(0.75, 0.75, 0.97, 0.6);
    legend->AddEntry(hist_V0_LL, "Polarized LL (combined)", "l");
    legend->AddEntry(hist_V0_TT, "Polarized TT (combined)", "l");
    legend->Draw();

    // Save the canvas as an image in the output_histograms folder
    std::string output_file = std::string(output_dir) + "/p_theta_V0_V1_combined_histogram.png";
    canvas->SaveAs(output_file.c_str());


    /*
    
        Plottings for deta, dphi, and mVV histograms

    */


    // Create canvases and save plots for deta, dphi, and mVV histograms
    hist_VV_deta_LL->Scale(1. / hist_VV_deta_LL->Integral());
    hist_VV_deta_TT->Scale(1. / hist_VV_deta_TT->Integral());
    
    hist_VV_dphi_LL->Scale(1. / hist_VV_dphi_LL->Integral());
    hist_VV_dphi_TT->Scale(1. / hist_VV_dphi_TT->Integral());

    hist_VV_mVV_LL->Scale(1. / hist_VV_mVV_LL->Integral());
    hist_VV_mVV_TT->Scale(1. / hist_VV_mVV_TT->Integral());

    hist_V0_z_j_LL->Scale(1. / hist_V0_z_j_LL->Integral());
    hist_V0_z_j_TT->Scale(1. / hist_V0_z_j_TT->Integral());

    // Plotting deta
    auto canvas1 = new TCanvas("canvas1", "deta Histogram", 800, 600);
    hist_VV_deta_LL->Draw("hist");
    hist_VV_deta_TT->Draw("samehist");
    auto legend1 = new TLegend(0.75, 0.75, 0.97, 0.6);
    legend1->AddEntry(hist_VV_deta_LL, "Polarized LL (deta)", "l");
    legend1->AddEntry(hist_VV_deta_TT, "Polarized TT (deta)", "l");
    legend1->Draw();
    canvas1->SaveAs((std::string(output_dir) + "/deta_histogram.png").c_str());

    // Plotting dphi
    auto canvas2 = new TCanvas("canvas2", "dphi Histogram", 800, 600);
    hist_VV_dphi_LL->Draw("hist");
    hist_VV_dphi_TT->Draw("samehist");
    auto legend2 = new TLegend(0.75, 0.75, 0.97, 0.6);
    legend2->AddEntry(hist_VV_dphi_LL, "Polarized LL (dphi)", "l");
    legend2->AddEntry(hist_VV_dphi_TT, "Polarized TT (dphi)", "l");
    legend2->Draw();
    canvas2->SaveAs((std::string(output_dir) + "/dphi_histogram.png").c_str());

    // Plotting mVV
    auto canvas3 = new TCanvas("canvas3", "mVV Histogram", 800, 600);
    hist_VV_mVV_LL->Draw("hist");
    hist_VV_mVV_TT->Draw("samehist");
    auto legend3 = new TLegend(0.75, 0.75, 0.97, 0.6);
    legend3->AddEntry(hist_VV_mVV_LL, "Polarized LL (mVV)", "l");
    legend3->AddEntry(hist_VV_mVV_TT, "Polarized TT (mVV)", "l");
    legend3->Draw();
    canvas3->SaveAs((std::string(output_dir) + "/mVV_histogram.png").c_str());


    // Plotting z_j
    auto canvas4 = new TCanvas("canvas4", "z_j histogram", 800, 600);
    hist_V0_z_j_LL->Draw("hist");
    hist_V0_z_j_TT->Draw("samehist");
    auto legend4 = new TLegend(0.75, 0.75, 0.97, 0.6);
    legend4->AddEntry(hist_V0_z_j_LL, "Polarized LL (z_j)", "l");
    legend4->AddEntry(hist_V0_z_j_TT, "Polarized TT (z_j)", "l");
    legend4->Draw();
    canvas4->SaveAs((std::string(output_dir) + "/z_j_histogram.png").c_str());

    // Close the files
    file_V0_LL->Close();
    file_V1_LL->Close();
    file_V0_TT->Close();
    file_V1_TT->Close();
    file_VV_deta_LL->Close();
    file_VV_deta_TT->Close();
    file_VV_dphi_LL->Close();
    file_VV_dphi_TT->Close();
    file_VV_mVV_LL->Close();
    file_VV_mVV_TT->Close();
    file_V0_z_j_LL->Close();
    file_V1_z_j_LL->Close();
    file_V0_z_j_TT->Close();
    file_V1_z_j_TT->Close();
}