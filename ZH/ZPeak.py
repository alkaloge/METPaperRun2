#!/usr/bin/env python

__author__ = "Alexis Kalogeropoulos" 

# import external modules 
import sys
import numpy as np
from ROOT import TFile, TTree, TH1, TH1D, TCanvas, TLorentzVector  
from math import sqrt, pi

# import from ZH_Run2/funcs/
sys.path.insert(1,'../funcs/')
#import tauFun
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
    
    return parser.parse_args()

args = getArgs()
print("args={0:s}".format(str(args)))
maxPrint = args.maxPrint 

cutCounter = {}
cutCounterGenWeight = {}

doJME  = args.doSystematics.lower() == 'true' or args.doSystematics.lower() == 'yes' or args.doSystematics == '1'
#cats = ['eee','eem','eet', 'mmm', 'mme', 'mmt']
cats=[ 'eeee', 'eemm', 'mmee', 'mmmm', 'eee', 'eem', 'mme', 'mmm', 'ee', 'mm']
catss=[ 'ee', 'mm']
doJME= True

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
    #if args.year !=2016 : PU.calculateWeights(args.nickName,args.year)
    #else : PU.calculateWeights('TTJets_DiLept',args.year)
else :
    CJ = ''
    if args.year == 2016 : CJ = GF.checkJSON(filein='Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt')
    if args.year == 2017 : CJ = GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2018 : CJ = GF.checkJSON(filein='Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt')


varSystematics=['']


print 'systematics', doJME, varSystematics

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


if args.weights > 0 :
    hWeight = TH1D("hWeights","hWeights",1,-0.5,0.5)
    hWeight.Sumw2()

    for count, e in enumerate(inTree) :
        hWeight.Fill(0, e.genWeight)
    

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
    if args.weights == 2 : 
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
    
isMC = True
if not MC : 
    isMC = False

sysT = ["Central"]
print("Opening {0:s} as output.".format(outFileName))
doSyst= True
onlyNom= True
outTuple = outTuple.outTuple(outFileName, era, doSyst, sysT, isMC, onlyNom)


tStart = time.time()
countMod = 1000

allMET=[]

if onlyNom == False :
    for i,j in enumerate(outTuple.allsystMET):
	if 'MET' in j and 'T1_' in j and 'phi' not in j : allMET.append(j)

Weights=Weights.Weights(args.year)

print 'will run on nMax', nMax



for count, e in enumerate(inTree) :
    if count % countMod == 0 :
        print("Count={0:d}".format(count))
        if count >= 10000 : countMod = 10000
    if count == nMax : break    

    
    for cat in cats : 
        cutCounter[cat].count('All')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('All', e.genWeight)

    isInJSON = False
    if not MC : isInJSON = CJ.checkJSON(e.luminosityBlock,e.run)
    if not isInJSON and not MC :
        #print("Event not in JSON: Run:{0:d} LS:{1:d}".format(e.run,e.luminosityBlock))
        continue

    for cat in cats: cutCounter[cat].count('InJSON')
    
    MetFilter = GF.checkMETFlags(e,args.year)
    if MetFilter : continue
    
    for cat in cats: cutCounter[cat].count('METfilter') 

    if unique :
        if e.event in uniqueEvents :
            for cat in cats: cutCounter[cat].count('Unique') 
        else :
            continue

    if not TF.goodTrigger(e, args.year) : continue
    
    for cat in cats: 
        lepMode = cat[:2]
	cutCounter[cat].count('Trigger')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)
            
        if args.category != 'none' and not lepMode in args.category : continue

        if lepMode == 'ee' :
            if e.nElectron < 2 : continue
	    cutCounter[cat].count('LeptonCount')
	    if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonCount', e.genWeight)

        if lepMode == 'mm' :
            if e.nMuon < 2 : continue 
	    cutCounter[cat].count('LeptonCount')
	    if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonCount', e.genWeight)

    met_pt = float(e.MET_pt)
    met_phi = float(e.MET_phi)

    if era=='2017' :
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
        if era=='2017' :
            try : 
		met_pt = float(e.METFixEE2017_T1_pt)
		met_phi = float(e.METFixEE2017_T1_phi)
	    except AttributeError : 
		met_pt = float(e.METFixEE2017_pt)
		met_phi = float(e.METFixEE2017_phi)
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
            
	    for j in range(e.nMuon): 
                e.Muon_pt[j] = muPt[j]
                e.Muon_mass[j] = muMass[j]
	    for j in range(e.nElectron): 
                e.Electron_pt[j] = elePt[j]
                e.Electron_mass[j] = eleMass[j]
	    for j in range(e.nTau): 
                e.Tau_pt[j] = tauPt[j]
                e.Tau_mass[j] = tauMass[j]
             

	if isMC: 

	    met_pt, met_phi, metlist, philist = Weights.applyES(e, args.year, systematic, metPtPhi, allMET)

	    #met_pt, met_phi = Weights.applyES(e, args.year, systematic, metPtPhi, allMET)
	    if systematic == 'Central' :
		for i, j in enumerate (metlist): 

		    outTuple.list_of_arrays[i][0] = metlist[i]
		for i, j in enumerate (philist): 
		    outTuple.list_of_arrays[i+len(metlist)][0] = philist[i]
	lepList=[]
	pairList=[]

	lepList_2=[]
	pairList_2=[]

	goodElectronList = TF.makeGoodElectronList(e)
	goodMuonList = TF.makeGoodMuonList(e)
	tauList = TF.getGoodTauList(cat, e)
	goodElectronList, goodMuonList = TF.eliminateCloseLeptons(e, goodElectronList, goodMuonList)
	goodElectronListExtraLepton=[]
	goodMuonListExtraLepton=[]


	for cat in catss: 
	    lepMode = cat[:2]
	    if lepMode == 'ee' :

		if len(goodElectronList) < 2 :continue
		cutCounter[cat].count('GoodLeptons')
		if MC : cutCounterGenWeight[cat].countGenWeight('GoodLeptons', e.genWeight)

		pairList, lepList = TF.findZ(goodElectronList,[], e)
		if len(lepList) <2 : continue

		goodElectronListExtraLepton = TF.makeGoodElectronListExtraLepton(e,lepList)

		# if there was a lepton rejected from the findZ put it in the extraLeptonsList
		if len(lepList) < len(goodElectronList) : 
		    for i in goodElectronList :
			if i not in lepList and i not in goodElectronListExtraLepton: goodElectronListExtraLepton.append(i)

		goodMuonListExtraLepton = goodMuonList
		#for i in lepList : 
		#    if i in goodMuonListExtraLepton : goodMuonListExtraLepton.remove(i)
		cutCounter[cat].count('LeptonPair')
		if MC : cutCounterGenWeight[cat].countGenWeight('LeptonPair', e.genWeight)
		#print ''
		#print 'stats goodEl', goodElectronList, 'Z peak', lepList, 'goodExtra', goodElectronListExtraLepton, goodMuonListExtraLepton, e.event

	    #if lepMode != 'ee' : continue

	    if lepMode == 'mm' :

		if len(goodMuonList) < 2 : continue
		cutCounter[cat].count('GoodLeptons')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('GoodLeptons', e.genWeight)

		pairList, lepList = TF.findZ([],goodMuonList, e)
		if len(lepList) <2 : continue
		goodMuonListExtraLepton = TF.makeGoodMuonListExtraLepton(e,lepList)

		# if there was a lepton rejected from the findZ put it in the extraLeptonsList
		if len(lepList) < len(goodMuonList) : 
		    for i in goodMuonList :
			if i not in lepList and i not in goodMuonListExtraLepton: goodMuonListExtraLepton.append(i)

		goodElectronListExtraLepton = goodElectronList

		#for i in lepList : 
		#    if i in goodElectronListExtraLepton : goodElectronListExtraLepton.remove(i)
		cutCounter[cat].count('LeptonPair')
		if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonPair', e.genWeight)
		


	    # eliminate close leptons amongst selected ones
	    goodElectronListExtraLepton, goodMuonListExtraLepton = TF.eliminateCloseLeptons(e, goodElectronListExtraLepton, goodMuonListExtraLepton)

	    #print 'stats goodEl after cleaning close leptons', goodElectronList, 'Z peak', lepList, 'goodExtra', goodElectronListExtraLepton, 'goodExtraMuons', goodMuonListExtraLepton, e.event

	    
	    # now will select a third lepton that is not part of the Z peak already

	    #newList=[]
	    LepP, LepM = TLorentzVector(), TLorentzVector()
	    if len(pairList)>1 : 
		LepP, LepM = pairList[0], pairList[1]

	    if len(pairList)<1 : continue

	    #print e.event, lepMode, cat, count
	    #continue
		    
	    #if len(goodMuonListExtraLepton) > 0 or len(goodElectronListExtraLepton) > 0  : print 'again----', e.event, 'goodEl', goodElectronList, 'goodM', goodMuonList, 'ExtraEl', goodElectronListExtraLepton, 'ExtraM', goodMuonListExtraLepton, 'taus', tauList,lepMode, cat, (LepP+LepM).M(), 'pair ?', lepList

	    catev = lepMode

	    LepP_2, LepM_2 = TLorentzVector(), TLorentzVector()
	    LepP_2el, LepM_2el = TLorentzVector(), TLorentzVector()
	    LepP_2mu, LepM_2mu = TLorentzVector(), TLorentzVector()
	    M_2l, M_2el, M_2mu = 0., 0.,0
	    pairList_2el, lepList_2el = [], []
	    pairList_2mu, lepList_2mu = [], []

	    tauCands=[]

	    for tauMode in ['et','mt','tt'] :
		#if args.category != 'none' and tauMode != args.category[2:] : continue
		catt= lepMode + tauMode
		if tauMode == 'tt' :
		    #tauListt = TF.getTauList(catt, e, pairList=pairList)
		    bestTauPair = TF.getBestTauPair(catt, e, tauList)
		    if len(bestTauPair)>0 :
			tauCands.append( bestTauPair[0])
			tauCands.append( bestTauPair[1])
                        #print 'found a good tauPair here', tauCands
					
		if tauMode == 'et' :
		    bestTauPair = TF.getBestETauPair(e,cat=catt,pairList=pairList)
		    if len(bestTauPair)>0 : tauCands.append(bestTauPair[1])
		if tauMode == 'mt' :
		    bestTauPair = TF.getBestMuTauPair(e,cat=catt,pairList=pairList)
		    if len(bestTauPair)>0 :tauCands.append( bestTauPair[1])


            #print cat, tauList, tauCands
	    #more leptons present - check if that coincides with nominal H->em channel
	    if len(goodElectronListExtraLepton)>0 and len(goodMuonListExtraLepton)>0 : 
		bestTauPair = TF.getBestEMuTauPair(e,cat=lepMode+'em',pairList=pairList)
		if len(bestTauPair)>1 :  #if you find a good H->e-mu tau, remove it from the ExtraLeptonList
		    #print 'we have a situation here...', bestTauPair, goodElectronListExtraLepton, goodMuonListExtraLepton, cat, catev, lepList, e.Electron_pt[bestTauPair[0]], e.Muon_pt[bestTauPair[1]], e.Electron_pt[goodElectronListExtraLepton[0]], e.Muon_pt[goodMuonListExtraLepton [0]], bestTauPair[0], bestTauPair[1]
		    if bestTauPair[0] in goodElectronListExtraLepton : goodElectronListExtraLepton.remove(bestTauPair[0])
		    if bestTauPair[1] in goodMuonListExtraLepton : goodMuonListExtraLepton.remove(bestTauPair[1])
		    if len(goodElectronListExtraLepton) == 0 and len(goodMuonListExtraLepton) == 0 : catev =lepMode

		    #print '=================================> lets look at this', e.event, 'nEle', len(goodElectronListExtraLepton), 'nM', len(goodMuonListExtraLepton)
		    if len(goodElectronListExtraLepton) != 0 and len(goodMuonListExtraLepton) == 0 : 
			if len(goodElectronListExtraLepton) == 1 : 
			    catev = lepMode + 'e'
			    lepList_2el = goodElectronListExtraLepton

			if len(goodElectronListExtraLepton) > 1 : 
			    pairList_2el, lepList_2el = TF.findZ(goodElectronListExtraLepton,[],e)

			    if len(lepList_2el) < 2 :  
				catev = lepMode + 'e'
				lepList_2el.append(goodElectronListExtraLepton[0])

			    if len(lepList_2el) > 1 : 
				catev= lepMode + 'ee' 
				LepP_2el, LepM_2el = pairList_2el[0], pairList_2el[1]


		    if len(goodElectronListExtraLepton) == 0 and len(goodMuonListExtraLepton) != 0 : 
			if len(goodMuonListExtraLepton) == 1 : 
			    catev =lepMode + 'm'
			    lepList_2mu = goodMuonListExtraLepton

			if len(goodMuonListExtraLepton) > 1 : 
			    pairList_2mu, lepList_2mu = TF.findZ([],goodMuonListExtraLepton,e)

			    if len(lepList_2mu) < 2  : 
				catev = lepMode + 'm' 
				lepList_2mu.append(goodMuonListExtraLepton[0])

			    if len(lepList_2mu) > 1  : 
				catev= lepMode + 'mm' 
				LepP_2mu, LepM_2mu = pairList_2mu[0], pairList_2mu[1]

		    #print 'did I fix it ? ...', bestTauPair, goodElectronListExtraLepton, goodMuonListExtraLepton, cat, catev, lepList

		# if there is not bestTau Pair, just take the leading lepton to form a new cat
		if len(bestTauPair)<2 : 
		    if TF.ComparepT (goodElectronListExtraLepton[0],goodMuonListExtraLepton[0],e) : 
			catev = lepMode +'e'		    
			lepList_2el.append(goodElectronListExtraLepton[0])
		    else : 
			catev = lepMode+ 'm'
			lepList_2mu.append(goodMuonListExtraLepton[0])
		    '''
		    if len(goodElectronListExtraLepton)>1 and len(goodMuonListExtraLepton)>1: 
			pairList_2el, lepList_2el = TF.findZ(goodElectronListExtraLepton,[],e)
			pairList_2mu, lepList_2mu = TF.findZ([], goodMuonListExtraLepton,e)
			if len(lepList_2mu) == 0 and len(lepList_2el) == 0 : continue

			if len(lepList_2mu) == 0 and len(lepList_2el) > 1 :
			    catenv = lepMode + 'ee'
			if len(lepList_2mu) > 1 and len(lepList_2el) == 0 :
			    catenv = lepMode + 'mm'

			if len(pairList_2el) > 1 and len(pairList_2mu) > 1 : 
			    M_2el = (LepM_2el + LepP_2el)
			    M_2mu = (LepM_2mu + LepP_2mu)
			    if M_2el.Pt() > M_2mu.Pt() : 
				pairList_2el, lepList_2el = pairList_2el, lepList_2el
				lepList_2mu = []
				catev = lepMode+'ee'

			    else  : 
				pairList_2mu, lepList_2mu = pairList_2mu, lepList_2mu
				lepList_2el = []
				catev = lepMode+'mm'

		    '''
	    #print 'and now lepList', lepList, 'cat=====', catev, 'lepList_2', lepList_2el, lepList_2mu, '+', lepList_2,  'lepList', lepList, 'extraEl==========>', len(goodElectronListExtraLepton), goodElectronListExtraLepton, 'extraMu=========>', len(goodMuonListExtraLepton), goodMuonListExtraLepton, 'extraTau=============>', len(tauList)
	    # 1 additional lepton mu/el and no el/mu
	    if len(goodElectronListExtraLepton)==1 and len(goodMuonListExtraLepton)==0 : 
		catev = lepMode+'e' 
		lepList_2el = goodElectronListExtraLepton
	    if len(goodMuonListExtraLepton)==1 and len(goodElectronListExtraLepton)==0 : 
		catev = lepMode+'m' 
		lepList_2mu = goodMuonListExtraLepton
	      

	    # when we have more leptons around from one flavour and zero from the other
	    if len(goodElectronListExtraLepton)>1 and len(goodMuonListExtraLepton)==0: 
		pairList_2el, lepList_2el = TF.findZ(goodElectronListExtraLepton,[],e)


		if len(lepList_2el) < 2 :  
		    catev = lepMode + 'e'
		    lepList_2el.append(goodElectronListExtraLepton[0])
		   

		if len(lepList_2el) > 1 : 
		    catev= lepMode + 'ee' 
		    LepP_2el, LepM_2el = pairList_2el[0], pairList_2el[1]

	   
	    if len(goodMuonListExtraLepton)>1 and len(goodElectronListExtraLepton)==0 : 
		pairList_2mu, lepList_2mu = TF.findZ([],goodMuonListExtraLepton,e)

		if len(lepList_2mu) < 2  : 
		    catev = lepMode + 'm' 
		    lepList_2mu.append(goodMuonListExtraLepton[0])

		if len(lepList_2mu) > 1  : 
		    catev= lepMode + 'mm' 
		    LepP_2mu, LepM_2mu = pairList_2mu[0], pairList_2mu[1]


	    lepList_2 = lepList_2el + lepList_2mu
	    #print '========!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!this is odd....', lepList, 'cat=====', catev, 'lepList_2', lepList_2, 'mass',  'mass_2', M_2el, M_2mu , 'extraEl==========>', len(goodElectronListExtraLepton), 'extraMu=========>', len(goodMuonListExtraLepton)


            
	    if catev == lepMode+'ee' : 
		M_2el = (LepM_2el + LepP_2el)
		if not TF.mllCut( (LepP+LepM).M() ) and not TF.mllCut(M_2el.M()): continue
	    if catev == lepMode+'mm' : 
		M_2mu = (LepM_2mu + LepP_2mu)
		if not TF.mllCut( (LepP+LepM).M() ) and not TF.mllCut(M_2mu.M()): continue

            if TF.mllCut( (LepP+LepM).M()) :
		for it in tauCands :
		    if it in tauList : 
			#print '---------------------------> I will have to remove', it, tauList, tauCands, catev
			tauList.remove(it)       
			#two passages as for tt channel we save two permutations
			#if it in tauCands : 
			#	#print '---------------------------> I will have to remove', it, tauList, tauCands, catev
			#	tauList.remove(it)       


	    #if len(catev) < 4 and  not TF.mllCut( (LepP+LepM).M() ) : continue
	    
	    #if len(goodMuonListExtraLepton) == 0 and len(goodElectronListExtraLepton) == 0 and len(tauList) > 1 : continue #we dont want to have taus with no leptons present - overlap with ZH
	    #if (len(goodMuonListExtraLepton) == 1 or len(goodElectronListExtraLepton) == 1) and len(tauList) == 1 : continue  #we dont want to the l+tau_h categories

	    if lepMode == 'ee' :
		if cat[:2] =='ee' :
		    cutCounter[cat].count('FoundZ')
		    if  MC :   cutCounterGenWeight[cat].countGenWeight('FoundZ', e.genWeight)
	    if lepMode == 'mm' :
		if cat[:2] =='mm' : 
		    cutCounter[cat].count('FoundZ')
		    if  MC :   cutCounterGenWeight[cat].countGenWeight('FoundZ', e.genWeight)
	    
	    #print 'and now lepList', lepList, 'cat=====', catev, 'lepList_2', lepList_2el, lepList_2mu, '+', lepList_2,  'lepList', lepList, 'extraEl==========>', len(goodElectronListExtraLepton), goodElectronListExtraLepton, 'extraMu=========>', len(goodMuonListExtraLepton), goodMuonListExtraLepton, 'extraTau=============>', len(tauList)

	    #if len(catev) <3 and len(tauCand)==0 : continue

	    
	    if LepP.Pt() > LepM.Pt() and LepP.Pt()<25 : continue
	    if LepM.Pt() > LepP.Pt() and LepM.Pt()<25 : continue
	    
	    if MC :
		outTuple.setWeight(PU.getWeight(e.PV_npvs)) 
		outTuple.setWeightPU(PU.getWeight(e.Pileup_nPU)) 
		outTuple.setWeightPUtrue(PU.getWeight(e.Pileup_nTrueInt)) 
		#print 'nPU', e.Pileup_nPU, e.Pileup_nTrueInt, PU.getWeight(e.Pileup_nPU), PU.getWeight(e.Pileup_nTrueInt), PU.getWeight(e.PV_npvs), PU.getWeight(e.PV_npvsGood)
	    else : 
		outTuple.setWeight(1.) 
		outTuple.setWeightPU(1.) ##
		outTuple.setWeightPUtrue(1.)
	    

	    if not MC : isMC = False

	    if len(tauList) > 0 : print catev, 'lepList', lepList,'lepList_2', lepList_2, 'exEl', goodElectronListExtraLepton, 'ExM', goodMuonListExtraLepton, 'tauList Cands', tauCands, 'tauList', tauList, (LepP+LepM).M()

	    #doJME=False
	    #outTuple.Fill3L(e,catev,LepP,LepM,lepList,lepList_2,goodElectronListExtraLepton, goodMuonListExtraLepton, tauCands, isMC, era, doJME, met_pt, met_phi) 
	    #outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era,doJME, met_pt, met_phi,  isyst, tauMass, tauPt, eleMass, elePt, muMass, muPt)

	if maxPrint > 0 :
	    maxPrint -= 1
	    print("\n\nGood Event={0:d} cat={1:s}  MCcat={2:s}".format(e.event,cat,GF.eventID(e)))
	    print("goodMuonList={0:s} goodElectronList={1:s} Mll={2:.1f} bestTauPair={3:s}".format(
		str(goodMuonList),str(goodElectronList),M,str(bestTauPair)))
	    print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
	    GF.printEvent(e)
	    print("Event ID={0:s} cat={1:s}".format(GF.eventID(e),cat))
		

dT = time.time() - tStart
print("Run time={0:.2f} s  time/event={1:.1f} us".format(dT,1000000.*dT/count))

hCutFlow=[]
hCutFlowW=[]
countt=0
for cat in cats :
    print('\nSummary for {0:s}'.format(cat))
    cutCounter[cat].printSummary()
    hName="hCutFlow_"+str(cat)
    hNameW="hCutFlowWeighted_"+str(cat)
    hCutFlow.append( TH1D(hName,hName,15,0.5,15.5))
    if MC  : hCutFlowW.append( TH1D(hNameW,hNameW,15,0.5,15.5))
    lcount=len(cutCounter[cat].getYield())
    for i in range(lcount) :
        #hCutFlow[cat].Fill(1, float(cutCounter[cat].getYield()[i]))
        yields = cutCounter[cat].getYield()[i]
        hCutFlow[countt].Fill(i+1, float(yields))
        hCutFlow[countt].GetXaxis().SetBinLabel(i+1,str(cutCounter[cat].getLabels()[i]))

        if MC : 
	    yieldsW = cutCounterGenWeight[cat].getYieldWeighted()[i]
            hCutFlowW[countt].Fill(i+1, float(yieldsW))
            hCutFlowW[countt].GetXaxis().SetBinLabel(i+1,str(cutCounterGenWeight[cat].getLabels()[i]))
            #print cat, cutCounter[cat].getYield()[i], i, cutCounter[cat].getLabels()[i]

    
    hCutFlow[countt].Sumw2()
    if MC : hCutFlowW[countt].Sumw2()
    countt+=1

if not MC : CJ.printJSONsummary()


outTuple.writeTree()

