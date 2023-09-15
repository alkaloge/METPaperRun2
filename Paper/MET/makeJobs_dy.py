import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
samples = ["data", "dy", "dynlo", "top", "ew"]
channels = ["MuMu","ElEl"]
years = ["2016preVFP", "2016postVFP", "2017", "2018"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016preVFP", "2016postVFP"]
extra = ""
vars = ["MET_T1_pt", "PuppiMET_pt", "boson_pt", "METWmass", "u_par_MET", "u_perp_MET", "PuppiMETWmass"]
vars = ['RawMET_pt', 'RawPuppiMET_pt', 'METCorGood_T1_pt', 'PuppiMETCorGood_pt', 'METCorGood_T1Smear_pt', 'boson_pt', 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', 'u_parboson_METCorGood_T1Smear', 'u_parboson_METCorGood_T1', 'u_perp_METCorGood_T1Smear', 'u_perp_METCorGood_T1', 'u_parboson_PuppiMETCorGood', 'u_perp_PuppiMETCorGood']

#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars = ["mll"]
IDWP = "_cutbased"

#IDWP = "_mvaid"
alljetcuts = ["njetsgeq0", "njetsgt0"]
btag = "nbtagl" + IDWP + "_varbins_isocut"
btag = "nbtagl" + IDWP + "_varbins"
#btag = "nbtagl" + IDWP + "_varbins_isocuttight"
allpv= ['lt10' ] 
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
allpv=['_pugeq40']
#allpv=[]
pu=""
veto="1"
tosend=[]
print("will make jobs for", btag, vars, years, pu, allpv, alljetcuts)
if True:
#for pu in allpv : 
    for jetcut in alljetcuts:
	for yr in years:

	    for ss in samples:
		ss = ss + "_" + jetcut + "_" + btag + pu + "_hitslt" + veto + extra


		for ch in channels:
		    for vr in vars:
			script_file_path = 'Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
			jdl = 'jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
			tosend.append(jdl)
			for sy in allsyst:
			    if 'data' in ss and 'Up' in sy : continue
			    if 'data' in ss and 'Down' in sy : continue
			    if ( 'mll' in vr or 'boson_pt' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr) and ( 'JE' in sy or 'Uncl' in sy ): continue
			    if sy == "Nominal":
				sy = ""

				#os.system('cp job_template_empty Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				os.system('cp job_template Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				os.system('cp jdl_template_dy Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

				os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

			    with open(script_file_path, 'a') as script_file:
				command = 'python dy_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
                                #print command
				script_file.write(command)
			    #os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

			os.system('echo "cp plotS*root ../../." >> Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

print '................To be send ', tosend
if len(tosend) > 0 :
    os.system('cd Jobs_dy' + IDWP)
    for i in tosend:
        #i = i.replace('jdl','sh')
        #command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ; cd ..;'.format('Jobs_dy' + IDWP, i)
        command = 'cd {0:s}; condor_submit {1:s}; touch {1:s}.submitted '.format('Jobs_dy' + IDWP, i)
        #command = 'cp {0:s}/{1:s} . ; cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET; . {1:s}; '.format('Jobs_dy' + IDWP, i)
        #print command
        if not os.path.isfile('{0:s}.submitted'.format(i)) :
           #print 'should send', command
           os.system(command)

