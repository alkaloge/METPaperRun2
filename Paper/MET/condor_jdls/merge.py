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
if 'Gjets' in channels : Njet=['eq1', 'incl']
if 'Gjets' in channels : Njet=['incl']
#MC = ['QCD_HT1000to1500MG',    'QCD_HT100to200MG' ,     'QCD_HT1500to2000MG',    'QCD_HT2000toInfMG' ,    'QCD_HT200to300MG',    'QCD_HT300to500MG' ,    'QCD_HT500to700MG' ,    'QCD_HT50to100MG' ,    'QCD_HT700to1000MG' 'WJetsToLNu_NLO' ]

MC = ['GJets_HT-40To100', 'GJets_HT-100To200', 'GJets_HT-200To400','GJets_HT-400To600','GJets_HT-600ToInf', 'QCD_HT1000to1500MG',    'QCD_HT100to200MG' ,     'QCD_HT1500to2000MG',    'QCD_HT2000toInfMG' ,    'QCD_HT200to300MG',        'QCD_HT300to500MG' ,    'QCD_HT500to700MG' ,    'QCD_HT50to100MG' ,    'QCD_HT700to1000MG' , 'WJetsToLNu_NLO']

command = sys.argv[1]
if command.lower() == "merge" or command.lower()=='step1': 
    for year in years:
        if year == '2016all' : continue
	for channel in channels:
            for njet in Njet:
		if channel == "Gjets" :
                    #if '2018' in year: os.system("hadd -f scales_EGamma_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_EGamma_Run{0}*root".format(year, channel, njet))
                    if '2018' not in year: os.system("hadd -f scales_SinglePhoton_Run{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_all_SinglePhoton_Run{0}*root".format(year, channel, njet))
                    for mc in MC : 
                        #os.system("hadd -f scales_{3}_{0}_{1}_Njet{2}.root {1}_{0}/scales_Njet{2}_{3}_*{1}.root".format(year, channel, njet,mc))
                        os.system("python merge_histos.py {0} {1} {2}".format(mc, year, njet))



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


if command.lower() == "subtract" or command.lower() == 'step2': 
    for year in years:
	for channel in channels:
            for njet in Njet:
		if channel != "Gjets" : 
		    if channel == "MuMu" and 'pre' not in year : os.system("python extract2.py scales_SingleMuon_Run{0}_{1}_Njet{2}.root {1} {0} ".format(year, channel, njet))
		    if channel == "ElEl" : 
			if year == "2017" or '2016' in year :os.system("python extract2.py scales_SingleElectron_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
			if year == "2018" :os.system("python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    os.system("python extract2.py scales_DYJetsToLLM50_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    os.system("python extract2.py scales_DYJetsToLLM50NLO_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))

		if channel == "Gjets" : 
		    if year == "2018" :
                        os.system("hadd -f weighted_scales_EGamma_Run{0}_{1}_Njet{2}.root scales_EGamma_Run{0}_{1}_Njet{2}.root weighted_mc_scales_QCD*_{0:s}_{1}_Njet{2}.root weighted_mc_scales_WJetsToLNu_NLO*_{0:s}_{1}_Njet{2}.root".format(year, channel, njet))
                    if year != "2018" :
                        os.system("hadd -f weighted_scales_SinglePhoton_Run{0}_{1}_Njet{2}.root scales_SinglePhoton_Run{0}_{1}_Njet{2}.root weighted_mc_scales_QCD*_{0:s}_{1}_Njet{2}.root weighted_mc_scales_WJetsToLNu_NLO*_{0:s}_{1}_Njet{2}.root".format(year, channel, njet))
                    os.system("hadd -f weighted_scales_GJetsHT{0}_{1}_Njet{2}.root weighted_mc_scales_GJets_HT-*_{0:s}_{1}_Njet{2}.root ".format(year, channel, njet))



if command.lower() == "extract" or command.lower() == 'step3': 
    for year in years:
	for channel in channels:
            for njet in Njet:
		if channel != "Gjets" : 
		    if channel == "MuMu" and 'pre' not in year : os.system("python extract2.py scales_SingleMuon_Run{0}_{1}_Njet{2}.root {1} {0} ".format(year, channel, njet))
		    if channel == "ElEl" : 
			if year == "2017" or '2016' in year :os.system("python extract2.py scales_SingleElectron_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
			if year == "2018" :os.system("python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    os.system("python extract2.py scales_DYJetsToLLM50_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		    os.system("python extract2.py scales_DYJetsToLLM50NLO_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet))
		if channel == "Gjets" : 
		    if year == "2018" :
                        print 'hi'
                        os.system("python extract2.py weighted_scales_EGamma_Run{0}_{1}_Njet{2}.root {0:s} {1:s} {1:s}_mc_sub".format(year, channel, njet))
                        os.system("python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {0:s} {1:s} {1:s}".format(year, channel, njet))
                        print "python extract2.py scales_EGamma_Run{0}_{1}_Njet{2}.root {0:s} {1:s} {1:s}_mc_sub".format(year, channel, njet)

		    if year != "2018" :
                        os.system("python extract2.py weighted_scales_SinglePhoton_Run{0}_{1}_Njet{2}.root {0} {1} {1}_mc_sub".format(year, channel, njet))
                        os.system("python extract2.py scales_SinglePhoton_Run{0}_{1}_Njet{2}.root {0} {1} {1}".format(year, channel, njet))
		    os.system("python extract2.py weighted_scales_GJetsHT{0}_{1}_Njet{2}.root {0:s} {1:s} {1:s}_mc_sub".format(year, channel, njet))

		    #for mc in MC : 
		    #	os.system("python extract2.py scales_{3}_{0}_{1}_Njet{2}.root {1} {0}".format(year, channel, njet, mc))
