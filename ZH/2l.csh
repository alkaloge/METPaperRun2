
#xrdcp root://cms-xrd-global.cern.ch//store/user/jbechtel/taupog/nanoAOD-v2/DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1-v1/32/myNanoProdMc2017_NANO_31.root inFile.root

#python 2Lep.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2018/DYJetsToLLM50/all_DYJetsToLLM50_file001_part_1of3_Muons.root -o DYMu.root --nickName DYJetsToLLM50 -y 2017 -s 2Lep -w 0 -n 5000 -j 0
python 2Lep.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2018/DYJetsToLLM50NLO/all_DYJetsToLLM50NLO_file001_part_1of3_Muons.root -o DYEl.root --nickName DYJetsToLLM50 -y 2017 -s 2Lep -w 0 -n 500 -j 0
#python 2Lep.py -f /eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2018/SingleMuon_Run2018D/all_SingleMuon_Run2018D_file001_part_2of3_Muons.root -o DYElData.root --nickName DYJetsToLLM50 -y 2018 -s 2Lep -w 0 -n 500 -j 0 -d data

#python 2Lep.py -f  inFileDYNLO.root -o DYEl.root --nickName DYJetsToLLM50 -y 2018 -s 2Lep -w 0 -n 5000 -j 0



#xrdcp root://cms-xrd-global.cern.ch//store/user/swozniew/taupog/nanoAOD-v2/SingleMuon_Run2018D_22Jan2019v2_13TeV_MINIAOD/73/myNanoProdData2018D_NANO_17972.root inFile.root
#python ZPeak.py -f inFile.root -o SingleMuon_Run2018D_22Jan2019_v2_NanoAODv5_000.root --nickName SingleMuon_Run2018D_22Jan2019_v2_NanoAODv5 -y 2018 -s ZPeak -w 0 -j no -d Data -n 25000

#rm inFile.root

