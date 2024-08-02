import os

allsyst = [    "Nominal",    "JESUp",    "JESDown",    "JERUp",    "JERDown",    "UnclusteredUp",    "UnclusteredDown",    "PUUp",    "PUDown",    "IDUp",    "IDDown"]
allsyst = [    "Nominal",    "JESUp",    "JESDown", "UnclusteredUp",    "UnclusteredDown",    "PUUp",    "PUDown",    "IDUp",    "IDDown"]
#allsyst = [ "JESUp",    "JESDown",   "UnclusteredUp",    "UnclusteredDown",    "PUUp",    "PUDown",    "IDUp",    "IDDown"]
#allsyst = ["Nominal"]
#allsyst = ["JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown", "PUUp", "PUDown", "IDUp", "IDDown"]
samples = ["data",    "qcd",    "dy",    "top",    "ew",    "ewk",    "ewknlo61",    "ewkincl",    "ewkht"]
samples = ["data", "qcd", "dy", "top", "ew", "ewk", "ewknlo61"]
#samples = ["qcd", "dy", "top", "ew", "ewk", "ewknlo61"]
#samples=["qcd", "dy", "top", "ew", "ewknlo61", "ewkincl"]
#samples=["data", "qcd", "dy", "top", "ew", "ewk",  "ewkincl"]
#samples=["qcd", "dy", "top", "ew", "ewk", "ewknlo61", "ewkincl", "ewkht"]
#samples=["data", "ewknlo61"]
channels = ["MuNu", "ElNu"]
#channels = ["MuNu"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2017", "2016postVFP", "2018"]
#years = ["2016preVFP", "2016postVFP"]
years = ["2016preVFP", "2016postVFP"]
#years = ["2018A","2018B", "2018C","2018D"]
years = ["2018", "2017", "2016preVFP", "2016postVFP"]
#years = ["2018", "2016preVFP", "2016postVFP"]
years = ["2016preVFP", "2016postVFP"]
#years += ["2018", "2017"]
years = ["2018"]
extra = ""


varsall = [ "MET_T1_pt", "PuppiMET_pt", "MET_T1_phi", "PuppiMET_phi", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi", "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt", "METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm", "METCorGoodboson_T1Smear_transm", "METCorGoodboson_T1Smear_phi", "METCorGoodboson_T1Smear_pt", "MET_T1Smear_phi", "METCorGoodSmearboson_pt", "METCorGoodSmearboson_transm", "METCorGoodSmearboson_m", "METCorGoodSmearboson_phi"] 
varspaper = [ "METCorGoodSmearboson_m", "METCorGoodSmearboson_phi", "METCorGoodSmearboson_pt", "METCorGoodSmearboson_transm", "METCorGood_T1Smear_phi", "METCorGood_T1Smear_pt", "METCorGood_T1_phi", "METCorGood_T1_pt", "METCorGoodboson_m", "METCorGoodboson_phi", "METCorGoodboson_pt", "METCorGoodboson_transm", "MET_T1Smear_phi", "MET_T1Smear_pt", "MET_T1_phi", "MET_T1_pt", "PuppiMETCorGood_phi", "PuppiMETCorGood_pt", "PuppiMETCorGoodboson_m", "PuppiMETCorGoodboson_phi", "PuppiMETCorGoodboson_pt", "PuppiMETCorGoodboson_transm", "PuppiMET_phi", "PuppiMET_pt", "RawMET_phi", "RawMET_pt", "RawPuppiMET_phi", "RawPuppiMET_pt"] 

varspaper +=["METCorSmearboson_m", "METCorSmearboson_phi", "METCorSmearboson_pt", "METCorSmearboson_transm", "METCor_T1Smear_phi", "METCor_T1Smear_pt", "METCor_T1_phi", "METCor_T1_pt", "METCorboson_m", "METCorboson_phi", "METCorboson_pt", "METCorboson_transm",  "PuppiMETCor_phi", "PuppiMETCor_pt", "PuppiMETCorboson_m", "PuppiMETCorboson_phi", "PuppiMETCorboson_pt", "PuppiMETCorboson_transm"]

varsdR=["dRMETCorGood_T1J1", "dRMETCorGood_T1J2", "dRPuppiMETCorGood_T1J1","dRPuppiMETCorGood_J2"]
varsdR+=["dRMETCor_T1J1", "dRMETCor_T1J2", "dRPuppiMETCor_T1J1","dRPuppiMETCor_J2"]

vars= varspaper
vars += ['dPhiMETCorGood_T1J1', 'dPhiPuppiMETCorGood_J1', 'dPhiMETCorGood_T1J2', 'dPhiPuppiMETCorGood_J2', 'dRMETCorGood_T1J1', 'dRPuppiMETCorGood_J1', 'dRMETCorGood_T1J2', 'dRPuppiMETCorGood_J2']
vars += ['dPhiMETCor_T1J1', 'dPhiPuppiMETCor_J1', 'dPhiMETCor_T1J2', 'dPhiPuppiMETCor_J2', 'dRMETCor_T1J1', 'dRPuppiMETCor_J1', 'dRMETCor_T1J2', 'dRPuppiMETCor_J2']


#vars= [var for var in varspaper if "_pt" in var]
#vars = varspaper
#replacement_string = 'CorGood'
#new_string='Cor'
#vars = [new_string if item == replacement_string else item for item in varspaper]

#vars=["njets", "iso_1", "METCorGoodboson_transm"]
#vars=["njets", "iso_1", "METCorGoodboson_transm"]
#vars += varsM
# vars=varsall
#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt"]
#vars = ["METCorGood_T1_pt"]
#vaars += ["METCorGood_T1Smear_pt"]

IDWP = "_cutbased"

#IDWP = "_mvaid"
alljetcuts = ["njetsgeq0", "njetsgt0", "njetseq0"]
#alljetcuts = ["njetsgeq0"]

#btag = "nbtagl" + IDWP + "_varbins"

btag = "nbtagl" + IDWP + "_varbins_isocuttight_cutbasedtight"
btag = "nobtag" + IDWP + "_varbins_isocuttight_cutbasedtight"

btag = "nbtagl" + IDWP + "_varbins_noveto_mtmassgt80"

#btag = "nbtagl" + IDWP + "_varbins_noveto_mtmassgt80"

SR = "isolt0p15_mtmassgt80"
B = "isolt0p15_mtmasslt80"
D = "isogt0p15_mtmasslt80"
C = "isogt0p15_mtmassgt80"
#SR = "isolt0p01_mtmassgt80"

btag = "nbtagl" + IDWP + "_varbins_vetolept_" + SR
btag = "nbtagl" + IDWP + "_longbins_vetolept_" + SR
btag = "nbtagl" + IDWP + "_openbins_vetolept_" + SR
# nbtagl_cutbased_varbins_vetolept

OneByOne = False

OneByOne = True
#btag = "nobtag" + IDWP + "_varbins_isocut"

allpv = ['_pult10',    '_pu10to20',    '_pu20to30',    '_pu30to40',    '_pu40to50',   '_pugeq50']
# allpv=['_pugeq40']
# allpv=[]
pu = ""
veto = "1"
tosend = []
tosendroot = []
print(("will make jobs for", btag, vars, years, pu, allpv, alljetcuts))
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
                            script_file_path = 'Jobs_wjets' + IDWP + '/jobb_' + \
                                str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'
                            jdl = 'jobb_' + \
                                str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl'
                            tosend.append(jdl)
                            for sy in allsyst:
                                if 'data' in ss and 'Up' in sy:
                                    continue
                                if 'data' in ss and 'Down' in sy:
                                    continue
                                if ('Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr) and (
                                        'JE' in sy or 'Uncl' in sy):
                                    continue
                                # if ( 'mll' in vr or 'boson_pt' in vr or
                                # 'boson_phi' in vr or 'Photon' in vr or 'Raw'
                                # in vr or 'iso_1' in vr or 'ignificance' in vr
                                # ) and ( 'JE' in sy or 'Uncl' in sy ):
                                # continue
                                if sy == "Nominal":
                                    sy = ""

                                    #os.system('cp job_template_empty Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')
                                    os.system('cp job_template Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh'); 
                                    os.system('cp jdl_template_wjets Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
 
                                    # if ch =='ElEl' and ('ew_' in ss or 'dy_' in ss ):
                                    #    os.system("sed -i '7i\RequestMemory = 4000' Jobs_wjets" + IDWP + "/jobb_" + str(yr) + "_" + vr + "allsyst_" + ss + "_" + ch + ".jdl")
                                    os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')
                                    os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.jdl')


                                with open(script_file_path, 'a') as script_file:
                                    command = 'python3 wjets_met_distribution.py -y ' +  str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
                                    # print command
                                    script_file.write(command)
                                #os.system('echo python gjets_met_distribution.py -y ' + str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')

                            os.system('echo "cp plotS*root ../../." >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + 'allsyst_' + ss + '_' + ch + '.sh')


                # if 'top' in ss or ss=='ewk':
                # if 'not (top' in ss  or 'ewk'!=ss) :
                else:
                    for ch in channels:
                        for vr in vars:
                            for sy in allsyst:
                                if 'data' in ss and 'Up' in sy:
                                    continue
                                if 'data' in ss and 'Down' in sy:
                                    continue
                                if 'data' in ss and 'Smear' in vr:
                                    continue
                                if 'smear' not in vr.lower() and 'JER' in sy:
                                    continue
                                # if ( 'mll' in vr or 'boson_pt' in vr or
                                # 'boson_phi' in vr or 'Photon' in vr or 'Raw'
                                # in vr or 'iso_1' in vr or 'ignificance' in vr
                                # ) and ( 'JE' in sy or 'Uncl' in sy ):
                                # continue
                                if sy == "Nominal":
                                    sy = ""
                                if ('Photon' in vr or 'Raw' in vr or 'iso_1' in vr or 'ignificance' in vr) and (
                                        'JE' in sy or 'Uncl' in sy):
                                    continue
                                script_file_path = 'Jobs_wjets' + IDWP + '/jobb_' + \
                                    str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.sh'
                                jdl = 'jobb_' + \
                                    str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.jdl'
                                rootfile = 'plotS_' + \
                                    str(yr) + '_' + ss + '_' + vr + sy + '_' + ch + '.root'
                                # print 'jdl', jdl, sy
                                tosend.append(jdl)
                                tosendroot.append(rootfile)
                                os.system('cp job_template Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.sh')

                                os.system('cp jdl_template_wjets Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.jdl')

                                os.system('sed -i \'s/EXECHERE/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.sh/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.jdl'); 

                                os.system('sed -i \'s/YEARHERE/' + str(yr) + '/g\' Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.jdl')


                                with open(script_file_path, 'a') as script_file:
                                    command = 'python3 wjets_met_distribution.py -y ' + \
                                        str(yr) + ' -v ' + vr + sy + ' -q 0 -e ' + ss + ' -c ' + ch + ' -l no\n'
                                    script_file.write(command)
                                os.system('echo "cp plotS*root ../../." >> Jobs_wjets' + IDWP + '/jobb_' + str(yr) + '_' + vr + sy + '_' + ss + '_' + ch + '.sh')


print('................To be send ', len(tosend), tosend)
if len(tosend) > 0:
    os.system('cd Jobs_wjets' + IDWP)
    #    for i in tosend:
    for i, rootfile in zip(tosend, tosendroot):
        #i = i.replace('jdl','sh')
        #command = 'cd {0:s} ;condor_submit {1:s}; touch {1:s}.submitted ; cd ..;'.format('Jobs_wjets' + IDWP, i)
        #command = 'cp {0:s}/{1:s} . ; cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET; . {1:s}; '.format('Jobs_wjets' + IDWP, i)
        command = 'cd {0:s}; condor_submit {1:s}; touch {1:s}.submitted '.format(
            'Jobs_wjets' + IDWP, i)
        # print command
        # plotS_2018_ewk_njetsgt0_nobtag_cutbased_varbins_noveto_mtmassgt80_hitslt1_METCorGood_T1_ptJESUp_MuNu.root
        # print  '{0:s}/{1:s}.submitted'.format('Jobs_wjets' + IDWP, i)
        jdl_submitted_path = os.path.join(
            'Jobs_wjets' + IDWP, i + '.submitted')
        rootfile_submitted_path = os.path.join('Jobs_wjets' + IDWP, rootfile)

        # if not os.path.isfile('{0:s}/{1:s}.submitted'.format('Jobs_wjets' +
        # IDWP, i)) :
        if not os.path.isfile(jdl_submitted_path) or not os.path.isfile(
                rootfile_submitted_path):
            print('should send', i, 'as ', rootfile, ' does not exist')
            os.system(command)
        # else :
        #    print 'this one exists.....', i+'.submitted'
