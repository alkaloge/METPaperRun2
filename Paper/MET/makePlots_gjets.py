import os

years = ["2018"]

channels = ["Gjets"]
vars = ["RawMET_pt", "RawPuppiMET_pt", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGood_T1Smear_pt", "boon_pt", "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "iso_1"]
vars=["iso_1"]
alljetcuts = ["njetsgeq0", "njetsgt0"]
#alljetcuts = ["njetsgeq0"]
#Jobs_gjets_cutbased/plotS_2017_gjets_njetsgt0_nbtagl_cutbased_varbins_isocuttight_hitslt1_u_perp_METCorGood_T1Smear_Gjets.root
ID = "cutbased"
veto="1"
for nj in alljetcuts:

    njets = nj+'_nbtagl_' + ID + "_varbins_isocuttight"
    extraTag = "gjets_" + njets + "_Scale"
    for yr in years:
	for ch in channels:
	    for var in vars:

		patternNom = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		patternJE = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JE*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		patternUncl = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		patternPU = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(yr, njets, veto, var, ch, ID)
		patternID = " Jobs_gjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(yr, njets, veto, var, ch, ID)

		pattern =''
		if 'Raw' in var or 'mll' in var or 'boson_pt' in var or 'Photon' in var or 'iso_1' in var: pattern = patternNom + patternPU + patternID
		else : pattern = patternNom + patternJE + patternUncl + patternPU + patternID
		# Use the filename pattern in the hadd command
		fileIn="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch)

		hadd_command = "hadd -f {0:s} {1:s}".format(fileIn, pattern)
		if yr =='2016' : hadd_command = "hadd -f {0:s} plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(fileIn, njets, veto, var, ch)
		print hadd_command
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
		# cp plots/test/paperv2/${var}_${ch}${yr}_doQCD_0${extraTagNLO}_1Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/${var}_${yr}_doQCD0_${extraTagNLO}_Log_${ch}.pdf

		print "done copying over"

