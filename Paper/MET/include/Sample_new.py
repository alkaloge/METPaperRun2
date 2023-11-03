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

   def __init__(self, name, location, xsection, isdata, doee, dokfactorweight, iszjets, era, channel, isLocal=True, isWinclWNjets=False, IWDP='mvaID'):
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
      tfileloc = ''
      #root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/WJetsToLNu_NLO_2016preVFP/WJetsToLNu_NLO_2016preVFP_MuMu.root",
      #if isLocal:
      #if not isLocal:
      #    loc = self.location.replace('/eos/uscms/store/group/','root://cmseos.fnal.gov//store/user/')
      #    self.location=loc
      loc = self.location.replace('group','user')
      self.location = loc
      '''
      if 'Run' not in name : 
	  if 'preVFP' in location and 'preVFP' not in str(era): tfileloc= self.location+'/{0:s}_{1:s}preVFP_{2:s}.root'.format( str(name), str(era), str(channel))
	  else : tfileloc=self.location+'/{0:s}_{1:s}_{2:s}.root'.format( str(name), str(era), str(channel))
      else : tfileloc = self.location+'/{0:s}_{1:s}.root'.format( str(name), str(era), str(channel))
      if isLocal  : self.tfile = TFile(tfileloc)

      else  :
          print 'this is not local, will try to read from-->', 'root://cmseos.fnal.gov//', '+ tfileloc', tfileloc 
          self.tfile = TFile.Open("root://cmseos.fnal.gov//"+tfileloc, "READ")
      '''

      chain_events = r.TChain("Events")
      chain_weights = r.TChain("hWeights")
      if 'Run' not in name:
          if 'preVFP' in location and 'preVFP' not in str(era):
	      file_pattern = '{0:s}_{1:s}preVFP_{2:s}'.format(str(name), str(era), str(channel))
	  else:
	      file_pattern = '{0:s}_{1:s}_{2:s}/'.format(str(name), str(era), str(channel))
      else:
          file_pattern = '{0:s}_{1:s}/'.format(str(name), str(era), str(channel))

      # Specify the patterns for the files you want to read
      file_patterns = [file_pattern + "*Muons.root", file_pattern + "*weights"]  # Adjust these patterns as needed
      file_patterns = ["*Muons.root",  "*weights"]  # Adjust these patterns as needed

      print "file_patterns", file_patterns
      # Add all matching files to the TChain
      if isLocal:
          for pattern in file_patterns:
   	      files = r.TFile.GetListOfFiles(location, pattern)
	      for file in files:
                  if 'weights' not in pattern : 
		      chain_events.Add(file.GetTitle())
		      print("Added file:", filename)
                  else:
		      chain_weights.Add(file.GetTitle())
		      print("Added weights file:", filename)
      else:
          for pattern in file_patterns:
    	      file_location = "root://cmseos.fnal.gov//" + location + pattern
              if 'weights' not in pattern : 
	          chain_events.Add(file_location)
	      else:
		  chain_weights.Add(file_location)

      # Now, you can use 'chain_events' to read from all matched files
      nEntries = chain_events.GetEntries()
      self.ttree = chain_events  # Assign the TChain to self.ttree
      hWeights = None
      for entry in range(nEntries):
  	  chain_weights.GetEntry(entry)

	  # Access the hWeights histogram from the current file
	  hWeightCurrent = chain_weights.GetFile().Get("hWeights")

	  # Accumulate histograms
	  if hWeights is None:
	      hWeights = hWeightCurrent.Clone()
	  else:
	      hWeights.Add(hWeightCurrent)

      htest = hWeights

      try:self.count = htest.GetSumOfWeights()
      except AttributeError:
          self.count = 1.
          self.xSection = 0
      if self.xSection !=0 : print self.name, 'neentries', self.ttree.GetEntries()
      #self.count = self.tfile.Get('demo/nEvents').GetSumOfWeights()
      else :
          #self.count = self.ttree.GetEntries()
          self.count = 1



      #print 'will try to read from ', self.location, self.tfile.GetName(), name, era, channel
      print 'will try to read from', file_location, 'nEvents', nEntries, self.count
      '''    
      #else : 
          #/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/ST_s-channel_antitop_2016
          # root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/WJetsToLNu_NLO_2016preVFP/WJetsToLNu_NLO_2016preVFP_MuMu.root
          #newlocation = self.location.split['Wjets_T1']
          #self.location='root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/'+self.location.split('Wjets_T1')[1]
          if 'Gjets' in channel : 
              
              self.location='root://cmseos.fnal.gov//store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets_out/'+self.location.split('Gjets_out')[1]
              if  IWDP=='mvaID' : self.location='root://cmseos.fnal.gov//store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets_out_mvaID/'+self.location.split('Gjets_out_mvaID')[1]
              if  IWDP=='cutBased' : self.location='root://cmseos.fnal.gov//store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets_out_cutBased/'+self.location.split('Gjets_out_cutBased')[1]
              #self.location  = loc.replace('Gjets_out', 'Gjet_out_'+TheSelection)
              print 'This is for Gjets', self.location
          if 'MuMu' in channel or 'ElEl' in channel: 
              self.location='root://cmseos.fnal.gov//store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/'+self.location.split('2Lep')[1]
          print 'check 1======================>', isLocal, self.location
	  if 'Run' not in name : 
	      if 'preVFP' in location and 'preVFP' not in str(era): self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}preVFP_{2:s}.root'.format( str(name), str(era), str(channel)))
	      else : self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}_{2:s}.root'.format( str(name), str(era), str(channel)))
	  else  : self.tfile = TFile.Open(self.location+'/{0:s}_{1:s}.root'.format( str(name), str(era), str(channel)))
      '''
      #if not self.isData : self.tfileW = TFile(self.location+'/{0:s}_{1:s}.weights.root'.format( str(name), str(era)))
      #self.tfile = TFile(self.location+'/*.root'.format( str(name), str(era)))
      #self.tfileW = TFile(self.location+'/*weights'.format( str(name), str(era)))
      #self.ttree = self.tfile.Get('Events')

      print self.name
      self.puWeight  = "1.0"
      '''
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



   # this is the correct one!!!
   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, channel):
      print 'inside the correct one....', name, var, options
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
      print 'cross check, isdata=================>', self.isData, lumi, name, var,channel, options
      if self.isData: cut =  cut    + ")"
      if not self.isData :
          print 'not data, will also apply weights'

          #cut =  cut    + "* ( " + str(lumi)  +  " )"  + "* ( " + str(self.lumWeight)  +  " )" + "* ( " + "Generator_weight " +  " )"  + "* ( " + "weightPUtrue " +  " )"  + "* ( " + "L1PreFiringWeight_Nom " +  " )"
          #cut =  cut    + "&&    (abs(gen_match_1[0])==1 || abs(gen_match_1[0])==15) )" 
          cut =  cut    + ")" 
          #cut =  cut    + "* ( " + "weight[0] " +  " )"  + "* ( " + "L1PreFiringWeight_Nom[0] " +  " )"  + "* ( " + "IDSF " +  " )"+ "* ( " + "TrigSF" +  " )"+ "* ( " + "IsoSF " +  " )"
          cut =  cut    + "* ( " + "weight[0] " +  " )"  + "* ( " + "L1PreFiringWeight_Nom[0] " +  " )"  
          if 'puup'not in var.lower() and 'pudown' not in var.lower() : 
              cut =  cut    + "* fabs( " + "weightPUtruejson[0] " +  " )"  
              #cut =  cut    + "* fabs( " + "weightPUtrue[0] " +  " )"  
          if 'puup' in var.lower(): 
              cut =  cut    + "* fabs( " + "weightPUtruejson_up[0] " +  " )"  
              var = var.replace('PUUp', '')
              var = var.replace('PUup', '')
          if 'pudown' in var.lower(): 
              cut =  cut    + "* fabs( " + "weightPUtruejson_down[0] " +  " )"  
              var = var.replace('PUDown', '')
              var = var.replace('PUdown', '')


          if 'ElNu' in channel or 'MuNu' in channel: 
              #print 'there you are', channel
              if 'WJetsToLNu' in h.GetName() and 'NLO' not in h.GetName(): cut = cut +  " && LHE_Njets[0]<1 "

              if 'MuNu' in channel : cut =  cut    + "* ( " + "TrigSF1[0] " +  " )"  
	      if 'isoup' not in var.lower() and 'isodown' not in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1[0] " +  " )"  
	      if 'isoup' in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1_up[0] " +  " )"  
		  var = var.replace('ISoUp', '')
		  var = var.replace('ISoup', '')
	      if 'isodown' in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1_down[0] " +  " )"   
		  var = var.replace('ISoDown', '')
		  var = var.replace('ISodown', '')

	      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1[0] " +  " )"  
	      if 'idup' in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1_up[0] " +  " )"  
		  var = var.replace('IDUp', '')
		  var = var.replace('IDup', '')
	      if 'iddown' in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1_down[0] " +  " )"   
		  var = var.replace('IDDown', '')
		  var = var.replace('IDdown', '')


          if 'ElEl' in channel or 'MuMu' in channel: 
              #print 'there you are', channel
              if 'MuMu' in channel : cut =  cut    + "* ( " + "TrigSF1[0] " +  " )"  + "* ( " + "TrigSF2[0] " +  " )"
	      if 'isoup' not in var.lower() and 'isodown' not in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1[0] " +  " )"  + "* ( " + "IsoSF2[0] " +  " )"
	      if 'isoup' in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1_up[0] " +  " )"  + "* ( " + "IsoSF2_up[0] " +  " )"
		  var = var.replace('ISoUp', '')
		  var = var.replace('ISoup', '')
	      if 'isodown' in var.lower() :
		  cut =  cut    + "* ( " + "IsoSF1_down[0] " +  " )"   + "* ( " + "IsoSF2_down[0] " +  " )"
		  var = var.replace('ISoDown', '')
		  var = var.replace('ISodown', '')

	      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1[0] " +  " )"  + "* ( " + "IDSF2[0] " +  " )"
	      if 'idup' in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1_up[0] " +  " )"  + "* ( " + "IDSF2_up[0] " +  " )"
		  var = var.replace('IDUp', '')
		  var = var.replace('IDup', '')
	      if 'iddown' in var.lower() :
		  cut =  cut    + "* ( " + "IDSF1_down[0] " +  " )"   + "* ( " + "IDSF2_down[0] " +  " )"
		  var = var.replace('IDDown', '')
		  var = var.replace('IDdown', '')





          if 'Gjets' in channel : 
              if 'Gjets' not in channel : cut =  cut    + "* ( " + "TrigSF1[0] " +  " )"  
              if 'Gjets'  in channel : 
                  if 'cutbasedtight' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFT[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFT_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDp', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFT_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

                  if 'cutbasedmedium' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFM[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFM_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDup', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFM_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

                  if 'mvaid80' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDup', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

                  if 'mvaid90' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDup', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

                  if 'mvaidwp80' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDup', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP80_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

                  if 'mvaidwp90' in options :
		      if 'idup' not in var.lower() and 'iddown' not in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90[0] " +  " )"  
		      if 'idup' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90_up[0] " +  " )"  
			  var = var.replace('IDUp', '')
			  var = var.replace('IDup', '')
		      if 'iddown' in var.lower() :
			  cut =  cut    + "* ( " + "IDSFWP90_down[0] " +  " )"  
			  var = var.replace('IDDown', '')
			  var = var.replace('IDdown', '')

              if 'Gjets' not  in channel : 
		  if 'idup' not in var.lower() and 'iddown' not in var.lower() :
		      cut =  cut    + "* ( " + "IDSF[0] " +  " )"  
		  if 'idup' in var.lower() :
		      cut =  cut    + "* ( " + "IDSF_up[0] " +  " )"  
		      var = var.replace('IDUp', '')
		      var = var.replace('IDup', '')
		  if 'iddown' in var.lower() :
		      cut =  cut    + "* ( " + "IDSF_down[0] " +  " )"  
		      var = var.replace('IDDown', '')
		      var = var.replace('IDdown', '')
          
          if 'WJets' in h.GetName() and 'NLO' not in h.GetName() :
               cut = cut +  "&& ( " + "weight[0] " +  " ) < 10"
      #if not self.isData :
      #    if 'QCD' in name : cut = cut +  "* ( " + "Photon_genPartFlav_1[0] !=1" +  " ) "

      if self.isData :
          if 'Photon' in name or 'Photon' in cut : cut = cut +  "* ( " + "weightpsjson[0] " +  " ) "
          #cut = cut +  "* min( " + "weightpsjson[0] " + "," + "weightps2[0]" +  " ) "

      if 'u_par' in var or 'u_perp' in var :
	  if 'parboson' not in var: var = "-1.*"+var
	  if 'u_perp'  in var: var = var + "/boson_pt"
	  if 'u_parboson' in var : 
	      var = var.replace("parboson", "par")
              var  = var + "+ boson_pt"
          if 'resp' in var : 
	      var = var.replace("resp", "")
	      var  = "("+var + ")/boson_pt"



          #cut = cut +  "&& ( " + var +  " ) > -410" + "&& ( " + var +  " ) < 410 && boson_pt >=0"
          #cut = cut +  "&& boson_pt >=0"
          #cut = cut +  "&& boson_pt >=0"
         
      print '============================>>>>>>>>>>', h.GetName(), cut, 'puweigh = ', options
      #cut =  cut    + "&& Entry$ < 1000"
      print 'some info....', name, "var", var, "cut", cut, "options", options
      evscale=1.
     
      
      try : self.ttree.Project(name, var, cut, options)
      except AttributeError : 
          h.Scale(0)
          print 'BIG PROBLEM================!!!!!!!!!!!!!!!!!!!!!!########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################', h.GetName()
      #try:self.ttree.Draw("{0:s}>>h".format(str(var)), cut, options)
      #except AttributeError : h.Scale(0)


      try : print 'some info======================....', self.ttree.GetEntries(), h.GetName(), h.GetSumOfWeights(), h.GetTitle(), "cut", cut, "lumiWeight*lumi", str(self.lumWeight*lumi), "lumi", lumi, 'lumiW', self.lumWeight
      except AttributeError : print 'cannot give more info....'
      
      #if not self.isData : h.Scale(lumi*self.lumWeight)
      if not self.isData : h.Scale(float(lumi*float(self.lumWeight))*evscale)
      return h

   def getTH2F(self, lumi, name, var, nbinx, xmin, xmax, nbiny, ymin, ymax, cut, options, xlabel, ylabel):
   
     h = TH2F(name, "", nbinx, xmin, xmax, nbiny, ymin, ymax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     h.GetYaxis().SetTitle(ylabel)
     
     if(self.isData == 0):
        cut = cut + "* ( " + str(self.lumWeight*lumi) + " * genWeight/abs(genWeight) * " + self.puWeight + " )" 
     
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

   def __init__(self, fileName, name, isdata, chann, islocal=True, isWjetsWNjets=False,  IWDP='mvaID'):
      self.name  = name
      self.isData = isdata
      self.blocks = []
      self.channel  = 'MuMu'
      self.isWjetsWNjets = isWjetsWNjets
      self.IWDP=  IWDP
      self.islocal = islocal
      self.parseFileName(fileName, chann, islocal, isWjetsWNjets, IWDP)

   def parseFileName(self, fileName, chann, islocal, isWjetsWNjets, IWDP):
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

        sample = Sample(name, location,  xsection, isdata, doboson, dokfactor, iszjets, year, chann, islocal, isWjetsWNjets, IWDP)
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


   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, rereco,  islog):
     #options='onebin'
     print 'options--------------------------->', options
     if 'njets' in var or 'nTau' in var or 'nMuon' in var: nbin=range(0,10,1)
     if 'mll' in var : 
         nbin=arange(60,120,2)
     if '_pt' in var : 
         if 'Photon' not in cut :
	     #if islog < 1 : nbin = range(0,140,10)
	     #else : nbin = range(0,400,25)
	     nbin = range(0,225,25)
	     if '10bin' in options : nbin = range(0,210,10)
	     if 'varbin' in options : nbin = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200]
	     if 'onebin' in options  : nbin=range(0,200,1)
         else :
	     if 'boson_pt' not in var : 
		 nbin = range(0,225,25)
		 if '10bin' in options : nbin = range(0,210,10)
		 if 'varbin' in options : nbin = [10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200]
		 if 'onebin' in options  : nbin=range(0,200,1)
	     if 'boson_pt' in var : 
		 nbin = range(50,225,25)
		 if '10bin' in options : nbin = range(50,210,10)
		 if 'varbin' in options : nbin = [50, 60, 70, 80, 90, 100, 120, 150, 200]
		 if 'onebin' in options  : nbin=range(50,200,1)

     if 'Photon_r9' in var : 
         nbin = arange(0.8, 1.05, 0.01)
     if 'Photon_hoe' in var : 
         nbin = arange(0.0, 0.2, 0.005)
     if 'jetIdx' in var : 
         nbin = arange(-1, 23,1)

     if 'iso' in var : 
         nbin = arange( 0., 0.10, 0.005)

     if 'sieie' in var : 
         nbin = arange( 0., 0.016, 0.002)

     if 'WTmass' in var or 'Wmass' in var : 
         islog  = False 
         nbin = range(40,200,10)
  
     if 'eta' in var : 
         nbin = arange(-2.4,2.4,0.1)
     if 'phi' in var or 'dPhi' in var: 
         nbin = arange(-3.14,3.14+0.314,0.314)
         #if 'onebin' in options  : nbin=range(-3,3,1)
     if 'dR' in var or 'dr' in var: 
         nbin = arange(0,4.2,.2)
         #if 'onebin' in options  : nbin=range(-3,3,1)

     if 'tight' in var or 'high' in var or 'is' in var and 'iso' not in var: nbin = range(-1,2)
     if 'PV' in var : 
         nbin = arange(0,100,0.5)
     if 'ip3d' in var : 
         nbin=arange(0,0.1,0.005)
     if 'sip3d' in var : 
         nbin=arange(0,10,0.005)
     if 'u_perp' in var and '/' not in var: 
         nbin=arange(-200,210,10)
     if 'u_par' in var and '/' not in var: 
         nbin=arange(-200,210,10)
     if ('u_perp' in var or 'u_par' in var ) and '/' in var: 
         nbin=arange(-2,2,0.05)
     if ('parresp' in var ) and '/' in var: 
         nbin=arange(-3,3,0.05)
     if ('perpresp' in var ) and '/' in var: 
         nbin=arange(-3,3,0.05)
     #if 'boson_pt' in var : 
     #    if 'Photon' not in cut : nbin = range(0,140,10)
     #    else : nbin = range(50,140,10)
  

     #if 'phi' in var : nbin=[ 0.,0.1,  0.2,0.3,  0.4,0.5,  0.6,0.7,  0.8,0.9,  1.,1.1,  1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,1.9,  2., 2.1, 2.2,2.3,  2.4,2.5,  2.6, 2.7, 2.8,2.9,  3.]

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
	 bw = int((xmax-xmin)/nbin)
	 #h = TH1F(name, "", nbin+2, xmin-bw, xmax+bw)
	 h = TH1F(name, "", nbin, xmin, xmax)
	 ylabel = "Events / " + str(bw) + " GeV"
         h_of = None
	 #h_of = TH1F(name+'_of', '', nbin+1, xmin, xmax+bw)
	 h_of = TH1F(name+'_of', '', nbin, xmin, xmax)
         #h_of = TH1F(name+'_of', '', nbin+2, xmin-bw, xmax+bw)
	 #if 'u_par' not in var and 'u_perp' not in var : h_of = TH1F(name+'_of', '', nbin+1, xmin, xmax+bw)
	 #if 'u_par' in var or 'u_perp' in var : h_of = TH1F(name+'_of', '', nbin+2, xmin-bw, xmax+bw)
	 #h_of = TH1F(name+'_of', '', nbin+2, xmin-bw, xmax+bw)
     #h= h_of
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
     #if 'u_p' in var: 
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


     #h_of.GetXaxis().SetRangeUser(h_of.GetXaxis().GetXmin(), h_of.GetXaxis().GetXmax() + h_of.GetXaxis().GetBinWidth(1)/10)
     h_of.GetXaxis().SetRangeUser(h_of.GetXaxis().GetXmin(), h_of.GetXaxis().GetXmax())

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

