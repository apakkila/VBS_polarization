
# SAMPLELIST=(
# # VBS_madspin_WW_SS_4f
# # VBS_madspin_WW_SS_4f_mmjj150_ptW150
# # VBS_madspin_WW_SS_4f_mmjj150_ptW250
# # VBS_madspin_WW_SS_4f_mmjj150
# # VBS_madspin_WW_SS_LL_4f_mmjj150
# # VBS_madspin_WW_SS_LT_4f_mmjj150
# # VBS_madspin_WW_SS_TT_4f_mmjj150
# )

SAMPLELIST=(
WPJJWMJJjj_EWK_LO_4f_mmjj150
# WPMJJWPMJJjj_EWK_LO_4f_mmjj150
# ZJJWPMJJjj_EWK_LO_4f_mmjj150
# ZJJZJJjj_EWK_LO_4f_mmjj150
#ZNuNuWPMJJjj_EWK_LO_4f_mmjj150
#ZNuNuZJJjj_EWK_LO_4f_mmjj150
# WPJJWMJJjj_QCD_LO_4f_mmjj150
# WPMJJWPMJJjj_QCD_LO_4f_mmjj150
# ZJJWPMJJjj_QCD_LO_4f_mmjj150
# ZJJZJJjj_QCD_LO_4f_mmjj150
# ZNuNuWPMJJjj_QCD_LO_4f_mmjj150
# ZNuNuZJJjj_QCD_LO_4f_mmjj150
)

NFILES=1

for SAMPLE in ${SAMPLELIST[@]};
do
  echo -e "\n\n"
  echo $SAMPLE
  python3 -u ProcessNano.py --sample $SAMPLE --nfiles $NFILES
done
