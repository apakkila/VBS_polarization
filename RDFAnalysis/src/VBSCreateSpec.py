import json
import ROOT
from typing import List
from VBSHelpers import findFiles, parseFileName

if __name__ == "__main__":
    input_filelist = "inputfiles/filelist.txt"
    json_vars = "inputfiles/variables.json"
    
    # HOX! FromSpec has an issue that /eos/ is not recognized as a valid path (even on lxplus)
    # This can also be changed to other prefixes
    file_prefix = "root://eosuser.cern.ch/"
    
    with open(json_vars) as f:
        json_variables = json.load(f)
        
    filelist = findFiles(input_filelist)
    
    result_dict = {"samples" : {}}
    MC_dict = {"samples" : {}}
    Data_dict = {"samples" : {}}    
    for file in filelist:
        parsed_file = parseFileName(file)
        
        result_dict["samples"][parsed_file["full_name"]] = {}
        result_dict["samples"][parsed_file["full_name"]]["trees"] = ["Events"]
        result_dict["samples"][parsed_file["full_name"]]["files"] = [file_prefix + file]
        
        # Define metadata
        result_dict["samples"][parsed_file["full_name"]]["metadata"] = {}
        result_dict["samples"][parsed_file["full_name"]]["metadata"]["lumi"] = json_variables["lumi"][parsed_file["year"][0]]
        result_dict["samples"][parsed_file["full_name"]]["metadata"]["lumiUp"] = json_variables["lumiUp"][parsed_file["year"][0]]
        result_dict["samples"][parsed_file["full_name"]]["metadata"]["lumiDown"] = json_variables["lumiDown"][parsed_file["year"][0]]
        result_dict["samples"][parsed_file["full_name"]]["metadata"]["MC"] = (1 if parsed_file["isMC"] else 0)
        result_dict["samples"][parsed_file["full_name"]]["metadata"]["sampleName"] = parsed_file["full_name"]
        
        # TODO: 
        # 1. Add a possibility for signal samples or general categorization
        # 2. Add a possibility for different triggers
        # 3. Add a possibility for three different PNet WPs. THESE CANNOT BE LIST DUE TO SPEC
        
        # MC specifics
        if parsed_file["isMC"]:
            full_year = "MC" + parsed_file["year"][0]
            try:
                result_dict["samples"][parsed_file["full_name"]]["metadata"]["xsec"] = json_variables["xs"][full_year][parsed_file["dataset"]]
            except KeyError:
                result_dict["samples"][parsed_file["full_name"]]["metadata"]["xsec"] = 1
                print(f"Cross section for {parsed_file['full_name']} not found in json file")
                
            # Sum of weights, slow in the loop like this, but only done once so...
            rdf = ROOT.RDataFrame("Runs", file)
            ROOT.RDF.Experimental.AddProgressBar(rdf)
            genEventSumw = rdf.Sum("genEventSumw").GetValue()
        
            result_dict["samples"][parsed_file["full_name"]]["metadata"]["sumOfWeights"] = genEventSumw
        
    # Get the MC and Data samples
    for sample in result_dict["samples"]:
        if result_dict["samples"][sample]["metadata"]["MC"]:
            MC_dict["samples"][sample] = result_dict["samples"][sample]
        else:
            Data_dict["samples"][sample] = result_dict["samples"][sample]
        
    # Write to file
    with open("inputfiles/sample_dict.json", "w") as f:
        json.dump(result_dict, f, indent=4)
    with open("inputfiles/MC_samples.json", "w") as f:
        json.dump(MC_dict, f, indent=4)
    with open("inputfiles/DT_samples.json", "w") as f:
        json.dump(Data_dict, f, indent=4)

    print("Done")