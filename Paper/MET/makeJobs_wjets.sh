 #!/bin/bash

allsyst=(Nominal JESUp JESDown JERUp JERDown UnclusteredUp UnclusteredDown)
#allsyst=(Nominal JESUp JESDown UnclusteredUp UnclusteredDown)
#allsyst=(JESUp JESDown JERUp JERDown UnclusteredUp UnclusteredDown)
#allsyst=(JERUp JERDown)

#years=(2016postVFP)
#years=(2017)
samples=(data qcd qcdpt dy top ew ewk ewknlo ewkincl ewkincl61 ewknlo61)
samples=(data qcd dy top ew ewk ewknlo ewkincl ewkincl61 ewknlo61)
samples=(data qcd dy top ew ewk ewknlo61 ewkincl)
#samples=(ewkincl ewk )
channels=(MuMu ElEl)
#2016postVFP MET_T1_pt 0 datatop MuMu
years=(2016BpreVFP 2016CpreVFP 2016DpreVFP 2016EpreVFP 2016FpreVFP)
#years=(2016preVFP 2016postVFP)
years=(2016preVFP 2016postVFP 2017 2018)
years=(2016preVFP 2016postVFP 2017 2018)
#years=(2017)



vars=(METCorGood_T1_pt PuppiMETCorGood_pt  PuppiMET_pt MET_T1_pt  METCorGood_T1_phi PuppiMETCorGood_phi  PuppiMET_pt MET_T1_phi)
vars=(METWTmass PuppiMETWTmass Puppiboson_pt  Puppiboson_phi RawMET_pt RawMET_phi METCorGoodWTmass   PuppiMETCorGoodWTmass)
vars=(RawPuppiMET_pt RawPuppiMET_phi RawMET_pt RawMET_phi)
vars=(MET_T1_pt PuppiMET_pt MET_T1_phi  PuppiMET_phi)
vars=(METWTmass PuppiMETWTmass Puppiboson_pt  Puppiboson_phi METCorGoodWTmass PuppiMETCorGoodWTmass)
vars=(METCorGood_T1_pt PuppiMETCorGood_pt  PuppiMET_pt MET_T1_pt RawMET_pt RawPuppiMET_pt)
vars=(boson_pt  boson_phi Puppiboson_pt  Puppiboson_phi)
vars=(METCorGood_T1_pt PuppiMETCorGood_pt  PuppiMET_pt MET_T1_pt  METCorGood_T1_phi PuppiMETCorGood_phi  PuppiMET_pt MET_T1_phi boson_pt  boson_phi Puppiboson_pt  Puppiboson_phi RawPuppiMET_pt RawPuppiMET_phi RawMET_pt RawMET_phi METWTmass PuppiMETWTmass METCorGoodWTmass PuppiMETCorGoodWTmass)
vars=(METCorGood_T1_phi METCorGood_T1_pt MET_T1_phi PuppiMETCorGood_phi  PuppiMETCorGood_pt)
#vars=(RawMET_pt RawPuppiMET_pt METCorGood_T1_pt MET_T1_pt PuppiMET_pt  PuppiMETCorGood_pt)
vars=( METCorGood_T1_pt MET_T1_pt PuppiMET_pt  PuppiMETCorGood_pt)
dosend="1"
moremem="0"

# jets >=0 or >0 , bTag L or T, metwmass 0 or 80, vetoall, vetophoton
njetcuts=(njetsgeq0_ njetsgt0_)

vetocuts=(noveto_ vetoall_ vetophoton_)

masses=(massgt0_ massgt80_)
njetcuts=(njetsgt0_ njetsgeq0_)
vetocuts=(noveto_ vetophoton_)
btags=(nbtagl_ btagt_)

masses=(massgt0_ massgt80_)
njetcuts=(njetsgeq0_ njetsgt0_)
btags=(nbtagl_ )
vetocuts=(noveto_ )
vetocuts=(noveto_10bins_)

veto="1"

for nj in ${njetcuts[@]}; do
for iv in ${vetocuts[@]}; do

for im in ${masses[@]}; do

for ib in ${btags[@]}; do
jetcut=${nj}${im}${ib}${iv}

#for jetcut in ${alljetcuts[@]}; do
for sy in ${allsyst[@]}; do
  dosend="1"
  for yr in ${years[@]}; do
  
    dosend="1"
    for ss in ${samples[@]}; do
    # if [[ $ss == "data" ]] && [[ $sy != "Nominal" ]] ; then
    # dosend="0"
    #fi
    
    #if [[ $ss == "ewk" ]]  && [[ $yr == "2016postVFP" ]] ; then
    #if [[ $ss == "ewk" || $ss == "top" ]] ; then
    if [[ $ss == "top" ]] ; then
    moremem="1"
    fi
        ss=${ss}_${jetcut}hitslt${veto}
        for ch in ${channels[@]}; do
        
          for vr in ${vars[@]}; do

      #echo $sy, $yr, $ss


  if [[ $sy == "Nominal" ]] ; then sy=""
  fi
  cp job_template Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  #echo job_template Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  echo python met_distribution_single.py -y $yr -v $vr$sy -q 0 -e ${ss} -c $ch -l no >> Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  cp jdl_template Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl

#echo $ss , $yr
if [[ $moremem == "1" ]]  ; then
  #echo "will modify memory"

  sed  -i '1 i request_memory = 4200' Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
fi
  yrr=${yr}
  if [[ "$yrr" == *"preVFP"*  ]] ; then
  yrr="2016preVFP"
  fi
 
  sed -i 's/EXECHERE/jobb_'${yr}'_'${vr}''${sy}'_'${ss}'_'${ch}'.sh/g' Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
  sed -i 's/YEARHERE/'${yrr}'/g' Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
  echo "cp plotS*root ../../." >> Jobs/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh

  #fi
  #plotS_2016postVFP_ewk_MET_T1_ptUnclusteredUp_MuMu.root
  #if [[ ! -f Jobs/plotS_${yr}_${ss}_${vr}${sy}_${ch}.root ]] ; then
  #echo do send  Jobs/plotS_${yr}_${ss}_${vr}${sy}_${ch}.root 
  #cd Jobs;   condor_submit jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl; cd ..
  #fi

        done
      done
    done
  done
done
done
done
done
done

rm Jobs/*Up*data* Jobs/*Down*data*
rm Jobs/*Raw*Up* Jobs/*Raw*Down*

for nj in ${njetcuts[@]}; do
for iv in ${vetocuts[@]}; do

for im in ${masses[@]}; do

for ib in ${btags[@]}; do
jetcut=${nj}${im}${ib}${iv}

#for jetcut in ${alljetcuts[@]}; do

for sy in ${allsyst[@]}; do

  for yr in ${years[@]}; do
  
    for ss in ${samples[@]}; do

    
        ss=${ss}_${jetcut}hitslt${veto}
        for ch in ${channels[@]}; do
        
          for var in ${vars[@]}; do

      #echo $sy, $yr, $ss

  
  if [[ $sy == "Nominal" ]] ; then sy=""
  fi

  if [[ ! -f Jobs/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
  #if [[ ! -f Jobs/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
  #do
  echo this is not there... Jobs/plotS_${yr}_${ss}_${var}${sy}${ch}.root 
  #echo send   Jobs/plotS_${yr}_${ss}_${var}${sy}_${ch}.root
  cd Jobs;   
  condor_submit jobb_${yr}_${var}${sy}_${ss}_${ch}.jdl; cd ..
  fi

        done
      done
    done
  done
done
done
done
done
done
