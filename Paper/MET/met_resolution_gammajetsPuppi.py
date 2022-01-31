#####################################################################
#################### MET RESOLUTION##################################
#####################################################################
# this one plots scale of the different met types, in ee/mumu 


import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TF1, TLatex, TPaveStats, TGraph, TGraphErrors, TPad, TMultiGraph, TLine, TLegend, RooHistPdf, RooFormulaVar, RooPlot, RooAddPdf, RooFitResult,  RooDataHist, RooDataSet,  RooFit, RooArgList, RooRealVar, RooArgSet, RooLinkedList, RooVoigtian
import math, sys, optparse, copy, re, array
import numpy as np
from array import array


import include.helper     as helper
import include.Region     as Region
import include.Canvas     as Canvas
import include.CutManager as CutManager
import include.Sample     as Sample

def makeUpara(met, phi,boson, boson_phi):
    uPara = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson + " + " + boson +")" )
    return uPara
def makeUperp(met, phi,boson, boson_phi):
    uPerp = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*sin( " +boson_phi +" )-(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*cos( " +boson_phi +" ))/" +boson +")" )                             
    return uPerp

def constructModel(Hist, bkg_hist,  m, um,uM, BKGSubtraction, eemm, upd,  cut, var, plot_name):
    f = 0
    efwhm = 0
    v_m.setVal(Hist.mean(x) );
    v_m.setRange(Hist.mean(x) - Hist.sigma(x), Hist.mean(x) + Hist.sigma(x));
    voigt = RooVoigtian ("voigt", "Voigtian", x, v_m, gamma_Z0, g_w)
    xFrame = x.frame()
    Hist.plotOn(xFrame)
    if BKGSubtraction:
        plotda = Canvas.Canvas("met/gammajets/resolution/fit/"+dire+var+dependence+cut , "png",0.6, 0.7, 0.8, 0.9)
        bkg_pdf =  RooHistPdf("bkg_pdf","bkg_pdf",RooArgSet(x),bkg_hist)
        lAbkgFrac = RooRealVar("AbkgFrac","AbkgFrac",0.5,0.,1.)
        sigbkgFrac = RooFormulaVar("bkgfrac","@0",RooArgList(lAbkgFrac))
        model = RooAddPdf("modelSB","modelSB",voigt,bkg_pdf,sigbkgFrac)
        result = model.fitTo (Hist, RooFit.Minimizer("Minuit","Migrad"),RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel (-1)) 
        model.plotOn(xFrame)
        model.plotOn(xFrame, RooFit.Components("bkg_pdf"), RooFit.LineColor(r.kRed)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kRed)  ,RooFit.DrawOption("F"))
        model.plotOn(xFrame, RooFit.Components("voigt")  , RooFit.LineColor(r.kGreen)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kGreen)  ,RooFit.DrawOption("L")) 
        xFrame.Draw()
    
    else:   
        plotmc = Canvas.Canvas("met/gammajets/resolution/mcfit/"+dire+var+dependence+cut , "png",0.6, 0.7, 0.8, 0.9)
        result = voigt.fitTo(Hist, RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1)) 
        voigt.plotOn(xFrame,RooFit.FillColor(r.kGray),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))
        voigt.plotOn(xFrame,RooFit.LineColor(r.kGray))  
        xFrame.Draw()
    sigma = g_w.getVal()
    gamma = gamma_Z0.getVal()
    esigma = g_w.getError()
    egamma = gamma_Z0.getError()
    Vsg = result.correlation(g_w, gamma_Z0)
    Vgs = result.correlation(gamma_Z0, g_w)
    Vss = result.correlation(g_w, g_w)
    Vgg = result.correlation(gamma_Z0, gamma_Z0)
    f = FWHM(sigma, gamma)
    efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)
    if BKGSubtraction:
        plotda.save(0, 1, 0, xFrame.chiSquare(), "FWHM = %.1f " %(f), "x", "")
    else:
        if (upd ==""):
            plotmc.save(0, 1, 0, xFrame.chiSquare(),  "FWHM = %.1f " %(f), "x", "") 
    print 'fwhm', f
    return f, efwhm

def FWHMError_fixed(sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg):
    a = 0.5346
    b = 0.2166
    c = 2 * math.sqrt( 2*math.log(2) )
    f_g = c * sigma
    f_l = 2 * gamma
    sq = math.sqrt( b * pow(f_l, 2) + pow(f_g, 2) )
    dfds = c * ( f_g / sq )
    dfdg = 2 * ( a + b * f_l / sq )
    p1 = dfds * dfds * esigma * esigma * pow( Vss, 2 )
    p2 = dfds * dfdg * esigma * egamma * pow( Vsg, 2 )
    p3 = dfdg * dfds * egamma * esigma * pow( Vgs, 2 )
    p4 = dfdg * dfdg * egamma * egamma * pow( Vgg, 2 );
    return math.sqrt ( p1 + p2 + p3 + p4 )

def FWHM(sigma, gamma):
    f_g = 2 * sigma * math.sqrt(2 * math.log(2))
    f_l = 2 * gamma
    return ((0.5346 * 2 * gamma + math.sqrt(0.2166 * f_l * f_l + f_g * f_g))/2.3548) 

if __name__ == "__main__":


    doBKGSubtraction = True
    doPostFix = True
    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="just do a testrun. takes one variable in one eta for one region")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples.dat', help='the samples file. default \'samples.dat\'')
    (opts, args) = parser.parse_args()
    print 'Going to load DATA and MC trees...'
    bkgDatasets = ['QCD_HT200to300_ext', 'QCD_HT300to500_ext', 'QCD_HT500to700_ext',  'QCD_HT700to1000_ext','QCD_HT1000to1500_ext', 'QCD_HT1500to2000_ext', 'QCD_HT2000toInf_ext', 'TGJets_ext', 'TTGJets', 'WGToLNuG_amcatnlo_ext', 'ZGTo2LG_ext', 'ZGTo2NuG','WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400_ext','WJetsToLNu_HT400to600_ext','WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT800to1200_ext','WJetsToLNu_HT1200to2500_ext', 'WJetsToLNu_HT2500toInf_ext']
    gjetsDatasets = ['GJets_HT40to100_ext','GJets_HT100to200_ext', 'GJets_HT200to400_ext', 'GJets_HT400to600_ext','GJets_HT600toInf_ext' ]
    if doPostFix:
        daDatasets = ['SinglePhoton_Run2016B_03Feb2017_v2', 'SinglePhoton_Run2016C_03Feb2017', 'SinglePhoton_Run2016D_03Feb2017', 'SinglePhoton_Run2016E_03Feb2017', 'SinglePhoton_Run2016F_03Feb2017', 'SinglePhoton_Run2016G_03Feb2017', 'SinglePhoton_Run2016H_03Feb2017_v2']
    else:
        daDatasets = ['SinglePhoton_Run2016B_ReReco_v2','SinglePhoton_Run2016C_ReReco_v2', 'SinglePhoton_Run2016D_ReReco_v2', 'SinglePhoton_Run2016E_ReReco_v2', 'SinglePhoton_Run2016F_ReReco_v1', 'SinglePhoton_Run2016G_ReReco_v1', 'SinglePhoton_Run2016H_PromptReco_v2', 'SinglePhoton_Run2016H_PromptReco_v3']
    channel = 'gamma'
    if doBKGSubtraction:
        treeBKG = Sample.Tree(helper.selectSamples(opts.sampleFile, bkgDatasets, 'bkg'), 'bkg'  , 0)
        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, daDatasets, 'da'), 'da', 1)
        trees = [treeBKG, treeDA] 
        plot_name = 'Data'
    else:
        treeGJETS = Sample.Tree(helper.selectSamples(opts.sampleFile, gjetsDatasets, 'gjets'), 'gjets'  , 0)
        trees = [treeGJETS]
        plot_name =  'GJets'
    if doBKGSubtraction:
        direction = [plot_name]  
        updown = [""]  
        uPerpPuppi = [makeUperp('metPuppi_pt', 'metPuppi_phi', 'gamma_pt', 'gamma_phi')] 
        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'gamma_pt', 'gamma_phi')] 
    else:
        direction = [plot_name]  
        #direction = [plot_name,plot_name+'_up_jes_DY', plot_name+'_down_jes_DY', plot_name+'_up_jer_DY', plot_name+'_down_jer_DY',plot_name+'_up_uncl_DY', plot_name+'_down_uncl_DY']  
        updown = [""]  
        #updown = ["","_up", "_down",  "_jerUp", "_jerDown", "_unclUp", "_unclDown"]  

        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'gamma_pt', 'gamma_phi'), makeUpara('metPuppi_jecUp_pt', 'metPuppi_jecUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('metPuppi_jecDown_pt', 'metPuppi_jecDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('metPuppi_shifted_JetResUp_pt', 'metPuppi_shifted_JetResUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('metPuppi_shifted_JetResDown_pt', 'metPuppi_shifted_JetResDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('metPuppi_shifted_UnclusteredEnUp_pt', 'metPuppi_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUpara('metPuppi_shifted_UnclusteredEnDown_pt', 'metPuppi_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        uPerpPuppi = [makeUperp('metPuppi_pt', 'metPuppi_phi', 'gamma_pt', 'gamma_phi'), makeUperp('metPuppi_jecUp_pt', 'metPuppi_jecUp_phi', 'gamma_pt', 'gamma_phi'), makeUperp('metPuppi_jecDown_pt', 'metPuppi_jecDown_phi', 'gamma_pt', 'gamma_phi'), makeUperp('metPuppi_shifted_JetResUp_pt', 'metPuppi_shifted_JetResUp_phi', 'gamma_pt', 'gamma_phi'), makeUperp('metPuppi_shifted_JetResDown_pt', 'metPuppi_shifted_JetResDown_phi', 'gamma_pt', 'gamma_phi'), makeUperp('metPuppi_shifted_UnclusteredEnUp_pt', 'metPuppi_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUperp('metPuppi_shifted_UnclusteredEnDown_pt', 'metPuppi_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 


    variable = [uPerpPuppi, uParaPuppi]
    variablename = ['_uPerpPuppi', '_uParaPuppi']
    dependences = [  'nVert']
    print 'Trees successfully loaded...'
    lumi = 35.9

   
    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager.CutManager()

    regions = []
    
    GammaJets = Region.region('met' +variablename[0], 
            [cuts.gammas()],
            'met_pt',
            'gamma_pt',
            variablename[0], 
            [range(-100,300,50)],
            False)
    regions.append(GammaJets)                                 
    
    vtxbins = [[0.5, 6],[6, 8],[8, 10], [10, 12],[12,14], [14 ,16],[16, 18], [18, 20], [20,  22], [22, 24], [24, 26], [26, 28], [28, 32], [32, 40]]
    qtbins = [[0, 15], [15, 30],[30, 51],  [51, 65],[65, 80],[80,110], [110, 140], [140, 170], [170, 200],[200, 250] ,[250, 330]]
    sumetbins = [ [400, 500],[500, 600], [600, 700], [700, 800],[800, 900],  [900, 1000],[1000, 1100], [1100, 1300],  [1300, 1600], [1600, 2500]]
    scalebins = [ [0,24],[24, 30],[30, 38],[38, 46], [46, 52], [52, 60], [60, 68], [68, 76], [76, 84],[84,92],[92,100], [100, 115], [115, 130],  [130, 150], [150, 175], [175, 200], [200, 225], [225, 250], [250, 275],[275, 305], [305, 335], [335, 365], [365, 400], [400, 440],  [440, 500]]
    cutsList = []
    binposition = []
    binerror = []
    g_w = RooRealVar("g_w", "width Gaus", 10.,0. , 100., "GeV") # sigma
    gamma_Z0 = RooRealVar("gamma_Z0_U", "Z0 width", 2.3, 0., 100., "GeV") # gamma
    v_m = RooRealVar("v_m", "v_m",0,-10.,10.)
    for dependence in dependences :                                                                                                                                                                  
        if dependence == 'nVert':
            bins = vtxbins        
        if dependence == 'gamma_pt':
            bins = qtbins       
        for dire in direction:
            if doBKGSubtraction:
                if doPostFix:
                    fileD =  TFile("tgraphs/DatagjetsScaleMarch27Puppi_03Feb.root");
                else:
                    fileD =  TFile("tgraphs/DatagjetsScaleMarch27Puppi_23Sep.root");
            else: 
                if doPostFix:
                    fileD =  TFile("tgraphs/GJetsgjetsScaleMarch27Puppi_03Feb.root");
                else:
                    fileD =  TFile("tgraphs/GJetsgjetsScaleMarch27Puppi_23Sep.root");
            hScale = fileD.Get("met_uParaPuppi_over_qt");
            a = "*( "
            for q in scalebins:   
                miniqt = float(min(scalebins[scalebins.index(q)]))
                maxiqt = float(max(scalebins[scalebins.index(q)]))
                midqt = float((miniqt+maxiqt)/2)
                x = hScale.GetY() 
                if scalebins.index(q)== 0:
                    a = a + " ("+ str(miniqt) +" < gamma_pt && gamma_pt < "+ str(maxiqt) +")*(1/ " + str(x[scalebins.index(q)]) +")" 
                else:
                    a = a + " + ("+ str(miniqt)+" < gamma_pt && gamma_pt <"+str(maxiqt)+")*(1/" + str(x[scalebins.index(q)]) +")"
            a = a+ ")"       
            print a
            fileD.Close()                                                                                                                
            if doPostFix:
                f2 = TFile(dire + "gjetsResolutionMarch27Puppi_03Feb.root", "UPDATE");   
            else:
                f2 = TFile(dire + "gjetsResolutionMarch27Puppi_23Sep.root", "UPDATE");   
            upd = updown[direction.index(dire)]
            for vari in variable:
                var = vari[direction.index(dire)]
                for reg in regions:
                    cutsList = []; binposition = [];binerror = [];ratio = [];data_fwhms = [];data_fwhm = [];data_errors = [];data_error = [];mc_fwhm = [];mc_fwhms = [];mc_error = [];mc_errors = []
                    print 'doing variable: ', dire , variablename[variable.index(vari)]
                    for i in bins:
                        mini = float(min(bins[bins.index(i)]))
                        maxi = float(max(bins[bins.index(i)]))
                        mid = float((mini+maxi)/2)
                        binposition.append(mid)
                        binerror.append(0.0)
                        if ((dependence == 'nVert') or (dependence == 'met_sumEt')):
                            cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) + " &&  gamma_pt > 50 "]))
                        else:
                            cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini)]))
                    for i in cutsList:
                        print i
                        binLow = -80.; binHigh = 80.; nbins = 300;
                        x = RooRealVar("x", "x", binLow, binHigh)
                        for tree in trees:
                            if doBKGSubtraction:
                                if tree.name == 'bkg':
                                    bkg_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'bkg', var+a,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)    
                                    bkg_Hist = RooDataHist("bkg","bkg"+i,RooArgList(x),bkg_hist)                 
                                    m_bkg = bkg_hist.GetMean()
                                    um_bkg = bkg_hist.GetMean()-bkg_hist.GetRMS()
                                    uM_bkg = bkg_hist.GetMean()+bkg_hist.GetRMS()
                                if tree.name == 'da':
                                    data_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var+a,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                    data_Hist = RooDataHist("da","da"+i, RooArgList(x), data_hist)                  
                                    m_da = data_hist.GetMean()  
                                    um_da = data_hist.GetMean()-data_hist.GetRMS()
                                    uM_da = data_hist.GetMean()+data_hist.GetRMS()                                                   
                            if tree.name == 'gjets':
                                gjets_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'gjets', var+a, nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                gjets_Hist = RooDataHist("gjets","gjets"+i, RooArgList(x), gjets_hist)
                                gjets_BkgHist = RooDataHist()                                                          
                                m_gjets = gjets_hist.GetMean() 
                                um_gjets = gjets_hist.GetMean()-gjets_hist.GetRMS()
                                uM_gjets = gjets_hist.GetMean()+gjets_hist.GetRMS()
                        
                        if doBKGSubtraction:
                            if dependence == 'gamma_pt':
                                if cutsList.index(i) < 2:
                                    data_fwhm = 0
                                    data_error = 0      
                                else:                             
                                    data_fwhm, data_error = constructModel(data_Hist, bkg_Hist, m_da, um_da, uM_da, True, channel, upd,  str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            else:
                                data_fwhm, data_error = constructModel(data_Hist, bkg_Hist, m_da, um_da, uM_da, True, channel, upd,  str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            data_fwhms.append(data_fwhm)
                            data_errors.append(data_error)
                        else: 
                            if dependence == 'gamma_pt':
                                if cutsList.index(i) < 2:
                                    mc_fwhm = 0.
                                    mc_error = 0.                   
                                else:                             
                                    mc_fwhm, mc_error = constructModel(gjets_Hist, gjets_BkgHist, m_gjets, um_gjets, uM_gjets, False, channel, upd, str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            else:
                                mc_fwhm, mc_error = constructModel(gjets_Hist, gjets_BkgHist, m_gjets, um_gjets, uM_gjets, False, channel, upd, str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            mc_fwhms.append(mc_fwhm)
                            mc_errors.append(mc_error)
                    if doBKGSubtraction:
                        graph = TGraphErrors(len(binposition), array("f", binposition), array("f", data_fwhms), array("f", binerror), array("f", data_errors))
                        graph.Write (channel+"_met" +variablename[variable.index(vari)]+ "_vs_" + dependence);
                    else:
                        graph_mc = TGraphErrors(len(binposition), array("f", binposition), array("f", mc_fwhms), array("f", binerror), array("f", mc_errors))
                        graph_mc.Write (channel+"_met"+variablename[variable.index(vari)] + "_vs_" + dependence);
        f2.Close()







