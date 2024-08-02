import ROOT
import random
import array

nJetBins = 3
nZPtBins = 5
zPtBins = [0,10,20,30,50,1000]
jetBins = [-0.5,0.5,1.5,2.5]

NJetBins = ["NJet0","NJet1","NJetGe2"]
ZPtBins = ["Pt0to10",
	   "Pt10to20",
	   "Pt20to30",
	   "Pt30to50",
	   "PtGt50"]

RecoilZParal = "recoilZParal_"
RecoilZPerp = "recoilZPerp_"
RecoilPuppiZParal = "recoilPuppiZParal_"
RecoilPuppiZPerp = "recoilPuppiZPerp_"


samples = [
    "SingleMuon_Run2018", "DYJetsToLL_M-50_TuneCP5_13TeV_madgraphMLM_pythia8_ZPt",
    "WW_TuneCP5_13TeV-pythia8",
    "WZ_TuneCP5_13TeV-pythia8",
    "ZZ_TuneCP5_13TeV-pythia8",
    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
    "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
    "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    "TTTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
    "TTToSemiLeptonic_TuneCP5_13TeV_powheg_pythia8",
    "TTToHadronic_TuneCP5_13TeV_powheg_pythia8",
]




def createHistos(rootfile):
    print 'working for ', rootfile
    ZPtBinsH = ROOT.TH1D("ZPtBinsH", "ZPtBinsH", nZPtBins - 1, array.array('d', zPtBins))
    for iB in range(nZPtBins-1):
       ZPtBinsH.GetXaxis().SetBinLabel(iB + 1, ZPtBins[iB])

    # Saving jet bins
    JetBinsH = ROOT.TH1D("JetBinsH", "JetBinsH", nJetBins - 1, array.array('d', jetBins))
    for iB in range(nJetBins-1):
        JetBinsH.GetXaxis().SetBinLabel(iB + 1, NJetBins[iB])

    recoilZParalH = []
    recoilZPerpH = []
    recoilPuppiZParalH = []
    recoilPuppiZPerpH = []
    recoilZParal_Ptbins_nJetsH = [[None]*nZPtBins for _ in range(nJetBins)]
    recoilZPerp_Ptbins_nJetsH = [[None]*nZPtBins for _ in range(nJetBins)]
    recoilPuppiZParal_Ptbins_nJetsH = [[None]*nZPtBins for _ in range(nJetBins)]
    recoilPuppiZPerp_Ptbins_nJetsH = [[None]*nZPtBins for _ in range(nJetBins)]

    

    for i in range(nJetBins-1):
	for j in range(nZPtBins-1):
	    # Creating histograms for each combination of jet and Z pt bins
	    name_suffix = NJetBins[i] + "_" + ZPtBins[j]

	    # Filling histograms with random numbers between -100 and 100
	    recoilZParalH = ROOT.TH1D(RecoilZParal + name_suffix, RecoilZParal + name_suffix, 100, -200, 200)
	    recoilZPerpH = ROOT.TH1D(RecoilZPerp + name_suffix, RecoilZPerp + name_suffix, 100, -200, 200)
	    recoilPuppiZParalH = ROOT.TH1D(RecoilPuppiZParal + name_suffix, RecoilPuppiZParal + name_suffix, 100, -200, 200)
	    recoilPuppiZPerpH = ROOT.TH1D(RecoilPuppiZPerp + name_suffix, RecoilPuppiZPerp + name_suffix, 100, -200, 200)

	    for _ in range(100000):
		rand_val = random.gauss(0, 50)
		recoilZParalH.Fill(rand_val)
		recoilZPerpH.Fill(rand_val)
		recoilPuppiZParalH.Fill(rand_val)
		recoilPuppiZPerpH.Fill(rand_val)

	    # Saving histograms in respective arrays
	    recoilZParal_Ptbins_nJetsH[i][j] = recoilZParalH
	    recoilZPerp_Ptbins_nJetsH[i][j] = recoilZPerpH
	    recoilPuppiZParal_Ptbins_nJetsH[i][j] = recoilPuppiZParalH
	    recoilPuppiZPerp_Ptbins_nJetsH[i][j] = recoilPuppiZPerpH

    # Save histograms in a .root file
    output_file = ROOT.TFile('{0:s}.root'.format(rootfile), "RECREATE")
    output_file.cd()

    ZPtBinsH.Write()
    JetBinsH.Write()

    for i in range(nJetBins-1):
	for j in range(nZPtBins-1):
	    recoilZParal_Ptbins_nJetsH[i][j].Write()
	    recoilZPerp_Ptbins_nJetsH[i][j].Write()
	    recoilPuppiZParal_Ptbins_nJetsH[i][j].Write()
	    recoilPuppiZPerp_Ptbins_nJetsH[i][j].Write()

    output_file.Write()
    output_file.Close()

for i in samples:
    createHistos(str(i))
