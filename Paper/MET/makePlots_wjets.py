#!/usr/bin/env python
import os

years = ["2016preVFP", "2016postVFP", "2017", "2018", "2016"]
#years = ["2016preVFP", "2016postVFP", "2017", "2016"]
#years = ["2016postVFP"]
#years = ["2017", "2018"]
years = ["2016preVFP", "2016postVFP", "2016", "2017", "2018"]
#years = ["2016preVFP", "2016postVFP", "2016", "2017"]
years = ["2016preVFP", "2016postVFP","2016", "2017"]
years = ["2016preVFP", "2016postVFP", "2016","2017", "2018"]
years = ["2017","2018"]
#years = ["2016preVFP"]
#years = ["2016preVFP", "2016postVFP","2016"]
years = ["2016preVFP", "2016postVFP","2016"]
years += ["2018", "2017"]
#years = ["2016postVFP"]
years=["2016", "Run2"]
years = ["2016preVFP", "2016postVFP", "2016", "2017", "2018"]
years = ["2016preVFP", "2016postVFP",  "2017", "2018"]
years=["2016postVFP", "2016postVFP"]
years = ["2018"]

dirRoot='./Root_Wjets/'

channels = ["MuNu", "ElNu"]
#channels = ["ElNu"]
vars = ["RawMET_pt", "RawPuppiMET_pt", "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGood_T1Smear_pt", "boson_pt", "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]
#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars=["iso_1", "Photon_hoe_1", "Photon_sieie_1"]
vars=["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
vars=["RawMET_pt", "RawMET_phi", "RawPuppiMET_pt", "RawPuppiMET_phi", "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]


vars=["u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]

vars=["RawMET_pt", "RawMET_phi", "RawPuppiMET_pt", "RawPuppiMET_phi"]

vars=["u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET"]
vars=["u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood"]
vars=["METCorGood_T1_phi", "PuppiMETCorGood_phi", "boson_phi", "METCorGood_T1Smear_phi","boson_phi"]


vars=["METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood",   "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt","METCorGoodboson_m", "MET_T1_pt", "MET_T1_phi", "PuppiMET_pt", "PuppiMET_phi"]

varsall=["MET_T1_pt", "PuppiMET_pt", "MET_T1_phi", "PuppiMET_phi", "METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', 'u_perp_RawPuppiMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood",  "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm",  "METCorGoodboson_T1Smear_transm","METCorGoodboson_T1Smear_phi", "METCorGoodboson_T1Smear_pt"]

#varsall=["u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood",   "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm"]

#vars=["METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt",  "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood",   "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt" "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm"]

#vars=["METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt" "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm"]

#vars=["u_parboson_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_parboson_METCorGood_T1Smear"]
#vars=["METCorGood_T1_pt", "PuppiMETCorGood_pt"]
#vars=["MET_T1_phi","MET_T1_pt", "RawMET_pt", "RawPuppiMET_pt", "RawMET_phi", "RawPuppiMET_phi"]
#avars=["RawMET_pt", "RawMET_phi","METCorGood_T1_phi", "PuppiMETCorGood_pt","METCorGood_T1_pt"]

#vars= [var for var in varsall if "_pt" in var]
#vars=["MET_T1_pt", "METCorGoodboson_pt", "METCorGoodboson_phi", "PuppiMET_pt", "PuppiMET_phi", "MET_T1_phi"]

#vars+=["METCorGoodboson_pt", "PuppiMETCorGoodboson_pt" , "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm"]
#vars=["PuppiMETCorGoodboson_pt", "METCorGoodboson_pt"]
#vars=["PuppiMETCorGoodboson_m", "METCorGoodboson_m"]
#vars=["u_parboson_METCorGood_T1Smear"]
varsall+=["METCorGoodSmearboson_pt", "METCorGoodSmearboson_transm", "METCorGoodSmearboson_m", "METCorGoodSmearboson_phi"]
varsall+=["MET_T1Smear_pt","MET_T1Smear_phi", "METCorGood_T1Smear_pt", "METCorGood_T1Smear_phi"]
vars=varsall

vars=["PuppiMETCorGood_pt"]
vars=["METCorGoodboson_transm", "METCorGoodSmearboson_transm","PuppiMETCorGoodboson_transm"]
vars=["PuppiMETCorGoodboson_pt", "METCorGoodboson_pt", "METCorGoodSmearboson_pt"]
vars+=["PuppiMETCorGoodboson_phi", "METCorGoodboson_phi", "METCorGoodSmearboson_phi"]

vars=["PuppiMETCorGoodboson_m", "METCorGoodboson_m", "METCorGoodSmearboson_m"]

###########################
varspaper= ["METCorGoodSmearboson_m", "METCorGoodSmearboson_phi", "METCorGoodSmearboson_pt", "METCorGoodSmearboson_transm", "METCorGood_T1Smear_phi", "METCorGood_T1Smear_pt", "METCorGood_T1_phi", "METCorGood_T1_pt", "METCorGoodboson_m", "METCorGoodboson_phi", "METCorGoodboson_pt", "METCorGoodboson_transm", "MET_T1Smear_phi", "MET_T1Smear_pt", "MET_T1_phi", "MET_T1_pt", "PuppiMETCorGood_phi", "PuppiMETCorGood_pt", "PuppiMETCorGoodboson_m", "PuppiMETCorGoodboson_phi", "PuppiMETCorGoodboson_pt", "PuppiMETCorGoodboson_transm", "PuppiMET_phi", "PuppiMET_pt", "RawMET_phi", "RawMET_pt", "RawPuppiMET_phi", "RawPuppiMET_pt"]
vars=varspaper

vars +=["METCorSmearboson_m", "METCorSmearboson_phi", "METCorSmearboson_pt", "METCorSmearboson_transm", "METCor_T1Smear_phi", "METCor_T1Smear_pt", "METCor_T1_phi", "METCor_T1_pt", "METCorboson_m", "METCorboson_phi", "METCorboson_pt", "METCorboson_transm",  "PuppiMETCor_phi", "PuppiMETCor_pt", "PuppiMETCorboson_m", "PuppiMETCorboson_phi", "PuppiMETCorboson_pt", "PuppiMETCorboson_transm"]

vars += ['dPhiMETCorGood_T1J1', 'dPhiPuppiMETCorGood_J1', 'dPhiMETCorGood_T1J2', 'dPhiPuppiMETCorGood_J2', 'dRMETCorGood_T1J1', 'dRPuppiMETCorGood_J1', 'dRMETCorGood_T1J2', 'dRPuppiMETCorGood_J2']
vars += ['dPhiMETCor_T1J1', 'dPhiPuppiMETCor_J1', 'dPhiMETCor_T1J2', 'dPhiPuppiMETCor_J2', 'dRMETCor_T1J1', 'dRPuppiMETCor_J1', 'dRMETCor_T1J2', 'dRPuppiMETCor_J2']

#vars=["METCorboson_transm"]
#varspaper=["PuppiMETCorGood_pt", "METCorGood_T1_pt"]
#varspaper=["METCorGood_T1_pt"]
#vars= [var for var in varspaper if "_m" in var]
#varss= [var for var in varspaper if "_phi" in var]

#vars= [var for var in varsall if "Raw" in var]
alljetcuts = ["njetsgeq0", "njetsgt0", "njetseq0"]
alljetcuts += ["njets_lpt_leta_geq0", "njets_lpt_heta_geq0", "njets_lpt_leta_gt0", "njets_lpt_heta_gt0", "njets_hpt_leta_geq0", "njets_hpt_heta_geq0", "njets_hpt_leta_gt0", "njets_hpt_heta_gt0"]
alljetcuts = ["njetsgt0", "njetseq0"]
alljetcuts = ["njetsgeq0", "njetsgt0", "njetseq0"]
alljetcuts = ["njetsgt0"]

unique_list = []
for item in vars:
    if item not in unique_list:
        unique_list.append(item)
#print(unique_list)

doPost = False
#doPost =True
vars=unique_list

dryRun = False
ID = "cutbased"
#ID = "mvaid"
#njetsgt0_nbtagl_cutbased_varbins_isocuttight_cutbasedtight
veto="1"
allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pugeq40']
allpv=['_pugeq40']
pu=""

doQCD = 0
SR = "isolt0p15_mtmassgt80"
B = "isolt0p15_mtmasslt80"
D = "isogt0p15_mtmasslt80"
C = "isogt0p15_mtmassgt80"

#SR = "isolt0p01_mtmassgt80"

regions = [SR, B, C, D]
regions = [SR]


#aregion=SR
#isocuttight_pixelSeed_electronVeto
if True:
#for pu in allpv : 
    for nj in alljetcuts:

        for region in regions : 
            njetssideband = nj+'_nbtagl_' + ID + "_varbins_sideband"+pu

            #njets = nj+'_nbtagl_' + ID + "_varbins_isocut"+pu
            #njets = nj+'_nobtag_' + ID + "_varbins_isocut"+pu
            njets = nj+'_nobtag_' + ID + "_varbins_noveto_mtmassgt80"+pu
            #njets = nj+'_nobtag_' + ID + "_varbins_noveto_mtmassgt80"+region+pu
            njets = nj+'_nobtag_' + ID + "_varbins_vetolept_"+region+pu
            njets = nj+'_nbtagl_' + ID + "_varbins_vetolept_"+region+pu

            njetsB = nj+'_nbtagl_' + ID + "_varbins_vetolept_"+B+pu
            njetsC = nj+'_nbtagl_' + ID + "_varbins_vetolept_"+C+pu
            njetsD = nj+'_nbtagl_' + ID + "_varbins_vetolept_"+D+pu


            #isocuttight_cutbasedtight
            if ID == 'mvaid' : njets = nj+'_nbtagl_' + ID + "_varbins_isocuttight_mvaid80"+pu

            #njets = njets.replace('varbins', 'longbins')
            njets = njets.replace('varbins', 'openbins')

            #njetsgt0_nbtagl_cutbased_varbins_isocut
            #njets = nj+'_nbtagl_' + ID + "_varbins_cutbasedtight"+pu
            #if ID == 'mvaid' : njets = nj+'_nbtagl_' + ID + "_varbins_mvaid80"+pu
            #njets = nj+'_nbtagl_' + ID + "_varbins"+pu
            extraTag="WInclWNjets_QCDHT_nLepEq1_"+njets

            extraTagNLO="WInclNLO_QCDHT_nLepEq1_"+njets
            extraTagNLO61="WInclNLO61_QCDHT_nLepEq1_"+njets

            extraTagIncl61="WIncl61_QCDHT_nLepEq1_"+njets
            extraTagIncl="WIncl_QCDHT_nLepEq1_"+njets
            extraTagHT="WInclHT_QCDHT_nLepEq1_"+njets


            #extraTag +="_noScale"
            #extraTagIncl +="_noScale"
            #extraTagNLO61 +="_noScale"
            #extraTagHT +="_noScale"

            extraTag +="_Scale"
            extraTagIncl +="_Scale"
            extraTagNLO61 +="_Scale"
            extraTagHT +="_Scale"
            IDdir=ID+"_oldTrigger"
            IDdir=ID
            dummySyst = False
            #IDdir=ID+"_deepCSV_noHEM"
            for yr in years:
                for ch in channels:
                    for var in vars:
                        #if 'Smear' not in var : continue 
                        if 'Smear' in var : 
                            newvar = var.replace("Smear", "")
                            cpSmeardata = "cp Jobs_wjets_{5:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{6:s}_{4:s}.root  Jobs_wjets_{5:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, IDdir, newvar)
                            print ('=========================>', cpSmeardata )
                            os.system(cpSmeardata)
                        patternNom = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, IDdir)
                        patternJE = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JES*_{4:s}.root".format(yr, njets, veto, var, ch, IDdir)
                        patternUncl = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(yr, njets, veto, var, ch, IDdir)
                        patternPU = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(yr, njets, veto, var, ch, IDdir)
                        patternID = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(yr, njets, veto, var, ch, IDdir)

                        patternNomSD = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njetssideband, veto, var, ch, IDdir)
                        patternJESD = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JES*_{4:s}.root".format(yr, njetssideband, veto, var, ch, IDdir)
                        patternUnclSD = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(yr, njetssideband, veto, var, ch, IDdir)
                        patternPUSD = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(yr, njetssideband, veto, var, ch, IDdir)
                        patternIDSD = " Jobs_wjets_{5:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(yr, njetssideband, veto, var, ch, IDdir)

                        pattern =''
                        patternSD =''
                        if 'Raw' in var or 'mll' in var or 'Photon' in var or 'iso_1' in var or '_sign' in var:  
                            pattern = patternNom + patternPU + patternID
                            patternSD = patternNomSD + patternPUSD + patternIDSD
                        else : 
                            pattern = patternNom + patternJE + patternUncl + patternPU + patternID
                            patternSD = patternNomSD + patternJESD + patternUnclSD + patternPUSD + patternIDSD

                        # Use the filename pattern in the hadd command
                        fileIn="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch)
                        fileInB="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njetsB, veto, var, ch)
                        fileInC="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njetsC, veto, var, ch)
                        fileInD="plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njetsD, veto, var, ch)

                        #first make qcd
                        if dummySyst : pattern = patternNom
                        hadd_command = "hadd -f {0:s} {1:s}".format(fileIn, pattern)


                        #if yr =='2016' : hadd_command = "hadd -f {0:s} plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(fileIn, njets, veto, var, ch)
                        if yr =='Run2' : hadd_command = "hadd -f {0:s} {5:s}/plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2017_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2018_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(fileIn, njets, veto, var, ch,dirRoot)
                        if yr =='2016' : hadd_command = "hadd -f {0:s} {5:s}/plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(fileIn, njets, veto, var, ch,dirRoot)
                        print (hadd_command)
                        if not dryRun : os.system(hadd_command)
                        if doQCD : 
                            patternB = pattern.replace(SR, B)
                            patternC = pattern.replace(SR, C)
                            patternD = pattern.replace(SR, D)
                            #print fileInB, fileInC, fileInD
                            hadd_commandB = "hadd -f {0:s} {1:s}".format(fileInB, patternB)
                            hadd_commandC = "hadd -f {0:s} {1:s}".format(fileInC, patternC)
                            hadd_commandD = "hadd -f {0:s} {1:s}".format(fileInD, patternD)
                            os.system(hadd_commandB)
                            os.system(hadd_commandC)
                            os.system(hadd_commandD)
                        print ("done merging")

                        # if 'nlo' in extraTag:
                        #     os.system("python makeStack.py -y {} -v {} -q 0 -e {} -c {} -l no".format(yr, var, extraTagNLO, ch))
                        #     # -c is the channel, use mumu or mm

                        #os.system("python makeStack_wjets.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no".format(fileIn, yr, var, extraTagIncl, ch))
                        #os.system("python makeStack_wjets.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no".format(fileIn, yr, var, extraTagNLO61, ch))
                        # -c is the channel, use mumu or mm

                        #for taG in [extraTag, extraTagIncl, extraTagNLO61, extraTagHT]:
                        if not doQCD : 
                            #for taG in [extraTag, extraTagIncl, extraTagNLO61]:
                            #for taG in [extraTagIncl, extraTag]:
                            #for taG in [extraTagNLO61, extraTagHT]:
                            for taG in [extraTagNLO61]:
                            #for taG in [extraTag]:
                                if not dryRun : 
                                    if not doPost :os.system("python3 makeStack_wjets.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no -s {}".format(fileIn, yr, var, taG, ch, int(dummySyst)))
                                    #if not doPost : print 'ok' 
                                    else :os.system("python3 makePostFit_wjets.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no -s {}".format(fileIn, yr, var, taG, ch, int(dummySyst)))
                                chP = ch
                                if doPost : chP = ch+'_postFit'
                                os.system("cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_0{2:s}_0Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Wjetsv4/{0:s}_{1:s}_doQCD0_{2:s}_noLog_{4:s}.pdf".format(var, yr, taG, ch, chP))

                                os.system("cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_0{2:s}_1Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Wjetsv4/{0:s}_{1:s}_doQCD0_{2:s}_Log_{4:s}.pdf".format(var, yr, taG, ch, chP))
                                #os.system("cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_1{2:s}_0Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Wjetsv3/{0:s}_{1:s}_doQCD1_{2:s}_noLog_{4:s}.pdf".format(var, yr, taG, ch, chP))

                                #os.system("cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_1{2:s}_1Log.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Wjetsv3/{0:s}_{1:s}_doQCD1_{2:s}_Log_{4:s}.pdf".format(var, yr, taG, ch, chP))

                            print ("done plotting....")
                            print ("done copying over")

