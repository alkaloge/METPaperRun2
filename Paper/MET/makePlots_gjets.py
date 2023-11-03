import os

years = ["2016preVFP", "2016postVFP", "2017", "2018", "2016"]
#years = ["2016preVFP", "2016postVFP", "2017", "2016"]
#years = ["2018"]

channels = ["Gjets"]
vars = ["RawMET_pt", "RawPuppiMET_pt", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGood_T1Smear_pt", "boson_pt", "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi"]

vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars=["iso_1", "Photon_hoe_1", "Photon_sieie_1"]
#vars=["METCorGood_T1_pt"]

#vars=["boson_pt", "boson_phi"]
alljetcuts = ["njetsgeq0", "njetsgt0"]
#alljetcuts = ["njetsgeq0"]
#Jobs_gjets_cutbased/plotS_2017_gjets_njetsgt0_nbtagl_cutbased_varbins_isocuttight_hitslt1_u_perp_METCorGood_T1Smear_Gjets.root
ID = "cutbased"
#ID = "mvaid"
#njetsgt0_nbtagl_cutbased_varbins_isocuttight_cutbasedtight
veto="1"
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pugeq40']
#allpv=['_pu30to40']
pu=""
#isocuttight_pixelSeed_electronVeto
#if True:
for pu in allpv : 
    for nj in alljetcuts:

	njetssideband = nj+'_nbtagl_' + ID + "_varbins_sideband"+pu

	njets = nj+'_nbtagl_' + ID + "_varbins_isocuttight_cutbasedtight"+pu

	njets = nj+'_nobtag_' + ID + "_varbins_isocuttight_cutbasedtight"+pu
	#njets = nj+'_nobtag_' + ID + "_varbins_cutbasedtight"+pu
 
	if ID == 'mvaid' : njets = nj+'_nbtagl_' + ID + "_varbins_isocuttight_mvaid80"+pu


	#njets = nj+'_nbtagl_' + ID + "_varbins_cutbasedtight"+pu
	#if ID == 'mvaid' : njets = nj+'_nbtagl_' + ID + "_varbins_mvaid80"+pu
	#njets = nj+'_nbtagl_' + ID + "_varbins"+pu
	extraTag = "gjets_" + njets + "_Scale"
	for yr in years:
	    for ch in channels:
		for var in vars:
                    #plotS_2018_ew_njetsgt0_nbtagl_cutbased_varbins_sidebandc_hitslt1_iso_1_Gjets.root

		    patternNom = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		    patternJE = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JE*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		    patternUncl = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		    patternPU = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		    patternID = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(yr, njets, veto, var, ch, ID)

		    patternNomSD = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njetssideband, veto, var, ch, ID)
		    patternJESD = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JE*_{4:s}.root".format(yr, njetssideband, veto, var, ch, ID)
		    patternUnclSD = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(yr, njetssideband, veto, var, ch, ID)
		    patternPUSD = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(yr, njetssideband, veto, var, ch, ID)
		    patternIDSD = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(yr, njetssideband, veto, var, ch, ID)

		    pattern =''
		    patternSD =''
		    if 'Raw' in var or 'mll' in var or 'boson_pt' in var or 'Photon' in var or 'iso_1' in var: 
                        pattern = patternNom + patternPU + patternID
                        patternSD = patternNomSD + patternPUSD + patternIDSD
		    else : 
                        pattern = patternNom + patternJE + patternUncl + patternPU + patternID
                        patternSD = patternNomSD + patternJESD + patternUnclSD + patternPUSD + patternIDSD

		    # Use the filename pattern in the hadd command
		    fileIn="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch)

                    #first make qcd

		    hadd_command = "hadd -f {0:s} {1:s}".format(fileIn, pattern)
		    if yr =='2016' : hadd_command = "hadd -f {0:s} plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(fileIn, njets, veto, var, ch)
		    print hadd_command
                    #if not os.path.isfile(fileIn):
		    os.system(hadd_command)
		    print "done merging"

		    # if 'nlo' in extraTag:
		    #     os.system("python makeStack.py -y {} -v {} -q 0 -e {} -c {} -l no".format(yr, var, extraTagNLO, ch))
		    #     # -c is the channel, use mumu or mm

		    os.system("python makeStack_gjets.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no".format(fileIn, yr, var, extraTag, ch))
		    # -c is the channel, use mumu or mm

		    print "done plotting...."
		    #RawMET_pt_gjets2018_doQCD_0gjets_njetsgt0_nbtagl_cutbased_varbins_isocuttight_Scale_1Log.pdf 
		    #METCorGood_T1_pt_2018_doQCD0_gjets_njetsgt0_nbtagl_cutbased_varbins_isocuttight_BtagL_T1_r9_noScale_Log_Gjets.pdf
		    #${var}_gjets${yr}_doQCD_0${extraTag}_0Log.pdf

		    os.system("cp plots/test/paperv2/{0:s}_gjets{1:s}_doQCD_0{2:s}_0Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Gjv2/{0:s}_{1:s}_doQCD0_{2:s}_noLog_Gjets.pdf".format(var, yr, extraTag))

		    os.system("cp plots/test/paperv2/{0:s}_gjets{1:s}_doQCD_0{2:s}_1Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Gjv2/{0:s}_{1:s}_doQCD0_{2:s}_Log_Gjets.pdf".format(var, yr, extraTag))

                    if '_pu' in extraTag : 
			os.system("cp plots/test/paperv2/{0:s}_gjets{1:s}_doQCD_0{2:s}_0Log_norm.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Gjv2/{0:s}_{1:s}_doQCD0_{2:s}_noLog_norm_Gjets.pdf".format(var, yr, extraTag))

			os.system("cp plots/test/paperv2/{0:s}_gjets{1:s}_doQCD_0{2:s}_1Log_norm.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Gjv2/{0:s}_{1:s}_doQCD0_{2:s}_Log_norm_Gjets.pdf".format(var, yr, extraTag))


		    # cp plots/test/paperv2/${var}_${ch}${yr}_doQCD_0${extraTagNLO}_1Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/${var}_${yr}_doQCD0_${extraTagNLO}_Log_${ch}.pdf

		    print "done copying over"

