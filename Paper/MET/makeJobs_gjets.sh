 #!/bin/bash

allsyst=(Nominal JESUp JESDown JERUp JERDown UnclusteredUp UnclusteredDown)
#allsyst=(JESUp JESDown JERUp JERDown UnclusteredUp UnclusteredDown)
allsyst=(Nominal)

samples=(data gjets tx ew qcd ewknlo)
channels=(Gjets)

years=(2016BpreVFP 2016CpreVFP 2016DpreVFP 2016EpreVFP 2016FpreVFP)
years=(2016preVFP 2017 2018) 
years=(2016preVFP 2016postVFP 2017 2018)
years=(2017 2018)
years=(2016preVFP 2016postVFP)
#Bv1_preVFP Bv2_preVFP C_preVFP D_preVFP E_preVFP Fv2_preVFP Fv1 G H
years=(2017 2018 2016preVFP 2016postVFP)
years=(2017  2016preVFP 2016postVFP 2018)
years=(2017  2016 2018)
years=(2016postVFP 2016preVFP)
years=(2016postVFP 2016preVFP 2017 2018)
years=(2016postVFP 2016preVFP 2018 2017)
#years=(2018)
extra=''
vars=(MET_T1_pt PuppiMET_pt boson_pt)
vars=(METWmass u_par_MET u_perp_MET PuppiMETWmass)
vars=(MET_T1_pt PuppiMET_pt boson_pt METWmass u_par_MET u_perp_MET PuppiMETWmass)


vars=(METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi )
vars=(njets METWTmass PuppiMETWTmass METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi MET_T1_pt PuppiMET_pt MET_T1_phi PuppiMET_phi Puppiboson_pt boson_pt METWmass PuppiMETWmass jpt jeta)
vars=(njets METWTmass PuppiMETWTmass METCor_T1_pt METCor_T1_phi METCorGood_T1_pt METCorGood_T1_phi PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi MET_T1_pt PuppiMET_pt MET_T1_phi PuppiMET_phi Puppiboson_pt boson_pt METWmass PuppiMETWmass jpt jeta)

#vars=(METCor_T1_phi METCorGood_T1_phi PuppiMETCor_phi PuppiMETCorGood_phi  MET_T1_phi PuppiMET_phi jpt jeta )
vars=(MET_T1_pt METCorGood_T1_pt METCor_T1_phi METCorGood_T1_pt PuppiMETCor_pt PuppiMETCor_phi PuppiMETCorGood_pt PuppiMETCorGood_phi zll boson_pt boson_phi)

vars=(njets METCorGood_T1_pt METCorGood_T1_pt PuppiMETCorGood_pt PuppiMETCorGood_phi mll boson_pt boson_phi nbtagL nbtagM nbtagT u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET)

vars=(METCorGood_T1_pt  METCorGood_T1_phi PuppiMETCorGood_pt PuppiMETCorGood_phi boson_pt boson_phi)
vars=(METCorGood_T1_pt iso_1 Photon_r9_1 iso_1 njets boson_pt PuppiMETCorGood_pt PuppiMETCor_pt METCor_T1_pt)
vars=(METCorGood_T1_phi  PuppiMETCorGood_phi boson_phi boson_pt u_par_METCorGood_T1 u_perp_METCorGood_T1 u_par_MET u_perp_MET u_par_PuppiMET u_perp_PuppiMET)
#vars=(METCorGood_T1_pt PuppiMETCorGood_pt)
#vars=(METCorGood_T1_phi  PuppiMETCorGood_phi boson_phi boson_pt njets)
#vars=(boson_pt)

dosend="1"
moremem="0"
#jetcut="geq0_etaVeto_btagL"  
#jetcut="gt0"  

alljetcuts=(njetsgeq0 njetsgt0)
alljetcuts=(njetsgt0)
btag="nbtagl_10bins"
#btag="nobtag_10bins"
btag="nbtagl"

veto="1"
for jetcut in ${alljetcuts[@]}; do
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
	    #ss=${ss}_njets${jetcut}_hitslt${veto}${extra}
	    ss=${ss}_${jetcut}_${btag}_hitslt${veto}${extra}
	    for ch in ${channels[@]}; do
	    
	      for vr in ${vars[@]}; do

	  #echo $sy, $yr, $ss


      if [[ $sy == "Nominal" ]] ; then sy=""
      fi
      cp job_template Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
      #echo job_template Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
      echo python gjets_met_distribution.py -y $yr -v $vr$sy -q 0 -e ${ss} -c $ch -l no >> Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh
      cp jdl_template Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl

    #echo $ss , $yr
    #if [[ $moremem == "1" ]]  ; then
    #  #echo "will modify memory"

    #  sed  -i '1 i request_memory = 4200' Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
    #fi
      yrr=${yr}
      if [[ "$yrr" == *"preVFP"*  ]] ; then
      yrr="2016preVFP"
      fi
     
      sed -i 's/EXECHERE/jobb_'${yr}'_'${vr}''${sy}'_'${ss}'_'${ch}'.sh/g' Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
      sed -i 's/YEARHERE/'${yrr}'/g' Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.jdl
      echo "cp plotS*root ../../." >> Jobs_gjets/jobb_${yr}_${vr}${sy}_${ss}_${ch}.sh


	    done
	  done
	done
      done
    done
done

rm Jobs_gjets/*Up*data* Jobs_gjets/*Down*data* Jobs_gjets/*data*Down* Jobs_gjets/*data*Up*

for jetcut in ${alljetcuts[@]}; do
    for sy in ${allsyst[@]}; do

      for yr in ${years[@]}; do
      
	for ss in ${samples[@]}; do

	
	    #ss=${ss}_njets${jetcut}_hitslt${veto}${extra}
	    ss=${ss}_${jetcut}_${btag}_hitslt${veto}${extra}
	    for ch in ${channels[@]}; do
	    
	      for var in ${vars[@]}; do

	  #echo $sy, $yr, $ss

      
      if [[ $sy == "Nominal" ]] ; then sy=""
      fi
      #plotS_2018_ew_njetsgt0_hitslt2_MET_T1_pt_MuMu.root
      #plotS_2016preVFP_ewk_njetsgt0_hitslt2_PuppiMETWmassJESUp_ElEl.root

      #Jobs_gjets/plotS_2016postVFP_ewk_njetsgt0_hitslt2_METWmassUnclusteredDown_MuMu.root
      # Jobs_gjets/jobb_2016postVFP_METWmassUnclusteredDown_ewk_njetsgt0_hitslt2_ElEl.sh
      #plotS_2017_ew_njetsgt0_hitslt2_PuppiMETCorGood_ptJERUp_MuMu.root
      if [[ ! -f Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
      #echo Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}_${ch}.root 
      #if [[ ! -f Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}_${ch}.root ]] ; then
      #do
      echo this is not there... Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}${ch}.root 
      #echo send   Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}_${ch}.root
      cd Jobs_gjets;   
      condor_submit jobb_${yr}_${var}${sy}_${ss}_${ch}.jdl; cd ..
      else echo Jobs_gjets/plotS_${yr}_${ss}_${var}${sy}_${ch}.root
      fi 
	    done
	  done
	done
      done
    done
done
