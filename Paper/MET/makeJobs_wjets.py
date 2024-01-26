import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
#allsyst = [ "IDUp", "IDDown"]
#allsyst = ["Nominal"]
samples=["data", "qcd", "dy", "top", "ew", "ewk", "ewknlo61", "ewkincl", "ewkht"]
samples=["data", "qcd", "dy", "top", "ew", "ewk", "ewknlo61", "ewkincl"]
#samples=["qcd", "dy", "top", "ew", "ewk", "ewknlo61", "ewkincl", "ewkht"]
#samples=["ewk","ewkincl", "ewknlo61"]
#samples=["ewknlo61"]
channels = ["MuNu","ElNu"]
#channels = ["ElNu"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016postVFP", "2018"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016preVFP", "2016", "2018"]
years = ["2016preVFP","2016postVFP", "2017", "2018"]
#years = ["2016preVFP","2016postVFP"]
#years = ["2018A","2018B", "2018C","2018D"]
years = ["2018", "2017", "2016preVFP","2016postVFP"]
#years = ["2016postVFP"]
#years = ["2018", "2017"]
#years = ["2016preVFP","2016postVFP"]
extra = ""
vars = ["MET_T1_pt", "PuppiMET_pt", "boson_pt", "METWmass", "u_par_MET", "u_perp_MET", "PuppiMETWmass"]


vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt", "mll"]
vars = ["mll", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt"]
vars = ['RawMET_pt', 'RawPuppiMET_pt', 'METCorGood_T1_pt', 'PuppiMETCorGood_pt', 'METCorGood_T1Smear_pt', 'boson_pt', 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', 'u_parboson_METCorGood_T1Smear', 'u_parboson_METCorGood_T1', 'u_perp_METCorGood_T1Smear', 'u_perp_METCorGood_T1', 'u_parboson_PuppiMETCorGood', 'u_perp_PuppiMETCorGood', 'mll']


vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]
vars = ["u_parboson_RawPuppiMET", "u_perp_RawPuppiMET", "u_parboson_RawMET" , "u_perp_RawMET" ]

varsall=["MET_T1_pt", "PuppiMET_pt", "MET_T1_phi", "PuppiMET_phi", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood", "mll",  "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm"]

#vars=["METCorGood_T1Smear_phi"]
#vars=["MET_T1_phi","MET_T1_pt", "RawMET_pt", "RawPuppiMET_pt", "RawMET_phi", "RawPuppiMET_phi"]
#vars= [var for var in varsall if "Puppi" in var]

#vars=["njets", "iso_1", "METCorGoodboson_transm"]
#vars=["njets", "iso_1", "METCorGoodboson_transm"]
#vars += varsM
vars=varsall
vars=["PuppiMETCorGoodboson_m"]
#vars=["PuppiMETCorGoodboson_phi",     "METCorGoodboson_phi"]
#vars=["RawMET_pt", "RawMET_phi","METCorGood_T1_phi", "PuppiMETCorGood_pt","METCorGood_T1_pt"]
#vars=["PuppiMETCorGood_phi", "METCorGood_T1_phi", "PuppiMETCorGood_pt","METCorGood_T1_pt"]

IDWP = "_cutbased"

#IDWP = "_mvaid"
alljetcuts = ["njetsgeq0", "njetsgt0", "njetseq0"]
#alljetcuts = ["njetsgeq0"]

#btag = "nbtagl" + IDWP + "_varbins"

btag = "nbtagl" + IDWP + "_varbins_isocuttight_cutbasedtight"
btag = "nobtag" + IDWP + "_varbins_isocuttight_cutbasedtight"

btag = "nbtagl" + IDWP + "_varbins_noveto_mtmassgt80"

btag = "nbtagl" + IDWP + "_varbins_noveto_mtmassgt80"

SR = "isolt0p15_mtmassgt80"
B = "isolt0p15_mtmasslt80"
D = "isogt0p15_mtmasslt80"
C = "isogt0p15_mtmassgt80"
#SR = "isolt0p01_mtmassgt80"

btag = "nbtagl" + IDWP + "_varbins_vetolept_"+SR


OneByOne = False

OneByOne = True
#btag = "nobtag" + IDWP + "_varbins_isocut"

allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
#allpv=['_pugeq40']
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
		#if 'top' in ss : OneByOne = True
		#if ss=='ewk' : OneByOne = True
                   
		ss = ss + "_" + jetcut + "_" + btag + pu + "_hitslt" + veto + extra

                if not OneByOne:
		    for ch in channels:
			for vr in vars:
			    script_file_path = 'Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
			    jdl = 'jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
			    tosend.append(jdl)
			    for sy in allsyst:
				if 'data' in ss and 'Up' in sy : continue
				if 'data' in ss and 'Down' in sy : continue
				if ( 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				#if ( 'mll' in vr or 'boson_pt' in vr or 'boson_phi' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				if sy == "Nominal":
				    sy = ""

				    #os.system('cp job_template_empty Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				    os.system('cp job_template Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
				    os.system('cp jdl_template_dy Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				    #if ch =='ElEl' and ('ew_' in ss or 'dy_' in ss ):   
				    #    os.system("sed -i '7i\RequestMemory = 4000' Jobs_wjets" + IDWP + "/jobb_" + str(yr) + "_" + vr + "allsyst_" + ss + "_" + ch + ".jdl")
				    os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
				    os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

				with open(script_file_path, 'a') as script_file:
				    command = 'python wjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
				    #print command
				    script_file.write(command)
				#os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

			    os.system('echo "cp plotS*root ../../." >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                #if 'top' in ss or ss=='ewk':
                #if 'not (top' in ss  or 'ewk'!=ss) :
                else:
		    for ch in channels:
			for vr in vars:
			    for sy in allsyst:
				if 'data' in ss and 'Up' in sy : continue
				if 'data' in ss and 'Down' in sy : continue
				#if ( 'mll' in vr or 'boson_pt' in vr or 'boson_phi' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				if sy == "Nominal": sy = ""
				if ( 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
				script_file_path = 'Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh'
				jdl = 'jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl'
                                #print 'jdl', jdl, sy
			        tosend.append(jdl)

				os.system('cp job_template Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')
				os.system('cp jdl_template_dy Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
				os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
				os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')

				with open(script_file_path, 'a') as script_file:
				    command = 'python wjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
				    script_file.write(command)

			        os.system('echo "cp plotS*root ../../." >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')

print '................To be send ', len(tosend), tosend
if len(tosend) > 0 :
    os.system('cd Jobs_wjets' + IDWP)
    for i in tosend:
        #i = i.replace('jdl','sh')
        #command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ; cd ..;'.format('Jobs_wjets' + IDWP, i)
        #command = 'cp {0:s}/{1:s} . ; cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET; . {1:s}; '.format('Jobs_wjets' + IDWP, i)
        command = 'cd {0:s}; condor_submit {1:s}; touch {1:s}.submitted '.format('Jobs_wjets' + IDWP, i)
        #print command
        #plotS_2018_ewk_njetsgt0_nobtag_cutbased_varbins_noveto_mtmassgt80_hitslt1_METCorGood_T1_ptJESUp_MuNu.root
        #print  '{0:s}/{1:s}.submitted'.format('Jobs_wjets' + IDWP, i)

        if not os.path.isfile('{0:s}/{1:s}.submitted'.format('Jobs_wjets' + IDWP, i)) :
           print 'should send', command
           os.system(command)
        #else : 
        #    print 'this one exists.....', i+'.submitted'
