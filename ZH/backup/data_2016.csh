cp ../MC/cuts_ZH.yaml cuts.yaml

#xrdcp root://cms-xrd-global.cern.ch//store/user/mscham/taupog/nanoAOD-v2/SingleMuon_Run2016F_17Jul2018v1_13TeV_MINIAOD/69/myNanoProdData2016_NANO_68.root inFileD2016.root
#python ZHdebug.py -f inFileD2016.root -o SingleMuon_Run2016F_17Jul2018_v1_NanoAODv5_001.root --nickName SingleMuon_Run2016F_17Jul2018_v1_NanoAODv5 -y 2016 -s ZH -w 0 -j no -d Data -n 1000000
#python ZHdebug.py -f SM.root  -o SM_debug.root --nickName SingleMuon_Run2016F_17Jul2018_v1_NanoAODv5 -y 2016 -s ZH -w 0 -j no -d Data 
python ZH.py -f SM.root  -o SM_debug.root --nickName SingleMuon_Run2016F_17Jul2018_v1_NanoAODv5 -y 2016 -s ZH -w 0 -j no -d Data -n 60000

#rm inFile.root
