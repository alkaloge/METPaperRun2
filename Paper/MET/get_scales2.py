import ROOT
from ROOT import gROOT, gStyle, TChain, TFile, TH1F, TString, TH1, kTRUE, kFALSE, kBlack
from array import array
import sys, os
import math
def create1DEmptyhistoVarBins(name, bins, varbins, color, style):
    TH1.SetDefaultSumw2(kTRUE)

    hTemp = TH1F(name, name, 400, -20., 20.)
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

    hTemp = TH1F(name, name, 400, -20., 20.)
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
    tree.Project(name, branch, cut)
    #tree.Project(name, branch, cut, "", 1000)

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
    Njet = str(sys.argv[4])
    fIn = str(sys.argv[5])
    if Njet=='eq0'  : sjets = '==0'
    elif Njet=='eq1'  : sjets = '==1'
    elif Njet=='geq1'  : sjets = '>=1'
    elif Njet=='incl' : sjets = '>=0'
    else : 
        print  ' sorry, you must define Njet from eq0, eq1 or incl'
        sys.exit(1)

    print "year", year,  "isMC", isMC, "channel", channel
    #sys.exit(1)

    gROOT.SetBatch(False)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1)
    gStyle.SetPalette(1)

    gROOT.SetBatch(True)
    t_ = TChain("Events")

    #input_files = sys.argv[1:]
    #for file in input_files:
    #fileIn = "inFile.root"
    t_.Add("inFile_{}".format(fIn))
    #t_.Add("/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/SingleMuon_Run2018A/SingleMuon_Run2018A_2018.root")

    print("Number of entries:", t_.GetEntries())
    TFileOut = "output_Njet{}.root".format(Njet)
    
    fileI = ROOT.TFile("inFile_{}".format(fIn), "READ")

    cuts = [
        "(0<=event.boson_pt and event.boson_pt<20)",
        "(20<=event.boson_pt and event.boson_pt<40)",
        "(40<=event.boson_pt and event.boson_pt<60)",
        "(60<=event.boson_pt and event.boson_pt<80)",
        "(80<=event.boson_pt and event.boson_pt<100)",
        "(100<=event.boson_pt and event.boson_pt<120)",
        "(120<=event.boson_pt and event.boson_pt<160)",
        "(160<=event.boson_pt and event.boson_pt<200)",
        "(200<=event.boson_pt and event.boson_pt<300)",
        "(300<=event.boson_pt)"
    ]
    varbins = array('d', [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.])
    bins = len(varbins) - 1

    print "trying the nPVGood bins"

    folder_names = {
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

    cuts_npv = [
        "(0<=event.nPVGood  and  event.nPVGood<10)",
        "(10<=event.nPVGood  and  event.nPVGood<20)",
        "(20<=event.nPVGood  and  event.nPVGood<30)",
        "(30<=event.nPVGood  and  event.nPVGood<40)",
        "(40<=event.nPVGood  and  event.nPVGood<50)",
        "(50<=event.nPVGood  and  event.nPVGood<60)",
        "(60<=event.nPVGood)"
    ]
    folder_names_npv = {
	"(0<=event.nPVGood  and  event.nPVGood<10)": "nPVGoodLt10",
	"(10<=event.nPVGood  and  event.nPVGood<20)": "nPVGoodGt10Lt20",
	"(20<=event.nPVGood  and  event.nPVGood<30)": "nPVGoodGt20Lt30",
	"(30<=event.nPVGood  and  event.nPVGood<40)": "nPVGoodGt30Lt40",
	"(40<=event.nPVGood  and  event.nPVGood<50)": "nPVGoodGt40Lt50",
	"(50<=event.nPVGood  and  event.nPVGood<60)": "nPVGoodGt50Lt60",
	"(60<=event.nPVGood)": "nPVGoodGt60"
    }
    varbins_npv = array('d', [0., 10., 20., 30., 40., 50., 60., 70.])
    bins_npv = len(varbins_npv) - 1

    print "done with bins"


    #jcut = " (nMuon==2  and  Flag_BadPFMuonDzFilter==1  and  math.fabs(d0_1)<0.045  and  math.fabs(dZ_1)<0.2  and  math.fabs(q_1)==1  and  iso_1 <= .15  and  math.fabs(d0_2)<0.045  and  math.fabs(dZ_2)<0.2  and  math.fabs(q_2)==1  and  iso_2 <= .15  and  nPVndof>4  and  math.fabs(PVz)<26  and  (PVy*PVy + PVx*PVx)<3  and  nPV>2  and  njets>0  and  nbtagL==0.0  and  cat==2 )"
    #if channel == "ElEl": jcut = " ( nElectron==2  and  Flag_BadPFMuonDzFilter==1   and   !(math.fabs(eta_1)>1.4442  and   math.fabs(eta_1)<1.5660)  and  math.fabs(d0_1)<0.045  and  math.fabs(dZ_1)<0.2  and  math.fabs(q_1)==1  and  iso_1 <= .15  and    !(math.fabs(eta_2)>1.4442  and   math.fabs(eta_2)<1.5660)  and  math.fabs(d0_2)<0.045  and  math.fabs(dZ_2)<0.2  and   math.fabs(q_2)==1  and  iso_2 <= .15  and  nPVndof>4  and  math.fabs(PVz)<26  and  (PVy*PVy + PVx*PVx)<3  and  nPV>2  and  cat==1   and njets>0    and  nbtagL==0.0  and  Electron_convVeto > 0  and  Electron_lostHits<1 )"
    jcut=''
    if channel == "MuMu":

        jcut = '(event.nMuon==2  and  event.Flag_BadPFMuonDzFilter==1  and  math.fabs(event.d0_1)<0.045  and  math.fabs(event.dZ_1)<0.2  and  math.fabs(event.q_1)==1  and  math.fabs(event.iso_1) <= .15  and  math.fabs(event.d0_2)<0.045  and  math.fabs(event.dZ_2)<0.2  and  math.fabs(event.q_2)==1  and  math.fabs(event.iso_2) <= .15  and  event.nPVndof>4  and  math.fabs(event.PVz)<26  and  (event.PVy*event.PVy + event.PVx*event.PVx)<3  and  event.nPVGood>2  and  event.njets{0:s}  and  event.nbtagL==0.0  and  event.cat==2 )'.format(str(sjets))
        jcut = '(event.nMuon==2  and  event.Flag_BadPFMuonDzFilter==1  and  math.fabs(event.d0_1)<0.045  and  math.fabs(event.dZ_1)<0.2  and  math.fabs(event.q_1)==1  and  math.fabs(event.iso_1) <= .15  and  math.fabs(event.d0_2)<0.045  and  math.fabs(event.dZ_2)<0.2  and  math.fabs(event.q_2)==1  and  math.fabs(event.iso_2) <= .15  and  event.nPVGood>2  and  event.njets{0:s}  and  event.cat==2 )'.format(str(sjets))

    if channel == "ElEl":
        jcut = " ( event.nElectron==2  and  event.Flag_BadPFMuonDzFilter==1  and   ( math.fabs(event.eta_1)<=1.4442 or math.fabs(event.eta_1)>=1.5660) and math.fabs(event.d0_1)<0.045  and  math.fabs(event.dZ_1)<0.2 and  event.q_1==1  and  event.iso_1 <= .15  and   (math.fabs(event.eta_2)<=1.4442 or math.fabs(event.eta_2)>=1.5660)   and  math.fabs(event.d0_2)<0.045  and  math.fabs(event.dZ_2)<0.2  and   math.fabs(event.q_2)==1  and  event.iso_2 <= .15  and  event.nPVndof>4  and  math.fabs(event.PVz)<26  and  (event.PVy*event.PVy + event.PVx*event.PVx)<3  and  event.nPVGood>2  and  event.cat==1   and event.njets{0:s}    and  event.nbtagL==0.0  and  event.Electron_convVeto > 0  and  event.Electron_lostHits<1 )".format(str(sjets))

        jcut = " ( event.nElectron==2  and  event.Flag_BadPFMuonDzFilter==1  and   ( math.fabs(event.eta_1)<=1.4442 or math.fabs(event.eta_1)>=1.5660) and math.fabs(event.d0_1)<0.045  and  math.fabs(event.dZ_1)<0.2 and  event.q_1==1  and  event.iso_1 <= .15  and   (math.fabs(event.eta_2)<=1.4442 or math.fabs(event.eta_2)>=1.5660)   and  math.fabs(event.d0_2)<0.045  and  math.fabs(event.dZ_2)<0.2  and   math.fabs(event.q_2)==1  and  event.iso_2 <= .15  and event.nPVGood>2  and  event.cat==1   and event.njets{0:s}    and  event.Electron_convVeto > 0  and  event.Electron_lostHits<1 )".format(str(sjets))

    if channel == "Gjets" : 
        #jcut = " (  event.Flag_BadPFMuonDzFilter==1 and  event.nPVndof>4 and math.fabs(event.PVz)<26 and (event.PVy*event.PVy + event.PVx*event.PVx)<3 and event.nPVGood>2 and event.njets{0:s}  and event.Photon_r9_1>=0.9 and event.Photon_r9_1<=1. and event.nbtagL==0.0)".format(str(sjets))
        jcut = " (   event.pt_1>=50 and math.fabs(event.eta_1)<1.44 and event.Flag_BadPFMuonDzFilter==1 and event.nPVGood>2 and event.njets{0:s}  and event.Photon_r9_1>=0.9 and event.Photon_r9_1<=1. and event.nbtagL==0.0 and event.iso_1<=0.005 and event.Photon_cutBased_1 ==3 )".format(str(sjets))


    extra_conditions =''
    
    if not isMC and channel =='Gjets': 
        #jcut = jcut + " * ( event.weightpsjson)" 
        extra_conditions =  "  ( event.weightpsjson)" 
    if isMC :
	if channel != 'Gjets' : extra_conditions = "( event.weight  * math.fabs(event.weightPUtruejson) * event.L1PreFiringWeight_Nom * event.IDSF1 * event.IDSF2 * event.IsoSF1 * event.IsoSF2 * event.TrigSF1 * event.TrigSF2)"
	else : extra_conditions = "( event.weight  * math.fabs(event.weightPUtruejson) * event.L1PreFiringWeight_Nom * event.IDSFT )"
    
    #jcutmc = jcut + " * " + extra_conditions
    weight = 1.
    #if isMC : jcut = jcutmc
    print 'Cut ', isMC, jcut
    # Open the input root file
    #fileOut = TFile("output_vsptvspu_{}.root".format(str(year)), "RECREATE")

    # Loop over cuts
    h_scale_rawmet_list_vspt = []
    h_scale_perp_rawmet_list_vspt = []
    h_upara_rawmet_list_vspt = []
    h_uparaboson_rawmet_list_vspt = []
    h_uperp_rawmet_list_vspt = []

    h_scale_rawpuppi_list_vspt = []
    h_scale_perp_rawpuppi_list_vspt = []
    h_upara_rawpuppi_list_vspt = []
    h_uparaboson_rawpuppi_list_vspt = []
    h_uperp_rawpuppi_list_vspt = []

    h_scale_t1_list_vspt = []
    h_scale_perp_t1_list_vspt = []
    h_upara_t1_list_vspt = []
    h_uparaboson_t1_list_vspt = []
    h_uperp_t1_list_vspt = []

    h_scale_t1smear_list_vspt = []
    h_scale_perp_t1smear_list_vspt = []
    h_upara_t1smear_list_vspt = []
    h_uparaboson_t1smear_list_vspt = []
    h_uperp_t1smear_list_vspt = []

    h_scale_puppi_list_vspt = []
    h_scale_perp_puppi_list_vspt = []
    h_upara_puppi_list_vspt = []
    h_uparaboson_puppi_list_vspt = []
    h_uperp_puppi_list_vspt = []


    h_scale_rawmet_list_npv = []
    h_scale_perp_rawmet_list_npv = []
    h_upara_rawmet_list_npv = []
    h_uparaboson_rawmet_list_npv = []
    h_uperp_rawmet_list_npv = []

    h_scale_rawpuppi_list_npv = []
    h_scale_perp_rawpuppi_list_npv = []
    h_upara_rawpuppi_list_npv = []
    h_uparaboson_rawpuppi_list_npv = []
    h_uperp_rawpuppi_list_npv = []

    h_scale_t1_list_npv = []
    h_scale_perp_t1_list_npv = []
    h_upara_t1_list_npv = []
    h_uparaboson_t1_list_npv = []
    h_uperp_t1_list_npv = []

    h_scale_t1smear_list_npv = []
    h_scale_perp_t1smear_list_npv = []
    h_upara_t1smear_list_npv = []
    h_uparaboson_t1smear_list_npv = []
    h_uperp_t1smear_list_npv = []

    h_scale_puppi_list_npv = []
    h_scale_perp_puppi_list_npv = []
    h_upara_puppi_list_npv = []
    h_uparaboson_puppi_list_npv = []
    h_uperp_puppi_list_npv = []

    for i0 in xrange(len(cuts)):
	#folder.cd()
	h_scale_rawmet_vspt = ROOT.TH1F("h_scale_rawmet_vspt_%d" % i0, "h_scale_rawmet_vspt_%d" % i0, 400, -20., 20.)
	h_scale_perp_rawmet_vspt = ROOT.TH1F("h_scale_perp_rawmet_vspt_%d" % i0, "h_scale_perp_rawmet_vspt_%d" % i0, 400, -20., 20.)
	h_upara_rawmet_vspt = ROOT.TH1F("h_upara_rawmet_vspt_%d" % i0, "h_upara_rawmet_vspt_%d" % i0, 100,-200.,200.)
	h_uparaboson_rawmet_vspt = ROOT.TH1F("h_uparaboson_rawmet_vspt_%d" % i0, "h_uparaboson_rawmet_vspt_%d" % i0, 100,-200.,200.)
	h_uperp_rawmet_vspt = ROOT.TH1F("h_uperp_rawmet_vspt_%d" % i0, "h_perp_rawmet_vspt_%d" % i0, 100,-200.,200.)

	h_scale_rawmet_list_vspt.append(h_scale_rawmet_vspt)
	h_scale_perp_rawmet_list_vspt.append(h_scale_perp_rawmet_vspt)
	h_upara_rawmet_list_vspt.append(h_upara_rawmet_vspt)
	h_uparaboson_rawmet_list_vspt.append(h_uparaboson_rawmet_vspt)
	h_uperp_rawmet_list_vspt.append(h_uperp_rawmet_vspt)

	h_scale_rawpuppi_vspt = ROOT.TH1F("h_scale_rawpuppi_vspt_%d" % i0, "h_scale_rawpuppi_vspt_%d" % i0, 400, -20., 20.)
	h_scale_perp_rawpuppi_vspt = ROOT.TH1F("h_scale_perp_rawpuppi_vspt_%d" % i0, "h_scale_perp_rawpuppi_vspt_%d" % i0, 400, -20., 20.)
	h_upara_rawpuppi_vspt = ROOT.TH1F("h_upara_rawpuppi_vspt_%d" % i0, "h_upara_rawpuppi_vspt_%d" % i0, 100,-200.,200.)
	h_uparaboson_rawpuppi_vspt = ROOT.TH1F("h_uparaboson_rawpuppi_vspt_%d" % i0, "h_uparaboson_rawpuppi_vspt_%d" % i0, 100,-200.,200.)
	h_uperp_rawpuppi_vspt = ROOT.TH1F("h_uperp_rawpuppi_vspt_%d" % i0, "h_perp_rawpuppi_vspt_%d" % i0, 100,-200.,200.)

	h_scale_rawpuppi_list_vspt.append(h_scale_rawpuppi_vspt)
	h_scale_perp_rawpuppi_list_vspt.append(h_scale_perp_rawpuppi_vspt)
	h_upara_rawpuppi_list_vspt.append(h_upara_rawpuppi_vspt)
	h_uparaboson_rawpuppi_list_vspt.append(h_uparaboson_rawpuppi_vspt)
	h_uperp_rawpuppi_list_vspt.append(h_uperp_rawpuppi_vspt)


	h_scale_t1_vspt = ROOT.TH1F("h_scale_t1_vspt_%d" % i0, "h_scale_t1_vspt_%d" % i0, 400, -20., 20.)
	h_scale_perp_t1_vspt = ROOT.TH1F("h_scale_perp_t1_vspt_%d" % i0, "h_scale_perp_t1_vspt_%d" % i0, 400, -20., 20.)
	h_upara_t1_vspt = ROOT.TH1F("h_upara_t1_vspt_%d" % i0, "h_upara_t1_vspt_%d" % i0, 100,-200.,200.)
	h_uparaboson_t1_vspt = ROOT.TH1F("h_uparaboson_t1_vspt_%d" % i0, "h_uparaboson_t1_vspt_%d" % i0, 100,-200.,200.)
	h_uperp_t1_vspt = ROOT.TH1F("h_uperp_t1_vspt_%d" % i0, "h_perp_t1_vspt_%d" % i0, 100,-200.,200.)

	h_scale_t1_list_vspt.append(h_scale_t1_vspt)
	h_scale_perp_t1_list_vspt.append(h_scale_perp_t1_vspt)
	h_upara_t1_list_vspt.append(h_upara_t1_vspt)
	h_uparaboson_t1_list_vspt.append(h_uparaboson_t1_vspt)
	h_uperp_t1_list_vspt.append(h_uperp_t1_vspt)

        if isMC : 
	    h_scale_t1smear_vspt = ROOT.TH1F("h_scale_t1smear_vspt_%d" % i0, "h_scale_t1smear_vspt_%d" % i0, 400, -20., 20.)
	    h_scale_perp_t1smear_vspt = ROOT.TH1F("h_scale_perp_t1smear_vspt_%d" % i0, "h_scale_perp_t1smear_vspt_%d" % i0, 400, -20., 20.)
	    h_upara_t1smear_vspt = ROOT.TH1F("h_upara_t1smear_vspt_%d" % i0, "h_upara_t1smear_vspt_%d" % i0, 100,-200.,200.)
	    h_uparaboson_t1smear_vspt = ROOT.TH1F("h_uparaboson_t1smear_vspt_%d" % i0, "h_uparaboson_t1smear_vspt_%d" % i0, 100,-200.,200.)
	    h_uperp_t1smear_vspt = ROOT.TH1F("h_uperp_t1smear_vspt_%d" % i0, "h_perp_t1smear_vspt_%d" % i0, 100,-200.,200.)

	    h_scale_t1smear_list_vspt.append(h_scale_t1smear_vspt)
	    h_scale_perp_t1smear_list_vspt.append(h_scale_perp_t1smear_vspt)
	    h_upara_t1smear_list_vspt.append(h_upara_t1smear_vspt)
	    h_uparaboson_t1smear_list_vspt.append(h_uparaboson_t1smear_vspt)
	    h_uperp_t1smear_list_vspt.append(h_uperp_t1smear_vspt)


	h_scale_puppi_vspt = ROOT.TH1F("h_scale_puppi_vspt_%d" % i0, "h_scale_puppi_vspt_%d" % i0, 400, -20., 20.)
	h_scale_perp_puppi_vspt = ROOT.TH1F("h_scale_perp_puppi_vspt_%d" % i0, "h_scale_perp_puppi_vspt_%d" % i0, 400, -20., 20.)
	h_upara_puppi_vspt = ROOT.TH1F("h_upara_puppi_vspt_%d" % i0, "h_upara_puppi_vspt_%d" % i0, 100,-200.,200.)
	h_uparaboson_puppi_vspt = ROOT.TH1F("h_uparaboson_puppi_vspt_%d" % i0, "h_uparaboson_puppi_vspt_%d" % i0, 100,-200.,200.)
	h_uperp_puppi_vspt = ROOT.TH1F("h_uperp_puppi_vspt_%d" % i0, "h_perp_puppi_vspt_%d" % i0, 100,-200.,200.)

	h_scale_puppi_list_vspt.append(h_scale_puppi_vspt)
	h_scale_perp_puppi_list_vspt.append(h_scale_perp_puppi_vspt)
	h_upara_puppi_list_vspt.append(h_upara_puppi_vspt)
	h_uparaboson_puppi_list_vspt.append(h_uparaboson_puppi_vspt)
	h_uperp_puppi_list_vspt.append(h_uperp_puppi_vspt)


    for i0 in xrange(len(cuts_npv)):
	#folder.cd()
	h_scale_rawmet_npv = ROOT.TH1F("h_scale_rawmet_npv_%d" % i0, "h_scale_rawmet_npv_%d" % i0, 400, -20., 20.)
	h_scale_perp_rawmet_npv = ROOT.TH1F("h_scale_perp_rawmet_npv_%d" % i0, "h_scale_perp_rawmet_npv_%d" % i0, 400, -20., 20.)
	h_upara_rawmet_npv = ROOT.TH1F("h_upara_rawmet_npv_%d" % i0, "h_upara_rawmet_npv_%d" % i0, 100,-200.,200.)
	h_uparaboson_rawmet_npv = ROOT.TH1F("h_uparaboson_rawmet_npv_%d" % i0, "h_uparaboson_rawmet_npv_%d" % i0, 100,-200.,200.)
	h_uperp_rawmet_npv = ROOT.TH1F("h_uperp_rawmet_npv_%d" % i0, "h_perp_rawmet_npv_%d" % i0, 100,-200.,200.)

	h_scale_rawmet_list_npv.append(h_scale_rawmet_npv)
	h_scale_perp_rawmet_list_npv.append(h_scale_perp_rawmet_npv)
	h_upara_rawmet_list_npv.append(h_upara_rawmet_npv)
	h_uparaboson_rawmet_list_npv.append(h_uparaboson_rawmet_npv)
	h_uperp_rawmet_list_npv.append(h_uperp_rawmet_npv)

	h_scale_rawpuppi_npv = ROOT.TH1F("h_scale_rawpuppi_npv_%d" % i0, "h_scale_rawpuppi_npv_%d" % i0, 400, -20., 20.)
	h_scale_perp_rawpuppi_npv = ROOT.TH1F("h_scale_perp_rawpuppi_npv_%d" % i0, "h_scale_perp_rawpuppi_npv_%d" % i0, 400, -20., 20.)
	h_upara_rawpuppi_npv = ROOT.TH1F("h_upara_rawpuppi_npv_%d" % i0, "h_upara_rawpuppi_npv_%d" % i0, 100,-200.,200.)
	h_uparaboson_rawpuppi_npv = ROOT.TH1F("h_uparaboson_rawpuppi_npv_%d" % i0, "h_uparaboson_rawpuppi_npv_%d" % i0, 100,-200.,200.)
	h_uperp_rawpuppi_npv = ROOT.TH1F("h_uperp_rawpuppi_npv_%d" % i0, "h_perp_rawpuppi_npv_%d" % i0, 100,-200.,200.)

	h_scale_rawpuppi_list_npv.append(h_scale_rawpuppi_npv)
	h_scale_perp_rawpuppi_list_npv.append(h_scale_perp_rawpuppi_npv)
	h_upara_rawpuppi_list_npv.append(h_upara_rawpuppi_npv)
	h_uparaboson_rawpuppi_list_npv.append(h_uparaboson_rawpuppi_npv)
	h_uperp_rawpuppi_list_npv.append(h_uperp_rawpuppi_npv)


	h_scale_t1_npv = ROOT.TH1F("h_scale_t1_npv_%d" % i0, "h_scale_t1_npv_%d" % i0, 400, -20., 20.)
	h_scale_perp_t1_npv = ROOT.TH1F("h_scale_perp_t1_npv_%d" % i0, "h_scale_perp_t1_npv_%d" % i0, 400, -20., 20.)
	h_upara_t1_npv = ROOT.TH1F("h_upara_t1_npv_%d" % i0, "h_upara_t1_npv_%d" % i0, 100,-200.,200.)
	h_uparaboson_t1_npv = ROOT.TH1F("h_uparaboson_t1_npv_%d" % i0, "h_uparaboson_t1_npv_%d" % i0, 100,-200.,200.)
	h_uperp_t1_npv = ROOT.TH1F("h_uperp_t1_npv_%d" % i0, "h_perp_t1_npv_%d" % i0, 100,-200.,200.)

	h_scale_t1_list_npv.append(h_scale_t1_npv)
	h_scale_perp_t1_list_npv.append(h_scale_perp_t1_npv)
	h_upara_t1_list_npv.append(h_upara_t1_npv)
	h_uparaboson_t1_list_npv.append(h_uparaboson_t1_npv)
	h_uperp_t1_list_npv.append(h_uperp_t1_npv)

        if isMC : 
	    h_scale_t1smear_npv = ROOT.TH1F("h_scale_t1smear_npv_%d" % i0, "h_scale_t1smear_npv_%d" % i0, 400, -20., 20.)
	    h_scale_perp_t1smear_npv = ROOT.TH1F("h_scale_perp_t1smear_npv_%d" % i0, "h_scale_perp_t1smear_npv_%d" % i0, 400, -20., 20.)
	    h_upara_t1smear_npv = ROOT.TH1F("h_upara_t1smear_npv_%d" % i0, "h_upara_t1smear_npv_%d" % i0, 100,-200.,200.)
	    h_uparaboson_t1smear_npv = ROOT.TH1F("h_uparaboson_t1smear_npv_%d" % i0, "h_uparaboson_t1smear_npv_%d" % i0, 100,-200.,200.)
	    h_uperp_t1smear_npv = ROOT.TH1F("h_uperp_t1smear_npv_%d" % i0, "h_perp_t1smear_npv_%d" % i0, 100,-200.,200.)

	    h_scale_t1smear_list_npv.append(h_scale_t1smear_npv)
	    h_scale_perp_t1smear_list_npv.append(h_scale_perp_t1smear_npv)
	    h_upara_t1smear_list_npv.append(h_upara_t1smear_npv)
	    h_uparaboson_t1smear_list_npv.append(h_uparaboson_t1smear_npv)
	    h_uperp_t1smear_list_npv.append(h_uperp_t1smear_npv)


	h_scale_puppi_npv = ROOT.TH1F("h_scale_puppi_npv_%d" % i0, "h_scale_puppi_npv_%d" % i0, 400, -20., 20.)
	h_scale_perp_puppi_npv = ROOT.TH1F("h_scale_perp_puppi_npv_%d" % i0, "h_scale_perp_puppi_npv_%d" % i0, 400, -20., 20.)
	h_upara_puppi_npv = ROOT.TH1F("h_upara_puppi_npv_%d" % i0, "h_upara_puppi_npv_%d" % i0, 100,-200.,200.)
	h_uparaboson_puppi_npv = ROOT.TH1F("h_uparaboson_puppi_npv_%d" % i0, "h_uparaboson_puppi_npv_%d" % i0, 100,-200.,200.)
	h_uperp_puppi_npv = ROOT.TH1F("h_uperp_puppi_npv_%d" % i0, "h_perp_puppi_npv_%d" % i0, 100,-200.,200.)

	h_scale_puppi_list_npv.append(h_scale_puppi_npv)
	h_scale_perp_puppi_list_npv.append(h_scale_perp_puppi_npv)
	h_upara_puppi_list_npv.append(h_upara_puppi_npv)
	h_uparaboson_puppi_list_npv.append(h_uparaboson_puppi_npv)
	h_uperp_puppi_list_npv.append(h_uperp_puppi_npv)





    for count, event in enumerate(t_):
        if count % 10000==0 : print 'looping.... isMC', isMC, count, extra_conditions
        #if count == 5000 : break

	if eval(jcut):
	    #t_.GetEntry(event)
	    for i0 in range(len(cuts)):
		#if eval(jcut + " and " + cuts[i0]):
		if eval(cuts[i0]):
		#if eval(jcut ):
		#if jcut + " and " + cuts[i0] :
		    if len(extra_conditions)>0 : weight = eval(extra_conditions)
                    #print 'weight is', weight
		    #print jcut, cuts[i0], event.MET_T1_pt, count, event.boson_pt, math.fabs(-event.weightPUtrue), weight
		    h_scale_rawmet_list_vspt[i0].Fill((-event.u_par_RawMET) / event.boson_pt, weight)
		    h_scale_perp_rawmet_list_vspt[i0].Fill((-event.u_perp_RawMET) / (event.boson_pt*event.boson_pt), weight) # probably I should do /boson_pt^2
		    h_upara_rawmet_list_vspt[i0].Fill(-event.u_par_RawMET, weight)
		    h_uparaboson_rawmet_list_vspt[i0].Fill(event.u_par_RawMET+event.boson_pt, weight)
		    h_uperp_rawmet_list_vspt[i0].Fill(-event.u_perp_RawMET/event.boson_pt, weight)

		    h_scale_rawpuppi_list_vspt[i0].Fill((-event.u_par_RawPuppiMET) / event.boson_pt, weight)
		    h_scale_perp_rawpuppi_list_vspt[i0].Fill((-event.u_perp_RawPuppiMET) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_rawpuppi_list_vspt[i0].Fill(-event.u_par_RawPuppiMET, weight)
		    h_uparaboson_rawpuppi_list_vspt[i0].Fill(event.u_par_RawPuppiMET+event.boson_pt, weight)
		    h_uperp_rawpuppi_list_vspt[i0].Fill(-event.u_perp_RawPuppiMET/event.boson_pt, weight)

		    h_scale_t1_list_vspt[i0].Fill((-event.u_par_METCorGood_T1) / event.boson_pt, weight)
		    h_scale_perp_t1_list_vspt[i0].Fill((-event.u_perp_METCorGood_T1) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_t1_list_vspt[i0].Fill(-event.u_par_METCorGood_T1, weight)
		    h_uparaboson_t1_list_vspt[i0].Fill(event.u_par_METCorGood_T1+event.boson_pt, weight)
		    h_uperp_t1_list_vspt[i0].Fill(-event.u_perp_METCorGood_T1/event.boson_pt, weight)

		    if isMC : 
			h_scale_t1smear_list_vspt[i0].Fill((-event.u_par_METCorGood_T1Smear) / event.boson_pt, weight)
			h_scale_perp_t1smear_list_vspt[i0].Fill((-event.u_perp_METCorGood_T1Smear) / (event.boson_pt*event.boson_pt), weight)
			h_upara_t1smear_list_vspt[i0].Fill(-event.u_par_METCorGood_T1Smear, weight)
			h_uparaboson_t1smear_list_vspt[i0].Fill(event.u_par_METCorGood_T1Smear+event.boson_pt, weight)
			h_uperp_t1smear_list_vspt[i0].Fill(-event.u_perp_METCorGood_T1Smear/event.boson_pt, weight)

		    h_scale_puppi_list_vspt[i0].Fill((-event.u_par_PuppiMETCorGood) / event.boson_pt, weight)
		    h_scale_perp_puppi_list_vspt[i0].Fill((-event.u_perp_PuppiMETCorGood) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_puppi_list_vspt[i0].Fill(-event.u_par_PuppiMETCorGood, weight)
		    h_uparaboson_puppi_list_vspt[i0].Fill(event.u_par_PuppiMETCorGood+event.boson_pt, weight)
		    h_uperp_puppi_list_vspt[i0].Fill(-event.u_perp_PuppiMETCorGood/event.boson_pt, weight)

		######
            for i0 in range(len(cuts_npv)):
                if eval(cuts_npv[i0]):
		    #if eval(jcut + " and " + cuts_npv[i0]):
		    #if eval(jcut ):
		    #if jcut + " and " + cuts_npv[i0] :
		    if len(extra_conditions): weight = eval(extra_conditions)
		    #print jcut, cuts_npv[i0], event.MET_T1_pt, count, event.boson_pt, math.fabs(-event.weightPUtrue), weight


		    h_scale_rawmet_list_npv[i0].Fill((-event.u_par_RawMET) / event.boson_pt, weight)
		    h_scale_perp_rawmet_list_npv[i0].Fill((-event.u_perp_RawMET) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_rawmet_list_npv[i0].Fill(-event.u_par_RawMET, weight)
		    h_uparaboson_rawmet_list_npv[i0].Fill(event.u_par_RawMET+event.boson_pt, weight)
		    h_uperp_rawmet_list_npv[i0].Fill(-event.u_perp_RawMET/event.boson_pt, weight)

		    h_scale_rawpuppi_list_npv[i0].Fill((-event.u_par_RawPuppiMET) / event.boson_pt, weight)
		    h_scale_perp_rawpuppi_list_npv[i0].Fill((-event.u_perp_RawPuppiMET) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_rawpuppi_list_npv[i0].Fill(-event.u_par_RawPuppiMET, weight)
		    h_uparaboson_rawpuppi_list_npv[i0].Fill(event.u_par_RawPuppiMET+event.boson_pt, weight)
		    h_uperp_rawpuppi_list_npv[i0].Fill(-event.u_perp_RawPuppiMET/event.boson_pt, weight)

		    h_scale_t1_list_npv[i0].Fill((-event.u_par_METCorGood_T1) / event.boson_pt, weight)
		    h_scale_perp_t1_list_npv[i0].Fill((-event.u_perp_METCorGood_T1) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_t1_list_npv[i0].Fill(-event.u_par_METCorGood_T1, weight)
		    h_uparaboson_t1_list_npv[i0].Fill(event.u_par_METCorGood_T1+event.boson_pt, weight)
		    h_uperp_t1_list_npv[i0].Fill(-event.u_perp_METCorGood_T1/event.boson_pt, weight)

		    if isMC : 
			h_scale_t1smear_list_npv[i0].Fill((-event.u_par_METCorGood_T1Smear) / event.boson_pt, weight)
			h_scale_perp_t1smear_list_npv[i0].Fill((-event.u_perp_METCorGood_T1Smear) / (event.boson_pt*event.boson_pt), weight)
			h_upara_t1smear_list_npv[i0].Fill(-event.u_par_METCorGood_T1Smear, weight)
			h_uparaboson_t1smear_list_npv[i0].Fill(event.u_par_METCorGood_T1Smear+event.boson_pt, weight)
			h_uperp_t1smear_list_npv[i0].Fill(-event.u_perp_METCorGood_T1Smear/event.boson_pt, weight)

		    h_scale_puppi_list_npv[i0].Fill((-event.u_par_PuppiMETCorGood) / event.boson_pt, weight)
		    h_scale_perp_puppi_list_npv[i0].Fill((-event.u_perp_PuppiMETCorGood) / (event.boson_pt*event.boson_pt), weight)
		    h_upara_puppi_list_npv[i0].Fill(-event.u_par_PuppiMETCorGood, weight)
		    h_uparaboson_puppi_list_npv[i0].Fill(event.u_par_PuppiMETCorGood+event.boson_pt, weight)
		    h_uperp_puppi_list_npv[i0].Fill(-event.u_perp_PuppiMETCorGood/event.boson_pt, weight)

    # done with event
    fileOut = TFile(TFileOut, "RECREATE")
    if isMC :
        try :  
	    hW = fileI.Get("hWeights")
	    fileOut.cd()
	    hW.Write()
        except ReferenceError : print 'no hWeights....'
    for i0 in xrange(len(cuts)):


        cut = cuts[i0]
        folder_name = folder_names[cut]
	fileOut.cd()
        folder = fileOut.mkdir("Folder_%d_vspt_%s" % (i0, folder_name))
        folder = fileOut.cd("Folder_%d_vspt_%s" % (i0, folder_name))
	#afolder = fileOut.mkdir("Folder_%d_vspt" % i0)
	#folder = fileOut.cd("Folder_%d_vspt" % i0)

	h_scale_rawmet_list_vspt[i0].Write()
	h_scale_perp_rawmet_list_vspt[i0].Write()
	h_upara_rawmet_list_vspt[i0].Write()
	h_uparaboson_rawmet_list_vspt[i0].Write()
	h_uperp_rawmet_list_vspt[i0].Write()

	h_scale_rawpuppi_list_vspt[i0].Write()
	h_scale_perp_rawpuppi_list_vspt[i0].Write()
	h_upara_rawpuppi_list_vspt[i0].Write()
	h_uparaboson_rawpuppi_list_vspt[i0].Write()
	h_uperp_rawpuppi_list_vspt[i0].Write()


        print h_scale_t1_list_vspt[i0].GetSumOfWeights(), h_scale_perp_t1_list_vspt[i0].GetSumOfWeights()
	h_scale_t1_list_vspt[i0].Write()
	h_scale_perp_t1_list_vspt[i0].Write()
	h_upara_t1_list_vspt[i0].Write()
	h_uparaboson_t1_list_vspt[i0].Write()
	h_uperp_t1_list_vspt[i0].Write()
        if isMC : 

	    h_scale_t1smear_list_vspt[i0].Write()
	    h_scale_perp_t1smear_list_vspt[i0].Write()
	    h_upara_t1smear_list_vspt[i0].Write()
	    h_uparaboson_t1smear_list_vspt[i0].Write()
	    h_uperp_t1smear_list_vspt[i0].Write()

	h_scale_puppi_list_vspt[i0].Write()
	h_scale_perp_puppi_list_vspt[i0].Write()
	h_upara_puppi_list_vspt[i0].Write()
	h_uparaboson_puppi_list_vspt[i0].Write()
	h_uperp_puppi_list_vspt[i0].Write()

    for i0 in xrange(len(cuts_npv)):

	fileOut.cd()
	#folder = fileOut.mkdir("Folder_%d_npv" % i0)
	#folder = fileOut.cd("Folder_%d_npv" % i0)

        cut = cuts_npv[i0]
        #folder_name = ''
        folder_name = folder_names_npv[cut] 
        folder = fileOut.mkdir("Folder_%d_npv_%s" % (i0, folder_name))
        folder = fileOut.cd("Folder_%d_npv_%s" % (i0, folder_name))

	h_scale_rawmet_list_npv[i0].Write()
	h_scale_perp_rawmet_list_npv[i0].Write()
	h_upara_rawmet_list_npv[i0].Write()
	h_uparaboson_rawmet_list_npv[i0].Write()
	h_uperp_rawmet_list_npv[i0].Write()



	h_scale_rawpuppi_list_npv[i0].Write()
	h_scale_perp_rawpuppi_list_npv[i0].Write()
	h_upara_rawpuppi_list_npv[i0].Write()
	h_uparaboson_rawpuppi_list_npv[i0].Write()
	h_uperp_rawpuppi_list_npv[i0].Write()




	h_scale_t1_list_npv[i0].Write()
	h_scale_perp_t1_list_npv[i0].Write()
	h_upara_t1_list_npv[i0].Write()
	h_uparaboson_t1_list_npv[i0].Write()
	h_uperp_t1_list_npv[i0].Write()
        if isMC : 


	    h_scale_t1smear_list_npv[i0].Write()
	    h_scale_perp_t1smear_list_npv[i0].Write()
	    h_upara_t1smear_list_npv[i0].Write()
	    h_uparaboson_t1smear_list_npv[i0].Write()
	    h_uperp_t1smear_list_npv[i0].Write()




	h_scale_puppi_list_npv[i0].Write()
	h_scale_perp_puppi_list_npv[i0].Write()
	h_upara_puppi_list_npv[i0].Write()
	h_uparaboson_puppi_list_npv[i0].Write()
	h_uperp_puppi_list_npv[i0].Write()




    fileOut.Write()
    fileOut.Close()





get_scales()



