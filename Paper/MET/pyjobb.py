import ROOT as r

from ROOT import TTree, TFile, TCut, TH1F, TH2F, THStack, TCanvas, TEntryList


tfile= TFile.Open("root://cmsxrootd.fnal.gov///store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/WJetsToLNu_NLO_2016preVFP/WJetsToLNu_NLO_2016preVFP_MuMu.root","read")

tfile.cd()
tfile.ls()
ttree = tfile.Get('Events')
print 'eventsssss', ttree.GetEntries()



