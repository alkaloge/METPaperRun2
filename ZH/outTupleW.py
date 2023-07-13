# output ntuple for Wjets analysis for CMSSW_10_2_X

from ROOT import TLorentzVector, TH1
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
class outTupleW() :
    
    def __init__(self,fileName, era, doSyst=False,shift=[], isMC=True, onlyNom=False, isW=False):
        from array import array
        from ROOT import TFile, TTree

        self.sf_EleTrig = ''
        self.sf_EleTrig = SF.SFs()
        #Electron_RunUL2016postVFP_Ele25_EtaLt2p1.root  Electron_RunUL2016preVFP_Ele25_EtaLt2p1.root   Electron_RunUL2017_Ele35.root                  Electron_RunUL2018_Ele35.root
        self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2018_Ele35.root'}
        if '2016pre' in str(era):  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2016preVFP_Ele25_EtaLt2p1.root'}
        if '2016' in str(era) and 'pre' not in str(era):  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2016postVFP_Ele25_EtaLt2p1.root'}
        if '2017' in str(era) :  self.TriggerSF={'dir' : './', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron_RunUL2017_Ele35.root'}

        print 'era', era, self.TriggerSF['fileElectron']
        self.sf_EleTrig.ScaleFactor("{0:s}{1:s}".format(self.TriggerSF['dir'],self.TriggerSF['fileElectron']))


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
			self.list_of_arraysJetsFlavour.append( array('i',[-1]*15))
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
			    self.list_of_arraysJetsFlavour.append( array('i',[-1]*15))
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
        
        self.nGoodElectron    = array('I',[0])
        self.nGoodMuon        = array('I',[0])
        self.Flag_hfNoisyHitsFilter        = array('I',[0])
        self.Flag_BadPFMuonDzFilter        = array('I',[0])

        self.L1PreFiringWeight_Nom        = array('f',[0])
        self.L1PreFiringWeight_Up        = array('f',[0])
        self.L1PreFiringWeight_Down        = array('f',[0])

        self.d0_1        = array('f',[0])
        self.dZ_1        = array('f',[0])
        
        self.pt_uncor_1        = array('f',[0])
        self.m_uncor_1        = array('f',[0])

        self.Electron_mvaFall17V2noIso_WP90_1 = array('f',[0])
        self.Electron_mvaFall17V2Iso_WP90_1 = array('f',[0])
        self.Electron_cutBased_1 = array('f',[0])
        self.Electron_convVeto        = array('f',[0])
        self.Electron_lostHits        = array('I',[0])
        self.gen_match_1 = array('i',[0])


        # di-lepton variables.   1 and 2 refer to plus and minus charge
        self.mll       = array('f',[0])
        self.W_Pt       = array('f',[0])
        self.IDSF      = array('f',[0])
        self.IsoSF      = array('f',[0])
        self.TrigSF      = array('f',[0])
        #self.muonTightiDsf_1      = array('f',[0])

        self.m_1_tr   = array('f',[0])
        self.pt_1      = array('f',[0])
        self.pt_1_tr   = array('f',[0])
        self.GenPart_statusFlags_1   = array('i',[0])
        self.GenPart_status_1     = array('i',[0])
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
        
        # MET variables
        self.metcov00    = array('f',[0])
        self.metcov01    = array('f',[0])
        self.metcov10    = array('f',[0])
        self.metcov11    = array('f',[0])

	self.MET_pt = array('f',[-99])
	self.MET_phi = array('f',[-99])
	self.MET_phi = array('f',[-99])
	self.RawMET_pt = array('f',[-99])
	self.RawMET_phi = array('f',[-99])
	self.RawPuppiMET_pt = array('f',[-99])
	self.RawPuppiMET_phi = array('f',[-99])
	self.boson_pt = array('f',[-99])
	self.boson_phi = array('f',[-999])

        '''
	self.u_par_RawMET = array('f',[-999])
	self.u_perp_RawMET = array('f',[-999])
	self.u_par_RawPuppiMET = array('f',[-999])
	self.u_perp_RawPuppiMET = array('f',[-999])

	self.u_par_MET = array('f',[-999])
	self.u_perp_MET = array('f',[-999])
        '''

        if doSyst :

	    branches = ['MET', 'MET_T1', 'METCor_T1', 'METCorGood_T1', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear']
            if not isMC:  branches = ['MET', 'MET_T1', 'METCor_T1', 'METCorGood_T1', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood']

	    attributes = ['pt', 'phi']
	    variations = ['', 'JESUp', 'JESDown', 'JERUp', 'JERDown', 'UnclusteredUp', 'UnclusteredDown']
            if not isMC: variations = [''] 

	    for branch in branches:
		for attr in attributes:
		    for var in variations:
			#if (branch == 'MET' or branch == 'MET_T1') and var == '':
			if (branch == 'MET' ) and var == '':
			    continue
			branch_name = "{}_{}{}".format(branch, attr, var)
			setattr(self, branch_name, array('f', [-99]))
                        self.t.Branch(branch_name, getattr(self, branch_name), '{}/F'.format(branch_name))
			#print("Created branch--->:", branch_name)

	    branches = ['METboson', 'PuppiMETboson', 'METCorboson', 'PuppiMETCorboson','METCorGoodboson', 'PuppiMETCorGoodboson']

	    attributes = ['pt', 'phi', 'm']
	    variations = ['', 'JESUp', 'JESDown', 'JERUp', 'JERDown', 'UnclusteredUp', 'UnclusteredDown']
            if not isMC: variations = [''] 

	    for branch in branches:
		for attr in attributes:
		    for var in variations:
			branch_name = "{}_{}{}".format(branch, attr, var)
			setattr(self, branch_name, array('f', [-99]))
                        self.t.Branch(branch_name, getattr(self, branch_name), '{}/F'.format(branch_name))




	    branches = ['MET_T1', 'PuppiMET', 'METCor_T1', 'PuppiMETCor', 'METCorGood_T1', 'PuppiMETCorGood', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear']
            if not isMC:   branches = ['MET_T1', 'PuppiMET', 'METCor_T1', 'PuppiMETCor', 'METCorGood_T1', 'PuppiMETCorGood' ]
	    attributes = ['u_par', 'u_perp']
	    variations = ['','UnclusteredUp', 'UnclusteredDown', 'JESUp', 'JESDown', 'JERUp', 'JERDown']
            if not isMC: variations = [''] 


            for attr in attributes:
	        for branch in branches:
		    for var in variations:
			branch_name = "{}_{}{}".format(attr,branch,  var)
			setattr(self, branch_name, array('f', [-999]))
                        self.t.Branch(branch_name, getattr(self, branch_name), '{}/F'.format(branch_name))
			#print("Created branch:", branch_name)

	    branches = ['Wmass', 'WTmass'  ]
	    attributes = ['MET', 'METT1', 'METT1SmearCor', 'METT1SmearCorGood','METCor', 'METCorGood', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood'  ]
	    variations = ['','UnclusteredUp', 'UnclusteredDown', 'JESUp', 'JESDown', 'JERUp', 'JERDown']
            if not isMC: variations = [''] 

     
            for attr in attributes:
		for branch in branches:
		    for var in variations:
			branch_name = "{}{}{}".format(atr,branch,  var)
			setattr(self, branch_name, array('f', [-1.]))
			self.t.Branch(branch_name, getattr(self, branch_name), '{}/F'.format(branch_name))
			#print("Created branch:", branch_name)

	    branches = ['Wmass', 'WTmass'  ]
	    attributes = ['RawMET',  'RawPuppiMET'  ]
     
            for attr in attributes:
		for branch in branches:
		    branch_name = "{}{}".format(atr,branch,  )
		    setattr(self, branch_name, array('f', [-1.]))
		    self.t.Branch(branch_name, getattr(self, branch_name), '{}/F'.format(branch_name))
		    #print("Created branch:", branch_name)



        '''
	self.DphiWMET = array('f',[0])
	self.DphiWPuppiMET = array('f',[0])
	self.DphilMET = array('f',[0])
	self.DphilPuppiMET = array('f',[0])
        '''


        self.isTrig_1   = array('f',[0])
        self.isTrigObj   = array('I',[0])

        # jet variables
        #self.njetsold = array('f',[-1]*15)

        self.njets     = array('i',[0])
        self.nbtagL     = array('i',[0])
        self.nbtagM     = array('i',[0])
        self.nbtagT     = array('i',[0])

        self.jflavour     = array('i',[-9]*15)
        self.jeta     = array('f',[-9.99]*15)
        self.jpt     = array('f',[-9.99]*15)
        self.btagDeep     = array('f',[-9.99]*15)

        self.bpt_1     = array('f',[-9.99]*15)
        self.bpt_1_tr  = array('f',[-9.99]*15)
        self.beta_1    = array('f',[-9.99]*15)
        self.beta_1_tr = array('f',[-9.99]*15)
        self.bphi_1    = array('f',[-9.99]*15)
        self.bphi_1_tr = array('f',[-9.99]*15)
        self.bcsv_1    = array('f',[-9.99]*15)
        self.bcsvfv_1    = array('f',[-9.99]*15)

      
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


        self.t.Branch('pt_1',        self.pt_1,        'pt_1/F')
        self.t.Branch('IDSF',        self.IDSF,        'IDSF/F')
        self.t.Branch('TrigSF',        self.TrigSF,        'TrigSF/F')
        self.t.Branch('IsoSF',        self.IsoSF,        'IsoSF/F')
        self.t.Branch('m_1_tr',     self.m_1_tr,     'm_1_tr/F')
        self.t.Branch('pt_1_tr',     self.pt_1_tr,     'pt_1_tr/F')
        self.t.Branch('phi_1',       self.phi_1,       'phi_1/F')  
        self.t.Branch('phi_1_tr',    self.phi_1_tr,    'phi_1_tr/F')
        self.t.Branch('eta_1',       self.eta_1,       'eta_1/F')    
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
 

        # MET variables
        self.t.Branch('metcov00', self.metcov00, 'metcov00/F')
        self.t.Branch('metcov01', self.metcov01, 'metcov01/F')
        self.t.Branch('metcov10', self.metcov10, 'metcov10/F')
        self.t.Branch('metcov11', self.metcov11, 'metcov11/F')



        self.t.Branch('MET_pt', self.MET_pt, 'MET_pt /F')
        self.t.Branch('MET_phi', self.MET_phi, 'MET_phi /F')

        self.t.Branch('RawMET_pt', self.RawMET_pt, 'RawMET_pt /F')
        self.t.Branch('RawMET_phi', self.RawMET_phi, 'RawMET_phi /F')
        self.t.Branch('RawPuppiMET_pt', self.RawPuppiMET_pt, 'RawPuppiMET_pt /F')
        self.t.Branch('RawPuppiMET_phi', self.RawPuppiMET_phi, 'RawPuppiMET_phi /F')

        self.t.Branch('PuppiMET_pt', self.PuppiMET_pt, 'PuppiMET_pt /F')
        self.t.Branch('PuppiMET_phi', self.PuppiMET_phi, 'PuppiMET_phi /F')

        self.t.Branch('u_par_RawMET', self.u_par_RawMET, 'u_par_RawMET /F')
        self.t.Branch('u_perp_RawMET', self.u_perp_RawMET, 'u_perp_RawMET /F')
        self.t.Branch('u_par_MET', self.u_par_MET, 'u_par_MET /F')
        self.t.Branch('u_perp_MET', self.u_perp_MET, 'u_perp_MET /F')
        self.t.Branch('u_par_RawPuppiMET', self.u_par_RawPuppiMET, 'u_par_RawPuppiMET /F')
        self.t.Branch('u_perp_RawPuppiMET', self.u_perp_RawPuppiMET, 'u_perp_RawPuppiMET /F')


	self.t.Branch('MET_significance', self.MET_significance, 'MET_significance /F')
        self.t.Branch('boson_pt', self.boson_pt, 'boson_pt /F')
        self.t.Branch('boson_phi', self.boson_phi, 'boson_phi /F')


        # trigger sf
        self.t.Branch('isTrig_1',  self.isTrig_1, 'isTrig_1/F' )
        self.t.Branch('isLead_1',  self.isLead_1, 'isLead_1/F' )
        self.t.Branch('isTrigObj',  self.isTrigObj, 'isTrigObj/l' )


        # jet variables
        self.t.Branch('njets', self.njets, 'njets/i')
        self.t.Branch('nbtagL', self.nbtagL, 'nbtagL/i')
        self.t.Branch('nbtagM', self.nbtagM, 'nbtagM/i')
        self.t.Branch('nbtagT', self.nbtagT, 'nbtagT/i')

        self.t.Branch('jflavour',     self.jflavour,     'jflavour[15]/i' )
        self.t.Branch('jeta',     self.jeta,     'jeta[15]/F' )
        self.t.Branch('jpt',     self.jpt,     'jpt[15]/F' )
        self.t.Branch('btagDeep', self.btagDeep, 'btagDeep[15]/i')


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
		    self.t.Branch('jflavour{0:s}'.format(v), self.list_of_arraysJetsFlavour[i], 'jflavour{0:s}[15]/i'.format(v))
		    self.t.Branch('jpt{0:s}'.format(v), self.list_of_arraysJetsPt[i], 'jpt{0:s}[15]/F'.format(v))
		    self.t.Branch('jeta{0:s}'.format(v), self.list_of_arraysJetsEta[i], 'jeta{0:s}[15]/F'.format(v))
		    self.t.Branch('btagDeep{0:s}'.format(v), self.list_of_arraysJetsNbtagDeep[i], 'btagDeep{0:s}[15]/F'.format(v))

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

                #print '====================>',self.tN[i-1], self.tN[i-1].GetName()

	self.t.SetBranchStatus("GenPart*",1)
	self.t.SetBranchStatus("*_tr*",1)
	#self.t.SetBranchStatus("*LHE*",1)
	self.t.SetBranchStatus("*LHEScaleWeight*",1)
	self.t.SetBranchStatus("*Up*",1)
	self.t.SetBranchStatus("*Down*",1)

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
                #if entry.event==18093 and syst=='_jesEC2Up' : print 'inside jets', jpt[j], syst, entry.event, "Jet_pt{0:s}".format(str(syst))

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
			#if entry.event == 207273709 : print 'seems goodfor iv--->', iv, 'jet', j, entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
			if j not in goodJets : goodJets.append(j)
		    else: 
			#if entry.event == 207273709 : print ' failed for lepton--->', iv, 'jet', j, 'njets', entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
			if j not in failJets : failJets.append(j)
			#continue
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
    

    def FillW(self, entry, cat, Lep, lepList, tauList, photonList, electronList, muonList, isMC, era, doUncertainties=False , proc="EOY") : 
    #def Fill(self, entry, SVFit, cat, jt1, jt2, LepP, LepM, lepList, isMC, era, doUncertainties=False ,  met_pt=-99, met_phi=-99, systIndex=0) : 
        SystIndex = 0

        #if SystIndex >0 : doUncertainties=False

        #channel_ll = 'mm' or 'ee'
        channel_ll = cat
	channel = cat

        if SystIndex ==0 : 

	    is_trig_1, is_trig_2, is_Dtrig_1, obj_1 = 0., 0., 0.,0.
	    TrigListLep = []
	    TrigListTau = []
	    hltListLep  = []
	    hltListLepSubL  = []
            objList=[]
	    TrigListLep, hltListLep, hltListLepSubL = GF.findSingleLeptTrigger(lepList, entry, channel_ll, era)
	    TrigListLep = list(dict.fromkeys(TrigListLep))
	    #if len(hltListLep) > 0 or len(hltListLepSubL)>0 :     print GF.printEvent(entry), SystIndex
	    if len(hltListLep) > 0 and  len(hltListLepSubL) == 0 :
		is_trig_1 = 1
	    if len(hltListLep) == 0 and len(hltListLepSubL) > 0 :
		is_trig_1 = 2
	    if len(hltListLep) > 0 and len(hltListLepSubL)>0 :
		is_trig_1 = 3
            #for 2016 UL, leadL= IsoMu24, subLeadL = IsoTkMu24 should give 2 if both fire,

	    self.whichTriggerWord[0]=0
	    self.whichTriggerWordSubL[0]=0

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
	    self.VetoTau[0]  = len(tauList)
	    self.VetoPhoton[0]  = len(photonList)
	    self.VetoElectron[0]  = len(electronList)
	    self.VetoMuon[0]  = len(muonList)
	    self.lumi[0] = entry.luminosityBlock 
	    self.evnt[0]  = entry.event
	    self.iso_1[0]  = -1
	    self.PFiso_1[0]  = -1
	    self.q_1[0]  = -2


	    self.isGlobal_1[0]      = -1
	    self.isStandalone_1[0]      = -1
	    self.isPFcand_1[0]      = -1
	    self.isTracker_1[0]     = -1
	    self.inTimeMuon_1[0]  = -1
	    self.highPtId_1[0]  = -99
	    self.highPurity_1[0]  = -1

	    self.ip3d_1[0]  = -99
	    self.sip3d_1[0]  = -99
	    self.looseId_1[0]       = -1
	    self.mediumId_1[0]       = -1 
	    self.pfIsoId_1[0]       = -1 
	    self.mediumPromptId_1[0]   = -1
	    self.tightId_1[0]       = -1 
	    self.tightCharge_1[0] = -1

	    self.GenPart_statusFlags_1[0]    = -1
	    self.GenPart_status_1[0]    = -1
	    self.gen_match_1[0] = -1


	    try:
		self.L1PreFiringWeight_Nom[0] = entry.L1PreFiringWeight_Nom
		self.L1PreFiringWeight_Up[0] = entry.L1PreFiringWeight_Up
		self.L1PreFiringWeight_Down[0] = entry.L1PreFiringWeight_Dn
	    except AttributeError : 
		self.L1PreFiringWeight_Nom[0] = 1
		self.L1PreFiringWeight_Up[0] = 1
		self.L1PreFiringWeight_Down[0] = 1


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
	self.cat[0]  = tauFun2.catToNumberW(cat)


        self.pt_1[0]   = Lep.Pt()
        self.phi_1[0]  = Lep.Phi()
        self.eta_1[0]  = Lep.Eta()
        muoneff=1.
        muoniso=1.
        muontrig=1.
        eleeff=1.
        eleiso=1.
        eletrig=1.
	self.IDSF[0]  = 1.
	self.IsoSF[0]  = 1.
	self.TrigSF[0]  = 1.
	yearin=era
        if isMC :
	    if '2016' in era and 'pre' in era : yearin='2016preVFP'
	    if '2016' in era and 'pre' not in era : yearin='2016postVFP'

	    if channel_ll == 'mnu' : 
		  
		muoneff = self.evaluator["NUM_TightID_DEN_TrackerMuons"].evaluate("{0:s}_UL".format( str(yearin)), fabs(Lep.Eta()), Lep.Pt(), "sf")
		muoniso = self.evaluator["NUM_TightRelIso_DEN_TightIDandIPCut"].evaluate("{0:s}_UL".format(str(yearin)), fabs(Lep.Eta()), Lep.Pt(), "sf")
		if era == '2016' : muontrig = self.evaluator["NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(yearin)), fabs(Lep.Eta()), Lep.Pt(), "sf")
                #NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight  
		if era =='2017' :  muontrig = self.evaluator["NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(Lep.Eta()), Lep.Pt(), "sf")
		if era =='2018' :  muontrig = self.evaluator["NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate("{0:s}_UL".format(str(era)), fabs(Lep.Eta()), Lep.Pt(), "sf")  ### for 2018 the json Veto only 24 SF..but we have used the HLT27
		#print 'sfs are', muoneff , muoniso, muontrig

		self.IDSF[0]  = muoneff
		self.IsoSF[0]  = muoniso
		self.TrigSF[0]  = muontrig

	    if channel_ll == 'enu' : 
		eleeff = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "RecoAbove20", Lep.Eta(), Lep.Pt() )
		eleiso = self.evaluatorEl["UL-Electron-ID-SF"].evaluate(yearin, "sf" , "wp90iso", Lep.Eta(), Lep.Pt() )

		self.IDSF[0]  = eleeff
                self.IsoSF[0]  = eleiso
                self.TrigSF[0] = 1.
                eff_trig_d_1 =  self.sf_EleTrig.get_EfficiencyData(Lep.Pt,Lep.Eta())
                eff_trig_mc_1 =  self.sf_EleTrig.get_EfficiencyMC(Lep.Pt,Lep.Eta())
                if eff_trig_mc_1 !=0 :    self.TrigSF[0] = float(eff_trig_d_1/eff_trig_mc_1)
		else : self.TrigSF[0]  = 1.




	lep_index_1 = lepList[0]

	if SystIndex ==0 : 
	    self.isTrig_1[0]   = is_trig_1
        #print 'cat', cat, channel_ll, self.pt_1[0], self.eta_1[0], self.isTrig_1[0]
	leplist=[]
	leplist.append(Lep)

	if channel_ll == 'enu' : 
      
            self.iso_1[0]  = entry.Electron_pfRelIso03_all[lep_index_1]
            self.q_1[0]  = entry.Electron_charge[lep_index_1]
            self.d0_1[0]   = entry.Electron_dxy[lep_index_1]
            self.dZ_1[0]   = entry.Electron_dz[lep_index_1]
            self.Electron_mvaFall17V2noIso_WP90_1[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_1]
            self.Electron_mvaFall17V2Iso_WP90_1[0]  = entry.Electron_mvaFall17V2Iso_WP90[lep_index_1]
            self.Electron_cutBased_1[0]  = entry.Electron_cutBased[lep_index_1]
            self.Electron_convVeto[0]  = entry.Electron_convVeto[lep_index_1]
            self.Electron_lostHits[0]  = ord(entry.Electron_lostHits[lep_index_1])
	    #if SystIndex ==0 and  isMC : 
            #	self.pt_uncor_1[0] = ePt[lep_index_1]
            #	self.m_uncor_1[0] = eMass[lep_index_1]

            if isMC :
		self.gen_match_1[0] = ord(entry.Electron_genPartFlav[lep_index_1])

	if channel_ll == 'mnu' : 
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

        
	# genMatch the di-lepton variables
	if isMC :
	    idx_Lep1 = -1
	    idx_Lep1_tr = -1
	    if (Lep.M() > 0.05): # muon mass 
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep, 'm')
		try :
		    idx_Lep1_tr = entry.Muon_genPartIdx[idx_Lep1]
		except IndexError : pass 
		    
	    elif (Lep.M() < 0.05 < 0.05): # electron mass
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep, 'e')
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
	
	SaveEventMu = False
	SaveEventEl = False

	if '2016' in era:  
            SaveEventMu = cat=='mnu' and (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>26 and self.tightId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.isTrig_1[0]>0 and (self.iso_1[0] < 0.5 or self.PFiso_1[0]>2) # and fabs(self.PVz[0])<26 and (self.PVy[0]*self.PVy[0] + self.PVx[0]*self.PVx[0])<3 and self.nPV[0]>2 
            SaveEventEl = cat=='enu' and  self.pt_1[0]>27 and self.Electron_mvaFall17V2Iso_WP90_1[0]>0 and fabs(self.eta_1[0])<2.1 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.isTrig_1[0]>0 and self.iso_1[0] < 0.5 #and fabs(self.PVz[0])<26  and (self.PVy[0]*self.PVy[0] + self.PVx[0]*self.PVx[0])<3 and self.nPV[0]>2 
            #print "self.isGlobal_1[0]>0", self.isGlobal_1[0]>0, "self.isTracker_1[0]>0", self.isTracker_1[0]>0, "self.pt_1[0]>26", self.pt_1[0]>26, "self.tightId_1[0]>0", self.tightId_1[0]>0, "fabs(self.eta_1[0])<2.4", fabs(self.eta_1[0])<2.4, "fabs(self.dZ_1[0])<0.2", fabs(self.dZ_1[0])<0.2, "self.iso_1[0] < 0.5 or self.PFiso_1[0]>2", self.iso_1[0] < 0.5 or self.PFiso_1[0]>2, era, "self.isTrig_1[0]>0", self.isTrig_1[0]>0

        else : 
	    SaveEventMu = cat=='mnu' and (self.isGlobal_1[0]>0 or self.isTracker_1[0]>0) and self.pt_1[0]>29 and self.tightId_1[0]>0 and fabs(self.eta_1[0])<2.4 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.isTrig_1[0]>0 and (self.iso_1[0] < 0.5 or self.PFiso_1[0]>2)#and fabs(self.PVz[0])<26  and (self.PVy[0]*self.PVy[0] + self.PVx[0]*self.PVx[0])<3 and self.nPV[0]>2 
	    SaveEventEl = cat=='enu' and  self.pt_1[0]>37 and self.Electron_mvaFall17V2Iso_WP90_1[0]>0 and fabs(self.eta_1[0])<2.1 and  fabs(self.dZ_1[0])<0.2 and  fabs(self.d0_1[0])<0.045 and self.isTrig_1[0]>0 and self.iso_1[0] < 0.5 #and fabs(self.PVz[0])<26  and (self.PVy[0]*self.PVy[0] + self.PVx[0]*self.PVx[0])<3 and self.nPV[0]>2 
        #print 'saveeent', SaveEventMu, SaveEventEl, cat
        #if entry.genWeight > 10 : 
        #    SaveEventMu = False
        #    SaveEventEl = False

        if SaveEventMu or SaveEventEl:

	#if True:  

	    self.MET_significance[0]= entry.MET_significance
	    pmetV, metV, metVT1, metVP, metVR, metUn, metVTest, metVSmear, metVTestSmear=  TLorentzVector(),TLorentzVector(),TLorentzVector(),TLorentzVector(),  TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector()
            self.Flag_hfNoisyHitsFilter[0] = 1
            self.Flag_BadPFMuonDzFilter[0] = 1

	    if 'UL' in proc :

		try:
                    self.MET_pt[0]= entry.MET_pt
		    self.MET_phi[0]= entry.MET_phi
	            metV.SetPtEtaPhiM(entry.MET_pt,0, entry.MET_phi,0)
		    metV.SetPz(0.)
		    metV.SetE(metV.Pt())

		    #self.u_par_MET[0]= self.getu_par_MET( entry, metV.X(), metV.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
		    #self.u_perp_MET[0]= self.getu_perp_MET( entry, metV.X(), metV.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
                    self.METWmass[0] = (metV+Lep).M()
                    self.METWTmass[0] = (metV+Lep).Mt()

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
		    metVT1.SetE(metVT1.Pt())
                    self.METT1Wmass[0] = (metVT1+Lep).M()
                    self.METT1WTmass[0] = (metVT1+Lep).Mt()

		    metVSmear.SetPtEtaPhiM(entry.MET_T1Smear_pt,0, entry.MET_T1Smear_phi,0)
		    metVSmear.SetPz(0.)
		    metVSmear.SetE(metV.Pt())
                    self.METT1SmearWmass[0] = (metVSmear+Lep).M()
                    self.METT1SmearWTmass[0] = (metVSmear+Lep).Mt()


		    metVP.SetPtEtaPhiM(entry.PuppiMET_pt,0, entry.PuppiMET_phi,0)
		    metVP.SetPz(0.)
		    metVP.SetE(metVP.Pt())
                    self.PuppiMETWmass[0] = (metVT1+Lep).M()
                    self.PuppiMETWTmass[0] = (metVT1+Lep).Mt()

		except AttributeError : 
		    self.MET_T1_pt[0]= -1
		    self.MET_T1_phi[0]= -99
		    metVT1.SetPtEtaPhiM(0,0,0,0)
		    self.MET_T1Smear_pt[0]= -1
		    self.MET_T1Smear_phi[0]= -99

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
		#self.u_par_RawMET[0]= self.getu_par_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
		#self.u_perp_RawMET[0]= self.getu_perp_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )

	        try : metVR.SetPtEtaPhiM(entry.RawPuppiMET_pt,0, entry.RawPuppiMET_phi,0)
                except AttributeError : metVR.SetPtEtaPhiM(-1,0, -99,0)
	        metVR.SetPz(0.)
	        metVR.SetE(metVR.Pt())
		self.RawMETWmass[0] = (metVR+Lep).M()
		self.RawMETWTmass[0] = (metVR+Lep).Mt()

		metVP.SetPtEtaPhiM(entry.RawPuppiMET_pt,0, entry.RawPuppiMET_phi,0)
		metVP.SetPz(0.)
		metVP.SetE(metVP.Pt())
		self.PuppiMETWmass[0] = (metVP+Lep).M()
		self.PuppiMETWTmass[0] = (metVP+Lep).Mt()

		#self.u_par_RawPuppiMET[0]= self.getu_par_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
		#self.u_perp_RawPuppiMET[0]= self.getu_perp_MET( entry, metVR.X(), metVR.Y(), (LepP+LepM).X(), (LepP+LepM).Y(), (LepP+LepM).Pt() )
            
		met = correctedMET(entry.MET_T1_pt, entry.MET_T1_phi, entry.PV_npvs, entry.run, isMC, yearin, True, False)
		mett = correctedMET(entry.MET_T1_pt, entry.MET_T1_phi, entry.PV_npvsGood, entry.run, isMC, yearin, True, False)
		self.METCor_T1_pt[0]= met[2]
		self.METCor_T1_phi[0]= met[3]

		self.METCorGood_T1_pt[0]= mett[2]
		self.METCorGood_T1_phi[0]= mett[3]

		metVT1.SetPtEtaPhiM(mett[2],0, mett[3],0)
		metVT1.SetPz(0.)
		metVT1.SetE(metVT1.Pt())
		self.METT1CorGoodWmass[0] = (metVT1+Lep).M()
		self.METT1CorGoodWTmass[0] = (metVT1+Lep).Mt()

		metVSmear.SetPtEtaPhiM(entry.MET_T1Smear_pt,0, entry.MET_T1Smear_phi,0)
		metVSmear.SetPz(0.)
		metVSmear.SetE(metV.Pt())
		self.METT1SmearWmass[0] = (metVSmear+Lep).M()
		self.METT1SmearWTmass[0] = (metVSmear+Lep).Mt()


		    metVP.SetPtEtaPhiM(entry.PuppiMET_pt,0, entry.PuppiMET_phi,0)
		    metVP.SetPz(0.)
		    metVP.SetE(metVP.Pt())
                    self.PuppiMETWmass[0] = (metVT1+Lep).M()
                    self.PuppiMETWTmass[0] = (metVT1+Lep).Mt()
		
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



                # in case of no corrections, the default MET is used
	        if  doUncertainties and isMC: 
		    self.MET_ptUnclusteredUp[0] =  (metV+metUn).Pt()
		    self.MET_ptUnclusteredDown[0] =  (metV-metUn).Pt()
		    self.MET_phiUnclusteredUp[0] =  (metV+metUn).Phi()
		    self.MET_phiUnclusteredDown[0] =  (metV-metUn).Phi()
	 


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
                                ss=syst
                                if 'jes' in syst : ss = 'JES'
                                if 'jer' in syst : ss = 'JER'
                                if 'uncl' in syst : ss = 'Unclustered'

				metpt = getattr(entry, "{0:s}_T1_pt{1:s}{2:s}".format(mfl, syst, dr), None)
				metphi = getattr(entry, "{0:s}_T1_phi{1:s}{2:s}".format(mfl, syst, dr), None)
                                getattr(self, '{}_T1_pt{}{}'.format(mfl,ss,dr ))[0] = metpt
                                getattr(self, '{}_T1_phi{}{}'.format(mfl,ss,dr ))[0] = metphi

                                #smear
				metpts = getattr(entry, "{0:s}_T1Smear_pt{1:s}{2:s}".format(mfl, syst, dr), None)
				metphis = getattr(entry, "{0:s}_T1Smear_phi{1:s}{2:s}".format(mfl, syst, dr), None)
                                getattr(self, '{}_T1Smear_pt{}{}'.format(mfl,ss,dr ))[0] = metpts
                                getattr(self, '{}_T1Smear_phi{}{}'.format(mfl,ss,dr ))[0] = metphis
		      
				pmet = correctedMET(metpt, metphi, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetg = correctedMET(metpt, metphi, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
				pmets = correctedMET(metpts, metphis, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetsg = correctedMET(metpts, metphis, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
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
                                getattr(self, '{}_pt{}{}'.format(mfl,syst,dr ))[0] = metpt
                                getattr(self, '{}_phi{}{}'.format(mfl,syst,dr ))[0] = metphi
                                #print '{}_pt{}{}'.format(mfl,syst,dr ), metpt

		      
				pmet = correctedMET(metpt, metphi, entry.PV_npvs, entry.run, isMC, str(era), True, True)
				pmetg = correctedMET(metpt, metphi, entry.PV_npvsGood, entry.run, isMC, str(era), True, True)
      
				#print "{0:s}_pt{1:s}{2:s}".format(mfl, syst, dr), "{0:s}_phi{1:s}{2:s}".format(mfl, syst, dr), metpt, metphi, entry.MET_T1_pt, entry.MET_T1_phi, entry.PuppiMET_pt, entry.PuppiMET_phi, pmet[2], pmet[3]
                                outvalues_pt_PMET.append(pmet[2])
                                outvalues_phi_PMET.append(pmet[3])
                                outvalues_pt_PGMET.append(pmetg[2])
                                outvalues_phi_PGMET.append(pmetg[3])




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
                if doUncertainties: 
		    main_branches = ['MET_T1', 'METCor_T1', 'METCorGood_T1', 'MET_T1Smear', 'METCor_T1Smear', 'METCorGood_T1Smear', 'PuppiMET', 'PuppiMETCor', 'PuppiMETCorGood']

		    systematics = ['', 'JES', 'JER', 'Unclustered']
		    if not isMC : systematics = ['']
		    variations = ['Up', 'Down']
		    if not isMC : variations = []

		    for branch in main_branches:
			for systematic in systematics:
			    if systematic ==  '' :

				pt_value = getattr(self, branch + '_pt')
				phi_value = getattr(self, branch + '_phi')
				metV.SetPtEtaPhiM(float(pt_value[0]), 0.0, float(phi_value[0]), 0.0)
				metV.SetPz(0.)
				metV.SetE(metV.Pt())

				u_par_value = self.getu_par_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                getattr(self, 'u_par_' + branch)[0] = u_par_value
				u_perp_value = self.getu_perp_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                getattr(self, 'u_perp_' + branch)[0] = u_perp_value

			    else : 
				for variation in variations:

					pt_value = getattr(self, branch + '_pt' + systematic + variation)
					phi_value = getattr(self, branch + '_phi' + systematic + variation)

					metV.SetPtEtaPhiM(float(pt_value[0]), 0.0, float(phi_value[0]), 0.0)
					metV.SetPz(0.)
					metV.SetE(metV.Pt())


					u_par_value = self.getu_par_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                        getattr(self, 'u_par_' + branch +  systematic + variation)[0] = u_par_value
					u_perp_value = self.getu_perp_MET(entry, metV.X(), metV.Y(), (LepP + LepM).X(), (LepP + LepM).Y(), (LepP + LepM).Pt())
                                        getattr(self, 'u_perp_' + branch +  systematic + variation)[0] = u_perp_value


					#print("Branch:", 'u_par_' + branch + systematic + variation, "Value:", u_par_value)
					#print("Branch:", 'u_perp_' + branch + systematic + variation, "Value:", u_perp_value)



            ###############################filling MET systematics

	    if 'UL' in proc or '2016' not in str(era):
                try : 
                    self.Flag_hfNoisyHitsFilter[0] = int(entry.Flag_hfNoisyHitsFilter)
            
		except AttributeError:  self.Flag_hfNoisyHitsFilter[0] = 1

                try : self.Flag_BadPFMuonDzFilter[0] = int(entry.Flag_BadPFMuonDzFilter)
		except AttributeError: self.Flag_BadPFMuonDzFilter[0] = 1


	    if  doUncertainties : 


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



