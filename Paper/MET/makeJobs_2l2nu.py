import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
#allsyst = [ "IDUp", "IDDown"]
#allsyst = ["Nominal"]
samples=["data", "qcd", "dy", "top", "ew", "ewk", "ewknlo61", "ewkincl"]
samples = ["data", "dyptz", "dynlo", "top", "ew"]
#samples = ["dyptz"]
channels = ["2Mu2Nu","2El2Nu"]
#channels = ["2El2Nu"]
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
years = ["2016preVFP","2016postVFP"]
years += ["2018", "2017"]
years = ["2018"]
extra = ""

vars = ["METCor_T1_pt", "PuppiMETCor_pt", "boson_pt", "METCor_T1Smear_pt", "mll"]
vars = ["mll", "METCor_T1_phi", "PuppiMETCor_phi", "boson_phi", "METCor_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi", "METCor_T1_pt", "PuppiMETCor_pt", "boson_pt", "METCor_T1Smear_pt"]
#vars = ["RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt"]

varsall=["MET_T1_pt", "PuppiMET_pt", "MET_T1_phi", "PuppiMET_phi", "METCor_T1_phi", "PuppiMETCor_phi", "METCorboson_phi", "PuppiMETCorboson_phi", "METCor_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCor_T1Smear", "u_parboson_METCor_T1", "u_perp_METCor_T1Smear", "u_perp_METCor_T1", "u_parboson_PuppiMETCor", "u_perp_PuppiMETCor", "mll",  "METCor_T1_pt", "PuppiMETCor_pt", "METCorboson_pt", "PuppiMETCorboson_pt", "METCor_T1Smear_pt","METCorboson_m", "PuppiMETCorboson_m", "METCorboson_mt", "PuppiMETCorboson_mt", "METCorboson_T1Smear_mt","METCorboson_T1Smear_phi", "METCorboson_T1Smear_pt", "MET_T1Smear_phi"]
#vars=["MET_T1_phi","MET_T1_pt", "RawMET_pt", "RawPuppiMET_pt", "RawMET_phi", "RawPuppiMET_phi"]

varsall=["METCorSmearboson_pt", "METCorSmearboson_mt", "METCorSmearboson_m", "METCorSmearboson_phi"]
vars= [var for var in varsall if "Smear" in var]

#vars += varsM
#vars=varsall
#vars=["PuppiMETCorboson_m"]
#vars=["PuppiMETCorboson_phi",     "METCorboson_phi"]
#vars=["PuppiMETCor_phi", "METCor_T1_phi", "PuppiMETCor_pt","METCor_T1_pt"]

vars = ["MET_T1_pt", "MET_T1_phi", "METCor_T1_pt", "METCor_T1_phi"]
vars = ["METCor_T1_pt", "PuppiMETCor_pt"]
vars += ["dPhiMETCor_T1J1", "dPhiPuppiMETCor_J1", "dPhiMETCor_T1J2", "dPhiPuppiMETCor_J2"]
vars += ["PuppiMETCorboson_mt", "METCorboson_mt", "PuppiMETCorboson_pt", "METCorboson_pt","PuppiMETCorboson_m", "METCorboson_m", "PuppiMETCorboson_phi", "METCorboson_phi"]
vars+=['mll', 'njets', 'iso_1', 'iso_2', 'eta_1', 'eta_2', 'boson_pt', 'boson_phi']
vars+=['pt_1', 'pt_2']

IDWP = "_cutbased"

#IDWP = "_mvaid"
alljetcuts = ["njetseq0",  "njetsgt0_isvbf", "njetsgt0_isnotvbf"]
#alljetcuts = ["njetsgeq0"]

#btag = "nbtagl" + IDWP + "_varbins"

btag = "nbtagl" + IDWP + "_varbins_isocuttight_cutbasedtight"
btag = "nobtag" + IDWP + "_varbins_isocuttight_cutbasedtight"


btag = "nobtag" + IDWP + "_varbins_vetolept_metlt100"

SR = "isolt0p15_mtmassgt80"
B = "isolt0p15_mtmasslt80"
D = "isogt0p15_mtmasslt80"
C = "isogt0p15_mtmassgt80"
#SR = "isolt0p01_mtmassgt80"

#btag = "nbtagm" + IDWP + "_varbins_vetolept_"+SR
btag = "nbtagl" + IDWP + "_openbins_vetolept_metlt100"

btag = "nbtagl" + IDWP + "_openbins"
#btag = "nbtagl" + IDWP + "_varbins"
#dyptz_njetseq0_nbtagl_cutbased_varbins_vetolept_metlt100

OneByOne = False

OneByOne = True

allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
allmet=['_metlt100', '_metgt100']
#allpv=['_pugeq40']
#allpv=[]
pu=""
veto="1"
tosend=[]
print(("will make jobs for", btag, vars, years, pu, allpv, allmet, alljetcuts))
#if True:
for pu in allmet : 
    for jetcut in alljetcuts:
        for yr in years:

            for ss in samples:
                #if 'top' in ss : OneByOne = True
                #if ss=='ewk' : OneByOne = True

                ss = ss + "_" + jetcut + "_" + btag + pu + "_hitslt" + veto + extra

                if not OneByOne:
                    for ch in channels:
                        for vr in vars:
                            script_file_path = 'Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
                            jdl = 'jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
                            tosend.append(jdl)
                            for sy in allsyst:
                                if 'data' in ss and 'Up' in sy : continue
                                if 'data' in ss and 'Down' in sy : continue
                                if ( 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
                                #if ( 'mll' in vr or 'boson_pt' in vr or 'boson_phi' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
                                if sy == "Nominal":
                                    sy = ""

                                    #os.system('cp job_template_empty Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                                    os.system('cp job_template Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                                    os.system('cp jdl_template_2l2nu Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
                                    #if ch =='2El2Nu' and ('ew_' in ss or 'dy_' in ss ):   
                                    #    os.system("sed -i '7i\RequestMemory = 4000' Jobs_2l2nu" + IDWP + "/jobb_" + str(yr) + "_" + vr + "allsyst_" + ss + "_" + ch + ".jdl")
                                    os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
                                    os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')

                                with open(script_file_path, 'a') as script_file:
                                    command = 'python3 2l2nu_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
                                    #print command
                                    script_file.write(command)
                                #os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

                            os.system('echo "cp plotS*root ../../." >> Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                #if 'top' in ss or ss=='ewk':
                #if 'not (top' in ss  or 'ewk'!=ss) :
                else:
                    for ch in channels:
                        for vr in vars:
                            for sy in allsyst:
                                if 'data' in ss and 'Up' in sy : continue
                                if 'data' in ss and 'Down' in sy : continue
                                if 'data' in ss and 'Smear' in vr : continue
                                if 'smear' not in vr.lower() and 'JER' in sy : continue
                                #if ( 'mll' in vr or 'boson_pt' in vr or 'boson_phi' in vr or 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
                                if sy == "Nominal": sy = ""
                                if ( 'Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr ) and ( 'JE' in sy or 'Uncl' in sy ): continue
                                script_file_path = 'Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh'
                                jdl = 'jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl'
                                #print 'jdl', jdl, sy
                                tosend.append(jdl)

                                os.system('cp job_template Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')
                                os.system('cp jdl_template_2l2nu Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
                                os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh/g\' Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')
                                os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.jdl')

                                with open(script_file_path, 'a') as script_file:
                                    command = 'python3 2l2nu_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
                                    script_file.write(command)

                                os.system('echo "cp plotS*root ../../." >> Jobs_2l2nu' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy+'_' + ss + '_' + ch + '.sh')

print(('................To be send ', len(tosend), tosend))
if len(tosend) > 0 :
    os.system('cd Jobs_2l2nu' + IDWP)
    for i in tosend:
        #i = i.replace('jdl','sh')
        #command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ; cd ..;'.format('Jobs_2l2nu' + IDWP, i)
        #command = 'cp {0:s}/{1:s} . ; cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET; . {1:s}; '.format('Jobs_2l2nu' + IDWP, i)
        command = 'cd {0:s}; condor_submit {1:s}; touch {1:s}.submitted '.format('Jobs_2l2nu' + IDWP, i)
        #print command
        #plotS_2018_ewk_njetsgt0_nobtag_cutbased_varbins_noveto_mtmassgt80_hitslt1_METCor_T1_ptJESUp_2Mu2Nu.root
        #print  '{0:s}/{1:s}.submitted'.format('Jobs_2l2nu' + IDWP, i)

        if not os.path.isfile('{0:s}/{1:s}.submitted'.format('Jobs_2l2nu' + IDWP, i)) :
            print(('should send', command))
            os.system(command)
        #else : 
        #    print 'this one exists.....', i+'.submitted'
