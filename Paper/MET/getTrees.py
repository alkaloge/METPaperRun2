import ROOT as r
from ROOT import TFile, TTree

fIn="/eos/uscms/store/group/lpcsusyhiggs/ntuples/MetStudies/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/histo_77.root"

fIn="f.root"
fIn="temp_out.ntup"
fIn='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets/DYJetsToLLM50_2018/DYJetsToLLM50_2018.root'
fIn='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets/WJetsToLNu_2018/WJetsToLNu_2018.root'
f = TFile.Open(fIn ,"READ")


llist=['PuppiMET_', 'MET_', 'MET_T1_']
llist=['PuppiMET_']

pts=['pt','phi']
var=['Up', 'Down']
syst=['Unclustered', 'JER', 'JES']

mets=[]

mets.append('RawPuppiMET_pt')
mets.append('RawPuppiMET_phi')
mets.append('PuppiMET_pt')
mets.append('PuppiMET_phi')
mets.append('RawMET_pt')
mets.append('RawMET_phi')
mets.append('MET_pt')
mets.append('MET_phi')
mets.append('MET_T1_pt')
mets.append('MET_T1_phi')

for l in llist:
    for p in pts:
	for s in syst:
	    for v in var:
                if l=='MET_T1_' and 'JER' in s: s='_jer'
                if l=='MET_T1_' and 'JES' in s: s='_jesTotal'
                mets.append(l+p+s+v)

print mets

ins=[]
    

tree= f.Get("Events")

#tree.Scan(':'.join(mets))
tree.Print()



