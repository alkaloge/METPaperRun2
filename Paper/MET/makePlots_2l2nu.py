#!/usr/bin/env python
import os
from ROOT import TFile

years = ["2016preVFP", "2016postVFP", "2017", "2018", "2016"]
#years = ["2016preVFP", "2016postVFP", "2017", "2016"]
#years = ["2016postVFP"]
#years = ["2017", "2018"]
years = ["2016preVFP", "2016postVFP", "2016", "2017", "2018", "Run2"]
#years = ["2016preVFP", "2016postVFP", "2016"]

years = ["2018"]

channels = ["2Mu2Nu", "2El2Nu"]
channels = ["2Mu2Nu"]
vars = [
    "RawMET_pt",
    "RawPuppiMET_pt",
    "METCorGood_T1_pt",
    "PuppiMETCorGood_pt",
    "METCorGood_T1Smear_pt",
    "boson_pt",
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_perp_RawPuppiMET",
    "u_parboson_METCorGood_T1Smear",
    "u_parboson_METCorGood_T1",
    "u_perp_METCorGood_T1Smear",
    "u_perp_METCorGood_T1",
    "u_parboson_PuppiMETCorGood",
    "u_perp_PuppiMETCorGood"]
#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "METCorGood_T1Smear_pt"]
#vars=["iso_1", "Photon_hoe_1", "Photon_sieie_1"]

vars = [
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_perp_RawPuppiMET",
    "u_parboson_METCorGood_T1Smear",
    "u_parboson_METCorGood_T1",
    "u_perp_METCorGood_T1Smear",
    "u_perp_METCorGood_T1",
    "u_parboson_PuppiMETCorGood",
    "u_perp_PuppiMETCorGood"]

vars = [
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_perp_RawPuppiMET"]
vars = [
    "METCorGood_T1_phi",
    "PuppiMETCorGood_phi",
    "boson_phi",
    "METCorGood_T1Smear_phi",
    "boson_phi"]

vars = [
    "METCorGood_T1_phi",
    "PuppiMETCorGood_phi",
    "boson_phi",
    "METCorGood_T1Smear_phi",
    "boson_phi",
    "RawMET_phi",
    "RawPuppiMET_phi"]

vars = [
    "METCorGood_T1_phi",
    "PuppiMETCorGood_phi",
    "boson_phi",
    "METCorGood_T1Smear_phi",
    "RawMET_phi",
    "RawPuppiMET_phi",
    "RawMET_phi",
    "RawPuppiMET_phi",
    "RawMET_pt",
    "RawPuppiMET_pt",
    'u_parboson_RawMET',
    'u_parboson_RawPuppiMET',
    'u_perp_RawMET',
    'u_perp_RawPuppiMET',
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_perp_RawPuppiMET",
    "u_parboson_METCorGood_T1Smear",
    "u_parboson_METCorGood_T1",
    "u_perp_METCorGood_T1Smear",
    "u_perp_METCorGood_T1",
    "u_parboson_PuppiMETCorGood",
    "u_perp_PuppiMETCorGood",
    "mll",
    "METCorGood_T1_pt",
    "PuppiMETCorGood_pt",
    "boson_pt",
    "METCorGood_T1Smear_pt"]
# vars=["PuppiMETCorGood_phi"]
#vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "boson_pt", "mll"]
vars = [
    "MET_T1_phi",
    "MET_T1_pt",
    "PuppiMET_pt",
    "PuppiMET_phi",
    'u_parboson_RawMET',
    'u_parboson_RawPuppiMET',
    'u_perp_RawMET',
    'u_perp_RawPuppiMET',
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_perp_RawPuppiMET",
    "u_parboson_METCorGood_T1Smear",
    "u_parboson_METCorGood_T1",
    "u_perp_METCorGood_T1Smear",
    "u_perp_METCorGood_T1",
    "u_parboson_PuppiMETCorGood",
    "u_perp_PuppiMETCorGood"]

varsall = [
    "MET_T1_phi",
    "MET_T1_pt",
    "PuppiMET_pt",
    "PuppiMET_phi",
    "METCorGood_T1_phi",
    "PuppiMETCorGood_phi",
    "boson_phi",
    "METCorGood_T1Smear_phi",
    "RawMET_phi",
    "RawPuppiMET_phi",
    "RawMET_pt",
    "RawPuppiMET_pt",
    'u_parboson_RawMET',
    'u_parboson_RawPuppiMET',
    'u_perp_RawMET',
    'u_perp_RawPuppiMET',
    "u_parboson_RawMET",
    "u_parboson_RawPuppiMET",
    "u_perp_RawMET",
    "u_parboson_METCorGood_T1Smear",
    "u_parboson_METCorGood_T1",
    "u_perp_METCorGood_T1Smear",
    "u_perp_METCorGood_T1",
    "u_parboson_PuppiMETCorGood",
    "u_perp_PuppiMETCorGood",
    "mll",
    "METCorGood_T1_pt",
    "PuppiMETCorGood_pt",
    "boson_pt",
    "METCorGood_T1Smear_pt"]


vars = [var for var in varsall if "phi" in var]
vars = ["METCorGood_T1_pt"]
vars = [
    "METCorGood_T1_pt",
    "PuppiMETCorGood_pt",
    "METCorGood_transm",
    "METCorGood_pt",
    "PuppiMETCorGoodboson_pt",
    "PuppiMETCorGoodboson_transm"]
vars = [
    "dPhiMETCorGood_T1J1",
    "dPhiPuppiMETCorGood_J1",
    "dPhiMETCorGood_T1J2",
    "dPhiPuppiMETCorGood_J2"]
vars += ["PuppiMETCorGoodboson_transm",
         "METCorGoodboson_transm",
         "PuppiMETCorGoodboson_pt",
         "METCorGoodboson_pt",
         "PuppiMETCorGoodboson_m",
         "METCorGoodboson_m",
         "PuppiMETCorGoodboson_phi",
         "METCorGoodboson_phi"]
vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt"]
vars = [
    'mll',
    'njets',
    'iso_1',
    'iso_2',
    'eta_1',
    'eta_2',
    'boson_pt',
    'boson_phi']

vars = ['pt_1', 'pt_2']

alljetcuts = ["njetseq0", "njetsgt0_isvbf"]
alljetcuts += ["njetsgt0_isnotvbf"]
#alljetcuts = ["njetsg_lpt_leta_eq0", "njets_lpt_leta_gt0"]
#alljetcuts += ["njetsg_hpt_leta_eq0", "njets_hpt_leta_gt0"]
#alljetcuts = ["njets_lpt_leta_geq0", "njets_lpt_heta_geq0", "njets_lpt_leta_gt0", "njets_lpt_heta_gt0", "njets_hpt_leta_geq0", "njets_hpt_heta_geq0", "njets_hpt_leta_gt0", "njets_hpt_heta_gt0"]
#alljetcuts = ["njetsgt0"]
ID = "cutbased"
#ID = "mvaid"
# njetsgt0_nbtagl_cutbased_varbins_isocuttight_cutbasedtight
veto = "1"
allpv = ['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pugeq40']
allpv = ['_pugeq40']
allpv = ['_metgt100', '_metlt100']
# allpv=['_metlt100']
pu = ""

# dirDY="_bugJets"
dirDY = ""
# dirDY='./Jobs_2l2nu_'+ID
rootDir = './Root_2l2nu'

# isocuttight_pixelSeed_electronVeto
# if True:
for pu in allpv:
    for nj in alljetcuts:

        njetssideband = nj + '_nbtagl_' + ID + "_varbins_sideband" + pu

        #njets = nj+'_nbtagl_' + ID + "_varbins_isocut"+pu
        #njets = nj+'_nobtag_' + ID + "_varbins_isocut"+pu
        #njets = nj+'_nbtagl_' + ID + "_varbins_isocuttight_cutbasedtight"+pu
        njets = nj + '_nobtag_' + ID + "_varbins_isocuttight_cutbasedtight" + pu
        #njets = nj+'_nbtagl_' + ID + "_varbins_isocut"+pu
        njets = nj + '_nobtag_' + ID + "_varbins_isocut" + pu
        njets = nj + '_nbtagl_' + ID + "_varbins_vetolept_metlt100" + pu
        njets = nj + '_nbtagl_' + ID + "_varbins_vetolept" + \
            pu  # varbins_vetolept_metlt100_hitslt1
        njets = nj + '_nbtagl_' + ID + "_varbins" + \
            pu  # varbins_vetolept_metlt100_hitslt1
        njets = nj + '_nobtag_' + ID + "_varbins" + \
            pu  # varbins_vetolept_metlt100_hitslt1
        # isocuttight_cutbasedtight
        if ID == 'mvaid':
            njets = nj + '_nbtagl_' + ID + "_varbins_isocuttight_mvaid80" + pu

        # njetsgt0_nbtagl_cutbased_varbins_isocut
        #njets = nj+'_nbtagl_' + ID + "_varbins_cutbasedtight"+pu
        #if ID == 'mvaid' : njets = nj+'_nbtagl_' + ID + "_varbins_mvaid80"+pu
        #njets = nj+'_nbtagl_' + ID + "_varbins"+pu
        #extraTag = "dynlo_" + njets + "_Scale"
        extraTags = ["dyptz_", "dynlo_"]
        #extraTags = ["dyptz_"]
        #extraTag = "dy_" + njets + "_Scale"
        for extraT in extraTags:
            extraTag = extraT + njets + "_noScale"
            for yr in years:
                for ch in channels:
                    for var in vars:

                        if 'Smear' in var:
                            newvar = var.replace("Smear", "")
                            cpSmeardata = "cp Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{7:s}_{4:s}.root  Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(
                                yr, njets, veto, var, ch, ID, dirDY, newvar)
                            #cpSmeardata = "cp {5:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{6:s}_{4:s}.root  {5:s}/plotS_{0:s}_data_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, dirDY,newvar)
                            print('=========================>', cpSmeardata)
                            os.system(cpSmeardata)

                        patternNom = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(
                            yr, njets, veto, var, ch, ID, dirDY)
                        #patternNom = " Jobs_2l2nu_{5:s}{6:s}_bugJets/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(yr, njets, veto, var, ch, ID,dirDY)
                        patternJE = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JE*_{4:s}.root".format(
                            yr, njets, veto, var, ch, ID, dirDY)
                        patternUncl = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(
                            yr, njets, veto, var, ch, ID, dirDY)
                        patternPU = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(
                            yr, njets, veto, var, ch, ID, dirDY)
                        patternID = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(
                            yr, njets, veto, var, ch, ID, dirDY)

                        patternNomSD = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(
                            yr, njetssideband, veto, var, ch, ID, dirDY)
                        patternJESD = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}JE*_{4:s}.root".format(
                            yr, njetssideband, veto, var, ch, ID, dirDY)
                        patternUnclSD = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}Uncl*_{4:s}.root".format(
                            yr, njetssideband, veto, var, ch, ID, dirDY)
                        patternPUSD = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}PU*_{4:s}.root".format(
                            yr, njetssideband, veto, var, ch, ID, dirDY)
                        patternIDSD = " Jobs_2l2nu_{5:s}{6:s}/plotS_{0:s}_*_{1:s}_hitslt{2:s}_{3:s}ID*_{4:s}.root".format(
                            yr, njetssideband, veto, var, ch, ID, dirDY)

                        pattern = ''
                        patternSD = ''
                        if 'Raw' in var or 'mll' in var or 'boson_pt' in var or 'Photon' in var or 'iso_1' in var or '_sign' in var:
                            pattern = patternNom + patternPU + patternID
                            patternSD = patternNomSD + patternPUSD + patternIDSD
                        else:
                            pattern = patternNom + patternJE + patternUncl + patternPU + patternID
                            patternSD = patternNomSD + patternJESD + \
                                patternUnclSD + patternPUSD + patternIDSD

                        # Use the filename pattern in the hadd command
                        fileIn = "plotS_{0:s}_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(
                            yr, njets, veto, var, ch)

                        # first make qcd
                        pattern = patternNom
                        hadd_command = "hadd -f {0:s} {1:s}".format(
                            fileIn, pattern)
                        if yr == 'Run2':
                            hadd_command = "hadd -f {0:s} {5:s}/plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2017_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2018_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root".format(
                                fileIn,
                                njets,
                                veto,
                                var,
                                ch,
                                rootDir)
                        if yr == '2016':
                            hadd_command = "hadd -f {0:s} {5:s}/plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root {5:s}/plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(
                                fileIn, njets, veto, var, ch, rootDir)
                        #if yr =='2016' : hadd_command = "hadd -f {0:s} plotS_2016preVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root plotS_2016postVFP_{1:s}_hitslt{2:s}_{3:s}_{4:s}.root ".format(fileIn, njets, veto, var, ch)
                        print(hadd_command)
                        os.system(hadd_command)
                        print("done merging...>", fileIn)
                        #ftest = TFile.Open(fileIn, 'read')
                        # ftest.ls()

                        os.system(
                            "python3 makeStack_2l2nu.py -f {} -y {} -v {} -q 0 -e {} -c {} -l no".format(
                                fileIn, yr, var, extraTag, ch))
                        # -c is the channel, use mumu or mm

                        print("done plotting....")
                        # RawMET_pt_2l2nu2018_doQCD_0gjets_njetsgt0_nbtagl_cutbased_varbins_isocuttight_Scale_1Log.png
                        # ${var}_2l2nu${yr}_doQCD_0${extraTag}_0Log.png
                        os.system(
                            "cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_0{2:s}_0Log.png /publicweb/a/alkaloge/plots/MetStudiesPaper/2L2Nu/{0:s}_{1:s}_doQCD0_{2:s}_noLog_{3:s}.png".format(
                                var,
                                yr,
                                extraTag,
                                ch))

                        os.system(
                            "cp plots/test/paperv2/{0:s}_{3:s}{1:s}_doQCD_0{2:s}_1Log.png /publicweb/a/alkaloge/plots/MetStudiesPaper/2L2Nu/{0:s}_{1:s}_doQCD0_{2:s}_Log_{3:s}.png".format(
                                var,
                                yr,
                                extraTag,
                                ch))
                        # cp
                        # plots/test/paperv2/${var}_${ch}${yr}_doQCD_0${extraTagNLO}_1Log.png
                        # /publicweb/a/alkaloge/plots/MetStudiesPaper/${var}_${yr}_doQCD0_${extraTagNLO}_Log_${ch}.png

                        print("done copying over")
