void plotting_histograms()
{
    // Create the output directory if it doesn't exist
    const char* output_dir = "output_histograms_visualized";
    struct stat info;
    if (stat(output_dir, &info) != 0) {
        mkdir(output_dir, 0777);
    }

    // collect sample names, 24 in total
    char sample_names[24] = [
        // V0
        "Histo_h_V0_p_theta",
        "Histo_h_V0_z_j",
        "Histo_h_V0_pt",
        "Histo_h_V0_eta",
        "Histo_h_V0_phi",
        "Histo_h_V0_mass",
        
        // V1
        "Histo_h_V1_p_theta",
        "Histo_h_V1_z_j",
        "Histo_h_V1_pt",
        "Histo_h_V1_eta",
        "Histo_h_V1_phi",
        "Histo_h_V1_mass",

        // VV
        "Histo_h_VV_deta",
        "Histo_h_VV_dphi",
        "Histo_h_VV_mVV",

        // TagJJ
        "Histo_h_TagJJ_deta",
        "Histo_h_TagJJ_dphi",
        "Histo_h_TagJJ_mJJ",

        // TagJet0
        "Histo_h_Tagjet0_eta", 
        "Histo_h_Tagjet0_pt",  
        "Histo_h_Tagjet0_phi", 
        "Histo_h_Tagjet0_mass", 
        
        // TagJet1
        "Histo_h_Tagjet1_eta", 
        "Histo_h_Tagjet1_pt",
        "Histo_h_Tagjet1_phi", 
        "Histo_h_Tagjet1_mass",
        ];


    // iterate over the file names and collect the histograms to a disctionary


    // plot the histograms in the same dictionary into one plot, 7 in total per plot

        // How to extract the sample names? They are basically in the same order as the file names, so we can use the same index to access them.

    // Open the .root files

    // Check if the files are opened successfully

    // Extract histograms from the files

    // Combine histograms

    // Set color lines for the plots

    // Set line widths for the plots

    // Name the axis of the plots

    // Normalize histograms

    // Create canvas to plot the histograms

    // Add a legend

    // Save the canvas as an image in the output_histograms_visualized folder

    // Close the files

}