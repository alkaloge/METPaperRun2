import os
import sys

years = ["2018", "2017", "2016", "2016pre"]
years = ["2016" , "2016preVFP"]
years = ["2017", "2018", "2016preVFP" ]
years = ["2018"]
channels = ["MuMu" ,"ElEl"]
channels = ["MuMu"]
channels = ["Gjets"]
Njet=['eq0', 'eq1', 'geq1', 'incl']
if 'Gjets' in channels : Njet=['eq1', 'geq1', 'incl']


command = sys.argv[1]
if command.lower() == "merge" : 
    for year in years:
        if year == '2016all' : continue
	for channel in channels:
            for njet in Njet:
		if channel == "Gjets" :
                    if '2018' in year: os.system("hadd -f scales_EGamma_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_EGamma_Run{0}*root".format(year, channel, njet))
                    if '2018' not in year: os.system("hadd -f scales_SinglePhoton_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SinglePhoton_Run{0}*root".format(year, channel, njet))
                    os.system("hadd -f scales_GjetsHT_{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_GJets_HT*_{1}*root".format(year, channel, njet))
		if channel == "MuMu" and 'pre' not in year: os.system("hadd -f scales_SingleMuon_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SingleMuon_Run{0}*root".format(year, channel, njet))
		if channel == "MuMu" and 'pre' in year: os.system("hadd -f scales_SingleMuon_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SingleMuon_Run2016*pre*root".format(year, channel, njet))
		if channel == "ElEl" : 
		    if year == "2017" or year=='2016' :os.system("hadd -f scales_SingleElectron_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SingleElectron_Run{0}*root".format(year, channel, njet))
		    if year == "2016preFVP"  :os.system("hadd -f scales_SingleElectron_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SingleElectron_Run2016*pre*root".format(year, channel, njet))
		    if year == "2018" :os.system("hadd -f scales_EGamma_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_EGamma_Run{0}*root".format(year, channel, njet))
		if channel != "Gjets": 
		    os.system("hadd -f scales_DYJetsToLLM50_{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_DYJetsToLLM50_*file*root".format(year, channel, njet))
		    os.system("hadd -f scales_DYJetsToLLM50NLO_{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_DYJetsToLLM50NLO_*file*root".format(year, channel, njet))

if command.lower() == "merge2016" : 
    year="2016"
    for channel in channels:
	for njet in Njet:
	    if channel == "MuMu" : 
		os.system("hadd -f scales_SingleMuon_Run{0}all_{1}_Njet{2}.root scales_SingleMuon_Run{0}_{1}_Njet{2}.root scales_SingleMuon_Run{0}preVFP_{1}_Njet{2}.root".format(year, channel, njet))
	    if channel == "ElEl" : 
		os.system("hadd -f scales_SingleElectron_Run{0}all_{1}_Njet{2}.root scales_SingleElectron_Run{0}_{1}_Njet{2}.root scales_SingleElectron_Run{0}preVFP_{1}_Njet{2}.root".format(year, channel, njet))
	    os.system("hadd -f scales_DYJetsToLLM50_{0}all_{1}_Njet{2}.root scales_DYJetsToLLM50_{0}_{1}_Njet{2}.root  scales_DYJetsToLLM50_{0}preVFP_{1}_Njet{2}.root".format(year, channel, njet))
	    os.system("hadd -f scales_DYJetsToLLM50NLO_{0}all_{1}_Njet{2}.root scales_DYJetsToLLM50NLO_{0}_{1}_Njet{2}.root  scales_DYJetsToLLM50NLO_{0}preVFP_{1}_Njet{2}.root".format(year, channel, njet))



if command.lower() == "extract" : 
    for year in years:
	for channel in channels:
            for njet in Njet:
		if channel == "MuMu" and 'pre' not in year : os.system("python extract2.py scales_SingleMuon_Run{0}_{1}_Njet{2}.root {1} {0} ".format(year, channel, njet))
		if channel == "ElEl" : 
		    if year == "2017" or '2016' in year :os.system("python extract2.py scales_SingleElectron_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    if year == "2018" :os.system("python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		os.system("python extract2.py scales_DYJetsToLLM50_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		os.system("python extract2.py scales_DYJetsToLLM50NLO_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		if channel == "Gjets" : 
		    if year == "2018" :os.system("python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    if year != "2018" :os.system("python extract2.py scales_SinglePhoton_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    os.system("python extract2.py scales_GjetsHT_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))

