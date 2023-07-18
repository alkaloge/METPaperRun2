import ROOT as r
from array import array
from ROOT import TTree, TFile, TCut, TH1F, TH2F, THStack, TCanvas, TEntryList
from math import sqrt, sin, cos, pi, tan, acos, atan2,log
from numpy import arange

class dupeDetector() :

    def __init__(self):
        self.nCalls = 0
        self.runEventList = []
        self.DuplicatedEvents = []

    #def checkEvent(self,entry,cat) :
    def checkEvent(self,entry) :
        self.nCalls += 1
        #runEvent = "{0:d}:{1:d}:{2:d}:{3:s}".format(entry.lumi,entry.run,entry.evt,cat)
        runEvent = "{0:d}:{1:d}:{2:d}".format(entry.lumi,entry.run,entry.evnt)
        if runEvent in self.runEventList :
            #print("Event in list: runEventList={0:s}".format(str(self.runEventList)))
            self.DuplicatedEvents.append(runEvent)
            #print 'duplicated event', entry.lumi,entry.run,entry.evt
            return True
        else :
            self.runEventList.append(runEvent)
            #print("New event: runEventList={0:s}".format(str(self.runEventList)))
            return False

        print 'print report', self.DuplicatedEvents

    def printSummary(self) :
        print("Duplicate Event Summary: Calls={0:d} Unique Events={1:d}".format(self.nCalls,len(self.runEventList)))
        return


class Sample:
   'Common base class for all Samples'

   def __init__(self, name, location, xsection, isdata, doee, dokfactorweight, iszjets, era, channel, isLocal=True, isWinclWNjets=False):
      self.name = name
      self.location = location
      self.xSection = xsection
      self.isData = isdata
      self.isee = doee
      self.dokfactorWeight = dokfactorweight
      self.isZjets = iszjets
      self.era = era
      self.channel = channel
      self.tfile = ''
      #root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/2Lep/WJetsToLNu_NLO_2016preVFP/WJetsToLNu_NLO_2016preVFP_MuMu.root",
      if isLocal:
	  if 'Run' not in name : 
	      if 'preVFP' in location and 'preVFP' not in str(era): self.tfile = TFile(self.location+'/{0:s}_{1:s}preVFP_{2:s}.root'.format( str(name), str(era), str(channel)))
	      else : self.tfile = TFile(self.location+'/{0:s}_{1:s}_{2:s}.root'.format( str(name), str(era), str(channel)))
	  else  : self.tfile = TFile(self.location+'/{0:s}_{1:s}.root'.format( str(name), str(era), str(channel)))
      else : 
          #/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2Lep/ST_s-channel_antitop_2016
          # root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/2Lep/WJetsToLNu_NLO_2016preVFP/WJetsToLNu_NLO_2016preVFP_MuMu.root
          #newlocation = self.location.split['2Lep']
          #self.location='root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/2Lep/'+self.location.split('2Lep')[1]
          self.location='root://cmseos.fnal.gov//store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/'+self.location.split('2Lep')[1]
          print 'check 1======================>', isLocal, self.location
	  if 'Run' not in name : 
	      if 'preVFP' in location and 'preVFP' not in str(era): self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}preVFP_{2:s}.root'.format( str(name), str(era), str(channel)))
	      else : self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}_{2:s}.root'.format( str(name), str(era), str(channel)))
	  else  : self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}.root'.format( str(name), str(era), str(channel)))

      #if not self.isData : self.tfileW = TFile(self.location+'/{0:s}_{1:s}.weights.root'.format( str(name), str(era)))
      #self.tfile = TFile(self.location+'/*.root'.format( str(name), str(era)))
      #self.tfileW = TFile(self.location+'/*weights'.format( str(name), str(era)))
      print 'will try to read from ', self.tfile.GetName(), name, era, channel
      self.ttree = self.tfile.Get('Events')
      print self.name
      self.puWeight  = "1.0"
      if not self.isData:
          htest = self.tfile.Get('hWeights')
          if isWinclWNjets :
              print 'you are binding Wjets Inclusive and WNjets exclusive samples....'
	      if 'WJetsToLNu' not in self.tfile.GetName() : htest = self.tfile.Get('hWeights')
	      else :  htest = self.tfile.Get('W0genWeights')

          if 'WJetsToLNu' in self.tfile.GetName() and 'NLO' in self.tfile.GetName(): htest = self.tfile.Get('hWeights')

          try:self.count = htest.GetSumOfWeights()
          except AttributeError: 
              self.count = 1.
              self.xSection = 0
      if self.xSection !=0 : print self.name, 'neentries', self.ttree.GetEntries()        
      #self.count = self.tfile.Get('demo/nEvents').GetSumOfWeights()
      else :
          #self.count = self.ttree.GetEntries()
          self.count = 1

      '''
      if not self.isData:
          gw = 0.
          for i in self.ttree:
              gw = abs(i.genWeight)
              if gw: break
          
          #self.count = self.tfile.Get('SumGenWeights').GetBinContent(1)/abs(gw)
          self.count = self.tfile.Get('demo/nEvents').GetSumOfWeights()
      else:
          self.count = self.tfile.Get('Count').GetBinContent(1)
      '''
      self.lumWeight =  1.0
      if not self.isData:
        #if 'WJets' in self.name and 'NLO' not in self.name: 
        #    print 'before changing', float(self.count), float(self.xSection) / float(self.count)
        #    #self.count = 6.5393807e+08
        #    #print '=========================================> changed for Wjets', self.name, self.count, float(self.xSection) / float(self.count)
     
        self.lumWeight = float(self.xSection) / float(self.count)
        print 'name ',self.name
        print 'xsec ',self.xSection
        print 'count ',self.count
        print 'lumweight ' ,self.lumWeight

   def printSample(self):
      print "#################################"
      print "Sample Name: ", self.name
      print "Sample Location: ", self.location
      print "Sample XSection: ", self.xSection
      print "Sample IsData: ", self.isData
      print "Sample LumWeight: ", self.lumWeight
      print "#################################"


   def getTH1FLoop(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, doNPV):
      print 'inside the correct one....'

      #hdupe = TH1F('hdupe', "", len(nbin)-1, array('d', nbin))
      if(xmin == xmax):
        h = TH1F(name, "", len(nbin)-1, array('d', nbin))
        ylabel = "# events"
      else:
        h = TH1F(name, "", nbin, xmin, xmax)
        bw = int((xmax-xmin)/nbin)
        ylabel = "Events / " + str(bw) + " GeV"
      h.Sumw2()
      h.GetXaxis().SetTitle(xlabel)
      h.GetYaxis().SetTitle(ylabel)

      addCut = "1."
      addPrescale = "1." 
              
          #cut = "("+ cut + addTriggers + addDataFilters+ ")" + "* (" + addPrescale +")" 
      print 'cross check, isdata', self.isData, lumi, name, var
      lumi *=1000
      if self.isData: cut =  cut    + ")"
      if not self.isData:
          #cut =  cut    + "* ( " + str(lumi)  +  " )"  + "* ( " + str(self.lumWeight)  +  " )" + "* ( " + "Generator_weight " +  " )"  + "* ( " + "weightPUtrue " +  " )"  + "* ( " + "L1PreFiringWeight_Nom " +  " )"
          cut =  cut    + "* ( " + str(lumi)  +  " )"  + "* ( " + str(self.lumWeight)  +  " )" + "* ( " + "weight " +  " )"  + "* fabs( " + "weightPUtrue " +  " )"  + "* ( " + "L1PreFiringWeight_Nom " +  " )" + "* ( " + "IDSF " +  " )"+ "* ( " + "TrigSF" +  " )"+ "* ( " + "IsoSF " +  " )"
          #cut =  cut  + "* ( " + "Generator_weight " +  " )"  + "* ( " + "weightPUtrue " +  " )"  + "* ( " + "L1PreFiringWeight_Nom " +  " )"
          #cut =  cut  + "* ( " + "weight " +  " )"  + "* ( " + "weightPUtrue " +  " )"

      #double dphi = fabs(fabs(fabs(MuonsPhi[0]-MET_phi)-TMath::Pi())-TMath::Pi());
      #transvMass = sqrt(2*MuonsPt[0]*MET_pt*(1-cos(dphi)));
      '''
          addCut = "1."
          if doNPV: 
              #addCut = "1"
              addCut = "puWeightNPV"
          else:
              addCut = "puWeightNTI"
          if self.dokfactorWeight:
              #cut =  cut  + "* ( " + str(self.lumWeight*lumi)  +  " )" + "* ( " + "genWeight/abs(genWeight) " +  " )" 
              cut =  cut  + "*( puWeightGJets )"+  "*( photonEff )"  +  "*( kfactorWeight )" + "* ( " + str(self.lumWeight*lumi)  +  " )" + "* ( " + "genWeight/abs(genWeight) " +  " )" 
          else:
              if self.isee:
              else:
      #print cut
      '''
      entryList = TEntryList("entryListName", "Title of the entry list")
      for i, e in enumerate(self.ttree) :
          if i % 250000 ==0: print i/1e6, 'from ', self.ttree.GetEntries()/1e6, float(i/float(self.ttree.GetEntries()))
          passEvt = e.nMuon==1 and e.nTau==0 and e.njets >=0  and e.pt_1> 27 and (e.isGlobal_1>0 or e.isTracker_1>0) and abs(e.eta_1)<2.4 and abs(e.dZ_1)<0.2 and abs(e.d0_1)<0.045 and e.isTrig_1>0 and  e.iso_1 < 0.15 and e.mediumId_1 >0 and e.nbtagT==0 
          if passEvt : entryList.Enter(self.ttree.GetReadEntry())
          else : continue

      self.ttree.SetEntryList(entryList)
      for i, e in enumerate(self.ttree) :
          if i % 100000 ==0: print i/1e6, 'from ', self.ttree.GetEntries()/1e6, float(i/float(self.ttree.GetEntries()))


          #if e.nMuon!=1 : continue
          #passEvt = e.nMuon==1 and e.nTau==0 and e.njets >=0  and e.pt_1> 27 and (e.isGlobal_1>0 or e.isTracker_1>0) and abs(e.eta_1)<2.4 and abs(e.dZ_1)<0.2 and abs(e.d0_1)<0.045 and e.isTrig_1>0 and  e.iso_1 < 0.15 and e.mediumId_1 >0 and e.nbtagT==0 
          weight = 1.
          #if 'WJets' in self.name and 'NLO' not in self.name and e.Generator_weight > 15 : continue
          if not self.isData : weight  = e.Generator_weight*e.weightPUtrue*e.L1PreFiringWeight_Nom
          h.Fill(var, weight)

          #print 'met------------->', vin, e.evt
          
      #self.ttree.Project(name, var, cut, options)

      if not self.isData :
          h.Scale(self.lumWeight*lumi)

      print '=====================some info======================....', h.GetName(), h.GetSumOfWeights(), h.GetTitle(), "cut", cut, "lumiWe*lumi", str(self.lumWeight*lumi), "lumi", lumi
      return h



   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, doNPV):
      print 'inside the correct one.... ignore the rest....'
      if(xmin == xmax):
        h = TH1F(name, "", len(nbin)-1, array('d', nbin))
        #h = TH1F(name, "", 10,0.,500.)
        ylabel = "# events"
      else:
        h = TH1F(name, "", nbin, xmin, xmax)
        #h = TH1F(name, "", 10,0.,500.)
        bw = int((xmax-xmin)/nbin)
        ylabel = "Events / " + str(bw) + " GeV"
      h.Sumw2()
      h.GetXaxis().SetTitle(xlabel)
      h.GetYaxis().SetTitle(ylabel)

      addCut = "1."
      addPrescale = "1." 
              
          #cut = "("+ cut + addTriggers + addDataFilters+ ")" + "* (" + addPrescale +")" 
      lumi *=1000.
      print 'cross check, isdata=================>', self.isData, lumi, name, var
      if self.isData: cut =  cut    + ")"
      if not self.isData :
          print 'not data, will also apply weights'


          #cut =  cut    + "* ( " + str(lumi)  +  " )"  + "* ( " + str(self.lumWeight)  +  " )" + "* ( " + "Generator_weight " +  " )"  + "* ( " + "weightPUtrue " +  " )"  + "* ( " + "L1PreFiringWeight_Nom " +  " )"
          #cut =  cut    + "&&    (abs(gen_match_1[0])==1 || abs(gen_match_1[0])==15) )" 
          if 'WJetsToLNu' in h.GetName() and 'NLO' not in h.GetName(): cut = cut +  " && LHE_Njets[0]<1 "
          cut =  cut    + ")" 
          cut =  cut    + "* ( " + "weight[0] " +  " )"  + "* fabs( " + "weightPUtrue[0] " +  " )"  + "* ( " + "L1PreFiringWeight_Nom[0] " +  " )"  + "* ( " + "IDSF " +  " )"+ "* ( " + "TrigSF" +  " )"+ "* ( " + "IsoSF " +  " )"
          if 'WJets' in h.GetName() and 'NLO' not in h.GetName() :
               cut = cut +  "&& ( " + "weight[0] " +  " ) < 10"
      #cut =  cut    + "&& Entry$ < 1000"
      if 'u_par' in var or 'u_perp' in var :
	  if 'parboson' not in var: var = "-1.*"+var
	  if 'u_parboson' in var : 
	      var = var.replace("parboson", "par")
              var  = var + "+ boson_pt"
          if 'parresp' in var : 
	      var = var.replace("parresp", "par")
	      var  = var + "*boson_pt"
          cut = cut +  "&& ( " + var +  " ) > -410" + "&& ( " + var +  " ) < 410 && boson_pt >=0"

      print 'some info....', name, "var", var, "cut", cut, "options", options
      evscale=1.
     
      #if self.ttree.GetEntries() > 100000 : 
      #    evscale = 100000/self.ttree.GetEntries()
      #    self.ttree.SetEntries(100000)
      try : self.ttree.Project(name, var, cut, options)
      except AttributeError : 
          h.Scale(0)
          print 'BIG PROBLEM================!!!!!!!!!!!!!!!!!!!!!!########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################', h.GetName()
      #try:self.ttree.Draw("{0:s}>>h".format(str(var)), cut, options)
      #except AttributeError : h.Scale(0)

      kf = 1.
      #if 'JetsToLNu' in h.GetName() and 'WJets' not in h.GetName() : kf = 1.221 # 1.166
      #if 'JetsToLNu' in h.GetName() and 'WJets' not in h.GetName() : kf *=1/0.60815635
      #if 'JetsToLNu' in h.GetName() and 'WJets' not in h.GetName() : kf = 1.166

      try : print 'some info=======!=!=!=============....', self.ttree.GetEntries(), h.GetName(), h.GetSumOfWeights(), h.GetTitle(), "cut", cut, "lumiWeight*lumi", str(self.lumWeight*lumi), "lumi", lumi, 'lumiW', self.lumWeight, 'kfactor', kf, var
      except AttributeError : print 'cannot give more info....'
      
      #if not self.isData : h.Scale(lumi*self.lumWeight)
      if not self.isData : h.Scale(float(lumi*kf*float(self.lumWeight))*evscale)
      return h

   def getTH2F(self, lumi, name, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel):
   
     #tmp_full= tree.getTH2F(lumi, var,  Variable, 20, 0,200, 20, 0, 200, cuts.Add(cut, jetCut) , "", varTitle)
     h = TH2F(name, "", nbinx, xmin, xmax, nbiny, ymin, ymax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     if(self.isData == 0):
        #cut = cut + "* ( " + str(self.lumWeight*lumi) + " * genWeight/abs(genWeight) * " + self.puWeight + " )" 
        cut = cut + "* ( " + str(self.lumWeight*lumi*1000) +  " ))" 
        #cut = cut + "* ("+1000*lumi+"*("+self.lumWeight+")))"
     else : cut = cut + ")"
     print lumi, name, 'var ', var, nbinx, xmin, xmax, nbiny, ymin, ymax, 'cut ', cut, options, xlabel, ylabel, '<---inside TH2'
     
     self.ttree.Project(name, var, cut, options) 
     return h

class Block:
   'Common base class for all Sample Blocks'

   def __init__(self, name, label, color, isdata):
      self.name  = name
      self.color = color
      self.isData = isdata
      self.label = label
      self.samples = []

   def printBlock(self):

      print "####################"
      print "Block Name: ", self.name
      print "Block Color: ", self.color
      print "Block IsData: ", self.isData
      print "####################"
      print "This block contains the following Samples"

      for l in self.samples:
        l.printSample()
     

   def addSample(self, s):
      self.samples.append(s)

   def getTH1FLoop(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, rereco):

     if(xmin == xmax):
       h = TH1F(name, "", len(nbin)-1, array('d', nbin))
       ylabel = "# events"
     else:
       h = TH1F(name, "", nbin, xmin, xmax)
       bw = int((xmax-xmin)/nbin)
       ylabel = "Events / " + str(bw) + " GeV"
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)

     for s in self.samples:
       AuxName = "auxT1_sample" + s.name
       haux = s.getTH1FLoop(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel, rereco)
       h.Add(haux)
       del haux


     h.SetLineColor(self.color)
     h.SetMarkerColor(self.color)
     h.SetTitle(self.label)

     return h




   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, rereco):

     if(xmin == xmax):
       h = TH1F(name, "", len(nbin)-1, array('d', nbin))
       ylabel = "# events"
     else:
       h = TH1F(name, "", nbin, xmin, xmax)
       bw = int((xmax-xmin)/nbin)
       ylabel = "Events / " + str(bw) + " GeV"
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)

     for s in self.samples:
       AuxName = "auxT1_sample" + s.name
       haux = s.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel, rereco)
       h.Add(haux)
       del haux


     h.SetLineColor(self.color)
     h.SetMarkerColor(self.color)
     h.SetTitle(self.label)

     return h

   def getTH2F(self, lumi, name, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel):
   
     h = TH2F(name, "", nbinx, xmin, xmax, nbiny, ymin, ymax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     for s in self.samples:
     
       AuxName = "auxT2_block" + s.name
       haux = s.getTH2F(lumi, AuxName, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel)
       h.Add(haux)
       del haux

     return h   

       

class Tree:
   'Common base class for a physics meaningful tree'

   def __init__(self, fileName, name, isdata, chann, islocal=True, isWjetsWNjets=False):
      self.name  = name
      self.isData = isdata
      self.blocks = []
      self.channel  = 'MuMu'
      self.isWjetsWNjets = isWjetsWNjets
      self.islocal = islocal
      self.parseFileName(fileName, chann, islocal, isWjetsWNjets)

   def parseFileName(self, fileName, chann, islocal, isWjetsWNjets):
      f = open(fileName)
    
      for l in f.readlines():

        if (l[0] == "#" or len(l) < 2):
          continue

        splitedLine = str.split(l)
        block       = splitedLine[0]
        theColor    = splitedLine[1]
        name        = splitedLine[2]
        label       = splitedLine[3]
        location    = splitedLine[4]
        xsection    = float(splitedLine[5])
        isdata =  int(splitedLine[6])
        doboson =  int(splitedLine[7])
        dokfactor =  int(splitedLine[8])
        iszjets =  int(splitedLine[9])
        year =  int(splitedLine[10])
        
        
         
        color = 0
        plusposition = theColor.find("+")
        if(plusposition == -1):
          color = eval(theColor)
        else:
          color = eval(theColor[0:plusposition])
          color = color + int(theColor[plusposition+1:len(theColor)])

        sample = Sample(name, location,  xsection, isdata, doboson, dokfactor, iszjets, year, chann, islocal, isWjetsWNjets)
        coincidentBlock = [l for l in self.blocks if l.name == block]

        if(coincidentBlock == []):

          newBlock = Block(block, label, color, isdata)
          newBlock.addSample(sample)
          self.addBlock(newBlock)

        else:

          coincidentBlock[0].addSample(sample)




   def printTree(self):

      print "######"
      print "Tree Name: ", self.name
      print "Tree IsData: ", self.isData
      print "######"
      print "This Tree contains the following Blocks"

      for l in self.blocks:
        l.printBlock()
     

   def addBlock(self, b):
      self.blocks.append(b)



   def getYields(self, lumi, var, xmin, xmax, cut):
  
      h = self.getTH1F(lumi, "yields", var, 1, xmin, xmax, cut, "", "", rereco)
      nbinmin = h.FindBin(xmin)
      nbinmax = h.FindBin(xmax)
      error = r.Double()
      value = h.IntegralAndError(nbinmin, nbinmax, error)
      y = [value, error]
      
      del h
      return y

   def getStack(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel):
   
     hs = THStack(name, "")
     for b in self.blocks:
     
       AuxName = "auxStack_block_" + name + "_" + b.name
       haux = b.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel, rereco)
       haux.SetFillColor(b.color)
       hs.Add(haux)
       del haux


     can_aux = TCanvas("can_aux")
     can_aux.cd()
     hs.Draw()
     del can_aux

     hs.GetXaxis().SetTitle(xlabel)
     b = int((xmax-xmin)/nbin)
     ylabel = "Events / " + str(b) + " GeV"
     hs.GetYaxis().SetTitle(ylabel)

     return hs   


   def getTH1FLoop(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, rereco):
     
     if(xmin == xmax):
       _nbins = len(nbin)-1
       _arr = array('d', nbin)
       h = TH1F(name, "", _nbins, _arr)
       if len(nbin) > 50 :  # this option is for when you want underflow bins, make sure to modify the nbins if you want underflow bins for a plot with fewer bins 
           _newarr = array('d', [ 2*_arr[0]-_arr[1] ]) +_arr +  array('d', [ 2*_arr[-1]-_arr[-2] ]) 
           h_of = TH1F(name+'_of', "", _nbins+2, _newarr)
       else:
           _newarr = _arr + array('d', [ 2*_arr[-1]-_arr[-2] ]) 
           h_of = TH1F(name+'_of', "", _nbins+1, _newarr)
       ylabel = "# events"
     else:
         h = TH1F(name, "", nbin, xmin, xmax)
         bw = int((xmax-xmin)/nbin)
         ylabel = "Events / " + str(bw) + " GeV"
         h_of = TH1F(name+'_of', '', nbin+1, xmin, xmax+bw)
     print 'some info', h.GetName(), h.GetSumOfWeights()
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     for b in self.blocks:
       AuxName = "auxh1_block_" + name + "_" + b.name
       haux = b.getTH1FLoop(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel, rereco)
       h.Add(haux)
       del haux

     if options == 'noOF':
         for _bin in range(0, h_of.GetNbinsX()):
            h_of.SetBinContent(_bin, h.GetBinContent(_bin))
            h_of.SetBinError(_bin, h.GetBinError(_bin))        
     else:
         if ((xmin == xmax) and len(nbin) > 50):    
             for _bin in range(0, h_of.GetNbinsX()+1):
                 h_of.SetBinContent(_bin+1, h.GetBinContent(_bin))
                 h_of.SetBinError  (_bin+1, h.GetBinError  (_bin)) 
         else:
             for _bin in range(1, h_of.GetNbinsX()+1):
                 h_of.SetBinContent(_bin, h.GetBinContent(_bin))
                 h_of.SetBinError(_bin, h.GetBinError(_bin))        


     return h_of
     del h_of
     del h


   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, rereco, islog):
     #options='onebin'
     if 'njets' in var or 'nTau' in var or 'nMuon' in var: nbin=range(0,10,1)
     if 'mll' in var : 
         nbin=arange(60,120,2.5)
     if 'MET_T1_pt' in var or 'PuppiMET_pt' in var or 'MET_pt' in var or 'METCor' in var: 
         #if islog < 1 : nbin = range(0,140,10)
         #else : nbin = range(0,400,25)
         nbin = range(0,200,25)
         if '10bin' in options : nbin = range(0,210,10)
         if 'onebin' in options  : nbin=range(0,200,1)

     if 'WTmass' in var or 'Wmass' in var : 
         islog  = False 
         nbin = range(40,200,10)
  
     if 'eta' in var : 
         nbin = arange(-2.4,2.4,0.1)
     if 'phi' in var : 
         nbin = arange(-3.1,3.1,0.2)
         #if 'onebin' in options  : nbin=range(-3,3,1)

     if 'tight' in var or 'high' in var or 'is' in var: nbin = range(-1,2)
     if 'PV' in var : 
         nbin = arange(0,100,0.5)
     if 'iso' in var : 
         nbin=arange(0,1,0.05)
     if 'ip3d' in var : 
         nbin=arange(0,0.1,0.005)
     if 'sip3d' in var : 
         nbin=arange(0,10,0.005)
     if 'u_perp' in var and '/' not in var: 
         nbin=arange(-400,400,5)
     if 'u_par' in var and '/' not in var: 
         nbin=arange(-400,400,5)
     if ('u_perp' in var or 'u_par' in var ) and '/' in var: 
         nbin=arange(-2,2,0.05)
     if ('parresp' in var ) and '/' in var: 
         nbin=arange(-3,3,0.05)
     if 'boson_pt' in var : 
         nbin = range(0,140,10)
  

     #if 'phi' in var : nbin=[ 0.,0.1,  0.2,0.3,  0.4,0.5,  0.6,0.7,  0.8,0.9,  1.,1.1,  1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,1.9,  2., 2.1, 2.2,2.3,  2.4,2.5,  2.6, 2.7, 2.8,2.9,  3.]
     #if 'phi' in var : nbin= [ -3., -2.9,-2.8, -2.7, -2.6,-2.5,  -2.4,-2.3, -2.2,-2.1, -2,-1.9, -1.8,-1.7, -1.6,-1.5, -1.4,-1.3, -1.2,-1.1, -1.,-0.9, -0.8,-0.7, -0.6, -0.5,-0.4,-0.3, -0.2,-0.1, 0.,0.1,  0.2,0.3,  0.4,0.5,  0.6,0.7,  0.8,0.9 ,  1.,1.1,  1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,1.9,  2., 2.1, 2.2, 2.3,  2.4,2.5,  2.6, 2.7, 2.8,2.9,  3.]

     if(xmin == xmax):
       _nbins = len(nbin)-1
       _arr = array('d', nbin)
       h = TH1F(name, "", _nbins, _arr)
       if len(nbin) > 50 :  # this option is for when you want underflow bins, make sure to modify the nbins if you want underflow bins for a plot with fewer bins 
           _newarr = array('d', [ 2*_arr[0]-_arr[1] ]) +_arr +  array('d', [ 2*_arr[-1]-_arr[-2] ]) 
           h_of = TH1F(name+'_of', "", _nbins+2, _newarr)
       else:
           _newarr = _arr + array('d', [ 2*_arr[-1]-_arr[-2] ]) 
           h_of = TH1F(name+'_of', "", _nbins+1, _newarr)
       ylabel = "# events"
     else:
	 h = TH1F(name, "", nbin, xmin, xmax)
	 bw = int((xmax-xmin)/nbin)
	 ylabel = "Events / " + str(bw) + " GeV"
         h_of = None
	 h_of = TH1F(name+'_of', '', nbin+1, xmin, xmax+bw)
	 h_of = TH1F(name+'_of', '', nbin, xmin, xmax)
	 #if 'u_par' not in var and 'u_perp' not in var : h_of = TH1F(name+'_of', '', nbin+1, xmin, xmax+bw)
	 if 'u_par' in var or 'u_perp' in var : h_of = TH1F(name+'_of', '', nbin+2, xmin-bw, xmax+bw)
	 h_of = TH1F(name+'_of', '', nbin+2, xmin-bw, xmax+bw)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     for b in self.blocks:
       AuxName = "auxh1_block_" + name + "_" + b.name
       #cut =  cut    + "&& Entry$ < 100000"
       print 'some infooooo....', name, "var", var, "cut", cut, "options", options, 'blocks', self.blocks, b
       haux = b.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel, rereco)
       h.Add(haux)
       del haux
     '''
     if options == 'noOF':
         for _bin in range(0, h_of.GetNbinsX()):
            h_of.SetBinContent(_bin, h.GetBinContent(_bin))
            h_of.SetBinError(_bin, h.GetBinError(_bin))        
     else:
         if ((xmin == xmax) and len(nbin) > 50):    
             for _bin in range(0, h_of.GetNbinsX()+1):
                 h_of.SetBinContent(_bin+1, h.GetBinContent(_bin))
                 h_of.SetBinError  (_bin+1, h.GetBinError  (_bin)) 
         else:
             #if 'u_par' not in var and 'u_perp' not in var and 'parresp' not in var:
             if 'u_par' not in var and 'u_perp' not in var :
		 for _bin in range(1, h_of.GetNbinsX()+1):
		     h_of.SetBinContent(_bin, h.GetBinContent(_bin))
		     h_of.SetBinError(_bin, h.GetBinError(_bin))        
             else :
                 for _bin in range(0, h_of.GetNbinsX()+1):
		     h_of.SetBinContent(_bin+1, h.GetBinContent(_bin))
		     h_of.SetBinError(_bin+1, h.GetBinError(_bin))        
     '''
     h_of = h.Clone()
     underflowContent = h_of.GetBinContent(0)
     bin1Content = h_of.GetBinContent(1)
     bin1Error = sqrt(h_of.GetBinError(0)**2 + h_of.GetBinError(1)**2)
     if 'u_p' in var or 'phi' in var: 
	 h_of.SetBinContent(1, underflowContent + bin1Content)
	 h_of.SetBinError(1, bin1Error)
	 h_of.SetBinError(0, 0.)
	 h_of.SetBinContent(0, 0.)

     # Move the overflow bin content to the last bin and recalculate the error
     lastBinIndex = h_of.GetNbinsX() + 1
     overflowContent = h_of.GetBinContent(lastBinIndex )
     overflowError = sqrt(h_of.GetBinError(lastBinIndex - 1)**2 + h_of.GetBinError(lastBinIndex)**2)
     h_of.SetBinContent(lastBinIndex - 1, overflowContent + h_of.GetBinContent(lastBinIndex-1))
     h_of.SetBinError(lastBinIndex - 1, overflowError)
     h_of.SetBinError(lastBinIndex , 0.)
     h_of.SetBinContent(lastBinIndex , 0.)




     return h_of
     del h_of
     del h

   def getTH2F(self, lumi, name, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel):
   
     h = TH2F(name, "", nbinx, xmin, xmax, nbiny, ymin, ymax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     for b in self.blocks:
     
       AuxName = "aux_block" + name + "_" + b.name
       haux = b.getTH2F(lumi, AuxName, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel)
       h.Add(haux)
       del haux

     return h   

