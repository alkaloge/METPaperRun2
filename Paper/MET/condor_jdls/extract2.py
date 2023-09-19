import ROOT
from array import array
from ROOT import TH1, TH1F, TFile
import sys, os


def changeSignOfHistogram(histogram):
    # Iterate over each bin in the histogram
    for bin in range(1, histogram.GetNbinsX() + 1):
        # Get the current bin content
        content = histogram.GetBinContent(bin)

        # Multiply the content by -1 to change the sign
        new_content = -1 * content

        # Set the new content for the bin
        histogram.SetBinContent(bin, new_content)




def extract2():

    filename = sys.argv[1]
    #python extract.py filename ismc MuMu 2018 dy

    isMC=True
    channel='MuMu'
    if "run20" in str(filename).lower()  or 'single' in str(filename).lower() or 'egamma' in str(filename).lower(): isMC = False

    year = str(sys.argv[2])
    channel = str(sys.argv[3])
    channelDir = str(sys.argv[4])

    lumi=1.
    if year == "2017 ": lumi = 41.48

    if year == "2018":  lumi = 59.83
    if year == "2016":  lumi = 19.35
    if year == "2016all":  lumi = 19.35+16.98
    if year == "2016postVFP": lumi = 16.98
    if year == "2016preVFP": lumi = 19.35


    print "year", year, "lumi", lumi, "isMC", isMC, "channel", channel, "channelDir", channelDir, "args", sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]



    # Open the ROOT file
    file = ROOT.TFile(filename, "READ")


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
	#"(0<=event.nPVGood )": "nPVGoodIncl",
	"(0<=event.nPVGood  and  event.nPVGood<10)": "nPVGoodLt10",
	"(10<=event.nPVGood  and  event.nPVGood<20)": "nPVGoodGt10Lt20",
	"(20<=event.nPVGood  and  event.nPVGood<30)": "nPVGoodGt20Lt30",
	"(30<=event.nPVGood  and  event.nPVGood<40)": "nPVGoodGt30Lt40",
	"(40<=event.nPVGood  and  event.nPVGood<50)": "nPVGoodGt40Lt50",
	"(50<=event.nPVGood  and  event.nPVGood<60)": "nPVGoodGt50Lt60",
	"(60<=event.nPVGood)": "nPVGoodGt60"
    }
    '''
    folder_names_npv = {
	0: "nPVGoodIncl",
	1: "nPVGoodLt10",
	2: "nPVGoodGt10Lt20",
	3: "nPVGoodGt20Lt30",
	4: "nPVGoodGt30Lt40",
	#5: "nPVGoodGt40",
	5: "nPVGoodGt40Lt50",
	6: "nPVGoodGt50Lt60",
	7: "nPVGoodGt60"
    }
    '''
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


    # Create histograms for vspt and npv
    h_scale_rawmet_vspt = ROOT.TH1F("h_scale_rawmet_vspt", "", bins, varbins)
    h_upara_rawmet_vspt = ROOT.TH1F("h_upara_rawmet_vspt", "", bins, varbins)
    h_uparaboson_rawmet_vspt = ROOT.TH1F("h_uparaboson_rawmet_vspt", "", bins, varbins)
    h_uperp_rawmet_vspt = ROOT.TH1F("h_uperp_rawmet_vspt", "", bins, varbins)
    h_scale_rawpuppi_vspt = ROOT.TH1F("h_scale_rawpuppi_vspt", "", bins, varbins)
    h_upara_rawpuppi_vspt = ROOT.TH1F("h_upara_rawpuppi_vspt", "", bins, varbins)
    h_uparaboson_rawpuppi_vspt = ROOT.TH1F("h_uparaboson_rawpuppi_vspt", "", bins, varbins)
    h_uperp_rawpuppi_vspt = ROOT.TH1F("h_uperp_rawpuppi_vspt", "", bins, varbins)
    h_scale_t1_vspt = ROOT.TH1F("h_scale_t1_vspt", "", bins, varbins)
    h_upara_t1_vspt = ROOT.TH1F("h_upara_t1_vspt", "", bins, varbins)
    h_uparaboson_t1_vspt = ROOT.TH1F("h_uparaboson_t1_vspt", "", bins, varbins)
    h_uperp_t1_vspt = ROOT.TH1F("h_uperp_t1_vspt", "", bins, varbins)
    h_scale_t1smear_vspt = ROOT.TH1F("h_scale_t1smear_vspt", "", bins, varbins)
    h_upara_t1smear_vspt = ROOT.TH1F("h_upara_t1smear_vspt", "", bins, varbins)
    h_uparaboson_t1smear_vspt = ROOT.TH1F("h_uparaboson_t1smear_vspt", "", bins, varbins)
    h_uperp_t1smear_vspt = ROOT.TH1F("h_uperp_t1smear_vspt", "", bins, varbins)
    h_scale_puppi_vspt = ROOT.TH1F("h_scale_puppi_vspt", "", bins, varbins)
    h_upara_puppi_vspt = ROOT.TH1F("h_upara_puppi_vspt", "", bins, varbins)
    h_uparaboson_puppi_vspt = ROOT.TH1F("h_uparaboson_puppi_vspt", "", bins, varbins)
    h_uperp_puppi_vspt = ROOT.TH1F("h_uperp_puppi_vspt", "", bins, varbins)


    h_scale_rawmet_npv = ROOT.TH1F("h_scale_rawmet_npv", "",bins_npv,varbins_npv)
    h_upara_rawmet_npv = ROOT.TH1F("h_upara_rawmet_npv", "",bins_npv,varbins_npv)
    h_uparaboson_rawmet_npv = ROOT.TH1F("h_uparaboson_rawmet_npv", "",bins_npv,varbins_npv)
    h_uperp_rawmet_npv = ROOT.TH1F("h_uperp_rawmet_npv", "",bins_npv,varbins_npv)
    h_scale_rawpuppi_npv = ROOT.TH1F("h_scale_rawpuppi_npv", "",bins_npv,varbins_npv)
    h_upara_rawpuppi_npv = ROOT.TH1F("h_upara_rawpuppi_npv", "",bins_npv,varbins_npv)
    h_uparaboson_rawpuppi_npv = ROOT.TH1F("h_uparaboson_rawpuppi_npv", "",bins_npv,varbins_npv)
    h_uperp_rawpuppi_npv = ROOT.TH1F("h_uperp_rawpuppi_npv", "",bins_npv,varbins_npv)
    h_scale_t1_npv = ROOT.TH1F("h_scale_t1_npv", "",bins_npv,varbins_npv)
    h_upara_t1_npv = ROOT.TH1F("h_upara_t1_npv", "",bins_npv,varbins_npv)
    h_uparaboson_t1_npv = ROOT.TH1F("h_uparaboson_t1_npv", "",bins_npv,varbins_npv)
    h_uperp_t1_npv = ROOT.TH1F("h_uperp_t1_npv", "",bins_npv,varbins_npv)
    h_scale_t1smear_npv = ROOT.TH1F("h_scale_t1smear_npv", "",bins_npv,varbins_npv)
    h_upara_t1smear_npv = ROOT.TH1F("h_upara_t1smear_npv", "",bins_npv,varbins_npv)
    h_uparaboson_t1smear_npv = ROOT.TH1F("h_uparaboson_t1smear_npv", "",bins_npv,varbins_npv)
    h_uperp_t1smear_npv = ROOT.TH1F("h_uperp_t1smear_npv", "",bins_npv,varbins_npv)
    h_scale_puppi_npv = ROOT.TH1F("h_scale_puppi_npv", "",bins_npv,varbins_npv)
    h_upara_puppi_npv = ROOT.TH1F("h_upara_puppi_npv", "",bins_npv,varbins_npv)
    h_uparaboson_puppi_npv = ROOT.TH1F("h_uparaboson_puppi_npv", "",bins_npv,varbins_npv)
    h_uperp_puppi_npv = ROOT.TH1F("h_uperp_puppi_npv", "",bins_npv,varbins_npv)


    h_scale_perp_rawmet_vspt = ROOT.TH1F("h_scale_perp_rawmet_vspt", "", bins, varbins)
    h_scale_perp_rawpuppi_vspt = ROOT.TH1F("h_scale_perp_rawpuppi_vspt", "", bins, varbins)
    h_scale_perp_t1_vspt = ROOT.TH1F("h_scale_perp_t1_vspt", "", bins, varbins)
    h_scale_perp_t1smear_vspt = ROOT.TH1F("h_scale_perp_t1smear_vspt", "", bins, varbins)
    h_scale_perp_puppi_vspt = ROOT.TH1F("h_scale_perp_puppi_vspt", "", bins, varbins)


    h_scale_perp_rawmet_npv = ROOT.TH1F("h_scale_perp_rawmet_npv", "",bins_npv,varbins_npv)
    h_scale_perp_rawpuppi_npv = ROOT.TH1F("h_scale_perp_rawpuppi_npv", "",bins_npv,varbins_npv)
    h_scale_perp_t1_npv = ROOT.TH1F("h_scale_perp_t1_npv", "",bins_npv,varbins_npv)
    h_scale_perp_t1smear_npv = ROOT.TH1F("h_scale_perp_t1smear_npv", "",bins_npv,varbins_npv)
    h_scale_perp_puppi_npv = ROOT.TH1F("h_scale_perp_puppi_npv", "",bins_npv,varbins_npv)





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




    # Get the top directory of the ROOT file
    top_directory = file.GetDirectory("")

    weight = 1.
    
    for i, cut in enumerate(cuts_vspt):
	
        if str(i) == "0" : continue
	folder_name = "Folder_%d_vspt_%s" % (i, folder_names[i])
	print '......................', folder_name
	folder = top_directory.GetDirectory(folder_name)
        #file.ls()
        #top_directory.ls()
        
	if folder:
	    h_scale_rawmet = folder.Get("h_scale_rawmet_vspt_{}".format(i))
	    h_scale_rawpuppi = folder.Get("h_scale_rawpuppi_vspt_{}".format(i))
	    h_scale_t1 = folder.Get("h_scale_t1_vspt_{}".format(i))
	    h_scale_t1smear = folder.Get("h_scale_t1smear_vspt_{}".format(i))
	    h_scale_puppi = folder.Get("h_scale_puppi_vspt_{}".format(i))

	    h_scale_perp_rawmet = folder.Get("h_scale_perp_rawmet_vspt_{}".format(i))
	    h_scale_perp_rawpuppi = folder.Get("h_scale_perp_rawpuppi_vspt_{}".format(i))
	    h_scale_perp_t1 = folder.Get("h_scale_perp_t1_vspt_{}".format(i))
	    h_scale_perp_t1smear = folder.Get("h_scale_perp_t1smear_vspt_{}".format(i))
	    h_scale_perp_puppi = folder.Get("h_scale_perp_puppi_vspt_{}".format(i))



	    h_upara_rawmet = folder.Get("h_upara_rawmet_vspt_{}".format(i))
	    h_uparaboson_rawmet = folder.Get("h_uparaboson_rawmet_vspt_{}".format(i))
	    h_upara_rawpuppi = folder.Get("h_upara_rawpuppi_vspt_{}".format(i))
	    h_uparaboson_rawpuppi = folder.Get("h_uparaboson_rawpuppi_vspt_{}".format(i))
	    h_upara_t1 = folder.Get("h_upara_t1_vspt_{}".format(i))
	    h_uparaboson_t1 = folder.Get("h_uparaboson_t1_vspt_{}".format(i))
	    h_upara_t1smear = folder.Get("h_upara_t1smear_vspt_{}".format(i))
	    h_uparaboson_t1smear = folder.Get("h_uparaboson_t1smear_vspt_{}".format(i))
	    h_upara_puppi = folder.Get("h_upara_puppi_vspt_{}".format(i))
	    h_uparaboson_puppi = folder.Get("h_uparaboson_puppi_vspt_{}".format(i))

	    h_uperp_rawmet = folder.Get("h_uperp_rawmet_vspt_{}".format(i))
	    h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi_vspt_{}".format(i))
	    h_uperp_t1 = folder.Get("h_uperp_t1_vspt_{}".format(i))
	    h_uperp_t1smear = folder.Get("h_uperp_t1smear_vspt_{}".format(i))
	    h_uperp_puppi = folder.Get("h_uperp_puppi_vspt_{}".format(i))
	    '''
	    changeSignOfHistogram(h_upara_rawmet)
	    changeSignOfHistogram(h_uparaboson_rawmet)
	    changeSignOfHistogram(h_upara_rawpuppi)
	    changeSignOfHistogram(h_uparaboson_rawpuppi)
	    changeSignOfHistogram(h_upara_t1)
	    changeSignOfHistogram(h_uparaboson_t1)
	    if isMC : changeSignOfHistogram(h_upara_t1smear)
	    if isMC : changeSignOfHistogram(h_uparaboson_t1smear)
	    changeSignOfHistogram(h_upara_puppi)
	    changeSignOfHistogram(h_uparaboson_puppi)
	    changeSignOfHistogram(h_uperp_rawmet)
	    changeSignOfHistogram(h_uperp_rawpuppi)
	    changeSignOfHistogram(h_uperp_t1)
	    if isMC : changeSignOfHistogram(h_uperp_t1smear)
	    changeSignOfHistogram(h_uperp_puppi)
            '''
	    if isMC and weight!=1.: 
		h_scale_rawmet.Scale(weight)
		h_scale_rawpuppi.Scale(weight)
		h_scale_t1.Scale(weight)
		h_scale_puppi.Scale(weight)
		h_scale_t1smear.Scale(weight)

		h_scale_perp_rawmet.Scale(weight)
		h_scale_perp_rawpuppi.Scale(weight)
		h_scale_perp_t1.Scale(weight)
		h_scale_perp_puppi.Scale(weight)
		h_scale_perp_t1smear.Scale(weight)

	    scalecor_rawmet = 1.0
	    if h_scale_rawmet.GetMean() != 0:
		scalecor_rawmet = 1.0 / h_scale_rawmet.GetMean()
	     
	    scalecor_rawpuppi = 1.0
	    if h_scale_rawpuppi.GetMean() != 0:
		scalecor_rawpuppi = 1.0 / h_scale_rawpuppi.GetMean()

	    scalecor_t1 = 1.0
	    if h_scale_t1.GetMean() != 0:
		scalecor_t1 = 1.0 / h_scale_t1.GetMean()

	    scalecor_t1smear = 1.0
	    if isMC and h_scale_t1smear.GetMean() != 0:
		scalecor_t1smear = 1.0 / h_scale_t1smear.GetMean()

	    scalecor_puppi= 1.0
	    if h_scale_puppi.GetMean() != 0:
		scalecor_puppi   = 1.0 / h_scale_puppi.GetMean()

	    scalecor_rawmet = 1.0
	    scalecor_rawpuppi = 1.0
	    scalecor_t1 = 1.0
	    scalecor_t1smear = 1.0
	    scalecor_puppi = 1.0

	    #print 'vspt_', scalecor_puppi, scalecor_rawmet, scalecor_rawpuppi, scalecor_t1, scalecor_t1smear
            if weight!=1. : 
		h_upara_rawmet.Scale(weight * scalecor_rawmet)
		h_uparaboson_rawmet.Scale(weight * scalecor_rawmet)
		h_upara_rawpuppi.Scale(weight * scalecor_rawpuppi)
		h_uparaboson_rawpuppi.Scale(weight * scalecor_rawpuppi)
		h_upara_t1.Scale(weight * scalecor_t1)
		h_uparaboson_t1.Scale(weight * scalecor_t1)
		h_upara_puppi.Scale(weight * scalecor_puppi)
		h_uparaboson_puppi.Scale(weight * scalecor_puppi)

		h_uperp_rawmet.Scale(weight * scalecor_rawmet)
		h_uperp_rawpuppi.Scale(weight * scalecor_rawpuppi)

		#print 'before....', h_uperp_t1.GetRMS(), h_uperp_puppi.GetRMS(), h_uperp_t1.GetMean(), h_uperp_puppi.GetMean()

		h_uperp_t1.Scale(weight * scalecor_t1)
		h_uperp_puppi.Scale(weight * scalecor_puppi)

		#print 'after some....', h_uperp_t1.GetRMS(), h_uperp_puppi.GetRMS(), h_uperp_t1.GetMean(), h_uperp_puppi.GetMean(), isMC, weight, scalecor_t1, scalecor_puppi, weight * scalecor_puppi
		if isMC : 
		    h_upara_t1smear.Scale(weight * scalecor_t1smear)
		    h_uparaboson_t1smear.Scale(weight * scalecor_t1smear)
		    h_uperp_t1smear.Scale(weight * scalecor_t1smear)
	   
	    h_scale_rawmet_vspt.SetBinContent(i + 1, 1. * h_scale_rawmet.GetMean())
	    h_scale_rawmet_vspt.SetBinError(i + 1, h_scale_rawmet.GetMeanError())
	    h_upara_rawmet_vspt.SetBinContent(i + 1, h_upara_rawmet.GetRMS())
	    h_uparaboson_rawmet_vspt.SetBinContent(i + 1, h_uparaboson_rawmet.GetRMS())
	    h_upara_rawmet_vspt.SetBinError(i + 1, h_upara_rawmet.GetRMSError())
	    h_uparaboson_rawmet_vspt.SetBinError(i + 1, h_uparaboson_rawmet.GetRMSError())
	    h_uperp_rawmet_vspt.SetBinContent(i + 1, h_uperp_rawmet.GetRMS())
	    h_uperp_rawmet_vspt.SetBinError(i + 1, h_uperp_rawmet.GetRMSError())

	    h_scale_rawpuppi_vspt.SetBinContent(i + 1, 1. * h_scale_rawpuppi.GetMean())
	    h_scale_rawpuppi_vspt.SetBinError(i + 1, h_scale_rawpuppi.GetMeanError())
	    h_upara_rawpuppi_vspt.SetBinContent(i + 1, h_upara_rawpuppi.GetRMS())
	    h_uparaboson_rawpuppi_vspt.SetBinContent(i + 1, h_uparaboson_rawpuppi.GetRMS())
	    h_upara_rawpuppi_vspt.SetBinError(i + 1, h_upara_rawpuppi.GetRMSError())
	    h_uparaboson_rawpuppi_vspt.SetBinError(i + 1, h_uparaboson_rawpuppi.GetRMSError())
	    h_uperp_rawpuppi_vspt.SetBinContent(i + 1, h_uperp_rawpuppi.GetRMS())
	    h_uperp_rawpuppi_vspt.SetBinError(i + 1, h_uperp_rawpuppi.GetRMSError())

	    h_scale_t1_vspt.SetBinContent(i + 1, 1. * h_scale_t1.GetMean())
	    h_scale_t1_vspt.SetBinError(i + 1, h_scale_t1.GetMeanError())
	    h_upara_t1_vspt.SetBinContent(i + 1, h_upara_t1.GetRMS())
	    h_uparaboson_t1_vspt.SetBinContent(i + 1, h_uparaboson_t1.GetRMS())
	    h_upara_t1_vspt.SetBinError(i + 1,  h_upara_t1.GetRMSError())
	    h_uparaboson_t1_vspt.SetBinError(i + 1,  h_uparaboson_t1.GetRMSError())
	    h_uperp_t1_vspt.SetBinContent(i + 1,  h_uperp_t1.GetRMS())
	    h_uperp_t1_vspt.SetBinError(i + 1, h_uperp_t1.GetRMSError())
	    if isMC: 
		h_scale_t1smear_vspt.SetBinContent(i + 1, 1. * h_scale_t1smear.GetMean())
		h_scale_t1smear_vspt.SetBinError(i + 1, h_scale_t1smear.GetMeanError())
		h_upara_t1smear_vspt.SetBinContent(i + 1, h_upara_t1smear.GetRMS())
		h_uparaboson_t1smear_vspt.SetBinContent(i + 1, h_uparaboson_t1smear.GetRMS())
		h_upara_t1smear_vspt.SetBinError(i + 1, h_upara_t1smear.GetRMSError())
		h_uparaboson_t1smear_vspt.SetBinError(i + 1, h_uparaboson_t1smear.GetRMSError())
		h_uperp_t1smear_vspt.SetBinContent(i + 1, h_uperp_t1smear.GetRMS())
		h_uperp_t1smear_vspt.SetBinError(i + 1, h_uperp_t1smear.GetRMSError())

	    h_scale_puppi_vspt.SetBinContent(i + 1, 1. * h_scale_puppi.GetMean())
	    h_scale_puppi_vspt.SetBinError(i + 1, h_scale_puppi.GetMeanError())
	    h_upara_puppi_vspt.SetBinContent(i + 1, h_upara_puppi.GetRMS())
	    h_uparaboson_puppi_vspt.SetBinContent(i + 1, h_uparaboson_puppi.GetRMS())
	    h_upara_puppi_vspt.SetBinError(i + 1, h_upara_puppi.GetRMSError())
	    h_uparaboson_puppi_vspt.SetBinError(i + 1, h_uparaboson_puppi.GetRMSError())
	    h_uperp_puppi_vspt.SetBinContent(i + 1,  h_uperp_puppi.GetRMS())
	    h_uperp_puppi_vspt.SetBinError(i + 1,  h_uperp_puppi.GetRMSError())
	    
	    #scale_perp
	    h_scale_perp_rawmet_vspt.SetBinContent(i + 1, 1. * h_scale_perp_rawmet.GetMean())
	    h_scale_perp_rawmet_vspt.SetBinError(i + 1, h_scale_perp_rawmet.GetMeanError())

	    h_scale_perp_rawpuppi_vspt.SetBinContent(i + 1, 1. * h_scale_perp_rawpuppi.GetMean())
	    h_scale_perp_rawpuppi_vspt.SetBinError(i + 1, h_scale_perp_rawpuppi.GetMeanError())

	    h_scale_perp_t1_vspt.SetBinContent(i + 1, 1. * h_scale_perp_t1.GetMean())
	    h_scale_perp_t1_vspt.SetBinError(i + 1, h_scale_perp_t1.GetMeanError())
	    if isMC: 
		h_scale_perp_t1smear_vspt.SetBinContent(i + 1, 1. * h_scale_perp_t1smear.GetMean())
		h_scale_perp_t1smear_vspt.SetBinError(i + 1, h_scale_perp_t1smear.GetMeanError())

	    h_scale_perp_puppi_vspt.SetBinContent(i + 1, 1. * h_scale_perp_puppi.GetMean())
	    h_scale_perp_puppi_vspt.SetBinError(i + 1, h_scale_perp_puppi.GetMeanError())




	    outrawmetd.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_rawmet.GetMean(), h_scale_rawmet.GetMeanError(), h_upara_rawmet.GetRMS(), h_upara_rawmet.GetRMSError(), h_uperp_rawmet.GetRMS(), h_uperp_rawmet.GetRMSError(), h_scale_perp_rawmet.GetMean(), h_scale_perp_rawmet.GetMeanError()))
	    #outrawmetd.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_rawmet.GetMean(), h_scale_rawmet.GetMeanError(), h_uparaboson_rawmet.GetRMS(), h_uparaboson_rawmet.GetRMSError(), h_uperp_rawmet.GetRMS(), h_uperp_rawmet.GetRMSError(), h_scale_perp_rawmet.GetMean(), h_scale_perp_rawmet.GetMeanError()))

	    outrawpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_rawpuppi.GetMean(), h_scale_rawpuppi.GetMeanError(), h_upara_rawpuppi.GetRMS(), h_upara_rawpuppi.GetRMSError(), h_uperp_rawpuppi.GetRMS(), h_uperp_rawpuppi.GetRMSError(), h_scale_perp_rawpuppi.GetMean(), h_scale_perp_rawpuppi.GetMeanError()))
	    #outrawpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_rawpuppi.GetMean(), h_scale_rawpuppi.GetMeanError(), h_uparaboson_rawpuppi.GetRMS(), h_uparaboson_rawpuppi.GetRMSError(), h_uperp_rawpuppi.GetRMS(), h_uperp_rawpuppi.GetRMSError(), h_scale_perp_rawpuppi.GetMean(), h_scale_perp_rawpuppi.GetMeanError()))

	    outt1d.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_t1.GetMean(), h_scale_t1.GetMeanError(), h_upara_t1.GetRMS(), h_upara_t1.GetRMSError(), h_uperp_t1.GetRMS(), h_uperp_t1.GetRMSError(), h_scale_perp_t1.GetMean(), h_scale_perp_t1.GetMeanError()))
	    #outt1d.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_t1.GetMean(), h_scale_t1.GetMeanError(), h_uparaboson_t1.GetRMS(), h_uparaboson_t1.GetRMSError(), h_uperp_t1.GetRMS(), h_uperp_t1.GetRMSError(), h_scale_perp_t1.GetMean(), h_scale_perp_t1.GetMeanError()))
	    if isMC: 
		outt1smeard.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_t1smear.GetMean(), h_scale_t1smear.GetMeanError(), h_upara_t1smear.GetRMS(), h_upara_t1smear.GetRMSError(), h_uperp_t1smear.GetRMS(), h_uperp_t1smear.GetRMSError(), h_scale_perp_t1smear.GetMean(), h_scale_perp_t1smear.GetMeanError()))
		#outt1smeard.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_t1smear.GetMean(), h_scale_t1smear.GetMeanError(), h_uparaboson_t1smear.GetRMS(), h_uparaboson_t1smear.GetRMSError(), h_uperp_t1smear.GetRMS(), h_uperp_t1smear.GetRMSError(), h_scale_perp_t1smear.GetMean(), h_scale_perp_t1smear.GetMeanError()))

	    #outpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_puppi.GetMean(), h_scale_puppi.GetMeanError(), h_upara_puppi.GetRMS(), h_upara_puppi.GetRMSError(), h_uperp_puppi.GetRMS(), h_uperp_puppi.GetRMSError(), h_scale_perp_puppi.GetMean(), h_scale_perp_puppi.GetMeanError()))
	    outpuppid.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_vspt[i], h_scale_puppi.GetMean(), h_scale_puppi.GetMeanError(), h_uparaboson_puppi.GetRMS(), h_uparaboson_puppi.GetRMSError(), h_uperp_puppi.GetRMS(), h_uperp_puppi.GetRMSError(), h_scale_perp_puppi.GetMean(), h_scale_perp_puppi.GetMeanError()))



    # Loop over vspt directories and fill the histogram
    for i, cut in enumerate(cuts_npv):
	
        #if str(i) == "0" : continue
	folder_name = "Folder_%d_npv_%s" % (i, folder_names_npv[i])
	folder = top_directory.GetDirectory(folder_name)
	if folder:
            #print 'inside...', folder_name
	    '''
	    h_scale_rawmet = folder.Get("h_scale_rawmet")
	    h_scale_rawpuppi = folder.Get("h_scale_rawpuppi")
	    h_scale_t1 = folder.Get("h_scale_t1")
	    h_scale_t1smear = folder.Get("h_scale_t1smear")
	    h_scale_puppi = folder.Get("h_scale_puppi")

	    h_upara_rawmet = folder.Get("h_upara_rawmet")
	    h_uparaboson_rawmet = folder.Get("h_uparaboson_rawmet")
	    h_upara_rawpuppi = folder.Get("h_upara_rawpuppi")
	    h_uparaboson_rawpuppi = folder.Get("h_uparaboson_rawpuppi")
	    h_upara_t1 = folder.Get("h_upara_t1")
	    h_uparaboson_t1 = folder.Get("h_uparaboson_t1")
	    h_upara_t1smear = folder.Get("h_upara_t1smear")
	    h_uparaboson_t1smear = folder.Get("h_uparaboson_t1smear")
	    h_upara_puppi = folder.Get("h_upara_puppi")
	    h_uparaboson_puppi = folder.Get("h_uparaboson_puppi")

	    h_uperp_rawmet = folder.Get("h_uperp_rawmet")
	    h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi")
	    h_uperp_t1 = folder.Get("h_uperp_t1")
	    h_uperp_t1smear = folder.Get("h_uperp_t1smear")
	    h_uperp_puppi = folder.Get("h_uperp_puppi")
	    '''
	    h_scale_rawmet = folder.Get("h_scale_rawmet_npv_{}".format(i))
	    h_scale_rawpuppi = folder.Get("h_scale_rawpuppi_npv_{}".format(i))
	    h_scale_t1 = folder.Get("h_scale_t1_npv_{}".format(i))
	    h_scale_t1smear = folder.Get("h_scale_t1smear_npv_{}".format(i))
	    h_scale_puppi = folder.Get("h_scale_puppi_npv_{}".format(i))

	    h_scale_perp_rawmet = folder.Get("h_scale_perp_rawmet_npv_{}".format(i))
	    h_scale_perp_rawpuppi = folder.Get("h_scale_perp_rawpuppi_npv_{}".format(i))
	    h_scale_perp_t1 = folder.Get("h_scale_perp_t1_npv_{}".format(i))
	    h_scale_perp_t1smear = folder.Get("h_scale_perp_t1smear_npv_{}".format(i))
	    h_scale_perp_puppi = folder.Get("h_scale_perp_puppi_npv_{}".format(i))



	    h_upara_rawmet = folder.Get("h_upara_rawmet_npv_{}".format(i))
	    h_uparaboson_rawmet = folder.Get("h_uparaboson_rawmet_npv_{}".format(i))
	    h_upara_rawpuppi = folder.Get("h_upara_rawpuppi_npv_{}".format(i))
	    h_uparaboson_rawpuppi = folder.Get("h_uparaboson_rawpuppi_npv_{}".format(i))
	    h_upara_t1 = folder.Get("h_upara_t1_npv_{}".format(i))
	    h_uparaboson_t1 = folder.Get("h_uparaboson_t1_npv_{}".format(i))
	    h_upara_t1smear = folder.Get("h_upara_t1smear_npv_{}".format(i))
	    h_uparaboson_t1smear = folder.Get("h_uparaboson_t1smear_npv_{}".format(i))
	    h_upara_puppi = folder.Get("h_upara_puppi_npv_{}".format(i))
	    h_uparaboson_puppi = folder.Get("h_uparaboson_puppi_npv_{}".format(i))

	    h_uperp_rawmet = folder.Get("h_uperp_rawmet_npv_{}".format(i))
	    h_uperp_rawpuppi = folder.Get("h_uperp_rawpuppi_npv_{}".format(i))
	    h_uperp_t1 = folder.Get("h_uperp_t1_npv_{}".format(i))
	    h_uperp_t1smear = folder.Get("h_uperp_t1smear_npv_{}".format(i))
	    h_uperp_puppi = folder.Get("h_uperp_puppi_npv_{}".format(i))
            '''
	    changeSignOfHistogram(h_upara_rawmet)
	    changeSignOfHistogram(h_uparaboson_rawmet)
	    changeSignOfHistogram(h_upara_rawpuppi)
	    changeSignOfHistogram(h_uparaboson_rawpuppi)
	    changeSignOfHistogram(h_upara_t1)
	    changeSignOfHistogram(h_uparaboson_t1)
	    if isMC : changeSignOfHistogram(h_upara_t1smear)
	    if isMC : changeSignOfHistogram(h_uparaboson_t1smear)
	    changeSignOfHistogram(h_upara_puppi)
	    changeSignOfHistogram(h_uparaboson_puppi)
	    changeSignOfHistogram(h_uperp_rawmet)
	    changeSignOfHistogram(h_uperp_rawpuppi)
	    changeSignOfHistogram(h_uperp_t1)
	    if isMC : changeSignOfHistogram(h_uperp_t1smear)
	    changeSignOfHistogram(h_uperp_puppi)
            '''


	    if isMC : 
		h_scale_rawmet.Scale(weight)
		h_scale_rawpuppi.Scale(weight)
		h_scale_t1.Scale(weight)
		h_scale_t1smear.Scale(weight)
		h_scale_puppi.Scale(weight)

		h_scale_perp_rawmet.Scale(weight)
		h_scale_perp_rawpuppi.Scale(weight)
		h_scale_perp_t1.Scale(weight)
		h_scale_perp_t1smear.Scale(weight)
		h_scale_perp_puppi.Scale(weight)

	    scalecor_rawmet = 1.0
	    if h_scale_rawmet.GetMean() != 0:
		scalecor_rawmet = 1.0 / h_scale_rawmet.GetMean()

	    scalecor_rawpuppi = 1.0
	    if h_scale_rawpuppi.GetMean() != 0:
		scalecor_rawpuppi = 1.0 / h_scale_rawpuppi.GetMean()

	    scalecor_t1 = 1.0
	    if h_scale_t1.GetMean() != 0:
		scalecor_t1 = 1.0 / h_scale_t1.GetMean()

	    scalecor_t1smear = 1.0
	    if isMC and h_scale_t1smear.GetMean() != 0:
		scalecor_t1smear = 1.0 / h_scale_t1smear.GetMean()

	    scalecor_puppi = 1.0
	    if h_scale_puppi.GetMean() != 0:
		scalecor_puppi   = 1.0 / h_scale_puppi.GetMean()

	    scalecor_rawmet = 1.0
	    scalecor_rawpuppi = 1.0
	    scalecor_t1 = 1.0
	    scalecor_t1smear = 1.0
	    scalecor_puppi = 1.0

	    #print 'npv_', scalecor_puppi, scalecor_rawmet, scalecor_rawpuppi, scalecor_t1, scalecor_t1smear
	    h_upara_rawmet.Scale(weight * scalecor_rawmet)
	    h_uparaboson_rawmet.Scale(weight * scalecor_rawmet)
	    h_upara_rawpuppi.Scale(weight * scalecor_rawpuppi)
	    h_uparaboson_rawpuppi.Scale(weight * scalecor_rawpuppi)
	    h_upara_t1.Scale(weight * scalecor_t1)
	    h_uparaboson_t1.Scale(weight * scalecor_t1)
	    h_upara_puppi.Scale(weight * scalecor_puppi)
	    h_uparaboson_puppi.Scale(weight * scalecor_puppi)
	    #print ''
	    #print 'before....', h_uperp_t1.GetRMS(), h_uperp_puppi.GetRMS(), h_uperp_t1.GetMean(), h_uperp_puppi.GetMean(), weight * scalecor_puppi, h_uperp_t1.GetSumOfWeights()

	    h_uperp_rawmet.Scale(weight * scalecor_rawmet)
	    h_uperp_rawpuppi.Scale(weight * scalecor_rawpuppi)
	    h_uperp_t1.Scale(weight * scalecor_t1)
	    h_uperp_puppi.Scale( float(weight * scalecor_puppi))
	    #print 'after npv....', h_uperp_t1.GetRMS(), h_uperp_puppi.GetRMS(), h_uperp_t1.GetMean(), h_uperp_puppi.GetMean(), weight * scalecor_puppi, h_uperp_t1.GetSumOfWeights()
	    if isMC : 
		h_upara_t1smear.Scale(weight * scalecor_t1smear)
		h_uparaboson_t1smear.Scale(weight * scalecor_t1smear)
		h_uperp_t1smear.Scale(weight * scalecor_t1smear)
	   
	    #print 'scalecor', scalecor_rawmet, scalecor_rawpuppi, scalecor_puppi, scalecor_t1, scalecor_t1smear
	    h_scale_rawmet_npv.SetBinContent(i + 1, 1. * h_scale_rawmet.GetMean())
	    h_scale_rawmet_npv.SetBinError(i + 1, h_scale_rawmet.GetMeanError())
	    h_upara_rawmet_npv.SetBinContent(i + 1, h_upara_rawmet.GetRMS())
	    h_uparaboson_rawmet_npv.SetBinContent(i + 1, h_uparaboson_rawmet.GetRMS())
	    h_upara_rawmet_npv.SetBinError(i + 1, h_upara_rawmet.GetRMSError())
	    h_uparaboson_rawmet_npv.SetBinError(i + 1, h_uparaboson_rawmet.GetRMSError())
	    h_uperp_rawmet_npv.SetBinContent(i + 1, h_uperp_rawmet.GetRMS())
	    h_uperp_rawmet_npv.SetBinError(i + 1, h_uperp_rawmet.GetRMSError())

	    h_scale_rawpuppi_npv.SetBinContent(i + 1, 1. * h_scale_rawpuppi.GetMean())
	    h_scale_rawpuppi_npv.SetBinError(i + 1, h_scale_rawpuppi.GetMeanError())
	    h_upara_rawpuppi_npv.SetBinContent(i + 1, h_upara_rawpuppi.GetRMS())
	    h_uparaboson_rawpuppi_npv.SetBinContent(i + 1, h_uparaboson_rawpuppi.GetRMS())
	    h_upara_rawpuppi_npv.SetBinError(i + 1, h_upara_rawpuppi.GetRMSError())
	    h_uparaboson_rawpuppi_npv.SetBinError(i + 1, h_uparaboson_rawpuppi.GetRMSError())
	    h_uperp_rawpuppi_npv.SetBinContent(i + 1, h_uperp_rawpuppi.GetRMS())
	    h_uperp_rawpuppi_npv.SetBinError(i + 1, h_uperp_rawpuppi.GetRMSError())

	    h_scale_t1_npv.SetBinContent(i + 1, 1. * h_scale_t1.GetMean())
	    h_scale_t1_npv.SetBinError(i + 1, h_scale_t1.GetMeanError())
	    h_upara_t1_npv.SetBinContent(i + 1, h_upara_t1.GetRMS())
	    h_uparaboson_t1_npv.SetBinContent(i + 1, h_uparaboson_t1.GetRMS())
	    h_upara_t1_npv.SetBinError(i + 1,  h_upara_t1.GetRMSError())
	    h_uparaboson_t1_npv.SetBinError(i + 1,  h_uparaboson_t1.GetRMSError())
	    h_uperp_t1_npv.SetBinContent(i + 1, h_uperp_t1.GetRMS())
	    h_uperp_t1_npv.SetBinError(i + 1, h_uperp_t1.GetRMSError())
	    if isMC : 
		h_scale_t1smear_npv.SetBinContent(i + 1, 1. * h_scale_t1smear.GetMean())
		h_scale_t1smear_npv.SetBinError(i + 1, h_scale_t1smear.GetMeanError())
		h_upara_t1smear_npv.SetBinContent(i + 1, h_upara_t1smear.GetRMS())
		h_uparaboson_t1smear_npv.SetBinContent(i + 1, h_uparaboson_t1smear.GetRMS())
		h_upara_t1smear_npv.SetBinError(i + 1, h_upara_t1smear.GetRMSError())
		h_uparaboson_t1smear_npv.SetBinError(i + 1, h_uparaboson_t1smear.GetRMSError())
		h_uperp_t1smear_npv.SetBinContent(i + 1, h_uperp_t1smear.GetRMS())
		h_uperp_t1smear_npv.SetBinError(i + 1, h_uperp_t1smear.GetRMSError())


	    h_scale_puppi_npv.SetBinContent(i + 1, 1. * h_scale_puppi.GetMean())
	    h_scale_puppi_npv.SetBinError(i + 1, h_scale_puppi.GetMeanError())
	    h_upara_puppi_npv.SetBinContent(i + 1,  h_upara_puppi.GetRMS())
	    h_uparaboson_puppi_npv.SetBinContent(i + 1,  h_uparaboson_puppi.GetRMS())
	    h_upara_puppi_npv.SetBinError(i + 1, h_upara_puppi.GetRMSError())
	    h_uparaboson_puppi_npv.SetBinError(i + 1, h_uparaboson_puppi.GetRMSError())
	    h_uperp_puppi_npv.SetBinContent(i + 1, h_uperp_puppi.GetRMS())
	    h_uperp_puppi_npv.SetBinError(i + 1, h_uperp_puppi.GetRMSError())




	    h_scale_perp_rawmet_npv.SetBinContent(i + 1, 1. * h_scale_perp_rawmet.GetMean())
	    h_scale_perp_rawmet_npv.SetBinError(i + 1, h_scale_perp_rawmet.GetMeanError())

	    h_scale_perp_rawpuppi_npv.SetBinContent(i + 1, 1. * h_scale_perp_rawpuppi.GetMean())
	    h_scale_perp_rawpuppi_npv.SetBinError(i + 1, h_scale_perp_rawpuppi.GetMeanError())

	    h_scale_perp_t1_npv.SetBinContent(i + 1, 1. * h_scale_perp_t1.GetMean())
	    h_scale_perp_t1_npv.SetBinError(i + 1, h_scale_perp_t1.GetMeanError())
	    if isMC : 
		h_scale_perp_t1smear_npv.SetBinContent(i + 1, 1. * h_scale_perp_t1smear.GetMean())
		h_scale_perp_t1smear_npv.SetBinError(i + 1, h_scale_perp_t1smear.GetMeanError())


	    h_scale_perp_puppi_npv.SetBinContent(i + 1, 1. * h_scale_perp_puppi.GetMean())
	    h_scale_perp_puppi_npv.SetBinError(i + 1, h_scale_perp_puppi.GetMeanError())



	    outrawmetdn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_rawmet.GetMean(), h_scale_rawmet.GetMeanError(), h_upara_rawmet.GetRMS(), h_upara_rawmet.GetRMSError(), h_uperp_rawmet.GetRMS(), h_uperp_rawmet.GetRMSError(), h_scale_perp_rawmet.GetMean(), h_scale_perp_rawmet.GetMeanError()))
	    #outrawmetdn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_rawmet.GetMean(), h_scale_rawmet.GetMeanError(), h_uparaboson_rawmet.GetRMS(), h_uparaboson_rawmet.GetRMSError(), h_uperp_rawmet.GetRMS(), h_uperp_rawmet.GetRMSError(), h_scale_perp_rawmet.GetMean(), h_scale_perp_rawmet.GetMeanError()))

	    outrawpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_rawpuppi.GetMean(), h_scale_rawpuppi.GetMeanError(), h_upara_rawpuppi.GetRMS(), h_upara_rawpuppi.GetRMSError(), h_uperp_rawpuppi.GetRMS(), h_uperp_rawpuppi.GetRMSError(), h_scale_perp_rawpuppi.GetMean(), h_scale_perp_rawpuppi.GetMeanError()))
	    #outrawpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_rawpuppi.GetMean(), h_scale_rawpuppi.GetMeanError(), h_uparaboson_rawpuppi.GetRMS(), h_uparaboson_rawpuppi.GetRMSError(), h_uperp_rawpuppi.GetRMS(), h_uperp_rawpuppi.GetRMSError(), h_scale_perp_rawpuppi.GetMean(), h_scale_perp_rawpuppi.GetMeanError()))

	    outt1dn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_t1.GetMean(), h_scale_t1.GetMeanError(), h_upara_t1.GetRMS(), h_upara_t1.GetRMSError(), h_uperp_t1.GetRMS(), h_uperp_t1.GetRMSError(), h_scale_perp_t1.GetMean(), h_scale_perp_t1.GetMeanError()))
	    #outt1dn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_t1.GetMean(), h_scale_t1.GetMeanError(), h_uparaboson_t1.GetRMS(), h_uparaboson_t1.GetRMSError(), h_uperp_t1.GetRMS(), h_uperp_t1.GetRMSError(), h_scale_perp_t1.GetMean(), h_scale_perp_t1.GetMeanError()))
	    if isMC:
		outt1smeardn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_t1smear.GetMean(), h_scale_t1smear.GetMeanError(), h_upara_t1smear.GetRMS(), h_upara_t1smear.GetRMSError(), h_uperp_t1smear.GetRMS(), h_uperp_t1smear.GetRMSError(), h_scale_perp_t1smear.GetMean(), h_scale_perp_t1smear.GetMeanError()))
		#outt1smeardn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_t1smear.GetMean(), h_scale_t1smear.GetMeanError(), h_uparaboson_t1smear.GetRMS(), h_uparaboson_t1smear.GetRMSError(), h_uperp_t1smear.GetRMS(), h_uperp_t1smear.GetRMSError(), h_scale_perp_t1smear.GetMean(), h_scale_perp_t1smear.GetMeanError()))

	    #outpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_puppi.GetMean(), h_scale_puppi.GetMeanError(), h_upara_puppi.GetRMS(), h_upara_puppi.GetRMSError(), h_uperp_puppi.GetRMS(), h_uperp_puppi.GetRMSError(), h_scale_perp_puppi.GetMean(), h_scale_perp_puppi.GetMeanError()))
	    outpuppidn.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cuts_npv[i], h_scale_puppi.GetMean(), h_scale_puppi.GetMeanError(), h_uparaboson_puppi.GetRMS(), h_uparaboson_puppi.GetRMSError(), h_uperp_puppi.GetRMS(), h_uperp_puppi.GetRMSError(), h_scale_perp_puppi.GetMean(), h_scale_perp_puppi.GetMeanError()))





    file0 = ROOT.TFile("out.root", "RECREATE")


    h_scale_rawmet_vspt.Write()
    h_scale_rawpuppi_vspt.Write()
    h_scale_t1_vspt.Write()
    h_scale_t1smear_vspt.Write()
    h_scale_puppi_vspt.Write()
    h_scale_perp_rawmet_vspt.Write()
    h_scale_perp_rawpuppi_vspt.Write()
    h_scale_perp_t1_vspt.Write()
    h_scale_perp_t1smear_vspt.Write()
    h_scale_perp_puppi_vspt.Write()


    h_upara_rawmet_vspt.Write()
    h_uparaboson_rawmet_vspt.Write()
    h_upara_rawpuppi_vspt.Write()
    h_uparaboson_rawpuppi_vspt.Write()
    h_upara_t1smear_vspt.Write()
    h_uparaboson_t1smear_vspt.Write()
    h_upara_puppi_vspt.Write()
    h_uparaboson_puppi_vspt.Write()
    h_uperp_rawmet_vspt.Write()
    h_uperp_rawpuppi_vspt.Write()
    h_uperp_t1smear_vspt.Write()
    h_uperp_puppi_vspt.Write()



    h_scale_rawmet_npv.Write()
    h_scale_rawpuppi_npv.Write()
    h_scale_t1_npv.Write()
    h_scale_t1smear_npv.Write()
    h_scale_puppi_npv.Write()

    h_scale_perp_rawmet_npv.Write()
    h_scale_perp_rawpuppi_npv.Write()
    h_scale_perp_t1_npv.Write()
    h_scale_perp_t1smear_npv.Write()
    h_scale_perp_puppi_npv.Write()

    h_upara_rawmet_npv.Write()
    h_uparaboson_rawmet_npv.Write()
    h_upara_rawpuppi_npv.Write()
    h_uparaboson_rawpuppi_npv.Write()
    h_upara_t1_npv.Write()
    h_uparaboson_t1_npv.Write()
    h_upara_t1smear_npv.Write()
    h_uparaboson_t1smear_npv.Write()
    h_upara_puppi_npv.Write()
    h_uparaboson_puppi_npv.Write()
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

extract2()
