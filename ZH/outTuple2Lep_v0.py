#r output ntuple for H->tautau analysis for CMSSW_10_2_X

from ROOT import TLorentzVector, TH1, std
from math import sqrt, sin, cos, pi, fabs
import tauFun2
import ROOT, array
import os
import sys
import generalFunctions as GF
import ScaleFactor as SF
from METCorrections import correctedMET

sys.path.insert(1,'../correctionlib/')
from correctionlib import _core


electronMass = 0.0005
muonMass  = 0.105
class outTuple2Lep() :
    
    def __init__(self,fileName, era, doSyst=False,shift=[], isMC=True, onlyNom=False, isW=False):
        from array import array
        from ROOT import TFile, TTree

        # Tau Decay types
        ########### JetMet systematics
        self.sf_EleTrig = ''
        self.sf_EleTrig = SF.SFs()
        #Electron_RunUL2016postVFP_Ele25_EtaLt2p1.root  Electron_RunUL2016preVFP_Ele25_EtaLt2p1.root   Electron_RunUL2017_Ele35.root                  Electron_RunUL2018_Ele35.root
        self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2018_Ele35.root'}
        if '2016pre' in str(era):  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2016preVFP_Ele25_EtaLt2p1.root'}
        if '2016' in str(era) and 'pre' not in str(era):  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2016postVFP_Ele25_EtaLt2p1.root'}
        if '2017' in str(era) :  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2017_Ele35.root'}

        print 'era', era, self.TriggerSF['fileElectron']
        self.sf_EleTrig.ScaleFactor("{0:s}{1:s}".format(self.TriggerSF['dir'],self.TriggerSF['fileElectron']))

        #lines above with .root files, lines below with correction lib

        self.evaluator=''
	self.fname = "./muon_Z_{0:s}.json.gz".format(str(era))
	if self.fname.endswith(".json.gz"):
	    import gzip
	    with gzip.open(self.fname,'rt') as file:
		self.datasf = file.read().strip()
		self.evaluator = _core.CorrectionSet.from_string(self.datasf)
	else:
	    self.evaluator = _core.CorrectionSet.from_file(self.fname)
		# Tau Decay types

        self.evaluatorEl=''
	self.fnameEl = "./electron_{0:s}.json.gz".format(str(era))
	if self.fnameEl.endswith(".json.gz"):
	    import gzip
	    with gzip.open(self.fnameEl,'rt') as file:
		self.datasfEl = file.read().strip()
		self.evaluatorEl = _core.CorrectionSet.from_string(self.datasfEl)
	else:
	    self.evaluatorEl = _core.CorrectionSet.from_file(self.fnameEl)
		# Tau Decay types
        print 'initialized the UL SF from', self.fname, self.fnameEl
	# TrackerMuon Reconstruction UL scale factor
	#self.valsf = self.evaluator["NUM_MediumID_DEN_TrackerMuons"].evaluate("2017_UL", 1.1, 30.0, "sf")
	#print("sf 1 is: " + str(self.valsf))
        ########### JetMet systematics
	#self.listsyst=['njets', 'nbtag', 'jpt', 'jeta', 'jflavour','MET_T1_pt', 'MET_T1_phi', 'MET_pt', 'MET_phi', 'MET_T1Smear_pt', 'MET_T1Smear_phi']
        self.jessyst=['_nom']
	self.listsyst=['MET_T1_pt', 'MET_T1_phi', 'MET_pt', 'MET_phi', 'PuppiMET_pt', 'PuppiMET_phi', 'MET_T1Smear_pt', 'MET_T1Smear_phi']
	#self.flavlist = ['MET', 'MET_T1', 'MET_T1', 'METCor_T1', 'METCorGood_T1', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood']
        if doSyst :
	    self.jessyst=['_nom', '_jesTotal', '_jer','_jesHEMIssue']  

        if onlyNom :
	    self.jessyst=['_nom']



	varss=['Up','Down']
        self.n = array('f', [ 0 ])

        self.allsystMET = []
        self.allsystJets = []
        self.jetsVariations=[]
        self.list_of_arrays = []           
        self.list_of_arrays_noES = []           
        self.list_of_arraysJetsPt = []           
        self.list_of_arraysJetsEta = []           
        self.list_of_arraysJetsFlavour = []           
        self.list_of_arraysJetsNbtagDeep = []           
        self.list_of_arraysJetsNbtagL = []           
        self.list_of_arraysJetsNbtagM = []           
        self.list_of_arraysJetsNbtagT = []           
        self.list_of_arraysJetsNjets = []           
        self.list_of_arraysJetsFlavour = []           
	self.tauMass = 1.7768 

        if not isMC  :
        
	    self.listsyst=[ 'MET_pt', 'MET_phi']
	    self.jessyst=['_nom']
	    varss=[]

        if doSyst : 

	    #self.jetsVariations.append('_nom')
	    self.allsystMET = []
	    self.allsystJets = []
	    #create a list with Up/Down from the above combinations
	    
	    for i_ in self.listsyst :
		for jes in self.jessyst :
		    if 'nom' not in jes :
			for var in varss :
			    if 'MET' in i_ and 'T1' in i_: 
				self.allsystMET.append(i_+jes+var)
				self.list_of_arrays.append(array('f', [ 0 ]))
				self.list_of_arrays_noES.append(array('f', [ 0 ]))
 
                    '''
		    if 'nom' in jes :
			if 'MET' in i_ : continue
			    #self.allsystMET.append(i_+jes)
			    #self.list_of_arrays.append(array('f', [ 0 ]))

                    ''' 
            for jes in self.jessyst :
		    if 'nom' in jes :   
			self.allsystJets.append(jes)
			self.list_of_arraysJetsNjets.append( array('i',[-1]))
			self.list_of_arraysJetsNbtagL.append( array('i',[-1]))
			self.list_of_arraysJetsNbtagM.append( array('i',[-1]))
			self.list_of_arraysJetsNbtagT.append( array('i',[-1]))
			self.list_of_arraysJetsFlavour.append( array('i',[-99]*15))
			self.list_of_arraysJetsEta.append( array('f',[-9.99]*15))
			self.list_of_arraysJetsPt.append( array('f',[-9.99]*15))
			self.list_of_arraysJetsNbtagDeep.append( array('i',[-1]*15))
		    else :   
		        for var in varss :
			    self.allsystJets.append(jes+var)
			    self.list_of_arraysJetsNjets.append( array('i',[-1]))
			    self.list_of_arraysJetsNbtagL.append( array('i',[-1]))
			    self.list_of_arraysJetsNbtagM.append( array('i',[-1]))
			    self.list_of_arraysJetsNbtagT.append( array('i',[-1]))
			    self.list_of_arraysJetsFlavour.append( array('i',[-99]*15))
			    self.list_of_arraysJetsEta.append( array('f',[-9.99]*15))
			    self.list_of_arraysJetsPt.append( array('f',[-9.99]*15))
			    self.list_of_arraysJetsNbtagDeep.append( array('i',[-1]*15))
                     
                
	    #for i_ in self.allsystMET :  self.list_of_arrays.append(array('f', [ 0 ]))

	    #for i_ in self.allsystJets :  
		
             

        print '------>systematics list', self.allsystMET
        print '------>jetssystematics list', self.allsystJets


        self.f = TFile( fileName, 'recreate' )
        self.t = TTree( 'Events', 'Output tree' )

        self.entries          = 0 
        self.run              = array('l',[0])
        self.lumi             = array('l',[0])
        self.evnt              = array('l',[0])

        self.nElectron        = array('I',[0])
        self.nMuon            = array('I',[0])
        self.nTau            = array('I',[0])
        self.VetoTau            = array('I',[0])
        self.VetoPhoton            = array('I',[0])
        self.VetoElectron            = array('I',[0])
        self.VetoMuon            = array('I',[0])
        self.nPU              = array('I',[0])
        self.nPUEOOT              = array('I',[0])
        self.nPULOOT              = array('I',[0])
        self.nPUtrue              = array('f',[0])
        self.nPV              = array('I',[0])
        self.PVx              = array('f',[0])
        self.PVy              = array('f',[0])
        self.PVz              = array('f',[0])
        self.nPVscore              = array('f',[0])
        self.nPVchi2              = array('f',[0])
        self.nPVndof              = array('f',[0])
        self.nPVGood              = array('I',[0])
        self.cat              = array('I',[0])
        self.weight           = array('f',[0])
        self.weightPU           = array('f',[0])
        self.weightPUtrue           = array('f',[0])
        self.LHEweight        = array('f',[0])
        self.Generator_weight = array('f',[0])
        self.LHE_Njets        = array('i',[-1])
        self.electronTriggerWord  = array('I',[0])
        self.muonTriggerWord  = array('I',[0])         
        self.whichTriggerWord  = array('I',[0])         
        self.whichTriggerWordSubL  = array('I',[0])         
        self.LHEScaleWeights        = array('f',[1]*9)
        
        self.nGoodElectron    = array('l',[0])
        self.nGoodMuon        = array('l',[0])
        self.Flag_hfNoisyHitsFilter        = array('I',[0])
        self.Flag_BadPFMuonDzFilter        = array('I',[0])

        self.L1PreFiringWeight_Nom        = array('f',[0])
        self.L1PreFiringWeight_Up        = array('f',[0])
        self.L1PreFiringWeight_Down        = array('f',[0])
        self.Electron_convVeto        = array('f',[0])
        self.Electron_lostHits        = array('I',[0])

        # di-lepton variables.   1 and 2 refer to plus and minus charge
        self.mll       = array('f',[0])
        self.zll_pt       = array('f',[0])
        self.zll_phi       = array('f',[0])

        self.d0_1        = array('f',[0])
        self.dZ_1        = array('f',[0])
        self.d0_2        = array('f',[0])
        self.dZ_2        = array('f',[0])
        
        self.pt_uncor_1        = array('f',[0])
        self.m_uncor_1        = array('f',[0])
        self.pt_uncor_2        = array('f',[0])
        self.m_uncor_2        = array('f',[0])

        self.Electron_mvaFall17V2noIso_WP90_1 = array('f',[0])
        self.Electron_mvaFall17V2Iso_WP90_1 = array('f',[0])
        self.Electron_cutBased_1 = array('f',[0])
        self.gen_match_1 = array('l',[0])

        self.Electron_mvaFall17V2noIso_WP90_2 = array('f',[0])
        self.Electron_mvaFall17V2Iso_WP90_2 = array('f',[0])
        self.Electron_cutBased_2 = array('f',[0])
        self.gen_match_2 = array('l',[0])

        # di-lepton variables.   1 and 2 refer to plus and minus charge
        self.mll       = array('f',[0])

        self.IDSF1      = array('f',[0])
        self.IsoSF1      = array('f',[0])
        self.TrigSF1      = array('f',[0])
        self.IDSF2      = array('f',[0])
        self.IsoSF2      = array('f',[0])
        self.TrigSF2      = array('f',[0])
        self.IDSF      = array('f',[0])
        self.IsoSF      = array('f',[0])
        self.TrigSF      = array('f',[0])
        #self.muonTightiDsf_1      = array('f',[0])


        self.m_1_tr   = array('f',[0])
        self.pt_1      = array('f',[0])
        self.pt_1_tr   = array('f',[0])
        self.GenPart_statusFlags_1   = array('l',[0])
        self.GenPart_status_1     = array('l',[0])
        self.phi_1     = array('f',[0])
        self.phi_1_tr  = array('f',[0])
        self.eta_1     = array('f',[0])
        self.eta_1_tr  = array('f',[0])
        self.iso_1       = array('f',[0])
        self.PFiso_1       = array('f',[0])
        self.q_1       = array('f',[0])
        self.Muon_Id_1       = array('f',[0])
        self.isGlobal_1       = array('f',[0])
        self.isStandalone_1       = array('f',[0])

        self.highPtId_1       = array('f',[0])
        self.highPurity_1       = array('f',[0])
        self.inTimeMuon_1       = array('f',[0])
        self.ip3d_1       = array('f',[0])
        self.sip3d_1       = array('f',[0])
        self.stations_1       = array('I',[0])
        self.TrackerL_1       = array('I',[0])

        self.isPFcand_1       = array('f',[0])
        self.isTracker_1       = array('f',[0])
        self.tightId_1       = array('f',[0])
        self.tightCharge_1       = array('f',[0])
        self.mediumId_1       = array('f',[0])
        self.pfIsoId_1       = array('f',[0])
        self.mediumPromptId_1       = array('f',[0])
        self.looseId_1       = array('f',[0])




        # second candidate
        self.m_2_tr   = array('f',[0])
        self.pt_2   = array('f',[0])
        self.pt_2_tr   = array('f',[0])
        self.GenPart_statusFlags_2   = array('l',[0])
        self.GenPart_status_2     = array('l',[0])
        self.phi_2     = array('f',[0])
        self.phi_2_tr  = array('f',[0])
        self.eta_2     = array('f',[0])
        self.eta_2_tr  = array('f',[0])
        self.iso_2       = array('f',[0])
        self.PFiso_2       = array('f',[0])
        self.q_2       = array('f',[0])
        self.Muon_Id_2       = array('f',[0])
        self.isGlobal_2       = array('f',[0])
        self.isStandalone_2       = array('f',[0])

        self.highPtId_2       = array('f',[0])
        self.highPurity_2       = array('f',[0])
        self.inTimeMuon_2       = array('f',[0])
        self.ip3d_2       = array('f',[0])
        self.sip3d_2       = array('f',[0])
        self.stations_2       = array('I',[0])
        self.TrackerL_2       = array('I',[0])

        self.isPFcand_2       = array('f',[0])
        self.isTracker_2       = array('f',[0])
        self.tightId_2       = array('f',[0])
        self.tightCharge_2       = array('f',[0])
        self.mediumId_2       = array('f',[0])
        self.pfIsoId_2       = array('f',[0])
        self.mediumPromptId_2       = array('f',[0])
        self.looseId_2       = array('f',[0])


        # MET variables
        self.metcov00    = array('f',[0])
        self.metcov01    = array('f',[0])
        self.metcov10    = array('f',[0])
        self.metcov11    = array('f',[0])

	self.MET_pt = array('f',[-99])
	self.MET_phi = array('f',[-99])
	self.MET_significance = array('f',[-99])

	self.RawMET_pt = array('f',[-99])
	self.RawMET_phi = array('f',[-99])
	self.RawPuppiMET_pt = array('f',[-99])
	self.RawPuppiMET_phi = array('f',[-99])

	self.PuppiMET_pt = array('f',[-99])
	self.PuppiMET_phi = array('f',[-99])

        
        if doSyst :

	    branches = ['PuppiMET', 'MET', 'MET_T1', 'METCor_T1', 'METCorGood_T1', 'PuppiMETCor', 'PuppiMETCorGood', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear']
	    attributes = ['pt', 'phi']
	    variations = ['', 'JESUp', 'JESDown', 'JERUp', 'JERDown', 'UnclusteredUp', 'UnclusteredDown']

	    for branch in branches:
		for attr in attributes:
		    for var in variations:
			#if (branch == 'MET' or branch == 'MET_T1') and var == '':
			if (branch == 'MET' ) and var == '':
			    continue
			branch_name = "{}_{}{}".format(branch, attr, var)
			setattr(self, branch_name, array('f', [-99]))
			print("Created branch:", branch_name)
			#setattr(self, f"{branch}_{attr}{var}", array('f', [-99]))



	self.boson_pt = array('f',[-99])
	self.boson_phi = array('f',[-999])
	self.Puppiboson_pt = array('f',[-99])
	self.Puppiboson_phi = array('f',[-999])


	self.u_par_RawMET = array('f',[-999])
	self.u_perp_RawMET = array('f',[-999])

	self.u_par_MET = array('f',[-999])
	self.u_perp_MET = array('f',[-999])
	self.u_par_MET_T1 = array('f',[-999])
	self.u_perp_MET_T1 = array('f',[-999])
	self.u_par_PuppiMET = array('f',[-999])
	self.u_perp_PuppiMET = array('f',[-999])
	self.u_par_PuppiMETCor = array('f',[-999])
	self.u_perp_PuppiMETCor = array('f',[-999])
	self.u_par_PuppiMETCorGood = array('f',[-999])
	self.u_perp_PuppiMETCorGood = array('f',[-999])
	self.u_par_METCor_T1 = array('f',[-999])
	self.u_perp_METCor_T1 = array('f',[-999])
	self.u_par_METCorGood_T1 = array('f',[-999])
	self.u_perp_METCorGood_T1 = array('f',[-999])
        #smear
	self.u_par_MET_T1Smear = array('f',[-999])
	self.u_perp_MET_T1Smear = array('f',[-999])
	self.u_par_METCor_T1Smear = array('f',[-999])
	self.u_perp_METCor_T1Smear = array('f',[-999])
	self.u_par_METCorGood_T1Smear = array('f',[-999])
	self.u_perp_METCorGood_T1Smear = array('f',[-999])

        if doSyst :
	    #systematics

	    branches = ['MET_T1', 'PuppiMET', 'METCor_T1', 'PuppiMETCor', 'METCorGood_T1', 'PuppiMETCorGood', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear']
	    attributes = ['u_par', 'u_perp']
	    variations = ['UnclusteredUp', 'UnclusteredDown', 'JESUp', 'JESDown', 'JERUp', 'JERDown']

	    # Adding branches for Smear variations
	    smear_variations = ['SmearUnclusteredUp', 'SmearUnclusteredDown', 'SmearJESUp', 'SmearJESDown', 'SmearJERUp', 'SmearJERDown']

            for attr in attributes:
	        for branch in branches:
		    for var in variations:
			branch_name = "{}_{}{}".format(attr,branch,  var)
			setattr(self, branch_name, array('f', [-999]))
			print("Created branch:", branch_name)


            '''
	    self.u_par_MET_T1UnclusteredUp = array('f',[-999])
	    self.u_perp_MET_T1UnclusteredUp = array('f',[-999])
	    self.u_par_PuppiMETUnclusteredUp = array('f',[-999])
	    self.u_perp_PuppiMETUnclusteredUp = array('f',[-999])


	    self.u_par_MET_T1UnclusteredDown = array('f',[-999])
	    self.u_perp_MET_T1UnclusteredDown = array('f',[-999])
	    self.u_par_PuppiMETUnclusteredDown = array('f',[-999])
	    self.u_perp_PuppiMETUnclusteredDown = array('f',[-999])

            #JES

	    self.u_par_MET_T1JESUp = array('f',[-999])
	    self.u_perp_MET_T1JESUp = array('f',[-999])
	    self.u_par_PuppiMETJESUp = array('f',[-999])
	    self.u_perp_PuppiMETJESUp = array('f',[-999])


	    self.u_par_MET_T1JESDown = array('f',[-999])
	    self.u_perp_MET_T1JESDown = array('f',[-999])
	    self.u_par_PuppiMETJESDown = array('f',[-999])
	    self.u_perp_PuppiMETJESDown = array('f',[-999])


	    #JER

	    self.u_par_MET_T1JERUp = array('f',[-999])
	    self.u_perp_MET_T1JERUp = array('f',[-999])
	    self.u_par_PuppiMETJERUp = array('f',[-999])
	    self.u_perp_PuppiMETJERUp = array('f',[-999])



	    self.u_par_MET_T1JERDown = array('f',[-999])
	    self.u_perp_MET_T1JERDown = array('f',[-999])
	    self.u_par_PuppiMETJERDown = array('f',[-999])
	    self.u_perp_PuppiMETJERDown = array('f',[-999])

            ##fix

	    self.u_par_METCor_T1UnclusteredUp = array('f',[-999])
	    self.u_perp_METCor_T1UnclusteredUp = array('f',[-999])
	    self.u_par_PuppiMETCorUnclusteredUp = array('f',[-999])
	    self.u_perp_PuppiMETCorUnclusteredUp = array('f',[-999])

	    self.u_par_METCor_T1UnclusteredDown = array('f',[-999])
	    self.u_perp_METCor_T1UnclusteredDown = array('f',[-999])
	    self.u_par_PuppiMETCorUnclusteredDown = array('f',[-999])
	    self.u_perp_PuppiMETCorUnclusteredDown = array('f',[-999])

            #JES
	    self.u_par_METCor_T1JESUp = array('f',[-999])
	    self.u_perp_METCor_T1JESUp = array('f',[-999])
	    self.u_par_PuppiMETCorJESUp = array('f',[-999])
	    self.u_perp_PuppiMETCorJESUp = array('f',[-999])

	    self.u_par_METCor_T1JESDown = array('f',[-999])
	    self.u_perp_METCor_T1JESDown = array('f',[-999])
	    self.u_par_PuppiMETCorJESDown = array('f',[-999])
	    self.u_perp_PuppiMETCorJESDown = array('f',[-999])


	    #JER
	    self.u_par_METCor_T1JERUp = array('f',[-999])
	    self.u_perp_METCor_T1JERUp = array('f',[-999])
	    self.u_par_PuppiMETCorJERUp = array('f',[-999])
	    self.u_perp_PuppiMETCorJERUp = array('f',[-999])

	    self.u_par_METCor_T1JERDown = array('f',[-999])
	    self.u_perp_METCor_T1JERDown = array('f',[-999])
	    self.u_par_PuppiMETCorJERDown = array('f',[-999])
	    self.u_perp_PuppiMETCorJERDown = array('f',[-999])

            ###CorGood
	    self.u_par_METCorGood_T1UnclusteredUp = array('f',[-999])
	    self.u_perp_METCorGood_T1UnclusteredUp = array('f',[-999])
	    self.u_par_PuppiMETCorGoodUnclusteredUp = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodUnclusteredUp = array('f',[-999])

	    self.u_par_METCorGood_T1UnclusteredDown = array('f',[-999])
	    self.u_perp_METCorGood_T1UnclusteredDown = array('f',[-999])
	    self.u_par_PuppiMETCorGoodUnclusteredDown = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodUnclusteredDown = array('f',[-999])

            #JES
	    self.u_par_METCorGood_T1JESUp = array('f',[-999])
	    self.u_perp_METCorGood_T1JESUp = array('f',[-999])
	    self.u_par_PuppiMETCorGoodJESUp = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodJESUp = array('f',[-999])

	    self.u_par_METCorGood_T1JESDown = array('f',[-999])
	    self.u_perp_METCorGood_T1JESDown = array('f',[-999])
	    self.u_par_PuppiMETCorGoodJESDown = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodJESDown = array('f',[-999])


	    #JER
	    self.u_par_METCorGood_T1JERUp = array('f',[-999])
	    self.u_perp_METCorGood_T1JERUp = array('f',[-999])
	    self.u_par_PuppiMETCorGoodJERUp = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodJERUp = array('f',[-999])

	    self.u_par_METCorGood_T1JERDown = array('f',[-999])
	    self.u_perp_METCorGood_T1JERDown = array('f',[-999])
	    self.u_par_PuppiMETCorGoodJERDown = array('f',[-999])
	    self.u_perp_PuppiMETCorGoodJERDown = array('f',[-999])


	    #Smear

	    self.u_par_MET_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_perp_MET_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_par_MET_T1SmearUnclusteredDown = array('f',[-999])
	    self.u_perp_MET_T1SmearUnclusteredDown = array('f',[-999])

            #JES
	    self.u_par_MET_T1SmearJESUp = array('f',[-999])
	    self.u_perp_MET_T1SmearJESUp = array('f',[-999])
	    self.u_par_MET_T1SmearJESDown = array('f',[-999])
	    self.u_perp_MET_T1SmearJESDown = array('f',[-999])

	    #JER

	    self.u_par_MET_T1SmearJERUp = array('f',[-999])
	    self.u_perp_MET_T1SmearJERUp = array('f',[-999])
	    self.u_par_MET_T1SmearJERDown = array('f',[-999])
	    self.u_perp_MET_T1SmearJERDown = array('f',[-999])

            ##fix CorGood

	    self.u_par_METCor_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_perp_METCor_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_par_METCor_T1SmearUnclusteredDown = array('f',[-999])
	    self.u_perp_METCor_T1SmearUnclusteredDown = array('f',[-999])

            #JES
	    self.u_par_METCor_T1SmearJESUp = array('f',[-999])
	    self.u_perp_METCor_T1SmearJESUp = array('f',[-999])
	    self.u_par_METCor_T1SmearJESDown = array('f',[-999])
	    self.u_perp_METCor_T1SmearJESDown = array('f',[-999])


	    #JER
	    self.u_par_METCor_T1SmearJERUp = array('f',[-999])
	    self.u_perp_METCor_T1SmearJERUp = array('f',[-999])
	    self.u_par_METCor_T1SmearJERDown = array('f',[-999])
	    self.u_perp_METCor_T1SmearJERDown = array('f',[-999])



	    self.u_par_METCorGood_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearUnclusteredUp = array('f',[-999])
	    self.u_par_METCorGood_T1SmearUnclusteredDown = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearUnclusteredDown = array('f',[-999])

            #JES
	    self.u_par_METCorGood_T1SmearJESUp = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearJESUp = array('f',[-999])
	    self.u_par_METCorGood_T1SmearJESDown = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearJESDown = array('f',[-999])


	    #JER
	    self.u_par_METCorGood_T1SmearJERUp = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearJERUp = array('f',[-999])
	    self.u_par_METCorGood_T1SmearJERDown = array('f',[-999])
	    self.u_perp_METCorGood_T1SmearJERDown = array('f',[-999])

            '''

        self.isTrig_1   = array('f',[0])
        self.isLead_1   = array('f',[0])
        self.isTrigObj   = array('l',[0])

        # jet variables
        #self.njetsold = array('f',[-1]*12)
        self.njets     = array('i',[0])
        self.nbtagL     = array('i',[0])
        self.nbtagM     = array('i',[0])
        self.nbtagT     = array('i',[0])

        self.jflavour     = array('f',[-9.99]*12)
        self.jeta     = array('f',[-9.99]*12)
        self.jpt     = array('f',[-9.99]*12)
        self.btagDeep     = array('f',[-9.99]*12)

        self.bpt_1     = array('f',[0]*12)
        self.bpt_1_tr  = array('f',[0]*12)
        self.beta_1    = array('f',[0]*12)
        self.beta_1_tr = array('f',[0]*12)
        self.bphi_1    = array('f',[0]*12)
        self.bphi_1_tr = array('f',[0]*12)
        self.bcsv_1    = array('f',[0]*12)
        self.bcsvfv_1    = array('f',[0]*12)
      
        self.t.Branch('mll',        self.mll,         'mll/F' )
        self.t.Branch('zll_pt',        self.zll_pt,         'zll_pt/F' )
        self.t.Branch('zll_phi',        self.zll_phi,         'zll_phi/F' )
        
        self.t.Branch('run',              self.run,               'run/l' )
        self.t.Branch('lumi',             self.lumi,              'lumi/l' )
        self.t.Branch('evnt',              self.evnt,               'evnt/l' )
        self.t.Branch('nElectron',              self.nElectron,               'nElectron/I' )
        self.t.Branch('Electron_convVeto',              self.Electron_convVeto,               'Electron_convVeto/F' )
        self.t.Branch('Electron_lostHits',              self.Electron_lostHits,               'Electron_lostHits/I' )

        self.t.Branch('nMuon',              self.nMuon,               'nMuon/I' )
        self.t.Branch('nTau',              self.nTau,               'nTau/I' )
        self.t.Branch('VetoTau',              self.VetoTau,               'VetoTau/I' )
        self.t.Branch('VetoPhoton',              self.VetoPhoton,               'VetoPhoton/I' )
        self.t.Branch('VetoElectron',              self.VetoElectron,               'VetoElectron/I' )
        self.t.Branch('VetoMuon',              self.VetoMuon,               'VetoMuon/I' )
        self.t.Branch('nPU',              self.nPU,               'nPU/I' )
        self.t.Branch('nPUEOOT',              self.nPUEOOT,               'nPUEOOT/I' )
        self.t.Branch('nPULOOT',              self.nPULOOT,               'nPULOOT/I' )
        self.t.Branch('nPUtrue',              self.nPUtrue,               'nPUtrue/F' )
        self.t.Branch('nPV',              self.nPV,               'nPV/I' )
        self.t.Branch('nPVscore',              self.nPVscore,               'nPVscore/F' )
        self.t.Branch('nPVchi2',              self.nPVchi2,               'nPVchi2/F' )
        self.t.Branch('nPVndof',              self.nPVndof,               'nPVndof/F' )
        self.t.Branch('PVx',              self.PVx,               'PVx/F' )
        self.t.Branch('PVy',              self.PVy,               'PVy/F' )
        self.t.Branch('PVz',              self.PVz,               'PVz/F' )
        self.t.Branch('nPVGood',              self.nPVGood,               'nPVGood/I' )
        self.t.Branch('cat',              self.cat,               'cat/I' )
        self.t.Branch('weight',           self.weight,            'weight/F' )
        self.t.Branch('weightPU',           self.weightPU,            'weightPU/F' )
        self.t.Branch('weightPUtrue',           self.weightPUtrue,            'weightPUtrue/F' )
        self.t.Branch('LHEweight',        self.LHEweight,         'LHEweight/F' )
        self.t.Branch('LHE_Njets',        self.LHE_Njets,         'LHE_Njets/i' )
        self.t.Branch('LHEScaleWeights',        self.LHEScaleWeights,         'LHEScaleWeights[9]/F' )
        self.t.Branch('Generator_weight', self.Generator_weight,  'Generator_weight/F' )
        self.t.Branch('electronTriggerWord',  self.electronTriggerWord, 'electronTriggerWord/I' )
        self.t.Branch('muonTriggerWord',      self.muonTriggerWord,  'muonTriggerWord/I' )
        self.t.Branch('whichTriggerWord',      self.whichTriggerWord,  'whichTriggerWord/I' )
        self.t.Branch('whichTriggerWordSubL',      self.whichTriggerWordSubL,  'whichTriggerWordSubL/I' )

        self.t.Branch('L1PreFiringWeight_Nom',        self.L1PreFiringWeight_Nom,        'L1PreFiringWeight_Nom/F')
        self.t.Branch('L1PreFiringWeight_Up',        self.L1PreFiringWeight_Up,        'L1PreFiringWeight_Up/F')
        self.t.Branch('L1PreFiringWeight_Down',        self.L1PreFiringWeight_Down,        'L1PreFiringWeight_Down/F')
        
        self.t.Branch('nGoodElectron',    self.nGoodElectron,     'nGoodElectron/I' )
        self.t.Branch('nGoodMuon',        self.nGoodMuon,         'nGoodMuon/I' )
        self.t.Branch('Flag_hfNoisyHitsFilter',        self.Flag_hfNoisyHitsFilter,         'Flag_hfNoisyHitsFilter/I' )
        self.t.Branch('Flag_BadPFMuonDzFilter',        self.Flag_BadPFMuonDzFilter,         'Flag_BadPFMuonDzFilter/I' )
        
        self.t.Branch('GenPart_statusFlags_1',     self.GenPart_statusFlags_1,     'GenPart_statusFlags_1/I')
        self.t.Branch('GenPart_status_1',     self.GenPart_status_1,     'GenPart_status_1/I')
        self.t.Branch('pt_uncor_1',        self.pt_uncor_1,        'pt_uncor_1/F')
        self.t.Branch('m_uncor_1',        self.m_uncor_1,        'm_uncor_1/F')
        self.t.Branch('gen_match_1', self.gen_match_1, 'gen_match_1/I')
        self.t.Branch('stations_1', self.stations_1, 'stations_1/I')
        self.t.Branch('TrackerL_1', self.TrackerL_1, 'TrackerL_1/I')

        self.t.Branch('IDSF1',        self.IDSF1,        'IDSF1/F')
        self.t.Branch('TrigSF1',        self.TrigSF1,        'TrigSF1/F')
        self.t.Branch('IsoSF1',        self.IsoSF1,        'IsoSF1/F')
        self.t.Branch('IDSF2',        self.IDSF2,        'IDSF2/F')
        self.t.Branch('TrigSF2',        self.TrigSF2,        'TrigSF2/F')
        self.t.Branch('IsoSF2',        self.IsoSF2,        'IsoSF2/F')
        self.t.Branch('IDSF',        self.IDSF,        'IDSF/F')
        self.t.Branch('TrigSF',        self.TrigSF,        'TrigSF/F')
        self.t.Branch('IsoSF',        self.IsoSF,        'IsoSF/F')

        self.t.Branch('pt_1',        self.pt_1,        'pt_1/F')
        self.t.Branch('m_1_tr',     self.m_1_tr,     'm_1_tr/F')
        self.t.Branch('pt_1_tr',     self.pt_1_tr,     'pt_1_tr/F')
        self.t.Branch('phi_1',       self.phi_1,       'phi_1/F')  
        self.t.Branch('phi_1_tr',    self.phi_1_tr,    'phi_1_tr/F')
        self.t.Branch('eta_1',       self.eta_1,       'eta_1/F')    
        self.t.Branch('eta_1_tr',       self.eta_1_tr,       'eta_1_tr/F')    
        self.t.Branch('iso_1',       self.iso_1,       'iso_1/F')
        self.t.Branch('PFiso_1',       self.PFiso_1,       'PFiso_1/F')
        self.t.Branch('q_1',       self.q_1,       'q_1/F')
        self.t.Branch('d0_1',        self.d0_1,        'd0_1/F')
        self.t.Branch('dZ_1',        self.dZ_1,        'dZ_1/F')
        self.t.Branch('Muon_Id_1',       self.Muon_Id_1,       'Muon_Id_1/F')
        self.t.Branch('isGlobal_1',       self.isGlobal_1,       'isGlobal_1/F')
        self.t.Branch('isStandalone_1',       self.isStandalone_1,       'isStandalone_1/F')

        self.t.Branch('highPtId_1',       self.highPtId_1,       'highPtId_1/F')
        self.t.Branch('highPurity_1',       self.highPurity_1,       'highPurity_1/F')
        self.t.Branch('inTimeMuon_1',       self.inTimeMuon_1,       'inTimeMuon_1/F')
        self.t.Branch('ip3d_1',       self.ip3d_1,       'ip3d_1/F')
        self.t.Branch('sip3d_1',       self.sip3d_1,       'sip3d_1/F')


        self.t.Branch('isPFcand_1',       self.isPFcand_1,       'isPFcand_1/F')
        self.t.Branch('isTracker_1',       self.isTracker_1,       'isTracker_1/F')
        self.t.Branch('tightId_1', self.tightId_1, 'tightId_1/F')
        self.t.Branch('tightCharge_1', self.tightCharge_1, 'tightCharge_1/F')
        self.t.Branch('mediumId_1', self.mediumId_1, 'mediumId_1/F')
        self.t.Branch('pfIsoId_1', self.pfIsoId_1, 'pfIsoId_1/F')
        self.t.Branch('mediumPromptId_1', self.mediumPromptId_1, 'mediumPromptId_1/F')
        self.t.Branch('looseId_1', self.looseId_1, 'looseId_1/F')


        self.t.Branch('Electron_mvaFall17V2Iso_WP90_1',              self.Electron_mvaFall17V2Iso_WP90_1,               'Electron_mvaFall17V2Iso_WP90_1/F' )
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_1',              self.Electron_mvaFall17V2noIso_WP90_1,               'Electron_mvaFall17V2noIso_WP90_1/F' )
        self.t.Branch('Electron_cutBased_1',              self.Electron_cutBased_1,               'Electron_cutBased_1/I' )


        self.t.Branch('GenPart_statusFlags_2',     self.GenPart_statusFlags_2,     'GenPart_statusFlags_2/I')
        self.t.Branch('GenPart_status_2',     self.GenPart_status_2,     'GenPart_status_2/I')
        self.t.Branch('pt_uncor_2',        self.pt_uncor_2,        'pt_uncor_2/F')
        self.t.Branch('m_uncor_2',        self.m_uncor_2,        'm_uncor_2/F')
        self.t.Branch('gen_match_2', self.gen_match_2, 'gen_match_2/I')
        self.t.Branch('stations_2', self.stations_2, 'stations_2/I')
        self.t.Branch('TrackerL_2', self.TrackerL_2, 'TrackerL_2/I')


        self.t.Branch('pt_2',        self.pt_2,        'pt_2/F')
        self.t.Branch('m_2_tr',     self.m_2_tr,     'm_2_tr/F')
        self.t.Branch('pt_2_tr',     self.pt_2_tr,     'pt_2_tr/F')
        self.t.Branch('phi_2',       self.phi_2,       'phi_2/F')  
        self.t.Branch('phi_2_tr',    self.phi_2_tr,    'phi_2_tr/F')
        self.t.Branch('eta_2',       self.eta_2,       'eta_2/F')    
        self.t.Branch('eta_2_tr',       self.eta_2_tr,       'eta_2_tr/F')    
        self.t.Branch('iso_2',       self.iso_2,       'iso_2/F')
        self.t.Branch('PFiso_2',       self.PFiso_2,       'PFiso_2/F')
        self.t.Branch('q_2',       self.q_2,       'q_2/F')
        self.t.Branch('d0_2',        self.d0_2,        'd0_2/F')
        self.t.Branch('dZ_2',        self.dZ_2,        'dZ_2/F')
        self.t.Branch('Muon_Id_2',       self.Muon_Id_2,       'Muon_Id_2/F')
        self.t.Branch('isGlobal_2',       self.isGlobal_2,       'isGlobal_2/F')
        self.t.Branch('isStandalone_2',       self.isStandalone_2,       'isStandalone_2/F')

        self.t.Branch('highPtId_2',       self.highPtId_2,       'highPtId_2/F')
        self.t.Branch('highPurity_2',       self.highPurity_2,       'highPurity_2/F')
        self.t.Branch('inTimeMuon_2',       self.inTimeMuon_2,       'inTimeMuon_2/F')
        self.t.Branch('ip3d_2',       self.ip3d_2,       'ip3d_2/F')
        self.t.Branch('sip3d_2',       self.sip3d_2,       'sip3d_2/F')


        self.t.Branch('isPFcand_2',       self.isPFcand_2,       'isPFcand_2/F')
        self.t.Branch('isTracker_2',       self.isTracker_2,       'isTracker_2/F')
        self.t.Branch('tightId_2', self.tightId_2, 'tightId_2/F')
        self.t.Branch('tightCharge_2', self.tightCharge_2, 'tightCharge_2/F')
        self.t.Branch('mediumId_2', self.mediumId_2, 'mediumId_2/F')
        self.t.Branch('pfIsoId_2', self.pfIsoId_2, 'pfIsoId_2/F')
        self.t.Branch('mediumPromptId_2', self.mediumPromptId_2, 'mediumPromptId_2/F')
        self.t.Branch('looseId_2', self.looseId_2, 'looseId_2/F')


        self.t.Branch('Electron_mvaFall17V2Iso_WP90_2',              self.Electron_mvaFall17V2Iso_WP90_2,               'Electron_mvaFall17V2Iso_WP90_2/F' )
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_2',              self.Electron_mvaFall17V2noIso_WP90_2,               'Electron_mvaFall17V2noIso_WP90_2/F' )
        self.t.Branch('Electron_cutBased_2',              self.Electron_cutBased_2,               'Electron_cutBased_2/I' )



        
        # MET variables
        self.t.Branch('metcov00', self.metcov00, 'metcov00/F')
        self.t.Branch('metcov01', self.metcov01, 'metcov01/F')
        self.t.Branch('metcov10', self.metcov10, 'metcov10/F')
        self.t.Branch('metcov11', self.metcov11, 'metcov11/F')

        '''
	self.t.Branch('u_par_RawMET', self.u_par_RawMET, 'u_par_RawMET/F')
	self.t.Branch('u_perp_RawMET', self.u_perp_RawMET, 'u_perp_RawMET/F')
	self.t.Branch('u_par_MET', self.u_par_MET, 'u_par_MET/F')
	self.t.Branch('u_perp_MET', self.u_perp_MET, 'u_perp_MET/F')
	self.t.Branch('u_par_MET_T1', self.u_par_MET_T1, 'u_par_MET_T1/F')
	self.t.Branch('u_perp_MET_T1', self.u_perp_MET_T1, 'u_perp_MET_T1/F')
	self.t.Branch('u_par_METCor_T1', self.u_par_METCor_T1, 'u_par_METCor_T1/F')
	self.t.Branch('u_perp_METCor_T1', self.u_perp_METCor_T1, 'u_perp_METCor_T1/F')
	self.t.Branch('u_par_METCorGood_T1', self.u_par_METCorGood_T1, 'u_par_METCorGood_T1/F')
	self.t.Branch('u_perp_METCorGood_T1', self.u_perp_METCorGood_T1, 'u_perp_METCorGood_T1/F')
	self.t.Branch('u_par_PuppiMET', self.u_par_PuppiMET, 'u_par_PuppiMET/F')
	self.t.Branch('u_perp_PuppiMET', self.u_perp_PuppiMET, 'u_perp_PuppiMET/F')
	self.t.Branch('u_par_PuppiMETCor', self.u_par_PuppiMETCor, 'u_par_PuppiMETCor/F')
	self.t.Branch('u_perp_PuppiMETCor', self.u_perp_PuppiMETCor, 'u_perp_PuppiMETCor/F')
	self.t.Branch('u_par_PuppiMETCorGood', self.u_par_PuppiMETCorGood, 'u_par_PuppiMETCorGood/F')
	self.t.Branch('u_perp_PuppiMETCorGood', self.u_perp_PuppiMETCorGood, 'u_perp_PuppiMETCorGood/F')

        #smear
	self.t.Branch('u_par_MET_T1Smear', self.u_par_MET_T1Smear, 'u_par_MET_T1Smear/F')
	self.t.Branch('u_perp_MET_T1Smear', self.u_perp_MET_T1Smear, 'u_perp_MET_T1Smear/F')
	self.t.Branch('u_par_METCor_T1Smear', self.u_par_METCor_T1Smear, 'u_par_METCor_T1Smear/F')
	self.t.Branch('u_perp_METCor_T1Smear', self.u_perp_METCor_T1Smear, 'u_perp_METCor_T1Smear/F')
	self.t.Branch('u_par_METCorGood_T1Smear', self.u_par_METCorGood_T1Smear, 'u_par_METCorGood_T1Smear/F')
	self.t.Branch('u_perp_METCorGood_T1Smear', self.u_perp_METCorGood_T1Smear, 'u_perp_METCorGood_T1Smear/F')
        '''

	prefixes = ['u_par_', 'u_perp_']
	branches = [
	    'RawMET',
	    'MET',
	    'MET_T1',
	    'METCor_T1',
	    'METCorGood_T1',
	    'PuppiMET',
	    'PuppiMETCor',
	    'PuppiMETCorGood',
	]
	suffixes = ['', 'Smear']

	for prefix in prefixes:
	    for branch in branches:
		for suffix in suffixes:
		    if ('Raw' in branch or 'Puppi' in branch) and suffix == 'Smear':   continue
		    attr_name = prefix + branch + suffix
                    setattr(self, attr_name, array('f', [0]))
		    self.t.Branch(attr_name, getattr(self, attr_name), '{}/F'.format(attr_name))




	self.t.Branch('boson_pt', self.boson_pt, 'boson_pt/F')
	self.t.Branch('boson_phi', self.boson_phi, 'boson_phi/F')
	self.t.Branch('Puppiboson_pt', self.Puppiboson_pt, 'Puppiboson_pt/F')
	self.t.Branch('Puppiboson_phi', self.Puppiboson_phi, 'Puppiboson_phi/F')

        self.t.Branch('RawMET_pt', self.RawMET_pt, 'RawMET_pt /F')
        self.t.Branch('RawMET_phi', self.RawMET_phi, 'RawMET_phi /F')
        self.t.Branch('RawPuppiMET_pt', self.RawPuppiMET_pt, 'RawPuppiMET_pt /F')
        self.t.Branch('RawPuppiMET_phi', self.RawPuppiMET_phi, 'RawPuppiMET_phi /F')

        self.t.Branch('PuppiMET_pt', self.PuppiMET_pt, 'PuppiMET_pt /F')
        self.t.Branch('PuppiMET_phi', self.PuppiMET_phi, 'PuppiMET_phi /F')

	self.t.Branch('MET_phi', self.MET_phi, 'MET_phi /F')
	self.t.Branch('MET_pt', self.MET_pt, 'MET_pt /F')

	self.t.Branch('MET_significance', self.MET_significance, 'MET_significance /F')
	self.t.Branch('MET_T1_pt', self.MET_T1_pt, 'MET_T1_pt /F')
	self.t.Branch('MET_T1_phi', self.MET_T1_phi, 'MET_T1_phi /F')
	self.t.Branch('METCor_T1_pt', self.METCor_T1_pt, 'METCor_T1_pt /F')
	self.t.Branch('METCor_T1_phi', self.METCor_T1_phi, 'METCor_T1_phi /F')
	self.t.Branch('METCorGood_T1_pt', self.METCorGood_T1_pt, 'METCorGood_T1_pt /F')
	self.t.Branch('METCorGood_T1_phi', self.METCorGood_T1_phi, 'METCorGood_T1_phi /F')
	self.t.Branch('PuppiMETCor_pt', self.PuppiMETCor_pt, 'PuppiMETCor_pt /F')
	self.t.Branch('PuppiMETCor_phi', self.PuppiMETCor_phi, 'PuppiMETCor_phi /F')
	self.t.Branch('PuppiMETCorGood_pt', self.PuppiMETCorGood_pt, 'PuppiMETCorGood_pt /F')
	self.t.Branch('PuppiMETCorGood_phi', self.PuppiMETCorGood_phi, 'PuppiMETCorGood_phi /F')
	#smear
	self.t.Branch('MET_T1Smear_pt', self.MET_T1Smear_pt, 'MET_T1Smear_pt /F')
	self.t.Branch('MET_T1Smear_phi', self.MET_T1Smear_phi, 'MET_T1Smear_phi /F')
	self.t.Branch('METCor_T1Smear_pt', self.METCor_T1Smear_pt, 'METCor_T1Smear_pt /F')
	self.t.Branch('METCor_T1Smear_phi', self.METCor_T1Smear_phi, 'METCor_T1Smear_phi /F')
	self.t.Branch('METCorGood_T1Smear_pt', self.METCorGood_T1Smear_pt, 'METCorGood_T1Smear_pt /F')
	self.t.Branch('METCorGood_T1Smear_phi', self.METCorGood_T1Smear_phi, 'METCorGood_T1Smear_phi /F')


        if doSyst :
	    self.t.Branch('u_par_MET_T1UnclusteredUp', self.u_par_MET_T1UnclusteredUp, 'u_par_MET_T1UnclusteredUp/F')
	    self.t.Branch('u_perp_MET_T1UnclusteredUp', self.u_perp_MET_T1UnclusteredUp, 'u_perp_MET_T1UnclusteredUp/F')
	    self.t.Branch('u_par_PuppiMETUnclusteredUp', self.u_par_PuppiMETUnclusteredUp, 'u_par_PuppiMETUnclusteredUp/F')
	    self.t.Branch('u_perp_PuppiMETUnclusteredUp', self.u_perp_PuppiMETUnclusteredUp, 'u_perp_PuppiMETUnclusteredUp/F')

            '''
	    self.t.Branch('boson_ptUnclusteredUp/F', self.boson_ptUnclusteredUp, 'boson_ptUnclusteredUp/F')
	    self.t.Branch('boson_phiUnclusteredUp/F', self.boson_phiUnclusteredUp, 'boson_phiUnclusteredUp/F')
	    self.t.Branch('Puppiboson_ptUnclusteredUp/F', self.Puppiboson_ptUnclusteredUp, 'Puppiboson_ptUnclusteredUp/F')
	    self.t.Branch('Puppiboson_phiUnclusteredUp/F', self.Puppiboson_phiUnclusteredUp, 'Puppiboson_phiUnclusteredUp/F')
            '''


	    self.t.Branch('u_par_MET_T1UnclusteredDown', self.u_par_MET_T1UnclusteredDown, 'u_par_MET_T1UnclusteredDown/F')
	    self.t.Branch('u_perp_MET_T1UnclusteredDown', self.u_perp_MET_T1UnclusteredDown, 'u_perp_MET_T1UnclusteredDown/F')
	    self.t.Branch('u_par_PuppiMETUnclusteredDown', self.u_par_PuppiMETUnclusteredDown, 'u_par_PuppiMETUnclusteredDown/F')
	    self.t.Branch('u_perp_PuppiMETUnclusteredDown', self.u_perp_PuppiMETUnclusteredDown, 'u_perp_PuppiMETUnclusteredDown/F')

            '''
	    self.t.Branch('boson_ptUnclusteredDown/F', self.boson_ptUnclusteredDown, 'boson_ptUnclusteredDown/F')
	    self.t.Branch('boson_phiUnclusteredDown/F', self.boson_phiUnclusteredDown, 'boson_phiUnclusteredDown/F')
	    self.t.Branch('Puppiboson_ptUnclusteredDown/F', self.Puppiboson_ptUnclusteredDown, 'Puppiboson_ptUnclusteredDown/F')
	    self.t.Branch('Puppiboson_phiUnclusteredDown/F', self.Puppiboson_phiUnclusteredDown, 'Puppiboson_phiUnclusteredDown/F')
            '''


	    self.t.Branch('u_par_MET_T1JESUp', self.u_par_MET_T1JESUp, 'u_par_MET_T1JESUp/F')
	    self.t.Branch('u_perp_MET_T1JESUp', self.u_perp_MET_T1JESUp, 'u_perp_MET_T1JESUp/F')
	    self.t.Branch('u_par_PuppiMETJESUp', self.u_par_PuppiMETJESUp, 'u_par_PuppiMETJESUp/F')
	    self.t.Branch('u_perp_PuppiMETJESUp', self.u_perp_PuppiMETJESUp, 'u_perp_PuppiMETJESUp/F')

            '''
	    self.t.Branch('boson_ptJESUp/F', self.boson_ptJESUp, 'boson_ptJESUp/F')
	    self.t.Branch('boson_phiJESUp/F', self.boson_phiJESUp, 'boson_phiJESUp/F')
	    self.t.Branch('Puppiboson_ptJESUp/F', self.Puppiboson_ptJESUp, 'Puppiboson_ptJESUp/F')
	    self.t.Branch('Puppiboson_phiJESUp/F', self.Puppiboson_phiJESUp, 'Puppiboson_phiJESUp/F')
            '''


	    self.t.Branch('u_par_MET_T1JESDown', self.u_par_MET_T1JESDown, 'u_par_MET_T1JESDown/F')
	    self.t.Branch('u_perp_MET_T1JESDown', self.u_perp_MET_T1JESDown, 'u_perp_MET_T1JESDown/F')
	    self.t.Branch('u_par_PuppiMETJESDown', self.u_par_PuppiMETJESDown, 'u_par_PuppiMETJESDown/F')
	    self.t.Branch('u_perp_PuppiMETJESDown', self.u_perp_PuppiMETJESDown, 'u_perp_PuppiMETJESDown/F')

            '''
	    self.t.Branch('boson_ptJESDown/F', self.boson_ptJESDown, 'boson_ptJESDown/F')
	    self.t.Branch('boson_phiJESDown/F', self.boson_phiJESDown, 'boson_phiJESDown/F')
	    self.t.Branch('Puppiboson_ptJESDown/F', self.Puppiboson_ptJESDown, 'Puppiboson_ptJESDown/F')
	    self.t.Branch('Puppiboson_phiJESDown/F', self.Puppiboson_phiJESDown, 'Puppiboson_phiJESDown/F')
            '''


	    self.t.Branch('u_par_MET_T1JERUp', self.u_par_MET_T1JERUp, 'u_par_MET_T1JERUp/F')
	    self.t.Branch('u_perp_MET_T1JERUp', self.u_perp_MET_T1JERUp, 'u_perp_MET_T1JERUp/F')
	    self.t.Branch('u_par_PuppiMETJERUp', self.u_par_PuppiMETJERUp, 'u_par_PuppiMETJERUp/F')
	    self.t.Branch('u_perp_PuppiMETJERUp', self.u_perp_PuppiMETJERUp, 'u_perp_PuppiMETJERUp/F')

            '''
	    self.t.Branch('boson_ptJERUp/F', self.boson_ptJERUp, 'boson_ptJERUp/F')
	    self.t.Branch('boson_phiJERUp/F', self.boson_phiJERUp, 'boson_phiJERUp/F')
	    self.t.Branch('Puppiboson_ptJERUp/F', self.Puppiboson_ptJERUp, 'Puppiboson_ptJERUp/F')
	    self.t.Branch('Puppiboson_phiJERUp/F', self.Puppiboson_phiJERUp, 'Puppiboson_phiJERUp/F')
            '''


	    self.t.Branch('u_par_MET_T1JERDown', self.u_par_MET_T1JERDown, 'u_par_MET_T1JERDown/F')
	    self.t.Branch('u_perp_MET_T1JERDown', self.u_perp_MET_T1JERDown, 'u_perp_MET_T1JERDown/F')
	    self.t.Branch('u_par_PuppiMETJERDown', self.u_par_PuppiMETJERDown, 'u_par_PuppiMETJERDown/F')
	    self.t.Branch('u_perp_PuppiMETJERDown', self.u_perp_PuppiMETJERDown, 'u_perp_PuppiMETJERDown/F')

            '''
	    self.t.Branch('boson_ptJERDown/F', self.boson_ptJERDown, 'boson_ptJERDown/F')
	    self.t.Branch('boson_phiJERDown/F', self.boson_phiJERDown, 'boson_phiJERDown/F')
	    self.t.Branch('Puppiboson_ptJERDown/F', self.Puppiboson_ptJERDown, 'Puppiboson_ptJERDown/F')
	    self.t.Branch('Puppiboson_phiJERDown/F', self.Puppiboson_phiJERDown, 'Puppiboson_phiJERDown/F')
            '''

            #fix
            #fix
	    self.t.Branch('u_par_METCor_T1UnclusteredUp', self.u_par_METCor_T1UnclusteredUp, 'u_par_METCor_T1UnclusteredUp/F')
	    self.t.Branch('u_perp_METCor_T1UnclusteredUp', self.u_perp_METCor_T1UnclusteredUp, 'u_perp_METCor_T1UnclusteredUp/F')
	    self.t.Branch('u_par_PuppiMETCorUnclusteredUp', self.u_par_PuppiMETCorUnclusteredUp, 'u_par_PuppiMETCorUnclusteredUp/F')
	    self.t.Branch('u_perp_PuppiMETCorUnclusteredUp', self.u_perp_PuppiMETCorUnclusteredUp, 'u_perp_PuppiMETCorUnclusteredUp/F')

	    self.t.Branch('u_par_METCor_T1UnclusteredDown', self.u_par_METCor_T1UnclusteredDown, 'u_par_METCor_T1UnclusteredDown/F')
	    self.t.Branch('u_perp_METCor_T1UnclusteredDown', self.u_perp_METCor_T1UnclusteredDown, 'u_perp_METCor_T1UnclusteredDown/F')
	    self.t.Branch('u_par_PuppiMETCorUnclusteredDown', self.u_par_PuppiMETCorUnclusteredDown, 'u_par_PuppiMETCorUnclusteredDown/F')
	    self.t.Branch('u_perp_PuppiMETCorUnclusteredDown', self.u_perp_PuppiMETCorUnclusteredDown, 'u_perp_PuppiMETCorUnclusteredDown/F')


	    self.t.Branch('u_par_METCor_T1JESUp', self.u_par_METCor_T1JESUp, 'u_par_METCor_T1JESUp/F')
	    self.t.Branch('u_perp_METCor_T1JESUp', self.u_perp_METCor_T1JESUp, 'u_perp_METCor_T1JESUp/F')
	    self.t.Branch('u_par_PuppiMETCorJESUp', self.u_par_PuppiMETCorJESUp, 'u_par_PuppiMETCorJESUp/F')
	    self.t.Branch('u_perp_PuppiMETCorJESUp', self.u_perp_PuppiMETCorJESUp, 'u_perp_PuppiMETCorJESUp/F')


	    self.t.Branch('u_par_METCor_T1JESDown', self.u_par_METCor_T1JESDown, 'u_par_METCor_T1JESDown/F')
	    self.t.Branch('u_perp_METCor_T1JESDown', self.u_perp_METCor_T1JESDown, 'u_perp_METCor_T1JESDown/F')
	    self.t.Branch('u_par_PuppiMETCorJESDown', self.u_par_PuppiMETCorJESDown, 'u_par_PuppiMETCorJESDown/F')
	    self.t.Branch('u_perp_PuppiMETCorJESDown', self.u_perp_PuppiMETCorJESDown, 'u_perp_PuppiMETCorJESDown/F')


	    self.t.Branch('u_par_METCor_T1JERUp', self.u_par_METCor_T1JERUp, 'u_par_METCor_T1JERUp/F')
	    self.t.Branch('u_perp_METCor_T1JERUp', self.u_perp_METCor_T1JERUp, 'u_perp_METCor_T1JERUp/F')
	    self.t.Branch('u_par_PuppiMETCorJERUp', self.u_par_PuppiMETCorJERUp, 'u_par_PuppiMETCorJERUp/F')
	    self.t.Branch('u_perp_PuppiMETCorJERUp', self.u_perp_PuppiMETCorJERUp, 'u_perp_PuppiMETCorJERUp/F')

	    self.t.Branch('u_par_METCor_T1JERDown', self.u_par_METCor_T1JERDown, 'u_par_METCor_T1JERDown/F')
	    self.t.Branch('u_perp_METCor_T1JERDown', self.u_perp_METCor_T1JERDown, 'u_perp_METCor_T1JERDown/F')
	    self.t.Branch('u_par_PuppiMETCorJERDown', self.u_par_PuppiMETCorJERDown, 'u_par_PuppiMETCorJERDown/F')
	    self.t.Branch('u_perp_PuppiMETCorJERDown', self.u_perp_PuppiMETCorJERDown, 'u_perp_PuppiMETCorJERDown/F')

            #CorGood
	    self.t.Branch('u_par_METCorGood_T1UnclusteredUp', self.u_par_METCorGood_T1UnclusteredUp, 'u_par_METCorGood_T1UnclusteredUp/F')
	    self.t.Branch('u_perp_METCorGood_T1UnclusteredUp', self.u_perp_METCorGood_T1UnclusteredUp, 'u_perp_METCorGood_T1UnclusteredUp/F')
	    self.t.Branch('u_par_PuppiMETCorGoodUnclusteredUp', self.u_par_PuppiMETCorGoodUnclusteredUp, 'u_par_PuppiMETCorGoodUnclusteredUp/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodUnclusteredUp', self.u_perp_PuppiMETCorGoodUnclusteredUp, 'u_perp_PuppiMETCorGoodUnclusteredUp/F')

	    self.t.Branch('u_par_METCorGood_T1UnclusteredDown', self.u_par_METCorGood_T1UnclusteredDown, 'u_par_METCorGood_T1UnclusteredDown/F')
	    self.t.Branch('u_perp_METCorGood_T1UnclusteredDown', self.u_perp_METCorGood_T1UnclusteredDown, 'u_perp_METCorGood_T1UnclusteredDown/F')
	    self.t.Branch('u_par_PuppiMETCorGoodUnclusteredDown', self.u_par_PuppiMETCorGoodUnclusteredDown, 'u_par_PuppiMETCorGoodUnclusteredDown/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodUnclusteredDown', self.u_perp_PuppiMETCorGoodUnclusteredDown, 'u_perp_PuppiMETCorGoodUnclusteredDown/F')


	    self.t.Branch('u_par_METCorGood_T1JESUp', self.u_par_METCorGood_T1JESUp, 'u_par_METCorGood_T1JESUp/F')
	    self.t.Branch('u_perp_METCorGood_T1JESUp', self.u_perp_METCorGood_T1JESUp, 'u_perp_METCorGood_T1JESUp/F')
	    self.t.Branch('u_par_PuppiMETCorGoodJESUp', self.u_par_PuppiMETCorGoodJESUp, 'u_par_PuppiMETCorGoodJESUp/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodJESUp', self.u_perp_PuppiMETCorGoodJESUp, 'u_perp_PuppiMETCorGoodJESUp/F')


	    self.t.Branch('u_par_METCorGood_T1JESDown', self.u_par_METCorGood_T1JESDown, 'u_par_METCorGood_T1JESDown/F')
	    self.t.Branch('u_perp_METCorGood_T1JESDown', self.u_perp_METCorGood_T1JESDown, 'u_perp_METCorGood_T1JESDown/F')
	    self.t.Branch('u_par_PuppiMETCorGoodJESDown', self.u_par_PuppiMETCorGoodJESDown, 'u_par_PuppiMETCorGoodJESDown/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodJESDown', self.u_perp_PuppiMETCorGoodJESDown, 'u_perp_PuppiMETCorGoodJESDown/F')


	    self.t.Branch('u_par_METCorGood_T1JERUp', self.u_par_METCorGood_T1JERUp, 'u_par_METCorGood_T1JERUp/F')
	    self.t.Branch('u_perp_METCorGood_T1JERUp', self.u_perp_METCorGood_T1JERUp, 'u_perp_METCorGood_T1JERUp/F')
	    self.t.Branch('u_par_PuppiMETCorGoodJERUp', self.u_par_PuppiMETCorGoodJERUp, 'u_par_PuppiMETCorGoodJERUp/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodJERUp', self.u_perp_PuppiMETCorGoodJERUp, 'u_perp_PuppiMETCorGoodJERUp/F')

	    self.t.Branch('u_par_METCorGood_T1JERDown', self.u_par_METCorGood_T1JERDown, 'u_par_METCorGood_T1JERDown/F')
	    self.t.Branch('u_perp_METCorGood_T1JERDown', self.u_perp_METCorGood_T1JERDown, 'u_perp_METCorGood_T1JERDown/F')
	    self.t.Branch('u_par_PuppiMETCorGoodJERDown', self.u_par_PuppiMETCorGoodJERDown, 'u_par_PuppiMETCorGoodJERDown/F')
	    self.t.Branch('u_perp_PuppiMETCorGoodJERDown', self.u_perp_PuppiMETCorGoodJERDown, 'u_perp_PuppiMETCorGoodJERDown/F')


            #fix
	    self.t.Branch('u_par_MET_T1SmearUnclusteredUp', self.u_par_MET_T1SmearUnclusteredUp, 'u_par_MET_T1SmearUnclusteredUp/F')
	    self.t.Branch('u_perp_MET_T1SmearUnclusteredUp', self.u_perp_MET_T1SmearUnclusteredUp, 'u_perp_MET_T1SmearUnclusteredUp/F')

	    self.t.Branch('u_par_MET_T1SmearUnclusteredDown', self.u_par_MET_T1SmearUnclusteredDown, 'u_par_MET_T1SmearUnclusteredDown/F')
	    self.t.Branch('u_perp_MET_T1SmearUnclusteredDown', self.u_perp_MET_T1SmearUnclusteredDown, 'u_perp_MET_T1SmearUnclusteredDown/F')

	    self.t.Branch('u_par_MET_T1SmearJESUp', self.u_par_MET_T1SmearJESUp, 'u_par_MET_T1SmearJESUp/F')
	    self.t.Branch('u_perp_MET_T1SmearJESUp', self.u_perp_MET_T1SmearJESUp, 'u_perp_MET_T1SmearJESUp/F')

	    self.t.Branch('u_par_MET_T1SmearJESDown', self.u_par_MET_T1SmearJESDown, 'u_par_MET_T1SmearJESDown/F')
	    self.t.Branch('u_perp_MET_T1SmearJESDown', self.u_perp_MET_T1SmearJESDown, 'u_perp_MET_T1SmearJESDown/F')

	    self.t.Branch('u_par_MET_T1SmearJERUp', self.u_par_MET_T1SmearJERUp, 'u_par_MET_T1SmearJERUp/F')
	    self.t.Branch('u_perp_MET_T1SmearJERUp', self.u_perp_MET_T1SmearJERUp, 'u_perp_MET_T1SmearJERUp/F')

	    self.t.Branch('u_par_MET_T1SmearJERDown', self.u_par_MET_T1SmearJERDown, 'u_par_MET_T1SmearJERDown/F')
	    self.t.Branch('u_perp_MET_T1SmearJERDown', self.u_perp_MET_T1SmearJERDown, 'u_perp_MET_T1SmearJERDown/F')

	    self.t.Branch('u_par_METCor_T1SmearUnclusteredUp', self.u_par_METCor_T1SmearUnclusteredUp, 'u_par_METCor_T1SmearUnclusteredUp/F')
	    self.t.Branch('u_perp_METCor_T1SmearUnclusteredUp', self.u_perp_METCor_T1SmearUnclusteredUp, 'u_perp_METCor_T1SmearUnclusteredUp/F')

	    self.t.Branch('u_par_METCor_T1SmearUnclusteredDown', self.u_par_METCor_T1SmearUnclusteredDown, 'u_par_METCor_T1SmearUnclusteredDown/F')
	    self.t.Branch('u_perp_METCor_T1SmearUnclusteredDown', self.u_perp_METCor_T1SmearUnclusteredDown, 'u_perp_METCor_T1SmearUnclusteredDown/F')

	    self.t.Branch('u_par_METCor_T1SmearJESUp', self.u_par_METCor_T1SmearJESUp, 'u_par_METCor_T1SmearJESUp/F')
	    self.t.Branch('u_perp_METCor_T1SmearJESUp', self.u_perp_METCor_T1SmearJESUp, 'u_perp_METCor_T1SmearJESUp/F')

	    self.t.Branch('u_par_METCor_T1SmearJESDown', self.u_par_METCor_T1SmearJESDown, 'u_par_METCor_T1SmearJESDown/F')
	    self.t.Branch('u_perp_METCor_T1SmearJESDown', self.u_perp_METCor_T1SmearJESDown, 'u_perp_METCor_T1SmearJESDown/F')


	    self.t.Branch('u_par_METCor_T1SmearJERUp', self.u_par_METCor_T1SmearJERUp, 'u_par_METCor_T1SmearJERUp/F')
	    self.t.Branch('u_perp_METCor_T1SmearJERUp', self.u_perp_METCor_T1SmearJERUp, 'u_perp_METCor_T1SmearJERUp/F')

	    self.t.Branch('u_par_METCor_T1SmearJERDown', self.u_par_METCor_T1SmearJERDown, 'u_par_METCor_T1SmearJERDown/F')
	    self.t.Branch('u_perp_METCor_T1SmearJERDown', self.u_perp_METCor_T1SmearJERDown, 'u_perp_METCor_T1SmearJERDown/F')
  
            #CorGood
	    self.t.Branch('u_par_METCorGood_T1SmearUnclusteredUp', self.u_par_METCorGood_T1SmearUnclusteredUp, 'u_par_METCorGood_T1SmearUnclusteredUp/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearUnclusteredUp', self.u_perp_METCorGood_T1SmearUnclusteredUp, 'u_perp_METCorGood_T1SmearUnclusteredUp/F')

	    self.t.Branch('u_par_METCorGood_T1SmearUnclusteredDown', self.u_par_METCorGood_T1SmearUnclusteredDown, 'u_par_METCorGood_T1SmearUnclusteredDown/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearUnclusteredDown', self.u_perp_METCorGood_T1SmearUnclusteredDown, 'u_perp_METCorGood_T1SmearUnclusteredDown/F')

	    self.t.Branch('u_par_METCorGood_T1SmearJESUp', self.u_par_METCorGood_T1SmearJESUp, 'u_par_METCorGood_T1SmearJESUp/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearJESUp', self.u_perp_METCorGood_T1SmearJESUp, 'u_perp_METCorGood_T1SmearJESUp/F')

	    self.t.Branch('u_par_METCorGood_T1SmearJESDown', self.u_par_METCorGood_T1SmearJESDown, 'u_par_METCorGood_T1SmearJESDown/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearJESDown', self.u_perp_METCorGood_T1SmearJESDown, 'u_perp_METCorGood_T1SmearJESDown/F')


	    self.t.Branch('u_par_METCorGood_T1SmearJERUp', self.u_par_METCorGood_T1SmearJERUp, 'u_par_METCorGood_T1SmearJERUp/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearJERUp', self.u_perp_METCorGood_T1SmearJERUp, 'u_perp_METCorGood_T1SmearJERUp/F')

	    self.t.Branch('u_par_METCorGood_T1SmearJERDown', self.u_par_METCorGood_T1SmearJERDown, 'u_par_METCorGood_T1SmearJERDown/F')
	    self.t.Branch('u_perp_METCorGood_T1SmearJERDown', self.u_perp_METCorGood_T1SmearJERDown, 'u_perp_METCorGood_T1SmearJERDown/F')



	    self.t.Branch('PuppiMET_ptJESUp', self.PuppiMET_ptJESUp, 'PuppiMET_ptJESUp /F')
	    self.t.Branch('PuppiMET_ptJESDown', self.PuppiMET_ptJESDown, 'PuppiMET_ptJESDown /F')
	    self.t.Branch('PuppiMET_ptJERUp', self.PuppiMET_ptJERUp, 'PuppiMET_ptJERUp /F')
	    self.t.Branch('PuppiMET_ptJERDown', self.PuppiMET_ptJERDown, 'PuppiMET_ptJERDown /F')
	    self.t.Branch('PuppiMET_ptUnclusteredUp', self.PuppiMET_ptUnclusteredUp, 'PuppiMET_ptUnclusteredUp /F')
	    self.t.Branch('PuppiMET_ptUnclusteredDown', self.PuppiMET_ptUnclusteredDown, 'PuppiMET_ptUnclusteredDown /F')

	    self.t.Branch('PuppiMET_phiJESUp', self.PuppiMET_phiJESUp, 'PuppiMET_phiJESUp /F')
	    self.t.Branch('PuppiMET_phiJESDown', self.PuppiMET_phiJESDown, 'PuppiMET_phiJESDown /F')
	    self.t.Branch('PuppiMET_phiJERUp', self.PuppiMET_phiJERUp, 'PuppiMET_phiJERUp /F')
	    self.t.Branch('PuppiMET_phiJERDown', self.PuppiMET_phiJERDown, 'PuppiMET_phiJERDown /F')
	    self.t.Branch('PuppiMET_phiUnclusteredUp', self.PuppiMET_phiUnclusteredUp, 'PuppiMET_phiUnclusteredUp /F')
	    self.t.Branch('PuppiMET_phiUnclusteredDown', self.PuppiMET_phiUnclusteredDown, 'PuppiMET_phiUnclusteredDown /F')

	    self.t.Branch('MET_ptJESUp', self.MET_ptJESUp, 'MET_ptJESUp /F')
	    self.t.Branch('MET_ptJESDown', self.MET_ptJESDown, 'MET_ptJESDown /F')
	    self.t.Branch('MET_ptJERUp', self.MET_ptJERUp, 'MET_ptJERUp /F')
	    self.t.Branch('MET_ptJERDown', self.MET_ptJERDown, 'MET_ptJERDown /F')
	    self.t.Branch('MET_ptUnclusteredUp', self.MET_ptUnclusteredUp, 'MET_ptUnclusteredUp /F')
	    self.t.Branch('MET_ptUnclusteredDown', self.MET_ptUnclusteredDown, 'MET_ptUnclusteredDown /F')

	    self.t.Branch('MET_phiJESUp', self.MET_phiJESUp, 'MET_phiJESUp /F')
	    self.t.Branch('MET_phiJESDown', self.MET_phiJESDown, 'MET_phiJESDown /F')
	    self.t.Branch('MET_phiJERUp', self.MET_phiJERUp, 'MET_phiJERUp /F')
	    self.t.Branch('MET_phiJERDown', self.MET_phiJERDown, 'MET_phiJERDown /F')
	    self.t.Branch('MET_phiUnclusteredUp', self.MET_phiUnclusteredUp, 'MET_phiUnclusteredUp /F')
	    self.t.Branch('MET_phiUnclusteredDown', self.MET_phiUnclusteredDown, 'MET_phiUnclusteredDown /F')




	    self.t.Branch('MET_T1_ptJESUp', self.MET_T1_ptJESUp, 'MET_T1_ptJESUp /F')
	    self.t.Branch('MET_T1_phiJESUp', self.MET_T1_phiJESUp, 'MET_T1_phiJESUp /F')
	    self.t.Branch('MET_T1_ptJESDown', self.MET_T1_ptJESDown, 'MET_T1_ptJESDown /F')
	    self.t.Branch('MET_T1_phiJESDown', self.MET_T1_phiJESDown, 'MET_T1_phiJESDown /F')
	    self.t.Branch('MET_T1_ptJERUp', self.MET_T1_ptJERUp, 'MET_T1_ptJERUp /F')
	    self.t.Branch('MET_T1_phiJERUp', self.MET_T1_phiJERUp, 'MET_T1_phiJERUp /F')
	    self.t.Branch('MET_T1_ptJERDown', self.MET_T1_ptJERDown, 'MET_T1_ptJERDown /F')
	    self.t.Branch('MET_T1_phiJERDown', self.MET_T1_phiJERDown, 'MET_T1_phiJERDown /F')
	    self.t.Branch('MET_T1_ptUnclusteredUp', self.MET_T1_ptUnclusteredUp, 'MET_T1_ptUnclusteredUp /F')
	    self.t.Branch('MET_T1_ptUnclusteredDown', self.MET_T1_ptUnclusteredDown, 'MET_T1_ptUnclusteredDown /F')
	    self.t.Branch('MET_T1_phiUnclusteredUp', self.MET_T1_phiUnclusteredUp, 'MET_T1_phiUnclusteredUp /F')
	    self.t.Branch('MET_T1_phiUnclusteredDown', self.MET_T1_phiUnclusteredDown, 'MET_T1_phiUnclusteredDown /F')

	    self.t.Branch('METCor_T1_ptJESUp', self.METCor_T1_ptJESUp, 'METCor_T1_ptJESUp/F')
	    self.t.Branch('METCor_T1_phiJESUp', self.METCor_T1_phiJESUp, 'METCor_T1_phiJESUp /F')
	    self.t.Branch('METCor_T1_ptJESDown', self.METCor_T1_ptJESDown, 'METCor_T1_ptJESDown /F')
	    self.t.Branch('METCor_T1_phiJESDown', self.METCor_T1_phiJESDown, 'METCor_T1_phiJESDown /F')
	    self.t.Branch('METCor_T1_ptJERUp', self.METCor_T1_ptJERUp, 'METCor_T1_ptJERUp /F')
	    self.t.Branch('METCor_T1_phiJERUp', self.METCor_T1_phiJERUp, 'METCor_T1_phiJERUp /F')
	    self.t.Branch('METCor_T1_ptJERDown', self.METCor_T1_ptJERDown, 'METCor_T1_ptJERDown /F')
	    self.t.Branch('METCor_T1_phiJERDown', self.METCor_T1_phiJERDown, 'METCor_T1_phiJERDown /F')
	    self.t.Branch('METCor_T1_ptUnclusteredUp', self.METCor_T1_ptUnclusteredUp, 'METCor_T1_ptUnclusteredUp /F')
	    self.t.Branch('METCor_T1_ptUnclusteredDown', self.METCor_T1_ptUnclusteredDown, 'METCor_T1_ptUnclusteredDown /F')
	    self.t.Branch('METCor_T1_phiUnclusteredUp', self.METCor_T1_phiUnclusteredUp, 'METCor_T1_phiUnclusteredUp /F')
	    self.t.Branch('METCor_T1_phiUnclusteredDown', self.METCor_T1_phiUnclusteredDown, 'METCor_T1_phiUnclusteredDown /F')

	    self.t.Branch('METCorGood_T1_ptJESUp', self.METCorGood_T1_ptJESUp, 'METCorGood_T1_ptJESUp /F')
	    self.t.Branch('METCorGood_T1_phiJESUp', self.METCorGood_T1_phiJESUp, 'METCorGood_T1_phiJESUp /F')
	    self.t.Branch('METCorGood_T1_ptJESDown', self.METCorGood_T1_ptJESDown, 'METCorGood_T1_ptJESDown /F')
	    self.t.Branch('METCorGood_T1_phiJESDown', self.METCorGood_T1_phiJESDown, 'METCorGood_T1_phiJESDown /F')
	    self.t.Branch('METCorGood_T1_ptJERUp', self.METCorGood_T1_ptJERUp, 'METCorGood_T1_ptJERUp /F')
	    self.t.Branch('METCorGood_T1_phiJERUp', self.METCorGood_T1_phiJERUp, 'METCorGood_T1_phiJERUp /F')
	    self.t.Branch('METCorGood_T1_ptJERDown', self.METCorGood_T1_ptJERDown, 'METCorGood_T1_ptJERDown /F')
	    self.t.Branch('METCorGood_T1_phiJERDown', self.METCorGood_T1_phiJERDown, 'METCorGood_T1_phiJERDown /F')
	    self.t.Branch('METCorGood_T1_ptUnclusteredUp', self.METCorGood_T1_ptUnclusteredUp, 'METCorGood_T1_ptUnclusteredUp /F')
	    self.t.Branch('METCorGood_T1_ptUnclusteredDown', self.METCorGood_T1_ptUnclusteredDown, 'METCorGood_T1_ptUnclusteredDown /F')
	    self.t.Branch('METCorGood_T1_phiUnclusteredUp', self.METCorGood_T1_phiUnclusteredUp, 'METCorGood_T1_phiUnclusteredUp /F')
	    self.t.Branch('METCorGood_T1_phiUnclusteredDown', self.METCorGood_T1_phiUnclusteredDown, 'METCorGood_T1_phiUnclusteredDown /F')


	    self.t.Branch('PuppiMETCor_ptJESUp', self.PuppiMETCor_ptJESUp, 'PuppiMETCor_ptJESUp /F')
	    self.t.Branch('PuppiMETCor_phiJESUp', self.PuppiMETCor_phiJESUp, 'PuppiMETCor_phiJESUp /F')
	    self.t.Branch('PuppiMETCor_ptJESDown', self.PuppiMETCor_ptJESDown, 'PuppiMETCor_ptJESDown /F')
	    self.t.Branch('PuppiMETCor_phiJESDown', self.PuppiMETCor_phiJESDown, 'PuppiMETCor_phiJESDown /F')
	    self.t.Branch('PuppiMETCor_ptJERUp', self.PuppiMETCor_ptJERUp, 'PuppiMETCor_ptJERUp /F')
	    self.t.Branch('PuppiMETCor_phiJERUp', self.PuppiMETCor_phiJERUp, 'PuppiMETCor_phiJERUp /F')
	    self.t.Branch('PuppiMETCor_ptJERDown', self.PuppiMETCor_ptJERDown, 'PuppiMETCor_ptJERDown /F')
	    self.t.Branch('PuppiMETCor_phiJERDown', self.PuppiMETCor_phiJERDown, 'PuppiMETCor_phiJERDown /F')
	    self.t.Branch('PuppiMETCor_ptUnclusteredUp', self.PuppiMETCor_ptUnclusteredUp, 'PuppiMETCor_ptUnclusteredUp /F')
	    self.t.Branch('PuppiMETCor_ptUnclusteredDown', self.PuppiMETCor_ptUnclusteredDown, 'PuppiMETCor_ptUnclusteredDown /F')
	    self.t.Branch('PuppiMETCor_phiUnclusteredUp', self.PuppiMETCor_phiUnclusteredUp, 'PuppiMETCor_phiUnclusteredUp /F')
	    self.t.Branch('PuppiMETCor_phiUnclusteredDown', self.PuppiMETCor_phiUnclusteredDown, 'PuppiMETCor_phiUnclusteredDown /F')

	    self.t.Branch('PuppiMETCorGood_ptJESUp', self.PuppiMETCorGood_ptJESUp, 'PuppiMETCorGood_ptJESUp /F')
	    self.t.Branch('PuppiMETCorGood_phiJESUp', self.PuppiMETCorGood_phiJESUp, 'PuppiMETCorGood_phiJESUp /F')
	    self.t.Branch('PuppiMETCorGood_ptJESDown', self.PuppiMETCorGood_ptJESDown, 'PuppiMETCorGood_ptJESDown /F')
	    self.t.Branch('PuppiMETCorGood_phiJESDown', self.PuppiMETCorGood_phiJESDown, 'PuppiMETCorGood_phiJESDown /F')
	    self.t.Branch('PuppiMETCorGood_ptJERUp', self.PuppiMETCorGood_ptJERUp, 'PuppiMETCorGood_ptJERUp /F')
	    self.t.Branch('PuppiMETCorGood_phiJERUp', self.PuppiMETCorGood_phiJERUp, 'PuppiMETCorGood_phiJERUp /F')
	    self.t.Branch('PuppiMETCorGood_ptJERDown', self.PuppiMETCorGood_ptJERDown, 'PuppiMETCorGood_ptJERDown /F')
	    self.t.Branch('PuppiMETCorGood_phiJERDown', self.PuppiMETCorGood_phiJERDown, 'PuppiMETCorGood_phiJERDown /F')
	    self.t.Branch('PuppiMETCorGood_ptUnclusteredUp', self.PuppiMETCorGood_ptUnclusteredUp, 'PuppiMETCorGood_ptUnclusteredUp /F')
	    self.t.Branch('PuppiMETCorGood_ptUnclusteredDown', self.PuppiMETCorGood_ptUnclusteredDown, 'PuppiMETCorGood_ptUnclusteredDown /F')
	    self.t.Branch('PuppiMETCorGood_phiUnclusteredUp', self.PuppiMETCorGood_phiUnclusteredUp, 'PuppiMETCorGood_phiUnclusteredUp /F')
	    self.t.Branch('PuppiMETCorGood_phiUnclusteredDown', self.PuppiMETCorGood_phiUnclusteredDown, 'PuppiMETCorGood_phiUnclusteredDown /F')

            #smear
	    self.t.Branch('MET_T1Smear_ptJESUp', self.MET_T1Smear_ptJESUp, 'MET_T1Smear_ptJESUp /F')
	    self.t.Branch('MET_T1Smear_phiJESUp', self.MET_T1Smear_phiJESUp, 'MET_T1Smear_phiJESUp /F')
	    self.t.Branch('MET_T1Smear_ptJESDown', self.MET_T1Smear_ptJESDown, 'MET_T1Smear_ptJESDown /F')
	    self.t.Branch('MET_T1Smear_phiJESDown', self.MET_T1Smear_phiJESDown, 'MET_T1Smear_phiJESDown /F')
	    self.t.Branch('MET_T1Smear_ptJERUp', self.MET_T1Smear_ptJERUp, 'MET_T1Smear_ptJERUp /F')
	    self.t.Branch('MET_T1Smear_phiJERUp', self.MET_T1Smear_phiJERUp, 'MET_T1Smear_phiJERUp /F')
	    self.t.Branch('MET_T1Smear_ptJERDown', self.MET_T1Smear_ptJERDown, 'MET_T1Smear_ptJERDown /F')
	    self.t.Branch('MET_T1Smear_phiJERDown', self.MET_T1Smear_phiJERDown, 'MET_T1Smear_phiJERDown /F')
	    self.t.Branch('MET_T1Smear_ptUnclusteredUp', self.MET_T1Smear_ptUnclusteredUp, 'MET_T1Smear_ptUnclusteredUp /F')
	    self.t.Branch('MET_T1Smear_ptUnclusteredDown', self.MET_T1Smear_ptUnclusteredDown, 'MET_T1Smear_ptUnclusteredDown /F')
	    self.t.Branch('MET_T1Smear_phiUnclusteredUp', self.MET_T1Smear_phiUnclusteredUp, 'MET_T1Smear_phiUnclusteredUp /F')
	    self.t.Branch('MET_T1Smear_phiUnclusteredDown', self.MET_T1Smear_phiUnclusteredDown, 'MET_T1Smear_phiUnclusteredDown /F')

	    self.t.Branch('METCor_T1Smear_ptJESUp', self.METCor_T1Smear_ptJESUp, 'METCor_T1Smear_ptJESUp/F')
	    self.t.Branch('METCor_T1Smear_phiJESUp', self.METCor_T1Smear_phiJESUp, 'METCor_T1Smear_phiJESUp /F')
	    self.t.Branch('METCor_T1Smear_ptJESDown', self.METCor_T1Smear_ptJESDown, 'METCor_T1Smear_ptJESDown /F')
	    self.t.Branch('METCor_T1Smear_phiJESDown', self.METCor_T1Smear_phiJESDown, 'METCor_T1Smear_phiJESDown /F')
	    self.t.Branch('METCor_T1Smear_ptJERUp', self.METCor_T1Smear_ptJERUp, 'METCor_T1Smear_ptJERUp /F')
	    self.t.Branch('METCor_T1Smear_phiJERUp', self.METCor_T1Smear_phiJERUp, 'METCor_T1Smear_phiJERUp /F')
	    self.t.Branch('METCor_T1Smear_ptJERDown', self.METCor_T1Smear_ptJERDown, 'METCor_T1Smear_ptJERDown /F')
	    self.t.Branch('METCor_T1Smear_phiJERDown', self.METCor_T1Smear_phiJERDown, 'METCor_T1Smear_phiJERDown /F')
	    self.t.Branch('METCor_T1Smear_ptUnclusteredUp', self.METCor_T1Smear_ptUnclusteredUp, 'METCor_T1Smear_ptUnclusteredUp /F')
	    self.t.Branch('METCor_T1Smear_ptUnclusteredDown', self.METCor_T1Smear_ptUnclusteredDown, 'METCor_T1Smear_ptUnclusteredDown /F')
	    self.t.Branch('METCor_T1Smear_phiUnclusteredUp', self.METCor_T1Smear_phiUnclusteredUp, 'METCor_T1Smear_phiUnclusteredUp /F')
	    self.t.Branch('METCor_T1Smear_phiUnclusteredDown', self.METCor_T1Smear_phiUnclusteredDown, 'METCor_T1Smear_phiUnclusteredDown /F')

	    self.t.Branch('METCorGood_T1Smear_ptJESUp', self.METCorGood_T1Smear_ptJESUp, 'METCorGood_T1Smear_ptJESUp /F')
	    self.t.Branch('METCorGood_T1Smear_phiJESUp', self.METCorGood_T1Smear_phiJESUp, 'METCorGood_T1Smear_phiJESUp /F')
	    self.t.Branch('METCorGood_T1Smear_ptJESDown', self.METCorGood_T1Smear_ptJESDown, 'METCorGood_T1Smear_ptJESDown /F')
	    self.t.Branch('METCorGood_T1Smear_phiJESDown', self.METCorGood_T1Smear_phiJESDown, 'METCorGood_T1Smear_phiJESDown /F')
	    self.t.Branch('METCorGood_T1Smear_ptJERUp', self.METCorGood_T1Smear_ptJERUp, 'METCorGood_T1Smear_ptJERUp /F')
	    self.t.Branch('METCorGood_T1Smear_phiJERUp', self.METCorGood_T1Smear_phiJERUp, 'METCorGood_T1Smear_phiJERUp /F')
	    self.t.Branch('METCorGood_T1Smear_ptJERDown', self.METCorGood_T1Smear_ptJERDown, 'METCorGood_T1Smear_ptJERDown /F')
	    self.t.Branch('METCorGood_T1Smear_phiJERDown', self.METCorGood_T1Smear_phiJERDown, 'METCorGood_T1Smear_phiJERDown /F')
	    self.t.Branch('METCorGood_T1Smear_ptUnclusteredUp', self.METCorGood_T1Smear_ptUnclusteredUp, 'METCorGood_T1Smear_ptUnclusteredUp /F')
	    self.t.Branch('METCorGood_T1Smear_ptUnclusteredDown', self.METCorGood_T1Smear_ptUnclusteredDown, 'METCorGood_T1Smear_ptUnclusteredDown /F')
	    self.t.Branch('METCorGood_T1Smear_phiUnclusteredUp', self.METCorGood_T1Smear_phiUnclusteredUp, 'METCorGood_T1Smear_phiUnclusteredUp /F')
	    self.t.Branch('METCorGood_T1Smear_phiUnclusteredDown', self.METCorGood_T1Smear_phiUnclusteredDown, 'METCorGood_T1Smear_phiUnclusteredDown /F')



        # trigger sf
        self.t.Branch('isTrig_1',  self.isTrig_1, 'isTrig_1/F' )
        self.t.Branch('isLead_1',  self.isLead_1, 'isLead_1/F' )
        self.t.Branch('isTrigObj',  self.isTrigObj, 'isTrigObj/l' )


        # jet variables
        #self.t.Branch('njetsold', self.njetsold, 'njetsold[8]/F') 
        #self.t.Branch('nbtagold', self.nbtagold, 'nbtagold[8]/F')
        self.t.Branch('njets', self.njets, 'njets/i')
        self.t.Branch('nbtagL', self.nbtagL, 'nbtagL/i')
        self.t.Branch('nbtagM', self.nbtagM, 'nbtagM/i')
        self.t.Branch('nbtagT', self.nbtagT, 'nbtagT/i')

        self.t.Branch('jflavour',     self.jflavour,     'jflavour[12]/i' )
        self.t.Branch('jeta',     self.jeta,     'jeta[12]/F' )
        self.t.Branch('jpt',     self.jpt,     'jpt[12]/F' )
        self.t.Branch('btagDeep', self.btagDeep, 'btagDeep[12]/F')

        if doSyst : 
                #Book the branches and the arrays needed to store variables
		for i, v in enumerate(self.allsystMET):
                 
                    iMET= 'MET'
                    iiMET=iMET+'_noES'
	            self.t.Branch(iMET, self.list_of_arrays[i], '{0:s}/F'.format(iMET))
	            self.t.Branch(iiMET, self.list_of_arrays_noES[i], '{0:s}/F'.format(iiMET))

		for i, v in enumerate(self.allsystJets):
		    self.t.Branch('njets{0:s}'.format(v), self.list_of_arraysJetsNjets[i], 'njets{0:s}/i'.format(v))
		    self.t.Branch('nbtagL{0:s}'.format(v), self.list_of_arraysJetsNbtagL[i], 'nbtagL{0:s}/i'.format(v))
		    self.t.Branch('nbtagM{0:s}'.format(v), self.list_of_arraysJetsNbtagM[i], 'nbtagM{0:s}/i'.format(v))
		    self.t.Branch('nbtagT{0:s}'.format(v), self.list_of_arraysJetsNbtagT[i], 'nbtagT{0:s}/i'.format(v))
		    self.t.Branch('jflavour{0:s}'.format(v), self.list_of_arraysJetsFlavour[i], 'jflavour{0:s}[12]/i'.format(v))
		    self.t.Branch('jpt{0:s}'.format(v), self.list_of_arraysJetsPt[i], 'jpt{0:s}[12]/F'.format(v))
		    self.t.Branch('jeta{0:s}'.format(v), self.list_of_arraysJetsEta[i], 'jeta{0:s}[12]/F'.format(v))
		    self.t.Branch('btagDeep{0:s}'.format(v), self.list_of_arraysJetsNbtagDeep[i], 'btagDeep{0:s}[12]/F'.format(v))



        #self.MET_pt_jesEC2Up  = array('f',[0])
        #self.t.Branch('MET_pt_jesEC2Up', self.MET_pt_jesEC2Up, 'MET_pt_jesEC2Up/F' )
        self.tN=[]

	#self.t.SetBranchStatus("*Up",0)
	#self.t.SetBranchStatus("*Down",0)
	self.t.SetBranchStatus("GenPart*",0)
	self.t.SetBranchStatus("*_tr*",0)
	self.t.SetBranchStatus("*LHE*",1)
	#self.t.SetBranchStatus("*LHEScaleWeight",1)
	self.t.SetBranchStatus("*Up*",0)
	self.t.SetBranchStatus("*Down*",0)
	#self.t.SetBranchStatus("Smear",0)
        for i, isyst in enumerate(shift) : 
	    self.tN.append(isyst)

            #if isyst == "Events" : continue
            #else  : 
            if i > 0 : 
                self.tN[i-1]  = self.t.CloneTree()
                #self.t.SetBranchStatus("Smear",1)
                self.tN[i-1].SetName(isyst)

                print '====================>',self.tN[i-1], self.tN[i-1].GetName()

	self.t.SetBranchStatus("GenPart*",1)
	self.t.SetBranchStatus("*_tr*",1)
	#self.t.SetBranchStatus("*LHE*",1)
	self.t.SetBranchStatus("*LHEScaleWeight*",1)
	self.t.SetBranchStatus("*Up*",1)
	self.t.SetBranchStatus("*Down*",1)

    def getu_par_MET(self, entry, metx, mety, qx, qy, qt):

	uX = - metx - qx
	uY = - mety - qy
	upara = (uX*qx + uY*qy)/qt
	#uperp = (uX*qy - uY*qx)/qt
	return upara

    def getu_perp_MET(self, entry, metx, mety, qx, qy, qt):

	uX = - metx - qx
	uY = - mety - qy
	#upara = (uX*qx + uY*qy)/qt
	uperp = (uX*qy - uY*qx)/qt

	return uperp

    def calculate_uperp_and_upara(self, met_x, met_y, q_x, q_y, q_t):
	# Calculate the components of the "u" vector
	u_x = -met_x - q_x
	u_y = -met_y - q_y
	
	# Calculate the dot product of "u" and "q"
	u_dot_q = u_x*q_x + u_y*q_y
	
	# Calculate the magnitudes of "u" and "q"
	u_mag = sqrt(u_x**2 + u_y**2)
	q_mag = q_t
	
	# Calculate the perpendicular and parallel components of "u"
	uperp = (u_x*q_y - u_y*q_x)/q_mag
	upara = u_dot_q/q_mag
	
	return uperp, upara



    def makeUpara(self, enry, met_pt, met_phi, boson_pt, boson_phi):

        uPara = ( ((( - met_pt  *cos(met_phi  )  -  boson_pt *cos( boson_phi ))* boson_pt  *cos( boson_phi )+ ( -met_pt  *sin( met_phi)- boson_pt *sin( boson_phi  )) *boson_pt *sin( boson_phi ))/ boson_pt )/boson_pt)

        #uPara = ( " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +bo    son +"*sin( " +boson_phi +" ))/" +boson+")/zll_pt" )
        #uPara = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +bo    son +"*sin( " +boson_phi +" ))/" +boson+")/zll_pt" )
        return uPara


    def makeUparaRes(self, entry, met_pt, met_phi,boson_pt, boson_phi):
	uPara = ( ((( - met_pt *cos(met_phi ) - boson_pt *cos( boson_phi )) *boson_pt *cos(boson_phi )+(-met_pt *sin(met_phi ) - boson_pt *sin(boson_phi ))  *boson_pt *sin(boson_phi ))/ boson_pt + boson_pt ))

	#uPara = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson + " + " + boson +")" )
	return uPara

    def makeUperpRes(self, entry, met_pt, met_phi,boson_pt, boson_phi):


	#uPerp = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*sin( " +boson_phi +" )-(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*cos( " +boson_phi +" ))/" +boson +")" )                             
	uPerp = ( ((( -met_pt  *cos(met_phi  ) -boson_pt *cos( boson_phi ))  *boson_pt *sin( boson_phi  )- (-met_pt *sin( met_phi )- boson_pt *sin(boson_phi  )) *boson_pt  *cos( boson_phi  ))/ boson_pt ) )                             
	return uPerp




    def get_mt(self,METtype,entry,tau) :
        if METtype == 'MVAMet' :
            # temporary choice 
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PFMet' :
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PUPPIMet' :
            dphi = tau.Phi() - entry.PuppiMET_phi
            return sqrt(2.*tau.Pt()*entry.PuppiMET_pt*(1. - cos(dphi)))
        else :
            print("Invalid METtype={0:s} in outTuple.get_mt().   Exiting".format(METtype))

    def getPt_tt(self,entry,tau1,tau2) :
        ptMiss = TLorentzVector() 
        ptMiss.SetPtEtaPhiM(entry.MET_pt,0.,entry.MET_phi,0.)
	ptMiss.SetPz(0.)
        ptMiss.SetE(ptMiss.Pt())
        return (tau1+tau2+ptMiss).Pt()

    def getMt_tot(self,entry,tau1,tau2) :
        pt1, pt2, met = tau1.Pt(), tau2.Pt(), entry.MET_pt
        phi1, phi2, metphi = tau1.Phi(), tau2.Phi(), entry.MET_phi
        arg = 2.*(pt1*met*(1. - cos(phi1-metphi)) + pt2*met*(1. - cos(phi2-metphi)) + pt1*pt2*(1. - cos(phi2-phi1)))
        return sqrt(arg)

    def getDR(self,entry, v1,v2) :

        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        DR = sqrt(dPhi**2 + (v2.Eta()-v1.Eta())**2)
	return DR

    def getDRnV(self,entry, eta1,phi1, eta2,phi2) :

        dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
        DR = sqrt(dPhi**2 + (eta2-eta1)**2)
	return DR

    def getdPhi(self, entry, v1,v2) :
        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        return dPhi

    def getM_vis(self,entry,tau1,tau2) :
        return (tau1+tau2).M()

    def getJets(self,entry,tau1,tau2,era) :
	nJet30, jetList, bJetList, bJetListFlav = 0, [], [], []
        phi2_1, eta2_1 = tau1.Phi(), tau1.Eta() 
        phi2_2, eta2_2 = tau2.Phi(), tau2.Eta() 
	bjet_discr = 0.6321
	bjet_discrFlav = 0.0614
	if str(era) == '2017' : bjet_discr = 0.4941
	if str(era) == '2018' : bjet_discr = 0.4184

        for j in range(entry.nJet) :
            if entry.Jet_jetId[j]  < 2  : continue  #require tight jets
            if entry.Jet_pt[j]>20 and entry.Jet_pt[j] < 50 and entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
            if str(era) == '2017'  and entry.Jet_pt[j] > 20 and entry.Jet_pt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
            if entry.Jet_pt[j] < 20. : continue
            if abs(entry.Jet_eta[j]) > 4.7 : continue
            phi1, eta1 = entry.Jet_phi[j], entry.Jet_eta[j]
            dPhi = min(abs(phi2_1-phi1),2.*pi-abs(phi2_1-phi1))
            DR = sqrt(dPhi**2 + (eta2_1-eta1)**2)
            dPhi = min(abs(phi2_2-phi1),2.*pi-abs(phi2_2-phi1))
            DR = min(DR,sqrt(dPhi**2 + (eta2_2-eta1)**2))
            if DR < 0.5 : continue
            if entry.Jet_pt[j] > 30 :
		if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepB[j] > bjet_discr : bJetList.append(j)
		if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepFlavB[j] > bjet_discrFlav : bJetListFlav.append(j)
                jetList.append(j) 

        return jetList, bJetList,bJetListFlav



    def getJetsJMEMV(self,entry,LepList,era, syst,proc) :
	jetList, jetListFlav, jetListEta, jetListPt, bTagListDeep, bJetListL, bJetListM, bJetListT, bJetListFlav = [], [], [], [], [], [], [], [], []
	#print 'will try', len(LepList), 'syst', syst, 'proc', proc
	#bjet_discrL = 0.2217
	#bjet_discrM = 0.6321
	#bjet_discrT = 0.8953

        #default is 2016 post
	bjet_discrFlav = 0.0614
	bjet_discrL = 0.1918
	bjet_discrM = 0.5847
	bjet_discrT = 0.8767
        #print 'inside jets', era, proc
	if '2016pre' in str(era): 
	    bjet_discrL = 0.2027
	    bjet_discrM = 0.6001
	    bjet_discrT = 0.8819

	if '2016post' in str(era): 
	    bjet_discrL = 0.1918
	    bjet_discrM = 0.5847
	    bjet_discrT = 0.8767

	if str(era) == '2017' : 
	    bjet_discrL = 0.1355
	    bjet_discrM = 0.4506
	    bjet_discrT = 0.7738
	if str(era) == '2018' : 
	    bjet_discrL = 0.1208
	    bjet_discrM = 0.4168
	    bjet_discrT = 0.7665

	failJets=[]
        goodJets=[]
        bJetListL=[]
        bJetListM=[]
        bJetListT=[]
        bTagListDeep=[]
        
        #if syst !='' : syst="_"+syst
     
        if 'nom' in syst : syst='_nom'
          
        jpt=0.
        for j in range(entry.nJet) :
            try : 
		jpt = getattr(entry, "Jet_pt{0:s}".format(str(syst)), None)
                #if syst=='_nom' : print jpt[j],  entry.Jet_pt[j],  syst

		if jpt[j] < 30. : continue
		if entry.Jet_jetId[j]  < 2  : continue  #pass tight and tightLepVeto ID. 
		if jpt[j] < 50  : #loose jetPU_iD
		    if '2016' not in str(era) and  entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
		    if '2016' in str(era) and  entry.Jet_puId[j]  > 4  : continue #inverted working points https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetIDUL

		#if str(era) == '2017'  and jpt[j] > 20 and jpt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
		if abs(entry.Jet_eta[j]) > 4.7 : continue

		#for iv, lepv in enumerate(LepList) : 
		for iv, lv  in  enumerate(LepList) :
		    dr = self.getDRnV(entry, entry.Jet_eta[j], entry.Jet_phi[j], LepList[iv].Eta(), LepList[iv].Phi())
		    if float(dr) > 0.5 : 
			if j not in goodJets : goodJets.append(j)
		    else: 
			if j not in failJets : failJets.append(j)
            except : continue

        #print 'will check failed jets',  entry.luminosityBlock, entry.event, entry.run, failJets, goodJets, 'from nJet i', j, entry.nJet
        for j in failJets : 
            if j in goodJets : goodJets.remove(j)
        jpt=0
        for jj in goodJets : 
            #if isMC : 
            try : 
                jetListFlav.append(entry.Jet_partonFlavour[jj])
            except AttributeError  : jetListFlav.append(0)
            jetListEta.append(entry.Jet_eta[jj])
            jpt = getattr(entry, "Jet_pt{0:s}".format(str(syst)), None)
            jetListPt.append(jpt[jj])
            bTagListDeep.append(entry.Jet_btagDeepB[jj])

            #print 'will check',  entry.luminosityBlock, entry.event, entry.run, goodJets, jj, jpt[jj], 'flav', entry.Jet_partonFlavour[jj]
            if jpt[jj] > 30 : 

                jetList.append(jj) 

		if abs(entry.Jet_eta[jj]) < 2.5 : 
                    #print entry.Jet_btagDeepB[jj],  bjet_discrL,  bjet_discrM ,  bjet_discrT
		    if entry.Jet_btagDeepB[jj] > bjet_discrL : bJetListL.append(jj)
		    if entry.Jet_btagDeepB[jj] > bjet_discrM : bJetListM.append(jj)
		    if entry.Jet_btagDeepB[jj] > bjet_discrT : bJetListT.append(jj)
		    if entry.Jet_btagDeepFlavB[jj] > bjet_discrFlav : bJetListFlav.append(jj)
                #print '--added ', jj, 'in good list', jpt[jj], abs(entry.Jet_eta[jj])

        #if len(jetList)!=len(jetListPt) : print 'going out....', jetList, jetListPt, syst, len(jetList), len(jetListPt), entry.luminosityBlock, entry.event, entry.run
        #print 'going out....', jetList, jetListPt, syst, len(jetList), len(jetListPt), entry.luminosityBlock, entry.event, entry.run, btagWeightDeepCSVB
        #print ''
        #if entry.event == 207273709 : print 'this is check', jetList, jetListFlav, jetListEta,  jetListPt, bTagListDeep, bJetListL,bJetListM,bJetListT,bJetListFlav
        #print 'lets see', len(bJetListL), len(bJetListM), len(bJetListT), len(jetList)
        #print ''
        #print jetList, jetListEta, jetListPt
        return jetList, jetListFlav, jetListEta,  jetListPt, bTagListDeep, bJetListL,bJetListM,bJetListT,bJetListFlav


    def runSVFit(self, entry, channel, jt1, jt2, tau1, tau2, metpt, metphi) :
                      
        measuredMETx = metpt*cos(metphi)
        measuredMETy = metpt*sin(metphi)

        #define MET covariance
        covMET = ROOT.TMatrixD(2,2)
        covMET[0][0] = entry.MET_covXX
        covMET[1][0] = entry.MET_covXY
        covMET[0][1] = entry.MET_covXY
        covMET[1][1] = entry.MET_covYY

        #self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3

        if channel == 'et' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511) 
        elif channel == 'mt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.106) 
        elif channel == 'tt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), entry.Tau_mass[jt1])
                        
	if channel != 'em' :
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), entry.Tau_mass[jt2])

	if channel == 'em' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511)
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), 0.106)

        VectorOfTaus = ROOT.std.vector('MeasuredTauLepton')
        instance = VectorOfTaus()
        instance.push_back(measTau1)
        instance.push_back(measTau2)

        FMTT = ROOT.FastMTT()
        FMTT.run(instance, measuredMETx, measuredMETy, covMET)
        ttP4 = FMTT.getBestP4()
        return ttP4.M(), ttP4.Mt() 
    


    def Fill2Lep(self, entry, cat, LepP, LepM, lepList, isMC, era, doUncertainties=False , proc="EOY") : 
    #def Fill(self, entry, SVFit, cat, jt1, jt2, LepP, LepM, lepList, isMC, era, doUncertainties=False ,  met_pt=-99, met_phi=-99, systIndex=0) : 
        SystIndex = 0

        #if SystIndex >0 : doUncertainties=False
        leadL, subL =  TLorentzVector(), TLorentzVector()

        if LepP.Pt()>LepM.Pt() : 
            leadL=LepP
            subL=LepM
            self.isLead_1[0] = 1.
        else : 
            leadL=LepM
            subL=LepP
            self.isLead_1[0] = 0.

        #channel_ll = 'mm' or 'ee'
        channel_ll = cat
	channel = cat

        if SystIndex ==0 : 

	    is_trig_1, is_trig_2, is_Dtrig_1 = 0., 0., 0.
	    TrigListLep = []
	    TrigListTau = []
	    hltListLep  = []
	    hltListLepSubL  = []

	    TrigListLep, hltListLep, hltListLepSubL  = GF.findSingleLeptTrigger(lepList, entry, channel_ll, era)

	    TrigListLep = list(dict.fromkeys(TrigListLep))
	    #if len(hltListLep) > 0 or len(hltListLepSubL)>0 :     print GF.printEvent(entry), SystIndex

	    if len(hltListLep) > 0 and  len(hltListLepSubL) == 0 :
		is_trig_1 = 1
	    if len(hltListLep) == 0 and len(hltListLepSubL) > 0 :
		is_trig_1 = -1
	    if len(hltListLep) > 0 and len(hltListLepSubL)>0 :
		is_trig_1 = 2

	    self.whichTriggerWord[0]=0
	    self.whichTriggerWordSubL[0]=0

            #if is_trig_1 == 0 : continue

	    #if len(TrigListLep) >0 : print 'TrigerList ===========>', TrigListLep, lepList, hltListLep, channel_ll, 'istrig_1', is_trig_1, 'istrig_2', is_trig_2, 'lenTrigList', len(TrigListLep),  'lenLept', len(lepList), 'lepList_0', lepList[0], 'TrigList_0', TrigListLep[0], hltListLep
	    
	    for i,bit in enumerate(hltListLep):
		    
		if bit : 
		    self.whichTriggerWord[0] += 2**i

	    for j,bitt in enumerate(hltListLepSubL):
		if bitt : self.whichTriggerWordSubL[0] += 2**j

	    #if channel_ll=='ee' and entry.luminosityBlock==90 and entry.event==8904: print self.whichTriggerWord[0], 'hlt', hltListLep, 'hltsub', hltListLepSubL
	    #print cat, self.whichTriggerWord
	    # channel = 'mt', 'et', 'tt', or 'em'
	    self.entries += 1

	    self.run[0]  = entry.run
	    self.nElectron[0]  = entry.nElectron
	    self.nMuon[0]  = entry.nMuon
	    self.nTau[0]  = entry.nTau
	    self.lumi[0] = entry.luminosityBlock 
	    self.evnt[0]  = entry.event


	    self.mll[0]  = (LepP+LepM).M()
	    self.zll_pt[0]  = (LepP+LepM).Pt()
	    self.zll_phi[0]  = (LepP+LepM).Phi()
	    self.boson_pt[0] = (LepP+LepM).Pt()
	    self.boson_phi[0] = (LepP+LepM).Phi()

	    self.iso_1[0]  = -99
	    self.q_1[0]  = -99
	    self.isGlobal_1[0]  = -99
	    self.iso_2[0]  = -99
	    self.q_2[0]  = -99
	    self.isGlobal_2[0]  = -99
	    try:
		self.L1PreFiringWeight_Nom[0] = entry.L1PreFiringWeight_Nom
		self.L1PreFiringWeight_Up[0] = entry.L1PreFiringWeight_Up
		self.L1PreFiringWeight_Down[0] = entry.L1PreFiringWeight_Dn
	    except AttributeError : 
		self.L1PreFiringWeight_Nom[0] = 1
		self.L1PreFiringWeight_Up[0] = 1
		self.L1PreFiringWeight_Down[0] = 1
		
	    self.tightId_1[0]       = -1 
	    self.mediumId_1[0]       = -1 
	    self.mediumPromptId_1[0]   = -1
	    self.looseId_1[0]       = -1
	    self.isGlobal_1[0]      = -1
	    self.isTracker_1[0]     = -1

	    self.GenPart_statusFlags_1[0]    = -1
	    self.GenPart_status_1[0]    = -1
	    self.gen_match_1[0] = -1

	    self.tightId_2[0]       = -1 
	    self.mediumId_2[0]       = -1 
	    self.mediumPromptId_2[0]   = -1
	    self.looseId_2[0]       = -1
	    self.isGlobal_2[0]      = -1
	    self.isTracker_2[0]     = -1

	    self.GenPart_statusFlags_2[0]    = -1
	    self.GenPart_status_2[0]    = -1
	    self.gen_match_2[0] = -1

	    self.nPV[0]  = entry.PV_npvs
	    self.nPVGood[0]  = entry.PV_npvsGood
	    self.nPVchi2[0]  = entry.PV_chi2
	    self.nPVndof[0]  = entry.PV_ndof
	    self.nPVscore[0]  = entry.PV_score
	    self.PVx[0]  = entry.PV_x
	    self.PVy[0]  = entry.PV_y
	    self.PVz[0]  = entry.PV_z

	    try :
		self.nPU[0]  = entry.Pileup_nPU
		self.nPUEOOT[0]  = entry.Pileup_sumEOOT
		self.nPULOOT[0]  = entry.Pileup_sumLOOT
		self.nPUtrue[0]  = entry.Pileup_nTrueInt
	    except AttributeError :
		self.nPU[0]  = 1
		self.nPUEOOT[0]  = 1
		self.nPULOOT[0]  = 1
		self.nPUtrue[0]  = 1
            try :
		self.weight[0]           = entry.genWeight
		self.Generator_weight[0] = entry.Generator_weight
	    except AttributeError :
		self.weight[0]           = -100.
		self.Generator_weight[0] = -100.


	    try :
		if isMC : 
		    self.LHEweight[0]        = entry.LHEWeight_originalXWGTUP
		    self.LHE_Njets[0]        = ord(entry.LHE_Njets)
		if SystIndex == 0 : 
		    for i in range(0, int(entry.nLHEScaleWeight)) : 
			self.LHEScaleWeights[i] = entry.LHEScaleWeight[i]
	    except AttributeError :
		self.LHEweight[0]        = 1. 
		self.LHE_Njets[0] = -1
                self.LHEScaleWeights[0] = -1

			    


        e = entry

        '''
        List from Cecile 
        single ele 2016: HLT Ele25 eta2p1 WPTight Gsf v and cut pt(ele)>26, eta(ele)<2.1
        single ele 2017: HLT Ele27 WPTight Gsf v, HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>28, eta(ele)<2.1
        single ele 2018: HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>33, eta(ele)<2.1
        '''
        
        if int(SystIndex) ==0 : 
	    bits=[]
	    try : bits.append(e.HLT_Ele25_eta2p1_WPTight_Gsf)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Ele27_WPTight_Gsf)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Ele32_WPTight_Gsf)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Ele35_WPTight_Gsf)
	    except AttributeError : bits.append(False)
	    # pad upper bits in this byte with zeros (False) 
	    #for i in range(4) :
	    #    bits.append(False)
		
	    try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)
	    except AttributeError : bits.append(False) 

	    self.electronTriggerWord[0] = 0
	    for i, bit in enumerate(bits) :
		if bit : self.electronTriggerWord[0] += 2**i

	    '''
	    List from Cecile 
	    single mu 2016: HLT IsoMu22 v, HLT IsoMu22 eta2p1 v, HLT IsoTkMu22 v, HLT IsoTkMu22 eta2p1 v and cut pt(mu)>23, eta(mu)<2.1
	    single mu 2017: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
	    single mu 2018: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
	    '''
	    bits=[]
	    try : bits.append(e.HLT_IsoMu22)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_IsoMu22_eta2p1)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_IsoTkMu22)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_IsoTkMu22_eta2p1)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_IsoMu24)
	    except AttributeError : bits.append(False) 
	    try : bits.append(e.HLT_IsoMu27)
	    except AttributeError : bits.append(False) 

	    #for i in range(2) :
	    #    bits.append(False)                             # pad remaining bit in this bit 
	   
	    try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)
	    except AttributeError : bits.append(False) 
	    try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass12)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p12)
	    except AttributeError : bits.append(False)
	    try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ)
	    except AttributeError : bits.append(False) 
	    try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Mass12)
	    except AttributeError : bits.append(False) 

	    self.muonTriggerWord[0] = 0
	    for i, bit in enumerate(bits) :
		if bit : self.muonTriggerWord[0] += 2**i

            #neede for all systematics as jt1/jt2 may change per systematic
	self.cat[0]  = tauFun2.catToNumber2Lep(cat)


        self.pt_1[0]   = LepP.Pt()
        self.phi_1[0]  = LepP.Phi()
        self.eta_1[0]  = LepP.Eta()
        self.pt_2[0]   = LepM.Pt()
        self.phi_2[0]  = LepM.Phi()
        self.eta_2[0]  = LepM.Eta()
        muoneff1=1.
        muoniso1=1.
        muontrig1=1.
        eleeff1=1.
        eleiso1=1.
        eletrig1=1.

        muoneff2=1.
        muoniso2=1.
        muontrig2=1.
        eleeff=1.
        eleiso=1.
        eletrig=1.

	self.IDSF[0]  = 1.
	self.IsoSF[0]  = 1.
	self.TrigSF[0]  = 1.
	self.IDSF1[0]  = 1.
	self.IsoSF1[0]  = 1.
	self.TrigSF1[0]  = 1.
	self.IDSF2[0]  = 1.
	self.IsoSF2[0]  = 1.
	self.TrigSF2[0]  = 1.
	yearin=era
        #print leadL.Pt(), subL.Pt(), channel_ll, LepP.Pt(), LepM.Pt(), era, is_trig_1
        if isMC :
	    if '2016' in era and 'pre' in era : yearin='2016preVFP'
	    if '2016' in era and 'pre' not in era : yearin='2016postVFP'

	    if channel_ll == 'mm' : 
		  
		if LepP.Pt()> 15 : muoneff1 = self.evaluator["NUM_TightID_DEN_TrackerMuons"].evaluate("{0:s}_UL".format( str(yearin)), fabs(LepP.Eta()), LepP.Pt(), "sf")
		if LepM.Pt()> 15 : muoneff2 = self.evaluator["NUM_TightID_DEN_TrackerMuons"].evaluate("{0:s}_UL".format( str(yearin)), fabs(LepM.Eta()), LepM.Pt(), "sf")
		if LepP.Pt()> 15 : muoniso1 = self.evaluator["NUM_TightRelIso_DEN_TightIDandIPCut"].evaluate("{0:s}_UL".format(str(yearin)), fabs(LepP.Eta()), LepP.Pt(), "sf")
		if LepM.Pt()> 15 : muoniso2 = self.evaluator["NUM_TightRelIso_DEN_TightIDandIPCut"].evaluate("{0:s}_UL".format(str(yearin)), fabs(LepM.Eta()), LepM.Pt(), "sf")

		if era == '2016' : 
                    if leadL.Pt() > 26  : muontrig1 = self.evaluator["NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(yearin)), fabs(leadL.Eta()), leadL.Pt(), "sf")
                    if subL.Pt() > 26 : muontrig2 = self.evaluator["NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(yearin)), fabs(subL.Eta()), subL.Pt(), "sf")
                #NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight  
		if era =='2017' :  

                    if leadL.Pt() > 29 : muontrig1 = self.evaluator["NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(leadL.Eta()), leadL.Pt(), "sf")
                    if subL.Pt()>29 :muontrig2 = self.evaluator["NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(subL.Eta()), subL.Pt(), "sf")
		if era =='2018' :  

                    if leadL.Pt() > 26 : muontrig1 = self.evaluator["NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(leadL.Eta()), leadL.Pt(), "sf")  ### for 2018 the json Veto only 24 SF..but we have used the HLT27
                    if subL.Pt() > 26 : muontrig2 = self.evaluator["NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(subL.Eta()), subL.Pt(), "sf")  ### fora 2018 the json Veto only 24 SF..but we have used the HLT27

		#print 'sfs are', muoneff , muoniso, muontrig

		self.IDSF[0]  = muoneff1*muoneff2
		self.IsoSF[0]  = muoniso1*muoniso2

		self.IDSF1[0]  = muoneff1
		self.IsoSF1[0]  = muoniso1
		self.TrigSF1[0]  = muontrig1

		self.IDSF2[0]  = muoneff2
		self.IsoSF2[0]  = muoniso2
		self.TrigSF2[0]  = muontrig2
		if is_trig_1 == 2 : self.TrigSF[0]  = muontrig1*muontrig2
		if is_trig_1 == 1 : self.TrigSF[0]  = muontrig1
		if is_trig_1 == -1 : self.TrigSF[0]  = muontrig2

	    if channel_ll == 'ee' : 
                eleeff1=1.
                eleeff2=1.
                eleiso1=1.
                eleiso2=1.
		if LepP.Pt()> 20 : eleeff1 = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "RecoAbove20", LepP.Eta(), LepP.Pt() )
		if LepM.Pt() > 20 : eleeff2 = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "RecoAbove20", LepM.Eta(), LepM.Pt() )
		if LepP.Pt()>20 : eleiso1 = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "wp90iso", LepP.Eta(), LepP.Pt() )
		if LepM.Pt() > 20 : eleiso2 = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "wp90iso", LepM.Eta(), LepM.Pt() )

		self.IDSF[0]  = eleeff1*eleeff2
                self.IsoSF[0]  = eleiso1*eleiso2
		self.IDSF1[0]  = eleeff1
                self.IsoSF1[0]  = eleiso1
		self.IDSF2[0]  = eleeff2
                self.IsoSF2[0]  = eleiso2

                self.TrigSF[0] = 1.
                self.TrigSF1[0] = 1.
                self.TrigSF2[0] = 1.

		eff_trig_d_1 =  self.sf_EleTrig.get_EfficiencyData(leadL.Pt,leadL.Eta())
		eff_trig_mc_1 =  self.sf_EleTrig.get_EfficiencyMC(leadL.Pt,leadL.Eta())
		eff_trig_mc_2 =  self.sf_EleTrig.get_EfficiencyMC(subL.Pt,subL.Eta())
		eff_trig_d_2 =  self.sf_EleTrig.get_EfficiencyData(subL.Pt,subL.Eta())


                if eff_trig_mc_1 !=0 :    self.TrigSF1[0] = float(eff_trig_d_1/eff_trig_mc_1)
                if eff_trig_mc_2 !=0 :    self.TrigSF2[0] = float(eff_trig_d_2/eff_trig_mc_2)
		else : self.TrigSF[0]  = 1.
		if is_trig_1 == 2 : self.TrigSF[0]  = self.TrigSF1[0]*self.TrigSF2[0]
		if is_trig_1 == 1 : self.TrigSF[0]  = self.TrigSF1[0]
		if is_trig_1 == -1 : self.TrigSF[0]  = self.TrigSF2[0]


	lep_index_1 = lepList[0]
	lep_index_2 = lepList[1]
        # trig
        if SystIndex ==0 : 
	    self.isTrig_1[0]   = is_trig_1

        leplist=[]
        leplist.append(LepP)
        leplist.append(LepM)

	if channel_ll == 'ee' : 
            self.Electron_convVeto[0]  = entry.Electron_convVeto[lep_index_1]
            self.Electron_lostHits[0]  = ord(entry.Electron_lostHits[lep_index_1])
      
            self.iso_1[0]  = entry.Electron_pfRelIso03_all[lep_index_1]
            self.q_1[0]  = entry.Electron_charge[lep_index_1]
            self.d0_1[0]   = entry.Electron_dxy[lep_index_1]
            self.dZ_1[0]   = entry.Electron_dz[lep_index_1]
            self.Electron_mvaFall17V2noIso_WP90_1[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_1]
            self.Electron_mvaFall17V2Iso_WP90_1[0]  = entry.Electron_mvaFall17V2Iso_WP90[lep_index_1]
            self.Electron_cutBased_1[0]  = entry.Electron_cutBased[lep_index_1]
	    #if SystIndex ==0 and  isMC : 
	    #	self.pt_uncor_1[0] = ePt[lep_index_1]
	    #	self.m_uncor_1[0] = eMass[lep_index_1]

            if isMC :
		self.gen_match_1[0] = ord(entry.Electron_genPartFlav[lep_index_1])

            self.iso_2[0]  = entry.Electron_pfRelIso03_all[lep_index_2]
            self.q_2[0]  = entry.Electron_charge[lep_index_2]
            self.d0_2[0]   = entry.Electron_dxy[lep_index_2]
            self.dZ_2[0]   = entry.Electron_dz[lep_index_2]
            self.Electron_mvaFall17V2noIso_WP90_2[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_2]
            self.Electron_mvaFall17V2Iso_WP90_2[0]  = entry.Electron_mvaFall17V2Iso_WP90[lep_index_2]
            self.Electron_cutBased_2[0]  = entry.Electron_cutBased[lep_index_2]
	    #if SystIndex ==0 and  isMC : 
	    #	self.pt_uncor_2[0] = ePt[lep_index_2]
            #	self.m_uncor_2[0] = eMass[lep_index_2]

            if isMC :
		self.gen_match_2[0] = ord(entry.Electron_genPartFlav[lep_index_2])

	if channel_ll == 'mm' : 

            self.iso_1[0]  = entry.Muon_pfRelIso04_all[lep_index_1]
            self.PFiso_1[0]  = ord(entry.Muon_pfIsoId[lep_index_1])
	    self.q_1[0]  = entry.Muon_charge[lep_index_1]
	    self.d0_1[0]   = entry.Muon_dxy[lep_index_1]
	    self.dZ_1[0]   = entry.Muon_dz[lep_index_1]
	    self.looseId_1[0]   = entry.Muon_looseId[lep_index_1] 
            self.tightId_1[0]      = entry.Muon_tightId[lep_index_1]
            self.tightCharge_1[0]      = entry.Muon_tightCharge[lep_index_1]
	    self.mediumId_1[0]   = entry.Muon_mediumId[lep_index_1] 
	    self.pfIsoId_1[0]   = ord(entry.Muon_pfIsoId[lep_index_1])
	    self.mediumPromptId_1[0]   = entry.Muon_mediumPromptId[lep_index_1] 
	    self.isGlobal_1[0]   = entry.Muon_isGlobal[lep_index_1] 
	    try : self.isStandalone_1[0]   = entry.Muon_isStandalone[lep_index_1] 
	    except AttributeError : self.isStandalone_1[0] = 0 
            self.isPFcand_1[0]   = entry.Muon_isPFcand[lep_index_1] 
	    self.isTracker_1[0]   = entry.Muon_isTracker[lep_index_1] 

	    self.highPtId_1[0]  = ord(entry.Muon_highPtId[lep_index_1])
	    try : self.highPurity_1[0]  = entry.Muon_highPurity[lep_index_1]
            except AttributeError : self.highPurity_1[0] = 0
	    self.inTimeMuon_1[0]  = entry.Muon_inTimeMuon[lep_index_1]
	    self.ip3d_1[0]  = entry.Muon_ip3d[lep_index_1]
	    self.sip3d_1[0]  = entry.Muon_sip3d[lep_index_1]

            self.stations_1[0] = entry.Muon_nStations[lep_index_1]
            self.TrackerL_1[0] = entry.Muon_nTrackerLayers[lep_index_1]

            if isMC :
		self.gen_match_1[0] = ord(entry.Muon_genPartFlav[lep_index_1])


            self.iso_2[0]  = entry.Muon_pfRelIso04_all[lep_index_2]
            self.PFiso_2[0]  = ord(entry.Muon_pfIsoId[lep_index_2])
	    self.q_2[0]  = entry.Muon_charge[lep_index_2]
	    self.d0_2[0]   = entry.Muon_dxy[lep_index_2]
	    self.dZ_2[0]   = entry.Muon_dz[lep_index_2]
	    self.looseId_2[0]   = entry.Muon_looseId[lep_index_2] 
            self.tightId_2[0]      = entry.Muon_tightId[lep_index_2]
            self.tightCharge_2[0]      = entry.Muon_tightCharge[lep_index_2]
	    self.mediumId_2[0]   = entry.Muon_mediumId[lep_index_2] 
	    self.pfIsoId_2[0]   = ord(entry.Muon_pfIsoId[lep_index_2])
	    self.mediumPromptId_2[0]   = entry.Muon_mediumPromptId[lep_index_2] 
	    self.isGlobal_2[0]   = entry.Muon_isGlobal[lep_index_2] 
	    try : self.isStandalone_2[0]   = entry.Muon_isStandalone[lep_index_2] 
	    except AttributeError : self.isStandalone_2[0] = 0 
            self.isPFcand_2[0]   = entry.Muon_isPFcand[lep_index_2] 
	    self.isTracker_2[0]   = entry.Muon_isTracker[lep_index_2] 

	    self.highPtId_2[0]  = ord(entry.Muon_highPtId[lep_index_2])
	    try : self.highPurity_2[0]  = entry.Muon_highPurity[lep_index_2]
            except AttributeError : self.highPurity_2[0] = 0
	    self.inTimeMuon_2[0]  = entry.Muon_inTimeMuon[lep_index_2]
	    self.ip3d_2[0]  = entry.Muon_ip3d[lep_index_2]
	    self.sip3d_2[0]  = entry.Muon_sip3d[lep_index_2]

            self.stations_2[0] = entry.Muon_nStations[lep_index_2]
            self.TrackerL_2[0] = entry.Muon_nTrackerLayers[lep_index_2]

            if isMC :
		self.gen_match_2[0] = ord(entry.Muon_genPartFlav[lep_index_2])
        
        # genMatch the di-lepton variables
	if isMC :
	    idx_Lep1 = -1
	    idx_Lep1_tr = -1
	    if (LepP.M() > 0.05): # muon mass 
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, LepP, 'm')
		try :
		    idx_Lep1_tr = entry.Muon_genPartIdx[idx_Lep1]
		except IndexError : pass 
		    
	    elif (LepP.M() < 0.05 < 0.05): # electron mass
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, LepP, 'e')
		try :
		    idx_Lep1_tr = entry.Electron_genPartIdx[idx_Lep1]
		except IndexError : pass 
		    
	    if idx_Lep1_tr >= 0 :
		self.m_1_tr[0]  = entry.GenPart_mass[idx_Lep1_tr]
		self.pt_1_tr[0]  = entry.GenPart_pt[idx_Lep1_tr]
		self.eta_1_tr[0] = entry.GenPart_eta[idx_Lep1_tr]
		self.phi_1_tr[0] = entry.GenPart_phi[idx_Lep1_tr]
		self.GenPart_statusFlags_1[0]    = entry.GenPart_statusFlags[idx_Lep1_tr]
		self.GenPart_status_1[0]    = entry.GenPart_status[idx_Lep1_tr]

	    idx_Lep2 = -1
	    idx_Lep2_tr = -1
	    if (LepM.M() > 0.05): # muon mass 
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, LepM, 'm')
		try :
		    idx_Lep2_tr = entry.Muon_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    elif (LepM.M() < 0.05 < 0.05): # electron mass
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, LepM, 'e')
		try :
		    idx_Lep2_tr = entry.Electron_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    if idx_Lep2_tr >= 0 :
		self.m_2_tr[0]  = entry.GenPart_mass[idx_Lep2_tr]
		self.pt_2_tr[0]  = entry.GenPart_pt[idx_Lep2_tr]
		self.eta_2_tr[0] = entry.GenPart_eta[idx_Lep2_tr]
		self.phi_2_tr[0] = entry.GenPart_phi[idx_Lep2_tr]
		self.GenPart_statusFlags_2[0]    = entry.GenPart_statusFlags[idx_Lep2_tr]
		self.GenPart_status_2[0]    = entry.GenPart_status[idx_Lep2_tr]
        




        #fill the un-corrected or just in the case you dont care to doUncertainties       
	SaveEventMu = False
	SaveEventEl = False

        #SaveEventMu =  cat=='mm' and (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>24 and self.mediumId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.iso_1[0]<0.2   and (self.isGlobal_2[0]>0 or self.isTracker_2[0]>0) and self.pt_2[0]>24 and self.mediumId_2[0]>0 and fabs(self.eta_2[0])<2.4 and  fabs(self.dZ_2[0])<0.2 and  fabs(self.d0_2[0])<0.045 and self.iso_2[0]<0.2 and self.isTrig_1[0]!=0 and self.nbtagT[0]==0



	if '2016' in era:
	    SaveEventMu =  cat=='mm' and (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>10 and self.mediumId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.iso_1[0]<0.2   and (self.isGlobal_2[0]>0 or self.isTracker_2[0]>0) and self.pt_2[0]>10 and self.mediumId_2[0]>0 and fabs(self.eta_2[0])<2.4 and  fabs(self.dZ_2[0])<0.2 and  fabs(self.d0_2[0])<0.045 and self.iso_2[0]<0.2 and self.isTrig_1[0]!=0 
	    SaveEventEl = cat=='ee' and  self.pt_1[0]>10 and self.Electron_mvaFall17V2Iso_WP90_1[0]>0 and fabs(self.eta_1[0])<2.1 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.iso_1[0] < 0.15 and  self.pt_2[0]>10 and self.Electron_mvaFall17V2Iso_WP90_2[0]>0 and fabs(self.eta_2[0])<2.1 and  fabs(self.dZ_2[0])<0.2 and  fabs(self.d0_2[0])<0.045 and self.iso_2[0] < 0.15        and self.isTrig_1[0]!=0    

	else :
	    SaveEventMu =  cat=='mm' and (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>10 and self.mediumId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.iso_1[0]<0.2   and (self.isGlobal_2[0]>0 or self.isTracker_2[0]>0) and self.pt_2[0]>10 and self.mediumId_2[0]>0 and fabs(self.eta_2[0])<2.4 and  fabs(self.dZ_2[0])<0.2 and  fabs(self.d0_2[0])<0.045 and self.iso_2[0]<0.2 and self.isTrig_1[0]!=0 

	    SaveEventEl = cat=='ee' and  self.pt_1[0]>10 and self.Electron_mvaFall17V2Iso_WP90_1[0]>0 and fabs(self.eta_1[0])<2.1 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.iso_1[0] < 0.15 and  self.pt_2[0]>10 and self.Electron_mvaFall17V2Iso_WP90_2[0]>0 and fabs(self.eta_2[0])<2.1 and  fabs(self.dZ_2[0])<0.2 and  fabs(self.d0_2[0])<0.045 and self.iso_2[0] < 0.15        and self.isTrig_1[0]!=0    


        #if not SaveEventMu : 
        #    print (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0)  ,  self.pt_1[0]>10  ,  self.mediumId_1[0]>0  ,  fabs(self.eta_1[0])<2.4  ,   fabs(self.dZ_1[0])<0.2  ,   fabs(     self.d0_1[0])<0.045  ,  self.iso_1[0]<0.2    ,  (self.isGlobal_2[0]>0 or self.isTracker_2[0]>0)  ,  self.pt_2[0]>10  ,  self.mediumId_2[0]>0  ,  fabs(self.eta_2[0])<2.4  ,   fabs(self.dZ_2[0])<0.2  ,        fabs(self.d0_2[0])<0.045  ,  self.iso_2[0]<0.2  ,  self.isTrig_1[0], self.iso_2[0], self.nbtagL[0], self.nbtagM[0], self.nbtagT[0]
        if SaveEventMu or SaveEventEl:
            #print 'I will save this......', entry.event
            #if  self.nbtag[0] == 0 : 

	#if True:  
	    self.MET_significance[0]= entry.MET_significance
	    pmetV, metV, metVT1, metVR, metUn, metVTest, metVSmear, metVTestSmear=  TLorentzVector(),TLorentzVector(),TLorentzVector(),TLorentzVector(),  TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector()
            self.Flag_hfNoisyHitsFilter[0] = 1
            self.Flag_BadPFMuonDzFilter[0] = 1

	    if 'UL' in proc :

		try:
                    self.MET_pt[0]= entry.MET_pt
		    self.MET_phi[0]= entry.MET_phi
	            metV.SetPtEtaPhiM(entry.MET_pt,0, entry.MET_phi,0)
		    metV.SetPz(0.)
		    metV.SetE(metV.Pt())

		    self.u_par_MET[0]= self.getu_par_MET( entry, metV.X(), metV.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
		    self.u_perp_MET[0]= self.getu_perp_MET( entry, metV.X(), metV.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )

	            metUn.SetXYZT(entry.MET_MetUnclustEnUpDeltaX,entry.MET_MetUnclustEnUpDeltaY,0,0)
		    metUn.SetPz(0.)
		    metUn.SetE(metUn.Pt())
		except AttributeError:
		    self.MET_pt[0]= -1
		    self.MET_phi[0]= -99
	            metV.SetPtEtaPhiM(0,0,0,0)
		    metV.SetPz(0.)
	            metUn.SetPtEtaPhiM(0,0,0,0)
		    metUn.SetPz(0.)

		self.metcov00[0] = entry.MET_covXX
		self.metcov01[0] = entry.MET_covXY
		self.metcov10[0] = entry.MET_covXY
		self.metcov11[0] = entry.MET_covYY

		try :
		    #print entry.MET_T1_pt, entry.MET_T1_phi, entry.PV_npvsGood, entry.run, isMC, era, entry.PV_npvs

		    self.MET_T1_pt[0]= entry.MET_T1_pt
		    self.MET_T1_phi[0]= entry.MET_T1_phi
		    metVT1.SetPtEtaPhiM(entry.MET_T1_pt,0, entry.MET_T1_phi,0)
		    metVT1.SetPz(0.)
		    metVT1.SetE(metV.Pt())

		except AttributeError : 
		    self.MET_T1_pt[0]= -1
		    self.MET_T1_phi[0]= -99
		    metVT1.SetPtEtaPhiM(0,0,0,0)
		    self.MET_T1Smear_pt[0]= -1
		    self.MET_T1Smear_phi[0]= -99
		    metVSmear.SetPtEtaPhiM(0,0,0,0)

		self.PuppiMET_pt[0]= entry.PuppiMET_pt
		self.PuppiMET_phi[0]= entry.PuppiMET_phi
		try : self.RawPuppiMET_pt[0] = entry.RawPuppiMET_pt
                except AttributeError : self.RawPuppiMET_pt[0] = -1
		try : self.RawPuppiMET_phi[0] = entry.RawPuppiMET_phi
                except AttributeError : self.RawPuppiMET_phi[0]= -99
		try : self.RawMET_pt[0]= entry.RawMET_pt
		except AttributeError : self.RawMET_pt[0] = -1
		try : self.RawMET_phi[0]= entry.RawMET_phi
		except AttributeError : self.RawMET_phi[0] = -99

	        try : metVR.SetPtEtaPhiM(entry.RawMET_pt,0, entry.RawMET_phi,0)
                except AttributeError : metVR.SetPtEtaPhiM(-1,0, -99,0)
	        metVR.SetPz(0.)
	        metVR.SetE(metVR.Pt())
		self.u_par_RawMET[0]= self.getu_par_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
		self.u_perp_RawMET[0]= self.getu_perp_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
            
		met = correctedMET(entry.MET_T1_pt, entry.MET_T1_phi, entry.PV_npvs, entry.run, isMC, yearin, True, False)
		mett = correctedMET(entry.MET_T1_pt, entry.MET_T1_phi, entry.PV_npvsGood, entry.run, isMC, yearin, True, False)
		self.METCor_T1_pt[0]= met[2]
		self.METCor_T1_phi[0]= met[3]

		self.METCorGood_T1_pt[0]= mett[2]
		self.METCorGood_T1_phi[0]= mett[3]
		
                if isMC:
		    self.MET_T1Smear_pt[0]= entry.MET_T1Smear_pt
		    self.MET_T1Smear_phi[0]= entry.MET_T1Smear_phi


		    mets = correctedMET(entry.MET_T1Smear_pt, entry.MET_T1Smear_phi, entry.PV_npvs, entry.run, isMC, yearin, True, False)
		    self.METCor_T1Smear_pt[0]= mets[2]
		    self.METCor_T1Smear_phi[0]= mets[3]

		    metts = correctedMET(entry.MET_T1Smear_pt, entry.MET_T1Smear_phi, entry.PV_npvsGood, entry.run, isMC, yearin, True, False)
		    self.METCorGood_T1Smear_pt[0]= metts[2]
		    self.METCorGood_T1Smear_phi[0]= metts[3]

		pmet = correctedMET(entry.PuppiMET_pt, entry.PuppiMET_phi, entry.PV_npvs, entry.run, isMC, yearin, True, True)
		pmett = correctedMET(entry.PuppiMET_pt, entry.PuppiMET_phi, entry.PV_npvsGood, entry.run, isMC, yearin, True, True)
		self.PuppiMETCor_pt[0]= pmet[2]
		self.PuppiMETCor_phi[0]= pmet[3]
		self.PuppiMETCorGood_pt[0]= pmett[2]
		self.PuppiMETCorGood_phi[0]= pmett[3]

		self.Puppiboson_pt[0] = (LepP+LepM).Pt()
		self.Puppiboson_phi[0] = (LepP+LepM).Phi()


                # in case of no corrections, the default MET is used
	        if  doUncertainties : 
		    if isMC: 
			self.MET_ptUnclusteredUp[0] =  (metV+metUn).Pt()
			self.MET_ptUnclusteredDown[0] =  (metV-metUn).Pt()
			self.MET_phiUnclusteredUp[0] =  (metV+metUn).Phi()
			self.MET_phiUnclusteredDown[0] =  (metV-metUn).Phi()
	     
			
			self.PuppiMET_ptJESUp[0] = entry.PuppiMET_ptJESUp
			self.PuppiMET_ptJESDown[0] = entry.PuppiMET_ptJESDown
			self.PuppiMET_ptJERUp[0] = entry.PuppiMET_ptJERUp
			self.PuppiMET_ptJERDown[0] = entry.PuppiMET_ptJERDown

			self.PuppiMET_phiJESUp[0] = entry.PuppiMET_phiJESUp
			self.PuppiMET_phiJESDown[0] = entry.PuppiMET_phiJESDown
			self.PuppiMET_phiJERUp[0] = entry.PuppiMET_phiJERUp
			self.PuppiMET_phiJERDown[0] = entry.PuppiMET_phiJERDown

			self.PuppiMET_ptUnclusteredUp[0] = entry.PuppiMET_ptUnclusteredUp
			self.PuppiMET_ptUnclusteredDown[0] = entry.PuppiMET_ptUnclusteredDown
			self.PuppiMET_phiUnclusteredUp[0] = entry.PuppiMET_phiUnclusteredUp
			self.PuppiMET_phiUnclusteredDown[0] = entry.PuppiMET_phiUnclusteredDown

			self.MET_T1_ptJESUp[0] = entry.MET_T1_pt_jesTotalUp
			self.MET_T1_ptJESDown[0] = entry.MET_T1_pt_jesTotalDown
			self.MET_T1_ptJERUp[0] = entry.MET_T1_pt_jerUp
			self.MET_T1_ptJERDown[0] = entry.MET_T1_pt_jerDown

			self.MET_T1_phiJESUp[0] = entry.MET_T1_phi_jesTotalUp
			self.MET_T1_phiJESDown[0] = entry.MET_T1_phi_jesTotalDown
			self.MET_T1_phiJERUp[0] = entry.MET_T1_phi_jerUp
			self.MET_T1_phiJERDown[0] = entry.MET_T1_phi_jerDown

			self.MET_T1_ptUnclusteredUp[0] = entry.MET_T1_pt_unclustEnUp
			self.MET_T1_ptUnclusteredDown[0] = entry.MET_T1_pt_unclustEnDown
			self.MET_T1_phiUnclusteredUp[0] = entry.MET_T1_phi_unclustEnUp
			self.MET_T1_phiUnclusteredDown[0] = entry.MET_T1_phi_unclustEnDown


                metflavorsM=['MET']
                systsM = ['_jesTotal', '_jer', '_unclustEn'] #MET_T1_pt_jesTotalDown
                #systsM = ['_jesTotal']
                metflavorsP=[ 'PuppiMET']
                systsP = ['JES', 'JER', 'Unclustered'] #MET_T1_pt_jesTotalDown

                dirs=['Up','Down']
                #adirs=['Up']
                systs=[]
                outvalues_pt_MET=[]
                outvalues_phi_MET=[]
                outvalues_pt_METs=[]
                outvalues_phi_METs=[]

                outvalues_pt_PMET=[]
                outvalues_phi_PMET=[]

                outvalues_pt_GMET=[]
                outvalues_phi_GMET=[]
                outvalues_pt_GMETs=[]
                outvalues_phi_GMETs=[]

                outvalues_pt_PGMET=[]
                outvalues_phi_PGMET=[]
                #print 'new event'
                if isMC and doUncertainties: 
                    for mfl in metflavorsM : 
                        for  syst in systsM :
                            for dr in dirs :
                                #print 'will be doing', mfl, syst, dr
				metpt = getattr(entry, "{0:s}_T1_pt{1:s}{2:s}".format(mfl, syst, dr), None)
				metphi = getattr(entry, "{0:s}_T1_phi{1:s}{2:s}".format(mfl, syst, dr), None)

                                #smear
				metpts = getattr(entry, "{0:s}_T1Smear_pt{1:s}{2:s}".format(mfl, syst, dr), None)
				metphis = getattr(entry, "{0:s}_T1Smear_phi{1:s}{2:s}".format(mfl, syst, dr), None)
		      
				pmet = correctedMET(metpt, metphi, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetg = correctedMET(metpt, metphi, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
				pmets = correctedMET(metpts, metphis, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetsg = correctedMET(metpts, metphis, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
                                ss=syst
                                if 'jes' in syst : ss = 'JES'
                                if 'jer' in syst : ss = 'JER'
                                if 'uncl' in syst : ss = 'Unclustered'
                                outvalues_pt_MET.append(pmet[2])
				outvalues_phi_MET.append(pmet[3])
                                #smear
				outvalues_pt_METs.append(pmets[2])
                                outvalues_phi_METs.append(pmets[3])

                                outvalues_pt_GMET.append(pmetg[2])
                                outvalues_phi_GMET.append(pmetg[3])

                                outvalues_pt_GMETs.append(pmetsg[2])
                                outvalues_phi_GMETs.append(pmetsg[3])
                                
      
				#print "{0:s}_T1_pt{1:s}{2:s}".format(mfl, syst, dr), "{0:s}_T1_phi{1:s}{2:s}".format(mfl, syst, dr), metpt, metphi, entry.MET_T1_pt, entry.MET_T1_phi, entry.PuppiMET_pt, entry.PuppiMET_phi, getattr(self,"{0:s}Cor_T1_pt{1:s}{2:s}".format(mfl, ss, dr)), "{0:s}Cor_T1_pt{1:s}{2:s}".format(mfl, ss, dr), pmet[2], pmet[3]
                                #print  "{0:s}Cor_T1_pt{1:s}{2:s}".format(mfl, ss, dr), getattr(self,"{0:s}Cor_T1_pt{1:s}{2:s}[0]".format(mfl, ss, dr) ), pmet[2], pmet[3]
                    for mfl in metflavorsP : 
                        for  syst in systsP :
                            for dr in dirs :
                                
				metpt = getattr(entry, "{0:s}_pt{1:s}{2:s}".format(mfl, syst, dr), None)
				metphi = getattr(entry, "{0:s}_phi{1:s}{2:s}".format(mfl, syst, dr), None)

		      
				pmet = correctedMET(metpt, metphi, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetg = correctedMET(metpt, metphi, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
      
				#print "{0:s}_pt{1:s}{2:s}".format(mfl, syst, dr), "{0:s}_phi{1:s}{2:s}".format(mfl, syst, dr), metpt, metphi, entry.MET_T1_pt, entry.MET_T1_phi, entry.PuppiMET_pt, entry.PuppiMET_phi, pmet[2], pmet[3]
                                outvalues_pt_PMET.append(pmet[2])
                                outvalues_phi_PMET.append(pmet[3])
                                outvalues_pt_PGMET.append(pmetg[2])
                                outvalues_phi_PGMET.append(pmetg[3])



		    #print  outvalues_pt_MET,  outvalues_pt_PMET
		    #self.METCor_T1_ptJESUp[0] = outvalues_pt_MET[0]
		    #self.METCor_T1_pt[0] = outvalues_pt_MET[0]
		    #print outvalues_pt_MET[0]

		    self.METCor_T1_ptJESUp[0] = outvalues_pt_MET[0]
		    self.METCor_T1_phiJESUp[0] = outvalues_phi_MET[0]
		    self.METCor_T1_ptJESDown[0] = outvalues_pt_MET[1]
		    self.METCor_T1_phiJESDown[0] = outvalues_phi_MET[1]
		    self.METCor_T1_ptJERUp[0] = outvalues_pt_MET[2]
		    self.METCor_T1_phiJERUp[0] = outvalues_phi_MET[2]
		    self.METCor_T1_ptJERDown[0] = outvalues_pt_MET[3]
		    self.METCor_T1_phiJERDown[0] = outvalues_phi_MET[3]
		    self.METCor_T1_ptUnclusteredUp[0] = outvalues_pt_MET[4]
		    self.METCor_T1_phiUnclusteredUp[0] = outvalues_phi_MET[4]
		    self.METCor_T1_ptUnclusteredDown[0] = outvalues_pt_MET[5]
		    self.METCor_T1_phiUnclusteredDown[0] = outvalues_phi_MET[5]
                    #smear
		    self.METCor_T1Smear_ptJESUp[0] = outvalues_pt_METs[0]
		    self.METCor_T1Smear_phiJESUp[0] = outvalues_phi_METs[0]
		    self.METCor_T1Smear_ptJESDown[0] = outvalues_pt_METs[1]
		    self.METCor_T1Smear_phiJESDown[0] = outvalues_phi_METs[1]
		    self.METCor_T1Smear_ptJERUp[0] = outvalues_pt_METs[2]
		    self.METCor_T1Smear_phiJERUp[0] = outvalues_phi_METs[2]
		    self.METCor_T1Smear_ptJERDown[0] = outvalues_pt_METs[3]
		    self.METCor_T1Smear_phiJERDown[0] = outvalues_phi_METs[3]
		    self.METCor_T1Smear_ptUnclusteredUp[0] = outvalues_pt_METs[4]
		    self.METCor_T1Smear_phiUnclusteredUp[0] = outvalues_phi_METs[4]
		    self.METCor_T1Smear_ptUnclusteredDown[0] = outvalues_pt_METs[5]
		    self.METCor_T1Smear_phiUnclusteredDown[0] = outvalues_phi_METs[5]




		    self.PuppiMETCor_ptJESUp[0] = outvalues_pt_PMET[0]
		    self.PuppiMETCor_phiJESUp[0] = outvalues_phi_PMET[0]
		    self.PuppiMETCor_ptJESDown[0] = outvalues_pt_PMET[1]
		    self.PuppiMETCor_phiJESDown[0] = outvalues_phi_PMET[1]
		    self.PuppiMETCor_ptJERUp[0] = outvalues_pt_PMET[2]
		    self.PuppiMETCor_phiJERUp[0] = outvalues_phi_PMET[2]
		    self.PuppiMETCor_ptJERDown[0] = outvalues_pt_PMET[3]
		    self.PuppiMETCor_phiJERDown[0] = outvalues_phi_PMET[3]
		    self.PuppiMETCor_ptUnclusteredUp[0] = outvalues_pt_PMET[4]
		    self.PuppiMETCor_phiUnclusteredUp[0] = outvalues_phi_PMET[4]
		    self.PuppiMETCor_ptUnclusteredDown[0] = outvalues_pt_PMET[5]
		    self.PuppiMETCor_phiUnclusteredDown[0] = outvalues_phi_PMET[5]


		    self.METCorGood_T1_ptJESUp[0] = outvalues_pt_GMET[0]
		    self.METCorGood_T1_phiJESUp[0] = outvalues_phi_GMET[0]
		    self.METCorGood_T1_ptJESDown[0] = outvalues_pt_GMET[1]
		    self.METCorGood_T1_phiJESDown[0] = outvalues_phi_GMET[1]
		    self.METCorGood_T1_ptJERUp[0] = outvalues_pt_GMET[2]
		    self.METCorGood_T1_phiJERUp[0] = outvalues_phi_GMET[2]
		    self.METCorGood_T1_ptJERDown[0] = outvalues_pt_GMET[3]
		    self.METCorGood_T1_phiJERDown[0] = outvalues_phi_GMET[3]
		    self.METCorGood_T1_ptUnclusteredUp[0] = outvalues_pt_GMET[4]
		    self.METCorGood_T1_phiUnclusteredUp[0] = outvalues_phi_GMET[4]
		    self.METCorGood_T1_ptUnclusteredDown[0] = outvalues_pt_GMET[5]
		    self.METCorGood_T1_phiUnclusteredDown[0] = outvalues_phi_GMET[5]


		    self.METCorGood_T1Smear_ptJESUp[0] = outvalues_pt_GMETs[0]
		    self.METCorGood_T1Smear_phiJESUp[0] = outvalues_phi_GMETs[0]
		    self.METCorGood_T1Smear_ptJESDown[0] = outvalues_pt_GMETs[1]
		    self.METCorGood_T1Smear_phiJESDown[0] = outvalues_phi_GMETs[1]
		    self.METCorGood_T1Smear_ptJERUp[0] = outvalues_pt_GMETs[2]
		    self.METCorGood_T1Smear_phiJERUp[0] = outvalues_phi_GMETs[2]
		    self.METCorGood_T1Smear_ptJERDown[0] = outvalues_pt_GMETs[3]
		    self.METCorGood_T1Smear_phiJERDown[0] = outvalues_phi_GMETs[3]
		    self.METCorGood_T1Smear_ptUnclusteredUp[0] = outvalues_pt_GMETs[4]
		    self.METCorGood_T1Smear_phiUnclusteredUp[0] = outvalues_phi_GMETs[4]
		    self.METCorGood_T1Smear_ptUnclusteredDown[0] = outvalues_pt_GMETs[5]
		    self.METCorGood_T1Smear_phiUnclusteredDown[0] = outvalues_phi_GMETs[5]



		    self.PuppiMETCorGood_ptJESUp[0] = outvalues_pt_PGMET[0]
		    self.PuppiMETCorGood_phiJESUp[0] = outvalues_phi_PGMET[0]
		    self.PuppiMETCorGood_ptJESDown[0] = outvalues_pt_PGMET[1]
		    self.PuppiMETCorGood_phiJESDown[0] = outvalues_phi_PGMET[1]
		    self.PuppiMETCorGood_ptJERUp[0] = outvalues_pt_PGMET[2]
		    self.PuppiMETCorGood_phiJERUp[0] = outvalues_phi_PGMET[2]
		    self.PuppiMETCorGood_ptJERDown[0] = outvalues_pt_PGMET[3]
		    self.PuppiMETCorGood_phiJERDown[0] = outvalues_phi_PGMET[3]
		    self.PuppiMETCorGood_ptUnclusteredUp[0] = outvalues_pt_PGMET[4]
		    self.PuppiMETCorGood_phiUnclusteredUp[0] = outvalues_phi_PGMET[4]
		    self.PuppiMETCorGood_ptUnclusteredDown[0] = outvalues_pt_PGMET[5]
		    self.PuppiMETCorGood_phiUnclusteredDown[0] = outvalues_phi_PGMET[5]


			# Define a list of variations and their corresponding attribute names
                #metV.SetPtEtaPhiM(entry.PuppiMET_ptUnclusteredDown,0, entry.PuppiMET_phiUnclusteredDown,0)
                if isMC and doUncertainties: 
		    main_branches = ['MET_T1', 'METCor_T1', 'METCorGood_T1', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood']
		    #main_branches = ['MET_T1']

		    systematics = ['', 'JES', 'JER', 'Unclustered']
		    #systematics = ['', 'JES']
		    #systematics = ['Unclustered']
		    variations = ['Up', 'Down']
		    for branch in main_branches:
			for systematic in systematics:
			    if systematic ==  '' :

				pt_value = getattr(self, branch + '_pt')
				phi_value = getattr(self, branch + '_phi')
				metV.SetPtEtaPhiM(float(pt_value[0]), 0.0, float(phi_value[0]), 0.0)
				metV.SetPz(0.)
				metV.SetE(metV.Pt())

				u_par_value = self.getu_par_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                #setattr(self, 'u_par_' + branch+'[0]', array.array('f', [u_par_value]))
                                getattr(self, 'u_par_' + branch)[0] = u_par_value
				u_perp_value = self.getu_perp_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                #setattr(self, 'u_perp_' + branch+'[0]', array.array('f', [u_perp_value]))
                                getattr(self, 'u_perp_' + branch)[0] = u_perp_value
                                #self.t.GetBranch('u_par_' + branch).Fill()
                                #self.t.GetBranch('u_perp_' + branch).Fill()


				print("Branch:", 'u_par_' + branch, "Value:", u_par_value)
				print("Branch:", 'u_perp_' + branch, "Value:", u_perp_value)

			    else : 
				for variation in variations:

					pt_value = getattr(self, branch + '_pt' + systematic + variation)
					phi_value = getattr(self, branch + '_phi' + systematic + variation)

					metV.SetPtEtaPhiM(float(pt_value[0]), 0.0, float(phi_value[0]), 0.0)
					metV.SetPz(0.)
					metV.SetE(metV.Pt())


					u_par_value = self.getu_par_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
					#setattr(self, 'u_par_' + branch + '_' + systematic + variation+'[0]', array.array('f', [u_par_value]))
                                        getattr(self, 'u_par_' + branch +  systematic + variation)[0] = u_par_value

					u_perp_value = self.getu_perp_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
					#setattr(self, 'u_perp_' + branch + '_' + systematic + variation+'[0]', array.array('f', [u_perp_value]))
                                        getattr(self, 'u_perp_' + branch +  systematic + variation)[0] = u_perp_value

                                        #self.t.GetBranch('u_par_' + branch + '_' + systematic + variation).Fill()
                                        #self.t.GetBranch('u_perp_' + branch + '_' + systematic + variation).Fill()

					print("Branch:", 'u_par_' + branch + systematic + variation, "Value:", u_par_value)
					print("Branch:", 'u_perp_' + branch + systematic + variation, "Value:", u_perp_value)






					#print("pt_value: {} ({})".format(pt_value, type(pt_value)))
					#print("phi_value: {} ({})".format(phi_value, type(phi_value)))

			    #metV.SetPtEtaPhiM(float(pt_value[0]), 0.0, float(phi_value[0]), 0.0)


			    #u_par_value = self.getu_par_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
			    #u_perp_value = self.getu_perp_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())

			    #print("Setting attribute: u_par_{} with value: {}".format(attr_name, u_par_value))
			    #print("Setting attribute: u_perp_{} with value: {}".format(attr_name, u_perp_value))

	    if 'UL' in proc or '2016' not in str(era):
                try : 
                    self.Flag_hfNoisyHitsFilter[0] = int(entry.Flag_hfNoisyHitsFilter)
            
		except AttributeError:  self.Flag_hfNoisyHitsFilter[0] = 1

                try : self.Flag_BadPFMuonDzFilter[0] = int(entry.Flag_BadPFMuonDzFilter)
		except AttributeError: self.Flag_BadPFMuonDzFilter[0] = 1



	    if  doUncertainties : 



                '''
		self.boson_ptUnclusteredUp[0] = (metV+metUn+LepP+LepM).Pt()
		self.boson_phiUnclusteredUp[0] = (metV+metUn+LepP+LepM).Phi()

		self.boson_ptUnclusteredDown[0] = (metV-metUn+LepP+LepM).Pt()
		self.boson_phiUnclusteredDown[0] = (metV-metUn+LepP+LepM).Phi()
		#self.u_perp_MET_T1UnclusteredDown[0]=  (metV-metUn).Pt() * sin((LepP+LepM).Phi()-(metV-metUn).Phi())
		#r_METJESUpself.u_perp_MET_T1UnclusteredDown[0]=  (metV-metUn).Pt() * sin((LepP+LepM).Phi()-(metV-metUn).Phi())



		self.boson_ptJESUp[0] = (LepP+LepM).Pt()
		self.boson_phiJESUp[0] = (LepP+LepM).Phi()

		self.boson_ptJESDown[0] = (LepP+LepM).Pt()
		self.boson_phiJESDown[0] = (LepP+LepM).Phi()

		self.boson_ptJERUp[0] = (LepP+LepM).Pt()
		self.boson_phiJERUp[0] = (LepP+LepM).Phi()

		self.boson_ptJERDown[0] = (LepP+LepM).Pt()
		self.boson_phiJERDown[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptJESUp[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiJESUp[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptJESDown[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiJESDown[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptJERUp[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiJERUp[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptJERDown[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiJERDown[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptUnclusteredUp[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiUnclusteredUp[0] = (LepP+LepM).Phi()

		self.Puppiboson_ptUnclusteredDown[0] = (LepP+LepM).Pt()
		self.Puppiboson_phiUnclusteredDown[0] = (LepP+LepM).Phi()
                '''
		

		#print 'all systematics youcare ', self.allsystMET
		for i, v in enumerate(self.allsystMET) : 


		    try : j = getattr(entry, "{0:s}".format(str(v)))
		    except AttributeError : j = -9.99
		    self.list_of_arrays_noES[i][0] = j
		    #if '_pt_jerUp' in v  : print '=====================================while filling-----------------',j, self.list_of_arrays[i][0], i, v, entry.event 

		for i, v in enumerate(self.allsystJets) : 
		#njets_sys, nbtag_sys
		    jetList, jetListFlav, jetListEta, jetListPt, bTagListDeep, bJetListL,bJetListM, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist, era, str(v), proc) 
		    try : 
			self.list_of_arraysJetsNjets[i][0] = -1
			self.list_of_arraysJetsNjets[i][0] = len(jetList)#fix
			self.list_of_arraysJetsNbtagL[i][0] = len(bJetListL)
			self.list_of_arraysJetsNbtagM[i][0] = len(bJetListM)
			self.list_of_arraysJetsNbtagT[i][0] = len(bJetListT)
			#print 'jessyst===============!!!!!!!!!!!!', v, len(jetList), cat, jetList, self.list_of_arraysJetsNjets[i][0]
		    except IndexError : print 'hit the ceiling', len(jetListPt),  'event', entry.event, 'lumi', entry.luminosityBlock, 'run', entry.run

		    for ifl in range(len(jetList)) :
			try : 
			    self.list_of_arraysJetsPt[i][ifl] = jetListPt[ifl]
			    self.list_of_arraysJetsEta[i][ifl] = jetListEta[ifl]
			    self.list_of_arraysJetsFlavour[i][ifl] = jetListFlav[ifl]
			    #self.list_of_arraysJetsNbtagDeep[i][ifl] = bTagListDeep[ifl] #fix
			except IndexError : print 'hit the ceiling', len(jetListPt),  'event', entry.event, 'lumi', entry.luminosityBlock, 'run', entry.run

	    #fill the un-corrected or just in the case you dont care to doUncertainties      
	    nom_=''
	    sysj = ''
	    if doUncertainties : sysj='nom'
	    jetList, jetListFlav, jetListEta, jetListPt, bTagListDeep, bJetListL, bJetListM, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist,era,sysj,proc) 
            #print 'jessyst=========%%%%%%%%%%======!!!!!!!!!!!!', v, len(jetList), sysj, jetList
            self.njets[0], self.nbtagL[0], self.nbtagM[0], self.nbtagT[0]= -1, -1, -1, 1
	    self.njets[0] = len(jetList)
	    self.nbtagL[0] = len(bJetListL)
	    self.nbtagM[0] = len(bJetListM)
	    self.nbtagT[0] = len(bJetListT)
            #print 'and again', len(bJetListL),  len(bJetListM), len(bJetListT), self.nbtagL[0], self.nbtagM[0], self.nbtagT[0]
	    self.jpt[0]  = -9.99
	    self.jeta[0]  = -9.99
	    for ifl in range(len(jetListPt)) :
		try :
		    self.jflavour[ifl]  = jetListFlav[ifl]
		    self.jeta[ifl]  = jetListEta[ifl]
		    self.jpt[ifl]  = jetListPt[ifl]
		    self.btagDeep[ifl] = bTagListDeep[ifl]
		except IndexError : print 'we hit the ceiling', len(jetListPt),  'event', entry.event, 'lumi', entry.luminosityBlock, 'run', entry.run
	    #print self.jpt[0], self.jeta[0]
            '''
	    if self.nMuon[0] !=1 : print 'failed nMuon', entry.event, self.nMuon[0]
	    if self.nTau[0]!=0 :  print 'failed nTau', entry.event, self.nTau[0]
	    if (self.isGlobal_1[0]<1 and self.isTracker_1[0]<1) :  print 'failed muon Id', entry.event, self.isGlobal_1[0], self.isTracker_1[0]
	    if self.pt_1[0]<29 :  print 'failed pt', entry.event, self.pt_1[0]
	    if self.mediumId_1[0]<1 :  print 'failed mediumId', entry.event, self.mediumId_1[0]
	    if fabs(self.eta_1[0])>2.4 or  fabs(self.dZ_1[0])>0.2 or fabs(self.d0_1[0])>0.045:  print 'failed eta, dZ, d0', entry.event, fabs(self.eta_1[0]), fabs(self.dZ_1[0]),  fabs(self.d0_1[0])
	    if self.iso_1[0]>0.15 :  print 'failed iSo', entry.event, self.iso_1[0]
	    if self.isTrig_1[0]<1 :  print 'failed Trig', entry.event,  self.isTrig_1[0]
	    if self.nbtagT[0]>0 :  print 'failed bTag', entry.event, self.nbtagT[0]
	    if fabs(self.q_1[0]) !=1 :  print 'failed charge', entry.event, fabs(self.q_1[0])
	    '''
	    #SaveEvent = (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>24 and self.mediumId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.isTrig_1[0]>0 and self.nbtagT[0]==0
	    #SaveEvent=True
	    #if SaveEvent:
		#print 'I will save this......', entry.event
	    #if  self.nbtag[0] == 0 : 

	    #if self.nbtagL[0] == 0 :




	    if SystIndex == 0 : 
		self.t.Fill()
	    else : 
		self.tN[SystIndex-1].Fill()

	return



    def setWeight(self,weight) :
        self.weight[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPU(self,weight) :
        self.weightPU[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPUtrue(self,weight) :
        self.weightPUtrue[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return

    def FillTree(self) :
        self.t.Fill()

    def writeTree(self) :
        print("In outTuple.writeTree() entries={0:d}".format(self.entries))
        self.f.Write()
        self.f.Close()
        return



