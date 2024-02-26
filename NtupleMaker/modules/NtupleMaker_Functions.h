#ifndef NTUPLEMAKER_FUNCTIONS
#define NTUPLEMAKER_FUNCTIONS

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"
#include "TMath.h"
#include "utility"  // std::swap()

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
// Custom functions
//
//=========================================================
//
// Argsort with own Comparator function. ROOT has this in master branch
// but not in 6.22 and 6.24 so far. Reimplement here from:
// https://root.cern/doc/master/group__vecops.html#ga016d5ac674ce255c5f17088d068466d6
//
template <typename T, typename Compare>
RVec<typename RVec<T>::size_type> CustomArgsort(const RVec<T> &v, Compare &&c)
{
  using size_type = typename RVec<T>::size_type;
  RVec<size_type> i(v.size());
  std::iota(i.begin(), i.end(), 0);
  std::sort(i.begin(), i.end(), [&v, &c](size_type i1, size_type i2) { return c(v[i1], v[i2]); });
  return i;
}
//
//
//
bool sort_from_highest(float x, float y){
  return x > y;
}
bool sort_from_lowest(float x, float y){
  return x < y;
}
//
//
//
RVec<float> MSoftGen(
  rvec_f  GenJetAK8_eta, 
  rvec_f  GenJetAK8_phi,  
  rvec_f  SubGenJetAK8_pt, 
  rvec_f  SubGenJetAK8_eta, 
  rvec_f  SubGenJetAK8_phi,
  rvec_f  SubGenJetAK8_mass
){
  RVec<float> vec_msoft_gen(GenJetAK8_eta.size(), -1.f);
  
  bool subjet1_exist = false;
  bool subjet2_exist = false;

  ROOT::Math::PtEtaPhiMVector subjet1;
  ROOT::Math::PtEtaPhiMVector subjet2;

  for (size_t i = 0; i < GenJetAK8_eta.size(); i++)
  {
    subjet1_exist = false;
    subjet2_exist = false;

    subjet1 = ROOT::Math::PtEtaPhiMVector();
    subjet2 = ROOT::Math::PtEtaPhiMVector();

    for (size_t ii = 0; ii < SubGenJetAK8_pt.size(); ii++)
    { 
      if (ROOT::VecOps::DeltaR(GenJetAK8_eta[i], SubGenJetAK8_eta[ii], GenJetAK8_phi[i], SubGenJetAK8_phi[ii]) > 0.8) continue;
      if (!subjet1_exist and !subjet2_exist){
        subjet1 = ROOT::Math::PtEtaPhiMVector(SubGenJetAK8_pt[ii], SubGenJetAK8_eta[ii], SubGenJetAK8_phi[ii], SubGenJetAK8_mass[ii]);
        subjet1_exist = true;
      }
      else if (subjet1_exist and !subjet2_exist){
        subjet2 = ROOT::Math::PtEtaPhiMVector(SubGenJetAK8_pt[ii], SubGenJetAK8_eta[ii], SubGenJetAK8_phi[ii], SubGenJetAK8_mass[ii]);
        subjet2_exist = true;
      }
    }
    if (subjet1_exist and subjet2_exist){
      vec_msoft_gen[i] = (subjet1+subjet2).M();
    }
  }
  return vec_msoft_gen;
}
//
//
//
RVec<RVec<float>> MatchedGenJetAK8Kin(
  rvec_i  FatJet_genJetAK8Idx,
  rvec_f  GenJetAK8_pt, 
  rvec_f  GenJetAK8_eta, 
  rvec_f  GenJetAK8_phi, 
  rvec_f  GenJetAK8_mass, 
  rvec_f  GenJetAK8_msoftdrop
){
  RVec<RVec<float>> FatJet_MatchedGenJetAK8_Kin(5);
  RVec<float> vec_MatchedGenJetAK8_Pt(FatJet_genJetAK8Idx.size());
  RVec<float> vec_MatchedGenJetAK8_Eta(FatJet_genJetAK8Idx.size());
  RVec<float> vec_MatchedGenJetAK8_Phi(FatJet_genJetAK8Idx.size());
  RVec<float> vec_MatchedGenJetAK8_Mass(FatJet_genJetAK8Idx.size());
  RVec<float> vec_MatchedGenJetAK8_MSoftDrop(FatJet_genJetAK8Idx.size());

  for (size_t i = 0; i < FatJet_genJetAK8Idx.size(); i++)
  {
    const int& idx = FatJet_genJetAK8Idx[i];

    if(FatJet_genJetAK8Idx[i]>=0){
      vec_MatchedGenJetAK8_Pt[i] = GenJetAK8_pt[idx];
      vec_MatchedGenJetAK8_Eta[i] = GenJetAK8_eta[idx];
      vec_MatchedGenJetAK8_Phi[i] = GenJetAK8_phi[idx];
      vec_MatchedGenJetAK8_Mass[i] = GenJetAK8_mass[idx];
      vec_MatchedGenJetAK8_MSoftDrop[i] = GenJetAK8_msoftdrop[idx];
    }else{
      vec_MatchedGenJetAK8_Pt[i] = -1.f;
      vec_MatchedGenJetAK8_Eta[i] = -9.f;
      vec_MatchedGenJetAK8_Phi[i] = -9.f;
      vec_MatchedGenJetAK8_Mass[i] = -1.f;
      vec_MatchedGenJetAK8_MSoftDrop[i] = -1.f;
    }
  }

  FatJet_MatchedGenJetAK8_Kin[0] = vec_MatchedGenJetAK8_Pt;
  FatJet_MatchedGenJetAK8_Kin[1] = vec_MatchedGenJetAK8_Eta;
  FatJet_MatchedGenJetAK8_Kin[2] = vec_MatchedGenJetAK8_Phi;
  FatJet_MatchedGenJetAK8_Kin[3] = vec_MatchedGenJetAK8_Mass;
  FatJet_MatchedGenJetAK8_Kin[4] = vec_MatchedGenJetAK8_MSoftDrop;
  return FatJet_MatchedGenJetAK8_Kin;
}

RVec<float> MSoftRaw(
  rvec_i  FatJet_subJetIdx1,
  rvec_i  FatJet_subJetIdx2,
  rvec_f  SubJet_pt,
  rvec_f  SubJet_eta,
  rvec_f  SubJet_phi,
  rvec_f  SubJet_mass,
  rvec_f  SubJet_rawFactor
){
  RVec<float> vec_msoft_raw(FatJet_subJetIdx1.size());

  ROOT::Math::PtEtaPhiMVector subjet1_raw;
  ROOT::Math::PtEtaPhiMVector subjet2_raw;
  float msoft_raw = -1.f;

  for (size_t i = 0; i < FatJet_subJetIdx1.size(); i++)
  {
    const int& idx1 = FatJet_subJetIdx1[i];
    const int& idx2 = FatJet_subJetIdx2[i];

    msoft_raw = -1.f;
    if (idx1 >= 0 && idx2 >= 0){
      float sf1 = 1.f-SubJet_rawFactor[idx1];
      float sf2 = 1.f-SubJet_rawFactor[idx2];
      subjet1_raw = ROOT::Math::PtEtaPhiMVector(sf1*SubJet_pt[idx1], SubJet_eta[idx1], SubJet_phi[idx1], sf1*SubJet_mass[idx1]);
      subjet2_raw = ROOT::Math::PtEtaPhiMVector(sf2*SubJet_pt[idx2], SubJet_eta[idx2], SubJet_phi[idx2], sf2*SubJet_mass[idx2]);
      msoft_raw = (subjet1_raw+subjet2_raw).M();
    }
    vec_msoft_raw[i] = msoft_raw;
  }
  return vec_msoft_raw;
}
RVec<float> MSoftAK8JEC(
  rvec_i  FatJet_subJetIdx1,
  rvec_i  FatJet_subJetIdx2,
  rvec_f  FatJet_corr_JEC,
  rvec_f  SubJet_pt,
  rvec_f  SubJet_eta,
  rvec_f  SubJet_phi,
  rvec_f  SubJet_mass,
  rvec_f  SubJet_rawFactor
){
  RVec<float> vec_msoft_corr(FatJet_subJetIdx1.size());

  ROOT::Math::PtEtaPhiMVector subjet1_raw;
  ROOT::Math::PtEtaPhiMVector subjet2_raw;
  ROOT::Math::PtEtaPhiMVector subjet12_corr;

  float msoft_corr = -1.f;

  for (size_t i = 0; i < FatJet_subJetIdx1.size(); i++)
  {
    const int& idx1 = FatJet_subJetIdx1[i];
    const int& idx2 = FatJet_subJetIdx2[i];

    msoft_corr = -1.f;
    if (idx1 >= 0 && idx2 >= 0){
      float sf1 = 1.f-SubJet_rawFactor[idx1];
      float sf2 = 1.f-SubJet_rawFactor[idx2];
      subjet1_raw = ROOT::Math::PtEtaPhiMVector(sf1*SubJet_pt[idx1], SubJet_eta[idx1], SubJet_phi[idx1], sf1*SubJet_mass[idx1]);
      subjet2_raw = ROOT::Math::PtEtaPhiMVector(sf2*SubJet_pt[idx2], SubJet_eta[idx2], SubJet_phi[idx2], sf2*SubJet_mass[idx2]);
      subjet12_corr = FatJet_corr_JEC[i] * (subjet1_raw+subjet2_raw);
      msoft_corr = subjet12_corr.M();
    }
    vec_msoft_corr[i] = msoft_corr;
  }
  return vec_msoft_corr;
}
// NOTE: This does not work when use in Define. Why?
// auto sort_from_highest = [](float x, float y) {return x > y;};
//
//=========================================================
//
//
//
//
//=========================================================
float CalcEventWeightForAK8Tag_PassFail(
  rvec_f  vec_eff,
  rvec_f  vec_sf,
  rvec_i  vec_pass
){
  float weight_pass = 1.f;
  float weight_fail = 1.f;

  for (size_t i = 0; i < vec_pass.size(); i++)
  {
    if (vec_pass[i]){
      // P(Data) / P(MC) = (SF*eff) / eff
      weight_pass *= (vec_sf[i] * vec_eff[i]) / vec_eff[i];
    }
    else{
      // P(Data) / P(MC) = (1 - SF*eff) / (1-eff)
      weight_fail *= (1.f-(vec_sf[i] * vec_eff[i])) / (1.f-vec_eff[i]);
    }
  }
  return weight_pass * weight_fail;
}

float CalcEventWeightForAK8Tag_HPLPNP(
  rvec_f  vec_eff_tight,
  rvec_f  vec_eff_loose,
  rvec_f  vec_sf_tight,
  rvec_f  vec_sf_loose,
  rvec_i  vec_pass_HP,
  rvec_i  vec_pass_LP
){
  float weight_HP = 1.f;
  float weight_LP = 1.f;
  float weight_NP = 1.f;

  for (size_t i = 0; i < vec_pass_LP.size(); i++)
  {
    if (vec_pass_HP[i]){
      weight_HP *= (vec_sf_tight[i] * vec_eff_tight[i]) / vec_eff_tight[i];
    }
    else if(vec_pass_LP[i]){
      weight_LP *= ((vec_sf_loose[i] * vec_eff_loose[i]) - (vec_sf_tight[i] * vec_eff_tight[i]))
                   / (vec_eff_loose[i] - vec_eff_tight[i]);
    }
    else{
      weight_NP *= (1.f - (vec_sf_loose[i] * vec_eff_loose[i]))
                   / (1.f - vec_eff_loose[i]);
    }
  }
  return weight_HP * weight_LP * weight_NP;
}

//=========================================================
//
//
//
//
//=========================================================
struct TrigObjInfo{
  float pt = -1.f;
  float eta = -9.f;
  float phi = -9.f;
  int   id;
  int   filterBits;
  FourVector p4;
  TrigObjInfo() = default;
  TrigObjInfo(float pt_,float eta_,float phi_,int id_, int filterBits_){
    pt = pt_; eta = eta_; phi = phi_;
    id = id_; filterBits = filterBits_;
    p4 = FourVector(pt,eta,phi,0.);
  };
};

//=========================================================
//
//
//
//
//=========================================================
template < typename T, int idxMin = -1>
T GetFromVec(const RVec<T>& vec,  int idxObj,  T dummyValue){
  if (idxObj > idxMin and not (vec.empty()))
    return vec[idxObj];
  else
    return dummyValue;
  // return (idxObj > idxMin and (not vec.empty())) ? vec[idxObj] : dummyValue;
}

template < typename T, int idxMin = -1>
RVec<T> GetFromAnotherCollection(const RVec<int>& vecMatchIdx, const RVec<T>& vecTargetColl, T dummyValue){
  RVec<T> rvec_match(vecMatchIdx.size(), dummyValue);
  for (size_t i = 0; i < vecMatchIdx.size(); i++) {
    if (vecMatchIdx[i] > idxMin and not (vecTargetColl.empty()) and (vecMatchIdx[i] < vecTargetColl.size()))
      rvec_match[i] = vecTargetColl[vecMatchIdx[i]];
  }
  return rvec_match;
}
RVec<int> IsOverlap(const RVec<FourVector>& objs, const FourVector& ref, float max=0.8){
  RVec<int> rvec_overlap(objs.size());
  for (size_t i = 0; i < objs.size(); i++) {
    rvec_overlap[i] = VectorUtil::DeltaR(objs[i],ref) < max;
  }
  return rvec_overlap;
}
RVec<float> GetPtFromVecP4(const RVec<FourVector>& vecP4){
  RVec<float> rvec_pt(vecP4.size());
  for (size_t i = 0; i < vecP4.size(); i++) {
    rvec_pt[i] = vecP4[i].Pt();
  }
  return rvec_pt;
}
RVec<float> GetEtaFromVecP4(const RVec<FourVector>& vecP4){
  RVec<float> rvec_eta(vecP4.size());
  for (size_t i = 0; i < vecP4.size(); i++) {
    rvec_eta[i] = vecP4[i].Eta();
  }
  return rvec_eta;
}
RVec<float> GetPhiFromVecP4(const RVec<FourVector>& vecP4){
  RVec<float> rvec_phi(vecP4.size());
  for (size_t i = 0; i < vecP4.size(); i++) {
    rvec_phi[i] = vecP4[i].Phi();
  }
  return rvec_phi;
}
RVec<float> GetMassFromVecP4(const RVec<FourVector>& vecP4){
  RVec<float> rvec_mass(vecP4.size());
  for (size_t i = 0; i < vecP4.size(); i++) {
    rvec_mass[i] = vecP4[i].M();
  }
  return rvec_mass;
}

RVec<float> GeDeltaRFromTwoVecsOfP4(const RVec<FourVector>& vecP4A,const RVec<FourVector>& vecP4B){
  RVec<float> rvec_deltaR(vecP4A.size());
  for (size_t i = 0; i < vecP4A.size(); i++) {
    rvec_deltaR[i] = VectorUtil::DeltaR(vecP4A[i], vecP4B[i]);
  }
  return rvec_deltaR;
}

RVec<float> GeDeltaEtaFromTwoVecsOfP4(const RVec<FourVector>& vecP4A,const RVec<FourVector>& vecP4B){
  RVec<float> rvec_deltaEta(vecP4A.size());
  for (size_t i = 0; i < vecP4A.size(); i++) {
    rvec_deltaEta[i] = vecP4A[i].Eta() - vecP4B[i].Eta();
  }
  return rvec_deltaEta;
}

RVec<FourVector> GeP4SumFromTwoVecsOfP4(const RVec<FourVector>& vecP4A,const RVec<FourVector>& vecP4B){
  RVec<FourVector> rvec_P4Sum(vecP4A.size());
  for (size_t i = 0; i < vecP4A.size(); i++) {
    rvec_P4Sum[i] = vecP4A[i] + vecP4B[i];
  }
  return rvec_P4Sum;
}

// GetKinFromVecP4(vecP4, &FourVector::Pt);
// GetKinFromVecP4(vecP4, &FourVector::Eta);
// GetKinFromVecP4(vecP4, &FourVector::Phi);
RVec<float> GetKinFromVecP4(const RVec<FourVector>& vecP4, double (FourVector::*fp)() const){
  RVec<float> rvec_kin(vecP4.size());
  for (size_t i = 0; i < vecP4.size(); i++) {
    rvec_kin[i] = float(((&vecP4[i])->*fp)());
  }
  return rvec_kin;
}

// GetKinFromP4(p4, &FourVector::Pt);
// GetKinFromP4(p4, &FourVector::Eta);
// GetKinFromP4(p4, &FourVector::Phi);
float GetKinFromP4(FourVector* p4, double (FourVector::*fp)() const){
  return float((p4->*fp)());
}

int GetIdxFromVecIdx(rvec_ul vecIdx,  int idx)
{ 
  if (int(vecIdx.size()) >= idx+1) // Get idx-th 
    return vecIdx[idx];
  else 
    return -1;
}
auto DummySFAndSyst(const RVec<FourVector>& vecP4, const float sf){
  return Map(vecP4,[&sf](const FourVector& v){return RVec<float>({sf,sf,sf});});
}
//
// RVec<float> IfPassFill(int condition, float value, float dummy = -9.){
//   if(condition){
//     return value;
//   }else{
//     return dummy;
//   }
//   return -8.;
// }
//=========================================================
//
// Trigger
//
//=========================================================
// RVec<TrigObjInfo> MakeRVecTrigObjInfo(rvec_f pt,rvec_f eta,rvec_f phi,rvec_i id, rvec_i filterBits)
// {
//   RVec<TrigObjInfo> rvec_trigObjInfo(pt.size());
//   for (size_t i = 0; i < pt.size(); i++) {
//     rvec_trigObjInfo[i] = TrigObjInfo(pt[i],eta[i],phi[i],id[i],filterBits[i]);
//     rvec_trigObjInfo[i].idxInNano =  int(i);
//   }
//   return rvec_trigObjInfo;
// }
template<int trigObjID>
RVec<RVec<int>> MatchTrigObj(const RVec<FourVector>& objs, const RVec<TrigObjInfo>& trigObjs, float max=0.15)
{
  RVec<RVec<int>> rvec_rvec_idxs(objs.size());
  for (size_t i = 0; i < objs.size(); i++) {
    RVec<int> rvec_idxs;
    for (size_t ii = 0; ii < trigObjs.size(); ii++) {
      if (trigObjs[ii].id != trigObjID) continue;
      if (VectorUtil::DeltaR(objs[i],trigObjs[ii].p4) >= max) continue;
      rvec_idxs.emplace_back(ii);
    }
    rvec_rvec_idxs[i] = rvec_idxs;
  }
  return rvec_rvec_idxs;
}
//=========================================================
//
//
//
//
//=========================================================
template<int bitValue>
RVec<int> PassPUID(rvec_f pt,rvec_i puIdBit){
  RVec<int> rvec_puIdPass(pt.size());
  for (size_t i = 0; i < pt.size(); i++) {
    rvec_puIdPass[i] = pt[i] > 50.f ? true : puIdBit[i]&(1<<bitValue);
  }
  return rvec_puIdPass;
}


#endif

