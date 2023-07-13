#xrdcp root://cms-xrd-global.cern.ch//store/group/lpcsusyhiggs/ntuples/nAODv5/2018D/DoubleMuon/nAODv5_DeepTID_v2p1_Run2018D-PromptReco-v2/200108_145400/0002/FILEHERE_2295.root inFile.root
#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018A/SingleMuon/NANOAOD/02Apr2020-v1/240000/2A711CC2-7DE6-5541-88CC-BBD7A363F404.root d2018_l779.root
#python ZH.py -f d2018_l779.root -o test.root --nickName SingleMuon_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data


#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018B/SingleMuon/NANOAOD/02Apr2020-v1/50000/50806500-995C-7B45-8901-F211C1D8EF13.root  d2018_l509.root
#python ZH.py -f d2018_l509.root -o test.root --nickName SingleMuon_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data

#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018C/SingleMuon/NANOAOD/02Apr2020-v1/20000/6F90D250-C99F-C649-B4A5-F5095F0075BA.root  d2018_l1315.root
#python ZH.py -f d2018_l1315.root -o test.root --nickName SingleMuon_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data


#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018A/SingleMuon/NANOAOD/02Apr2020-v1/50000/CD88B537-E3AB-4D4D-867B-A161B5D391CF.root  d2018_l248.root
#python ZH.py -f d2018_l248.root -o test.root --nickName SingleMuon_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data


#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018D/EGamma/NANOAOD/02Apr2020-v1/30000/A08D110F-C8C6-DF48-AC1E-C69005149551.root   d2018el_l313.root
#python ZH.py -f d2018el_l313.root -o test.root --nickName EGamma_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data


#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018D/EGamma/NANOAOD/02Apr2020-v1/230000/7CC28FC2-522C-834C-90E0-A954407BF844.root   d2018el_l62.root
#python ZH.py -f d2018el_l62.root -o test.root --nickName EGamma_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data

#xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018D/EGamma/NANOAOD/02Apr2020-v1/230000/E37CA566-2905-094D-8931-8B3C43AC68EB.root   d2018el_1139.root


#xrdcp root://cmsxrootd.fnal.gov//store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_2018/SingleMuon/SingleMuon_Run2018D_2018/210109_171312/0000/SingleMuon_Run2018D_2018_4of5_64.root inFiled.root
#python ZH.py -f inFiled.root -o SingleMuon_Run2018D_1132.root --nickName SingleMuon_Run2018D -y 2018 -s ZH -w 0 -j 0 -d Data

#xrdcp root://cmsxrootd.fnal.gov//store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_2018/SingleMuon/SingleMuon_Run2018B_2018/201210_232435/0000/SingleMuon_Run2018B_2018_2of5_62.root inFiled178.root

xrdcp root://cmsxrootd.fnal.gov//store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_2018/SingleMuon/SingleMuon_Run2018B_2018/201210_232435/0000/SingleMuon_Run2018B_2018_2of5_63.root inFiled178.root
python ZH.py -f inFiled178.root -o SingleMuon_Run2018B_178.root --nickName SingleMuon_Run2018B -y 2018 -s ZH -w 0 -j 0 -d Data
