xrdcp root://cms-xrd-global.cern.ch//store/group/lpcsusyhiggs/ntuples/nAODv5/2018D/DoubleMuon/nAODv5_DeepTID_v2p1_Run2018D-PromptReco-v2/200108_145400/0002/FILEHERE_2295.root inFile.root
python ZH.py -f inFile.root -o DoubleMuon__Run2018DPromptRecov2_029.root --nickName DoubleMuon__Run2018DPromptRecov2 -y 2018 -s ZH  -w 0 -d Data

xrdcp root://cms-xrd-global.cern.ch//store/data/Run2016D/SingleMuon/NANOAOD/02Apr2020-v1/20000/F667DF11-5707-2941-A044-1D0ED88E4F74.root SM.root
