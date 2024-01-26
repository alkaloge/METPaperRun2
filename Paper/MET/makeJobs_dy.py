import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
#aallsyst=["Nominal"]
samples = ["data", "dy", "dynlo", "top", "ew"]
#samples = ["dy", "dynlo", "top", "ew"]
#samples = ["data", "dy",  "top", "ew"]
#samples = ["data"]
channels = ["MuMu","ElEl"]
#channels = ["MuMu"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016postVFP", "2018"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016preVFP", "2016postVFP", "2018"]
years = ["2017", "2016preVFP", "2016postVFP", "2018"]
#years = ["2016preVFP"]
extra = ""
vars = ["MET_T1_pt", "PuppiMET_pt", "boson_pt", "METWmass", "u_par_MET", "u_perp_MET", "PuppiMETWmass"]


vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt", "mll"]
vars = ["mll", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt"]
vars = ['RawMET_pt', 'RawPuppiMET_pt', 'METCorGood_T1_pt', 'PuppiMETCorGood_pt', 'METCorGood_T1Smear_pt', 'boson_pt', 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', 'u_parboson_METCorGood_T1Smear', 'u_parboson_METCorGood_T1', 'u_perp_METCorGood_T1Smear', 'u_perp_METCorGood_T1', 'u_parboson_PuppiMETCorGood', 'u_perp_PuppiMETCorGood', 'mll']


vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]
vars = ["u_parboson_RawPuppiMET", "u_perp_RawPuppiMET", "u_parboson_RawMET" , "u_perp_RawMET" ]

vars=["METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi",  "RawPuppiMET_phi" , "RawMET_phi",  "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "mll",  "METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]

vars=["MET_T1_phi", "MET_T1_pt", "PuppiMET_pt", "PuppiMET_phi","METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi",  "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "mll",  "METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars=["MET_T1_phi", "MET_T1_pt", "PuppiMET_pt", "PuppiMET_phi", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]

#vars=["MET_significance"]
#vars=["PuppiMETCorboson_pt", "PuppiMETCorboson_phi","METCorboson_pt", "METCorboson_phi"]
#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "mll"]
#vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", "boson_pt", "boson_phi", "mll", "METCorGood_T1Smear_pt"]

IDWP = "_cutbased"

#IDWP = "_mvaid"
alljetcuts = ["njetsgeq0", "njetsgt0"]

#btag = "nbtagl" + IDWP + "_varbins"

btag = "nbtagl" + IDWP + "_varbins_isocuttight_cutbasedtight"
btag = "nobtag" + IDWP + "_varbins_isocuttight_cutbasedtight"

#btag = "nobtag" + IDWP + "_varbins_isocut"

btag = "nobtag" + IDWP + "_varbins_isocut"

oneByOne = True
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
#allpv=['_pugeq40']
#allpv=[]
pu=""
veto="1"
OneByOne = False
OneByOne = True
tosend=[]
print("will make jobs for", btag, vars, years, pu, allpv, alljetcuts)
if True:
#for pu in allpv : 
    for jetcut in alljetcuts:
	for yr in years:

	    for ss in samples:
		ss = ss + "_" + jetcut + "_" + btag + pu + "_hitslt" + veto + extra

                if not OneByOne : 
		    for ch in channels:
			for vr in vars:
			    script_file_path = 'Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
			    jdl = 'jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
			    tosend.append(jdl)
			    for sy in allsyst:
				if 'data' in ss and 'Smear' in vr : continue
				if 'data' in ss and 'Up' in sy : continue
				if 'data' in ss and 'Down' in sy : continue
				if ( 'mll' in vr or 'boson_pt' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				if sy == "Nominal":
				    sy = ""

				    #os.system('cp job_template_empty Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				    os.system('cp job_template Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				    os.system('cp jdl_template_dy Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				    #if ch =='ElEl' and ('ew_' in ss or 'dy_' in ss ):   
				    #    os.system("sed -i '7i\RequestMemory = 4000' Jobs_dy" + IDWP + "/jobb_" + str(yr) + "_" + vr + "allsyst_" + ss + "_" + ch + ".jdl")
				    os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				    os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

				with open(script_file_path, 'a') as script_file:
				    command = 'python dy_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
				    #print command
				    script_file.write(command)
				#os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

			    os.system('echo "cp plotS*root ../../." >> Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                else:
		    for ch in channels:
			for vr in vars:
			    for sy in allsyst:
				if 'data' in ss and 'Up' in sy : continue
				if 'data' in ss and 'Down' in sy : continue
				#if ( 'mll' in vr or 'boson_pt' in vr or 'boson_phi' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				if sy == "Nominal": sy = ""
				if ( 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr or 'mll' in vr or 'boson_pt' in vr) and ( 'JE' in sy or 'Uncl' in sy ): continue
				script_file_path = 'Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh'
				jdl = 'jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl'
                                #print 'jdl', jdl, sy
                                rootfile='Jobs_dy'+IDWP+'/plotS_'+ str(yr) + '_' +  ss + '_' + vr+ sy+'_'+ ch + '.root'
                                isrootfile=os.path.isfile(rootfile)
                                if not isrootfile :
                                    #print 'root file does not exist', rootfile
				    tosend.append(jdl)

				    os.system('cp job_template Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')
				    os.system('cp jdl_template_dy Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
				    os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
				    os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')

				    with open(script_file_path, 'a') as script_file:
					command = 'python dy_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
					script_file.write(command)

				    os.system('echo "cp plotS*root ../../." >> Jobs_dy' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')

print '................To be send ', tosend
#exit()
if len(tosend) > 0 :
    os.system('cd Jobs_dy' + IDWP)
    for i in tosend:
        #i = i.replace('jdl','sh')
        #command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ; cd ..;'.format('Jobs_dy' + IDWP, i)
        #command = 'cp {0:s}/{1:s} . ; cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET; . {1:s}; '.format('Jobs_dy' + IDWP, i)
        command = 'cd {0:s}; condor_submit {1:s}; touch {1:s}.submitted '.format('Jobs_dy' + IDWP, i)
        print command
        if not os.path.isfile('{0:s}/{1:s}.submitted'.format('Jobs_dy' + IDWP, i)) :
           print 'should send', command
           os.system(command)
           #os.system(command)
        #else : 
        #    print 'this one exists.....', i+'.submitted'
    with open('jobs_dy.txt', 'a') as file:
	# Convert each element of the list to a string and write it to the file
	for item in tosend:
	    file.write(str(item) + '\n')
 



