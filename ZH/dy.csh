
#xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/40000/6D7BB75E-C44F-7E47-99E1-954DBC5320E9.root inFile.root
python 2Lep.py -f inFileDYnv9.root -o DYJetsToLL_000.root --nickName DYJetsToLL -y 2017 -s 2Lep -w 0 -j yes -n 2000
#rm inFile.root
