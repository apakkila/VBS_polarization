#ifndef NTUPLEMAKER_FUNCTIONS_GENLEVEL
#define NTUPLEMAKER_FUNCTIONS_GENLEVEL

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"
#include "TMath.h"
#include "utility"  // std::swap()
#include "NtupleMaker_Functions.h"

using namespace ROOT::VecOps;
using namespace ROOT::Math;
using RNode = ROOT::RDF::RNode;
using FourVector = ROOT::Math::PtEtaPhiMVector;
using rvec_i  = const RVec<int> &;
using rvec_rvec_i  = const RVec<RVec<int>> &;
using rvec_ul = const RVec<unsigned long> &;
using rvec_f  = const RVec<float> &;
using rvec_rvec_f  = const RVec<RVec<float>> &;

//=========================================================
//
// GenPart and GenLevel functions
//
//=========================================================
RVec<int> GetMotherPDGId(rvec_i genPartIdxMother, rvec_i pdgId)
{
  RVec<int> MotherPDGID(genPartIdxMother.size());
  for (size_t i = 0; i < genPartIdxMother.size(); i++){
    if (genPartIdxMother[i] >= 0){
      MotherPDGID[i] = pdgId[genPartIdxMother[i]];
    }
    else{
      MotherPDGID[i] = 0;
    }
  }
  return MotherPDGID;
}
RVec<int> GetGrandMotherPDGId(rvec_i genPartIdxMother, rvec_i pdgId)
{
  RVec<int> GrandMotherPDGID(genPartIdxMother.size());

  for (size_t i = 0; i < genPartIdxMother.size(); i++){

    // int momIdx      = genPartIdxMother[i];
    // int grandMomIdx = genPartIdxMother[momIdx];

    if (genPartIdxMother[i] >= 0){
      if (genPartIdxMother[genPartIdxMother[i]] >= 0){
        GrandMotherPDGID[i] = pdgId[genPartIdxMother[genPartIdxMother[i]]];
      }
    }
    else{
      GrandMotherPDGID[i] = 0;
    }
  }
  return GrandMotherPDGID;
}
float GetQuarkLeptonMass(const int& pdgId){
  if (abs(pdgId) == 5) return 4.18f;
  else if (abs(pdgId) == 4) return 1.27f;
  else if (abs(pdgId) == 3) return 0.093f;
  else if (abs(pdgId) == 2) return 0.0047f;
  else if (abs(pdgId) == 1) return 0.0022f;
  else if (abs(pdgId) == 11) return 0.00051f;
  else if (abs(pdgId) == 13) return 0.10566f;
  else if (abs(pdgId) == 15) return 1.77686f;
  else return 0.f;
}
//
// For each GenPart, check if it has a mother and give its own idx to the mother.
//
RVec<RVec<int>> GetGenPartIdxDaugther(rvec_i  GenPart_genPartIdxMother){
  RVec<RVec<int>> genPartIdxDaughter(GenPart_genPartIdxMother.size());
  for (size_t idx = 0; idx < GenPart_genPartIdxMother.size(); idx++){
    if (GenPart_genPartIdxMother[idx] >= 0){
      genPartIdxDaughter[GenPart_genPartIdxMother[idx]].emplace_back(idx);
    }
  }
  return genPartIdxDaughter;
}
//
//
//
int isDescendantOf(
  int genPartIdxMother,
  rvec_i GenPart_pdgId,
  rvec_i GenPart_genPartIdxMother,
  int ancestorPDGID
){
  while (genPartIdxMother >= 0){
    if (abs(GenPart_pdgId[genPartIdxMother]) == ancestorPDGID) {
      return 1;
    }
    else{
      return isDescendantOf(
        GenPart_genPartIdxMother[genPartIdxMother],
        GenPart_pdgId,
        GenPart_genPartIdxMother,
        ancestorPDGID
      );
    }
  }
  return 0;
}
int isDescendantOfZ(int genPartIdxMother, rvec_i GenPart_pdgId, rvec_i GenPart_genPartIdxMother){
  return isDescendantOf(genPartIdxMother, GenPart_pdgId, GenPart_genPartIdxMother, 23);
}
int isDescendantOfW(int genPartIdxMother, rvec_i GenPart_pdgId, rvec_i GenPart_genPartIdxMother){
  return isDescendantOf(genPartIdxMother, GenPart_pdgId, GenPart_genPartIdxMother, 24);
}
int isDescendantOfTop(int genPartIdxMother, rvec_i GenPart_pdgId, rvec_i GenPart_genPartIdxMother){
  return isDescendantOf(genPartIdxMother, GenPart_pdgId, GenPart_genPartIdxMother, 6);
}
int isDescendantOfHiggs(int genPartIdxMother, rvec_i GenPart_pdgId, rvec_i GenPart_genPartIdxMother){
  return isDescendantOf(genPartIdxMother, GenPart_pdgId, GenPart_genPartIdxMother, 25);
}

int getIdxFirstCopy(
  int idx,
  int pdgId,
  int genPartIdxMother,
  rvec_i GenPart_pdgId,
  rvec_i GenPart_genPartIdxMother
){
  if (genPartIdxMother >= 0 and abs(GenPart_pdgId[genPartIdxMother]) == pdgId){
    return getIdxFirstCopy(
      genPartIdxMother,
      GenPart_pdgId[genPartIdxMother],
      GenPart_genPartIdxMother[idx],
      GenPart_pdgId,
      GenPart_genPartIdxMother
    );
  }
  return idx;
}
int getIdxLastCopy(
  int idx,
  int pdgId,
  rvec_i GenPart_pdgId,
  rvec_rvec_i GenPart_genPartIdxDaughter
  ){

  int foundDauIdx=-1;

  for (size_t i=0; i < GenPart_genPartIdxDaughter[idx].size(); i++){
    int dauIdx = GenPart_genPartIdxDaughter[idx][i];
    if (GenPart_pdgId[dauIdx] == pdgId) foundDauIdx = dauIdx;
  }

  if (foundDauIdx!=-1){
    return getIdxLastCopy(foundDauIdx, pdgId, GenPart_pdgId, GenPart_genPartIdxDaughter);
  }
  return idx;
}

//
// Right way to do multiple branches for objects in a single loop function
//
RVec<RVec<int>> FatJetGenFlavourLabelsAndGenPartIndex_V2(
  rvec_f  FatJet_eta,
  rvec_f  FatJet_phi,
  rvec_f  GenPart_eta,
  rvec_f  GenPart_phi,
  rvec_i  GenPart_genPartIdxMother,
  rvec_rvec_i GenPart_genPartIdxDaughter,
  rvec_i  GenPart_pdgId,
  rvec_i  GenPart_motherPDGId,
  rvec_i  GenPart_statusFlags,
  rvec_i  GenPart_isWBoson,
  rvec_i  GenPart_isZBoson,
  rvec_i  GenPart_isHBoson,
  rvec_i  GenPart_isTop,
  rvec_i  GenPart_isQuark,
  rvec_i  GenPart_isBQuark,
  rvec_i  GenPart_isCQuark,
  rvec_i  GenPart_isLepton
){
  RVec<RVec<int>> FatJet_FlavourLabel_GenPartIndex(33);

  RVec<int> FlavourLabelW(FatJet_eta.size());
  RVec<int> FlavourLabelZ(FatJet_eta.size());
  RVec<int> FlavourLabelZbb(FatJet_eta.size());
  RVec<int> FlavourLabelZcc(FatJet_eta.size());
  RVec<int> FlavourLabelHbb(FatJet_eta.size());
  RVec<int> FlavourLabelTop(FatJet_eta.size());
  RVec<int> FlavourLabelWFromTop(FatJet_eta.size());
  RVec<int> FlavourIdx_W0_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_W0_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_W0_lep(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_W1_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_W1_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_W1_lep(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z0_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z0_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z0_lep0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z0_lep1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z1_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z1_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z1_lep0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Z1_lep1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_H0_bquark0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_H0_bquark1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_H1_bquark0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_H1_bquark1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Top0_bquark(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop0_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop0_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop0_lep(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_Top1_bquark(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop1_q0(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop1_q1(FatJet_eta.size(),-1);
  RVec<int> FlavourIdx_WFromTop1_lep(FatJet_eta.size(),-1);

  for (size_t i = 0; i < FatJet_eta.size(); i++)
  {
    RVec<float> dR_W;
    RVec<float> dR_Z;
    RVec<float> dR_Higgs;
    RVec<float> dR_Top;

    RVec<int> index_dR_W;
    RVec<int> index_dR_Z;
    RVec<int> index_dR_Higgs;
    RVec<int> index_dR_Top;

    for (size_t ii = 0; ii < GenPart_eta.size(); ii++)
    {
      float dR = ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[ii], FatJet_phi[i], GenPart_phi[ii]);
      //
      // find the W, Z, H, Top, W from Top
      //
      if ((GenPart_statusFlags[ii] & (1 << 13)) == 0) continue; //check should be isLastCopy()

      bool isW = GenPart_isWBoson[ii];
      bool isZ = GenPart_isZBoson[ii];
      bool isHiggs = GenPart_isHBoson[ii];
      bool isTop = GenPart_isTop[ii];
      bool isFromTop = isDescendantOfTop(GenPart_genPartIdxMother[ii], GenPart_pdgId, GenPart_genPartIdxMother);
      bool isWFromTop = GenPart_isWBoson[ii] and isFromTop;

      if (isW){
        dR_W.emplace_back(dR);
        index_dR_W.emplace_back(ii);
      }
      if (isZ){
        dR_Z.emplace_back(dR);
        index_dR_Z.emplace_back(ii);
      }
      if (isHiggs){
        dR_Higgs.emplace_back(dR);
        index_dR_Higgs.emplace_back(ii);
      }
      if (isTop){
        dR_Top.emplace_back(dR);
        index_dR_Top.emplace_back(ii);
      }
    }

    //
    // return an RVec of indices sorted by the dR values
    //
    // RVec<int> dR_sorted_W_idx = CustomArgsort(dR_W, sort_from_lowest);
    // RVec<int> dR_sorted_Z_idx = CustomArgsort(dR_Z, sort_from_lowest);
    // RVec<int> dR_sorted_Higgs_idx = CustomArgsort(dR_Higgs, sort_from_lowest);
    // RVec<int> dR_sorted_Top_idx = CustomArgsort(dR_Top, sort_from_lowest);

    RVec<int> idx_sortedByDR_W     = Take(index_dR_W,     CustomArgsort(dR_W, sort_from_lowest));
    RVec<int> idx_sortedByDR_Z     = Take(index_dR_Z,     CustomArgsort(dR_Z, sort_from_lowest));
    RVec<int> idx_sortedByDR_Higgs = Take(index_dR_Higgs, CustomArgsort(dR_Higgs, sort_from_lowest));
    RVec<int> idx_sortedByDR_Top   = Take(index_dR_Top,   CustomArgsort(dR_Top, sort_from_lowest));

    //=========
    // W-boson
    //=========
    for (size_t iii = 0; iii < idx_sortedByDR_W.size(); iii++){
      int idxW = idx_sortedByDR_W[iii];
      //
      // Get immediate quark daughters of the W
      //
      for (size_t iv = 0; iv < GenPart_genPartIdxDaughter[idxW].size(); iv++){
        int dauIdx = GenPart_genPartIdxDaughter[idxW][iv];
        if (ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[dauIdx], FatJet_phi[i], GenPart_phi[dauIdx]) > 0.8) continue;
        //
        if (GenPart_isQuark[dauIdx]){
          if (iii == 0){
            if     (FlavourIdx_W0_q0[i] == -1){FlavourIdx_W0_q0[i] = dauIdx;}
            else if(FlavourIdx_W0_q1[i] == -1){FlavourIdx_W0_q1[i] = dauIdx;}
          }
          if (iii == 1){
            if     (FlavourIdx_W1_q0[i] == -1){FlavourIdx_W1_q0[i] = dauIdx;}
            else if(FlavourIdx_W1_q1[i] == -1){FlavourIdx_W1_q1[i] = dauIdx;}
          }
        }
        if (GenPart_isLepton[dauIdx]){
          if (iii == 0){
            if(FlavourIdx_W0_lep[i] == -1) {FlavourIdx_W0_lep[i] = dauIdx;}
          }
          if (iii == 1){
            if(FlavourIdx_W1_q0[i] == -1) {FlavourIdx_W1_q0[i] = dauIdx;}
          }
        }
      }
      if (iii == 1) break;
    }

    //=========
    // Z-boson
    //=========
    for (size_t iii = 0; iii < idx_sortedByDR_Z.size(); iii++){
      int idxZ = idx_sortedByDR_Z[iii];
      //
      // Get immediate quark daughters of the Z
      //
      for (size_t iv = 0; iv < GenPart_genPartIdxDaughter[idxZ].size(); iv++){
        int dauIdx = GenPart_genPartIdxDaughter[idxZ][iv];
        if (ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[dauIdx], FatJet_phi[i], GenPart_phi[dauIdx]) > 0.8) continue;
        //
        if (GenPart_isQuark[dauIdx]){
          if (iii == 0){
            if     (FlavourIdx_Z0_q0[i] == -1){FlavourIdx_Z0_q0[i] = dauIdx;}
            else if(FlavourIdx_Z0_q1[i] == -1){FlavourIdx_Z0_q1[i] = dauIdx;}
          }
          if (iii == 1){
            if     (FlavourIdx_Z1_q0[i] == -1){FlavourIdx_Z1_q0[i] = dauIdx;}
            else if(FlavourIdx_Z1_q1[i] == -1){FlavourIdx_Z1_q1[i] = dauIdx;}
          }
        }
        if (GenPart_isLepton[dauIdx]){
          if (iii == 0){
            if     (FlavourIdx_Z0_lep0[i] == -1){FlavourIdx_Z0_lep0[i] = dauIdx;}
            else if(FlavourIdx_Z0_lep1[i] == -1){FlavourIdx_Z0_lep1[i] = dauIdx;}
          }
          if (iii == 1){
            if     (FlavourIdx_Z1_lep0[i] == -1){FlavourIdx_Z1_lep0[i] = dauIdx;}
            else if(FlavourIdx_Z1_lep1[i] == -1){FlavourIdx_Z1_lep1[i] = dauIdx;}
          }
        }
        if (iii == 1) break;
      }
    }
    //=========
    // H-boson
    //=========
    for (size_t iii = 0; iii < idx_sortedByDR_Higgs.size(); iii++){
      int idxHiggs= idx_sortedByDR_Higgs[iii];
      //
      // Get immediate b-quark daughters of the Higgs
      //
      for (size_t iv = 0; iv < GenPart_genPartIdxDaughter[idxHiggs].size(); iv++){
        int dauIdx = GenPart_genPartIdxDaughter[idxHiggs][iv];
        if (ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[dauIdx], FatJet_phi[i], GenPart_phi[dauIdx]) > 0.8) continue;
        //
        if (GenPart_isBQuark[dauIdx]){
          if (iii == 0){
            if     (FlavourIdx_H0_bquark0[i] == -1){FlavourIdx_H0_bquark0[i] = dauIdx;}
            else if(FlavourIdx_H0_bquark1[i] == -1){FlavourIdx_H0_bquark1[i] = dauIdx;}
          }
          if (iii == 1){
            if     (FlavourIdx_H1_bquark0[i] == -1){FlavourIdx_H1_bquark0[i] = dauIdx;}
            else if(FlavourIdx_H1_bquark1[i] == -1){FlavourIdx_H1_bquark1[i] = dauIdx;}
          }
        }
      }
      if (iii == 1) break;
    }
    //=========
    // Top
    //=========
    RVec<int> index_WFromTop;

    for (size_t iii = 0; iii < idx_sortedByDR_Top.size(); iii++){
      int idxTop = idx_sortedByDR_Top[iii];
      //
      // Get immediate b-quark daughters of the Top
      //
      for (size_t iv = 0; iv < GenPart_genPartIdxDaughter[idxTop].size(); iv++){
        int dauIdx = GenPart_genPartIdxDaughter[idxTop][iv];
        //
        //
        //
        if (GenPart_isWBoson[dauIdx]){
          int idxLastCopyWBoson = getIdxLastCopy(dauIdx,GenPart_pdgId[dauIdx],GenPart_pdgId,GenPart_genPartIdxDaughter);
          index_WFromTop.emplace_back(idxLastCopyWBoson);
        }
        //
        //
        //
        if (ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[dauIdx], FatJet_phi[i], GenPart_phi[dauIdx]) > 0.8) continue;
        //
        if (GenPart_isBQuark[dauIdx]){
          if (iii == 0){
            if (FlavourIdx_Top0_bquark[i] == -1){FlavourIdx_Top0_bquark[i] = dauIdx;}
          }
          if (iii == 1){
            if (FlavourIdx_Top1_bquark[i] == -1){FlavourIdx_Top1_bquark[i] = dauIdx;}
          }
        }

      }
      if (iii == 1) break;
    }

    //=========
    // W from Top
    //=========
    for (size_t iii = 0; iii < index_WFromTop.size(); iii++){
      int idxWFromTop = index_WFromTop[iii];
      //
      // Get immediate quark daughters of the W
      //
      for (size_t iv = 0; iv < GenPart_genPartIdxDaughter[idxWFromTop].size(); iv++){
        int dauIdx = GenPart_genPartIdxDaughter[idxWFromTop][iv];
        if (ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[dauIdx], FatJet_phi[i], GenPart_phi[dauIdx]) > 0.8) continue;
        //
        if (GenPart_isQuark[dauIdx]){
          if (iii == 0){
            if      (FlavourIdx_WFromTop0_q0[i] == -1){FlavourIdx_WFromTop0_q0[i] = dauIdx;}
            else if (FlavourIdx_WFromTop0_q1[i] == -1){FlavourIdx_WFromTop0_q1[i] = dauIdx;}
          }
          if (iii == 1){
            if      (FlavourIdx_WFromTop1_q0[i] == -1){FlavourIdx_WFromTop1_q0[i] = dauIdx;}
            else if (FlavourIdx_WFromTop1_q1[i] == -1){FlavourIdx_WFromTop1_q1[i] = dauIdx;}
          }
        }
        if (GenPart_isLepton[dauIdx]){
          if (iii == 0){
            if(FlavourIdx_WFromTop0_lep[i] == -1) {FlavourIdx_WFromTop0_lep[i] = dauIdx;}
          }
          if (iii == 1){
            if(FlavourIdx_WFromTop1_lep[i] == -1) {FlavourIdx_WFromTop1_lep[i] = dauIdx;}
          }
        }
      }
      if (iii == 1) break;
    }

    //
    // W->qq
    //
    if      (FlavourIdx_W0_q0[i]!=-1 and FlavourIdx_W0_q1[i]!=-1) FlavourLabelW[i] = 1;
    else if (FlavourIdx_W1_q0[i]!=-1 and FlavourIdx_W1_q1[i]!=-1) FlavourLabelW[i] = 1;
    else    FlavourLabelW[i] = 0;

    //
    // Z->qq
    //
    if (FlavourIdx_Z0_q0[i]!=-1 and FlavourIdx_Z0_q1[i]!=-1) {
      FlavourLabelZ[i] = 1;
      // double-b
      if (GenPart_isBQuark[FlavourIdx_Z0_q0[i]] and GenPart_isBQuark[FlavourIdx_Z0_q1[i]]) FlavourLabelZbb[i] = 1;
      else FlavourLabelZbb[i] = 0;
      // double-c
      if (GenPart_isCQuark[FlavourIdx_Z0_q0[i]] and GenPart_isCQuark[FlavourIdx_Z0_q1[i]]) FlavourLabelZcc[i] = 1;
      else FlavourLabelZcc[i] = 0;
    }
    else if (FlavourIdx_Z1_q0[i]!=-1 and FlavourIdx_Z1_q1[i]!=-1) {
      FlavourLabelZ[i] = 1;
      // double-b
      if (GenPart_isBQuark[FlavourIdx_Z1_q0[i]] and GenPart_isBQuark[FlavourIdx_Z1_q1[i]]) FlavourLabelZbb[i] = 1;
      else FlavourLabelZbb[i] = 0;
      // double-c
      if (GenPart_isCQuark[FlavourIdx_Z1_q0[i]] and GenPart_isCQuark[FlavourIdx_Z1_q1[i]]) FlavourLabelZcc[i] = 1;
      else FlavourLabelZcc[i] = 0;
    }
    else FlavourLabelZ[i] = 0;

    //
    // H->bb
    //
    if      (FlavourIdx_H0_bquark0[i] != -1 and FlavourIdx_H0_bquark1[i] != -1) FlavourLabelHbb[i] = 1;
    else if (FlavourIdx_H1_bquark0[i] != -1 and FlavourIdx_H1_bquark1[i] != -1) FlavourLabelHbb[i] = 1;
    else    FlavourLabelHbb[i] = 0;

    //
    // Top quark
    //
    if (FlavourIdx_Top0_bquark[i] != -1 and FlavourIdx_WFromTop0_q0[i] != -1 and FlavourIdx_WFromTop0_q1[i] != -1) FlavourLabelTop[i] = 1;
    else if (FlavourIdx_Top1_bquark[i] != -1 and FlavourIdx_WFromTop1_q0[i] != -1 and FlavourIdx_WFromTop1_q1[i] != -1) FlavourLabelTop[i] = 1;
    else FlavourLabelTop[i] = 0;

    //
    // W from Top quark
    //
    if (FlavourIdx_Top0_bquark[i] == -1 and FlavourIdx_WFromTop0_q0[i] != -1 and FlavourIdx_WFromTop0_q1[i] != -1) FlavourLabelWFromTop[i] = 1;
    else if (FlavourIdx_Top1_bquark[i] == -1 and FlavourIdx_WFromTop1_q0[i] != -1 and FlavourIdx_WFromTop1_q1[i] != -1) FlavourLabelWFromTop[i] = 1;
    else FlavourLabelWFromTop[i] = 0;
  }

  FatJet_FlavourLabel_GenPartIndex[0]  = FlavourLabelW;
  FatJet_FlavourLabel_GenPartIndex[1]  = FlavourLabelZ;
  FatJet_FlavourLabel_GenPartIndex[2]  = FlavourLabelZbb;
  FatJet_FlavourLabel_GenPartIndex[3]  = FlavourLabelZcc;
  FatJet_FlavourLabel_GenPartIndex[4]  = FlavourLabelHbb;
  FatJet_FlavourLabel_GenPartIndex[5]  = FlavourLabelTop;
  FatJet_FlavourLabel_GenPartIndex[6]  = FlavourLabelWFromTop;
  FatJet_FlavourLabel_GenPartIndex[7]  = FlavourIdx_W0_q0;
  FatJet_FlavourLabel_GenPartIndex[8]  = FlavourIdx_W0_q1;
  FatJet_FlavourLabel_GenPartIndex[9]  = FlavourIdx_W0_lep;
  FatJet_FlavourLabel_GenPartIndex[10] = FlavourIdx_W1_q0;
  FatJet_FlavourLabel_GenPartIndex[11] = FlavourIdx_W1_q1;
  FatJet_FlavourLabel_GenPartIndex[12] = FlavourIdx_W1_lep;
  FatJet_FlavourLabel_GenPartIndex[13] = FlavourIdx_Z0_q0;
  FatJet_FlavourLabel_GenPartIndex[14] = FlavourIdx_Z0_q1;
  FatJet_FlavourLabel_GenPartIndex[15] = FlavourIdx_Z0_lep0;
  FatJet_FlavourLabel_GenPartIndex[16] = FlavourIdx_Z0_lep1;
  FatJet_FlavourLabel_GenPartIndex[17] = FlavourIdx_Z1_q0;
  FatJet_FlavourLabel_GenPartIndex[18] = FlavourIdx_Z1_q1;
  FatJet_FlavourLabel_GenPartIndex[19] = FlavourIdx_Z1_lep0;
  FatJet_FlavourLabel_GenPartIndex[20] = FlavourIdx_Z1_lep1;
  FatJet_FlavourLabel_GenPartIndex[21] = FlavourIdx_H0_bquark0;
  FatJet_FlavourLabel_GenPartIndex[22] = FlavourIdx_H0_bquark1;
  FatJet_FlavourLabel_GenPartIndex[23] = FlavourIdx_H1_bquark0;
  FatJet_FlavourLabel_GenPartIndex[24] = FlavourIdx_H1_bquark1;
  FatJet_FlavourLabel_GenPartIndex[25] = FlavourIdx_Top0_bquark;
  FatJet_FlavourLabel_GenPartIndex[26] = FlavourIdx_WFromTop0_q0;
  FatJet_FlavourLabel_GenPartIndex[27] = FlavourIdx_WFromTop0_q1;
  FatJet_FlavourLabel_GenPartIndex[28] = FlavourIdx_WFromTop0_lep;
  FatJet_FlavourLabel_GenPartIndex[29] = FlavourIdx_Top1_bquark;
  FatJet_FlavourLabel_GenPartIndex[30] = FlavourIdx_WFromTop1_q0;
  FatJet_FlavourLabel_GenPartIndex[31] = FlavourIdx_WFromTop1_q1;
  FatJet_FlavourLabel_GenPartIndex[32] = FlavourIdx_WFromTop1_lep;

  return FatJet_FlavourLabel_GenPartIndex;
}


#endif