import os
import subprocess
import sys, json

def main(datasetName,sampleName, USERdataset=False):
  if not(USERdataset):
    out = subprocess.check_output("dasgoclient -json --query 'file dataset=%s'" %(datasetName), shell=True)
  else:
    out = subprocess.check_output("dasgoclient -json --query 'file dataset=%s instance=prod/phys03'" %(datasetName), shell=True)

  list_jsonDict = json.loads(out) # Get list of dictionary. Each element of list is for a file.

  fout = f"{sampleName}.txt"
  fo = open(fout, "w")
  print(f"Making {fout} with nfiles={len(list_jsonDict)}")
  for data in list_jsonDict:
    file_name = data["file"][0]["name"]
    fo.write(file_name+'\n')
  fo.close()


datasetDict = {
"WPJJWMJJjj_EWK_LO_4f_mmjj150"  : "/WPJJWMJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_QCD_LO_4f_mmjj150"  : "/WPJJWMJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_LO_4f_mmjj150": "/WPMJJWPMJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_QCD_LO_4f_mmjj150": "/WPMJJWPMJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_EWK_LO_4f_mmjj150"  : "/ZJJWPMJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_QCD_LO_4f_mmjj150"  : "/ZJJWPMJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJZJJjj_EWK_LO_4f_mmjj150"    : "/ZJJZJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJZJJjj_QCD_LO_4f_mmjj150"    : "/ZJJZJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZNuNuWPMJJjj_EWK_LO_4f_mmjj150": "/ZNuNuWPMJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZNuNuWPMJJjj_QCD_LO_4f_mmjj150": "/ZNuNuWPMJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZNuNuZJJjj_EWK_LO_4f_mmjj150"  : "/ZNuNuZJJjj_EWK_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZNuNuZJJjj_QCD_LO_4f_mmjj150"  : "/ZNuNuZJJjj_QCD_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
#
"WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150"     : "/WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150"     : "/WPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150"     : "/WPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150"     : "/WPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150"   : "/WPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150" : "/WPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150"   : "/WPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_EWK_PolarLL_FrameZW_LO_4f_mmjj150"     : "/ZJJWPMJJjj_EWK_PolarLL_FrameZW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_EWK_PolarLT_FrameZW_LO_4f_mmjj150"     : "/ZJJWPMJJjj_EWK_PolarLT_FrameZW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_EWK_PolarTL_FrameZW_LO_4f_mmjj150"     : "/ZJJWPMJJjj_EWK_PolarTL_FrameZW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJWPMJJjj_EWK_PolarTT_FrameZW_LO_4f_mmjj150"     : "/ZJJWPMJJjj_EWK_PolarTT_FrameZW_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJZJJjj_EWK_PolarLTTL_FrameZZ_LO_4f_mmjj150"     : "/ZJJZJJjj_EWK_PolarLTTL_FrameZZ_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"ZJJZJJjj_EWK_PolarTT_FrameZZ_LO_4f_mmjj150"       : "/ZJJZJJjj_EWK_PolarTT_FrameZZ_LO_4f_mmjj150_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
#
"WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300"    :"/WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300"    :"/WPJJWMJJjj_EWK_PolarLT_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300"    :"/WPJJWMJJjj_EWK_PolarTL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300"    :"/WPJJWMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300"  :"/WPMJJWPMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300":"/WPMJJWPMJJjj_EWK_PolarLTTL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
"WPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300"  :"/WPMJJWPMJJjj_EWK_PolarTT_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
#
# "WPJJWMJJjj_EWK_LO_4f_mmjj150_ptW300"   : "/WPJJWMJJjj_EWK_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "WPMJJWPMJJjj_EWK_LO_4f_mmjj150_ptW300" : "/WPMJJWPMJJjj_EWK_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "ZJJWPMJJjj_EWK_LO_4f_mmjj150_ptV300"   : "/ZJJWPMJJjj_EWK_LO_4f_mmjj150_ptV300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "ZJJZJJjj_EWK_LO_4f_mmjj150_ptZ300"     : "/ZJJZJJjj_EWK_LO_4f_mmjj150_ptZ300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "WPJJWMJJjj_EWK_LO_4f_mmjj150_mWW500"   : "/WPJJWMJJjj_EWK_LO_4f_mmjj150_mWW500_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "WPMJJWPMJJjj_EWK_LO_4f_mmjj150_mWW500" : "/WPMJJWPMJJjj_EWK_LO_4f_mmjj150_mWW500_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "ZJJWPMJJjj_EWK_LO_4f_mmjj150_mZW500"   : "/ZJJWPMJJjj_EWK_LO_4f_mmjj150_mZW500_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
# "ZJJZJJjj_EWK_LO_4f_mmjj150_mZZ500"     : "/ZJJZJJjj_EWK_LO_4f_mmjj150_mZZ500_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER",
#
# "NanoV15_WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300": "/WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoAODv15_v3p0_prodv2-00000000000000000000000000000000/USER",
# "NanoGen_WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300":"/WPJJWMJJjj_EWK_PolarLL_FrameWW_LO_4f_mmjj150_ptW300_madgraph_pythia8/nbinnorj-RunIII2024Summer24NanoGeN_v1p0-00000000000000000000000000000000/USER"
}

for key in datasetDict:
  datasetName=datasetDict[key]
  sampleName=key
  main(datasetName,sampleName,USERdataset=True)



# datasetName="/SingleNeutrino_E-10_gun/nbinnorj-Run3Summer22DR_GENSIMRECO_PileupMixing_v2p0-50e8537070b87bdc2ae2b04393d55e09/USER"
# sampleName="USER_Run3Summer22DR_GENSIMRECO_SingleNeutrino_E-10_gun"
# main(datasetName,sampleName,USERdataset=True)


