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
    (opts, args) = parser.parse_args()
    doDY = True
    doNPV = True
    doee = True
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : doee = False
    if 'el' in str(opts.Channel.lower()) : doee = True
    if doee :   channel = 'ElEl'
    else :   channel = 'MuMu'
    era = str(opts.Year)
    opts.sampleFile = 'samples_{0:s}.dat'.format(era)
    
    ee = era
    
    if 'dry' not in era : opts.sampleFile = 'samples_{0:s}_v2.dat'.format(era[:4], channel)
    else : opts.sampleFile = 'samples_2017_v2.dat'.format(era[:4])
    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':35.93, '2017':41.48, '2018':59.83, '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
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

            stDatasets = ['ST_s-channel_antitop', 'ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_s-channel_antitop', 'ST_t-channel_top','ST_tW_antitop', 'ST_tW_top']
 
            ttDatasets += stDatasets

            #ttDatasets = ['ST_s-channel_antitop', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            dyDatasets = ['DYJetsToLLM50', 'DYJetsToLLM10to50']
            #dyyDatasets = ['DYJetsToLLM10to50']
            #dyDatasets = ['DYJetsToLLM50']
            #dyDatasets = ['DYJetsToLLM50']
            ewDatasets = ['WW', 'WWW', 'WZZ']
            ewDatasets = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            #ewDataset = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo4L'] #ZZTo2Q2L only for 2017
            #ewDatasets = ['WW', 'WWW', 'WZZ']
            #ewkDatasets = ['WWTo2L2Nu_mm', 'WZTo2L2Q_mm', 'WZTo3LNu_amcatnlo_mm', 'ZZTo4L_mm', 'ZZTo2L2Nu_mm', 'ZZTo2L2Q_mm',  'WWW_mm', 'WWZ_mm', 'WZZ_mm', 'ZZZ_mm' ]
            #ewkDatasets = ['WJetsToLNu']
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
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']


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

            stDatasets = ['ST_s-channel_antitop', 'ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top']
            #stDatasets = ['ST_s-channel_antitop', 'ST_t-channel_top','ST_tW_antitop', 'ST_tW_top']
 
            ttDatasets += stDatasets

            #ttDatasets = ['ST_s-channel_antitop', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            dyDatasets = ['DYJetsToLLM50', 'DYJetsToLLM10to50']
            #dyyDatasets = ['DYJetsToLLM10to50']
            #dyDatasets = ['DYJetsToLLM50']
            #dyDatasets = ['DYJetsToLLM50']
            ewDatasets = ['WW', 'WWW', 'WZZ']
            ewDatasets = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L', 'WGToLNuG']# only for 2017
            #ewDataset = ['WW', 'WZ', 'WZZ', 'WWW', 'ZZTo2L2Nu', 'ZZTo4L'] #ZZTo2Q2L only for 2017
            #ewDatasets = ['WW', 'WWW', 'WZZ']
            #ewkDatasets = ['WWTo2L2Nu_mm', 'WZTo2L2Q_mm', 'WZTo3LNu_amcatnlo_mm', 'ZZTo4L_mm', 'ZZTo2L2Nu_mm', 'ZZTo2L2Q_mm',  'WWW_mm', 'WWZ_mm', 'WZZ_mm', 'ZZZ_mm' ]
            #ewkDatasets = ['WJetsToLNu']
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
            ewkAllDatasets = ['W1JetsToLNu','W2JetsToLNu','W3JetsToLNu','W4JetsToLNu', 'WJetsToLNu']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']

            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']



            #daDatasets = [ 'SingleMuon_Run2018A', 'SingleMuon_Run2018B', 'SingleMuon_Run2018C', 'SingleMuon_Run2018D']  
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

            #daDatasets = [ 'SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017F']  
            #daDatasets = [ 'SingleMuon_Run2017B']  
        print 'the lumito be used is ',lumi

        treeTT = Sample.Tree(helper.selectSamples(opts.sampleFile, ttDatasets, 'TOP'), 'TOP'  , 0, channel)
        ##treeST = Sample.Tree(helper.selectSamples(opts.sampleFile, stDatasets, 'STOP'), 'STOP'  , 0)
        treeDY = Sample.Tree(helper.selectSamples(opts.sampleFile, dyDatasets, 'DY'), 'DY'  , 0, channel)
        treeEW = Sample.Tree(helper.selectSamples(opts.sampleFile, ewDatasets, 'EW'), 'EW'  , 0, channel)
        treeEWK = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK'), 'EWK'  , 0, channel)

        treeEWKAll = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkAllDatasets, 'EWK'), 'EWK'  , 0, channel, True)

        treeEWKNLO = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkNLODatasets, 'EWKNLO'), 'EWKNLO'  , 0, channel)
        #treeEWK1 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk1Datasets, 'EWK1'), 'EWK1'  , 0, channel)
        #treeEWK2 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk2Datasets, 'EWK2'), 'EWK2'  , 0, channel)
        #treeEWK3 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk3Datasets, 'EWK3'), 'EWK3'  , 0, channel)
        #treeEWK4 = Sample.Tree(helper.selectSamples(opts.sampleFile, ewk4Datasets, 'EWK4'), 'EWK4'  , 0, channel)
        treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasets, 'QCD'), 'QCD'  , 0, channel)
        #treeQCDPt = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPt, 'QCD'), 'QCD'  , 0, channel)
        #treeQCDPtBins = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPtBins, 'QCD'), 'QCD'  , 0, channel)
        #treeEWKmcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWKmcnlo'), 'EWKmcnlo'  , 0)
        #treeEWK1mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK1mcnlo'), 'EWK1mcnlo'  , 0)
        #treeEWK2mcnlo = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK2mcnlo'), 'EWK2mcnlo'  , 0)
        #treeQCDPt = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdPtDatasets, 'QCD'), 'QCD'  , 0)

        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'DA'), 'DATA', 1, channel)
        #mcTrees = [  treeTT, treeEWK,  treeDY, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK, treeEWK1, treeEWK2, treeEWK3, treeEWK4]   
        mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKAll]   
        if 'NLO' in str(opts.ExtraTag) : mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKNLO]   

        #mcTrees = [ treeDY, treeQCD, treeEWK]   
        #mcTrees = [ treeDY, treeQCD,  treeTT, treeEW, treeEWKNLO]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWKmcnlo]   
        #mcTrees = [ treeDY, treeEWK]   
        #mcTreesQCD = [ treeQCD]   
        #mcTrees = [ treeEWK]   
        boson = 'boson_pt'
        boson_phi = 'boson_phi'
    else:
        qcdDatasets = ['QCD_HT200to300_ext', 'QCD_HT300to500_ext', 'QCD_HT500to700_ext',  'QCD_HT700to1000_ext','QCD_HT1000to1500_ext', 'QCD_HT1500to2000_ext', 'QCD_HT2000toInf_ext']
        #gjetsDatasets = ['GJets_HT40to100_ext','GJets_HT100to200', 'GJets_HT400to600_ext','GJets_HT600toInf_ext' ]
        gjetsDatasets = ['GJets_HT40to100_ext','GJets_HT100to200', 'GJets_HT200to400_ext', 'GJets_HT400to600_ext','GJets_HT600toInf_ext' ]
        ewkDatasets =  ['TGJets_ext','TTGJets',  'ZGTo2LG_ext','ZGTo2NuG','WGToLNuG_amcatnlo_ext',   'WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400_ext','WJetsToLNu_HT400to600_ext','WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT800to1200_ext', 'WJetsToLNu_HT2500toInf_ext']
        #ewkDatasets =  ['TGJets_ext', 'TTGJets', 'WGToLNuG_amcatnlo_ext', 'ZGTo2LG_ext','ZGTo2NuG',  'WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400_ext','WJetsToLNu_HT400to600_ext','WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT800to1200_ext', 'WJetsToLNu_HT2500toInf_ext']
        #daDatasets = ['SinglePhoton_Run2016C_03Feb2017']
        daDatasets = ['SinglePhoton_Run2016B_03Feb2017_v2', 'SinglePhoton_Run2016C_03Feb2017', 'SinglePhoton_Run2016D_03Feb2017', 'SinglePhoton_Run2016E_03Feb2017', 'SinglePhoton_Run2016F_03Feb2017', 'SinglePhoton_Run2016G_03Feb2017', 'SinglePhoton_Run2016H_03Feb2017_v2']
        run_str =''
        channel = '' 
        treeQCD =   Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasets, 'QCD'), 'QCD', 0)
        treeGJETS = Sample.Tree(helper.selectSamples(opts.sampleFile, gjetsDatasets, 'GJETS'),'GJETS', 0)
        treeEWK =   Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWK'), 'EWK', 0)
        treeDA =    Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'DA'), 'DATA', 1)
        mcTrees = [  treeEWK, treeQCD, treeGJETS]  
        boson = 'gamma_pt'
        boson_phi = 'gamma_phi'
        lumi = lumis[era]
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
        #doVariables = ['nVert']
        #doVariables = ['zll_mass']
        #doVariables = ['met_sumEt']
        #doVariables = ['lep_pt1', 'lep_pt2', 'lep_eta1', 'lep_eta2']
        #doVariables = ['zll_pt']
        #doVariables = ['met_uPerp', 'met_uPara']
        #doVariables = ['met_uPerp', 'met_uPara','metRaw_uPerp',  'metRaw_uPara']
        doVariables = ['MET_T1_pt']

        #doVariables = ['zll_pt', 'MET_pt', 'met_uPerp', 'met_uPara']
        #doVariables = ['met_uParaOverQt']
        #doVariables = ['MET_pt', 'MET_pt_0jet','MET_pt_1jet', 'met_rawPt', 'met_rawPt_0jet',  'met_rawPt_1jet']
        #doVariables = [ 'met_uPerp', 'met_uPerp_0jet', 'met_uPerp_1jet', 'met_uPara',  'met_uPara_0jet', 'met_uPara_1jet','metRaw_uPerp', 'metRaw_uPerp_0jet','metRaw_uPerp_1jet', 'metRaw_uPara', 'metRaw_uPara_0jet','metRaw_uPara_1jet']
        #doVariables = ['nVert', 'zll_pt', 'met_x', 'met_x_0jet','met_x_1jet',  'met_y','met_y_0jet', 'met_y_1jet','met_sumEt', 'met_sumEt_0jet','met_sumEt_1jet',  'met_rawSumEt',  'met_rawSumEt_0jet',  'met_rawSumEt_1jet', 'met_uPerp', 'met_uPerp_0jet', 'met_uPerp_1jet', 'met_uPara',  'met_uPara_0jet', 'met_uPara_1jet', 'MET_pt', 'MET_pt_0jet','MET_pt_1jet', 'met_rawPt', 'met_rawPt_0jet',  'met_rawPt_1jet','metRaw_uPerp', 'metRaw_uPara', 'met_sig','met_sig_1jet']
        #binnings    = [massbin]
        #binnings    = [bosonPtbin]
        #binnings    = [sumEtbin]
        binnings    = [bosonPtbin, bin1, bin2, bin2]
        #binnings = [bin2]
        #binnings = [bin2, bin2]
        #binnings    = [nbin]
        #binnings    = [bosonPtbin]
        #binnings    = [bin1, bin1, bin1, bin1,bin1, bin1]
        #binnings    = [bin2, bin2, bin2, bin2]
        #binnings    = [bin1, bin1, bin1, bin1, bin2, bin2, bin2, bin2, bin2, bin2, bin2, bin2]
        #binnings    = [bin2, bin2, bin2, bin2, bin2, bin2, sumbin,sumbin,sumbin,sumbin,sumbin,sumbin]
        #binnings    = [bin1, bin1, bin1, bin1, bin1, bin1]
        dependence = 'zll_pt'
        ZtoLL = Region.region('Zto',
                           cuts.leps(), doVariables, dependence, 'MET_T1_pt', binnings, True)
        regions.append(ZtoLL)                                                                                   
        
    else:
        #doVariables = [ 'gamma_pt','MET_pt',  'met_rawPt']
        #doVariables = ['met_sumEt']
        #doVariables = ['nVert']
        #doVariables = [ 'gamma_pt']
        #doVariables = [ 'MET_pt', 'met_rawPt','metPuppi_rawPt']
        doVariables = ['gamma_pt', 'MET_pt', 'met_uPerp', 'met_uPara']
        #doVariables = [ 'met_x',  'met_y','met_sumEt',  'met_rawSumEt']
        #doVariables = [  'met_uPara']
        #doVariables = ['MET_pt', 'met_rawPt','met_uPerp', 'met_uPara','metRaw_uPerp',  'metRaw_uPara']
        #doVariables = [  'met_uParaOverQt', 'met_uParaNoQt']
        #doVariables = [ 'metPuppi_pt']
        #doVariables = ['gamma_pt','MET_pt',  'met_rawPt', 'metPuppi_rawPt', 'metPuppi_pt', 'met_uPerp', 'met_uPara','metRaw_uPerp',  'metRaw_uPara','metPuppi_uPerp', 'metPuppi_uPara', 'metPuppiRaw_uPerp', 'metPuppiRaw_uPara']
        #doVariables = [ 'metPuppi_uPerp','metPuppi_uPara']
        #binnings    = [binDebug]
        binnings    = [gammaPtbin, bin1, bin2,bin2]
        #binnings    = [nbin]
        #binnings    = [gammaPtbin]
        #binnings    = [sumEtbin]
        #binnings    = [bin2, bin2]
        #binnings    = [gammabin,bin1,  bin1]
        #binnings    = [gammabin,bin1,  bin1, bin1, bin1, bin2, bin2, bin2, bin2, bin2, bin2, bin2, bin2]
        #binnings    = [bin1, bin2, bin2]
        #binnings    = [bin2, bin2, sumbin,sumbin]
        #binnings    = [bin2, bin2, bin2, bin2, bin2, bin2]
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
            mc_histo = 0; histo_err = 0; mc_up = 0; mc_down = 0; mc_jerup=0; mc_jerdown=0;mc_jesup = 0; mc_jesdown = 0; mc_unclUp = 0; mc_unclDown = 0; mc_stack = r.THStack();
            cut = reg.cuts
            met=['MET_T1_pt']
            phi=['MET_T1_phi']
            if doDY:
                leg = [0.65, 0.6, 0.81, 0.9]
                #leg = [0.7, 0.6, 0.88, 0.9]
            else:
                leg = [0.65, 0.6, 0.81, 0.9]
            #jetCut = " ( nMuon==1 && njets >=0  && pt_1> 27 && (isGlobal_1>0 || isTracker_1>0) && fabs(eta_1)<2.4 && fabs(d0_1)<0.045 && fabs(dZ_1)<0.2 && isTrig_1>0 &&  iso_1 < 0.15 && mediumId_1 >0 && nbtagT==0 )"
            #jetCut = " ( nMuon==1 && nTau==0 && njets >=0  && pt_1> 29 && (isGlobal_1>0 || isTracker_1>0) && fabs(eta_1)<2.4 && fabs(dZ_1)<0.2 && fabs(d0_1)<0.045 && isTrig_1>0 &&  iso_1 < 0.15 && tightId_1 >0 && nbtagT==0 )"
            #jetCut = " ( nMuon==1 && njets >=0  && pt_1> 29 && (isGlobal_1>0 || isTracker_1>0) && fabs(eta_1)<2.4 && fabs(dZ_1)<0.2 && fabs(d0_1)<0.045 && isTrig_1!=0 &&  tightId_1 >0 && nbtagT==0  ) &&  iso_1 <= 0.15"
            givein ='{0:s}'.format(str(opts.varr))

            jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==1 &&  tightId_1[0] >0 && nbtagT[0]==0   &&  iso_1[0] <= 0.15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]<20 && METWTmass[0]>0 && tightCharge_1[0]>1 && highPurity_1[0]>0 && isStandalone_1[0]>0 && hasTau[0]==0 && hasPhoton[0]==0"

            #jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==1 &&  tightId_1[0] >0  &&  iso_1[0] <= 0.15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]<20 && METWTmass[0]>0 && tightCharge_1[0]>1 && highPurity_1[0]>0 && isStandalone_1[0]>0 && nbtagL[0]==0 && hasTau[0]==0 && hasPhoton[0]==0"
            jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==1 &&  tightId_1[0] >0  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>-1 && isStandalone_1[0]>0 && nbtagL[0]==0 && hasPhoton[0]==0 && hasTau[0]==0"

            docat='1'
            if doee : docat='2'
            nLep = 'nMuon'

            jetCut = " (nMuon==1 && pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && Flag_BadPFMuonDzFilter[0]==1 && isTrig_1[0]==3 &&  tightId_1[0] >0  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2  && nbtagL[0]==0 && njets>-1 && cat=={0:s} && VetoElectron==0 && VetoPhoton==0".format(docat)
            
            jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && Flag_BadPFMuonDzFilter[0]==1 && isTrig_1[0]>0 &&  tightId_1[0] >0  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2  && nbtagL[0]==0 && njets>-1 && cat==1"

            jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && Flag_BadPFMuonDzFilter[0]==1 && isTrig_1[0]>0 &&  tightId_1[0] >0  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nMuon==1 && nbtagL[0]==0 && PFiso_1[0]==4".format(docat)

            jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&  nbtagL[0]==0 && PFiso_1[0]==4".format(docat)
            jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&  nbtagL[0]==0 && njets[0]>1".format(docat)
            jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&  nbtagL[0]==0 &&njets[0]>0 && METWTmass[0]>0".format(docat)
            jetCutEl = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nbtagL[0]==0 &&njets[0]>0 && PuppiMETWTmass[0] > 0".format(docat)

            if 'puppi' not in givein.lower() : 
                jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&  nbtagL[0]==0 &&njets[0]>0 && METWTmass[0]>80".format(docat)

                jetCutEl = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nbtagL[0]==0 &&njets[0]>0 && METWTmass[0] > 80".format(docat)

            else : 
                jetCutMu = " (nMuon[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} &&  nbtagL[0]==0 &&njets[0]>0 && PuppiMETWTmass[0]>80".format(docat)

                jetCutEl = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nbtagL[0]==0 &&njets[0]>0 && PuppiMETWTmass[0] > 80".format(docat)

            #jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==1 &&  tightId_1[0] >0  &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && njets[0]>-1 && isStandalone_1[0]>0 && nbtagL[0]==0  "
            
            jetCut= jetCutMu
            if doee : jetCut= jetCutEl

            jetCutInvIso = " (nMuon==1 && pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1[0]==2 &&  tightId_1[0] >0   &&  fabs(q_1[0])==1 &&  iso_1[0] > .15 && mediumPromptId_1[0]>0 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]<20 && METWTmass[0]>0 && isStandalone_1[0]>0 && nbtagL[0]==0"

            jetCutInvIso = " (nElectron[0]==1 && Flag_BadPFMuonDzFilter[0]==1  &&  fabs(q_1[0])==1 && iso_1[0] > .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat=={0:s} && nbtagL[0]==0".format(docat)

            #jetCut +=  "  && pt_2> 29 && (isGlobal_2>0 || isTracker_2>0) && fabs(eta_2)<2.4 && fabs(dZ_2)<0.2 && fabs(d0_2)<0.045 &&  tightId_2 >0   &&  iso_2 <= 0.10"
            #jetCut = " (pt_1[0]> 29 && (isGlobal_1[0]>0 || isTracker_1[0]>0) && fabs(eta_1[0])<2.4 && fabs(dZ_1[0])<0.2 && fabs(d0_1[0])<0.045 && isTrig_1==1 &&  tightId_1[0] >0 && nbtagT[0]==0   &&  mediumPromptId_1[0]>0 && nPVndof>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets<3 "
            
            #jetCut = "1"
            print color.blue+'************************************************************************************************'+color.end
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
                if 'phi_1' in givein : varTitle    = '#Phi(#mu)'
                if 'OQt' in givein : givein = givein.replace("OQt","/boson_pt")
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
                print met

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
                varTitle =  'u_{||}/q_{T} [GeV]';justMET = False;doUParaOverQt = True; 
                met = ['MET_pt']
                #met = ['MET_pt', 'MET_pt_JetEnUp', 'MET_pt_JetEnDown',  'MET_pt_JetResUp', 'MET_pt_JetResDown', 'MET_pt_UnclusteredEnUp', 'MET_pt_UnclusteredEnDown']
                phi = ['met_phi']
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
            for m in met:
                Variable = ""
                # here, either make the met, uPara or uPerp, and loop over all five types of met...
                if doUpara:
                    Variable = makeUPara(met[met.index(m)], phi[met.index(m)], boson, boson_phi)
                elif doUParaOverQt:
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
                if met.index(m) == 0:
                    #data_hist = treeDA.getTH1F(lumi, var+"_"+reg.name+'data'+str(met.index(m)), Variable, 110, -1.7, -0.3, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                    #data_hist = treeDA.getTH1F(lumi, var+"_"+reg.name+'data'+str(met.index(m)), Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                    varData = var
                    #if 'Up' in var or 'Down' in var : var.replace("_T1","")
                    print 'this is for data', var, 'bins', reg.bins[reg.rvars.index(var)]
                    data_hist = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV, isLog)
                    #data_hist.Scale(0.5)
		    d={'{0:s} tmp_full'.format(data_hist.GetName()):data_hist.Integral()}
		    yields.update(d)


                    print 'data ------->', data_hist.Integral()
                    #if (option == 'qtZ' or option =='qtG' or option == 'qtgamma'): 
                    #    data_hist.Scale(1,"width")
                    if doHighMetValues:
                        highMet = data_hist.FindLastBinAbove(0, 1)
                        print "high metbin data: ", highMet                 

                kfactor=1
                if doQCD and met.index(m) == 0: 
                    data_histInvIso = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV, isLog)
		    for itree, tree in  enumerate(mcTrees):
			ind = 0
			cuts = CutManager.CutManager()
			treename = tree.name.lower()
			print 'with  %s for QCD kfactor finding' %treename
			print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV
			
			if 'qcd' not in treename : tmp_fullMCInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV, isLog)
			if 'qcd' in treename :     tmp_fullQCDInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV, isLog)


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
                        #tmp_full= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable,  110, -1.7, -0.3, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                        print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV, 'from treename', treename
                        #tmp_full= tree.getTH1F(lumi, var+"_"+reg.name+treename+str(met.index(m)),  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV)
                        tmp_full= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV, isLog)
                        
                        if tmp_full.GetEntries()<0 : continue
                        if tmp_full.Integral<0 : 
                            print 'this has no meaningful entries... will skip it', tmp_full.GetName(), tmp_full.Integral()
                            continue
                        print ' histo has integral ', tmp_full.GetName(), tmp_full.Integral()
                        #if (option == 'qt' or option == "qtG" or option == "qtZ" or option == 'qtgamma'): 
                        #    tmp_full.Scale(1,"width")
                        tmp_full.SetFillColorAlpha(block.color, 0.5)
                        tmp_full.SetTitle(block.name)
                        if treename == 'gjets':
                            tmp_full.SetTitle("#gamma + jets")
                        if treename == 'qcd':
                            tmp_full.SetTitle("QCD multijet")
                            tmp_full.Scale(kfactor)
                        if treename == 'wjets':
                            tmp_full.SetTitle("W + jets")
                        if treename == 'ewk':
                            tmp_full.SetTitle("W + jets")

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
                            histo_err= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, doNPV, isLog)
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
            SetOwnership(tmp_histo, 0 )
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
		print "data mean ", data_hist.GetMean()
		#print 'stacking histograms...', mc_stack.GetIntegral()
		plot_var.addStack(mc_stack  , "hist" , 1, 1)

		#plot_var.addLatex (0.65, 0.55, 'Uncert.')
		if isSig:
		    plot_var.addHisto(f, "E,SAME"   , "#chi^{2} d.o.f. 2"  , "L", r.kBlack , 1, 0)
		plot_var.addHisto(data_hist, "E,SAME"   , "Data"  , "PL", r.kBlack , 1, 0)

		if noRatio:
		    plot_var.save(1,  1, lumi,  "", "", varTitle, option)
		else:
		    #data_hist = mc_histo
		    #met = ['MET_T1_pt', 'MET_T1_ptJESUp', 'MET_T1_ptJESDown','MET_T1_ptJERUp', 'MET_T1_ptJERUp', 'MET_T1_ptUnclusteredUp', 'MET_T1_ptUnclusteredUp']
		    #plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_unclUp, mc_unclDown, varTitle , option, run_str)
		    
		    for i in range(1, mc_histo.GetNbinsX()+1) : 
			mc_histo.SetBinError(i, mc_histo.GetBinError(i)*0.25)
		    #mc_jerup=mc_histo; mc_jerdown = mc_histo; mc_jesup = mc_histo; mc_jesdown = mc_histo;mc_unclUp = mc_histo; mc_unclDown = mc_histo
		    mc_jerup=mc_histo; mc_jerdown = mc_histo; 

		    plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle , option, run_str)
		    #plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle+"Int data"+str(data_hist.Integral()) , option, run_str)
            del plot_var
            del Variable
            print yields
            time.sleep(0.1)
            print color.blue+'********************************************DONE***************************************************'+color.end
