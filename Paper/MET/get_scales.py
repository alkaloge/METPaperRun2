import ROOT
from ROOT import gROOT, gStyle, TChain, TFile, TH1F, TString, TH1, kTRUE, kFALSE, kBlack
from array import array
import sys, os
def create1DEmptyhistoVarBins(name, bins, varbins, color, style):
    TH1.SetDefaultSumw2(kTRUE)

    hTemp = TH1F(name, name, bins, varbins)
    hTemp.SetLineWidth(3)
    hTemp.SetMarkerSize(0)
    hTemp.SetLineColor(color)
    hTemp.SetLineStyle(style)

    return hTemp


def create1DEmptyhisto(name, bins, xmin, xmax, color, style):
    TH1.SetDefaultSumw2(kTRUE)

    hTemp = TH1F(name, name, bins, xmin, xmax)
    hTemp.SetLineWidth(3)
    hTemp.SetMarkerSize(0)
    hTemp.SetLineColor(color)
    hTemp.SetLineStyle(style)

    return hTemp

def create1DhistoVarBins(tree, intLumi, cuts, branch, bins, varbins, useLog, color, style, name, norm, data):
    TH1.SetDefaultSumw2(kTRUE)

    cut = "(" + cuts + ")"

    hTemp = TH1F(name, name, bins, varbins)
    tree.Project(name, branch, cut)

    hTemp.SetLineWidth(3)
    hTemp.SetMarkerSize(0)
    hTemp.SetLineColor(color)
    hTemp.SetLineStyle(style)

    # Add overflow bin
    error = 0.
    integral = hTemp.IntegralAndError(bins, bins+1, error)
    hTemp.SetBinContent(bins, integral)
    hTemp.SetBinError(bins, error)

    if norm:
        hTemp.Scale(1. / hTemp.Integral())

    return hTemp


def create1Dhisto(tree, intLumi, cuts, branch, bins, xmin, xmax, useLog, color, style, name, norm, data):
    TH1.SetDefaultSumw2(kTRUE)

    cut = "(" + cuts + ")"

    hTemp = TH1F(name, name, bins, xmin, xmax)
    #tree.Project(name, branch, cut)
    tree.Project(name, branch, cut, "", 10000)

    hTemp.SetLineWidth(3)
    hTemp.SetMarkerSize(0)
    hTemp.SetLineColor(color)
    hTemp.SetLineStyle(style)

    # Add overflow bin
    error = ROOT.Double(0.0)
    integral = hTemp.IntegralAndError(bins, bins + 1, error)
    hTemp.SetBinContent(bins, integral)
    hTemp.SetBinError(bins, error)

    if norm:
        hTemp.Scale(1.0 / hTemp.Integral())

    return hTemp





def get_scales():
    #python get_scales.py ismc MuMu 2018 dy
    isMC=False
    channel=None
    if str(sys.argv[1]) == "1"  or str(sys.argv[1]).lower()  == "ismc" :  isMC = True
    channel = str(sys.argv[2])
    year = str(sys.argv[3])
    process = 'dy'
    if year == "2017 ": lumi = 41.48

    if year == "2018":  lumi = 59.83
    if year == "2016":  lumi = 19.35
    if year == "2016postVFP": lumi = 16.98
    if year == "2016preVFP": lumi = 19.35

    xsecslist = {
    "DYJets": 6077,
    "DYJetsNLO": 6529,
    }
    xsec = None
    for sample, xsec in xsecslist.items():
	if process.lower() in sample.lower():
	    selected_xsec = xsec
	    break


    print "year", year, "lumi", lumi, "isMC", "channel", channel, " process", process, "xsec", xsec
    #sys.exit(1)
    njets = -1
    sjets = "gt0" if njets < 0 else "geq0"

    gROOT.SetBatch(False)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1)
    gStyle.SetPalette(1)

    gROOT.SetBatch(True)
    t_ = TChain("Events")

    #input_files = sys.argv[1:]
    #for file in input_files:
    #fileIn = "inFile.root"
    t_.Add("inFile.root")
    #t_.Add("/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/SingleMuon_Run2018A/SingleMuon_Run2018A_2018.root")

    print("Number of entries:", t_.GetEntries())
    TFileOut = "output.root"
    fileOut = TFile(TFileOut, "RECREATE")
    
    fileI = ROOT.TFile("inFile.root", "READ")
    if isMC : 
        hW = fileI.Get("hWeights")
        fileOut.cd()
        hW.Write()

    cuts = [
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
    varbins = array('d', [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.])
    bins = len(varbins) - 1

    print "trying the nPVGood bins"

    cuts_npv = [
        "(0<=nPVGood && nPVGood<10)",
        "(10<=nPVGood && nPVGood<20)",
        "(20<=nPVGood && nPVGood<30)",
        "(30<=nPVGood && nPVGood<40)",
        "(40<=nPVGood && nPVGood<50)",
        "(50<=nPVGood && nPVGood<60)",
        "(60<=nPVGood)"
    ]
    varbins_npv = array('d', [0., 10., 20., 30., 40., 50., 60., 70.])
    bins_npv = len(varbins_npv) - 1

    print "done with bins"


    h_scale_rawmet_vspt = create1DEmptyhistoVarBins("h_scale_rawmet_vspt", bins, varbins, 1, 1)
    h_resperp_rawmet_vspt = create1DEmptyhistoVarBins("h_resperp_rawmet_vspt", bins, varbins, 1, 1)
    h_respara_rawmet_vspt = create1DEmptyhistoVarBins("h_respara_rawmet_vspt", bins, varbins, 1, 1)

    h_scale_rawmet_npv = create1DEmptyhistoVarBins("h_scale_rawmet_npv", bins_npv, varbins_npv, 1, 1)
    h_resperp_rawmet_npv = create1DEmptyhistoVarBins("h_resperp_rawmet_npv", bins_npv, varbins_npv, 1, 1)
    h_respara_rawmet_npv = create1DEmptyhistoVarBins("h_respara_rawmet_npv", bins_npv, varbins_npv, 1, 1)

    h_scale_rawpuppi_vspt = create1DEmptyhistoVarBins("h_scale_rawpuppi_vspt", bins, varbins, 1, 1)
    h_resperp_rawpuppi_vspt = create1DEmptyhistoVarBins("h_resperp_rawpuppi_vspt", bins, varbins, 1, 1)
    h_respara_rawpuppi_vspt = create1DEmptyhistoVarBins("h_respara_rawpuppi_vspt", bins, varbins, 1, 1)

    h_scale_rawpuppi_npv = create1DEmptyhistoVarBins("h_scale_rawpuppi_npv", bins_npv, varbins_npv, 1, 1)
    h_resperp_rawpuppi_npv = create1DEmptyhistoVarBins("h_resperp_rawpuppi_npv", bins_npv, varbins_npv, 1, 1)
    h_respara_rawpuppi_npv = create1DEmptyhistoVarBins("h_respara_rawpuppi_npv", bins_npv, varbins_npv, 1, 1)

    h_scale_t1_vspt = create1DEmptyhistoVarBins("h_scale_t1_vspt", bins, varbins, 2, 1)
    h_resperp_t1_vspt = create1DEmptyhistoVarBins("h_resperp_t1_vspt", bins, varbins, 2, 1)
    h_respara_t1_vspt = create1DEmptyhistoVarBins("h_respara_t1_vspt", bins, varbins, 2, 1)

    h_scale_t1_npv = create1DEmptyhistoVarBins("h_scale_t1_npv", bins_npv, varbins_npv, 2, 1)
    h_resperp_t1_npv = create1DEmptyhistoVarBins("h_resperp_t1_npv", bins_npv, varbins_npv, 2, 1)
    h_respara_t1_npv = create1DEmptyhistoVarBins("h_respara_t1_npv", bins_npv, varbins_npv, 2, 1)

    h_scale_t1smear_vspt = create1DEmptyhistoVarBins("h_scale_t1smear_vspt", bins, varbins, 2, 1)
    h_resperp_t1smear_vspt = create1DEmptyhistoVarBins("h_resperp_t1smear_vspt", bins, varbins, 2, 1)
    h_respara_t1smear_vspt = create1DEmptyhistoVarBins("h_respara_t1smear_vspt", bins, varbins, 2, 1)

    h_scale_t1smear_npv = create1DEmptyhistoVarBins("h_scale_t1smear_npv", bins_npv, varbins_npv, 2, 1)
    h_resperp_t1smear_npv = create1DEmptyhistoVarBins("h_resperp_t1smear_npv", bins_npv, varbins_npv, 2, 1)
    h_respara_t1smear_npv = create1DEmptyhistoVarBins("h_respara_t1smear_npv", bins_npv, varbins_npv, 2, 1)

    h_scale_puppi_vspt = create1DEmptyhistoVarBins("h_scale_puppi_vspt", bins, varbins, 3, 1)
    h_resperp_puppi_vspt = create1DEmptyhistoVarBins("h_resperp_puppi_vspt", bins, varbins, 3, 1)
    h_respara_puppi_vspt = create1DEmptyhistoVarBins("h_respara_puppi_vspt", bins, varbins, 3, 1)

    h_scale_puppi_npv = create1DEmptyhistoVarBins("h_scale_puppi_npv", bins_npv, varbins_npv, 3, 1)
    h_resperp_puppi_npv = create1DEmptyhistoVarBins("h_resperp_puppi_npv", bins_npv, varbins_npv, 3, 1)
    h_respara_puppi_npv = create1DEmptyhistoVarBins("h_respara_puppi_npv", bins_npv, varbins_npv, 3, 1)



    jcut = " (nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 && fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>0 && nbtagL[0]==0.0 && cat==2 )"
    if channel == "ElEl": jcut = " ( nElectron[0]==2 && Flag_BadPFMuonDzFilter[0]==1  &&  !(fabs(eta_1[0])>1.4442 &&  fabs(eta_1[0])<1.5660) && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 &&   !(fabs(eta_2[0])>1.4442 &&  fabs(eta_2[0])<1.5660) && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 &&  fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat==1  &&njets[0]>0   && nbtagL[0]==0.0 && Electron_convVeto[0] > 0 && Electron_lostHits[0]<1 )"


    if njets < 0:
	jcut = " (nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 && fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>=0 && nbtagL[0]==0.0 && cat==2 )"
	#jcutmc = "  ((nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 && fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>=0 && nbtagL[0]==0.0 && cat==2 ) * ( weight[0] ) * fabs( weightPUtrue[0] ) * ( L1PreFiringWeight_Nom[0] ) * ( IDSF ) * ( TrigSF ) * ( IsoSF ) )"

        if channel == "ElEl":
            jcut = " ( nElectron[0]==2 && Flag_BadPFMuonDzFilter[0]==1  &&  !(fabs(eta_1[0])>1.4442 &&  fabs(eta_1[0])<1.5660) && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15 &&   !(fabs(eta_2[0])>1.4442 &&  fabs(eta_2[0])<1.5660) && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2 &&  fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && cat==1  &&njets[0]>=0   && nbtagL[0]==0.0 && Electron_convVeto[0] > 0 && Electron_lostHits[0]<1 )"

    extra_conditions = "( weight[0]  * fabs(weightPUtrue[0]) * L1PreFiringWeight_Nom[0] * IDSF * TrigSF * IsoSF)"

    jcutmc = jcut + " * " + extra_conditions

    if isMC : jcut = jcutmc

    print 'Cut ', isMC, jcutmc
    # Open the input root file
    #fileOut = TFile("output_vsptvspu_{}.root".format(str(year)), "RECREATE")

    # Loop over cuts
    for i0 in xrange(len(cuts)):
	fileOut.cd()
	folder = fileOut.mkdir("Folder_%d_vspt" % i0)
	folder.cd()

	h_scale0_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_RawMET)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_rawmet", False, False)
	h_upara_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_RawMET)", 100, -500., 500., False, kBlack, 1, "h_upara_rawmet", False, False)
	h_uperp_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "-u_perp_RawMET", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_rawmet", False, False)

	h_scale0_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_RawPuppiMET)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_rawpuppi", False, False)
	h_upara_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_RawPuppiMET)", 100, -500., 500., False, kBlack, 1, "h_upara_rawpuppi", False, False)
	h_uperp_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "-u_perp_RawPuppiMET", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_rawpuppi", False, False)

	h_scale0_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_METCorGood_T1)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_t1", False, False)
	h_upara_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_METCorGood_T1)", 100, -500., 500., False, kBlack, 1, "h_upara_t1", False, False)
	h_uperp_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "-u_perp_METCorGood_T1", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_t1", False, False)

	h_scale0_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_METCorGood_T1Smear)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_t1smear", False, False)
	h_upara_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_METCorGood_T1Smear)", 100, -500., 500., False, kBlack, 1, "h_upara_t1smear", False, False)
	h_uperp_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "-u_perp_METCorGood_T1Smear", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_t1smear", False, False)

	h_scale0_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_PuppiMETCorGood)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_puppi", False, False)
	h_upara_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "(-u_par_PuppiMETCorGood)", 100, -500., 500., False, kBlack, 1, "h_upara_puppi", False, False)
	h_uperp_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts[i0], "-u_perp_PuppiMETCorGood", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_puppi", False, False)



	h_scale0_rawmet.Sumw2()
	h_scale0_rawpuppi.Sumw2()
	h_scale0_t1.Sumw2()
	h_scale0_t1smear.Sumw2()
	h_upara_rawmet.Sumw2()
	h_upara_rawpuppi.Sumw2()
	h_upara_t1.Sumw2()
	h_upara_t1smear.Sumw2()
	h_uperp_rawmet.Sumw2()
	h_uperp_rawpuppi.Sumw2()
	h_uperp_t1.Sumw2()
	h_uperp_t1smear.Sumw2()

	scalecor_rawmet = 1.
	if h_scale0_rawmet.GetMean() != 0:
	    scalecor_rawmet = 1. / h_scale0_rawmet.GetMean()

	scalecor_rawpuppi = 1.
	if h_scale0_rawpuppi.GetMean() != 0:
	    scalecor_rawpuppi = 1. / h_scale0_rawpuppi.GetMean()

	scalecor_t1 = 1.
	if h_scale0_t1.GetMean() != 0:
	    scalecor_t1 = 1. / h_scale0_t1.GetMean()

	scalecor_t1smear = 1.
	if h_scale0_t1smear.GetMean() != 0:
	    scalecor_t1smear = 1. / h_scale0_t1smear.GetMean()

	scalecor_puppi = 1.
	if h_scale0_puppi.GetMean() != 0:
	    scalecor_puppi = 1. / h_scale0_puppi.GetMean()

	h_scale_rawmet_vspt.SetBinContent(i0 + 1, 1. * h_scale0_rawmet.GetMean())
	h_scale_rawmet_vspt.SetBinError(i0 + 1, h_scale0_rawmet.GetMeanError())
	h_respara_rawmet_vspt.SetBinContent(i0 + 1, scalecor_rawmet * h_upara_rawmet.GetRMS())
	h_respara_rawmet_vspt.SetBinError(i0 + 1, scalecor_rawmet * h_upara_rawmet.GetRMSError())
	h_resperp_rawmet_vspt.SetBinContent(i0 + 1, scalecor_rawmet * h_uperp_rawmet.GetRMS())
	h_resperp_rawmet_vspt.SetBinError(i0 + 1, scalecor_rawmet * h_uperp_rawmet.GetRMSError())

	h_scale_rawpuppi_vspt.SetBinContent(i0 + 1, 1. * h_scale0_rawpuppi.GetMean())
	h_scale_rawpuppi_vspt.SetBinError(i0 + 1, h_scale0_rawpuppi.GetMeanError())
	h_respara_rawpuppi_vspt.SetBinContent(i0 + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMS())
	h_respara_rawpuppi_vspt.SetBinError(i0 + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMSError())
	h_resperp_rawpuppi_vspt.SetBinContent(i0 + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMS())
	h_resperp_rawpuppi_vspt.SetBinError(i0 + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMSError())

	h_scale_t1_vspt.SetBinContent(i0 + 1, 1. * h_scale0_t1.GetMean())
	h_scale_t1_vspt.SetBinError(i0 + 1, h_scale0_t1.GetMeanError())
	h_respara_t1_vspt.SetBinContent(i0 + 1, scalecor_t1 * h_upara_t1.GetRMS())
	h_respara_t1_vspt.SetBinError(i0 + 1, scalecor_t1 * h_upara_t1.GetRMSError())
	h_resperp_t1_vspt.SetBinContent(i0 + 1, scalecor_t1 * h_uperp_t1.GetRMS())
	h_resperp_t1_vspt.SetBinError(i0 + 1, scalecor_t1 * h_uperp_t1.GetRMSError())

	h_scale_t1smear_vspt.SetBinContent(i0 + 1, 1. * h_scale0_t1smear.GetMean())
	h_scale_t1smear_vspt.SetBinError(i0 + 1, h_scale0_t1smear.GetMeanError())
	h_respara_t1smear_vspt.SetBinContent(i0 + 1, scalecor_t1smear * h_upara_t1smear.GetRMS())
	h_respara_t1smear_vspt.SetBinError(i0 + 1, scalecor_t1smear * h_upara_t1smear.GetRMSError())
	h_resperp_t1smear_vspt.SetBinContent(i0 + 1, scalecor_t1smear * h_uperp_t1smear.GetRMS())
	h_resperp_t1smear_vspt.SetBinError(i0 + 1, scalecor_t1smear * h_uperp_t1smear.GetRMSError())

	h_scale_puppi_vspt.SetBinContent(i0 + 1, 1. * h_scale0_puppi.GetMean())
	h_scale_puppi_vspt.SetBinError(i0 + 1, h_scale0_puppi.GetMeanError())
	h_respara_puppi_vspt.SetBinContent(i0 + 1, scalecor_puppi * h_upara_puppi.GetRMS())
	h_respara_puppi_vspt.SetBinError(i0 + 1, scalecor_puppi * h_upara_puppi.GetRMSError())
	h_resperp_puppi_vspt.SetBinContent(i0 + 1, scalecor_puppi * h_uperp_puppi.GetRMS())
	h_resperp_puppi_vspt.SetBinError(i0 + 1, scalecor_puppi * h_uperp_puppi.GetRMSError())

	h_scale0_rawmet.Write()
	h_upara_rawmet.Write()
	h_uperp_rawmet.Write()

	h_scale0_rawpuppi.Write()
	h_upara_rawpuppi.Write()
	h_uperp_rawpuppi.Write()

	h_scale0_t1.Write()
	h_upara_t1.Write()
	h_uperp_t1.Write()

	h_scale0_t1smear.Write()
	h_upara_t1smear.Write()
	h_uperp_t1smear.Write()

	h_scale0_puppi.Write()
	h_upara_puppi.Write()
	h_uperp_puppi.Write()

	h_scale0_rawmet.Delete()
	h_upara_rawmet.Delete()
	h_uperp_rawmet.Delete()

	h_scale0_rawpuppi.Delete()
	h_upara_rawpuppi.Delete()
	h_uperp_rawpuppi.Delete()

	h_scale0_t1.Delete()
	h_upara_t1.Delete()
	h_uperp_t1.Delete()

	h_scale0_t1smear.Delete()
	h_upara_t1smear.Delete()
	h_uperp_t1smear.Delete()

	h_scale0_puppi.Delete()
	h_upara_puppi.Delete()
	h_uperp_puppi.Delete()


    for i0 in xrange(len(cuts_npv)):
	fileOut.cd()
	folder = fileOut.mkdir("Folder_%d_npv" % i0)
	folder.cd()
        print 'cut_npv', cuts_npv[i0], i0
	h_scale0_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_RawMET)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_rawmet", False, False)
	h_upara_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_RawMET)", 100, -500., 500., False, kBlack, 1, "h_upara_rawmet", False, False)
	h_uperp_rawmet = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "-u_perp_RawMET", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_rawmet", False, False)

	h_scale0_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_RawPuppiMET)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_rawpuppi", False, False)
	h_upara_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_RawPuppiMET)", 100, -500., 500., False, kBlack, 1, "h_upara_rawpuppi", False, False)
	h_uperp_rawpuppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "-u_perp_RawPuppiMET", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_rawpuppi", False, False)

	h_scale0_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_METCorGood_T1)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_t1", False, False)
	h_upara_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_METCorGood_T1)", 100, -500., 500., False, kBlack, 1, "h_upara_t1", False, False)
	h_uperp_t1 = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "-u_perp_METCorGood_T1", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_t1", False, False)

	h_scale0_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_METCorGood_T1Smear)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_t1smear", False, False)
	h_upara_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_METCorGood_T1Smear)", 100, -500., 500., False, kBlack, 1, "h_upara_t1smear", False, False)
	h_uperp_t1smear = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "-u_perp_METCorGood_T1Smear", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_t1smear", False, False)

	h_scale0_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_PuppiMETCorGood)/boson_pt", 4000, -100., 100., False, kBlack, 1, "h_scale0_puppi", False, False)
	h_upara_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "(-u_par_PuppiMETCorGood)", 100, -500., 500., False, kBlack, 1, "h_upara_puppi", False, False)
	h_uperp_puppi = create1Dhisto(t_, "1.", jcut + " && " + cuts_npv[i0], "-u_perp_PuppiMETCorGood", 20000, -1000., 1000., False, kBlack, 1, "h_uperp_puppi", False, False)



	h_scale0_rawmet.Sumw2()
	h_scale0_rawpuppi.Sumw2()
	h_scale0_t1.Sumw2()
	h_scale0_t1smear.Sumw2()
	h_upara_rawmet.Sumw2()
	h_upara_rawpuppi.Sumw2()
	h_upara_t1.Sumw2()
	h_upara_t1smear.Sumw2()
	h_uperp_rawmet.Sumw2()
	h_uperp_rawpuppi.Sumw2()
	h_uperp_t1.Sumw2()
	h_uperp_t1smear.Sumw2()

	scalecor_rawmet = 1.
	if h_scale0_rawmet.GetMean() != 0:
	    scalecor_rawmet = 1. / h_scale0_rawmet.GetMean()

	scalecor_rawpuppi = 1.
	if h_scale0_rawpuppi.GetMean() != 0:
	    scalecor_rawpuppi = 1. / h_scale0_rawpuppi.GetMean()

	scalecor_t1 = 1.
	if h_scale0_t1.GetMean() != 0:
	    scalecor_t1 = 1. / h_scale0_t1.GetMean()

	scalecor_t1smear = 1.
	if h_scale0_t1smear.GetMean() != 0:
	    scalecor_t1smear = 1. / h_scale0_t1smear.GetMean()

	scalecor_puppi = 1.
	if h_scale0_puppi.GetMean() != 0:
	    scalecor_puppi = 1. / h_scale0_puppi.GetMean()

	h_scale_rawmet_npv.SetBinContent(i0 + 1, 1. * h_scale0_rawmet.GetMean())
	h_scale_rawmet_npv.SetBinError(i0 + 1, h_scale0_rawmet.GetMeanError())
	h_respara_rawmet_npv.SetBinContent(i0 + 1, scalecor_rawmet * h_upara_rawmet.GetRMS())
	h_respara_rawmet_npv.SetBinError(i0 + 1, scalecor_rawmet * h_upara_rawmet.GetRMSError())
	h_resperp_rawmet_npv.SetBinContent(i0 + 1, scalecor_rawmet * h_uperp_rawmet.GetRMS())
	h_resperp_rawmet_npv.SetBinError(i0 + 1, scalecor_rawmet * h_uperp_rawmet.GetRMSError())

	h_scale_rawpuppi_npv.SetBinContent(i0 + 1, 1. * h_scale0_rawpuppi.GetMean())
	h_scale_rawpuppi_npv.SetBinError(i0 + 1, h_scale0_rawpuppi.GetMeanError())
	h_respara_rawpuppi_npv.SetBinContent(i0 + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMS())
	h_respara_rawpuppi_npv.SetBinError(i0 + 1, scalecor_rawpuppi * h_upara_rawpuppi.GetRMSError())
	h_resperp_rawpuppi_npv.SetBinContent(i0 + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMS())
	h_resperp_rawpuppi_npv.SetBinError(i0 + 1, scalecor_rawpuppi * h_uperp_rawpuppi.GetRMSError())

	h_scale_t1_npv.SetBinContent(i0 + 1, 1. * h_scale0_t1.GetMean())
	h_scale_t1_npv.SetBinError(i0 + 1, h_scale0_t1.GetMeanError())
	h_respara_t1_npv.SetBinContent(i0 + 1, scalecor_t1 * h_upara_t1.GetRMS())
	h_respara_t1_npv.SetBinError(i0 + 1, scalecor_t1 * h_upara_t1.GetRMSError())
	h_resperp_t1_npv.SetBinContent(i0 + 1, scalecor_t1 * h_uperp_t1.GetRMS())
	h_resperp_t1_npv.SetBinError(i0 + 1, scalecor_t1 * h_uperp_t1.GetRMSError())

	h_scale_t1smear_npv.SetBinContent(i0 + 1, 1. * h_scale0_t1smear.GetMean())
	h_scale_t1smear_npv.SetBinError(i0 + 1, h_scale0_t1smear.GetMeanError())
	h_respara_t1smear_npv.SetBinContent(i0 + 1, scalecor_t1smear * h_upara_t1smear.GetRMS())
	h_respara_t1smear_npv.SetBinError(i0 + 1, scalecor_t1smear * h_upara_t1smear.GetRMSError())
	h_resperp_t1smear_npv.SetBinContent(i0 + 1, scalecor_t1smear * h_uperp_t1smear.GetRMS())
	h_resperp_t1smear_npv.SetBinError(i0 + 1, scalecor_t1smear * h_uperp_t1smear.GetRMSError())

	h_scale_puppi_npv.SetBinContent(i0 + 1, 1. * h_scale0_puppi.GetMean())
	h_scale_puppi_npv.SetBinError(i0 + 1, h_scale0_puppi.GetMeanError())
	h_respara_puppi_npv.SetBinContent(i0 + 1, scalecor_puppi * h_upara_puppi.GetRMS())
	h_respara_puppi_npv.SetBinError(i0 + 1, scalecor_puppi * h_upara_puppi.GetRMSError())
	h_resperp_puppi_npv.SetBinContent(i0 + 1, scalecor_puppi * h_uperp_puppi.GetRMS())
	h_resperp_puppi_npv.SetBinError(i0 + 1, scalecor_puppi * h_uperp_puppi.GetRMSError())

	h_scale0_rawmet.Write()
	h_upara_rawmet.Write()
	h_uperp_rawmet.Write()

	h_scale0_rawpuppi.Write()
	h_upara_rawpuppi.Write()
	h_uperp_rawpuppi.Write()

	h_scale0_t1.Write()
	h_upara_t1.Write()
	h_uperp_t1.Write()

	h_scale0_t1smear.Write()
	h_upara_t1smear.Write()
	h_uperp_t1smear.Write()

	h_scale0_puppi.Write()
	h_upara_puppi.Write()
	h_uperp_puppi.Write()

	h_scale0_rawmet.Delete()
	h_upara_rawmet.Delete()
	h_uperp_rawmet.Delete()

	h_scale0_rawpuppi.Delete()
	h_upara_rawpuppi.Delete()
	h_uperp_rawpuppi.Delete()

	h_scale0_t1.Delete()
	h_upara_t1.Delete()
	h_uperp_t1.Delete()

	h_scale0_t1smear.Delete()
	h_upara_t1smear.Delete()
	h_uperp_t1smear.Delete()

	h_scale0_puppi.Delete()
	h_upara_puppi.Delete()
	h_uperp_puppi.Delete()

    
    fileOut.Write()
    fileOut.Close()





get_scales()



