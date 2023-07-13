#!/usr/bin/env python

""" ZH.py: makes an nTuple for the ZH->tautau analysis """

__author__ = "Dan Marlow, Alexis Kalogeropoulos, Gage DeZoort" 
__version__ = "GageDev_v1.1"

# import external modules 
import sys
import numpy as np
from ROOT import TFile, TTree, TH1, TH1D, TCanvas, TLorentzVector  
from math import sqrt, pi
#from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
#from TauPOG.TauIDSFs.TauIDSFTool import TauESTool
#from TauPOG.TauIDSFs.TauIDSFTool import TauFESTool

# import from ZH_Run2/funcs/
sys.path.insert(1,'../funcs/')
import tauFun2 as TF
import generalFunctions as GF 
import Weights 
import outTuple
import time

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    parser.add_argument("-f","--inFileName",default='ZHtoTauTau_test.root',help="File to be analyzed.")
    parser.add_argument("-c","--category",default='none',help="Event category to analyze.")
    parser.add_argument("--nickName",default='',help="MC sample nickname") 
    parser.add_argument("-d","--dataType",default='MC',help="Data or MC") 
    parser.add_argument("-o","--outFileName",default='',help="File to be used for output.")
    parser.add_argument("-n","--nEvents",default=0,type=int,help="Number of events to process.")
    parser.add_argument("-m","--maxPrint",default=0,type=int,help="Maximum number of events to print.")
    parser.add_argument("-t","--testMode",default='',help="tau MVA selection")
    parser.add_argument("-y","--year",default=2017,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-s","--selection",default='ZH',help="is this for the ZH or the AZH analysis?")
    parser.add_argument("-u","--unique",default='none',help="CSV file containing list of unique events for sync studies.") 
    parser.add_argument("-w","--weights",default=False,type=int,help="to re-estimate Sum of Weights")
    parser.add_argument("-j","--doSystematics",type=str, default='false',help="do JME systematics")
    parser.add_argument("-e","--era",type=str, default='EOY',help="EOY of UL")
    
    return parser.parse_args()

args = getArgs()
print("args={0:s}".format(str(args)))
maxPrint = args.maxPrint 

cutCounter = {}
cutCounterGenWeight = {}

doJME  = args.doSystematics.lower() == 'true' or args.doSystematics.lower() == 'yes' or args.doSystematics == '1'

#doJME = True

cats = ['eeee', 'eeet','eemt','eett','eeem','mmmm','mmet','mmmt','mmtt','mmem']
cats = ['eeee', 'mmmm']
cats = ['mmtt', 'mmet', 'mmmt', 'mmem']
#cats = ['mmmm']

for cat in cats : 
    cutCounter[cat] = GF.cutCounter()
    cutCounterGenWeight[cat] = GF.cutCounter()

inFileName = args.inFileName
print("Opening {0:s} as input.  Event category {1:s}".format(inFileName,cat))

isAZH=False
if str(args.selection) == 'AZH' : isAZH = True
if isAZH : print 'You are running on the AZH mode !!!'

inFile = TFile.Open(inFileName)
inFile.cd()

inTree = inFile.Get("Events")
nentries = inTree.GetEntries()
nMax = nentries
print("nentries={0:d} nMax={1:d}".format(nentries,nMax))
if args.nEvents > 0 : nMax = min(args.nEvents-1,nentries)


MC = len(args.nickName) > 0 
if args.dataType == 'Data' or args.dataType == 'data' : MC = False
if args.dataType == 'MC' or args.dataType == 'mc' : MC = True

if MC :
    print "this is MC, will get PU etc", args.dataType
    PU = GF.pileUpWeight()
    PU.calculateWeights(args.nickName,args.year)
    #else : PU.calculateWeights('TTJets_DiLept',args.year)
else :
    CJ = ''#GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2016 : CJ = GF.checkJSON(filein='Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt')
    if args.year == 2017 : CJ = GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2018 : CJ = GF.checkJSON(filein='Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt')


print 'systematics', doJME

era=str(args.year)

outFileName = GF.getOutFileName(args).replace(".root",".ntup")

if MC : 
    if "WJetsToLNu" in outFileName and 'TWJets' not in outFileName:
	hWxGenweightsArr = []
	for i in range(5):
	    hWxGenweightsArr.append(TH1D("W"+str(i)+"genWeights",\
		    "W"+str(i)+"genWeights",1,-0.5,0.5))
    elif "DYJetsToLL" in outFileName:
	hDYxGenweightsArr = []
	for i in range(5):
	    hDYxGenweightsArr.append(TH1D("DY"+str(i)+"genWeights",\
		    "DY"+str(i)+"genWeights",1,-0.5,0.5))

isZH = 'ZH' in outFileName or 'HZJ' in outFileName

if args.weights > 0 :
    hWeight = TH1D("hWeights","hWeights",1,-0.5,0.5)
    hWeight.Sumw2()
    hWeightScaleUp = TH1D("hWeightsScaleUp","hWeightsScaleUp",1,-0.5,0.5)
    hWeightScaleUp.Sumw2()
    hWeightScaleDown = TH1D("hWeightsScaleDown","hWeightsScaleDown",1,-0.5,0.5)
    hWeightScaleDown.Sumw2()


    hWeightScaleSTXS = TH1D("hWeightsScaleSTXS","hWeightsScaleSTXS",11,-0.5,10.5)
    hWeightScaleSTXS.Sumw2()
    hWeightScaleSTXSUp = TH1D("hWeightsScaleSTXSUp","hWeightsScaleSTXSUp",11,-0.5,10.5)
    hWeightScaleSTXSUp.Sumw2()
    hWeightScaleSTXSDown = TH1D("hWeightsScaleSTXSDown","hWeightsScaleSTXSDown",11,-0.5,10.5)
    hWeightScaleSTXSDown.Sumw2()



    for count, e in enumerate(inTree) :
        hWeight.Fill(0, e.genWeight)
        if isZH : 
	    hWeightScaleUp.Fill(0, e.genWeight*e.LHEScaleWeight[8])
	    hWeightScaleDown.Fill(0, e.genWeight*e.LHEScaleWeight[0])

	    hWeightScaleSTXS.Fill(0, e.genWeight)
	    hWeightScaleSTXSUp.Fill(0, e.genWeight*e.LHEScaleWeight[8])
	    hWeightScaleSTXSDown.Fill(0, e.genWeight*e.LHEScaleWeight[0])

	    if e.HTXS_stage1_1_cat_pTjet30GeV == 300 or e.HTXS_stage1_1_cat_pTjet30GeV == 400 or e.HTXS_stage1_1_cat_pTjet30GeV == 500 : 
	       hWeightScaleSTXS.Fill(1, e.genWeight)
	       hWeightScaleSTXSUp.Fill(1, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(1, e.genWeight*e.LHEScaleWeight[0])

	    if e.HTXS_stage1_1_cat_pTjet30GeV == 301 or e.HTXS_stage1_1_cat_pTjet30GeV == 401 or e.HTXS_stage1_1_cat_pTjet30GeV == 501 : 
	       hWeightScaleSTXS.Fill(2, e.genWeight)
	       hWeightScaleSTXSUp.Fill(2, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(2, e.genWeight*e.LHEScaleWeight[0])

	    if e.HTXS_stage1_1_cat_pTjet30GeV == 302 or e.HTXS_stage1_1_cat_pTjet30GeV == 402 or e.HTXS_stage1_1_cat_pTjet30GeV == 502 : 
	       hWeightScaleSTXS.Fill(3, e.genWeight)
	       hWeightScaleSTXSUp.Fill(3, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(3, e.genWeight*e.LHEScaleWeight[0])

	    if e.HTXS_stage1_1_cat_pTjet30GeV == 303 or e.HTXS_stage1_1_cat_pTjet30GeV == 403 or e.HTXS_stage1_1_cat_pTjet30GeV == 503 : 
	       hWeightScaleSTXS.Fill(4, e.genWeight)
	       hWeightScaleSTXSUp.Fill(4, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(4, e.genWeight*e.LHEScaleWeight[0])

	    if e.HTXS_stage1_1_cat_pTjet30GeV == 304 or e.HTXS_stage1_1_cat_pTjet30GeV == 404 or e.HTXS_stage1_1_cat_pTjet30GeV == 504 : 
	       hWeightScaleSTXS.Fill(5, e.genWeight)
	       hWeightScaleSTXSUp.Fill(5, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(5, e.genWeight*e.LHEScaleWeight[0])


	    if e.HTXS_stage1_1_cat_pTjet30GeV == 305 or e.HTXS_stage1_1_cat_pTjet30GeV == 405 or e.HTXS_stage1_1_cat_pTjet30GeV == 505 : 
	       hWeightScaleSTXS.Fill(6, e.genWeight)
	       hWeightScaleSTXSUp.Fill(6, e.genWeight*e.LHEScaleWeight[8])
	       hWeightScaleSTXSDown.Fill(6, e.genWeight*e.LHEScaleWeight[0])


    

        if "WJetsToLNu" in outFileName and 'TWJets' not in outFileName:

            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4: 	hWxGenweightsArr[npartons].Fill(0, e.genWeight)
        if "DYJetsToLL" in outFileName :
            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4 : hDYxGenweightsArr[npartons].Fill(0, e.genWeight)

    fName = GF.getOutFileName(args).replace(".root",".weights")
    fW = TFile( fName, 'recreate' )
    print 'Will be saving the Weights in', fName
    fW.cd()

    if "WJetsToLNu" in outFileName and 'TWJets' not in outFileName:
        for i in range(len(hWxGenweightsArr)):
            hWxGenweightsArr[i].Write()
    elif "DYJetsToLL" in outFileName:
        for i in range(len(hDYxGenweightsArr)):
            hDYxGenweightsArr[i].Write()

    hWeight.Write()
    hWeightScaleUp.Write()
    hWeightScaleDown.Write()
    hWeightScaleSTXS.Write()
    hWeightScaleSTXSUp.Write()
    hWeightScaleSTXSDown.Write()
    if args.weights > 1 : 
        fW.Close()
        sys.exit()

#############end weights

# read a CSV file containing a list of unique events to be studied 
unique = False 
if args.unique != 'none' :
    unique = True
    uniqueEvents = set()
    for line in open(args.unique,'r').readlines() : uniqueEvents.add(int(line.strip()))
    print("******* Analyzing only {0:d} events from {1:s} ******.".format(len(uniqueEvents),args.unique))
    
print("Opening {0:s} as output.".format(outFileName))

sysT = ["Central"]

sysall = [
'scale_e', 'scale_m_etalt1p2', 'scale_m_eta1p2to2p1', 'scale_m_etagt2p1',
'scale_t_1prong', 'scale_t_1prong1pizero', 'scale_t_3prong', 'scale_t_3prong1pizero']

#sysall = ['scale_e']

upS=sysall
downS=sysall

for i, sys in enumerate(sysall) : 
    sysT.append(sys+'Up')
    sysT.append(sys+'Down')


sysT=['Central']
print sysT

isMC = True
if not MC : 
    sysT = ["Central"]
    isMC = False

#sysT = ["Central"]
doSyst= False
outTuple = outTuple.outTuple(outFileName, era, doSyst, sysT, isMC)



tStart = time.time()
countMod = 1000

print outTuple.allsystMET

allMET=[]
for i,j in enumerate(outTuple.allsystMET):
    if 'MET' in j and 'T1_' in j and 'phi' not in j : allMET.append(j)



Weights=Weights.Weights(args.year)

lumiss=['1637', '1423', '1631', '1601','180']
# run lumi event
# 1                  1572                157154
for count, e in enumerate( inTree) :
    
    if count % countMod == 0 :
        print("Count={0:d}".format(count))
        if count >= 10000 : countMod = 10000
    if count == nMax : break    
    
    #if count<320000 : continue
    #if count>370000 : break
    printOn=False
    #if str(e.luminosityBlock) not in lumiss : continue
    #if str(e.luminosityBlock) in lumiss : printOn = True

    for cat in cats : 
        cutCounter[cat].count('All')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('All', e.genWeight)
 
    isInJSON = False
    if not MC : isInJSON = CJ.checkJSON(e.luminosityBlock,e.run)
    if not isInJSON and not MC :
        #print("Event not in JSON: Run:{0:d} LS:{1:d}".format(e.run,e.luminosityBlock))
        continue

    for cat in cats: 
        cutCounter[cat].count('InJSON')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('InJSON', e.genWeight)
    
    #MetFilter = GF.checkMETFlags(e,args.year, isMC, args.era)
    #if MetFilter and printOn :   print cat, e.run, e.luminosityBlock,  e.event, 'failed MET filters'
    #if MetFilter : continue
    
    for cat in cats: 
        cutCounter[cat].count('METfilter') 
	if  MC :   cutCounterGenWeight[cat].countGenWeight('METfilter', e.genWeight)


    if unique :
        if e.event in uniqueEvents :
            for cat in cats: cutCounter[cat].count('Unique') 
        else :
            continue
    if not TF.goodTrigger(e,args.year) and printOn :   print cat, e.run, e.luminosityBlock,  e.event, 'Triggers not present...'
    if not TF.goodTrigger(e, args.year) : continue


    isbTag = False 
    for j in range(e.nJet) :
	 if e.Jet_pt[j] > 35 and e.Jet_btagDeepFlavB[j] > 0.7476 : isbTag = True
    if  isbTag and printOn:   print e.run, e.luminosityBlock,  e.event, 'failed isbTag'
    if isbTag : continue
    for cat in cats:
	cutCounter[cat].count('0bTag')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('0bTag', e.genWeight)

    for cat in cats: 
        isTrig=False
	if cat[:2] =='mm': isTrig = e.HLT_IsoMu24 or e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ
	if cat[:2] =='ee' : isTrig = e.HLT_Ele27_WPTight_Gsf or e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ 
        
	if isTrig : 
            cutCounter[cat].count('Trigger')
	    if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)



    met_pt = float(e.MET_pt)
    met_phi = float(e.MET_phi)

    if era=='2017' and args.era=='EOY':
	met_pt = float(e.METFixEE2017_pt)
	met_phi = float(e.METFixEE2017_phi)

    if doJME :  #default after JME systematics with Smear
        if era!='2017' :
	    try : 
		met_pt = float(e.MET_T1_pt)
		met_phi = float(e.MET_T1_phi)
	    except AttributeError : 
		met_pt = float(e.MET_pt)
		met_phi = float(e.MET_pt)
        if era=='2017' and args.era=='EOY':
            try : 
		met_pt = float(e.METFixEE2017_T1_pt)
		met_phi = float(e.METFixEE2017_T1_phi)
	    except AttributeError : 
		met_pt = float(e.METFixEE2017_pt)
		met_phi = float(e.METFixEE2017_phi)

        if era=='2017' and args.era=='UL':
            try : 
		met_pt = float(e.MET_T1_pt)
		met_phi = float(e.MET_T1_phi)
	    except AttributeError : 
		met_pt = float(e.MET_pt)
		met_phi = float(e.MET_phi)

    #print met_pt, 'smear', e.MET_T1Smear_pt, 'uncorrected?', e.MET_pt
    tauMass=[]
    tauPt=[]
    eleMass=[]
    elePt=[]
    muMass=[]
    muPt=[]
    metPtPhi=[]
    metPtPhi.append(float(met_pt))
    metPtPhi.append(float(met_phi))

    if MC : 
	if len(muMass) == 0 :
	    for j in range(e.nMuon):
		muMass.append(e.Muon_mass[j])
		muPt.append(e.Muon_pt[j])

	if len(eleMass) == 0 :
	    for j in range(e.nElectron):
		eleMass.append(e.Electron_mass[j])
		elePt.append(e.Electron_pt[j])

	if len(tauMass) == 0 :
	    for j in range(e.nTau):
		tauMass.append(e.Tau_mass[j])
		tauPt.append(e.Tau_pt[j])



    
    for isyst, systematic in enumerate(sysT) : 
	if isyst>0 : #use the default pT/mass for Ele/Muon/Taus before doing any systematic
	#if 'Central' in systematic or 'prong' in systematic : #use the default pT/mass for Ele/Muon/Taus before doing the Central or the tau_scale systematics ; otherwise keep the correction

	    for j in range(e.nMuon): 
                e.Muon_pt[j] = muPt[j]
                e.Muon_mass[j] = muMass[j]
	    for j in range(e.nElectron): 
                e.Electron_pt[j] = elePt[j]
                e.Electron_mass[j] = eleMass[j]
	    for j in range(e.nTau): 
                e.Tau_pt[j] = tauPt[j]
                e.Tau_mass[j] = tauMass[j]
             

        
        #print ''
        #applyES - do it once for Central and redoit for tau_scale_systematics - otherwise keep the correction
        #print 'before fixxxxxxxxxxxx e.MET_T1_pt', e.MET_T1_pt, '== met_pt ? ', met_pt, '== what is fed in', metPtPhi[0], e.event, systematic
	#met_pt, met_phi = Weights.applyES(e, args.year, systematic, metPtPhi)
	if isMC: 

	    met_pt, met_phi, metlist, philist = Weights.applyES(e, args.year, systematic, metPtPhi, allMET)
	    #met_pt, met_phi = Weights.applyES(e, args.year, systematic, metPtPhi, allMET)
	    #print 'after fixxxxxxxxxxxx e.MET_T1_pt', e.MET_T1_pt, ' == what is fed in', metPtPhi[0], ' corrected MET ->', met_pt,  'some jesTotalUp MET', e.MET_T1_pt_jesTotalUp , e.event, systematic
	    
	    #if len(metlist) != len(philist) : print 'There is a problem with met/phi systematics list - will not concider this event', e.event
	    # uncomment the following if you need to pass the corrected MET for systematics to account for the ES corrections
	    if systematic == 'Central' :
		for i, j in enumerate (metlist): 

		    outTuple.list_of_arrays[i][0] = metlist[i]
		for i, j in enumerate (philist): 
		    outTuple.list_of_arrays[i+len(metlist)][0] = philist[i]

		    #if systematic == 'Central' and ( e.event==1481 or e.event==17892 or e.event==8904):
		    #    print 'it was', outTuple.list_of_arrays[i][0] , i, j, len(metlist) , metlist[i], e.event, e.MET_T1_pt_jesAbsoluteUp, len(sysT), systematic


	#for lepMode in ['ee','mm'] :
	goodElectronList = TF.makeGoodElectronListDCH(e)
	goodMuonList = TF.makeGoodMuonListDCH(e)

	#for cat in cats :
	#for lepMode in ['ee','mm'] :
	for lepMode in ['mm'] :

	    if args.category != 'none' and not lepMode in args.category : continue

            if lepMode == 'ee' :
                if e.nElectron < 2 : continue
            if lepMode == 'mm' :
                if e.nMuon < 2 : continue

	    #uncomment below for the dR cuts
	    #goodElectronList, goodMuonList = TF.eliminateCloseLeptons(e, goodElectronList, goodMuonList)
	    #goodElectronListExtraLepton=[]
	    #goodMuonListExtraLepton=[]

	    lepList=[]
	    lepListP=[]
	    lepListM=[]

            '''
	    if cat == 'eeee' :
		if len(goodElectronList) < 4 and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed as you have < 4 goodElectronList'
		if len(goodElectronList) < 4 : continue
		#for i in goodElectronList : print 'leptons electrons...', len(goodElectronList), i, e.Electron_pt[i], e.Electron_charge[i], e.Electron_phi[i],  e.HLT_Ele27_WPTight_Gsf, e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, e.event

		cutCounter[cat].count('FourLeptons')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('FourLeptons', e.genWeight)

		isTrig = e.HLT_Ele27_WPTight_Gsf or e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ 
		if  not isTrig and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed Trigger'
		if not isTrig : continue
		cutCounter[cat].count('Trigger')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)

		pairListP, lepListP, pairListM, lepListM, LeptV = TF.findHpair(goodElectronList,[], e)
		if  (len(lepListP)!=2 or len(lepListM)!=2) and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed (len(lepListP)!=2 or len(lepListM)!=2)'
		if len(lepListP)!=2 or len(lepListM)!=2 : continue
		LVP = pairListP[0] + pairListP[1]
		LVM = pairListM[0] + pairListM[1]
		netS = e.Electron_charge[lepListP[0]] + e.Electron_charge[lepListP[1]] + e.Electron_charge[lepListM[0]] + e.Electron_charge[lepListM[1]]
		if len(goodElectronList)==4 and len(lepListP)==2 and len(lepListM)==2 and not isbTag and isTrig and e.Electron_pt[lepListP[0]] >30 and e.Electron_pt[lepListM[0]]>30 and netS ==0 and LVP.M()>5 and LVM.M()>5 and len(goodMuonList)==0: 
		    print cat, e.run, e.luminosityBlock,  e.event, '{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(e.Electron_pt[lepListP[0]], e.Electron_pt[lepListP[1]], e.Electron_pt[lepListM[0]], e.Electron_pt[lepListM[1]], e.Electron_pfRelIso03_all[lepListP[0]], e.Electron_pfRelIso03_all[lepListP[1]], e.Electron_pfRelIso03_all[lepListM[0]], e.Electron_pfRelIso03_all[lepListM[1]] ) 
		    #if len(lepListP)==2 and len(lepListM)==2 : print e.luminosityBlock, e.run, e.event, e.Electron_pt[lepListP[0]], e.Electron_pt[lepListP[1]], e.Electron_pt[lepListM[0]], e.Electron_pt[lepListM[1]], isbTag, isTrig
		
		
		cutCounter[cat].count('TwoHHPairs')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('TwoHHPairs', e.genWeight)


	    if cat == 'mmmm' :
		if  len(goodMuonList) < 4 and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed as you have < 4 goodMuonList'
		if len(goodMuonList) < 4 : 
                    #GF.printEvent(e)
                    continue
		#for i in goodElectronList : print 'leptons electrons...', len(goodElectronList), i, e.Electron_pt[i], e.Electron_charge[i], e.Electron_phi[i],  e.HLT_Ele27_WPTight_Gsf, e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, e.event

		cutCounter[cat].count('FourLeptons')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('FourLeptons', e.genWeight)

		isTrig = e.HLT_IsoMu24 or e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or e.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
		isTrig = e.HLT_IsoMu24 or e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ

		if  not isTrig and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed Trigger'
		if not isTrig : continue
		cutCounter[cat].count('Trigger')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)

		pairListP, lepListP, pairListM, lepListM = TF.findHpair([],goodMuonList,e)
		if  (len(lepListP)!=2 or len(lepListM)!=2) and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed (len(lepListP)!=2 or len(lepListM)!=2)'
		if len(lepListP)!=2 or len(lepListM)!=2 : continue
		LVP = pairListP[0] + pairListP[1]
		LVM = pairListM[0] + pairListM[1]
		netS = e.Muon_charge[lepListP[0]] + e.Muon_charge[lepListP[1]] + e.Muon_charge[lepListM[0]] + e.Muon_charge[lepListM[1]]
		#if len(goodMuonList)==4 and len(lepListP)==2 and len(lepListM)==2 and not isbTag and isTrig and e.Muon_pt[lepListP[0]] >30 and e.Muon_pt[lepListM[0]]>30 and netS ==0 and LVP.M()>5 and LVM.M()>5 and len(goodElectronList)==0: 
		if len(goodMuonList)==4 and len(lepListP)==2 and len(lepListM)==2 and not isbTag and isTrig and e.Muon_pt[lepListP[0]] >30 and e.Muon_pt[lepListM[0]]>30 and netS ==0 and LVP.M()>5 and LVM.M()>5 and len(goodElectronList)==0: 
		    #print cat, e.run, e.luminosityBlock,  e.event, '{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], e.Muon_pfRelIso03_all[lepListP[0]], e.Muon_pfRelIso03_all[lepListP[1]], e.Muon_pfRelIso03_all[lepListM[0]], e.Muon_pfRelIso03_all[lepListM[1]] ) 
		    print cat, e.run, e.luminosityBlock,  e.event, '{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], e.Muon_tkRelIso[lepListP[0]], e.Muon_tkRelIso[lepListP[1]], e.Muon_tkRelIso[lepListM[0]], e.Muon_tkRelIso[lepListM[1]] ) 
		    #if len(lepListP)==2 and len(lepListM)==2 : print e.luminosityBlock, e.run, e.event, e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], isbTag, isTrig
		

		cutCounter[cat].count('TwoHHPairs')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('TwoHHPairs', e.genWeight)

            '''

            pairList=[]
            lepList=[]
            signC=0
            netS=-99
	    if lepMode=='mm' and len(goodMuonList) < 2 :
		if printOn:   print lepMode, e.run, e.luminosityBlock,  e.event, 'failed as you have < 2 goodMuonList'
		continue

	    if lepMode=='ee' and len(goodElectronList) < 2 :
		if printOn:   print lepMode, e.run, e.luminosityBlock,  e.event, 'failed as you have < 2 goodElectronList'
		continue

	    #mm + tau tau decays
	    ## pairListP -> containes the TLV of the ++ pair  
	    ## lepListP -> containes the indices of the ++ pair  

	    if lepMode=='mm' :
		pairListP, lepListP, pairListM, lepListM = TF.findHpair([],goodMuonList,e)
	    if lepMode=='ee' :
		pairListP, lepListP, pairListM, lepListM = TF.findHpair(goodElectronList,[],e)

	    if not (  (len(lepListP) ==2 and len(lepListM) == 0) or (len(lepListP) == 0 and len(lepListM) == 2) ) : continue

	    lepList=[]
	    if len(lepListP) ==2 and len(lepListM) == 0 : 
		pairList=pairListP
		lepList=lepListP
		print 'we have a pair of ++'

	    if len(lepListM) ==2 and len(lepListP) == 0 : 
		pairList=pairListM
		lepList=lepListM

            if lepMode=='mm' : 
                signC=e.Muon_charge[lepList[0]]
                netS = e.Muon_charge[lepList[0]] + e.Muon_charge[lepList[1]]
            if lepMode=='ee' : 
                signC=e.Electron_charge[lepList[0]]
                netS = e.Electron_charge[lepList[0]] + e.Electron_charge[lepList[1]]

	    print 'pairList checking------------------->', pairList, pairList[0].Px(), pairList[0].Pt(), lepMode, signC, netS

		#netS = e.Muon_charge[lepList[0]] + e.Muon_charge[lepList[1]]
		### signC carries info about the charge of the other higgs SS pair -> the tt pair must have then opposite sign charge compared to the lepton

            
            for cat in cats : 
		cutCounter[cat].count('TwoLeptons')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('TwoLeptons', e.genWeight)
	    

            for tauMode in ['et','mt','tt','em'] :
                if args.category != 'none' and tauMode != args.category[2:] : continue
                cat = lepMode + tauMode

		bestTauPair=[]

		if tauMode == 'tt' :
		    tauList = TF.getTauList(cat, e, pairList= pairList, signC=signC)
		    print "len of tauList", tauList
		    bestTauPair = TF.getBestTauPair(cat, e, tauList)
		    if len(bestTauPair) > 1 : print cat, tauMode, e.Muon_charge[lepList[0]], e.Muon_charge[lepList[1]], e.Tau_charge[bestTauPair[0]], e.Tau_charge[bestTauPair[1]], lepList, bestTauPair

		elif tauMode == 'et' :
		    bestTauPair = TF.getBestETauPair(e,cat=cat,pairList=pairList, signC=signC)
		    if len(bestTauPair) > 1 : print cat, tauMode, e.Muon_charge[lepList[0]], e.Muon_charge[lepList[1]], e.Electron_charge[bestTauPair[0]], e.Tau_charge[bestTauPair[1]], lepList, bestTauPair
		elif tauMode == 'mt' :
                    if lepMode=='mm' and len(goodMuonList)<3 : continue
		    bestTauPair = TF.getBestMuTauPair(e,cat=cat,pairList=pairList, signC=signC)
		    if len(bestTauPair) > 1 : print cat, tauMode, e.Muon_charge[lepList[0]], e.Muon_charge[lepList[1]], e.Muon_charge[bestTauPair[0]], e.Tau_charge[bestTauPair[1]], lepList, bestTauPair
		elif tauMode == 'em' :
		    bestTauPair = TF.getBestEMuTauPair(e,cat=cat,pairList=pairList, signC=signC)
		    if len(bestTauPair) > 1 : print cat, tauMode, e.Muon_charge[lepList[0]], e.Muon_charge[lepList[1]], e.Electron_charge[bestTauPair[0]], e.Muon_charge[bestTauPair[1]], lepList, bestTauPair
		else : continue
	    
	    continue

	    if len(bestTauPair) < 1 :
		if unique :
		    print("Tau Pair Fail: Event ID={0:d} cat={1:s}".format(e.event,cat))
		    bestTauPair = TF.getBestEMuTauPair(e,cat=cat,pairList=LeptV,printOn=True) 
		    GF.printEvent(e)
				    
		if False and maxPrint > 0 and (tauMode == GF.eventID(e)[2:4]) :
		    maxPrint -= 1
		    print("Failed tau-pair cut")
		    print("Event={0:d} cat={1:s}".format(e.event,cat))
		    print("goodMuonList={0:s} goodElectronList={1:s} Mll={3:.1f} bestTauPair={4:s}".format(
			str(goodMuonList),str(goodElectronList),str(pairList),M,str(bestTauPair)))
		    print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
		    GF.printEvent(e)
		    GF.printMC(e)
		continue


	    if len(bestTauPair) > 1 :
		jt1, jt2 = bestTauPair[0], bestTauPair[1]
	    else :
		continue

	    cutCounter[cat].count("GoodTauPair")
	    if  MC:   cutCounterGenWeight[cat].countGenWeight('GoodTauPair', e.genWeight)

	    if MC :
		outTuple.setWeight(PU.getWeight(e.PV_npvs)) 
		outTuple.setWeightPU(PU.getWeight(e.Pileup_nPU)) 
		outTuple.setWeightPUtrue(PU.getWeight(e.Pileup_nTrueInt)) 
		#print 'nPU', e.Pileup_nPU, e.Pileup_nTrueInt, PU.getWeight(e.Pileup_nPU), PU.getWeight(e.Pileup_nTrueInt), PU.getWeight(e.PV_npvs), PU.getWeight(e.PV_npvsGood)
	    else : 
		outTuple.setWeight(1.) 
		outTuple.setWeightPU(1.) ##
		outTuple.setWeightPUtrue(1.)


	    #cutCounter[cat].count("VVtightTauPair")
	    #if MC :   cutCounterGenWeight[cat].countGenWeight('VVtightTauPair', e.genWeight)
			
	    #SVFit = True
	    SVFit = False
	    
	    if not MC : isMC = False
	     
	    #print 'will Fill for syst', isyst, sysT[isyst]
	    outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era,doJME, met_pt, met_phi,  isyst, tauMass, tauPt, eleMass, elePt, muMass, muPt, args.era)
	    #outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era,doJME, met_pt, met_phi,  isyst)

	    if maxPrint > 0 :
		maxPrint -= 1
		print("\n\nGood Event={0:d} cat={1:s}  MCcat={2:s}".format(e.event,cat,GF.eventID(e)))
		print("goodMuonList={0:s} goodElectronList={1:s} Mll={2:.1f} bestTauPair={3:s}".format(
		    str(goodMuonList),str(goodElectronList),M,str(bestTauPair)))
		print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
		GF.printEvent(e)
		print("Event ID={0:s} cat={1:s}".format(GF.eventID(e),cat))


	    '''    



		pairListP, lepListP, pairListM, lepListM = TF.findHpair([],goodMuonList,e)
		if  (len(lepListP)!=2 or len(lepListM)!=2) and printOn:   print cat, e.run, e.luminosityBlock,  e.event, 'failed (len(lepListP)!=2 or len(lepListM)!=2)'
		if len(lepListP)!=2 or len(lepListM)!=2 : continue
		LVP = pairListP[0] + pairListP[1]
		LVM = pairListM[0] + pairListM[1]
		netS = e.Muon_charge[lepListP[0]] + e.Muon_charge[lepListP[1]] + e.Muon_charge[lepListM[0]] + e.Muon_charge[lepListM[1]]
		#if len(goodMuonList)==4 and len(lepListP)==2 and len(lepListM)==2 and not isbTag and isTrig and e.Muon_pt[lepListP[0]] >30 and e.Muon_pt[lepListM[0]]>30 and netS ==0 and LVP.M()>5 and LVM.M()>5 and len(goodElectronList)==0: 
		if len(goodMuonList)==4 and len(lepListP)==2 and len(lepListM)==2 and not isbTag and isTrig and e.Muon_pt[lepListP[0]] >30 and e.Muon_pt[lepListM[0]]>30 and netS ==0 and LVP.M()>5 and LVM.M()>5 and len(goodElectronList)==0: 
		    #print cat, e.run, e.luminosityBlock,  e.event, '{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], e.Muon_pfRelIso03_all[lepListP[0]], e.Muon_pfRelIso03_all[lepListP[1]], e.Muon_pfRelIso03_all[lepListM[0]], e.Muon_pfRelIso03_all[lepListM[1]] ) 
		    print cat, e.run, e.luminosityBlock,  e.event, '{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], e.Muon_tkRelIso[lepListP[0]], e.Muon_tkRelIso[lepListP[1]], e.Muon_tkRelIso[lepListM[0]], e.Muon_tkRelIso[lepListM[1]] ) 
		    #if len(lepListP)==2 and len(lepListM)==2 : print e.luminosityBlock, e.run, e.event, e.Muon_pt[lepListP[0]], e.Muon_pt[lepListP[1]], e.Muon_pt[lepListM[0]], e.Muon_pt[lepListM[1]], isbTag, isTrig
		

		cutCounter[cat].count('TwoHHPairs')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('TwoHHPairs', e.genWeight)


            #LepP, LepM = pairList[0], pairList[1]
	    #M = (LepM + LepP).M()
	    if not TF.mllCut(M) :
		if unique :
		    print("Zmass Fail: : Event ID={0:d} cat={1:s} M={2:.2f}".format(e.event,cat,M))
		    #GF.printEvent(e)
		    #if MC : GF.printMC(e)
		continue ##cut valid for both AZH and ZH



		cutCounter[cat].count("GoodTauPair")
		if  MC:   cutCounterGenWeight[cat].countGenWeight('GoodTauPair', e.genWeight)

		if MC :
		    outTuple.setWeight(PU.getWeight(e.PV_npvs)) 
		    outTuple.setWeightPU(PU.getWeight(e.Pileup_nPU)) 
		    outTuple.setWeightPUtrue(PU.getWeight(e.Pileup_nTrueInt)) 
		    #print 'nPU', e.Pileup_nPU, e.Pileup_nTrueInt, PU.getWeight(e.Pileup_nPU), PU.getWeight(e.Pileup_nTrueInt), PU.getWeight(e.PV_npvs), PU.getWeight(e.PV_npvsGood)
		else : 
		    outTuple.setWeight(1.) 
		    outTuple.setWeightPU(1.) ##
		    outTuple.setWeightPUtrue(1.)


			    
		SVFit = True
		#SVFit = False
		
		if not MC : isMC = False
		 
		outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era,doJME, met_pt, met_phi,  isyst, tauMass, tauPt, eleMass, elePt, muMass, muPt, args.era)
		#outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era,doJME, met_pt, met_phi,  isyst)

		if maxPrint > 0 :
		    maxPrint -= 1
		    print("\n\nGood Event={0:d} cat={1:s}  MCcat={2:s}".format(e.event,cat,GF.eventID(e)))
		    print("goodMuonList={0:s} goodElectronList={1:s} Mll={2:.1f} bestTauPair={3:s}".format(
			str(goodMuonList),str(goodElectronList),M,str(bestTauPair)))
		    print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
		    GF.printEvent(e)
		    print("Event ID={0:s} cat={1:s}".format(GF.eventID(e),cat))
    
	    '''
dT = time.time() - tStart
print("Run time={0:.2f} s  time/event={1:.1f} us".format(dT,1000000.*dT/count))

hLabels=[]
hLabels.append('All')
hLabels.append('inJSON')
hLabels.append('METfilter')
hLabels.append('0bTag')
hLabels.append('Trigger')
hLabels.append('TwoLeptons')
hLabels.append('GoodTauPair')

hCutFlow=[]
hCutFlowW=[]

#
outTuple.writeTree()
fW = TFile( outFileName, 'update' )
fW.cd()

print '------------------------->',fW, outFileName
for icat,cat in enumerate(cats) :
    print('\nSummary for {0:s}'.format(cat))
    cutCounter[cat].printSummary()
    hName="hCutFlow_"+str(cat)
    hNameW="hCutFlowWeighted_"+str(cat)
    hCutFlow.append( TH1D(hName,hName,20,0.5,20.5))
    if MC  : hCutFlowW.append( TH1D(hNameW,hNameW,20,0.5,20.5))
    #if not MC : lcount=len(cutCounter[cat].getYield()) #lcount stands for how many different values you have
    #else : lcount=len(cutCounterGenWeight[cat].getYieldWeighted()) #lcount stands for how many different values you have
    lcount=len(hLabels)
    print lcount, cat, icat
    for i in range(len(hLabels)) :
        hCutFlow[icat].GetXaxis().SetBinLabel(i+1,hLabels[i])
        if MC : hCutFlowW[icat].GetXaxis().SetBinLabel(i+1,hLabels[i])

    for i in range(lcount) :
        #hCutFlow[cat].Fill(1, float(cutCounter[cat].getYield()[i]))
        yields = cutCounter[cat].getYield()[i]
        hCutFlow[icat].Fill(i+1, float(yields))

        if MC : 
	    yieldsW = cutCounterGenWeight[cat].getYieldWeighted()[i]
            hCutFlowW[icat].Fill(i+1, float(yieldsW))
        #print cutCounter[cat].getYield()[i], i, cutCounter[cat].getLabels()[i]

       
    hCutFlow[icat].Sumw2()
    hCutFlow[icat].Write()
    if MC : 
        hCutFlowW[icat].Sumw2()
        hCutFlowW[icat].Write()
    icat+=1

if not MC : CJ.printJSONsummary()



