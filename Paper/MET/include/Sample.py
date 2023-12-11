import ROOT as r
from array import array
from ROOT import TTree, TFile, TCut, TH1F, TH1D, TH2F, THStack, TCanvas, TEntryList
from math import sqrt, sin, cos, pi, tan, acos, atan2,log
from numpy import arange
import os
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

def calculate_transverse_mass(pt_lepton, mass_lepton, met):
    # Assuming pt_lepton, mass_lepton, and met are the transverse momentum, mass, and missing transverse energy
    # Convert pt_lepton and met to TVector2
    vec_lepton = ROOT.TVector2(pt_lepton, 0)
    vec_met = ROOT.TVector2(met, 0)

    # Calculate Delta Phi
    delta_phi = vec_lepton.DeltaPhi(vec_met)

    # Calculate transverse mass
    m_T = ROOT.TMath.Sqrt(2 * pt_lepton * met * (1 - ROOT.TMath.Cos(delta_phi)))

    return m_T



class Sample:
   'Common base class for all Samples'

   def __init__(self, name, location, xsection, isdata, doee, dokfactorweight, iszjets, era, channel, isLocal=True, isWinclWNjets=False, IWDP='mvaID', doChain=True):
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

      
      if doChain : 
          print 'Ordered a TChaining...will run on the individual files.....'

	  chain_events = r.TChain("Events")
	  #chain_weights = r.TChain("hWeights")
	  if 'Run' not in name:
	      if 'preVFP' in location and 'preVFP' not in str(era):
		  file_pattern = '{0:s}_{1:s}preVFP_{2:s}'.format(str(name), str(era), str(channel))
	      else:
		  file_pattern = '{0:s}_{1:s}_{2:s}/'.format(str(name), str(era), str(channel))
	  else:
	      file_pattern = '{0:s}_{1:s}/'.format(str(name), str(era), str(channel))

	  # Specify the patterns for the files you want to read
	  #file_patterns = [file_pattern + "*Muons.root", file_pattern + "*weights"]  # Adjust these patterns as needed
	  #file_patterns = ["Muons.root",  "weights"]  # Adjust these patterns as needed
	  if 'MuNu' in self.channel or 'MuMu' in self.channel: file_patterns = "/*Muons.root"  # Adjust these patterns as needed
	  if 'ElNu' in self.channel or 'ElEl' in self.channel: file_patterns = "/*Electrons.root"  # Adjust these patterns as needed

          if 'Run' in file_pattern : file_patterns ='/all*Run*_*root'
	  print "file_patterns", file_patterns, isLocal, file_pattern, location, self.location
	  # Add all matching files to the TChain
          file_location = location + file_patterns
	  if not isLocal:
              file_location = "root://cmseos.fnal.gov//" + location + file_patterns

	  #for pattern in file_patterns:
	  chain_events.Add(file_location)
	  print("Added file to 'Events' chain:", file_location)
	  #else:
	  #    chain_weights.Add(file_location)
	  #    print("Added weights file to 'hWeights' chain:", file_location)
          '''
         
	  files = [file for file in os.listdir(location) if file.startswith('all') and file.endswith('.root')]

	  for file_name in files:
	      file_location = os.path.join(location, file_name)
	      if not isLocal:
	  	  file_location = "root://cmseos.fnal.gov//" + file_location

	      chain_events.Add(file_location)
	      print("Added file to 'Events' chain:", file_location, chain_events.GetEntries())

          '''

          '''
	  if isLocal:
	      for pattern in file_patterns:
		  print('Getting files matching pattern:', pattern)
		  files = []
		  for root, dirs, root_files in os.walk(location):
		      for root_file in root_files:
			  if pattern in root_file:
			      file_path = os.path.join(root, root_file)
			      files.append(file_path)
		  print('Files matching pattern:', files)
		  
		  for file_path in files:
		      if 'weights' not in pattern:
			  chain_events.Add(file_path)
			  print("Added file to 'Events' chain:", file_path)
		      #else:
		      #	  chain_weights.Add(file_path)
	              #	  print("Added weights file to 'hWeights' chain:", file_path)
	  else:
	      for pattern in file_patterns:
		  file_location = "root://cmseos.fnal.gov//" + location + pattern
		  if 'weights' not in pattern:
		      chain_events.Add(file_location)
		      print("Added file to 'Events' chain:", file_location)
		  #else:
		  #    chain_weights.Add(file_location)
		  #    print("Added weights file to 'hWeights' chain:", file_location)
          '''
	  # Now, you can use 'chain_events' to read from all matched files
	  nEntries = chain_events.GetEntries()
	  #nEntriesW = chain_weights.GetEntries()
	  self.ttree = chain_events  # Assign the TChain to self.ttree
	  hWeights = None
	  print 'ok. this works....'



	  if not self.isData:
              weights_2018={
	    'ZZTo2L2Nu' : 55393059.2321,
	    'TTTo2L2Nu' : 10457567170.1,
	    'WJetsToLNu' : 899814058.903,
	    'WJetsToLNuincl' : 1.1888747e+09,
	    'WW' : 15679122.7146,
	    'QCD_HT1500to2000' : 10411831.0,
	    'ZZTo4L' : 130483170.281,
	    'WZ' : 7940000.0,
	    'QCD_HT500to700' : 49184771.0,
	    'ST_s-channel' : 68767081.0058,
	    'ST_t-channel_top' : 18955983283.5,
	    'WGToLNuG' : 9850083.0,
	    'ZZZ' : 3690.78421879,
	    'W2JetsToLNu' : 40098866.6759,
	    'ST_tW_antitop' : 251902154.461,
	    'W1JetsToLNu' : 139159134.165,
	    'QCD_HT1000to1500' : 13754593.0,
	    'TTToSemiLeptonic' : 1.43354138329e+11,
	    'ST_tW_top' : 258137404.748,
	    'DYJetsToLLM50' : 96233328.0,
	    'QCD_HT700to1000' : 48506751.0,
	    'WZZ' : 17121.264862,
	    'QCD_HT100to200' : 82114770.0,
	    'W3JetsToLNu' : 20236537.9556,
	    'WWW' : 51638.2565607,
	    'QCD_HT50to100' : 36944853.0,
	    'ttWJets' : 27686862.0,
	    'QCD_HT200to300' : 57336623.0,
	    'WZTo3LNu' : 83145977.5623,
	    'QCD_HT300to500' : 61675573.0,
	    'DYJetsToLLM10to50' : 94452816.0,
	    'DYJetsToLLM10to50NLO' : 94452816.0,
	    'ST_t-channel_antitop' : 6114949634.87,
	    'ZZTo2Q2L' : 161924458.071,
	    'QCD_HT2000toInf' : 5374711.0,
	    'WJetsToLNu_NLO' : 5.01811676681e+12,
	    'WJetsToLNu_NLO61' : 5.01811676681e+12,
	    'W4JetsToLNu' : 57029839635.0,
	    'WJetsToLNu_HT-800To1200' : 7306187.0,
	    'WJetsToLNu_HT-200To400' : 57880058.0,
	    'WJetsToLNu_HT-600To800' : 7718765.0,
	    'WJetsToLNu_HT-1200To2500' : 6481518.0,
	    'WJetsToLNu_HT-100To200' : 66195407.0,
	    'WJetsToLNu_HT-2500ToInf' : 2097648.0,
	    'WJetsToLNu_HT-400To600' : 7444030.0,
	    'WJetsToLNu_HT-70To100' : 65203183.0}



              weights_2017={
		'ZZTo2L2Nu' : 39767479.5829,
		'WJetsToLNu_HT-800To1200' : 5088483.0,
		'WJetsToLNu_HT-200To400' : 40682216.0,
		'TTTo2L2Nu' : 7695841652.17,
		'WJetsToLNu' : 782170184.765,
		'WJetsToLNuincl' : 1.0308170e+09,
		'WW' : 15634116.1995,
		'QCD_HT1500to2000' : 7613935.0,
		'WJetsToLNu_HT-600To800' : 5545298.0,
		'ZZTo4L' : 131669255.013,
		'WZ' : 7889000.0,
		'QCD_HT500to700' : 36194860.0,
		'ST_s-channel' : 48361410.4205,
		'ST_t-channel_top' : 5734591181.42,
		'WGToLNuG' : 10302104.0,
		'QCD_HT50to100' : 26208347.0,
		'WJetsToLNu_HT-600To800_ext1' : 3711469.0,
		'W2JetsToLNu' : 38944765.4379,
		'ST_tW_antitop' : 184446306.894,
		'W1JetsToLNu' : 132885035.121,
		'TTToSemiLeptonic' : 1.04129959629e+11,
		'ST_tW_top' : 183284892.385,
		'WJetsToLNu_NLO' : 4.55989376573e+12,
		'WJetsToLNu_NLO61' : 4.55989376573e+12,
		'QCD_HT700to1000' : 32934816.0,
		'WJetsToLNu_HT-1200To2500' : 4290420.0,
		'WZZ' : 17023.6507413,
		'QCD_HT100to200' : 73254068.0,
		'QCD_HT1000to1500' : 4266174.0,
		'WJetsToLNu_HT-100To200' : 47424468.0,
		'W4JetsToLNu' : 61149413352.2,
		'ZZTo2Q2L' : 162895522.709,
		'ttWJets' : 27662138.0,
		'QCD_HT200to300' : 42714435.0,
		'QCD_HT300to500' : 43429979.0,
		'DYJetsToLLM10to50' : 68480179.0,
		'DYJetsToLLM10to50NLO' : 68480179.0,
		'ST_t-channel_antitop' : 4462868882.06,
		'WWW' : 36869.1608253,
		'DYJetsToLLM50' : 102863931.0,
		'WJetsToLNu_HT-400To600_ext1' : 1435543.0,
		'WJetsToLNu_HT-2500ToInf' : 1185699.0,
		'QCD_HT2000toInf' : 1847781.0,
		'WJetsToLNu_HT-400To600' : 5468473.0,
		'W3JetsToLNu' : 19790787.9141,
		'WJetsToLNu_HT-70To100' : 40239665.0,}




              weights_2016 = {
		'ZZTo2L2Nu' : 15509971.4162,
		'TTTo2L2Nu' : 3140127310.67,
		'WJetsToLNu' : 7.37278808976e+12,
		'WJetsToLNuincl' : 9.6974101e+12,
		'WW' : 15821137.2551,
		'QCD_HT1500to2000' : 3003707.0,
		'ZZTo4L' : 251315344.271,
		'WZ' : 7584000.0,
		'QCD_HT500to700' : 14212819.0,
		'QCD_HT100to200' : 23717410.0,
                'ST_s-channel' : 22286424.6235,
		'ST_t-channel_top' : 6703801969.77,
		'WGToLNuG' : 8394172.0,
		'QCD_HT50to100' : 11197186.0,
		'W2JetsToLNu' : 39941566.5092,
		'ST_tW_antitop' : 83024147.0543,
		'W1JetsToLNu' : 1.26365736659e+12,
		'TTToSemiLeptonic' : 43548253970.6,
		'ST_tW_top' : 80821434.5228,
		'DYJetsToLLM50' : 82448537.0,
		'QCD_HT700to1000' : 13194849.0,
		'QCD_HT100to200' : 23717410.0,
		'WZZ' : 260326.405728,
		'QCD_HT1000to1500' : 4365993.0,
		'WWW' : 897983.02362,
		'W4JetsToLNu' : 30810512901.7,
		'ZZTo2Q2L' : 75775135.9249,
		'ttWJets' : 901003.005917,
		'QCD_HT200to300' : 17569141.0,
		'QCD_HT300to500' : 16747056.0,
		'DYJetsToLLM10to50' : 26927726.0,
		'DYJetsToLLM10to50NLO' : 26927726.0,
		'ST_t-channel_antitop' : 1957283183.15,
		'QCD_HT2000toInf' : 1847781.0,
		'WJetsToLNu_NLO' : 4.87296446076e+12,
		'WJetsToLNu_NLO61' : 4.87296446076e+12,
		'W3JetsToLNu' : 18887529.5137,}





              weights_2016preVFP={
		'ZZTo2L2Nu' : 16419222.3522,
		'TTTo2L2Nu' : 2704527656.16,
		'WJetsToLNu' : 602065852.695,
		'WJetsToLNuincl' : 7.9600471e+08,
		'WW' : 15859130.7831,
		'QCD_HT1500to2000' : 3503675.0,
		'ZZTo4L' : 271601384.279,
		'WZ' : 7934000.0,
		'QCD_HT500to700' : 15775001.0,
		'ST_s-channel' : 19596249.8351,
		'ST_t-channel_top' : 5948135153.64,
		'WGToLNuG' : 9714707.0,
		'QCD_HT50to100' : 12233035.0,
		'W2JetsToLNu' : 44186948.5833,
		'ST_tW_antitop' : 74766341.1971,
		'W1JetsToLNu' : 197368322.281,
		'TTToSemiLeptonic' : 39772305959.2,
		'ST_tW_top' : 74624668.1187,
		'DYJetsToLLM50' : 95170542.0,
		'QCD_HT700to1000' : 15808790.0,
		'WZZ' : 308416.915451,
		'QCD_HT100to200' : 26312661.0,
		'QCD_HT1000to1500' : 4773503.0,
		'WWW' : 15310.5959079,
		'W4JetsToLNu' : 28287448247.5,
		'ZZTo2Q2L' : 88594639.7718,
		'ttWJets' : 27548593.0,
		'QCD_HT200to300' : 16524587.0,
		'QCD_HT300to500' : 16720486.0,
		'DYJetsToLLM10to50' : 32305345.0,
		'DYJetsToLLM10to50NLO' : 32305345.0,
		'ST_t-channel_antitop' : 1983864432.8,
		'QCD_HT2000toInf' : 1629000.0,
		'WJetsToLNu_NLO' : 4.98951935909e+12,
		'WJetsToLNu_NLO61' : 4.98951935909e+12,
		'W3JetsToLNu' : 18073455.0193, }

              weights_2Lep_2018={
		'ZZTo2L2Nu' : 55393059.2321,
		'TTTo2L2Nu' : 10457567170.1,
		'WJetsToLNu' : 899814058.903,
		'WW' : 15679122.7146,
		'ZZTo4L' : 130483170.281,
		'WZ' : 7940000.0,
		'ST_s-channel' : 68767081.0058,
		'ST_t-channel_top' : 18955983283.5,
		'WGToLNuG' : 9850083.0,
		'ZZZ' : 3690.78421879,
		'W2JetsToLNu' : 40098866.6759,
		'ST_tW_antitop' : 251902154.461,
		'W1JetsToLNu' : 139159134.165,
		'TTToSemiLeptonic' : 1.43354138329e+11,
		'ST_tW_top' : 258137404.748,
		'WZZ' : 17121.264862,
		'WWW' : 51638.2565607,
		'ZZTo2Q2L' : 161924458.071,
		'W4JetsToLNu' : 57029839635.0,
		'ttWJets' : 27686862.0,
		'WZTo3LNu' : 83145977.5623,
		'WWTo2L2Nu' : 110795280.393,
		'DYJetsToLLM10to50' : 94452816.0,
		'DYJetsToLLM10to50NLO' : 94452816.0,
		'ST_t-channel_antitop' : 6114949634.87,
		'DYJetsToLLM50NLO' : 3.32347727281e+12,
		'WZTo2Q2L' : 274146237.028,
		'WWZ' : 42310.5167204,
		'DYJetsToLLM50' : 96233328.0,
		'W3JetsToLNu' : 20236537.9556,}



              weights_2Lep_2017={
	        'ZZTo2L2Nu' : 39767479.5829,
		'TTTo2L2Nu' : 7695841652.17,
		'WJetsToLNu' : 782170184.765,
		'WW' : 15634116.1995,
		'QCD_HT1500to2000' : 7613935.0,
		'ZZTo4L' : 131669255.013,
		'WZ' : 7889000.0,
		'QCD_HT500to700' : 36194860.0,
		'ST_s-channel' : 48361410.4205,
		'ST_t-channel_top' : 5734591181.42,
		'WGToLNuG' : 10302104.0,
		'ZZZ' : 2232.54036875,
		'W2JetsToLNu' : 38944765.4379,
		'ST_tW_antitop' : 184446306.894,
		'W1JetsToLNu' : 132885035.121,
		'TTToSemiLeptonic' : 1.04129959629e+11,
		'ST_tW_top' : 183284892.385,
		'QCD_HT700to1000' : 32934816.0,
		'WZZ' : 17023.6507413,
		'QCD_HT100to200' : 73254068.0,
		'QCD_HT1000to1500' : 4266174.0,
		'WWW' : 36869.1608253,
		'W4JetsToLNu' : 61149413352.2,
		'ZZTo2Q2L' : 162895522.709,
		'ttWJets' : 27662138.0,
		'QCD_HT200to300' : 42714435.0,
		'WZTo3LNu' : 87396868.0337,
		'QCD_HT300to500' : 43429979.0,
		'WWTo2L2Nu' : 81217075.2477,
		'QCD_HT50to100' : 26208347.0,
		'DYJetsToLLM10to50' : 68480179.0,
		'DYJetsToLLM10to50NLO' : 68480179.0,
		'ST_t-channel_antitop' : 4462868882.06,
		'DYJetsToLLM50NLO' : 3.32297132154e+12,
		'WZTo2Q2L' : 279011951.235,
		'WWZ' : 30386.2912494,
		'QCD_HT2000toInf' : 1847781.0,
		'DYJetsToLLM50' : 102863931.0,
		'W3JetsToLNu' : 19790787.9141,}



              weights_2Lep_2016={
		'ZZTo2L2Nu' : 15509971.4162,
		'TTTo2L2Nu' : 3140127310.67,
		'WW' : 15821137.2551,
		'ZZTo4L' : 251315344.271,
		'WZ' : 7584000.0,
		'ST_s-channel' : 22286424.6235,
		'ST_t-channel_top' : 6703801969.77,
		'WGToLNuG' : 8394172.0,
		'ZZZ' : 66938.696801,
		'ST_tW_antitop' : 83024147.0543,
		'TTToSemiLeptonic' : 43548253970.6,
		'ST_tW_top' : 80821434.5228,
		'WZZ' : 260326.405728,
		'WWW' : 897983.02362,
		'ZZTo2Q2L' : 75775135.9249,
		'ttWJets' : 901003.005917,
		'WZTo3LNu' : 88368496.8435,
		'WWTo2L2Nu' : 32147079.1672,
		'DYJetsToLLM10to50' : 26927726.0,
		'DYJetsToLLM10to50NLO' : 26927726.0,
		'ST_t-channel_antitop' : 1957283183.15,
		'DYJetsToLLM50NLO' : 1.22093461966e+12,
		'WZTo2Q2L' : 129756624.839,
		'WWZ' : 11495.7245052,
		'WWZ_ext1' : 784713.668116,
		'DYJetsToLLM50' : 82448537.0, }




              weights_2Lep_2016preVFP={
		'ZZTo2L2Nu' : 16419222.3522,
		'TTTo2L2Nu' : 2704527656.16,
		'WW' : 15859130.7831,
		'ZZTo4L' : 271601384.279,
		'WZ' : 7934000.0,
		'ST_s-channel' : 19596249.8351,
		'ST_t-channel_top' : 5948135153.64,
		'WGToLNuG' : 9714707.0,
		'ZZZ' : 78317.0635339,
		'ST_tW_antitop' : 74766341.1971,
		'TTToSemiLeptonic' : 39772305959.2,
		'ST_tW_top' : 74624668.1187,
		'WZZ' : 308416.915451,
		'WWW' : 15310.5959079,
		'ZZTo2Q2L' : 88594639.7718,
		'ttWJets' : 27548593.0,
		'WZTo3LNu' : 81516536.6689,
		'WWTo2L2Nu' : 33456497.8642,
		'DYJetsToLLM10to50' : 32305345.0,
		'DYJetsToLLM10to50NLO' : 32305345.0,
		'ST_t-channel_antitop' : 1983864432.8,
		'DYJetsToLLM50NLO' : 1.52013901776e+12,
		'WZTo2Q2L' : 150461586.121,
		'WWZ' : 4447.16192749,
		'WWZ_ext1' : 866227.881285,
		'DYJetsToLLM50' : 95170542.0,}




              weights_=None
              if 'MuNu' in self.channel or 'ElNu' in self.channel:

		  if str(era) == "2018" : weights_ = weights_2018
		  if str(era) == "2017" : weights_ = weights_2017
		  if str(era) == "2016" or str(era) == "2016postVFP": weights_ = weights_2016
		  if str(era) == "2016preVFP" : weights_ = weights_2016preVFP

              if 'MuMu' in self.channel or 'ElEl' in self.channel:

		  if str(era) == "2018" : weights_ = weights_2Lep_2018
		  if str(era) == "2017" : weights_ = weights_2Lep_2017
		  if str(era) == "2016" or str(era) == "2016postVFP": weights_ = weights_2Lep_2016
		  if str(era) == "2016preVFP" : weights_ = weights_2Lep_2016preVFP
             
              try : self.count = weights_[str(name)] 

	      except AttributeError: 
		  self.count = 1.
		  self.xSection = 0

	  if self.xSection !=0 : print self.name, 'neentries', self.ttree.GetEntries()        
	  #self.count = self.tfile.Get('demo/nEvents').GetSumOfWeights()
	  else :
	      #self.count = self.ttree.GetEntries()
	      self.count = 1

      if not doChain : 
          print 'no chaining...will run on the merged'
	  if 'Run' not in name : 
	      if 'preVFP' in location and 'preVFP' not in str(era): tfileloc= self.location+'/{0:s}_{1:s}preVFP_{2:s}.root'.format( str(name), str(era), str(channel))
	      else : tfileloc=self.location+'/{0:s}_{1:s}_{2:s}.root'.format( str(name), str(era), str(channel))
	  else : tfileloc = self.location+'/{0:s}_{1:s}.root'.format( str(name), str(era), str(channel))
	  if isLocal  : self.tfile = TFile(tfileloc)

	  else  :
	      print 'this is not local, will try to read from-->', 'root://cmseos.fnal.gov//', '+ tfileloc', tfileloc 
	      self.tfile = TFile.Open("root://cmseos.fnal.gov//"+tfileloc, "READ")
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
	  print 'will try to read from ', self.location, self.tfile.GetName(), name, era, channel
	  self.ttree = self.tfile.Get('Events')
	  print self.name
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



   # this is the correct one!!!
   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel, channel):
      print 'inside the correct one....', name, var, options
      if(xmin == xmax):
        h = TH1D(name, "", len(nbin)-1, array('d', nbin))
        #h = TH1F(name, "", 10,0.,500.)
        ylabel = "# events"
      else:
        h = TH1D(name, "", nbin, xmin, xmax)
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
              #if 'WJetsToLNu' in h.GetName() and 'NLO' not in h.GetName() and 'incl' not in options: cut = cut +  " && LHE_Njets[0]<1 "
              if 'WJetsToLNu' in h.GetName() and 'NLO' not in h.GetName() and 'incl' not in options and 'ewkht' not in options: 
                  cut = cut +  " && LHE_Njets[0]<1 "

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
          
          #if 'WJets' in h.GetName() and 'NLO' not in h.GetName() :
          #     cut = cut +  "&& ( " + "weight[0] " +  " ) < 10"
      #if not self.isData :
      #    if 'QCD' in name : cut = cut +  "* ( " + "Photon_genPartFlav_1[0] !=1" +  " ) "

      if self.isData :
          if 'Photon' in name or 'Photon' in cut : cut = cut +  "* ( " + "weightpsjson[0] " +  " ) "
          #cut = cut +  "* min( " + "weightpsjson[0] " + "," + "weightps2[0]" +  " ) "

      if 'u_par' in var or 'u_perp' in var :
	  if 'parboson' not in var: var = "-1.*"+var
	  #if 'u_parboson' in var : 
	  #    var = var.replace("parboson", "par")

          if 'Gjets' in channel or 'ElEl' in channel or 'MuMu' in channel: 
	      if 'u_perp'  in var: var = var + "/boson_pt"
	      if 'u_parboson' in var : 
		  var = var.replace("parboson", "par")
		  var  = var + "+ boson_pt"
	      if 'resp' in var : 
		  var = var.replace("resp", "")
		  var  = "("+var + ")/boson_pt"

          if 'ElNu' in channel or 'MuNu' in channel: 
              bpt= "METCorGoodboson_pt"
              if "METCorGood" in var and "Puppi" not in var : bpt = "METCorGood_T1_pt"
              if "PuppiMETCorGood" in var  : bpt = "PuppiMETCorGood_pt"
	      if 'u_perp'  in var: var = var + "/"+bpt

	      if 'u_parboson' in var : 
		  var = var.replace("parboson", "par")
		  var  = var + "+ "+ bpt

	      if 'resp' in var : 
		  var = var.replace("resp", "")
		  var  = "("+var + ")/" + bpt



          #cut = cut +  "&& ( " + var +  " ) > -410" + "&& ( " + var +  " ) < 410 && boson_pt >=0"
          #cut = cut +  "&& boson_pt >=0"
          #cut = cut +  "&& boson_pt >=0"
         
      print '============================>>>>>>>>>>', h.GetName(), cut, 'puweigh = ', options, var
      #cut =  cut    + "&& Entry$ < 1000"
      print 'some info....', name, "var", var, "cut", cut, "options", options
      evscale=1.
     
      
      #try : self.ttree.Project(name, var, cut, options)
      #cut="( fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 &&  fabs(q_1[0])==1 && iso_1[0] <= .15&& iso_1>=0. && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPVGood[0]>2 && cat==1  && njets[0]  >=0 && METCorGoodboson_transm[0]  > 80. && VetoElectron[0]==0 && VetoMuon[0] == 0 && nbtagL[0]== 0.0 )"
      #cut="(Flag_BadPFMuonDzFilter[0]==1  && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 &&  fabs(q_1[0])==1 && iso_1[0] <= .15 && cat==1  && njets[0]  >=0 && METCorGoodboson_transm[0]  > 80. && nbtagL[0]== 0.0 && VetoMuon[0]==0 && VetoElectron[0]==0)"
      print 'UPDATEDDDDDDDDDDDDDDDDDDDDDDDDDDDd', cut, 'options------------>',options, self.isData
      #h.SetPrecision(123)
      if self.isData : self.ttree.SetWeight(1.)
      try : self.ttree.Project(name, var, cut)
      except AttributeError : 
          h.Scale(0)
          print 'BIG PROBLEM================!!!!!!!!!!!!!!!!!!!!!!########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################', h.GetName()
      #try:self.ttree.Draw("{0:s}>>h".format(str(var)), cut, options)
      #except AttributeError : h.Scale(0)


      try : print 'some info======================....entries ', self.ttree.GetEntries(), 'name', h.GetName(), 'SumOfWeights', h.GetSumOfWeights(), 'title', h.GetTitle(), "cut", cut, "lumiWeight*lumi", str(self.lumWeight*lumi), "lumi", lumi, 'lumiW', self.lumWeight
      except AttributeError : print 'cannot give more info....'
      
      #if not self.isData : h.Scale(lumi*self.lumWeight)
      if not self.isData : h.Scale(float(lumi*float(self.lumWeight))*evscale)

      print 'aftermath...', h.GetSumOfWeights(), 'entries', h.GetEntries(), 'underflow', h.GetBinContent(0), 'overflow', h.GetBinContent(h.GetNbinsX() + 1) 
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

   def __init__(self, fileName, name, isdata, chann, islocal=True, isWjetsWNjets=False,  IWDP='mvaID', dochain=False):
      self.name  = name
      self.isData = isdata
      self.blocks = []
      self.channel  = 'MuMu'
      self.isWjetsWNjets = isWjetsWNjets
      self.IWDP=  IWDP
      self.dochain=  dochain
      self.islocal = islocal
      self.parseFileName(fileName, chann, islocal, isWjetsWNjets, IWDP, dochain)
      #Sample.Tree(helper.selectSamples(opts.sampleFile, ewkNLODatasets, 'EWKNLO'), 'EWKNLO'  , 0, channel, isLocal)
   def parseFileName(self, fileName, chann, islocal, isWjetsWNjets, IWDP, dochain):
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

        sample = Sample(name, location,  xsection, isdata, doboson, dokfactor, iszjets, year, chann, islocal, isWjetsWNjets, IWDP, dochain)
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

     if 'iso_1' in var : 
         nbin = arange( 0., 0.20, 0.005)

     if 'sieie' in var : 
         nbin = arange( 0., 0.016, 0.002)

     if 'WTmass' in var or 'Wmass' in var or '_transm' in var: 
         islog  = False 
         nbin = range(20,200,10)
  
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

