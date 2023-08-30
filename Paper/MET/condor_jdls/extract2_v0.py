import ROOT
from array import array
from ROOT import TH1, TH1F, TFile
import sys, os

filename = sys.argv[1]
#python extract.py filename ismc MuMu 2018 dy

isMC=True
channel='MuMu'
if "run20" in str(filename).lower() : isMC = False

#if str(sys.argv[1]) == "1"  or str(sys.argv[1]).lower()  == "ismc" :  isMC = True
channel = str(sys.argv[2])
year = str(sys.argv[3])


lumi=1.
if year == "2017 ": lumi = 41.48

if year == "2018":  lumi = 59.83
if year == "2016":  lumi = 19.35
if year == "2016postVFP": lumi = 16.98
if year == "2016preVFP": lumi = 19.35

xsecslist = {
"DYJets": 6077,
}


xsec = None
for sample, xsec in xsecslist.items():
    if str(filename).lower() in sample.lower():
	selected_xsec = xsec
	break



print "year", year, "lumi", lumi, "isMC", "channel", channel, "xsec", xsec



# Open the ROOT file
file = ROOT.TFile(filename, "READ")
hW = None
if isMC :
    hW = file.Get("hWeights") 


# Define the cuts for vspt and npv
cuts_vspt = [
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

cuts_npv = [
    "(0<=nPVGood&&nPVGood<10)",
    "(10<=nPVGood&&nPVGood<20)",
    "(20<=nPVGood&&nPVGood<30)",
    "(30<=nPVGood&&nPVGood<40)",
    "(40<=nPVGood&&nPVGood<50)",
    "(50<=nPVGood&&nPVGood<60)",
    "(60<=nPVGood)"
]

varbins = array('d', [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.])
bins = len(varbins) - 1


varbins_npv = array('d', [0., 10., 20., 30., 40., 50., 60., 70.])
bins_npv = len(varbins_npv) - 1


# Create histograms for vspt and npv
h_scale0_rawmet_vspt = ROOT.TH1F("h_scale0_rawmet_vspt", "", bins, varbins)
h_upara_rawmet_vspt = ROOT.TH1F("h_upara_rawmet_vspt", "", bins, varbins)
h_uperp_rawmet_vspt = ROOT.TH1F("h_uperp_rawmet_vspt", "", bins, varbins)
h_scale0_rawpuppi_vspt = ROOT.TH1F("h_scale0_rawpuppi_vspt", "", bins, varbins)
h_upara_rawpuppi_vspt = ROOT.TH1F("h_upara_rawpuppi_vspt", "", bins, varbins)
h_uperp_rawpuppi_vspt = ROOT.TH1F("h_uperp_rawpuppi_vspt", "", bins, varbins)
h_scale0_t1_vspt = ROOT.TH1F("h_scale0_t1_vspt", "", bins, varbins)
h_upara_t1_vspt = ROOT.TH1F("h_upara_t1_vspt", "", bins, varbins)
h_uperp_t1_vspt = ROOT.TH1F("h_uperp_t1_vspt", "", bins, varbins)
h_scale0_t1smear_vspt = ROOT.TH1F("h_scale0_t1smear_vspt", "", bins, varbins)
h_upara_t1smear_vspt = ROOT.TH1F("h_upara_t1smear_vspt", "", bins, varbins)
h_uperp_t1smear_vspt = ROOT.TH1F("h_uperp_t1smear_vspt", "", bins, varbins)
h_scale0_puppi_vspt = ROOT.TH1F("h_scale0_puppi_vspt", "", bins, varbins)
h_upara_puppi_vspt = ROOT.TH1F("h_upara_puppi_vspt", "", bins, varbins)
h_uperp_puppi_vspt = ROOT.TH1F("h_uperp_puppi_vspt", "", bins, varbins)


h_scale0_rawmet_npv = ROOT.TH1F("h_scale0_rawmet_npv", "",bins_npv,varbins_npv)
h_upara_rawmet_npv = ROOT.TH1F("h_upara_rawmet_npv", "",bins_npv,varbins_npv)
h_uperp_rawmet_npv = ROOT.TH1F("h_uperp_rawmet_npv", "",bins_npv,varbins_npv)
h_scale0_rawpuppi_npv = ROOT.TH1F("h_scale0_rawpuppi_npv", "",bins_npv,varbins_npv)
h_upara_rawpuppi_npv = ROOT.TH1F("h_upara_rawpuppi_npv", "",bins_npv,varbins_npv)
h_uperp_rawpuppi_npv = ROOT.TH1F("h_uperp_rawpuppi_npv", "",bins_npv,varbins_npv)
h_scale0_t1_npv = ROOT.TH1F("h_scale0_t1_npv", "",bins_npv,varbins_npv)
h_upara_t1_npv = ROOT.TH1F("h_upara_t1_npv", "",bins_npv,varbins_npv)
h_uperp_t1_npv = ROOT.TH1F("h_uperp_t1_npv", "",bins_npv,varbins_npv)
h_scale0_t1smear_npv = ROOT.TH1F("h_scale0_t1smear_npv", "",bins_npv,varbins_npv)
h_upara_t1smear_npv = ROOT.TH1F("h_upara_t1smear_npv", "",bins_npv,varbins_npv)
h_uperp_t1smear_npv = ROOT.TH1F("h_uperp_t1smear_npv", "",bins_npv,varbins_npv)
h_scale0_puppi_npv = ROOT.TH1F("h_scale0_puppi_npv", "",bins_npv,varbins_npv)
h_upara_puppi_npv = ROOT.TH1F("h_upara_puppi_npv", "",bins_npv,varbins_npv)
h_uperp_puppi_npv = ROOT.TH1F("h_uperp_puppi_npv", "",bins_npv,varbins_npv)

sjets='njetsgeq0'
#channel='MuMu'
year='2018'
dataVsPtFileName = "alldata_vspt_"+sjets+"_"+channel+".txt"
dataVsNvtxFileName = "alldata_npv_"+sjets+"_"+channel+".txt"
mcVsPtFileName = "dy_vspt_"+sjets+"_"+channel+".txt"
mcVsNvtxFileName = "dy_npv_"+sjets+"_"+channel+".txt"

if isMC : dataVsPtFileName = dataVsPtFileName.replace("alldata", "dy")
if isMC : dataVsNvtxFileName = dataVsNvtxFileName.replace("alldata", "dy")

outrawmetd = open("rawmet_" + year + "_" + dataVsPtFileName, "w")
outrawpuppid = open("rawpuppi_" + year + "_" + dataVsPtFileName, "w")
outt1d = open("t1_" + year + "_" + dataVsPtFileName, "w")
outt1smeard = open("t1smear_" + year + "_" + dataVsPtFileName, "w")
outpuppid = open("puppi_" + year + "_" + dataVsPtFileName, "w")


outrawmetdn = open("rawmet_" + year + "_" + dataVsNvtxFileName, "w")
outrawpuppidn = open("rawpuppi_" + year + "_" + dataVsNvtxFileName, "w")
outt1dn = open("t1_" + year + "_" + dataVsNvtxFileName, "w")
outt1smeardn = open("t1smear_" + year + "_" + dataVsNvtxFileName, "w")
outpuppidn = open("puppi_" + year + "_" + dataVsNvtxFileName, "w")




# Get the top directory of the ROOT file
top_directory = file.GetDirectory("")

weight = 1.
if isMC : weight *= 1000* lumi*xsec/hW.GetSumOfWeights()

# Loop over vspt directories and fill the histogram
for i, cut in enumerate(cuts_vspt):
    
    folder_name = "Folder_{}_vspt".format(i)
    folder = top_directory.GetDirectory(folder_name)
    if folder:
        h_scale0_rawmet = folder.Get("h_scale0_rawmet_vspt_{}".format(i))
        h_scale0_rawpuppi = folder.Get("h_scale0_rawpuppi_vspt_{}".format(i))
        h_scale0_t1 = folder.Get("h_scale0_t1_vspt_{}".format(i))
        h_scale0_t1smear = folder.Get("h_scale0_t1smear_vspt_{}".format(i))
        h_scale0_puppi = folder.Get("h_scale0_puppi_vspt_{}".format(i))

        h_upara_rawmet = folder.Get("h_upara_rawmet_vspt_{}".format(i))
        h_upara_rawpuppi = folder.Get("h_upara_rawpuppi_vspt_{}".format(i))
        h_upara_t1 = folder.Get("h_upara_t1_vspt_{}".format(i))
        h_upara_t1smear = folder.Get("h_upara_t1smear_vspt_{}".format(i))
        h_upara_puppi = folder.Get("h_upara_puppi_vspt_{}".format(i))

        h_uperp_rawmet = folder.Get("h_uperp_rawmet_vspt_{}".format(i))
        h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi_vspt_{}".format(i))
        h_uperp_t1 = folder.Get("h_uperp_t1_vspt_{}".format(i))
        h_uperp_t1smear = folder.Get("h_uperp_t1smear_vspt_{}".format(i))
        h_uperp_puppi = folder.Get("h_uperp_puppi_vspt_{}".format(i))

        if isMC : 
            h_scale0_rawmet.Scale(weight)
            h_scale0_rawpuppi.Scale(weight)
            h_scale0_t1.Scale(weight)
            h_scale0_t1smear.Scale(weight)
            h_scale0_puppi.Scale(weight)
            h_upara_rawmet.Scale(weight)
            h_upara_rawpuppi.Scale(weight)
            h_upara_t1.Scale(weight)
            h_upara_t1smear.Scale(weight)
            h_upara_puppi.Scale(weight)
            h_uperp_rawmet.Scale(weight)
            h_uperp_rawpuppi.Scale(weight)
            h_uperp_t1.Scale(weight)
            h_uperp_t1smear.Scale(weight)
            h_uperp_puppi.Scale(weight)

        scalecor_rawmet = 1.0
        if h_scale0_rawmet.GetMean() != 0:
            scalecor_rawmet = 1.0 / h_scale0_rawmet.GetMean()
         
        scalecor_rawpuppi = 1.0
        if h_scale0_rawpuppi.GetMean() != 0:
            scalecor_rawpuppi = 1.0 / h_scale0_rawpuppi.GetMean()

        scalecor_t1 = 1.0
        if h_scale0_t1.GetMean() != 0:
            scalecor_t1 = 1.0 / h_scale0_t1.GetMean()

        scalecor_t1smear = 1.0
        if isMC and h_scale0_t1smear.GetMean() != 0:
            scalecor_t1smear = 1.0 / h_scale0_t1smear.GetMean()

        scalecor_puppi = 1.0
        if h_scale0_puppi.GetMean() != 0:
            scalecor_puppi = 1.0 / h_scale0_puppi.GetMean()
        scalecor_rawmet = 1.0
        scalecor_rawpuppi = 1.0
        scalecor_t1 = 1.0
        scalecor_t1smear = 1.0
        scalecor_puppi = 1.0

        h_scale0_rawmet_vspt.SetBinContent(i + 1, 1. * h_scale0_rawmet.GetMean())
        h_scale0_rawmet_vspt.SetBinError(i + 1, h_scale0_rawmet.GetMeanError())
        h_upara_rawmet_vspt.SetBinContent(i + 1, scalecor_rawmet * h_upara_rawmet.GetRMS())
        h_upara_rawmet_vspt.SetBinError(i + 1, scalecor_rawmet * h_upara_rawmet.GetRMSError())
        h_uperp_rawmet_vspt.SetBinContent(i + 1, scalecor_rawmet * h_uperp_rawmet.GetRMS())
        h_uperp_rawmet_vspt.SetBinError(i + 1, scalecor_rawmet * h_uperp_rawmet.GetRMSError())

        h_scale0_rawpuppi_vspt.SetBinContent(i + 1, 1. * h_scale0_rawpuppi.GetMean())
        h_scale0_rawpuppi_vspt.SetBinError(i + 1, h_scale0_rawpuppi.GetMeanError())
        h_upara_rawpuppi_vspt.SetBinContent(i + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMS())
        h_upara_rawpuppi_vspt.SetBinError(i + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMSError())
        h_uperp_rawpuppi_vspt.SetBinContent(i + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMS())
        h_uperp_rawpuppi_vspt.SetBinError(i + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMSError())

        h_scale0_t1_vspt.SetBinContent(i + 1, 1. * h_scale0_t1.GetMean())
        h_scale0_t1_vspt.SetBinError(i + 1, h_scale0_t1.GetMeanError())
        h_upara_t1_vspt.SetBinContent(i + 1, scalecor_t1 * h_upara_t1.GetRMS())
        h_upara_t1_vspt.SetBinError(i + 1, scalecor_t1 * h_upara_t1.GetRMSError())
        h_uperp_t1_vspt.SetBinContent(i + 1, scalecor_t1 * h_uperp_t1.GetRMS())
        h_uperp_t1_vspt.SetBinError(i + 1, scalecor_t1 * h_uperp_t1.GetRMSError())
        if isMC: 
	    h_scale0_t1smear_vspt.SetBinContent(i + 1, 1. * h_scale0_t1smear.GetMean())
	    h_scale0_t1smear_vspt.SetBinError(i + 1, h_scale0_t1smear.GetMeanError())
	    h_upara_t1smear_vspt.SetBinContent(i + 1, scalecor_t1smear * h_upara_t1smear.GetRMS())
	    h_upara_t1smear_vspt.SetBinError(i + 1, scalecor_t1smear * h_upara_t1smear.GetRMSError())
	    h_uperp_t1smear_vspt.SetBinContent(i + 1, scalecor_t1smear * h_uperp_t1smear.GetRMS())
	    h_uperp_t1smear_vspt.SetBinError(i + 1, scalecor_t1smear * h_uperp_t1smear.GetRMSError())

        h_scale0_puppi_vspt.SetBinContent(i + 1, 1. * h_scale0_puppi.GetMean())
        h_scale0_puppi_vspt.SetBinError(i + 1, h_scale0_puppi.GetMeanError())
        h_upara_puppi_vspt.SetBinContent(i + 1, scalecor_puppi * h_upara_puppi.GetRMS())
        h_upara_puppi_vspt.SetBinError(i + 1, scalecor_puppi * h_upara_puppi.GetRMSError())
        h_uperp_puppi_vspt.SetBinContent(i + 1, scalecor_puppi * h_uperp_puppi.GetRMS())
        h_uperp_puppi_vspt.SetBinError(i + 1, scalecor_puppi * h_uperp_puppi.GetRMSError())
        
	outrawmetd.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_rawmet.GetMean(), h_scale0_rawmet.GetMeanError(), scalecor_rawmet*h_upara_rawmet.GetRMS(), scalecor_rawmet*h_upara_rawmet.GetRMSError(), scalecor_rawmet*h_uperp_rawmet.GetRMS(), scalecor_rawmet*h_uperp_rawmet.GetRMSError()))

	outrawpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_rawpuppi.GetMean(), h_scale0_rawpuppi.GetMeanError(), scalecor_rawpuppi*h_upara_rawpuppi.GetRMS(), scalecor_rawpuppi*h_upara_rawpuppi.GetRMSError(), scalecor_rawpuppi*h_uperp_rawpuppi.GetRMS(), scalecor_rawpuppi*h_uperp_rawpuppi.GetRMSError()))

	outt1d.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_t1.GetMean(), h_scale0_t1.GetMeanError(), scalecor_t1*h_upara_t1.GetRMS(), scalecor_t1*h_upara_t1.GetRMSError(), scalecor_t1*h_uperp_t1.GetRMS(), scalecor_t1*h_uperp_t1.GetRMSError()))
	if isMC : outt1smeard.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_t1smear.GetMean(), h_scale0_t1smear.GetMeanError(), scalecor_t1smear*h_upara_t1smear.GetRMS(), scalecor_t1smear*h_upara_t1smear.GetRMSError(), scalecor_t1smear*h_uperp_t1smear.GetRMS(), scalecor_t1smear*h_uperp_t1smear.GetRMSError()))

	outpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_puppi.GetMean(), h_scale0_puppi.GetMeanError(), scalecor_puppi*h_upara_puppi.GetRMS(), scalecor_puppi*h_upara_puppi.GetRMSError(), scalecor_puppi*h_uperp_puppi.GetRMS(), scalecor_puppi*h_uperp_puppi.GetRMSError()))
        #print "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_puppi.GetMean(), h_scale0_puppi.GetMeanError(), scalecor_puppi*h_upara_puppi.GetRMS(), scalecor_puppi*h_upara_puppi.GetRMSError(), scalecor_puppi*h_uperp_puppi.GetRMS(), scalecor_puppi*h_uperp_puppi.GetRMSError())
        #print "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_puppi.GetMean(), h_scale0_puppi.GetMeanError(), h_upara_puppi.GetRMS(), h_upara_puppi.GetRMSError(), h_uperp_puppi.GetRMS(), h_uperp_puppi.GetRMSError())
        #print 'mean', scalecor_puppi


# Loop over vspt directories and fill the histogram
for i, cut in enumerate(cuts_npv):
    
    folder_name = "Folder_{}_npv".format(i)
    folder = top_directory.GetDirectory(folder_name)
    if folder:
        '''
        h_scale0_rawmet = folder.Get("h_scale0_rawmet")
        h_scale0_rawpuppi = folder.Get("h_scale0_rawpuppi")
        h_scale0_t1 = folder.Get("h_scale0_t1")
        h_scale0_t1smear = folder.Get("h_scale0_t1smear")
        h_scale0_puppi = folder.Get("h_scale0_puppi")

        h_upara_rawmet = folder.Get("h_upara_rawmet")
        h_upara_rawpuppi = folder.Get("h_upara_rawpuppi")
        h_upara_t1 = folder.Get("h_upara_t1")
        h_upara_t1smear = folder.Get("h_upara_t1smear")
        h_upara_puppi = folder.Get("h_upara_puppi")

        h_uperp_rawmet = folder.Get("h_uperp_rawmet")
        h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi")
        h_uperp_t1 = folder.Get("h_uperp_t1")
        h_uperp_t1smear = folder.Get("h_uperp_t1smear")
        h_uperp_puppi = folder.Get("h_uperp_puppi")
        '''
        h_scale0_rawmet = folder.Get("h_scale0_rawmet_npv_{}".format(i))
        h_scale0_rawpuppi = folder.Get("h_scale0_rawpuppi_npv_{}".format(i))
        h_scale0_t1 = folder.Get("h_scale0_t1_npv_{}".format(i))
        h_scale0_t1smear = folder.Get("h_scale0_t1smear_npv_{}".format(i))
        h_scale0_puppi = folder.Get("h_scale0_puppi_npv_{}".format(i))

        h_upara_rawmet = folder.Get("h_upara_rawmet_npv_{}".format(i))
        h_upara_rawpuppi = folder.Get("h_upara_rawpuppi_npv_{}".format(i))
        h_upara_t1 = folder.Get("h_upara_t1_npv_{}".format(i))
        h_upara_t1smear = folder.Get("h_upara_t1smear_npv_{}".format(i))
        h_upara_puppi = folder.Get("h_upara_puppi_npv_{}".format(i))

        h_uperp_rawmet = folder.Get("h_uperp_rawmet_npv_{}".format(i))
        h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi_npv_{}".format(i))
        h_uperp_t1 = folder.Get("h_uperp_t1_npv_{}".format(i))
        h_uperp_t1smear = folder.Get("h_uperp_t1smear_npv_{}".format(i))
        h_uperp_puppi = folder.Get("h_uperp_puppi_npv_{}".format(i))

        if isMC : 
            h_scale0_rawmet.Scale(weight)
            h_scale0_rawpuppi.Scale(weight)
            h_scale0_t1.Scale(weight)
            h_scale0_t1smear.Scale(weight)
            h_scale0_puppi.Scale(weight)
            h_upara_rawmet.Scale(weight)
            h_upara_rawpuppi.Scale(weight)
            h_upara_t1.Scale(weight)
            h_upara_t1smear.Scale(weight)
            h_upara_puppi.Scale(weight)
            h_uperp_rawmet.Scale(weight)
            h_uperp_rawpuppi.Scale(weight)
            h_uperp_t1.Scale(weight)
            h_uperp_t1smear.Scale(weight)
            h_uperp_puppi.Scale(weight)

        scalecor_rawmet = 1.0
        if h_scale0_rawmet.GetMean() != 0:
            scalecor_rawmet = 1.0 / h_scale0_rawmet.GetMean()

        scalecor_rawpuppi = 1.0
        if h_scale0_rawpuppi.GetMean() != 0:
            scalecor_rawpuppi = 1.0 / h_scale0_rawpuppi.GetMean()

        scalecor_t1 = 1.0
        if h_scale0_t1.GetMean() != 0:
            scalecor_t1 = 1.0 / h_scale0_t1.GetMean()

        scalecor_t1smear = 1.0
        if isMC and h_scale0_t1smear.GetMean() != 0:
            scalecor_t1smear = 1.0 / h_scale0_t1smear.GetMean()

        scalecor_puppi = 1.0
        if h_scale0_puppi.GetMean() != 0:
            scalecor_puppi = 1.0 / h_scale0_puppi.GetMean()

        h_scale0_rawmet_npv.SetBinContent(i + 1, 1. * h_scale0_rawmet.GetMean())
        h_scale0_rawmet_npv.SetBinError(i + 1, h_scale0_rawmet.GetMeanError())
        h_upara_rawmet_npv.SetBinContent(i + 1, scalecor_rawmet * h_upara_rawmet.GetRMS())
        h_upara_rawmet_npv.SetBinError(i + 1, scalecor_rawmet * h_upara_rawmet.GetRMSError())
        h_uperp_rawmet_npv.SetBinContent(i + 1, scalecor_rawmet * h_uperp_rawmet.GetRMS())
        h_uperp_rawmet_npv.SetBinError(i + 1, scalecor_rawmet * h_uperp_rawmet.GetRMSError())

        h_scale0_rawpuppi_npv.SetBinContent(i + 1, 1. * h_scale0_rawpuppi.GetMean())
        h_scale0_rawpuppi_npv.SetBinError(i + 1, h_scale0_rawpuppi.GetMeanError())
        h_upara_rawpuppi_npv.SetBinContent(i + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMS())
        h_upara_rawpuppi_npv.SetBinError(i + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMSError())
        h_uperp_rawpuppi_npv.SetBinContent(i + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMS())
        h_uperp_rawpuppi_npv.SetBinError(i + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMSError())

        h_scale0_t1_npv.SetBinContent(i + 1, 1. * h_scale0_t1.GetMean())
        h_scale0_t1_npv.SetBinError(i + 1, h_scale0_t1.GetMeanError())
        h_upara_t1_npv.SetBinContent(i + 1, scalecor_t1 * h_upara_t1.GetRMS())
        h_upara_t1_npv.SetBinError(i + 1, scalecor_t1 * h_upara_t1.GetRMSError())
        h_uperp_t1_npv.SetBinContent(i + 1, scalecor_t1 * h_uperp_t1.GetRMS())
        h_uperp_t1_npv.SetBinError(i + 1, scalecor_t1 * h_uperp_t1.GetRMSError())
        if isMC : 
	    h_scale0_t1smear_npv.SetBinContent(i + 1, 1. * h_scale0_t1smear.GetMean())
	    h_scale0_t1smear_npv.SetBinError(i + 1, h_scale0_t1smear.GetMeanError())
	    h_upara_t1smear_npv.SetBinContent(i + 1, scalecor_t1smear * h_upara_t1smear.GetRMS())
	    h_upara_t1smear_npv.SetBinError(i + 1, scalecor_t1smear * h_upara_t1smear.GetRMSError())
	    h_uperp_t1smear_npv.SetBinContent(i + 1, scalecor_t1smear * h_uperp_t1smear.GetRMS())
	    h_uperp_t1smear_npv.SetBinError(i + 1, scalecor_t1smear * h_uperp_t1smear.GetRMSError())


        h_scale0_puppi_npv.SetBinContent(i + 1, 1. * h_scale0_puppi.GetMean())
        h_scale0_puppi_npv.SetBinError(i + 1, h_scale0_puppi.GetMeanError())
        h_upara_puppi_npv.SetBinContent(i + 1, scalecor_puppi * h_upara_puppi.GetRMS())
        h_upara_puppi_npv.SetBinError(i + 1, scalecor_puppi * h_upara_puppi.GetRMSError())
        h_uperp_puppi_npv.SetBinContent(i + 1, scalecor_puppi * h_uperp_puppi.GetRMS())
        h_uperp_puppi_npv.SetBinError(i + 1, scalecor_puppi * h_uperp_puppi.GetRMSError())

	outrawmetdn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_rawmet.GetMean(), h_scale0_rawmet.GetMeanError(), scalecor_rawmet*h_upara_rawmet.GetRMS(), scalecor_rawmet*h_upara_rawmet.GetRMSError(), scalecor_rawmet*h_uperp_rawmet.GetRMS(), scalecor_rawmet*h_uperp_rawmet.GetRMSError()))

	outrawpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_rawpuppi.GetMean(), h_scale0_rawpuppi.GetMeanError(), scalecor_rawpuppi*h_upara_rawpuppi.GetRMS(), scalecor_rawpuppi*h_upara_rawpuppi.GetRMSError(), scalecor_rawpuppi*h_uperp_rawpuppi.GetRMS(), scalecor_rawpuppi*h_uperp_rawpuppi.GetRMSError()))

	outt1dn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_t1.GetMean(), h_scale0_t1.GetMeanError(), scalecor_t1*h_upara_t1.GetRMS(), scalecor_t1*h_upara_t1.GetRMSError(), scalecor_t1*h_uperp_t1.GetRMS(), scalecor_t1*h_uperp_t1.GetRMSError()))
	if isMC : outt1smeardn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_t1smear.GetMean(), h_scale0_t1smear.GetMeanError(), scalecor_t1smear*h_upara_t1smear.GetRMS(), scalecor_t1smear*h_upara_t1smear.GetRMSError(), scalecor_t1smear*h_uperp_t1smear.GetRMS(), scalecor_t1smear*h_uperp_t1smear.GetRMSError()))

	outpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cut, h_scale0_puppi.GetMean(), h_scale0_puppi.GetMeanError(), scalecor_puppi*h_upara_puppi.GetRMS(), scalecor_puppi*h_upara_puppi.GetRMSError(), scalecor_puppi*h_uperp_puppi.GetRMS(), scalecor_puppi*h_uperp_puppi.GetRMSError()))




print h_scale0_puppi_npv.GetBinContent(1)


file0 = ROOT.TFile("out.root", "RECREATE")


h_scale0_rawmet_vspt.Write()
h_scale0_rawpuppi_vspt.Write()
h_scale0_t1_vspt.Write()
h_scale0_t1smear_vspt.Write()
h_scale0_puppi_vspt.Write()
h_upara_rawmet_vspt.Write()
h_upara_rawpuppi_vspt.Write()
h_upara_t1smear_vspt.Write()
h_upara_puppi_vspt.Write()
h_uperp_rawmet_vspt.Write()
h_uperp_rawpuppi_vspt.Write()
h_uperp_t1smear_vspt.Write()
h_uperp_puppi_vspt.Write()



h_scale0_rawmet_npv.Write()
h_scale0_rawpuppi_npv.Write()
h_scale0_t1_npv.Write()
h_scale0_t1smear_npv.Write()
h_scale0_puppi_npv.Write()
h_upara_rawmet_npv.Write()
h_upara_rawpuppi_npv.Write()
h_upara_t1_npv.Write()
h_upara_t1smear_npv.Write()
h_upara_puppi_npv.Write()
h_uperp_rawmet_npv.Write()
h_uperp_rawpuppi_npv.Write()
h_uperp_t1_npv.Write()
h_uperp_t1smear_npv.Write()
h_uperp_puppi_npv.Write()


file0.Write()
file0.Close()

# Close the file
file.Close()

outrawmetd.close()
outrawpuppid.close()
outt1d.close()
outt1smeard.close()
outpuppid.close()

outrawmetdn.close()
outrawpuppidn.close()
outt1dn.close()
outt1smeardn.close()
outpuppidn.close()


