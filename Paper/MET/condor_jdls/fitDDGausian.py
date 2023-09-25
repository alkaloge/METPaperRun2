import ROOT
from ROOT import TLatex, TPad, TH1
ROOT.gROOT.SetBatch(True)

import CMS_lumi, tdrstyle, sys, os
from array import array

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

# 
# Simple example of macro: plot with CMS name and lumi text
#  (this script does not pretend to work in all configurations)
# iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV) 
# For instance: 
#               iPeriod = 3 means: 7 TeV + 8 TeV
#               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV 
#               iPeriod = 0 means: free form (uses lumi_sqrtS)
# Initiated by: Gautier Hamel de Monchenault (Saclay)
# Translated in Python by: Joshua Hardenbrook (Princeton)
# Updated by:   Dinko Ferencek (Rutgers)
#



# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref


iPeriod = 9
filenameData = sys.argv[1]
filenameBkg = sys.argv[2]
#python extract.py filename ismc MuMu 2018 dy

channel='MuMu'

year = str(sys.argv[3])
channel = str(sys.argv[4])
channelDir = str(sys.argv[5])


lumi=1.
if year == "2017 ": lumi = 41.48
if year == "2018":  lumi = 59.83
if year == "2016":  lumi = 19.35
if year == "2016all":  lumi = 19.35+16.98
if year == "2016postVFP": lumi = 16.98
if year == "2016preVFP": lumi = 19.35


print "year", year, "lumi", lumi, "channel", channel, "channelDir", channelDir, "args", sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]


# Define the cuts for vspt and npv
cuts_vspt = [
    #"(0<=boson_pt",
    "(0<=boson_pt&&boson_pt<20)",
    "(20<=boson_pt&&boson_pt<40)",
    "(40<=boson_pt&&boson_pt<60)",
    "(60<=boson_pt&&boson_pt<80)",
    "(80<=boson_pt&&boson_pt<100)",
    "(100<=boson_pt&&boson_pt<120)",
    "(120<=boson_pt&&boson_pt<160)",
    "(160<=boson_pt&&boson_pt<200)",
    "(200<=boson_pt&&boson_pt<300)",
    "(300<=boson_pt)"
]
folder_names = {
    #"(0<=event.boson_pt)": "PtIncl",
    "(0<=event.boson_pt and event.boson_pt<20)": "PtLt20",
    "(20<=event.boson_pt and event.boson_pt<40)": "PtGt20Lt40",
    "(40<=event.boson_pt and event.boson_pt<60)": "PtGt40Lt60",
    "(60<=event.boson_pt and event.boson_pt<80)": "PtGt60Lt80",
    "(80<=event.boson_pt and event.boson_pt<100)": "PtGt80Lt100",
    "(100<=event.boson_pt and event.boson_pt<120)": "PtGt100Lt120",
    "(120<=event.boson_pt and event.boson_pt<160)": "PtGt120Lt160",
    "(160<=event.boson_pt and event.boson_pt<200)": "PtGt160Lt200",
    "(200<=event.boson_pt and event.boson_pt<300)": "PtGt200Lt300",
    "(300<=event.boson_pt)": "PtGt300"
}
'''
folder_names = {
    0: "PtIncl",
    1: "PtLt20",
    2: "PtGt20Lt40",
    3: "PtGt40Lt60",
    4: "PtGt60Lt80",
    5: "PtGt80Lt100",
    6: "PtGt100Lt120",
    7: "PtGt120Lt160",
    8: "PtGt160Lt200",
    9: "PtGt200Lt300",
    10: "PtGt300"
}
'''
folder_names = {
    0: "PtLt20",
    1: "PtGt20Lt40",
    2: "PtGt40Lt60",
    3: "PtGt60Lt80",
    4: "PtGt80Lt100",
    5: "PtGt100Lt120",
    6: "PtGt120Lt160",
    7: "PtGt160Lt200",
    8: "PtGt200Lt300",
    9: "PtGt300"
}

cuts_npv = [
    #"(0<=nPVGood)",
    "(0<=nPVGood&&nPVGood<10)",
    "(10<=nPVGood&&nPVGood<20)",
    "(20<=nPVGood&&nPVGood<30)",
    "(30<=nPVGood&&nPVGood<40)",
    "(40<=nPVGood&&nPVGood<50)",
    "(50<=nPVGood&&nPVGood<60)",
    "(60<=nPVGood)"
]
folder_names_npv = {
    0: "nPVGoodLt10",
    1: "nPVGoodGt10Lt20",
    2: "nPVGoodGt20Lt30",
    3: "nPVGoodGt30Lt40",
    4: "nPVGoodGt40Lt50",
    5: "nPVGoodGt50Lt60",
    6: "nPVGoodGt60"
}


varbins = array('d', [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.])
bins = len(varbins) - 1


varbins_npv = array('d', [0., 10., 20., 30., 40., 50., 60., 70.])
#varbins_npv = array('d', [0., 10., 20., 30., 40., 100.])
bins_npv = len(varbins_npv) - 1


file_data = ROOT.TFile(filenameData, "READ")
file_bkg = ROOT.TFile(filenameBkg, "READ")
sjets='njetsgeq0'
if 'eq0' in filenameData : sjets = 'njetseq0'
if 'eq1' in filenameData : sjets = 'njetseq1'
if 'geq1' in filenameData : sjets = 'njetsgeq1'
if 'incl' in filenameData : sjets = 'njetsincl'

'''
# Open the data, background1, and background2 ROOT files

# Get histograms from the ROOT files (replace with actual histogram names)
hist_data = file_data.Get("Folder_5_vspt_PtGt100Lt120/h_uparaboson_puppi_vspt_5")
hist_bkg1 = file_bkg1.Get("Folder_5_vspt_PtGt100Lt120/h_uparaboson_puppi_vspt_5")
hist_bkg1.Scale(-1)

for i in range(1,hist_bkg1.GetNbinsX()+1):
    if hist_bkg1.GetBinContent(i) < 0 : 
        hist_bkg1.SetBinContent(i,0)
        hist_bkg1.SetBinError(i,0)
    #if hist_bkg2.GetBinContent(i) < 0 : 
    #    hist_bkg2.SetBinContent(i,0)
    #    hist_bkg2.SetBinError(i,0)

sjets='njetsgeq0'
if 'eq0' in filename : sjets = 'njetseq0'
if 'eq1' in filename : sjets = 'njetseq1'
if 'geq1' in filename : sjets = 'njetsgeq1'
if 'incl' in filename : sjets = 'njetsincl'
#channel='MuMu'

#year='2018'
dataVsPtFileName = "alldata_vspt_"+sjets+"_"+channel+".txt"
dataVsNvtxFileName = "alldata_npv_"+sjets+"_"+channel+".txt"
mcVsPtFileName = "dy_vspt_"+sjets+"_"+channel+".txt"
mcVsNvtxFileName = "dy_npv_"+sjets+"_"+channel+".txt"
if 'Gjets' not in channel: 
    if isMC : 
	dataVsPtFileName = dataVsPtFileName.replace("alldata", "dy")
	dataVsNvtxFileName = dataVsNvtxFileName.replace("alldata", "dy")

    if isMC and 'nlo' in str(filename).lower(): 
	dataVsPtFileName = dataVsPtFileName.replace("alldata", "dynlo")
	dataVsNvtxFileName = dataVsNvtxFileName.replace("alldata", "dynlo")
	dataVsPtFileName = dataVsPtFileName.replace("dy", "dynlo")
	dataVsNvtxFileName = dataVsNvtxFileName.replace("dy", "dynlo")
if 'Gjets' in channel: 
    if isMC : 
	dataVsPtFileName = dataVsPtFileName.replace("alldata", "Gjets")
	dataVsNvtxFileName = dataVsNvtxFileName.replace("alldata", "Gjets")
	mcVsPtFileName = mcVsPtFileName.replace("dy", "Gjets")
	mcVsNvtxFileName = mcVsNvtxFileName.replace("dy", "Gjets")


outrawmetd = open("txt_"+channelDir+"/rawmet_" + year + "_" + dataVsPtFileName, "w")
outrawpuppid = open("txt_"+channelDir+"/rawpuppi_" + year + "_" + dataVsPtFileName, "w")
outt1d = open("txt_"+channelDir+"/t1_" + year + "_" + dataVsPtFileName, "w")
outt1smeard = open("txt_"+channelDir+"/t1smear_" + year + "_" + dataVsPtFileName, "w")
outpuppid = open("txt_"+channelDir+"/puppi_" + year + "_" + dataVsPtFileName, "w")


outrawmetdn = open("txt_"+channelDir+"/rawmet_" + year + "_" + dataVsNvtxFileName, "w")
outrawpuppidn = open("txt_"+channelDir+"/rawpuppi_" + year + "_" + dataVsNvtxFileName, "w")
outt1dn = open("txt_"+channelDir+"/t1_" + year + "_" + dataVsNvtxFileName, "w")
outt1smeardn = open("txt_"+channelDir+"/t1smear_" + year + "_" + dataVsNvtxFileName, "w")
outpuppidn = open("txt_"+channelDir+"/puppi_" + year + "_" + dataVsNvtxFileName, "w")



'''

# Get the top directory of the ROOT file
top_directory_data = file_data.GetDirectory("")
top_directory_bkg = file_bkg.GetDirectory("")

histo_names = [
    "h_scale_rawmet",
    "h_scale_rawpuppi",
    "h_scale_t1",
    "h_scale_t1smear",
    "h_scale_puppi",
    "h_scale_perp_rawmet",
    "h_scale_perp_rawpuppi",
    "h_scale_perp_t1",
    "h_scale_perp_t1smear",
    "h_scale_perp_puppi",
    "h_upara_rawmet",
    "h_uparaboson_rawmet",
    "h_upara_rawpuppi",
    "h_uparaboson_rawpuppi",
    "h_upara_t1",
    "h_uparaboson_t1",
    "h_upara_t1smear",
    "h_uparaboson_t1smear",
    "h_upara_puppi",
    "h_uparaboson_puppi",
    "h_uperp_rawmet",
    "h_uperp_rawpuppi",
    "h_uperp_t1",
    "h_uperp_t1smear",
    "h_uperp_puppi"
]

# Define the list of histograms
h_data = []
h_bkg = []





for i, cut in enumerate(cuts_vspt):
    
    if str(i) == "0" : continue
    if str(i) == "1" : continue
    folder_name = "Folder_%d_vspt_%s" % (i, folder_names[i])
    print '......................', folder_name
    folder_data = top_directory_data.GetDirectory(folder_name)
    folder_bkg = top_directory_bkg.GetDirectory(folder_name)
    #file.ls()
    #top_directory.ls()
    
    if folder_data:
        for name in histo_names:
                h =folder_data.Get("{}_vspt_{}".format(name, i))
                if h :
		    hname=  h.GetName() + folder_names[i]
                    hname = hname.replace('_vspt_'+str(i), '_vspt_')
		    h.SetName( hname)
		    print h.GetName()
		    h_data.append(h)
    if folder_bkg:
        for name in histo_names:
                h=folder_bkg.Get("{}_vspt_{}".format(name, i))
                if h : 
		    hname=  h.GetName() + folder_names[i]
                    hname = hname.replace('_vspt_'+str(i), '_vspt_')
                    if h.GetSumOfWeights()<-1. : h.Scale(-1)
		    h.SetName( hname)
		    h_bkg.append(h)

for i, cut in enumerate(cuts_npv):
    
    #if str(i) == "0" : continue
    #if str(i) == "1" : continue
    folder_name = "Folder_%d_npv_%s" % (i, folder_names_npv[i])
    print '......................', folder_name
    folder_data = top_directory_data.GetDirectory(folder_name)
    folder_bkg = top_directory_bkg.GetDirectory(folder_name)
    #file.ls()
    #top_directory.ls()
    

    
    if folder_data:
        for name in histo_names:
                h =folder_data.Get("{}_npv_{}".format(name, i))
                if h :
		    hname=  h.GetName() + folder_names_npv[i]
                    hname = hname.replace('_npv_'+str(i), '_npv_')
		    h.SetName( hname)
		    print h.GetName()
		    h_data.append(h)
    if folder_bkg:
        for name in histo_names:
                h=folder_bkg.Get("{}_npv_{}".format(name, i))
                if h : 
		    hname=  h.GetName() + folder_names_npv[i]
                    hname = hname.replace('_npv_'+str(i), '_npv_')
		    h.Scale(-1)
		    h.SetName( hname)
		    h_bkg.append(h)





print h_data

#sys.exit()



#canvas = ROOT.TCanvas("canvas", "Canvas", 800, 800)
canvas = ROOT.TCanvas("canvas","Canvas",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)


top_pad = ROOT.TPad("top_pad", "Top Pad", 0, 0.25, 1, 0.95)
top_pad.SetBottomMargin(0.05)  # Adjust the margin as needed
top_pad.SetLeftMargin(0.05)  # Adjust the margin as needed
top_pad.Draw()

# Create the bottom pad
bottom_pad = ROOT.TPad("bottom_pad", "Bottom Pad", 0, 0, 1, 0.24)
bottom_pad.SetTopMargin(0.02)  # Adjust the margin as needed
bottom_pad.SetBottomMargin(0.1)  # Adjust the margin as needed
bottom_pad.SetLeftMargin(0.05)  # Adjust the margin as needed
bottom_pad.Draw()


#canvas.Divide(1, 2)  # Divide the canvas into two pads

# First Pad (Top Pad) - Data and Fits


print 'check some facts', len(h_data), len(h_bkg)
#sys.exit()
counter=0

#for ih, hist_data in h_data:
for ih in range(len(h_data)):
    hist_data = h_data[ih]
    if hist_data:
	h_name = hist_data.GetName()
        #if 'boson' not in h_name : continue
        for ibk in range(len(h_bkg)):
            hist_bkg = h_bkg[ibk]
            savename = hist_bkg.GetName()
            #if not ('t1smear' in hist_bkg.GetName() and 't1_' in h_name): 
	    if ( 'scale' in hist_bkg.GetName() and 'scale' not in  h_name) : continue 
	    if ( 'para' in hist_bkg.GetName() and 'para' not in  h_name) : continue 
	    if ( 'perp' in hist_bkg.GetName() and 'perp' not in  h_name) : continue 

	    #if  't1' in h_name and 't1smear' in hist_bkg.GetName():
            #savename='t1s
           
            if 'vspt' in h_name and 'vspt' not in hist_bkg.GetName() : continue
            if 'npv' in h_name and 'npv' not in hist_bkg.GetName() : continue
            if 'puppi' in h_name and 'puppi' not in hist_bkg.GetName() : continue
            if 'perp' in h_name and 'perp' not in hist_bkg.GetName() : continue
            if 'paraboson' in h_name and 'paraboson' not in hist_bkg.GetName() : continue
            if 'rawmet' in h_name and 'rawmet' not in hist_bkg.GetName() : continue
            if 'rawpuppimet' in h_name and 'rawpuppimet' not in hist_bkg.GetName() : continue
            if 't1' in h_name and not ('t1' in hist_bkg.GetName() or 't1smear' in hist_bkg.GetName()): continue
            #    savename = h_name.replace('t1', 't1smear')    

	    #if (savename != h_name) : continue
            #if 'npv' not in h_name : continue
	    if (hist_bkg.GetName() != h_name) : continue
	    pngname = "fit_result_{}_{}_{}_{}.png".format(savename,sjets, channel,year)
	    pdfname = "fit_result_{}_{}_{}_{}.pdf".format(savename,sjets, channel,year)
	    print 'check on the names', h_name, hist_bkg.GetName(), savename
	    counter+=1
	    #if counter>100 : sys.exit()
	    for ib in range(1, hist_bkg.GetNbinsX()+1) :
		if hist_bkg.GetBinContent(ib) > hist_data.GetBinContent(ib) :
		    #print 'yes, found a problematic bin here....', hist_data.GetName(), ib, hist_data.GetBinContent(ib), hist_bkg.GetBinContent(ib)
		    hist_bkg.SetBinContent(ib, 0.2 * hist_data.GetBinContent(ib))
		    hist_bkg.SetBinError(ib, 2* hist_data.GetBinError(ib))
	    # Create a histogram for data-bkg distribution
	    hist_data_minus_bkg = hist_data.Clone()
	    hist_data_minus_bkg.Add(hist_bkg, -1)
	    hist_data_minus_bkg.SetLineColor(ROOT.kRed)
	    #hist_data_minus_bkg.Add(hist_bkg2, -1)
	    top_pad.Clear()
	    top_pad.Draw()
	    top_pad.cd()

	    # Fit data with a Gaussian (red)
	    #fit_data = hist_data.Fit("gaus", "SO", "", -100, 100)
	    hist_data.SetLineColor(ROOT.kBlue)
	    hist_data.SetLineWidth(2)
	    hist_data.SetMinimum(0)
	    hist_data.GetXaxis().SetRangeUser(-3,3)
	    if 'scale'  not in pngname :  hist_data.GetXaxis().SetRangeUser(-100,100)
	    hist_data.Draw()

	    #fit_data.Draw("same")  # Draw fit line for data (red)
	    # Plot bkg+bkg2 (green dashed)
	    hist_bkg_plus_bkg2 = hist_bkg.Clone()
	    #hist_bkg_plus_bkg2.Add(hist_bkg2)
	    hist_bkg_plus_bkg2.SetLineStyle(2)
	    hist_bkg_plus_bkg2.SetLineColor(ROOT.kGreen-1)
	    hist_bkg_plus_bkg2.SetMarkerColor(ROOT.kGreen-1)
	    hist_bkg_plus_bkg2.Draw("  same")  # Draw bkg+bkg2 (green dashed)
	    #hist_bkg_plus_bkg2.Draw(" L hist same")  # Draw bkg+bkg2 (green dashed)
	    #fit_func=None
	    #hist_data_minus_bkg=None
	    if 'scale' not in pngname : 
		fit_func = ROOT.TF1("fit_func", "gaus", -100, 100)
		#hist_data_minus_bkg_fit =hist_data_minus_bkg.Clone() 
		hist_data_minus_bkg.Fit("gaus", "","SAME",-100,100)
	    else : 
		fit_func = ROOT.TF1("fit_func", "gaus", -5, 5)
		#hist_data_minus_bkg_fit =hist_data_minus_bkg.Clone() 
		hist_data_minus_bkg.Fit("gaus", "","SAME",-3,3)

	    hist_data_minus_bkg.Fit(fit_func, "R")
	    mean = fit_func.GetParameter(1)
	    sigma = fit_func.GetParameter(2)
	    mean_error = fit_func.GetParError(1)
	    sigma_error = fit_func.GetParError(2)

	    #hist_data_minus_bkg.Fit(fitFunc, "SAME");
	    #ahist_data_minus_bkg.Fit(fit_func, "SAME")

	    # Fit data-bkg distribution with a Gaussian (blue)
	    #hist_data_minus_bkg = hist_data_minus_bkg.Clone()
	    #fit_data_minus_bkg = hist_data_minus_bkg.Fit("gaus", "","SAME")
	    #fit_data_minus_bkg_copy = hist_data.Fit("gaus", "S", "", -100, 100)

	    #hist_data.Draw()
	    #hist_data_minus_bkg.SetLineWidth(2)
	    #hist_data_minus_bkg.Draw(" hist same")
	    #fit_data_minus_bkg.Draw("same hist")  # Draw fit line for data-bkg (blue)

	    # Hide the entries, mean, and standard deviation
	    hist_data_minus_bkg.SetStats(0)
	    hist_data.SetStats(0)

	    #top_pad.Update()

	    # Add a TPaveText for displaying fit parameters
	    param_text = ROOT.TPaveText(0.75, 0.6, 0.9, 0.85, "NDC")
	    param_text.SetTextSize(0.04)
	    param_text.SetFillColor(0)
	    pname = ' 40 < q_{T} < 60 GeV'
	    if 'PtGt60' in hist_data.GetName() : pname = ' 60 < q_{T} < 80 GeV'
	    if 'PtGt80' in hist_data.GetName() : pname = ' 80 < q_{T} < 100 GeV'
	    if 'PtGt100' in hist_data.GetName() : pname = ' 100 < q_{T} < 120 GeV'
	    if 'PtGt120' in hist_data.GetName() : pname = ' 120 < q_{T} < 160 GeV'
	    if 'PtGt160' in hist_data.GetName() : pname = ' 160 < q_{T} < 200 GeV'
	    if 'PtGt200' in hist_data.GetName() : pname = ' 200 < q_{T} < 300 GeV'
	    if 'PtGt300' in hist_data.GetName() : pname = ' q_{T} > 300 GeV'

	    if 'PVGoodLt10' in hist_data.GetName() : pname = ' nVtx < 10 '
	    if 'PVGoodGt10Lt' in hist_data.GetName() : pname = ' 10 < nVtx < 20 '
	    if 'PVGoodGt20Lt' in hist_data.GetName() : pname = ' 20 < nVtx < 30 '
	    if 'PVGoodGt30Lt' in hist_data.GetName() : pname = ' 30 < nVtx < 40 '
	    if 'PVGoodGt40' in hist_data.GetName() : pname = ' 40 < nVtx < 50 '
	    if 'PVGoodGt50' in hist_data.GetName() : pname = ' 50 < nVtx < 60 '
	    if 'PVGoodGt60' in hist_data.GetName() : pname = ' nVtx > 60'

	    #param_text.AddText("{}".format(pname))
	    param_text.AddText("#gamma+jets, {}".format(pname))
	    param_text.AddText("Fit Parameters:")
	    param_text.AddText("Data-Bkg Gaussian:")
	    param_text.AddText("#mu: {:.2f} #pm {:.2f}".format(mean, mean_error))
	    param_text.AddText("#sigma: {:.2f} #pm {:.2f}".format(sigma ,sigma_error))
	    #param_text.AddText("Data Gaussian:")
	    #param_text.AddText("Mean: %.2f" % fit_data.Get().Parameter(1))
	    #param_text.AddText("Sigma: %.2f" % fit_data.Get().Parameter(2))
	    param_text.Draw("same")
	    legend = ROOT.TLegend(0.75, 0.2, 0.9, 0.5)  # Define the legend position

	    # Add entries to the legend
	    legend.SetFillStyle(0)  # 0 means transparent
	    legend.SetBorderSize(0)  # 0 means no border
	    legend.SetTextSize(0.04)  # Adjust the size as needed
	    legend.AddEntry(hist_data, "Data", "lp")
	    legend.AddEntry(hist_data_minus_bkg, "Data-Bkg", "lp")
	    legend.AddEntry(hist_bkg_plus_bkg2, "Total background", "lp")

	    # Draw the legend
	    legend.Draw()

	    
	    # Second Pad (Bottom Pad) - Pulls
	    bottom_pad.Clear()
	    bottom_pad.Draw()
	    bottom_pad.cd()


	    # Calculate the pulls (data - (bkg1+bkg2)) / data errors
	    hist_data_minus_bkg.GetXaxis().SetRangeUser(-3,3)
	    if 'scale' not in pngname : hist_data_minus_bkg.GetXaxis().SetRangeUser(-100,100)
	    hist_pulls = hist_data_minus_bkg.Clone()
	    hist_pulls.Divide(hist_data)

	    latexd = TLatex()
	    latexd.SetNDC();
	    latexd.SetTextAngle(90);
	    latexd.SetTextColor(ROOT.kBlack);
	    latexd.SetTextFont(42);
	    latexd.SetTextAlign(31);
	    latexd.SetTextSize(0.06);
	    latexd.DrawLatex(0.059, 0.93, "Events / GeV")
	    bottom_pad.Update()
	    canvas.Modified()
	    canvas.Update()
		# Create a TGraphErrors from the pulls histogram
	    num_bins = hist_pulls.GetNbinsX()
	    pulls_graph = ROOT.TGraphErrors(num_bins)
	    for i in range(1, num_bins + 1):
		x = hist_pulls.GetBinCenter(i)
		y = hist_pulls.GetBinContent(i)
		ey = hist_pulls.GetBinError(i)
		pulls_graph.SetPoint(i - 1, x, y)
		pulls_graph.SetPointError(i - 1, 0, ey)

	    pulls_graph.SetMarkerStyle(20)
	    pulls_graph.SetMinimum(-6)
	    pulls_graph.SetMaximum(6)
	    pulls_graph.GetXaxis().SetRangeUser(-3,3)

	    pulls_graph.GetYaxis().SetTitle("Pulls")
	    pulls_graph.GetYaxis().SetTitleSize(0.1)  # Adjust the size as needed
	    pulls_graph.GetYaxis().CenterTitle();
	    pulls_graph.GetYaxis().SetLabelSize(0.11);
	    #pulls_graph.GetYaxis().SetNdivisions(44);
	    pulls_graph.GetXaxis().SetTitleSize(0.135);
	    pulls_graph.GetXaxis().SetLabelSize(0.11);
	    pulls_graph.GetYaxis().SetTitleOffset(0.2);

	    if 'scale' not in pngname : pulls_graph.GetXaxis().SetRangeUser(-100,100)

	    pulls_graph.Draw("AP")  # Draw the pulls as a TGraphErrors

	    iPeriod=str(year)
	    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

	    canvas.cd()
	    canvas.Update()
	    canvas.RedrawAxis()
	    frame = canvas.GetFrame()
	    frame.Draw()


	    #update the canvas to draw the legend
	    canvas.Update()

	    #canvas.SaveAs(pngname)
	    canvas.SaveAs(pdfname)
	    del param_text
	    del legend


