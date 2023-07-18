

class CutManager:
   'This class serves as an on-demand cut server'

   def __init__(self):

      #self.filters = "Flag_globalTightHalo2016Filter == 1"
      self.filters = "Flag_globalTightHalo2016Filter == 1"
      self.filters = "nMuon[0]>0"
      self.filters = " (nMuon[0]>-1 || nElectron[0]>-1) && (njets==0 || (njets>0 &&  !(abs(jeta)>2.65&&abs(jeta)<3.14) ))"
      self.filters = " (nMuon[0]>-1 || nElectron[0]>-1) "
      self.filters = " (njets[0]>-100) "
      #self.filters = "(Flag_globalTightHalo2016Filter ==1&& Flag_badMuonMoriond2017 == 1 && Flag_badCloneMuonMoriond2017==1 && Flag_badChargedHadronFilter ==1 && Flag_HBHENoiseIsoFilter==1 && Flag_HBHENoiseFilter ==1 &&   Flag_goodVertices ==1 && Flag_EcalDeadCellTriggerPrimitiveFilter ==1)"
      #self.trigMMc = "(HLT_mu17mu8_dz > 0 || HLT_mu27tkmu8 > 0 || HLT_mu17tkmu8_dz > 0)"
      self.trigMMc = "(all_ifTriggerpassed[0] > 0 || all_ifTriggerpassed[1] > 0)"
      self.twoLeptons = "nLepGood20 == 2"
      #self.twoLeptons = "nLeptons > 1"
      self.twoGoodLeptons = "((nLepGood20 ==2 ) && (abs(lep_eta[0]) < 2.4)  && (abs(lep_eta[1]) < 2.4) )"
      self.noLeptons = "nLepGood10 ==0"
      self.bla = "PFMetPt >= 0"
      self.leptonPt = "nLepGood20 ==2"
      #self.leptonPt = "((lep_pt[0] > 20.)) && ((lep_pt[1] > 20.)) "
      self.leptonDR = "t.lepsDR_Edge > 0.3"       
      self.leptonEta = "(abs(genLep_pdgId) == 11 ) && (abs(abs(genLep_eta) - 1.5) > 0.1 && abs(abs(genLep_eta) - 1.5) > 0.1)  || ((abs(genLep_pdgId) == 13 ) && (abs(genLep_eta < 2.1)))"
      self.leptonsMll = "t.lepsMll_Edge > 20"
      self.goodLepton =   self.leptonPt + "&&" + self.leptonDR + "&&" + self.leptonEta + "&&" + self.leptonsMll
      self.nj2 = "(t.nJetSel_Edge >= 2)"
      self.jet1_pt = "(jet1_pt >= 0)"
      self.jet2_pt = "(jet2_pt >= 0) && (jet1_pt>= 0)"
      self.InclusiveCR = "(t.nJetSel_Edge >= 1 && t.lepsMll_Edge > 60 && t.lepsMll_Edge < 120)"
      self.nj0 = "(t.nJetSel_Edge >= 0)"
      self.nj1 = "(nJet40 > 0)"
      self.puWeight = "puWeight"
      self.gamma =  "(gamma_pt > 50)" +  "&&(ngamma == 1)"+ "&&" +  "(gamma_r9 < 1.0)" + " && " + "(gamma_r9 > 0.9) " + " && "+ "gamma_hOverE < 0.0269" + " && " + "gamma_sigmaIetaIeta < 0.00994  " +  " && " +  "(gamma_chHadIso < (0.202))" + " && "  + "(gamma_neuHadIso < (0.264 + 0.0148 * gamma_pt + 0.000017*gamma_pt*gamma_pt))"  +  " && "  +  "(gamma_phIso < (2.362 + 0.0047 * gamma_pt))"
      #self.lep1ID =  "(lep_pt[0] > 20) && (abs(lep_eta[0]) < 2.4) "
      #self.lep1ID =  "(lep_pt[0] > 20) && (abs(lep_eta[0]) < 2.5)"
      #self.lep2ID =  "(lep_pt[1] > 20) && (abs(lep_eta[1]) < 2.5)"
      self.lep1ID =  "(lep_relIso04[0] < 0.25 ) && (lep_pt[0] > 20) && (abs(lep_eta[0]) < 2.5)"
      self.lep2ID =  "(lep_relIso04[1] < 0.25 ) && (lep_pt[1] > 20) && (abs(lep_eta[1]) < 2.5)"
      #self.muonID = "lep_pt[0]>20 "
      #self.muonID = "lep_mediumMuonId[0] ==1 && lep_mediumMuonId[1] == 1"
      #self.muonID = "lep_mediumMuonId[0] ==1 && lep_mediumMuonId[1] == 1  && lep_relIso04[0] < 0.25 && lep_relIso04[1] < 0.25  "
      self.gammaPhoton200 =  "(gamma_pt > 200)" +  " && "  +  "(ngamma == 1)"+ "&&" +  "(gamma_r9 < 1.0)" + " && " + "(gamma_r9 > 0.9) " + " && "+ "gamma_hOverE < 0.0269" + " && " + "gamma_sigmaIetaIeta < 0.00994  " +  " && " +  "(gamma_chHadIso < (0.202))" + " && "  + "(gamma_neuHadIso < (0.264 + 0.0148 * gamma_pt + 0.000017*gamma_pt*gamma_pt))"  +  " && "  +  "(gamma_phIso < (2.362 + 0.0047 * gamma_pt))"  
      self.gammaPhoton200Upara =  "(gamma_pt > 200)" +  " && "  +  "(ngamma == 1)"+ "&&" +  "(gamma_r9 < 1.0)" + " && " + "(gamma_r9 > 0.9) " + " && "+ "gamma_hOverE < 0.0269" + " && " + "gamma_sigmaIetaIeta < 0.00994  " +  " && " +  "(gamma_chHadIso < (0.202))" + " && "  + "(gamma_neuHadIso < (0.264 + 0.0148 * gamma_pt + 0.000017*gamma_pt*gamma_pt))"  +  " && "  +  "(gamma_phIso < (2.362 + 0.0047 * gamma_pt))" + "&&" + "(((( -PFMetPt*cos(met_phi) - gamma_pt*cos(gamma_phi))* gamma_pt*cos(gamma_pt )+(- PFMetPt*sin( met_phi )- gamma_pt*sin(gamma_phi ))*gamma_pt*sin( gamma_phi))/gamma_pt + gamma_pt) < (-180))" 
      #self.gamma =  "(gamma_pt > 50)" +  " && "  +  "(ngamma == 1)"+ "&&" +  "(gamma_r9 < 1.0)" + " && " + "(gamma_r9 > 0.9) " + " && "+ "gamma_hOverE < 0.05" + " && " + "gamma_sigmaIetaIeta < 0.01 "+ " && " + "gamma_sigmaIetaIeta > 0.005 " 
      self.noLeptons = "nLepGood10 ==0"
      #self.Zmasswindow = "zll_mass > 76 && zll_mass < 106"
      self.Zmasswindow = "zll_mass > 81 && zll_mass < 101"
      self.Zpt = "zll_pt > 50 "
      self.zcut = "zll_pt < 0.5 "
      self.centralPhoton = "(abs(gamma_eta)<1.4) "
      self.central = "(abs(t.Lep1_eta_Edge)<1.4 && abs(t.Lep2_eta_Edge)<1.4)"
      self.forward = "(abs(t.Lep1_eta_Edge)>1.4 || abs(t.Lep2_eta_Edge)>1.4)"
      self.trigger12090 = "HLT_Photon120>0 && HLT_Photon90>0"
      self.trigger120 = "(HLT_Photon120>0  && gamma_pt > 85 && gamma_pt < 120  )* (HLT_BIT_HLT_Photon120_R9Id90_HE10_IsoM_v_Prescale)"                     
      self.trigger9075 = "HLT_Photon90>0 && HLT_Photon75>0"
      self.trigger90 = "(HLT_Photon90>0  && gamma_pt > 75 && gamma_pt < 90 )* (HLT_BIT_HLT_Photon90_R9Id90_HE10_IsoM_v_Prescale)"                     
      self.trigger7550 = "HLT_Photon75>0 && HLT_Photon50>0"
      self.trigger75 = "(HLT_Photon75>0  && gamma_pt > 65 && gamma_pt < 80 )* (HLT_BIT_HLT_Photon75_R9Id90_HE10_IsoM_v_Prescale)"                     
      self.trigger5030 = "HLT_Photon50>0 && HLT_Photon30>0"
      self.trigger50 = "(HLT_Photon50>0 && gamma_pt > 35 && gamma_pt < 70)* (HLT_BIT_HLT_Photon50_R9Id90_HE10_IsoM_v_Prescale) "                     
      self.trigger30 = "(HLT_Photon30>0 && gamma_pt > 30 )* (HLT_BIT_HLT_Photon30_R9Id90_HE10_IsoM_v_Prescale)"                     
      self.triggerPhoton = "(HLT_Photon120 == 1 || HLT_Photon90==1 ||HLT_Photon75 == 1 || HLT_Photon50 ==1 || HLT_Photon30 ==1 )"
      self.triggerLepton = ""

   def brackets(self, cut):
      return '('+cut+')'

   def AddList(self, cutlist):
      returncut = ''
      for cut in cutlist:
          returncut += cut
          if not cutlist.index(cut) == len(cutlist)-1:
            returncut += ' && '
      return self.brackets(returncut)
  
   def Add(self, cut1, cut2):

      return self.brackets(cut1 + " && " + cut2 )
  
   def gammas(self):
                                                                                                                                                     
      return self.brackets(self.nj1 + " && " + self.centralPhoton  + " && " + self.gamma  +" && " + self.noLeptons  + "&&" + self.filters )
  
   def gammasPhoton200(self):
   
      return self.brackets(self.nj1 + " && " + self.centralPhoton + " && " + self.gammaPhoton200  +" && " + self.noLeptons  + "&&" + self.filters )
   
  
  
   def gammasData(self):

       return self.brackets(self.nj1 + " && " + self.centralPhoton + " && " + self.gamma + " && " + self.triggerPhoton  +" && " + self.noLeptons+ "&&" + self.filters )
   
   def leps(self):

          #return self.brackets( self.filters + "&& "  +self.Zmasswindow  + " && "+ self.twoGoodLeptons  + " && " + self.leptonPt + "&&" + self.lep1ID  + "&&" + self.lep2ID ) 
          return self.brackets( self.filters )

   def nocuts(self):
          return self.brackets( self.twoLeptons ) 











