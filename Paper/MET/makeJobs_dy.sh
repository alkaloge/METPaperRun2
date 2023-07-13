 #!/bin/bash

allsyst=(Nominal JESUp JESDown JERUp JERDown UnclusteredUp UnclusteredDown)
#allsyst=(Nominal JESUp JESDown UnclusteredUp UnclusteredDown)
#allsyst=(JESUp JESDown JERUp JERDown)
allsyst=(Nominal)

samples=(data qcd dy dynlo top ewk ewknlo ew)
samples=(data dy top ew)
samples=(data dy dynlo top ew)
#samples=(data)
channels=(MuMu ElEl)
#2016postVFP MET_T1_pt 0 datatop MuMu
years=(2016BpreVFP 2016CpreVFP 2016DpreVFP 2016EpreVFP 2016FpreVFP)
years=(2016preVFP 2017 2018) 
years=(2016preVFP 2016postVFP 2017 2018)
#years=(2016preVFP 2016postVFP)
years=(2018)
extra=''
vars=(MET_T1_pt PuppiMET_pt boson_pt)
vars=(METWmass u_par_MET u_perp_MET PuppiMETWmass)

vars=(METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi )
vars=(njets METWTmass PuppiMETWTmass METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi MET_T1_pt PuppiMET_pt MET_T1_phi PuppiMET_phi Puppiboson_pt boson_pt METWmass PuppiMETWmass jpt jeta)
vars=(njets METWTmass PuppiMETWTmass METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi MET_T1_pt PuppiMET_pt MET_T1_phi PuppiMET_phi Puppiboson_pt boson_pt METWmass PuppiMETWmass jpt jeta)

vars=(MET_T1_pt METCorGood_T1_pt METCor_T1_phi METCorGood_T1_pt PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi zll boson_pt boson_phi)

#vars=(njets METCorGood_T1_pt METCorGood_T1_phi PuppiMETCorGood_pt PuppiMETCorGood_phi mll boson_pt boson_phi nbtagL nbtagM nbtagT u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET)
vars=(njets METCorGood_T1_pt METCorGood_T1_pt PuppiMETCorGood_pt PuppiMETCorGood_phi mll boson_pt boson_phi u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET)
vars=( METCorGood_T1_pt METCorGood_T1_phi PuppiMETCorGood_pt PuppiMETCorGood_phi mll boson_pt boson_phi u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET)
vars=(METCorGood_T1_pt PuppiMETCorGood_T1_pt)
vars=(mll METCorGood_T1_pt PuppiMETCorGood_T1_pt )

vars=( mll METCorGood_T1_pt METCorGood_T1_phi PuppiMETCorGood_pt PuppiMETCorGood_phi boson_pt boson_phi u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET MET_pt PuppiMET_pt RawMET_pt RawPuppiMET_pt   PuppiMET_phi RawPuppiMET_phi MET_phi RawMET_phi)
#vars=(METCorGood_T1_pt PuppiMETCorGood_pt MET_pt PuppiMET_pt RawMET_pt RawPuppiMET_pt METCorGood_phi MET_phi RawMET_phi PuppiMETCorGood_phi  PuppiMET_phi RawPuppiMET_phi )
vars=( mll METCorGood_T1_phi PuppiMETCorGood_phi boson_pt boson_phi u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET PuppiMET_phi RawPuppiMET_phi  RawMET_phi MET_T1_phi)
#vars=(METCorGood_T1_pt PuppiMETCorGood_pt MET_T1_pt PuppiMET_pt RawMET_pt RawPuppiMET_pt) 
#vars=(METCorGood_T1_phi PuppiMETCorGood_phi METCorGood_T1Smear_phi RawMET_phi RawPuppiMET_phi)
vars=(mll)
vars=(u_par_MET_T1 u_par_METCorGood_T1 u_par_METCorGood_T1Smear u_par_PuppiMET  u_par_PuppiMETCorGood u_par_RawMET u_par_RawPuppiMET)
vars=(u_perp_MET_T1 u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMET  u_perp_PuppiMETCorGood u_perp_RawMET u_perp_RawPuppiMET)
vars=(MET_T1_pt Puppi_pt MET_T1_phi Puppi_phi)
vars=(u_par_MET_T1 u_par_METCorGood_T1 u_par_METCorGood_T1Smear u_par_PuppiMET  u_par_PuppiMETCorGood u_par_RawMET u_par_RawPuppiMET)
vars=(u_perp_MET_T1 u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMET  u_perp_PuppiMETCorGood u_perp_RawMET u_perp_RawPuppiMET)
#vars=(u_par_METCorGood_T1 u_perp_METCorGood_T1)
#vars=(u_par_MET_T1 u_par_METCorGood_T1 u_par_METCorGood_T1Smear u_par_PuppiMET  u_par_PuppiMETCorGood u_par_RawMET u_par_RawPuppiMET)
vars=(METCorGood_T1_pt PuppiMETCorGood_pt METCorGood_T1Smear_pt RawMET_pt RawPuppiMET_pt )
#vars=(u_parboson_METCorGood_T1 u_parresp_METCorGood_T1 u_perp_METCorGood_T1 )
vars=(u_perp_MET_T1 u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMET  u_perp_PuppiMETCorGood u_perp_RawMET u_perp_RawPuppiMET)
vars=(u_parboson_MET_T1 u_parboson_METCorGood_T1 u_parboson_METCorGood_T1Smear u_parboson_PuppiMET  u_parboson_PuppiMETCorGood u_parboson_RawMET u_parboson_RawPuppiMET)
vars=(mll boson_pt boson_phi u_perp_MET_T1 u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMET  u_perp_PuppiMETCorGood u_perp_RawMET u_perp_RawPuppiMET u_parboson_MET_T1 u_parboson_METCorGood_T1 u_parboson_METCorGood_T1Smear u_parboson_PuppiMET  u_parboson_PuppiMETCorGood u_parboson_RawMET u_parboson_RawPuppiMET)
#vars=( u_perp_MET_T1 u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMET  u_perp_PuppiMETCorGood u_perp_RawMET u_perp_RawPuppiMET u_parboson_MET_T1 u_parboson_METCorGood_T1 u_parboson_METCorGood_T1Smear u_parboson_PuppiMET  u_parboson_PuppiMETCorGood u_parboson_RawMET u_parboson_RawPuppiMET)
vars=( u_perp_METCorGood_T1 u_perp_METCorGood_T1Smear u_perp_PuppiMETCorGood u_parboson_METCorGood_T1 u_parboson_METCorGood_T1Smear u_parboson_PuppiMETCorGood)
#vars=(PuppiMETCorGood_pt METCorGood_T1_pt METCorGood_T1Smear_pt)
dosend="1"
moremem="0"
#jetcut="njetsgt0"  
jetcut="njetsgeq0"  
#btag="nbtagl_10bins"
btag="nbtagl"
veto="1"

for sy in ${allsyst[@]}; do
  dosend="1"
  for yr in ${years[@]}; do
  
    dosend="1"
    for ss in ${samples[@]}; do
    # if [[ $ss == "data" ]] && [[ $sy != "Nominal" ]] ; then
    # dosend="0"
    #fi
    
    if [[ $ss == "ewk" ]]  && [[ $yr == "2016postVFP" ]] ; then
    moremem="1"
    fi
        ss=${ss}_${jetcut}_${btag}_hitslt${veto}${extra}
        for ch in ${channels[@]}; do
        
          for vr in ${vars[@]}; do



  if [[ $sy == "Nominal" ]] ; then sy=""
  fi
  cp job_template Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  #echo job_template Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  echo python dy_met_distribution.py -y $yr -v $vr$sy -q 0 -e ${ss} -c $ch -l no >> Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
  cp jdl_template Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl

#echo $ss , $yr
#if [[ $moremem == "1" ]]  ; then
#  #echo "will modify memory"

#  sed  -i '1 i request_memory = 4200' Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
#fi
  yrr=${yr}
  if [[ "$yrr" == *"preVFP"*  ]] ; then
  yrr="2016preVFP"
  fi
 
  sed -i 's/EXECHERE/jobb_'${yr}'_'${vr}''${sy}'_'${ss}'_'${ch}'.sh/g' Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
  sed -i 's/YEARHERE/'${yrr}'/g' Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
  echo "cp plotS*root ../../." >> Jobs_dy/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh

  #fi
  #plotS_2016postVFP_ewk_MET_T1_ptUnclusteredUp_MuMu.root
  #if [[ ! -f Jobs_dy/plotS_${yr}_${ss}_${vr}${sy}_${ch}.root ]] ; then
  #echo do send  Jobs_dy/plotS_${yr}_${ss}_${vr}${sy}_${ch}.root 
  #cd Jobs_dy;   condor_submit jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl; cd ..
  #fi

        done
      done
    done
  done
done

rm Jobs_dy/*Up*data* Jobs_dy/*Down*data*
rm Jobs_dy/*Raw*Up Jobs_dy/*Raw*Down*

for sy in ${allsyst[@]}; do

  for yr in ${years[@]}; do
  
    for ss in ${samples[@]}; do

    
        ss=${ss}_${jetcut}_${btag}_hitslt${veto}${extra}
        for ch in ${channels[@]}; do
        
          for var in ${vars[@]}; do

      #echo $sy, $yr, $ss

  
  if [[ $sy == "Nominal" ]] ; then sy=""
  fi
  #plotS_2018_ew_njetsgt0_hitslt2_MET_T1_pt_MuMu.root
  #plotS_2016preVFP_ewk_njetsgt0_hitslt2_PuppiMETWmassJESUp_ElEl.root

  #Jobs_dy/plotS_2016postVFP_ewk_njetsgt0_hitslt2_METWmassUnclusteredDown_MuMu.root
  # Jobs_dy/jobb_2016postVFP_METWmassUnclusteredDown_ewk_njetsgt0_hitslt2_ElEl.sh
  #plotS_2017_ew_njetsgt0_hitslt2_PuppiMETCorGood_ptJERUp_MuMu.root
  if [[ ! -f Jobs_dy/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
  #if [[ ! -f Jobs_dy/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
  #do
  echo this is not there... Jobs_dy/plotS_${yr}_${ss}_${var}${sy}${ch}.root 
  #echo send   Jobs_dy/plotS_${yr}_${ss}_${var}${sy}_${ch}.root
  cd Jobs_dy;   
  condor_submit jobb_${yr}_${var}${sy}_${ss}_${ch}.jdl; cd ..
  else echo Jobs_dy/plotS_${yr}_${ss}_${var}${sy}_${ch}.root
  fi 
        done
      done
    done
  done
done
