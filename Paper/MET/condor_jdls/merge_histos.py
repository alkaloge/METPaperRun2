import ROOT
import os
import sys
def scale_histos( mc_fileName, weight):
    mc_file = ROOT.TFile.Open(mc_fileName, "READ")
    ofile = 'weighted_mc_'+mc_fileName
    w_mc_file = ROOT.TFile.Open(ofile, "recreate")

    for folder_key in mc_file.GetListOfKeys():
        folder_name = folder_key.GetName()
        if not mc_file.Get(folder_name).InheritsFrom("TDirectory"):
            continue
        
        mc_folder = mc_file.Get(folder_name)
        w_mc_file.mkdir(folder_name)
        print 'working', folder_name, weight

        for histo_key in mc_folder.GetListOfKeys():
            histo_name = histo_key.GetName()
            if not mc_folder.Get(histo_name).InheritsFrom("TH1"):
                continue
            #print 'getting', histo_name
            mc_histo = mc_folder.Get(histo_name)
            
            if not mc_histo:
                print "WARNING: Histogram {histo_name} not found in MC file."
                continue

            #if haisto_name in weight_dictionary:
            #weight = weight_dictionary[histo_name]
            #print 'will subtract', mc_histo.GetName(),  mc_histo.GetSumOfWeights(), mc_fileName
            scale_factor = float(weight)
            mc_histo.Scale(scale_factor)
            #print 'just subtracted', mc_histo.GetName(), mc_histo.GetSumOfWeights()
            w_mc_file.cd(folder_name)
            mc_histo.Write()
            
            
    w_mc_file.Write()
    mc_file.Close()

# Example usage:
lumis={'2016':35.93, '2017':41.48, '2018':59.83}
#MC = ['GJets_HT-40To100', 'GJets_HT-100To200', 'GJets_HT-200To400','GJets_HT-400To600','GJets_HT-600ToInf', 'QCD_HT1000to1500',    'QCD_HT100to200' ,     'QCD_HT1500to2000',    'QCD_HT2000toInf' ,    'QCD_HT200to300',    'QCD_HT300to500' ,    'QCD_HT500to700' ,    'QCD_HT50to100' ,    'QCD_HT700to1000' , 'WJetsToLNu_NLO']
MC = ['GJets_HT-40To100', 'GJets_HT-100To200', 'GJets_HT-200To400','GJets_HT-400To600','GJets_HT-600ToInf', 'QCD_HT1000to1500MG',    'QCD_HT100to200MG' ,     'QCD_HT1500to2000MG',    'QCD_HT2000toInfMG' ,    'QCD_HT200to300MG',    'QCD_HT300to500MG' ,    'QCD_HT500to700MG' ,    'QCD_HT50to100MG' ,    'QCD_HT700to1000MG' , 'WJetsToLNu_NLO']

#MC = ['QCD_HT500to700MG']

Njet=['eq1', 'geq1', 'incl']


xsecslist = {
    "DYJets": 6077,
    "DYJetsNLO": 6529,
    'GJets_HT-100To200' : 9226.0,
    'GJets_HT-200To400' : 2300.0,
    'GJets_HT-400To600' : 277.0,
    'GJets_HT-40To100' : 20730.0,
    'GJets_HT-600ToInf' : 93.38,
    'QCD_HT1000to1500' : 1206.0,
    'QCD_HT1000to1500MG' : 1206.0,
    'QCD_HT100to200' : 27990000.0,
    'QCD_HT100to200MG' : 27990000.0,
    'QCD_HT1500to2000' : 119.9,
    'QCD_HT1500to2000MG' : 119.9,
    'QCD_HT2000toInf' : 25.24,
    'QCD_HT2000toInfMG' : 25.24,
    'QCD_HT200to300' : 1735000.0,
    'QCD_HT200to300MG' : 1735000.0,
    'QCD_HT300to500' : 366800.0,
    'QCD_HT300to500MG' : 366800.0,
    'QCD_HT500to700' : 31630.0,
    'QCD_HT500to700MG' : 31630.0,
    'QCD_HT50to100' : 186100000.0,
    'QCD_HT50to100MG' : 186100000.0,
    'QCD_HT700to1000' : 6802.0,
    'QCD_HT700to1000MG' : 6802.0,
    'ST_s-channel' : 3.74,
    'ST_t-channel_antitop' : 69.09,
    'ST_t-channel_top' : 115.3,
    'ST_tW_antitop' : 35.85,
    'ST_tW_top' : 35.85,
    'TGjets' : 2.967,
    'TTGjets' : 4.322,
    'TTGjets_ext1' : 4.322,
    'TTTo2L2Nu' : 88.287,
    'TTToHadronic' : 377.96,
    'TTToSemiLeptonic' : 365.35,
    'ttWJets' : 0.4611,
    'WG_PtG-130' : 0.8099,
    'WG_PtG-40To130' : 19.81,
    'WGToLNuG' : 489.0,
    'WJetsToLNu_NLO' : 67350.7,
    'ZGTo2NuG' : 30.11,
    'ZLLGJets_PtG-130' : 0.206,
    'ZLLGJets_PtG-15to130' : 96.34,
    'ZNuNuGJets_PtG-130' : 0.3036,
}


weights_2018  = { 'GJets_HT-100To200' : 31722998.0, 'GJets_HT-200To400' : 62439148.0, 'GJets_HT-400To600' : 16896943.0, 'GJets_HT-40To100' : 30564375.0,
    'GJets_HT-600ToInf' : 16621072.0,
    'QCD_HT1000to1500MG' : 15230975.0,
    'QCD_HT100to200MG' : 79857456.0,
    'QCD_HT1500to2000MG' : 11887406.0,
    'QCD_HT2000toInfMG' : 5710430.0,
    'QCD_HT200to300MG' : 61542214.0,
    'QCD_HT300to500MG' : 56214199.0,
    'QCD_HT500to700MG' : 61097673.0,
    'QCD_HT50to100MG' : 38521609.0,
    'QCD_HT700to1000MG' : 46800611.0,
    'TGjets' : 5909442.20158,
    'TTGjets' : 27849498.8651,
    'TTGjets_ext1' : 37406821.5573,
    'WG_PtG-130' : 4966262.0,
    'WG_PtG-40To130' : 4764595.0,
    'WGToLNuG' : 9850083.0,
    'WJetsToLNu_NLO' : 5.01811676681e+12,
    'ZGTo2NuG' : 200709536.233,
    'ZLLGJets_PtG-130' : 204929.638267,
    'ZLLGJets_PtG-15to130' : 7322772437.29,
    'ZNuNuGJets_PtG-130' : 989122.179502,
}

weights_2017={
    'GJets_HT-600ToInf' : 11425129.0,
    'ZLLGJets_PtG-130' : 204859.098256,
    'GJets_HT-100To200' : 23353502.0,
    'TTGjets' : 22157556.6335,
    'GJets_HT-40To100' : 21764861.0,
    'TGjets' : 5958486.17214,
    'WG_PtG-40To130' : 3598774.0,
    'QCD_HT50to100MG' : 39819368.0,
    'GJets_HT-400To600' : 11970409.0,
    'QCD_HT2000toInfMG' : 5614050.0,
    'WGToLNuG' : 10302104.0,
    'QCD_HT300to500MG' : 54770756.0,
    'ZLLGJets_PtG-15to130' : 7483331784.42,
    'ZNuNuGJets_PtG-130' : 855429.958555,
    'WG_PtG-130' : 3609634.0,
    'QCD_HT500to700MG' : 60395873.0,
    'ZGTo2NuG' : 137853651.468,
    'QCD_HT1000to1500MG' : 14164109.0,
    'QCD_HT200to300MG' : 60056309.0,
    'QCD_HT1500to2000MG' : 12402197.0,
    'QCD_HT100to200MG' : 80534025.0,
    'QCD_HT700to1000MG' : 47501834.0,
    'GJets_HT-200To400' : 54956719.0,
    'WWG' : 587295.22633,
    'WJetsToLNu_NLO' : 4.55989376573e+12,
}

weights_2016={
    'GJets_HT-600ToInf' : 4040799.0,
    'ZLLGJets_PtG-130' : 94716.3262457,
    'GJets_HT-100To200' : 9624073.0,
    'TTGjets' : 8868805.09113,
    'GJets_HT-40To100' : 7058610.0,
    'TGjets' : 2382046.6503,
    'WG_PtG-40To130' : 1386165.0,
    'QCD_HT50to100MG' : 35474117.0,
    'GJets_HT-400To600' : 4475962.0,
    'QCD_HT2000toInfMG' : 4867995.0,
    'WGToLNuG' : 8394172.0,
    'QCD_HT300to500MG' : 46335846.0,
    'ZLLGJets_PtG-15to130' : 3535049435.11,
    'ZNuNuGJets_PtG-130' : 246659.88616,
    'WG_PtG-130' : 1330669.0,
    'QCD_HT500to700MG' : 52661606.0,
    'ZGTo2NuG' : 137853651.468,
    'QCD_HT1000to1500MG' : 12254238.0,
    'QCD_HT200to300MG' : 43280518.0,
    'QCD_HT1500to2000MG' : 9376965.0,
    'QCD_HT100to200MG' : 73506112.0,
    'QCD_HT700to1000MG' : 41664730.0,
    'GJets_HT-200To400' : 18315845.0,
    'WWG' : 236166.066732,
    'WJetsToLNu_NLO' : 4.87296446076e+12,




}

weights_2016preVFP={
    'GJets_HT-600ToInf' : 4624766.0,
    'ZLLGJets_PtG-130' : 100290.441495,
    'GJets_HT-100To200' : 8461618.0,
    'TTGjets' : 9472781.7663,
    'GJets_HT-40To100' : 8246771.0,
    'TGjets' : 2964755.52092,
    'WG_PtG-40To130' : 1603255.0,
    'QCD_HT50to100MG' : 36599034.0,
    'GJets_HT-400To600' : 4338294.0,
    'QCD_HT2000toInfMG' : 4996082.0,
    'WGToLNuG' : 9714707.0,
    'QCD_HT300to500MG' : 46608401.0,
    'ZLLGJets_PtG-15to130' : 3731179815.96,
    'ZNuNuGJets_PtG-130' : 227554.488435,
    'WG_PtG-130' : 1457339.0,
    'QCD_HT500to700MG' : 56868784.0,
    'ZGTo2NuG' : 67129487.2814,
    'QCD_HT1000to1500MG' : 13823774.0,
    'QCD_HT200to300MG' : 51897795.0,
    'QCD_HT1500to2000MG' : 9893688.0,
    'QCD_HT100to200MG' : 67431856.0,
    'QCD_HT700to1000MG' : 40442876.0,
    'GJets_HT-200To400' : 19037560.0,
    'WWG' : 270688.411372,
    'WJetsToLNu_NLO' : 4.98951935909e+12,


}

mc=str(sys.argv[1])
year=str(sys.argv[2])
njet=str(sys.argv[3])

weights_ =weights_2018
if year=='2017' : weights_ = weights_2017
if year=='2016' : weights_ = weights_2016
if year=='2016preVFP' : weights_ = weights_2016preVFP
#for sample, xsec in xsecslist.items():
#    if 'QCD' in sample : 
#        print sample, xsec


w_ = float(xsecslist[mc]*lumis[year]*1000./weights_[mc])
if 'GJets' not in mc : w_ *=-1.
mc_file_path = "scales_{0:s}_{1:s}_Gjets_Njet{2:s}.root".format(mc, year, njet)
print 'will try', mc, 'xsec= ', xsecslist[mc], 'w= ', weights_[mc], 'njet', njet
print mc_file_path, mc, 'xsec= ', xsecslist[mc], 'w= ', weights_[mc],  'lumi', lumis[year] , 'tot_w', xsecslist[mc]*lumis[year]*1000/weights_[mc], "scaled to ", w_
scale_histos(mc_file_path, w_)

'''
for njet in Njet : 

    for mc in MC : 
	print mc, 'xsec= ', xsecslist[mc], 'w= ', weights_[mc],  'lumi', lumis[year] , 'tot_w', xsecslist[mc]*lumis[year]*1000/weights_[mc]
        w_ = xsecslist[mc]*lumis[year]*1000/weights_[mc]
	mc_file_path = "scales_{0:s}_{1:s}_Gjets_Njet{2:s}.root".format(mc, year, njet)
	scale_histos(mc_file_path, w_)
'''

