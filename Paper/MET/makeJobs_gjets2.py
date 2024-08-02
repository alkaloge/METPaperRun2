import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
#allsyst = ["IDUp", "IDDown"]

samples = ["data", "gjets", "tx", "ew", "ewknlo", "qcdmg"]
#samples=["data"]
channels = ["Gjets"]
years = ["2016preVFP", "2016postVFP", "2017", "2018"]
#years = ["2016preVFP", "2016postVFP"]
#years = ["2016preVFP"]
extra = ""
vars = ["MET_T1_pt", "PuppiMET_pt", "boson_pt", "METWmass", "u_par_MET", "u_perp_MET", "PuppiMETWmass"]

vars = ['RawMET_pt', 'RawPuppiMET_pt', 'METCorGood_T1_pt', 'PuppiMETCorGood_pt', 'METCorGood_T1Smear_pt', 'boson_pt', 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', 'u_parboson_METCorGood_T1Smear', 'u_parboson_METCorGood_T1', 'u_perp_METCorGood_T1Smear', 'u_perp_METCorGood_T1', 'u_parboson_PuppiMETCorGood', 'u_perp_PuppiMETCorGood']

vars = ["MET_T1_pt", "PuppiMET_pt", "MET_T1_phi", "PuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGood_T1Smear_pt", "boson_pt", "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi"]

#vars = ["Photon_hoe_1"]
vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]

#vars = ["boson_pt"]

#vars = ["iso_1", "Photon_hoe_1", "Photon_sieie_1"]

IDWPs = ["_cutbased", "_mvaid"]
IDWP = "_mvaid"
IDWP = "_cutbased"


#IDWP = "_mvaid"
alljetcuts = ["njetsgeq0", "njetsgt0"]
allpv= ['lt10' ] 
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pugeq40']
#allpv=['_pugeq40']

pu=""
veto="1"
tosend=[]
for pu in allpv : 
#if True:
    btag = "nbtagl" + IDWP + "_varbins"
    #btag = "nbtagl" + IDWP + "_varbins_isocuttight_cutbasedtight"+pu
    if IDWP == '_cutbased' : btag = "nobtag" + IDWP + "_varbins_isocuttight_cutbasedtight"
    #if IDWP == '_cutbased' : btag = "nobtag" + IDWP + "_varbins_cutbasedtight"

    if IDWP == '_mvaid' : btag = "nobtag" + IDWP + "_varbins_isocuttight_mvaid80"

    #btag = "nbtagl" + IDWP + "_varbins_sidebandd"

    #if IDWP == '_cutbased' : btag = "nbtagl" + IDWP + "_varbins_cutbasedtight"
    #if IDWP == '_mvaid' : btag = "nbtagl" + IDWP + "_varbins_mvaid80"
    
    print(("will make jobs for", btag, vars, years, pu, allpv, alljetcuts))
    for jetcut in alljetcuts:
	for yr in years:

	    for ss in samples:
		ss = ss + "_" + jetcut + "_" + btag + pu + "_hitslt" + veto + extra


		for ch in channels:
		    for vr in vars:
			script_file_path = 'Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
			jdl = 'jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
			tosend.append(jdl)
			for sy in allsyst:
			    if 'data' in ss and 'Up' in sy : continue
			    if 'data' in ss and 'Down' in sy : continue
			    if ('boson_pt' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'hoe' in vr) and ( 'JE' in sy or 'Uncl' in sy ): continue
			    if sy == "Nominal":
				sy = ""

				os.system('cp job_template Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				os.system('cp jdl_template Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

				os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

			    with open(script_file_path, 'a') as script_file:
				command = 'python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
				script_file.write(command)
			    #os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

			os.system('echo "cp plotS*root ../../." >> Jobs_gjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')


print('................To be send ', tosend)
if len(tosend) > 0 :
    os.system('cd Jobs_gjets' + IDWP)
    for i in tosend:
	command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ;cd ..;'.format('Jobs_gjets' + IDWP, i)
	#print command
	if not os.path.isfile('{0:s}/{1:s}.submitted'.format('Jobs_gjets' + IDWP,i)):
	   #print 'should send it....'
	   os.system(command)

