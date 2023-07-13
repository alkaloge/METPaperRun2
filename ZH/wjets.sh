

#python Wjets.py -f /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2018/WJetsToLNu/all_WJetsToLNu_file003_part_2of3.root --nickName WJetsToLNu -s WJetsToLNu -w 0 -y 2018 -j 1  -o WJetsToLNu_001.root

#python Wjets.py -f /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2018/SingleMuon_Run2018C/all_SingleMuon_Run2018C_file001_part_1of3.root --nickName WJetsToLNu -s WJetsToLNu -w 0 -y 2018 -j 1 -d data -o WJetsToLNu_001.root -n 1000

#python Wjets.py -f /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/tools/inFileW2018_Skim.root --nickName WJetsToLNu -s WJetsToLNu -w 0 -y 2018 -j 1 -d MC -o WJetsToLNu_001.root

#python Wjets.py -f /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2018/WJetsToLNu/all_WJetsToLNu_file058_part_1of3_Electrons.root --nickName WJetsToLNu -s WJetsToLNu -w 0 -y 2018 -j 1 -d MC -o WJetsToLNu_001.root -n 500
python Wjets.py -f /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2017/WJetsToLNu/all_WJetsToLNu_file058_part_1of3_Muons.root --nickName WJetsToLNu -s WJetsToLNu -w 0 -y 2017 -j 1 -d MC -o WJetsToLNu_001.root -n 2000

#python Wjets.py -f inFileWMC.root -n 10000  --nickName WJetsToLNu -s WJetsToLNu -w 1 -y 2018 -j 1  -o WJetsToLNu_001.root
#python Wjets.py -f inFileWMC.root -n 10000  --nickName WJetsToLNu -s WJetsToLNu -w 1 -y 2018 -j 0  -o WJetsToLNu_001_noSyst.root
#python Wjets.py -f inFile.root -n 10000  --nickName WW -s WW -w 1 -y 2017 -j 1  -o WW_001.root

#python Wjets.py -f inFileData.root -n 5000  --nickName Wjets -s Wjets -w 1 -y 2018 -j 1 -d Data
#python Wjets.py -n 5000 -f inD.root  --nickName Wjets -s Wjets -w 1 -y 2018 -j 1 -d Data
