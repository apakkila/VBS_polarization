#include <map>
#include <vector>
#include "TH1.h"
#include "TFile.h"
using namespace std;

struct Sample {
  string name;
  string nicename;
  string legend;

  int color;
  vector<string> subsamples;

  float yield;
  map<string, float> subsamples_yield;

  map<string, float> yield_systs;
  map<string, map<string, float>> subsamples_yield_systs;

  TH1D* h = nullptr;
  map<string, TH1D*> h_subSamples;

  map<string, TH1D*> h_systs;
  map<string, map<string, TH1D*>> h_subSamples_systs;

  void ClearHistos()
  {
    if(h) delete h;
    for(auto const& pair : h_subSamples){
      cout << pair.second << endl;
      if (pair.second) delete pair.second;
    }
    for(auto const& pair : h_systs){
      if (pair.second) delete pair.second;
    }
    for(auto const& pair : h_subSamples_systs){
      for(auto const& pair2 : pair.second){
        if (pair2.second) delete pair2.second;
      }
    }
  }
};
map<string, Sample*> GetMapOfSamples(){
  map<string, Sample*> samples;

  samples["DataUL16"] = new Sample;
  samples["DataUL16"]->name      = "Data16";
  samples["DataUL16"]->nicename  = "Data16";
  samples["DataUL16"]->legend    = "Data";
  samples["DataUL16"]->color     = kBlack;
  samples["DataUL16"]->subsamples = {
    "DataUL16APVB_JetHT",
    "DataUL16APVC_JetHT",
    "DataUL16APVD_JetHT",
    "DataUL16APVE_JetHT",
    "DataUL16APVF_JetHT",
    "DataUL16PostAPVF_JetHT",
    "DataUL16PostAPVG_JetHT",
    "DataUL16PostAPVH_JetHT",
  };

  samples["DataUL16APV"] = new Sample;
  samples["DataUL16APV"]->name      = "DataUL16APV";
  samples["DataUL16APV"]->nicename  = "Data16Early";
  samples["DataUL16APV"]->legend    = "Data";
  samples["DataUL16APV"]->color     = kBlack;
  samples["DataUL16APV"]->subsamples = {
    "DataUL16APVB_JetHT",
    "DataUL16APVC_JetHT",
    "DataUL16APVD_JetHT",
    "DataUL16APVE_JetHT",
    "DataUL16APVF_JetHT",
  };

  samples["DataUL16PostAPV"] = new Sample;
  samples["DataUL16PostAPV"]->name      = "DataUL16PostAPV";
  samples["DataUL16PostAPV"]->nicename  = "Data16Late";
  samples["DataUL16PostAPV"]->legend    = "Data";
  samples["DataUL16PostAPV"]->color     = kBlack;
  samples["DataUL16PostAPV"]->subsamples = {
    "DataUL16PostAPVF_JetHT",
    "DataUL16PostAPVG_JetHT",
    "DataUL16PostAPVH_JetHT",
  };

  samples["DataUL17"] = new Sample;
  samples["DataUL17"]->name     = "DataUL17";
  samples["DataUL17"]->nicename = "Data17";
  samples["DataUL17"]->legend   = "Data";
  samples["DataUL17"]->color    = kBlack;
  samples["DataUL17"]->subsamples = {
    "DataUL17B_JetHT",
    "DataUL17C_JetHT",
    "DataUL17D_JetHT",
    "DataUL17E_JetHT",
    "DataUL17F_JetHT",
  };

  samples["DataUL18"] = new Sample;
  samples["DataUL18"]->name     = "DataUL18";
  samples["DataUL18"]->nicename = "Data18";
  samples["DataUL18"]->legend   = "Data";
  samples["DataUL18"]->color    = kBlack;
  samples["DataUL18"]->subsamples = {
    "DataUL18A_JetHT",
    "DataUL18B_JetHT",
    "DataUL18C_JetHT",
    "DataUL18D_JetHT",
  };

  vector<string> mcEraNames = {
    "MCUL16",
    "MCUL16APV",
    "MCUL16PostAPV",
    "MCUL17",
    "MCUL18"
  };

  for (unsigned int i=0; i < mcEraNames.size();i++){
    std::string mcEra = mcEraNames.at(i);
    //
    //
    //
    samples[mcEra+"_QCD_HT"] = new Sample;
    samples[mcEra+"_QCD_HT"]->name     = mcEra+"_QCD_HT";
    samples[mcEra+"_QCD_HT"]->nicename = mcEra+"_QCD_HT";
    samples[mcEra+"_QCD_HT"]->legend   = "QCD";
    samples[mcEra+"_QCD_HT"]->color    = kGreen;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_QCD_HT"]->subsamples = {
        "MCUL16APV_QCD_HT50to100",
        "MCUL16APV_QCD_HT100to200",
        "MCUL16APV_QCD_HT200to300",
        "MCUL16APV_QCD_HT300to500",
        "MCUL16APV_QCD_HT500to700",
        "MCUL16APV_QCD_HT700to1000",
        "MCUL16APV_QCD_HT1000to1500",
        "MCUL16APV_QCD_HT1500to2000",
        "MCUL16APV_QCD_HT2000toInf",
        "MCUL16PostAPV_QCD_HT50to100",
        "MCUL16PostAPV_QCD_HT100to200",
        "MCUL16PostAPV_QCD_HT200to300",
        "MCUL16PostAPV_QCD_HT300to500",
        "MCUL16PostAPV_QCD_HT500to700",
        "MCUL16PostAPV_QCD_HT700to1000",
        "MCUL16PostAPV_QCD_HT1000to1500",
        "MCUL16PostAPV_QCD_HT1500to2000",
        "MCUL16PostAPV_QCD_HT2000toInf",
      };
    }
    else{
      samples[mcEra+"_QCD_HT"]->subsamples = {
        mcEra+"_QCD_HT50to100",
        mcEra+"_QCD_HT100to200",
        mcEra+"_QCD_HT200to300",
        mcEra+"_QCD_HT300to500",
        mcEra+"_QCD_HT500to700",
        mcEra+"_QCD_HT700to1000",
        mcEra+"_QCD_HT1000to1500",
        mcEra+"_QCD_HT1500to2000",
        mcEra+"_QCD_HT2000toInf",
      };
    }

    samples[mcEra+"_WJetsToQQ"] = new Sample;
    samples[mcEra+"_WJetsToQQ"]->name     = mcEra+"_WJetsToQQ";
    samples[mcEra+"_WJetsToQQ"]->nicename = mcEra+"_WJetsToQQ";
    samples[mcEra+"_WJetsToQQ"]->legend   = "W+jets";
    samples[mcEra+"_WJetsToQQ"]->color    = kBlue+1;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_WJetsToQQ"]->subsamples = {
        "MCUL16APV_WJetsToQQ_HT200to400",
        "MCUL16APV_WJetsToQQ_HT400to600",
        "MCUL16APV_WJetsToQQ_HT600to800",
        "MCUL16APV_WJetsToQQ_HT800toInf",
        "MCUL16PostAPV_WJetsToQQ_HT200to400",
        "MCUL16PostAPV_WJetsToQQ_HT400to600",
        "MCUL16PostAPV_WJetsToQQ_HT600to800",
        "MCUL16PostAPV_WJetsToQQ_HT800toInf",
      };
    }
    else{
      samples[mcEra+"_WJetsToQQ"]->subsamples = {
        mcEra+"_WJetsToQQ_HT200to400",
        mcEra+"_WJetsToQQ_HT400to600",
        mcEra+"_WJetsToQQ_HT600to800",
        mcEra+"_WJetsToQQ_HT800toInf",
      };
    }

    samples[mcEra+"_ZJetsToQQ"] = new Sample;
    samples[mcEra+"_ZJetsToQQ"]->name     = mcEra+"_ZJetsToQQ";
    samples[mcEra+"_ZJetsToQQ"]->nicename = mcEra+"_ZJetsToQQ";
    samples[mcEra+"_ZJetsToQQ"]->legend   = "Z+jets";
    samples[mcEra+"_ZJetsToQQ"]->color    = kBlue+2;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_ZJetsToQQ"]->subsamples = {
        "MCUL16APV_ZJetsToQQ_HT200to400",
        "MCUL16APV_ZJetsToQQ_HT400to600",
        "MCUL16APV_ZJetsToQQ_HT600to800",
        "MCUL16APV_ZJetsToQQ_HT800toInf",
        "MCUL16PostAPV_ZJetsToQQ_HT200to400",
        "MCUL16PostAPV_ZJetsToQQ_HT400to600",
        "MCUL16PostAPV_ZJetsToQQ_HT600to800",
        "MCUL16PostAPV_ZJetsToQQ_HT800toInf",
      };
    }
    else{
      samples[mcEra+"_ZJetsToQQ"]->subsamples = {
        mcEra+"_ZJetsToQQ_HT200to400",
        mcEra+"_ZJetsToQQ_HT400to600",
        mcEra+"_ZJetsToQQ_HT600to800",
        mcEra+"_ZJetsToQQ_HT800toInf",
      };
    }

    samples[mcEra+"_VJetsToQQ"] = new Sample;
    samples[mcEra+"_VJetsToQQ"]->name     = mcEra+"_VJetsToQQ";
    samples[mcEra+"_VJetsToQQ"]->nicename = mcEra+"_VJetsToQQ";
    samples[mcEra+"_VJetsToQQ"]->legend   = "V+jets";
    samples[mcEra+"_VJetsToQQ"]->color    = kBlue;
    samples[mcEra+"_VJetsToQQ"]->subsamples.insert(
      samples[mcEra+"_VJetsToQQ"]->subsamples.end(),
      samples[mcEra+"_WJetsToQQ"]->subsamples.begin(),
      samples[mcEra+"_WJetsToQQ"]->subsamples.end()
    );
    samples[mcEra+"_VJetsToQQ"]->subsamples.insert(
      samples[mcEra+"_VJetsToQQ"]->subsamples.end(),
      samples[mcEra+"_ZJetsToQQ"]->subsamples.begin(),
      samples[mcEra+"_ZJetsToQQ"]->subsamples.end()
    );

    samples[mcEra+"_TT"] = new Sample;
    samples[mcEra+"_TT"]->name     = mcEra+"_TT";
    samples[mcEra+"_TT"]->nicename = mcEra+"_TT";
    samples[mcEra+"_TT"]->legend   = "t#bar{t}";
    samples[mcEra+"_TT"]->color    = kOrange;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_TT"]->subsamples = {
        "MCUL16APV_TT_0L",
        "MCUL16APV_TT_1L",
        "MCUL16APV_TT_2L",
        "MCUL16PostAPV_TT_0L",
        "MCUL16PostAPV_TT_1L",
        "MCUL16PostAPV_TT_2L",
      };
    }
    else{
      samples[mcEra+"_TT"]->subsamples = {
        mcEra+"_TT_0L",
        mcEra+"_TT_1L",
        mcEra+"_TT_2L",
      };
    }

    samples[mcEra+"_ST"] = new Sample;
    samples[mcEra+"_ST"]->name     = mcEra+"_ST";
    samples[mcEra+"_ST"]->nicename = mcEra+"_ST";
    samples[mcEra+"_ST"]->legend   = "Single-t";
    samples[mcEra+"_ST"]->color    = kOrange;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_ST"]->subsamples = {
        "MCUL16APV_ST_schan_hadronicDecays",
        "MCUL16APV_ST_tW_antitop",
        "MCUL16APV_ST_tW_top",
        "MCUL16APV_ST_tchan_antitop",
        "MCUL16APV_ST_tchan_top",
        "MCUL16PostAPV_ST_schan_hadronicDecays",
        "MCUL16PostAPV_ST_tW_antitop",
        "MCUL16PostAPV_ST_tW_top",
        "MCUL16PostAPV_ST_tchan_antitop",
        "MCUL16PostAPV_ST_tchan_top",
      };
    }
    else{
      samples[mcEra+"_ST"]->subsamples = {
        mcEra+"_ST_schan_hadronicDecays",
        mcEra+"_ST_tW_antitop",
        mcEra+"_ST_tW_top",
        mcEra+"_ST_tchan_antitop",
        mcEra+"_ST_tchan_top",
      };
    }


    //
    //
    //
    samples[mcEra+"_TOP"] = new Sample;
    samples[mcEra+"_TOP"]->name     = mcEra+"_TOP";
    samples[mcEra+"_TOP"]->nicename = mcEra+"_TOP";
    samples[mcEra+"_TOP"]->legend   = "t#bar{t}/t";
    samples[mcEra+"_TOP"]->color    = kOrange;
    samples[mcEra+"_TOP"]->subsamples.insert(
      samples[mcEra+"_TOP"]->subsamples.end(),
      samples[mcEra+"_TT"]->subsamples.begin(),
      samples[mcEra+"_TT"]->subsamples.end()
    );
    samples[mcEra+"_TOP"]->subsamples.insert(
      samples[mcEra+"_TOP"]->subsamples.end(),
      samples[mcEra+"_ST"]->subsamples.begin(),
      samples[mcEra+"_ST"]->subsamples.end()
    );


    //
    //
    //
    samples[mcEra+"_VV_LO"]  = new Sample;
    samples[mcEra+"_VV_LO"]->name     = mcEra+"_VV_LO";
    samples[mcEra+"_VV_LO"]->nicename = mcEra+"_VV_LO";
    samples[mcEra+"_VV_LO"]->legend   = "VV (LO)";
    samples[mcEra+"_VV_LO"]->color    = kMagenta;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VV_LO"]->subsamples = {
        "MCUL16APV_WW",
        "MCUL16APV_WZ",
        "MCUL16APV_ZZ",
        "MCUL16PostAPV_WW",
        "MCUL16PostAPV_WZ",
        "MCUL16PostAPV_ZZ",
      };
    }
    else{
      samples[mcEra+"_VV_LO"]->subsamples = {
        mcEra+"_WW",
        mcEra+"_WZ",
        mcEra+"_ZZ",
      };
    }


    //
    //
    //
    samples[mcEra+"_VV_NLO"]  = new Sample;
    samples[mcEra+"_VV_NLO"]->name     = mcEra+"_VV_NLO";
    samples[mcEra+"_VV_NLO"]->nicename = mcEra+"_VV_NLO";
    samples[mcEra+"_VV_NLO"]->legend   = "VV (NLO)";
    samples[mcEra+"_VV_NLO"]->color    = kMagenta;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VV_NLO"]->subsamples = {
        "MCUL16APV_WZTo2Q2L",
        "MCUL16APV_ZZTo2Q2L",
        "MCUL16APV_WWTo1L1Nu2Q",
        "MCUL16APV_ZZTo4Q",
        "MCUL16APV_WWTo4Q",
        "MCUL16PostAPV_WZTo2Q2L",
        "MCUL16PostAPV_ZZTo2Q2L",
        "MCUL16PostAPV_WWTo1L1Nu2Q",
        "MCUL16PostAPV_ZZTo4Q",
        "MCUL16PostAPV_WWTo4Q"
      };
    }
    else{
      samples[mcEra+"_VV_NLO"]->subsamples = {
        mcEra+"_WZTo2Q2L",
        mcEra+"_ZZTo2Q2L",
        mcEra+"_WWTo1L1Nu2Q",
        mcEra+"_ZZTo4Q",
        mcEra+"_WWTo4Q",
      };
    }

    samples[mcEra+"_VVV_NLO"]  = new Sample;
    samples[mcEra+"_VVV_NLO"]->name     = mcEra+"_VVV_NLO";
    samples[mcEra+"_VVV_NLO"]->nicename = mcEra+"_VVV_NLO";
    samples[mcEra+"_VVV_NLO"]->legend   = "VVV (NLO)";
    samples[mcEra+"_VVV_NLO"]->color    = kMagenta+1;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VVV_NLO"]->subsamples = {
        "MCUL16APV_WWW",
        "MCUL16APV_WWZ",
        "MCUL16APV_WZZ",
        "MCUL16APV_ZZZ",
        "MCUL16PostAPV_WWW",
        "MCUL16PostAPV_WWZ",
        "MCUL16PostAPV_WZZ",
        "MCUL16PostAPV_ZZZ",
      };
    }
    else{
      samples[mcEra+"_VVV_NLO"]->subsamples = {
        mcEra+"_WWW",
        mcEra+"_WWZ",
        mcEra+"_WZZ",
        mcEra+"_ZZZ",
      };
    }

    //
    //
    //
    samples[mcEra+"_VBF"]  = new Sample;
    samples[mcEra+"_VBF"]->name     = mcEra+"_VBF";
    samples[mcEra+"_VBF"]->nicename = mcEra+"_VBF";
    samples[mcEra+"_VBF"]->legend   = "VBF";
    samples[mcEra+"_VBF"]->color    = kCyan;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VBF"]->subsamples = {
          "MCUL16APV_EWKWm2Jets_WToQQ",
          "MCUL16APV_EWKWp2Jets_WToQQ",
          "MCUL16APV_EWKZ2Jets_ZToQQ",
          "MCUL16PostAPV_EWKWm2Jets_WToQQ",
          "MCUL16PostAPV_EWKWp2Jets_WToQQ",
          "MCUL16PostAPV_EWKZ2Jets_ZToQQ",
      };
    }
    else{
      samples[mcEra+"_VBF"]->subsamples = {
          mcEra+"_EWKWm2Jets_WToQQ",
          mcEra+"_EWKWp2Jets_WToQQ",
          mcEra+"_EWKZ2Jets_ZToQQ",
      };
    }
    //
    //
    //
    samples[mcEra+"_VBS_WW_EWK"]  = new Sample;
    samples[mcEra+"_VBS_WW_EWK"]->name     = mcEra+"_VBS_WW_EWK";
    samples[mcEra+"_VBS_WW_EWK"]->nicename = mcEra+"_VBS_WW_EWK";
    samples[mcEra+"_VBS_WW_EWK"]->legend   = "VBS WW (EWK)";
    samples[mcEra+"_VBS_WW_EWK"]->color    = kRed+1;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VBS_WW_EWK"]->subsamples = {
        "MCUL16APV_VBS_WWOSTo4J_EWK",
        "MCUL16APV_VBS_WWSSTo4J_EWK",
        "MCUL16NonAPV_VBS_WWOSTo4J_EWK",
        "MCUL16NonAPV_VBS_WWSSTo4J_EWK",
      };
    }
    else{
      samples[mcEra+"_VBS_WW_EWK"]->subsamples = {
        mcEra+"_VBS_WWOSTo4J_EWK",
        mcEra+"_VBS_WWSSTo4J_EWK",
      };
    }

    //
    //
    //
    samples[mcEra+"_VBS_WW_QCD"]  = new Sample;
    samples[mcEra+"_VBS_WW_QCD"]->name     = mcEra+"_VBS_WW_QCD";
    samples[mcEra+"_VBS_WW_QCD"]->nicename = mcEra+"_VBS_WW_QCD";
    samples[mcEra+"_VBS_WW_QCD"]->legend   = "VBS WW (QCD)";
    samples[mcEra+"_VBS_WW_QCD"]->color    = kRed+2;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VBS_WW_QCD"]->subsamples = {
        "MCUL16APV_VBS_WWOSTo4J_QCD",
        "MCUL16APV_VBS_WWSSTo4J_QCD",
        "MCUL16PostAPV_VBS_WWOSTo4J_QCD",
        "MCUL16PostAPV_VBS_WWSSTo4J_QCD",
      };
    }
    else{
      samples[mcEra+"_VBS_WW_QCD"]->subsamples = {
        mcEra+"_VBS_WWOSTo4J_QCD",
        mcEra+"_VBS_WWSSTo4J_QCD",
      };
    }

    //
    //
    //
    samples[mcEra+"_VBS_WZ"]  = new Sample;
    samples[mcEra+"_VBS_WZ"]->name     = mcEra+"_VBS_WZ";
    samples[mcEra+"_VBS_WZ"]->nicename = mcEra+"_VBS_WZ";
    samples[mcEra+"_VBS_WZ"]->legend   = "VBS WZ";
    samples[mcEra+"_VBS_WZ"]->color    = kRed+3;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VBS_WZ"]->subsamples = {
        "MCUL16APV_VBS_ZWTo4J_EWK",
        "MCUL16APV_VBS_ZWTo4J_QCD",
        "MCUL16PostAPV_VBS_ZWTo4J_EWK",
        "MCUL16PostAPV_VBS_ZWTo4J_QCD",
      };
    }
    else{
      samples[mcEra+"_VBS_WZ"]->subsamples = {
        mcEra+"_VBS_ZWTo4J_EWK",
        mcEra+"_VBS_ZWTo4J_QCD",
      };
    }

    //
    //
    //
    samples[mcEra+"_VBS_ZZ"]  = new Sample;
    samples[mcEra+"_VBS_ZZ"]->name     = mcEra+"_VBS_ZZ";
    samples[mcEra+"_VBS_ZZ"]->nicename = mcEra+"_VBS_ZZ";
    samples[mcEra+"_VBS_ZZ"]->legend   = "VBS ZZ";
    samples[mcEra+"_VBS_ZZ"]->color    = kRed+4;
    if (mcEra == "MCUL16"){
      samples[mcEra+"_VBS_ZZ"]->subsamples = {
        "MCUL16APV_VBS_ZZTo4J_QCD",
        "MCUL16PostAPV_VBS_ZZTo4J_QCD",
      };
    }
    else{
      samples[mcEra+"_VBS_ZZ"]->subsamples = {
        mcEra+"_VBS_ZZTo4J_QCD",
      };
    }
  }



  // =============================================
  //
  // Run2
  //
  // =============================================

  samples["DataULRun2"] = new Sample;
  samples["DataULRun2"]->name     = "DataULRun2";
  samples["DataULRun2"]->nicename = "DataULRun2";
  samples["DataULRun2"]->legend   = "Data";
  samples["DataULRun2"]->color    = kBlack;
  samples["DataULRun2"]->subsamples = {};
  samples["DataULRun2"]->subsamples.insert(
    samples["DataULRun2"]->subsamples.end(),
    samples["DataUL16"]->subsamples.begin(),
    samples["DataUL16"]->subsamples.end()
  );
  samples["DataULRun2"]->subsamples.insert(
    samples["DataULRun2"]->subsamples.end(),
    samples["DataUL17"]->subsamples.begin(),
    samples["DataUL17"]->subsamples.end()
  );
  samples["DataULRun2"]->subsamples.insert(
    samples["DataULRun2"]->subsamples.end(),
    samples["DataUL18"]->subsamples.begin(),
    samples["DataUL18"]->subsamples.end()
  );

  //
  //
  //
  auto combSamplesRun2UL = [&samples](string _SampleName, string _Run2Name, string _Run2SingleEraName) {
    samples[_Run2Name+"_"+_SampleName] = new Sample;
    samples[_Run2Name+"_"+_SampleName]->name     = _Run2Name+"_"+_SampleName;
    samples[_Run2Name+"_"+_SampleName]->nicename = _Run2Name+"_"+_SampleName;
    samples[_Run2Name+"_"+_SampleName]->legend   = samples[_Run2SingleEraName+"_"+_SampleName]->legend;
    samples[_Run2Name+"_"+_SampleName]->color    = samples[_Run2SingleEraName+"_"+_SampleName]->color;
    samples[_Run2Name+"_"+_SampleName]->subsamples = {};
    vector<string> mcEraFullRun2Names = {
      "MCUL16APV",
      "MCUL16PostAPV",
      "MCUL17",
      "MCUL18"
    };
    for (unsigned int i=0; i < mcEraFullRun2Names.size();i++){
      std::string mcEra = mcEraFullRun2Names.at(i);
      samples[_Run2Name+"_"+_SampleName]->subsamples.insert(
        samples[_Run2Name+"_"+_SampleName]->subsamples.end(),
        samples[mcEra+"_"+_SampleName]->subsamples.begin(),
        samples[mcEra+"_"+_SampleName]->subsamples.end()
      );
    }
  };

  combSamplesRun2UL("QCD_HT","MCULRun2","MCUL17");
  combSamplesRun2UL("WJetsToQQ","MCULRun2","MCUL17");
  combSamplesRun2UL("ZJetsToQQ","MCULRun2","MCUL17");
  combSamplesRun2UL("VJetsToQQ","MCULRun2","MCUL17");
  combSamplesRun2UL("TOP","MCULRun2","MCUL17");
  combSamplesRun2UL("VV_LO","MCULRun2","MCUL17");
  combSamplesRun2UL("VV_NLO","MCULRun2","MCUL17");
  combSamplesRun2UL("VVV_NLO","MCULRun2","MCUL17");
  combSamplesRun2UL("VBF","MCULRun2","MCUL17");
  combSamplesRun2UL("VBS_WW_EWK","MCULRun2","MCUL17");
  combSamplesRun2UL("VBS_WW_QCD","MCULRun2","MCUL17");
  combSamplesRun2UL("VBS_WZ","MCULRun2","MCUL17");
  combSamplesRun2UL("VBS_ZZ","MCULRun2","MCUL17");

  // cout << samples["MCULRun2_VV_LO"]->name << endl;

  return samples;
}
