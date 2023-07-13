
#xrdcp root://cms-xrd-global.cern.ch//store/user/jbechtel/taupog/nanoAOD-v2/DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1-v1/32/myNanoProdMc2017_NANO_31.root inFile.root

#python 2Lep.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2018/DYJetsToLLM50/all_DYJetsToLLM50_file001_part_1of3_Muons.root -o DYMu.root --nickName DYJetsToLLM50 -y 2017 -s 2Lep -w 0 -n 5000 -j 0
#python Gjets.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets/2018/EGamma_Run2018D/all_EGamma_Run2018D_file001_part_1of3_Gjets.root -o GJets.root --nickName EGamma -y 2018 -s Gjets -w 0 -n 5000 -j 0 -d 1

#python Gjets.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets/2017/SinglePhoton_Run2017F/all_SinglePhoton_Run2017F_file001_part_1of3_Gjets.root -o GJets.root --nickName EGamma -y 2017 -s Gjets -w 0 -n 5000 -j 0 -d 1

python Gjets.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets/2016/SinglePhoton_Run2016C_preVFP/all_SinglePhoton_Run2016C_preVFP_file001_part_1of3_Gjets.root  -o GJets.root --nickName SinglePhoton_Run2016C_preVFP -y 2016 -s Gjets -w 0  -d Data -n 1000 -j 0

#python Gjets.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets/2018/TTGjets_2018/TTGjets_2018_Gjets.root -o GJets.root --nickName EGamma -y 2018 -s Gjets -w 0 -n 5000 -j 0 -d 0
#python Gjets.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets/2018/GJets_HT-100To200/all_GJets_HT-100To200_file001_part_1of3_Gjets.root -o GJets.root --nickName EGamma -y 2018 -s Gjets -w 0 -n 5000 -j 1 -d 0



#xrdcp root://cms-xrd-global.cern.ch//store/user/swozniew/taupog/nanoAOD-v2/SingleMuon_Run2018D_22Jan2019v2_13TeV_MINIAOD/73/myNanoProdData2018D_NANO_17972.root inFile.root
#python ZPeak.py -f inFile.root -o SingleMuon_Run2018D_22Jan2019_v2_NanoAODv5_000.root --nickName SingleMuon_Run2018D_22Jan2019_v2_NanoAODv5 -y 2018 -s ZPeak -w 0 -j no -d Data -n 25000

#rm inFile.root

