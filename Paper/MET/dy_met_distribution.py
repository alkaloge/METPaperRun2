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
import include.Sample    as Sample
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
    if doee :   channel = 'ElEl'
    else :   channel = 'MuMu'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    
    opts.sampleFile = 'samples_{0:s}_2l.dat'.format(era[:4], channel)
     
    if '2016' in era and 'pre' in era : 
        eras ='2016preVFP'
    if '2016' in era and 'post' in era : 
        eras ='2016postVFP'
    if '2016' in era and 'post' not in era  and 'pre' not in era: 
        eras ='2016postVFP'

    opts.sampleFile = 'samples_{0:s}_2l.dat'.format(eras)
    print 'will read Datasets from ', opts.sampleFile

    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':16.9777, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.351, '2016postVFP':16.9777,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    lumi = lumis[era]
    yields={}
    print 'Going to load DATA and MC trees...'
    if doDY:
        if doee:
            channel = 'ElEl'
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
            dyDatasetsNLO = ['DYJetsToLLM50NLO', 'DYJetsToLLM10to50']


            ewDatasets = ['ZZZ',  'WZTo2Q2L', 'WZTo3LNu', 'WWTo2L2Nu', 'WWW',  'WWZ', 'WZZ', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017

            #if '2016' in era : ewDatasets = ['WW', 'WZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']
            if '2016' in era : ewDatasets =  ['ZZZ', 'WWZ_ext1',  'WZTo2Q2L', 'WZTo3LNu', 'WWTo2L2Nu', 'WWW',  'WWZ', 'WZZ', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            #ewk1Datasets = ['W1JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            #ewk2Datasets = ['W2JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk3Datasets = ['W3JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk4Datasets = ['W4JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewkDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']
            ewkDatasets = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J']
            ewkNLODatasets = ['WJetsToLNu_NLO']
            ewkDatasets = ['WJetsToLNu']
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']
            #ewkAllDatasets = ['WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']


            #daDatasets = [ 'EGamma_Run2018A', 'EGamma_Run2018B', 'EGamma_Run2018C', 'EGamma_Run2018D']  
            daDatasets = [ 'SingleElectron_Run2017B','SingleElectron_Run2017C', 'SingleElectron_Run2017D', 'SingleElectron_Run2017E', 'SingleElectron_Run2017F']  
            #daDatasets = [ 'DoubleEG_Run2017B','DoubleEG_Run2017C', 'DoubleEG_Run2017D', 'DoubleEG_Run2017E', 'DoubleEG_Run2017F']  

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
            channel = 'MuMu'
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
            dyDatasetsNLO = ['DYJetsToLLM50NLO', 'DYJetsToLLM10to50']
            #ewDatasets = ['WW', 'WZTo3LNu', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            ewDatasets = ['WW', 'ZZZ',  'WZTo2Q2L', 'WZTo3LNu', 'WWTo2L2Nu', 'WWW',  'WWZ', 'WZZ', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017

            #if '2016' in era : ewDatasets = ['WW', 'WZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']
            if '2016' in era : ewDatasets =  ['WW', 'ZZZ', 'WWZ_ext1',  'WZTo2Q2L', 'WZTo3LNu', 'WWTo2L2Nu', 'WWW',  'WWZ', 'WZZ', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            ewk1Datasets = ['W1JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk2Datasets = ['W2JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk3Datasets = ['W3JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewk4Datasets = ['W4JetsToLNu']#, 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewkDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']
            ewkDatasets = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J']
            ewkNLODatasets = ['WJetsToLNu_NLO']
            #ewkDatasets = ['WJetsToLNu_0J','WJetsToLNu_1J','WJetsToLNu_2J']
            #ewkDatasets = ['WJetsToLNu', 'W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu']
            ewkDatasets = ['WJetsToLNu']
            #ewkAllDatasets = ['WJetsToLNu']
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']



            daDatasets = [ 'SingleMuon_Run2017B','SingleMuon_Run2017C', 'SingleMuon_Run2017D', 'SingleMuon_Run2017E', 'SingleMuon_Run2017F']  
            #daDatasets = [ 'DoubleMuon_Run2017B','DoubleMuon_Run2017C', 'DoubleMuon_Run2017D', 'DoubleMuon_Run2017E', 'DoubleMuon_Run2017F']  
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
        #treeST = Sample.Tree(helper.selectSamples(opts.sampleFile, stDatasets, 'STOP'), 'STOP'  , 0)
        treeDY = Sample.Tree(helper.selectSamples(opts.sampleFile, dyDatasets, 'DY'), 'DY'  , 0, channel, isLocal)
        treeDYnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, dyDatasetsNLO, 'DYnlo'), 'DYnlo'  , 0, channel, isLocal)
        treeEW = Sample.Tree(helper.selectSamples(opts.sampleFile, ewDatasets, 'EW'), 'EW'  , 0, channel, isLocal)
        #treeEWK = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK'), 'EWK'  , 0, channel, isLocal)

        #treeEWKAll = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkAllDatasets, 'EWK'), 'EWK'  , 0, channel, isLocal, True)

        #treeEWKNLO = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkNLODatasets, 'EWKNLO'), 'EWKNLO'  , 0, channel, isLocal)
        #treeEWK1 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk1Datasets, 'EWK1'), 'EWK1'  , 0, channel, isLocal)
        #treeEWK2 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk2Datasets, 'EWK2'), 'EWK2'  , 0, channel, isLocal)
        #treeEWK3 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk3Datasets, 'EWK3'), 'EWK3'  , 0, channel, isLocal)
        #treeEWK4 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk4Datasets, 'EWK4'), 'EWK4'  , 0, channel, isLocal)
        #treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasets, 'QCD'), 'QCD'  , 0, channel, isLocal)
        #treeQCDPt = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPt, 'QCD'), 'QCD'  , 0, channel, isLocal)
        #treeQCDPtBins = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPtBins, 'QCD'), 'QCD'  , 0, channel, isLocal)
        #treeEWKmcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWKmcnlo'), 'EWKmcnlo'  , 0)
        #treeEWK1mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK1mcnlo'), 'EWK1mcnlo'  , 0)
        #treeEWK2mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK2mcnlo'), 'EWK2mcnlo'  , 0)
        #treeQCDPt = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdPtDatasets, 'QCD'), 'QCD'  , 0)

        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'DA'), 'DATA', 1, channel, isLocal)
        #mcTrees = [  treeTT, treeEWK,  treeDY, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK, treeEWK1, treeEWK2, treeEWK3, treeEWK4]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        mcTrees = [ treeEW, treeTT, treeDY]   
        #mcTrees = [ treeDY]   
        #if 'NLO' in str(opts.ExtraTag) : mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]   

        #mcTrees = [ treeDY, treeQCD, treeEWK]   
        #mcTrees = [ treeDY, treeQCD,  treeTT, treeEW, treeEWKNLO]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKmcnlo]   
        #mcTrees = [ treeDY, treeEWK]   
        #mcTreesQCD = [ treeQCD]   
        #mcTrees = [ treeEWK]   
        inn = str(opts.ExtraTag).lower()
        if 'data' not in inn : treeDA =[]
        mcTrees = []
        if 'dy' in inn  : mcTrees = [treeDY]
        if 'dynlo' in inn  : mcTrees = [treeDYnlo]
        if 'singlet' in inn  : mcTrees = [treeST]
        if 'top' in inn  : mcTrees = [treeTT]
        if 'qcd' in inn  : mcTrees = [treeQCD]
        if 'ewk' in inn  : mcTrees = [treeEWKAll]
        if 'ewknlo' in inn  : mcTrees = [treeEWKNLO]
        if 'ew' in inn and 'ewk' not in inn : mcTrees = [treeEW]
        if 'allmc' in inn : mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]
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
    doQCD = int(opts.DoQCD)
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
            #jetCut = " ( nMuon==1 && njets >=0  && pt_1> 27 && (isGlobal_1>0 || isTracker_1>0) && fabs(eta_1)<2.4 && fabs(d0_1)<0.045 && fabs(dZ_1)<0.2 && isTrig_1>0 &&  iso_1 < 0.15 && mediumId_1 >0 && nbtagT==0 )"
            givein ='{0:s}'.format(str(opts.varr))

            newname = givein
            newname = str(givein).replace(":", "_vs_")
            if 'Smear' in givein and 'data' in inn  : 
                print 'need to FIX SMEARRRRRRRRRRRRRRRRRRRRRRRRRRRRRR', givein, inn
                givein = givein.replace("Smear", "")
            docat='2'
            if doee : docat='1'
            nLep = 'nMuon'


            jetcut='0'
            wtmasscut='80'
            extracut=''
            puppicut=''
            losthits="1"
            njetsSyst=''
            tagname = str(opts.ExtraTag).lower()
            PUw='nom'
            if 'puup' in tagname : PUw = 'up'
            if 'pudown' in tagname : PUw = 'down'

            if 'njet' in givein.lower() : jetcut='-1'
            if 'njetsgeq0' in str(opts.ExtraTag).lower() : jetcut='>=0'
            if 'njetsgeq1' in str(opts.ExtraTag).lower() : jetcut='>=1'
            if 'njetsgincl' in str(opts.ExtraTag).lower() : jetcut='>=0'
            if 'njetsgt1' in str(opts.ExtraTag).lower() : jetcut='>1'
            if 'njetsgt0' in str(opts.ExtraTag).lower() : jetcut='>0'
            if 'hitslt1' in str(opts.ExtraTag).lower() : losthits='1'
            if 'metwmass' in givein.lower() : wtmasscut='0'
             
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
            #if 'nobtag' in tagname : btagcut="T"
            drcutstr = "dRMETCorGood_T1J1"+extracut  
            if 'puppi' in givein.lower() :drcutstr = "dRPuppiMETCorGood_J1"+extracut
            drcut= ">=0.0"
            if 'dr' in tagname : drcut = ">=0.5"
            if 'both' in tagname : drcut = ">=0.5 && "+drcutstr + "<=3.5"
            photonr9='0.9'
            if 'photon_r9_1' in givein.lower() : photonr9='0.8'



            #extracut = ''
            if 'puppi' in givein.lower() : puppicut='Puppi'

	    #jetCutMu = " (nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15  &&  fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]> {1:s}  && nbtagL[0]==0.0 && cat=={0:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut)



	    #jetCutEl = " (nElectron[0]==2 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 &&  fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&njets[0]> {1:s}   && nbtagL[0]==0.0 && Electron_convVeto[0] > 0 && Electron_lostHits[0]<{5:s} ".format(docat, jetcut, wtmasscut, extracut, puppicut, losthits)

	    jetCutMu = " (nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15  && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 && fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets{3:s}[0] {1:s}  && nbtagL[0]==0.0 && cat=={0:s} ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut)

	    jetCutEl = " ( nElectron[0]==2 && Flag_BadPFMuonDzFilter[0]==1  &&  !(fabs(eta_1[0])>1.4442 &&  fabs(eta_1[0])<1.5660) && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 &&   !(fabs(eta_2[0])>1.4442 &&  fabs(eta_2[0])<1.5660) && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 &&  fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s} && njets{3:s}[0] {1:s}   && nbtagL[0]==0.0 && Electron_convVeto[0] > 0 && Electron_lostHits[0]<{5:s} ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, losthits)


            jetCut= jetCutMu
            if doee : jetCut= jetCutEl

            jetCutInvIso = " (nMuon==1 && pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==2 &&  tightId_1[0] >0   &&  fabs(q_1[0])==1 &&  iso_1[0] > .15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets[0]<20 && METWTmass[0]>0 && isStandalone_1[0]>0 && nbtagL[0]==0"

            jetCutInvIso = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] > .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat=={0:s} && nbtagL[0]==0".format(docat)

            #jetCut +=  "  && pt_2> 29 && (isGlobal_2>0 || isTracker_2>0) && fabs(eta_2)<2.4 && fabs(dZ_2)<0.2 && fabs(d0_2)<0.045 &&  tightId_2 >0   &&  iso_2 <= 0.10"

            if 'pult10' in tagname : jetCut  = jetCut + " && nPVGood[0]<10"
            if 'pu10to20' in tagname : jetCut  = jetCut + " && nPVGood[0]<20 && nPVGood>=10"
            if 'pu20to30' in tagname : jetCut  = jetCut + " && nPVGood[0]<30 && nPVGood>=20"
            if 'pu30to40' in tagname : jetCut  = jetCut + " && nPVGood[0]<40 && nPVGood>=30"
            if 'pu40to50' in tagname : jetCut  = jetCut + " && nPVGood[0]<50 && nPVGood>=40"
            if 'pugeq50' in tagname : jetCut  = jetCut + " && nPVGood[0]>=50 "
            if 'pugeq40' in tagname : jetCut  = jetCut + " && nPVGood[0]>=40 "
            if 'isocut' in tagname :  jetCut  = jetCut + " && iso_1 <=0.01"
            if 'isocuttight' in tagname :  jetCut  = jetCut + " && iso_1 <=0.005"

            print color.blue+'************************************************************************************************'+color.end
            print 'jetCut', jetCut
            print 'loading variable %s '%(var)
            # for all the variables with some met in them, we need to run over the jec/unclustered energy to get the errors, that is why there is some nasty repeating of lines below, and both the emt_pt and met_phi is needed for the uPara and uPerp, and the justMET, doUperp and doUpara are set, along with some options used in the plotting, definitions of the option can be found in the include/Canvas.py where all the plotting style is set
            if var == 'MET_T1_pt' or var == 'MET_pt':
                varTitle    = 'p_{T}^{miss} [GeV]';justMET = True;
                met = ['PuppiMET_pt']
                #double dphi = fabs(fabs(fabs(MuonsPhi[0]-MET_phi)-TMath::Pi())-TMath::Pi());
                #transvMass = sqrt(2*MuonsPt[0]*MET_pt*(1-cos(dphi)));
                met = ['DphilMET']
                met = ['njets']
                met = ['MET_T1_pt']
                met = ['METWTmass']
                met = ['METWmass']
                met = ['DphilMET']
                met = ['DphiWMET']
                if 'boson_pt' in givein.lower() : varTitle    = 'q_{T} [GeV]'
                if 'boson_phi' in givein : varTitle    = 'q_{#phi}'
                if 'PuppiMETmTmass' in givein : varTitle    = 'm_{T} [GeV]'
                if 'njets' in givein : varTitle    = 'njets'
                if 'DphiWMET' in givein : varTitle    = '#Delta#Phi(W,p_{T}^{miss})'
                if 'DphilMET' in givein : varTitle    = '#Delta#Phi(#mu,p_{T}^{miss})'
                if 'PuppiMET' in givein : varTitle    = 'p_{T}^{miss}'
                if 'wtmass' in givein.lower() : varTitle    = 'W_{T} [GeV]'
                if 'wmass' in givein.lower() : varTitle    = 'W [GeV]'
                if 'pt_1' in givein : varTitle    = 'p_{T}(#mu)'
                if 'eta_1' in givein : varTitle    = '#eta(#mu)'
                if 'phi_1' in givein.lower() : varTitle    = '#Phi(#mu)'
                if 'phi' in givein.lower() : varTitle    = '#Phi'
                if 'OQt' in givein.lower() : givein = givein.replace("OQt","/boson_pt")
                met = ['{0:s}'.format(str(givein))]

                #met = ['MET_T1_pt', 'MET_T1_ptJERUp', 'MET_T1_ptJERDown','MET_T1_ptJESUp', 'MET_T1_ptJESDown', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredDown']
                if 'all' in givein :
                    if 'allmet' == givein.lower() : met = ['MET_T1_pt', 'MET_T1_ptJESUp', 'MET_T1_ptJESDown', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredDown']
                    if 'allpuppi' == givein.lower() : met=['PuppiMET_pt', 'PuppiMET_ptJESUp', 'PuppiMET_ptJESDown', 'PuppiMET_ptUnclusteredUp', 'PuppiMET_ptUnclusteredDown']
                    if 'boson_pt' in givein.lower(): met=['boson_pt', 'boson_ptJESUp', 'boson_ptJESDown', 'boson_ptUnclusteredUp', 'boson_ptUnclusteredDown']
                print 'this is the variable=============>', met

                #met = ['{0:s}'.format(makeUPerp(MET_T1_pt, MET_T1_phi, boson_pt, boson_phi))]
                if 'u_par' in str(opts.varr) or 'u_perp' in str(opts.varr) : varTitle =  'u_{||} + q_{T} [GeV]';justMET = True;
                
                
            tmp_histo = 0
            histo_err = 0
            tmp_full = 0
            tmp_fullMCInvIso = 0
            tmp_fullQCDInvIso = 0
            
            fOut= TFile("plotS_{0:s}_{1:s}_{2:s}_{3:s}.root".format(str(era),str(inn), newname, str(channel)), "recreate")
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
                    print '------------------------------------------->', lumi, var, Variable, reg.bins[reg.rvars.index(var)], "", varTitle, doNPV, isLog
                    if ":" not in Variable : data_hist = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, doNPV, isLog)
                    else : data_hist= treeDA.getTH2F(lumi, var,  Variable, 20, 0,200, 20, 0, 200, cuts.Add(cut, jetCut) , "", "qT (GeV)", varTitle)
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
                    data_histInvIso = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, doNPV, isLog)
		    for itree, tree in  enumerate(mcTrees):
			ind = 0
			cuts = CutManager.CutManager()
			treename = tree.name.lower()
			print 'with  %s for QCD kfactor finding' %treename
			print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV
			
			if 'qcd' not in treename : tmp_fullMCInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, doNPV, isLog)
			if 'qcd' in treename :     tmp_fullQCDInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , inn, varTitle, doNPV, isLog)


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
                        print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV, 'from treename', treename
                        #tmp_full= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                        if ":" not in Variable : tmp_full= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, doNPV, isLog)
                        if ":" in Variable : 
                            print 'will try to read a TH2 histo.....'
                            tmp_full= tree.getTH2F(lumi, var,  Variable, 20, 0,200, 20, 0, 200, cuts.Add(cut, jetCut) , "", "qT (GeV)", varTitle)
                        
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
                            tmp_full.SetTitle("W+jets")
                        if treename == 'ewk':
                            tmp_full.SetTitle("W+jets (LO)")

                        if treename == 'ewknlo':
                            tmp_full.SetTitle("W+jets (NLO)")

                        if treename == 'dy':
                            if doee:
                                tmp_full.SetTitle("Z/#gamma^{*} #rightarrow ee")
				if 'nlo' in treename :
				    tmp_full.SetTitle("Z/#gamma^{*} #rightarrow ee (NLO)")
                            else:                                    
                                tmp_full.SetTitle("Z/#gamma^{*} #rightarrow #mu#mu")
				if 'nlo' in treename :
				    tmp_full.SetTitle("Z/#gamma^{*} #rightarrow #mu#mu (NLO)")
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
			mnew = m.replace(":", "_vs_")
                        print 'should have the correct name ????????????????????????????', tmp_full.GetName(), mnew, m
                        tmp_histo.Write('histo_'+treename+'_'+mnew)

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
                            histo_err= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, doNPV, isLog)
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
		    plot_var = Canvas.Canvas("test/paper/%s_%s%s%s%s_doQCD_%s%s_%sLog"%(newname,reg.name, channel, puname,str(era), str(int(doQCD)), str(opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])
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
                #if ":" in Variable or "vs" in Variable : noRatio = True

		if noRatio:
		    plot_var.save(1, lumi, isLog, "", "", "", varTitle, option, "", 0)
                    #def save(self, legend, lumi, log,chisquare, value, title, option, integral, fromFit): 
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
