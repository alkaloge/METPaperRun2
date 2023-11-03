##############################################################
##############################################################
######                                                 #######
######  |##\     /##|      |########| |##############| #######
######  |###\   /###|      |##|             |##|       #######
######  |####\_/####|      |##|             |##|       #######
######  |##|\###/|##|      |######|         |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |########|       |##|       #######
######                                                 #######             
##############################################################
##############################################################

import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership
import math, sys, optparse, array, time, copy

import include.helper     as helper
import include.Region     as Region
import include.Canvas     as Canvas
import include.CutManager as CutManager
import include.Sample     as Sample
import include.Rounder    as Rounder        
#import include.METCorrections as METCor

#from METCor import correctedMET


def makeUParaOverQt(met, phi,boson, boson_phi):
    uParaOverQt = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson+")/"+ boson   )
    return uParaOverQt

def makeUParaNoQt(met, phi,boson, boson_phi):
    uParaNoQt = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson+")" )
    return uParaNoQt                                                                                                                                                                                                                                                           
def makeUPara(met, phi,boson, boson_phi):
    
    uPara = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson+ " + " +boson+")" )
    print "uPara:  ", uPara
    return uPara                                                                                                                                                                                                                                                           
def makeUPerp(met, phi,boson, boson_phi):
    uPerp = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*sin( " +boson_phi +" )-(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*cos( " +boson_phi +" ))/" +boson +")" )                              
    print "uPerp:  ",uPerp
    return uPerp                                                                                                                                                                                                                                                                      
def makeMET(met):
# yes this is the smartest function 
    justMET = met 
    return justMET

era='2017'
channel=''
if __name__ == "__main__":

    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples_2017.dat', help='the samples file. default \'samples.dat\'')
    parser.add_option('-y', '--year', action='store', type=str, dest='Year', default='2017', help='choose from 2016, 2017, 2018 \'samples.dat\'')
    parser.add_option('-v', '--variable', action='store', type=str, dest='varr', default='MET_T1_pt', help='variable to plot ')
    parser.add_option('-q', '--doqcd', action='store', type=str, dest='DoQCD', default=0, help='do data-driven QCD')
    parser.add_option('-e', '--extra', action='store', type=str, dest='ExtraTag', default='', help='extra Tag')
    parser.add_option('-c', '--channel', action='store', type=str, dest='Channel', default='', help='channel')
    parser.add_option('-l', '--local', action='store', type=str, dest='Local', default='', help='running local or on condor')
    (opts, args) = parser.parse_args()
    doDY = True
    doNPV = True
    doee = True
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : doee = False
    if 'el' in str(opts.Channel.lower()) : doee = True
    if doee :   channel = 'ElNu'
    else :   channel = 'MuNu'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    
    opts.sampleFile = 'samples_{0:s}_v2.dat'.format(era[:4], channel)
     
    if '2016' in era and 'pre' in era : 
        eras ='2016preVFP'
    if '2016' in era and 'post' in era : 
        eras ='2016postVFP'
    if '2016' in era and 'post' not in era  and 'pre' not in era: 
        eras ='2016postVFP'

    opts.sampleFile = 'samples_{0:s}_v2.dat'.format(eras)
    print 'will read Datasets from ', opts.sampleFile

    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':16.9777, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.351, '2016postVFP':16.9777,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    lumi = lumis[era]
    yields={}
    print 'Going to load DATA and MC trees...'
    inn = str(opts.ExtraTag).lower()
    doQCD = int(opts.DoQCD)
    if 'qcdinv' in inn : doQCD=True
    if doDY:
        if doee:
            channel = 'ElNu'
            lumi = lumis[era]
            run = era

            ttDatasets = ['TTTo2L2Nu', 'TTToSemiLeptonic']
            tt2L2NuDatasets = ['TTTo2L2Nu']
            #ttDatasets = ['TTToSemiLeptonic']
            ttDatasets = ['TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            ttDatasets = ['TTTo2L2Nu', 'TTToSemiLeptonic']

            stDatasets = ['ST_s-channel', 'ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
 
            ttDatasets += stDatasets

            #ttDatasets = ['ST_s-channel_antitop', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            dyDatasets = ['DYJetsToLLM50', 'DYJetsToLLM10to50']
            ewDatasets = ['WW', 'WWW', 'WZZ']
            ewDatasets = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# 
            if '2016' in era : ewDatasets = ['WW', 'WZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']
            ewk1Datasets = ['W1JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk2Datasets = ['W2JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk3Datasets = ['W3JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk4Datasets = ['W4JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            #ewkDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']
            #ewkDatasets = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J']

            ewkNLODatasets = ['WJetsToLNu_NLO']
            ewkDatasets = ['WJetsToLNuincl']
            ewk61Datasets = ['WJetsToLNuincl61']
            ewkNLO61Datasets = ['WJetsToLNu_NLO61']
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']
            qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']

            qcdDatasetsPtBins = [ 'QCD_Pt-120to170_EMEn', 'QCD_Pt-15to20_EMEn', 'QCD_Pt-170to300_EMEn', 'QCD_Pt-20to30_EMEn', 'QCD_Pt-300toInf_EMEn', 'QCD_Pt-30to50_EMEn', 'QCD_Pt-50to80_EMEn', 'QCD_Pt-80to120_EMEn']
            

            #daDatasets = [ 'EGamma_Run2018A', 'EGamma_Run2018B', 'EGamma_Run2018C', 'EGamma_Run2018D']  
            daDatasets = [ 'SingleElectron_Run2017B','SingleElectron_Run2017C', 'SingleElectron_Run2017D', 'SingleElectron_Run2017E', 'SingleElectron_Run2017F']  
            if run =='2017B' : daDatasets = [ 'SingleElectron_Run2017B']
            if run =='2017C' : daDatasets = [ 'SingleElectron_Run2017C']
            if run =='2017D' : daDatasets = [ 'SingleElectron_Run2017D']
            if run =='2017E' : daDatasets = [ 'SingleElectron_Run2017E']
            if run =='2017F' : daDatasets = [ 'SingleElectron_Run2017F']
            if run=='dry': daDatasets = dyyDatasets

            if run =='2018' : daDatasets = [ 'EGamma_Run2018B','EGamma_Run2018C', 'EGamma_Run2018D', 'EGamma_Run2018A']
            if run =='2018A' : daDatasets = [ 'EGamma_Run2018A']
            if run =='2018B' : daDatasets = [ 'EGamma_Run2018B']
            if run =='2018C' : daDatasets = [ 'EGamma_Run2018C']
            if run =='2018D' : daDatasets = [ 'EGamma_Run2018D']

            if run =='2016' : daDatasets = [ 'SingleElectron_Run2016Bv1_preVFP', 'SingleElectron_Run2016Bv2_preVFP',  'SingleElectron_Run2016C_preVFP',  'SingleElectron_Run2016D_preVFP',  'SingleElectron_Run2016E_preVFP',  'SingleElectron_Run2016Fv2_preVFP',  'SingleElectron_Run2016Fv1',  'SingleElectron_Run2016G',  'SingleElectron_Run2016H']
            if run =='2016preVFP' : daDatasets = [ 'SingleElectron_Run2016Bv1_preVFP', 'SingleElectron_Run2016Bv2_preVFP',  'SingleElectron_Run2016C_preVFP',  'SingleElectron_Run2016D_preVFP',  'SingleElectron_Run2016E_preVFP',  'SingleElectron_Run2016Fv2_preVFP']
            if run =='2016postVFP' : daDatasets = [ 'SingleElectron_Run2016Fv1',  'SingleElectron_Run2016G',  'SingleElectron_Run2016H']
            if run =='2016' : daDatasets = [ 'SingleElectron_Run2016Fv1',  'SingleElectron_Run2016G',  'SingleElectron_Run2016H']

            if run =='2016BpreVFP' : daDatasets = [ 'SingleElectron_Run2016Bv1_preVFP', 'SingleElectron_Run2016Bv2_preVFP']
            if run =='2016CpreVFP' : daDatasets = [ 'SingleElectron_Run2016C_preVFP']
            if run =='2016DpreVFP' : daDatasets = [ 'SingleElectron_Run2016D_preVFP']
            if run =='2016EpreVFP' : daDatasets = [ 'SingleElectron_Run2016E_preVFP']
            if run =='2016FpreVFP' : daDatasets = [ 'SingleElectron_Run2016Fv2_preVFP']
            if run =='2016F' : daDatasets = [ 'SingleElectron_Run2016Fv1']
            if run =='2016G' : daDatasets = [ 'SingleElectron_Run2016G']
            if run =='2016H' : daDatasets = [ 'SingleElectron_Run2016H']

            #daDatasets = [ 'SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017F']  
            #daDatasets = [ 'SingleMuon_Run2017B']  
        else:
            channel = 'MuNu'
            lumi = lumis[era]
            run = era

            ttDatasets = ['TTTo2L2Nu', 'TTToSemiLeptonic']
            tt2L2NuDatasets = ['TTTo2L2Nu']
            #ttDatasets = ['TTToSemiLeptonic']
            ttDatasets = ['TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            ttDatasets = ['TTTo2L2Nu', 'TTToSemiLeptonic']

            stDatasets = ['ST_s-channel', 'ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_s-channel_antitop', 'ST_t-channel_top','ST_tW_antitop', 'ST_tW_top']
 
            ttDatasets += stDatasets

            #ttDatasets = ['ST_s-channel_antitop', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            dyDatasets = ['DYJetsToLLM50', 'DYJetsToLLM10to50']
            ewDatasets = ['WW', 'WWW', 'WZZ']
            ewDatasets = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            if '2016' in era : ewDatasets = ['WW', 'WZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']
            ewk1Datasets = ['W1JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk2Datasets = ['W2JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk3Datasets = ['W3JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk4Datasets = ['W4JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            #ewkDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']
            #ewkDatasets = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J']
            ewkNLODatasets = ['WJetsToLNu_NLO']
            #ewkDatasets = ['WJetsToLNu_0J','WJetsToLNu_1J','WJetsToLNu_2J']

            ewkDatasets = ['WJetsToLNuincl']
            ewk61Datasets = ['WJetsToLNuincl61']
            ewkNLO61Datasets = ['WJetsToLNu_NLO61']
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']
            qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']



            daDatasets = [ 'SingleMuon_Run2017B','SingleMuon_Run2017C', 'SingleMuon_Run2017D', 'SingleMuon_Run2017E', 'SingleMuon_Run2017F']  
            if run =='2017B' : daDatasets = [ 'SingleMuon_Run2017B']
            if run =='2017C' : daDatasets = [ 'SingleMuon_Run2017C']
            if run =='2017D' : daDatasets = [ 'SingleMuon_Run2017D']
            if run =='2017E' : daDatasets = [ 'SingleMuon_Run2017E']
            if run =='2017F' : daDatasets = [ 'SingleMuon_Run2017F']
            if run=='dry': daDatasets = dyyDatasets

            if run =='2018' : daDatasets = [ 'SingleMuon_Run2018B','SingleMuon_Run2018C', 'SingleMuon_Run2018D', 'SingleMuon_Run2018A']
            if run =='2018A' : daDatasets = [ 'SingleMuon_Run2018A']
            if run =='2018B' : daDatasets = [ 'SingleMuon_Run2018B']
            if run =='2018C' : daDatasets = [ 'SingleMuon_Run2018C']
            if run =='2018D' : daDatasets = [ 'SingleMuon_Run2018D']

            if run =='2016' : daDatasets = [ 'SingleMuon_Run2016Bv1_preVFP', 'SingleMuon_Run2016Bv2_preVFP',  'SingleMuon_Run2016C_preVFP',  'SingleMuon_Run2016D_preVFP',  'SingleMuon_Run2016E_preVFP',  'SingleMuon_Run2016Fv2_preVFP',  'SingleMuon_Run2016Fv1',  'SingleMuon_Run2016G',  'SingleMuon_Run2016H']
            if run =='2016preVFP' : daDatasets = [ 'SingleMuon_Run2016Bv1_preVFP', 'SingleMuon_Run2016Bv2_preVFP',  'SingleMuon_Run2016C_preVFP',  'SingleMuon_Run2016D_preVFP',  'SingleMuon_Run2016E_preVFP',  'SingleMuon_Run2016Fv2_preVFP']
            if run =='2016postVFP' : daDatasets = [ 'SingleMuon_Run2016Fv1',  'SingleMuon_Run2016G',  'SingleMuon_Run2016H']

            if run =='2016BpreVFP' : daDatasets = [ 'SingleMuon_Run2016Bv1_preVFP', 'SingleMuon_Run2016Bv2_preVFP']
            if run =='2016CpreVFP' : daDatasets = [ 'SingleMuon_Run2016C_preVFP']
            if run =='2016DpreVFP' : daDatasets = [ 'SingleMuon_Run2016D_preVFP']
            if run =='2016EpreVFP' : daDatasets = [ 'SingleMuon_Run2016E_preVFP']
            if run =='2016FpreVFP' : daDatasets = [ 'SingleMuon_Run2016Fv2_preVFP']
            if run =='2016F' : daDatasets = [ 'SingleMuon_Run2016Fv1']
            if run =='2016G' : daDatasets = [ 'SingleMuon_Run2016G']
            if run =='2016H' : daDatasets = [ 'SingleMuon_Run2016H']

            #daDatasets = [ 'SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017F']  
            #daDatasets = [ 'SingleMuon_Run2017B']  
        print 'the lumito be used is ',lumi
        isLocal = True
        if str(opts.Local) == '0' or str(opts.Local).lower() == 'false' or str(opts.Local).lower() == 'no': isLocal = False
        treeTT = Sample.Tree(helper.selectSamples(opts.sampleFile, ttDatasets, 'TOP'), 'TOP'  , 0, channel, isLocal)
        ##treeST = Sample.Tree(helper.selectSamples(opts.sampleFile, stDatasets, 'STOP'), 'STOP'  , 0)
        treeDY = Sample.Tree(helper.selectSamples(opts.sampleFile, dyDatasets, 'DY'), 'DY'  , 0, channel, isLocal)
        treeEW = Sample.Tree(helper.selectSamples(opts.sampleFile, ewDatasets, 'EW'), 'EW'  , 0, channel, isLocal)
        treeEWKincl = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWKincl'), 'EWKincl'  , 0, channel, isLocal)
        treeEWKincl61 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk61Datasets, 'EWKincl61'), 'EWKincl61'  , 0, channel, isLocal)

        treeEWKAll = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkAllDatasets, 'EWK'), 'EWK'  , 0, channel, isLocal, True)

        treeEWKNLO = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkNLODatasets, 'EWKNLO'), 'EWKNLO'  , 0, channel, isLocal)
        treeEWKNLO61 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkNLO61Datasets, 'EWKNLO61'), 'EWKNLO61'  , 0, channel, isLocal)
        #treeEWK1 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk1Datasets, 'EWK1'), 'EWK1'  , 0, channel, isLocal)
        #treeEWK2 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk2Datasets, 'EWK2'), 'EWK2'  , 0, channel, isLocal)
        #treeEWK3 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk3Datasets, 'EWK3'), 'EWK3'  , 0, channel, isLocal)
        #treeEWK4 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk4Datasets, 'EWK4'), 'EWK4'  , 0, channel, isLocal)
        if 'qcdpt' not in str(opts.ExtraTag) :      treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasets, 'QCD'), 'QCD'  , 0, channel, isLocal)
        if 'qcdpt' in str(opts.ExtraTag) :      treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPtBins, 'QCDPt'), 'QCDPt'  , 0, channel, isLocal)
        #treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPt, 'QCD'), 'QCD'  , 0, channel, isLocal)
        #treeQCDPtBins = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPtBins, 'QCD'), 'QCD'  , 0, channel, isLocal)
        #treeEWKmcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWKmcnlo'), 'EWKmcnlo'  , 0)
        #treeEWK1mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK1mcnlo'), 'EWK1mcnlo'  , 0)
        #treeEWK2mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK2mcnlo'), 'EWK2mcnlo'  , 0)

        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'DA'), 'DATA', 1, channel, isLocal)
        #mcTrees = [  treeTT, treeEWK,  treeDY, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK, treeEWK1, treeEWK2, treeEWK3, treeEWK4]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        mcTrees = []   
        if 'NLO' in str(opts.ExtraTag) : mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]   

        #mcTrees = [ treeDY, treeQCD, treeEWK]   
        #mcTrees = [ treeDY, treeQCD,  treeTT, treeEW, treeEWKNLO]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKmcnlo]   
        #mcTrees = [ treeDY, treeEWK]   
        #mcTreesQCD = [ treeQCD]   
        #mcTrees = [ treeEWK]   
        if 'data' not in inn and not doQCD : treeDA =[]
        mcTrees = []
        if 'dy' in inn  : mcTrees = [treeDY]
        if 'top' in inn  : mcTrees = [treeTT]
        if 'qcd' in inn : mcTrees = [treeQCD]
        if 'ewk' in inn  and 'incl' not in inn and 'nlo' not in inn: mcTrees = [treeEWKAll]
        if 'ewk' in inn  and 'incl' in inn and '61' not in inn: mcTrees = [treeEWKincl]
        if 'ewk' in inn  and 'incl' in inn and '61' in inn : mcTrees = [treeEWKincl61]
        if 'ewknlo' in inn and '61' not in inn : mcTrees = [treeEWKNLO]
        if 'ewknlo61' in inn : mcTrees = [treeEWKNLO61]
        if 'ew' in inn and 'ewk' not in inn : mcTrees = [treeEW]
        if 'allmc' in inn : mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]
        if doQCD : 
            if 'ewknlo' in inn and '61' not in inn: mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]
            if 'ewknlo' in inn and '61' in inn: mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO61]
            if 'incl' not in inn and 'nlo' not in inn: mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKAll]
            if 'incl' in inn and '61' not in inn: mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKincl]
            if 'incl' in inn and '61' in inn: mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKincl61]

        boson = 'boson_pt'
        boson_phi = 'boson_phi'
        print '================================================================================================================checkkkkkkkkkkkkkkkkkkkkk', str(opts.ExtraTag).lower(), treeDA, mcTrees


    run_str =str(lumi)
        
    print 'Trees successfully loaded... for ' ,era, lumi

    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle()
    cuts = CutManager.CutManager()
    color = helper.color

    lumi_str =channel+ 'lumi'+str(lumi)

    etabins = [ -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5,1,  1.5, 2, 2.5,3, 3.5, 4, 4.5, 5]
    hoverebins = [0.01, 0.015, 0.02, 0.025, 0.03,0.035, 0.040, 0.045, 0.05,0.055,   0.06, 0.065, 0.07, 0.075,  0.08,0.085, 0.09, 0.095, 0.1]
    chibins = [ 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0]
    sigmabins = [0., 0.001, 0.002, 0.003, 0.004,0.005,0.006, 0.007, 0.008, 0.009,  0.01 ]
    r9bins = [0.8 , 0.81, 0.82,0.83,  0.84,0.85, 0.86, 0.87,0.88, 0.89, 0.9,0.91, 0.92,0.93, 0.94,0.95, 0.96,0.97, 0.98,0.99, 1.0]
    phibins = [ -3., -2.9,-2.8, -2.7, -2.6,-2.5,  -2.4,-2.3, -2.2,-2.1, -2,-1.9, -1.8,-1.7, -1.6,-1.5, -1.4,-1.3, -1.2,-1.1, -1.,-0.9, -0.8,-0.7, -0.6, -0.5,-0.4,-0.3, -0.2,-0.1, 0.,0.1,  0.2,0.3,  0.4,0.5,  0.6,0.7,  0.8,0.9 ,  1.,1.1,  1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,1.9,  2., 2.1, 2.2,2.3,  2.4,2.5,  2.6, 2.7, 2.8,2.9,  3.]
    jetCut = "(njet >= 0)"
    jetCutInvIso = "(njet >= 0)"
    regions = []
    met = []
    gammaPtbin = [50, 60, 75, 90,105, 120, 140,160, 180, 200,  230, 260,  290, 315,  385] 
    gammaPtbinNEW = range(50, 800, 19) 
    bosonPtbin = [0, 15, 30, 45, 60, 75, 90,105, 120, 140,160, 180, 200,  230, 260,  290, 315,  385] 
    gammabin = [50, 63, 74, 85,96, 107, 118, 129, 140,  152, 164, 176, 188, 200, 215,  230, 245,  260,  275, 290, 305,  320,  340,  370, 400] 
    binsig = range(0, 100, 5) 
    massbin = range(70, 110, 1) 
    njetsbin = range(0, 10, 1) 
    binx = range(0, 400, 5)

    sumEtbin = range(0, 3000, 5) 
    bin2 = range(-200, 200, 5)
    binDebug = range(-190, -170, 1)
    bin1 = range(0, 200, 5)
    sumbin = range(0, 30000, 1000)
    nbin = range(0, 50, 2)
    njbin = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    fullbin = range(0, 10000, 1)
    doHighMetValues = False
    # doVariables below is a list of all the variables which should be plotted, select some or all and go for a coffee.
    if doDY:
        doVariables = ['MET_T1_pt']

        binnings    = [bosonPtbin, bin1, bin2, bin2]
        dependence = 'zll_pt'
        ZtoLL = Region.region('Zto',
                           cuts.leps(), doVariables, dependence, 'MET_T1_pt', binnings, True)
        regions.append(ZtoLL)                                                                                   
        
    else:
        doVariables = ['gamma_pt', 'MET_pt', 'met_uPerp', 'met_uPara']
        binnings    = [gammaPtbin, bin1, bin2,bin2]
        dependence = 'gamma_pt'
        Gamma = Region.region('GammaJets',
                           cuts.gammas(), doVariables, dependence, 'met', binnings, True)
        regions.append(Gamma)                                                                                   

    for reg in regions:
        print color.bold+color.red+'=========================================='
        print 'I am doing', reg.name, channel
        print '=========================================='+color.end
                    
        for var in reg.rvars:  
            Variable = []
            noRatio = False 
            justMET = False 
            doUperp = False
            doUpara = False
            doUParaNoQt = False
            doUParaOverQt = False
            isLog = 0; isSig = 0; fixAxis = 0;option ='met'
            data_hist = 0 ; mc_histo = 0; histo_err = 0; mc_up = 0; mc_down = 0; mc_jerup=0; mc_jerdown=0;mc_jesup = 0; mc_jesdown = 0; mc_unclUp = 0; mc_unclDown = 0; mc_stack = r.THStack();
            cut = reg.cuts
            met=['MET_T1_pt']
            phi=['MET_T1_phi']
            if doDY:
                leg = [0.65, 0.6, 0.81, 0.9]
                #leg = [0.7, 0.6, 0.88, 0.9]
            else:
                leg = [0.65, 0.6, 0.81, 0.9]
            givein ='{0:s}'.format(str(opts.varr))


            docat='1'
            if doee : docat='2'
            nLep = 'nMuon'

            jetcut='0'
            wtmasscut='80'
            extracut=''
            njetsSyst=''
            puppicut=''
            losthits="1"
            btagcut="L"
            jetcut='-1'
            tagname = str(opts.ExtraTag).lower()
            #njets_jesTotalUp  njets_jerUp
            if 'njetsgeq0' in str(opts.ExtraTag).lower() : jetcut='>=0'
            if 'njetsgeq1' in str(opts.ExtraTag).lower() : jetcut='>=1'
            if 'njetsgincl' in str(opts.ExtraTag).lower() : jetcut='>=0'
            if 'njetsgt1' in str(opts.ExtraTag).lower() : jetcut='>1'
            if 'njetsgt0' in str(opts.ExtraTag).lower() : jetcut='>0'
            if 'hitslt1' in str(opts.ExtraTag).lower() : losthits='1'
            if 'hitslt1' in tagname : losthits='1'
            if 'massgt0' in tagname: wtmasscut='0'
            if '_transm' in tagname: wtmasscut='0'
            if 'massgt80' in tagname: wtmasscut='80'
            
            if 'jesup' in givein.lower() : 
                extracut = 'JESUp'
                njetsSyst = '_jesTotalUp'
            if 'jesdown' in givein.lower() : 
                extracut = 'JESDown'
                njetsSyst = '_jesTotalDown'

            if 'unclusteredup' in givein.lower() : extracut = 'UnclusteredUp'
            if 'unclustereddown' in givein.lower() : extracut = 'UnclusteredDown'

            if 'jerup' in givein.lower() : 
                extracut = 'JERUp'
                njetsSyst = '_jerUp'
            if 'jerdown' in givein.lower() : 
                extracut = 'JERDown'
                njetsSyst = '_jerDown'

            if 'puppi' in tagname : puppicut='Puppi'
            if 'btagm' in tagname : btagcut="M"
            if 'btagt' in tagname : btagcut="T"

            ### ACTUAL CUTS
	    jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1  && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s}  && njets{6:s}[0]  {1:s} && {4:s}METCorGoodboson_transm{3:s}[0]> {2:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, btagcut, njetsSyst)
	    jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1  && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s}  && njets[0]  {1:s} && {4:s}METCorGoodboson_transm{3:s}[0]> {2:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, btagcut, njetsSyst)

	    jetCutEl = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 &&  !(fabs(eta_1[0])>1.4442 &&  fabs(eta_1[0])<1.5660) && fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s} && njets{7:s}[0] {1:s} && {4:s}METCorGoodboson_transm{3:s}[0] > {2:s} && Electron_convVeto[0] > 0 && Electron_lostHits[0]<{5:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, losthits,btagcut, njetsSyst)

            

            jetCutInvIso = " (nMuon==1 && pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==2 &&  tightId_1[0] >0   &&  fabs(q_1[0])==1 &&  iso_1[0] > .15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets[0]<20 && METCorGoodboson_transm[0]>0 && isStandalone_1[0]>0 && nbtagL[0]==0"
	    jetCutMuInvIso = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] > .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s} &&  nbtag{5:s}[0]==0 &&njets[0]> {1:s} && {4:s}METCorGoodboson_transm{3:s}[0]> {2:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, btagcut)

            #jetCutInvIso = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] > .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nbtagL[0]==0".format(docat)
	    jetCutElInvIso = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] > .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s} && nbtag{6:s}[0]==0 &&njets[0]> {1:s} && {4:s}METCorGoodboson_transm{3:s}[0] > {2:s} && Electron_convVeto[0] > 0 && Electron_lostHits[0]<{5:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, losthits,btagcut)

            jetCut= jetCutMu
            jetCutInvIso= jetCutMuInvIso
            if doee : 
                jetCut= jetCutEl
                jetCutInvIso= jetCutElInvIso
            print 'CCCCCCCCCCCCCCCCUTTTTS', jetCut, 'GiveIn', givein.lower(), tagname
            if 'vetophoton' in str(opts.ExtraTag).lower() : jetCut = jetCut+ "&&  VetoPhoton[0]==0"
            if 'vetotau' in str(opts.ExtraTag).lower() : jetCut = jetCut+ "&& VetoTau[0]==0"
            if 'vetoall' in str(opts.ExtraTag).lower() : jetCut = jetCut+ "&& VetoTau[0]==0 && VetoPhoton[0]==0"
            if 'pult10' in tagname : jetCut  = jetCut + " && nPVGood[0]<10"
            if 'pu10to20' in tagname : jetCut  = jetCut + " && nPVGood[0]<20 && nPVGood>=10"
            if 'pu20to30' in tagname : jetCut  = jetCut + " && nPVGood[0]<30 && nPVGood>=20"
            if 'pu30to40' in tagname : jetCut  = jetCut + " && nPVGood[0]<40 && nPVGood>=30"
            if 'pu40to50' in tagname : jetCut  = jetCut + " && nPVGood[0]<50 && nPVGood>=40"
            if 'pugeq50' in tagname : jetCut  = jetCut + " && nPVGood[0]>=50 "
            if 'pugeq40' in tagname : jetCut  = jetCut + " && nPVGood[0]>=40 "
            if 'nbtagl' in tagname :  jetCut  = jetCut + " && nbtagL[0]==0.0 "

            #jetCut = "1"
            print color.blue+'************************************************************************************************'+color.end
            print 'jetCut', jetCut
            print 'loading variable %s '%(var)
            # for all the variables with some met in them, we need to run over the jec/unclustered energy to get the errors, that is why there is some nasty repeating of lines below, and both the emt_pt and met_phi is needed for the uPara and uPerp, and the justMET, doUperp and doUpara are set, along with some options used in the plotting, definitions of the option can be found in the include/Canvas.py where all the plotting style is set
            if var == 'MET_T1_pt' or var == 'MET_pt':
                varTitle    = 'p_{T}^{miss} [GeV]';justMET = True;
                #met = ['MET_T1_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown', 'MET_pt_JetResUp', 'MET_pt_JetResDown','MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                #met = ['pt_1']
                met = ['PuppiMET_pt']
                #double dphi = fabs(fabs(fabs(MuonsPhi[0]-MET_phi)-TMath::Pi())-TMath::Pi());
                #transvMass = sqrt(2*MuonsPt[0]*MET_pt*(1-cos(dphi)));
                #met = ['TMath::Sqrt(     )']
                #met = ['njets']
                met = ['DphilMET']
                met = ['njets']
                met = ['MET_T1_pt']
                met = ['METCorGoodboson_transm']
                met = ['METWmass']
                met = ['DphilMET']
                met = ['DphiWMET']
                if 'boson_pt' in givein.lower() : varTitle    = 'q_{T} [GeV]'
                if 'boson_phi' in givein : varTitle    = 'q_{#phi}'
                if 'OQt' in givein.lower() : givein = givein.replace("OQt","/boson_pt")
                met = ['{0:s}'.format(str(givein))]

                #met = ['MET_T1_pt', 'MET_T1_ptJERUp', 'MET_T1_ptJERDown','MET_T1_ptJESUp', 'MET_T1_ptJESDown', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredDown']
                if 'all' in givein :
                    if 'allmet' == givein.lower() : met = ['MET_T1_pt', 'MET_T1_ptJESUp', 'MET_T1_ptJESDown', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredDown']
                    if 'allpuppi' == givein.lower() : met=['PuppiMET_pt', 'PuppiMET_ptJESUp', 'PuppiMET_ptJESDown', 'PuppiMET_ptUnclusteredUp', 'PuppiMET_ptUnclusteredDown']
                    if 'boson_pt' in givein.lower(): met=['boson_pt', 'boson_ptJESUp', 'boson_ptJESDown', 'boson_ptUnclusteredUp', 'boson_ptUnclusteredDown']
                    if  'puppimetwtmass' in givein.lower(): met=['PuppiMETWmass', 'PuppiMETWmassJESUp', 'PuppiMETWmassJESDown', 'PuppiMETWmassUnclusteredUp', 'PuppiMETWmassUnclusteredDown']
                    if  'metwtmass' in givein.lower() and 'puppi' not in givein.lower() : met=['METWmass', 'METWmassJESUp', 'METWmassJESDown', 'METWmassUnclusteredUp', 'METWmassUnclusteredDown']
                    if  'metmtmass' in givein.lower() and 'puppi' not in givein.lower() : met=['METmTmass', 'METmTmassJESUp', 'METmTmassJESDown', 'METmTmassUnclusteredUp', 'METmTmassUnclusteredDown']
                    if  'metmtmass' in givein.lower() and 'puppi' in givein.lower() : met=['PuppiMETmTmass', 'PuppiMETmTmassJESUp', 'PuppiMETmTmassJESDown', 'PuppiMETmTmassUnclusteredUp', 'PuppiMETmTmassUnclusteredDown']
                print 'this is the variable=============>', met

                #met = ['{0:s}'.format(makeUPerp(MET_T1_pt, MET_T1_phi, boson_pt, boson_phi))]
                if 'u_par' in str(opts.varr) or 'u_perp' in str(opts.varr) : varTitle =  'u_{||} + q_{T} [GeV]';justMET = True;
                
                
            elif var == 'met_x':
                varTitle    = 'p_{x}^{miss} [GeV]';justMET = True;  
                met = ['MET_pt*sin(met_phi)', 'MET_pt_JetEnUp*sin(met_jecUp_phi)', 'MET_pt_JetEnDown*sin(met_jecDown_phi)', 'MET_pt_JetResUp*sin(met_shifted_JetResUp_phi)', 'MET_pt_JetResDown*sin(met_shifted_JetResDown_phi)','MET_pt_UnclusteredEnUp*sin(met_shifted_UnclusteredEnUp_phi)', 'MET_pt_UnclusteredEnUp*sin(met_shifted_UnclusteredEnDown_phi)']
            elif var == 'met_y':
                varTitle    = 'p_{y}^{miss} [GeV]';justMET = True;
                met = ['MET_pt*cos(met_phi)', 'MET_pt_JetEnUp*cos(met_jecUp_phi)', 'MET_pt_JetEnDown*cos(met_jecDown_phi)', 'MET_pt_JetResUp*cos(met_shifted_JetResUp_phi)', 'MET_pt_JetResDown*cos(met_shifted_JetResDown_phi)','MET_pt_UnclusteredEnUp*cos(met_shifted_UnclusteredEnUp_phi)', 'MET_pt_UnclusteredEnUp*cos(met_shifted_UnclusteredEnDown_phi)']
            elif var == 'met_sumEt':
                varTitle    = '#Sigma p_{T} [GeV]';justMET = True;
                met = ['met_sumEt', 'met_jecUp_sumEt', 'met_jecDown_sumEt', 'met_shifted_JetResUp_sumEt', 'met_shifted_JetResDown_sumEt','met_shifted_UnclusteredEnUp_sumEt', 'met_shifted_UnclusteredEnDown_sumEt']
            elif var == 'met_rawPt': 
                varTitle    = 'Raw p_{T}^{miss} [GeV]';justMET = True;
                met = ['met_rawPt', 'met_jecUp_rawPt', 'met_jecDown_rawPt', 'met_shifted_JetResUp_rawPt', 'met_shifted_JetResDown_rawPt','met_shifted_UnclusteredEnUp_rawPt', 'met_shifted_UnclusteredEnDown_rawPt']
            elif var == 'met_rawSumEt':
                varTitle    = 'Raw #Sigma p_{T} [GeV]' ;justMET = True;
                met = ['met_rawSumEt', 'met_jecUp_rawSumEt', 'met_jecDown_rawSumEt', 'met_shifted_JetResUp_rawSumEt', 'met_shifted_JetResDown_rawSumEt','met_shifted_UnclusteredEnUp_rawSumEt', 'met_shifted_UnclusteredEnDown_rawSumEt']
            elif var == 'met_uPerp':
                varTitle    = 'u_{#perp}'+"  "+ ' [GeV]' ;justMET = False;doUperp = True;
                met = ['MET_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown', 'MET_pt_JetResUp', 'MET_pt_JetResDown', 'MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                phi = ['met_phi', 'met_jecUp_phi', 'met_jecDown_phi','met_shifted_JetResUp_phi','met_shifted_JetResDown_phi',  'met_shifted_UnclusteredEnUp_phi', 'met_shifted_UnclusteredEnDown_phi']
            elif var == 'met_uPara':
                varTitle =  'u_{||} + q_{T} [GeV]';justMET = False;doUpara = True; 
                #met = ['MET_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown',  'MET_pt_JetResUp', 'MET_pt_JetResDown', 'MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                #phi = ['met_phi', 'met_jecUp_phi', 'met_jecDown_phi', 'met_shifted_JetResUp_phi','met_shifted_JetResDown_phi', 'met_shifted_UnclusteredEnUp_phi', 'met_shifted_UnclusteredEnDown_phi']

                met = ['MET_T1_pt']
                phi = ['MET_T1_phi']

            elif var == 'met_uParaOverQt':
                print 'Happy hour !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', var
                varTitle =  'u_{||}/q_{T} [GeV]';justMET = False;doUParaOverQt = True; 
                met = ['MET_T1_pt']
                #met = ['MET_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown',  'MET_pt_JetResUp', 'MET_pt_JetResDown', 'MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                phi = ['MET_T1_phi']
                #phi = ['met_phi', 'met_jecUp_phi', 'met_jecDown_phi', 'met_shifted_JetResUp_phi','met_shifted_JetResDown_phi', 'met_shifted_UnclusteredEnUp_phi', 'met_shifted_UnclusteredEnDown_phi']
            elif var == 'met_uParaNoQt':
                varTitle =  'u_{||} [GeV]';justMET = False;doUParaNoQt = True; 
                met = ['MET_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown',  'MET_pt_JetResUp', 'MET_pt_JetResDown', 'MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                phi = ['met_phi', 'met_jecUp_phi', 'met_jecDown_phi', 'met_shifted_JetResUp_phi','met_shifted_JetResDown_phi', 'met_shifted_UnclusteredEnUp_phi', 'met_shifted_UnclusteredEnDown_phi']
            
            elif var == 'metRaw_uPerp':
                varTitle    = 'Raw u_{#perp}'+"  "+ ' [GeV]';justMET = False;doUperp = True;
                met=['met_rawPt','met_jecUp_rawPt','met_jecDown_rawPt','met_shifted_JetResUp_rawPt','met_shifted_JetResDown_rawPt','met_shifted_UnclusteredEnUp_rawPt','met_shifted_UnclusteredEnDown_rawPt']
                phi=['met_rawPhi','met_jecUp_rawPhi','met_jecDown_rawPhi','met_shifted_JetResUp_rawPhi','met_shifted_JetResDown_rawPhi','met_shifted_UnclusteredEnUp_rawPhi','met_shifted_UnclusteredEnDown_rawPhi']
            elif var == 'metRaw_uPara':                                                                                                                                                                                     
                varTitle =  'Raw u_{||} + q_{T} [GeV]';justMET = False;doUpara = True;
                met = ['met_rawPt', 'met_jecUp_rawPt', 'met_jecDown_rawPt','met_shifted_JetResUp_rawPt','met_shifted_JetResDown_rawPt', 'met_shifted_UnclusteredEnUp_rawPt', 'met_shifted_UnclusteredEnDown_rawPt']
                phi = ['met_rawPhi', 'met_jecUp_rawPhi', 'met_jecDown_rawPhi','met_shifted_JetResUp_rawPhi','met_shifted_JetResDown_rawPhi',  'met_shifted_UnclusteredEnUp_rawPhi', 'met_shifted_UnclusteredEnDown_rawPhi']
                    
            #miscellaneous plots without jec or unclustered errors
            elif var == 'nVert':
                varTitle = 'Number of vertices'
                met = ['nVert']   
                option = 'nvert'
                isLog = 0
                noRatio = False
                #leg = [0.68, 0.74, 0.82, 0.9]
            elif var == 'met_phi':
                varTitle = 'p_{T}^{miss} #phi'
                met = ['met_phi']                 
            elif var == 'met_sumEt':
                varTitle = 'sumEt'
                met = ['met_sumEt-gamma_pt']               
            
            elif var == 'nJet40':
                varTitle = 'nJet p_{T} > 40 GeV'
                met = ['nJet40']                
            elif var == 'nJetPuppi40':
                varTitle = 'nJetPuppi p_{T} > 40 GeV'
                jetCut = ("((gamma_hasGainSwitchFlag < 1  ))")
                met = ['nJetPuppi40']                
            elif var == 'zll_pt':
                varTitle    = 'q_{T} [GeV]'
                met = ['zll_pt']               
                option = 'qtZ'                       
                noRatio = False
                #leg = [0.58, 0.6, 0.85, 0.9]

            elif var == 'gamma_r9':
                varTitle    = 'R9'
                met = ['gamma_r9']               
                option = 'chi'                       
            elif var == 'gamma_hOverE':
                varTitle    = 'H/E'
                met = ['gamma_hOverE']      
                option = 'chi'          
            elif var == 'gamma_sigmaIetaIeta':
                varTitle    = '#sigma i#eta i#eta '
                met = ['gamma_sigmaIetaIeta']      
                option = 'chi'          
            elif var == 'zll_mass':
                varTitle    = 'm_{ll} [GeV] (200 < q_{T} < 300)'
                met = ['zll_mass']    
                option = 'mass'
            elif var == 'lep_pt1':
                print "here"
                varTitle    = 'Leading lep p_{T} [GeV]'
                met = ['lep_pt[0]']                    
            elif var == 'lep_pt2':
                varTitle    = 'Subleading lep p_{T} [GeV]'
                met = ['lep_pt[1]']                    
            elif var == 'lep_eta1':
                varTitle    = 'Leading lepton #eta'
                met = ['lep_eta[0]']                                   
            elif var == 'lep_eta2':
                varTitle    = 'Subleading lepton #eta'
                met = ['lep_eta[1]']                    
            elif var == 'met_sig':
                varTitle    = 'p_{T}^{miss} Significance [GeV]'
                met = ['met_sig']    
                isSig = 1
                option = 'sig0'
                leg = [0.68, 0.6, 0.82, 0.88]
            elif var == 'met_sig_1jet':
                varTitle    = 'p_{T}^{miss} Significance [GeV]'
                met = ['met_sig']   
                isSig = 1
                option = 'sig1'
                jetCut = ("(nJet40 >= 1)")
                leg = [0.68, 0.6, 0.82, 0.88]
            elif var == 'gamma_pt':
                varTitle    = 'q_{T} [GeV]'
                met = ['gamma_pt']      
                option ='qtG'
                #option ='qtgamma'
                noRatio = False
                #leg = [0.58, 0.6, 0.85, 0.9]
                #leg = [0.60, 0.6, 0.88, 0.9]
                #leg = [0.66, 0.7, 0.8, 0.88]
            elif var == 'chi2':
                varTitle = "#chi^{2} Probability"
                met =  ["TMath::Prob(met_sig,2)"]
                isLog = 0
                option = 'chi'
            elif var == 'chi2_1jet':
                varTitle = "#chi^{2} Probability , p_{T}^{jet1} > 50 GeV"
                met =  [" TMath::Prob(met_sig,2)"]
                cut = ("((jet1_pt >= 0))&&" + reg.cuts)
                isLog = 0
                option = 'chi'
            tmp_histo = 0
            histo_err = 0
            tmp_full = 0
            tmp_fullMCInvIso = 0
            tmp_fullQCDInvIso = 0
            #jetCut = "abs(zll_eta) < 1.4"
            #jetCut = "zll_pt > 440 && zll_pt < 500 && lep_hasGainSwitchFlag[0] < 1  && lep_hasGainSwitchFlag[1] < 1"
            #uParaCut = makeUPara("MET_pt", "met_phi", "gamma_pt", "gamma_phi")
            #print "uParaCut ", uParaCut
            #print "cut      ", cut
            fOut= TFile("plotS_{0:s}_{1:s}_{2:s}_{3:s}.root".format(str(era),str(inn), str(givein), str(channel)), "recreate")
            for m in met:
                Variable = ""
                # here, either make the met, uPara or uPerp, and loop over all five types of met...
                if doUpara:
                    Variable = makeUPara(met[met.index(m)], phi[met.index(m)], boson, boson_phi)
                elif doUParaOverQt: 
                    print 'Happy hour !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    Variable = makeUParaOverQt(met[met.index(m)], phi[met.index(m)], boson, boson_phi)
              
                elif doUParaNoQt:
                    Variable = makeUParaNoQt(met[met.index(m)], phi[met.index(m)], boson, boson_phi)
                elif doUperp:
                    Variable = makeUPerp(met[met.index(m)], phi[met.index(m)], boson, boson_phi)
                elif justMET:                                                           
                    Variable = makeMET(met[met.index(m)])
                    if doDY == 0:
                        Variable = makeMET(met[met.index(m)])
                        #VariableData = makeMET(metData[met.index(m)])
                else:
                    # ... or just take the first element in the list (for example for nvert, pt, eta plots etc.)
                    Variable = met[0]
                if 'njets' in var : reg.bins[reg.rvars.index(var)] = njetsbins
                what = False
                #if str(met.index(m)) == "0" and 'up' not in Variable.lower() and 'down' not in Variable.lower() and 'data' in inn:what = True
                #if met.index(m) == 0 and  'data' in inn:what = True
                if met.index(m) == 0 and 'up' not in givein.lower() and 'down' not in givein.lower() and 'data' in inn:what=True
                print 'cheeeck', met.index(m),  Variable.lower(), inn, what

                #if met.index(m) == 0 and 'up' not in Variable.lower() and 'down' not in Variable.lower() and 'data' in inn:
                #if met.index(m) == 0 and 'up' not in givein.lower() and 'down' not in givein.lower() and 'data' in inn:
                if met.index(m) == 0 and 'data' in inn:
                    #data_hist = treeDA.getTH1F(lumi, var+"_"+reg.name+'data'+str(met.index(m)), Variable, 110, -1.7, -0.3, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                    #data_hist = treeDA.getTH1F(lumi, var+"_"+reg.name+'data'+str(met.index(m)), Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                    varData = var
                    #if 'Up' in var or 'Down' in var : var.replace("_T1","")
                    print 'this is for data', var, 'bins', reg.bins[reg.rvars.index(var)]
                    data_hist = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, channel, isLog)
		    d={'{0:s} tmp_full'.format(data_hist.GetName()):data_hist.Integral()}
		    yields.update(d)
                    htitle = ''
                    if 'Muon' in daDatasets : htitle = 'SM'
                    if 'Electron' in daDatasets or 'EGamma' in daDatasets: htitle = 'SE'
                    print 'looks like I will run in data....'
		    fOut.cd()
		    data_hist.Write('histo_data')


                    print 'data ------->', data_hist.Integral()
                    #if (option == 'qtZ' or option =='qtG' or option == 'qtgamma'): 
                    #    data_hist.Scale(1,"width")

                kfactor=1
                if doQCD and met.index(m) == 0: 
                    data_histInvIso = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, channel, isLog)
		    for itree, tree in  enumerate(mcTrees):
			ind = 0
			cuts = CutManager.CutManager()
			treename = tree.name.lower()
			print 'with  %s for QCD kfactor finding' %treename
			print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, channel
			
			if 'qcd' not in treename : tmp_fullMCInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, channel, isLog)
			if 'qcd' in treename :     tmp_fullQCDInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, channel, isLog)


		    data_histInvIso.Add(tmp_fullMCInvIso,-1)
		    if tmp_fullQCDInvIso.GetSumOfWeights() > 0 : kfactor = data_histInvIso.GetSumOfWeights() / tmp_fullQCDInvIso.GetSumOfWeights()

                
                print color.bold+color.red+'='*20
                print ' kfactor QCD is', kfactor
                print '='*20+color.end

                for itree, tree in  enumerate(mcTrees):
                    ind = 0
                    cuts = CutManager.CutManager()
                    treename = tree.name.lower()
                    print 'with  %s' %treename
                    block = tree.blocks[0]
                    attr =  var+''
                    if met.index(m) == 0:
                        # this option here treats the first variable in the list met, which is either just the regular met, or the only element in a list, for nvert, pt eta, etc. This should get the TH1 for data and mc. For mc, both a full histo and a stack is made. 
                        print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, channel, 'from treename', treename
                        #tmp_full= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                        tmp_full= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, channel, isLog)
                        
                        if tmp_full.GetEntries()<0 : continue
                        if tmp_full.Integral<0 : 
                            print 'this has no meaningful entries... will skip it', tmp_full.GetName(), tmp_full.Integral()
                            continue
                        print ' histo has integral ', tmp_full.GetName(), tmp_full.Integral()
                        #if (option == 'qt' or option == "qtG" or option == "qtZ" or option == 'qtgamma'): 
                        #    tmp_full.Scale(1,"width")
                        tmp_full.SetFillColorAlpha(block.color, 0.5)
                        tmp_full.SetTitle(block.name)
                        htitle=treename
                        if treename == 'gjets':
                            tmp_full.SetTitle("#gamma + jets")
                        if treename == 'qcd':
                            tmp_full.SetTitle("QCD multijet")
                            tmp_full.Scale(kfactor)
                        if treename == 'wjets':
                            tmp_full.SetTitle("W + jets")
                        if treename == 'ewk' or treename == "ewkincl":
                            tmp_full.SetTitle("W + jets (LO)")
                        if treename == 'ewkincl61':
                            tmp_full.SetTitle("W + jets (LO)-61")
                        if treename == 'ewknlo61':
                            tmp_full.SetTitle("W + jets (NLO)-61")

                        if treename == 'ewknlo':
                            tmp_full.SetTitle("W + jets (NLO)")

                        if treename == 'dy':
                            if doee:
                                tmp_full.SetTitle("Z/#gamma^{*} #rightarrow ee")
                            else:                                    
                                tmp_full.SetTitle("Z/#gamma^{*} #rightarrow #mu#mu")
                            tmp_full.SetTitle("Z/#gamma^{*} + jets")
                        if treename == 'tt' or treename =='top' or 'TT' in treename:
                            tmp_full.SetTitle("Top quark")
                        if treename == 'ew':
                            tmp_full.SetTitle("Di/Triboson")
                        if treename == 'stop':
                            tmp_full.SetTitle("Single-Top quark")
                        
                        getattr(reg, attr).setHisto(tmp_full, 'MC', 'central')
                        tmp_histo = copy.deepcopy(tmp_full.Clone(var+reg.name))
                        fOut.cd()
                        tmp_histo.Write('histo_'+treename+'_'+m)

                        for i in range(1,tmp_histo.GetNbinsX()+1) : print 'bin i', i, tmp_histo.GetBinContent(i), tmp_histo.GetName(), tmp_histo.Integral()
                        tmp_histo.GetXaxis().SetTitle(varTitle)
                        mc_stack.Add(tmp_histo)
                        print 'some info on mcstack that I added', mc_stack.GetNhists(), mc_stack.GetName(), 'from ', tmp_histo.GetName(), tmp_histo.Integral()
                        #print 'itree ------->', itree, tree, mcTrees, len(mcTrees)
                        if not ind: mc_stack.Draw()
                        
                        #if itree == int(len(mcTrees)-1): 
                        mc_stack.Draw()
                        try : mc_stack.GetXaxis().SetTitle(tmp_histo.GetXaxis().GetTitle())
                        except ReferenceError: continue
                        ind+=1
                        print treename,  'histo has integral %.2f'%tmp_histo.Integral() , tmp_histo.GetName(), tmp_histo.GetEntries()

                        d={'{0:s} tmp_full'.format(tmp_full.GetName()):tmp_full.Integral()}
                        yields.update(d)
                        d={treename:tmp_full.Integral()}
                        yields.update(d)

                        if doHighMetValues:
                            highMet = tmp_histo.FindLastBinAbove(0, 1)
                            print "high metbin: ", highMet                 
                            
                        if not mc_histo:
                            mc_histo = copy.deepcopy(tmp_histo)
                            print 'creating copy at mc_histo', mc_histo.GetName(), mc_histo.Integral()
                        else:
                            mc_histo.Add(tmp_histo, 1.)                
                            print 'adding copy at mc_histo', mc_histo.GetName(), mc_histo.Integral()

                    if len(met)>1: # when the array is longer than one, do jec and met unclustered errors, and just get the histo, no stack obvi, and this is of course only done for mc.
                        #met = ['MET_T1_pt', 'MET_T1_ptJESUp', 'MET_T1_ptJESDown','MET_T1_ptJERUp', 'MET_T1_ptJERUp', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredDown']
                        print ' WILL WORK FOR INDEX ===============>', met.index(m), m
                        #mc_up = mc_histo; mc_down = mc_histo; mc_jesup = mc_histo; mc_jesdown = mc_histo;mc_unclUp = mc_histo; mc_unclDown = mc_histo

                        if met.index(m) > 0:
                            #histo_err= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable,  110, -1.7, -0.3, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                            #histo_err= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                            histo_err= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, channel, isLog)
                            fOut.cd()
                            histo_err.Write('histo_'+treename+"_"+m)
                            #if (option == 'qt' or option == 'qtZ' or option == 'qtG 'or option == 'qtgamma'): 
                            #    histo_err.Scale(1,"width")
                            SetOwnership(histo_err, 0 )
                        if met.index(m) == 1:
                            if not mc_jesup:                                    
                                mc_jesup = copy.deepcopy(histo_err);SetOwnership(mc_jesup, 0 )
                            else:
                                mc_jesup.Add(histo_err)
                            print 'doing mc_JESup'
                        if met.index(m) == 2:
                            if not mc_jesdown:
                                mc_jesdown = copy.deepcopy(histo_err);SetOwnership(mc_jesdown, 0 )
                            else:
                                mc_jesdown.Add(histo_err)
                            print 'doing mc_JESdown'                                                         
                        if met.index(m) == 3:
                            if not mc_unclUp:                                    
                                mc_unclUp = copy.deepcopy(histo_err);SetOwnership(mc_unclUp, 0 )
                            else:
                                mc_unclUp.Add(histo_err)
                            print 'doing mc_unclUp'
                        if met.index(m) == 4:
                            if not mc_unclDown:
                                mc_unclDown = copy.deepcopy(histo_err);SetOwnership(mc_unclDown, 0 )
                            else:
                                mc_unclDown.Add(histo_err)
                        '''
                        if met.index(m) == 1:
                            if not mc_jerup:                                    
                                mc_jerup = copy.deepcopy(histo_err);SetOwnership(mc_jerup, 0 )
                            else:
                                mc_jerup.Add(histo_err)
                            print 'doing JERUp'
                        if met.index(m) == 2:
                            if not mc_jerdown:
                                mc_jerdown = copy.deepcopy(histo_err);SetOwnership(mc_jerdown, 0 )
                            else:
                                mc_jerdown.Add(histo_err)
                            print 'doing JERdown'                                                         
                            print 'doing mc_unclDown'
                    '''
                    #else: # else, just do stat errors
                    if len(met)==1 :     mc_jerup=mc_histo; mc_jerdown = mc_histo; mc_jesup = mc_histo; mc_jesdown = mc_histo;mc_unclUp = mc_histo; mc_unclDown = mc_histo
                    if len(met)==3 :     mc_jerup=mc_histo; mc_jerdown = mc_histo; mc_unclUp = mc_histo; mc_unclDown = mc_histo
                    if len(met)==5 :     mc_jerup=mc_histo; mc_jerdown = mc_histo; 

            SetOwnership(mc_stack, 0 )                                                                                                                       
            if len(mcTrees)> 0 : SetOwnership(tmp_histo, 0 )
            try :SetOwnership(mc_histo, 0 )
            except TypeError : continue
            logcase=[0,1]
            for ilog in logcase :
                isLog = ilog
		print 'plotting ', var
		if isSig:
		    # this is an option for when the met significance plot is made, which make the little chi2 line.
		    print "bin cont ", mc_histo.Integral() 
	     
		    f = r.TF1("f", str(mc_histo.Integral())+"*2*TMath::Prob(x, 2)", 1, 40) 
		    plot_var = Canvas.Canvas("test/paper/%s_%s%s"%(var,reg.name, channel), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])
		else:
		    if doNPV:
			puReweight = ''
			puname = ''
		    else:
			puReweight = '#Tr'
			puname = 'ntiReweight'
		    plot_var = Canvas.Canvas("test/paper/%s_%s%s%s%s_doQCD_%s%s_%sLog"%(str(opts.varr),reg.name, channel, puname,str(era), str(int(doQCD)), str(opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])
		    #plot_var = Canvas.Canvas("test/paper/%s_%s%s%s_doQCD_%s%s"%(str(opts.varr), channel, puname, str(era), str(int(doQCD)), str(opts.ExtraTag)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])
		#print "data mean ", data_hist.GetMean()
		#pprint 'stacking histograms...', mc_stack.GetIntegral()
                if met.index(m) == 0 and ('up' in Variable.lower() or 'down' in Variable.lower()): data_hist = mc_histo
		plot_var.addStack(mc_stack  , "hist" , 1, 1)
                #fOut.cd()
                #mc_stack.Write(htitle)
		#plot_var.addLatex (0.65, 0.55, 'Uncert.')
		if isSig:
		    plot_var.addHisto(f, "E,SAME"   , "#chi^{2} d.o.f. 2"  , "L", r.kBlack , 1, 0)
                if not data_hist : data_hist = mc_histo
		plot_var.addHisto(data_hist, "E,SAME"   , "Data"  , "PL", r.kBlack , 1, 0)

		if noRatio:
		    plot_var.save(1,  1, lumi,  "", "", varTitle, option)
		else:
		    #data_hist = mc_histo
		    #met = ['MET_T1_pt', 'MET_T1_ptJESUp', 'MET_T1_ptJESDown','MET_T1_ptJERUp', 'MET_T1_ptJERUp', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredUp']
		    #plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_unclUp, mc_unclDown, varTitle , option, run_str)
		    
		    #for i in range(1, mc_histo.GetNbinsX()+1) : 
		    #	mc_histo.SetBinError(i, mc_histo.GetBinError(i)*0.25)
		    #mc_jerup=mc_histo; mc_jerdown = mc_histo; mc_jesup = mc_histo; mc_jesdown = mc_histo;mc_unclUp = mc_histo; mc_unclDown = mc_histo
		    mc_jerup=mc_histo; mc_jerdown = mc_histo; 

		    plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle , option, run_str)
		    #plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle+"Int data"+str(data_hist.Integral()) , option, run_str)
            del plot_var
            del Variable
            print yields
            time.sleep(0.1)
            print color.blue+'********************************************DONE***************************************************'+color.end
