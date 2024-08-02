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
    dogjets = True
    channel = 'Gjets'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    inn = str(opts.ExtraTag).lower()
    IDWP = 'mvaID'
    if 'cutbased' in inn : IDWP = 'cutBased'
    #opts.sampleFile = 'samples_{0:s}_gjets.dat'.format(era[:4], channel)
     
    if '2016' in era and 'pre' in era : 
        eras ='2016preVFP'
    if '2016' in era and 'post' in era : 
        eras ='2016postVFP'
    if '2016' in era and 'post' not in era  and 'pre' not in era: 
        eras ='2016postVFP'

    opts.sampleFile = 'samples_{0:s}_gjets_{1:s}.dat'.format(eras,IDWP)
    #opts.sampleFile = 'samples_{0:s}_gjets.dat'.format(eras,IDWP)
    print 'will read Datasets from ', opts.sampleFile

    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':35.93, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.72, '2016postVFP':16.15,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    #pay attention! 2016=2016postVFP
    lumis={'2016':16.9777, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.72, '2016postVFP':16.15,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    lumi = lumis[era]



    yields={}
    print 'Going to load DATA and MC trees...'
    if doDY:
        if dogjets:
            channel = 'Gjets'
            lumi = lumis[era]
            run = era


            txDatasets = ['TGjets', 'TTGjets', 'TTGjets_ext1']
            topDatasets = ['ST_s-channel', 'ST_t-channel_top', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToSemiLeptonic', 'TTToHadronic', 'ttWJets']
            #txDatasets += topDatasets
            if '2017' in run or '2016' in run : txDatasets = ['TGjets', 'TTGjets']
            #txDatasets = ['TTGjets']
 

            #ttDatasets = ['ST_s-channel_antitop', 'ST_t-channel_antitop', 'ST_tW_antitop', 'ST_tW_top', 'TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic']
            ewkDatasets = ['WJetsToLNu_NLO']

            ewnloDatasets = ['WGToLNuG']
            ewnloDatasets = ['WGToLNuG', 'ZGTo2NuG', 'ZNuNuGJets_PtG-130', 'ZLLGJets_PtG-15to130', 'ZLLGJets_PtG-130']
            ewDatasets = ['WG_PtG-130', 'WG_PtG-40To130', 'WGToLNuG', 'ZGTo2NuG', 'ZNuNuGJets_PtG-130', 'ZLLGJets_PtG-15to130', 'ZLLGJets_PtG-130']
            ewDatasets = ['WG_PtG-130', 'WG_PtG-40To130', 'ZGTo2NuG', 'ZNuNuGJets_PtG-130', 'ZLLGJets_PtG-15to130', 'ZLLGJets_PtG-130']
            ewDatasets = ['WG_PtG-130', 'WG_PtG-40To130',  'ZGTo2NuG', 'ZNuNuGJets_PtG-130', 'ZLLGJets_PtG-15to130', 'ZLLGJets_PtG-130']
            #if '2018' not in run : ewDatasets = ['WWG', 'WG_PtG-130', 'WG_PtG-40To130',  'ZGTo2NuG', 'ZNuNuGJets_PtG-130', 'ZLLGJets_PtG-15to130', 'ZLLGJets_PtG-130']
              
            gjetsDatasets = ['GJets_HT-40To100','GJets_HT-100To200', 'GJets_HT-200To400', 'GJets_HT-400To600', 'GJets_HT-600ToInf']

            qcdDatasets = ['QCD_HT50to100', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700',  'QCD_HT700to1000','QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']
            qcdmgDatasets = ['QCD_HT50to100MG', 'QCD_HT100to200MG', 'QCD_HT200to300MG', 'QCD_HT300to500MG', 'QCD_HT500to700MG',  'QCD_HT700to1000MG','QCD_HT1000to1500MG', 'QCD_HT1500to2000MG', 'QCD_HT2000toInfMG']


            #qcdDatasetsPt = [ 'QCD_Pt-20_MuEn']
            qcdDatasetsPtBins = [ 'QCD_Pt-1000_MuEn', 'QCD_Pt-15To20_MuEn', 'QCD_Pt-300To470_MuEn', 'QCD_Pt-470To600_MuEn', 'QCD_Pt-600To800_MuEn', 'QCD_Pt-80To120_MuEn', 'QCD_Pt-120To170_MuEn', 'QCD_Pt-170To300_MuEn', 'QCD_Pt-20To30_MuEn', 'QCD_Pt-30To50_MuEn', 'QCD_Pt-50To80_MuEn', 'QCD_Pt-800To1000_MuEn']


            #daDatasets = [ 'EGamma_Run2018A', 'EGamma_Run2018B', 'EGamma_Run2018C', 'EGamma_Run2018D']  
            daDatasets  =['SinglePhoton_Run2017B','SinglePhoton_Run2017C',  'SinglePhoton_Run2017D', 'SinglePhoton_Run2017E', 'SinglePhoton_Run2017F']
            if run =='2017B' : daDatasets = [ 'SinglePhoton_Run2017B']
            if run =='2017C' : daDatasets = [ 'SinglePhoton_Run2017C']
            if run =='2017D' : daDatasets = [ 'SinglePhoton_Run2017D']
            if run =='2017E' : daDatasets = [ 'SinglePhoton_Run2017E']
            if run =='2017F' : daDatasets = [ 'SinglePhoton_Run2017F']
            if run=='dry': daDatasets = txDatasets

            if run =='2018' : daDatasets = [ 'EGamma_Run2018B','EGamma_Run2018C', 'EGamma_Run2018D', 'EGamma_Run2018A']
            if run =='2018A' : daDatasets = [ 'EGamma_Run2018A']
            if run =='2018B' : daDatasets = [ 'EGamma_Run2018B']
            if run =='2018C' : daDatasets = [ 'EGamma_Run2018C']
            if run =='2018D' : daDatasets = [ 'EGamma_Run2018D']

            #if run =='2016' : daDatasets = [ 'SinglePhoton_Run2016Bv1_preVFP', 'SinglePhoton_Run2016Bv2_preVFP',  'SinglePhoton_Run2016C_preVFP',  'SinglePhoton_Run2016D_preVFP',  'SinglePhoton_Run2016E_preVFP',  'SinglePhoton_Run2016Fv2_preVFP',  'SinglePhoton_Run2016Fv1',  'SinglePhoton_Run2016G',  'SinglePhoton_Run2016H']
            if run =='2016preVFP' : daDatasets = [ 'SinglePhoton_Run2016Bv1_preVFP', 'SinglePhoton_Run2016Bv2_preVFP',  'SinglePhoton_Run2016C_preVFP',  'SinglePhoton_Run2016D_preVFP',  'SinglePhoton_Run2016E_preVFP',  'SinglePhoton_Run2016Fv2_preVFP']
            if run =='2016postVFP' : daDatasets = [ 'SinglePhoton_Run2016Fv1',  'SinglePhoton_Run2016G',  'SinglePhoton_Run2016H']
            if run =='2016' : daDatasets = [ 'SinglePhoton_Run2016Fv1',  'SinglePhoton_Run2016G',  'SinglePhoton_Run2016H']

            if run =='2016BpreVFP' : daDatasets = [ 'SinglePhoton_Run2016Bv1_preVFP', 'SinglePhoton_Run2016Bv2_preVFP']
            if run =='2016CpreVFP' : daDatasets = [ 'SinglePhoton_Run2016C_preVFP']
            if run =='2016DpreVFP' : daDatasets = [ 'SinglePhoton_Run2016D_preVFP']
            if run =='2016EpreVFP' : daDatasets = [ 'SinglePhoton_Run2016E_preVFP']
            if run =='2016FpreVFP' : daDatasets = [ 'SinglePhoton_Run2016Fv2_preVFP']
            if run =='2016F' : daDatasets = [ 'SinglePhoton_Run2016Fv1']
            if run =='2016G' : daDatasets = [ 'SinglePhoton_Run2016G']
            if run =='2016H' : daDatasets = [ 'SinglePhoton_Run2016H']

        print 'the lumito be used is ',lumi
        isLocal = True
        if str(opts.Local) == '0' or str(opts.Local).lower() == 'false' or str(opts.Local).lower() == 'no': isLocal = False
        treeTX = Sample.Tree(helper.selectSamples(opts.sampleFile, txDatasets, 'TX'), 'TX'  , 0, channel, isLocal, IDWP)
        treeEW = Sample.Tree(helper.selectSamples(opts.sampleFile, ewDatasets, 'EW'), 'EW'  , 0, channel, isLocal, IDWP)
        treeEWNLO = Sample.Tree(helper.selectSamples(opts.sampleFile, ewnloDatasets, 'EWNLO'), 'EWNLO'  , 0, channel, isLocal, IDWP)
        treeEWKNLO = Sample.Tree(helper.selectSamples(opts.sampleFile, ewkDatasets, 'EWKNLO'), 'EWKNLO'  , 0, channel, isLocal, IDWP)
        #treeQCD = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasets, 'QCD'), 'QCD'  , 0, channel, isLocal, IDWP)
        treeQCDMG = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdmgDatasets, 'QCDMG'), 'QCDMG'  , 0, channel, isLocal, IDWP)
        treeGjets = Sample.Tree(helper.selectSamples(opts.sampleFile, gjetsDatasets, 'GJets'), 'GJets'  , 0, channel, isLocal, IDWP)
        #treeQCDPt = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPt, 'QCD'), 'QCD'  , 0, channel, isLocal, IDWP)
        #treeQCDPtBins = Sample.Tree(helper.selectSamples(opts.sampleFile, qcdDatasetsPtBins, 'QCD'), 'QCD'  , 0, channel, isLocal, IDWP)

        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'DA'), 'DATA', 1, channel, isLocal, IDWP)
        #mcTrees = [  treeTT, treeEWK,  treeDY, treeEWK]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK, treeEWK1, treeEWK2, treeEWK3, treeEWK4]   
        #mcTrees = [ treeDY, treeQCD, treeTT, treeEW, treeEWK]   
        mcTrees = [ treeQCDMG, treeEWKNLO, treeTX, treeEW, treeGjets]   

        #mcTrees = [ treeDY]   
        if 'data' not in inn : treeDA =[]
        mcTrees = []
        if 'tx' in inn  : mcTrees = [treeTX]
        if 'qcd' in inn and 'mg' not in inn  : mcTrees = [treeQCD]
        if 'qcdmg' in inn   : mcTrees = [treeQCDMG]
        if 'gjets' in inn  : mcTrees = [treeGjets]
        if 'ewknlo' in inn  : mcTrees = [treeEWKNLO]
        if 'ew' in inn and 'ewk' not in inn : mcTrees = [treeEW]
        if 'ewnlo' in inn  : mcTrees = [treeEWNLO]
        if 'allmc' in inn : mcTrees = [ treeEWKNLO, treeQCDMG, treeTX, treeEW, treeGjets]
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
            givein ='{0:s}'.format(str(opts.varr))
            option=givein
            newname = givein
            newname = str(givein).replace(":", "_vs_")
            if 'Smear' in givein and 'data' in inn  : 
                print 'need to FIX SMEARRRRRRRRRRRRRRRRRRRRRRRRRRRRRR', givein, inn
                givein = givein.replace("Smear", "")


            docat='2'
            if dogjets : docat='1'
            nLep = 'nPhoton'



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
            if 'njetsgeq' in str(opts.ExtraTag).lower() : jetcut='-1'
            if 'hitslt1' in str(opts.ExtraTag).lower() : losthits='1'
            if 'metwmass' in givein.lower() : wtmasscut='0'
            '''
            if 'jetsgeq0' in tagname: jetcut='=0'
            if 'jetsgt0' in tagname: jetcut='0'
            if 'hitslt1' in tagname : losthits='1'
            if 'massgt0' in tagname: wtmasscut='0'
            if 'massgt80' in tagname: wtmasscut='80'
            '''
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


	    jetCut = " (  nPhoton[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>=0.9 && iso_1[0]<0.1 && nbtagL[0]==0.0 && cat==1 ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut)

            if 'nobtag' in tagname :
	        #jetCut = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>=0.9 && Photon_r9_1[0]<=1. ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut)
	        jetCut = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>={5:s} && Photon_r9_1[0]<=1. ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, photonr9)
            else :
	        #jetCut = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>=0.9 && Photon_r9_1[0]<=1. && nbtagL[0]==0.0".format(docat, jetcut, wtmasscut, njetsSyst, puppicut)
	        jetCut = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>={5:s} && Photon_r9_1[0]<=1. && nbtagL[0]==0.0 ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, photonr9)

	    #jetCutInvIso = " (  pt_1[0] >=50 && nPhoton[0]==1 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>=0.9 && iso_1[0]>0.1 && nbtagL[0]==0.0 && cat==1 ".format(docat, jetcut, wtmasscut, njetsSyst, puppicut)
	    jetCutB = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>={5:s} && Photon_r9_1[0]<=1. && nbtagL[0]==0.0 && Photon_cutBased_1== 2 && iso_1<=0.005".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, photonr9)
	    jetCutC = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>={5:s} && Photon_r9_1[0]<=1. && nbtagL[0]==0.0 && Photon_cutBased_1== 3 && iso_1>0.005".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, photonr9)
	    jetCutD = " (  pt_1[0]>=50 && fabs(eta_1[0])<1.44 && Flag_BadPFMuonDzFilter[0]==1 &&  nPVGood[0]>2 && njets{3:s}[0]> {1:s}  && Photon_r9_1[0]>={5:s} && Photon_r9_1[0]<=1. && nbtagL[0]==0.0 && Photon_cutBased_1== 2 && iso_1>0.005".format(docat, jetcut, wtmasscut, njetsSyst, puppicut, photonr9)
  
            if 'sideband' in tagname : 
                doQCD  = True
                if 'sidebandb' in tagname : jetCut = jetCutB
                if 'sidebandc' in tagname : jetCut = jetCutC
                if 'sidebandd' in tagname : jetCut = jetCutD

            if not doQCD : 
		if 'cutbasedtight' in tagname : jetCut = jetCut + " && Photon_cutBased_1== 3 "
		if 'cutbasedmedium' in tagname : jetCut = jetCut + " && Photon_cutBased_1== 2 "
		if 'mvaid80' in tagname : jetCut = jetCut + " && Photon_mvaID_WP80_1 ==1 "
		if 'mvaid90' in tagname : jetCut = jetCut + " && Photon_mvaID_WP90_1 ==1 "
		if 'isocut' in tagname and 'isocuttight' not in tagname: jetCut = jetCut + " && iso_1<=0.01 "
		if 'isocuttight' in tagname : jetCut = jetCut + " && iso_1<=0.005 "
		if 'isocutnotight' in tagname : jetCut = jetCut + " && iso_1 >0.005 "

            #if 'qcd' in inn : jetCut = jetCut + " && Photon_genPartFlav_1[0] !=1"
            if 'hoe' in tagname : jetCut = jetCut + " && Photon_hoe_1[0] <=0.04"
            if 'pixelseed' in tagname : jetCut = jetCut + " && Photon_pixelSeed_1[0] ==0"
            if 'electronveto' in tagname : jetCut = jetCut + " && Photon_electronVeto_1[0] ==1"
            if 'dr' in tagname : jetCut = jetCut + " && {0:s}{1:s}".format(drcutstr, drcut)
            if 'pult10' in tagname : jetCut  = jetCut + " && nPVGood[0]<10"
            if 'pu10to20' in tagname : jetCut  = jetCut + " && nPVGood[0]<20 && nPVGood>=10"
            if 'pu20to30' in tagname : jetCut  = jetCut + " && nPVGood[0]<30 && nPVGood>=20"
            if 'pu30to40' in tagname : jetCut  = jetCut + " && nPVGood[0]<40 && nPVGood>=30"
            if 'pu40to50' in tagname : jetCut  = jetCut + " && nPVGood[0]<50 && nPVGood>=40"
            if 'pugeq50' in tagname : jetCut  = jetCut + " && nPVGood[0]>=50 "
            if 'pugeq40' in tagname : jetCut  = jetCut + " && nPVGood[0]>=40 "

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
                if 'boson_pt' in givein.lower() : varTitle    = 'q_{T} [GeV]'
                if 'boson_phi' in givein : varTitle    = 'q_{#phi}'
                if 'PuppiMETmTmass' in givein : varTitle    = 'm_{T} [GeV]'
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
                    
                    print '------------------------------------------->', lumi, var, Variable, reg.bins[reg.rvars.index(var)], "", varTitle, channel, isLog
		    if ":" not in Variable : data_hist = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, channel, isLog)
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
                '''
                if doQCD and met.index(m) == 0: 
                    data_histInvIso = treeDA.getTH1F(lumi, var, Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, channel, isLog)
		    fOut.cd()
                    data_histInvIso.SetName('histo_data_QCD_inv')
                    data_histInvIso.Write('histo_data_QCD_inv')
		    for itree, tree in  enumerate(mcTrees):
			ind = 0
			cuts = CutManager.CutManager()
			treename = tree.name.lower()
			print 'with  %s for QCD kfactor finding' %treename
			print 'var to get', var+"_"+reg.name+treename+str(met.index(m)), ' or', var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, doNPV
			
			if 'qcd' not in treename : 
                            tmp_fullMCInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, channel, isLog)
		            fOut.cd()
                            tmp_fullMCInvIso.SetName(tmp_fullMCInvIso.GetName() + 'MC_inv')
                            tmp_fullMCInvIso.Write(tmp_fullMCInvIso.GetName() + 'MC_inv')

			if 'qcd' in treename :     
                            tmp_fullQCDInvIso= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCutInvIso) , "", varTitle, channel, isLog)
		            fOut.cd()
                            tmp_fullQCDInvIso.SetName(tmp_fullQCDInvIso.GetName() + 'QCD_inv')
                            tmp_fullQCDInvIso.Write(tmp_fullQCDInvIso.GetName() + 'QCD_inv')

                           
		    data_histInvIso.Add(tmp_fullMCInvIso,-1)
		    if tmp_fullQCDInvIso.GetSumOfWeights() > 0 : kfactor = data_histInvIso.GetSumOfWeights() / tmp_fullQCDInvIso.GetSumOfWeights()

                '''

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
                        if ":" not in Variable : tmp_full= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , inn, varTitle, channel, isLog)
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
                        if treename == 'qcdmg':
                            tmp_full.SetTitle("QCD MG multijet")
                            tmp_full.Scale(kfactor)
                        if treename == 'wjets':
                            tmp_full.SetTitle("W + jets")
                        if treename == 'ewk':
                            tmp_full.SetTitle("W + jets (LO)")

                        if treename == 'ewknlo':
                            tmp_full.SetTitle("W + jets (NLO)")

                        if treename == 'dy':
                            if dogjets:
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
                            tmp_full.SetTitle("V+Gamma")
                        if treename == 'ewnlo':
                            tmp_full.SetTitle("V+Gamma(WGnlo)")
                        if treename == 'stop':
                            tmp_full.SetTitle("Single-Top quark")
                        if treename == 'tx':
                            tmp_full.SetTitle("T(T)+Gamma ")
                        
                        getattr(reg, attr).setHisto(tmp_full, 'MC', 'central')
                        tmp_histo = copy.deepcopy(tmp_full.Clone(var+reg.name))
                        if doQCD : tmp_histo.SetName(tmp_histo.GetName() + '_QCD_inv')

                        fOut.cd()
			mnew = m.replace(":", "_vs_")
                        print 'should have the correct name ????????????????????????????', tmp_full.GetName(), mnew, m, treename, tmp_histo.GetName()
                        tmp_histo.Write('histo_'+treename+'_'+mnew)
                        print 'should have the correct name ????????????????????????????', tmp_full.GetName(), mnew, m, treename, tmp_histo.GetName()

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
                            histo_err= tree.getTH1F(lumi, var,  Variable, reg.bins[reg.rvars.index(var)], 1, 1, cuts.Add(cut, jetCut) , "", varTitle, channel, isLog)
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
            '''
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

            '''
            #del plot_var
            del Variable
            print yields
            time.sleep(0.1)
            print color.blue+'********************************************DONE***************************************************'+color.end
