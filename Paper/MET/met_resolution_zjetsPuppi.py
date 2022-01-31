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

def constructModel(Hist,  hist, bkg_hist,  m, um,uM, BKGSubtraction, eemm, upd, cut, var, plot_name):
    f = 0
    efwhm = 0
    plotmc = Canvas.Canvas("met/zjets/resolution/mcfit/"+dire+var+eemm +cut , "png",0.6, 0.7, 0.8, 0.9)
    plotda = Canvas.Canvas("met/zjets/resolution/fit/"+dire+var+eemm +cut , "png",0.6, 0.7, 0.8, 0.9)
#    v_m.setVal(Hist.mean(x) );
#    v_m.setRange(Hist.mean(x) - Hist.sigma(x), Hist.mean(x) + Hist.sigma(x));
#    
#    voigt = RooVoigtian ("voigt", "Voigtian", x, v_m, gamma_Z0, g_w)
#    xFrame = x.frame()
#    Hist.plotOn(xFrame)
#    if BKGSubtraction:
#        plotda = Canvas.Canvas("met/zjets/resolution/fit/"+dire+var+eemm +cut , "png",0.6, 0.7, 0.8, 0.9)
#        bkg_pdf =  RooHistPdf("bkg_pdf","bkg_pdf",RooArgSet(x),bkg_hist)
#        lAbkgFrac = RooRealVar("AbkgFrac","AbkgFrac",0.5,0.,1.)
#        sigbkgFrac = RooFormulaVar("bkgfrac","@0",RooArgList(lAbkgFrac))
#        model = RooAddPdf("modelSB","modelSB",voigt,bkg_pdf,sigbkgFrac)
#        result = model.fitTo (Hist, RooFit.Minimizer("Minuit","Migrad"),RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel (-1)) 
#        model.plotOn(xFrame)
#        model.plotOn(xFrame, RooFit.Components("bkg_pdf"), RooFit.LineColor(r.kRed)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kRed)  ,RooFit.DrawOption("F"))
#        model.plotOn(xFrame, RooFit.Components("voigt")  , RooFit.LineColor(r.kGreen)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kGreen)  ,RooFit.DrawOption("L")) 
#        xFrame.Draw()
#    else:   
#        plotmc = Canvas.Canvas("met/zjets/resolution/mcfit/"+dire+var+eemm +cut , "png",0.6, 0.7, 0.8, 0.9)
#        result = voigt.fitTo(Hist, RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1)) 
#        voigt.plotOn(xFrame,RooFit.FillColor(r.kGray),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))
#        voigt.plotOn(xFrame,RooFit.LineColor(r.kGray))  
#        xFrame.Draw()
#    sigma = g_w.getVal()
#    gamma = gamma_Z0.getVal()
#    esigma = g_w.getError()
#    print "esigma ", esigma
#    egamma = gamma_Z0.getError()
#    print "egamma ", egamma
#    Vsg = result.correlation(g_w, gamma_Z0)
#    Vgs = result.correlation(gamma_Z0, g_w)
#    Vss = result.correlation(g_w, g_w)
#    Vgg = result.correlation(gamma_Z0, gamma_Z0)
#    integral = hist.Integral()
#    if BKGSubtraction:
#        integral = hist.Integral()
#        if xFrame.chiSquare() > 10:
#            print "Bad chi2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    integral = hist.Integral()
    f = hist.GetRMS()
    efwhm = hist.GetRMSError()
    fromFit = False
    #    else:
    #        f = FWHM(sigma, gamma)
    #        chi2 = xFrame.chiSquare()
    #        efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)
    #        fromFit = True
    #else:
    #    integral = hist.Integral()
    #    if xFrame.chiSquare() > 10:
    #        plotmc = Canvas.Canvas("met/zjets/resolution/mcfit/"+dire+var+eemm +cut+"_restricted" , "png",0.6, 0.7, 0.8, 0.9)                                                                                                                                   
    #        result = voigt.fitTo(Hist, RooFit.Range(hist.GetMean()-2*hist.GetRMS(), hist.GetMean()+2*hist.GetRMS()), RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1)) 
    #        voigt.plotOn(xFrame,RooFit.FillColor(r.kBlue),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))
    #        voigt.plotOn(xFrame,RooFit.LineColor(r.kBlue))  
    #        xFrame.Draw()
    #        sigma = g_w.getVal()
    #        gamma = gamma_Z0.getVal()
    #        esigma = g_w.getError()
    #        egamma = gamma_Z0.getError()
    #        Vsg = result.correlation(g_w, gamma_Z0)
    #        Vgs = result.correlation(gamma_Z0, g_w)
    #        Vss = result.correlation(g_w, g_w)
    #        Vgg = result.correlation(gamma_Z0, gamma_Z0)
    #        if xFrame.chiSquare() > 10  or dire+var+eemm+cut == "DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_uPerpPuppi_EnVert4" or dire+var+eemm +cut == "DY_up_jes_DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_jes_DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_up_jer_DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_jer_DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_up_uncl_DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_uncl_DY_uPerpPuppi_EnVert1":
    #            fromFit = False
    #            f = hist.GetRMS()                                                                
    #            efwhm = hist.GetRMSError()
    #            chi2 = 0
    #            print "after restricting the range, bad chi2, take RMS from histogram ", f
    #        elif FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg) > 1 or dire+var+eemm +cut == "DY_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_uPerpPuppi_EnVert4" or dire+var+eemm +cut == "DY_up_jes_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_jes_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_up_jer_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_jer_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_up_uncl_uPerpPuppi_EnVert1"  or dire+var+eemm +cut == "DY_down_uncl_uPerpPuppi_EnVert1":
    #            fromFit = False
    #            f = hist.GetRMS()                                                                
    #            efwhm = hist.GetRMSError()
    #            chi2 = 0
    #            print "waaay too large error", FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg), " take mean from histo", f, " +- ", efwhm
    #        else: 
    #            fromFit = True
    #            f = FWHM(sigma, gamma)
    #            efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)
    #            chi2 = xFrame.chiSquare()                                                                                                                              
    #            print "after restricting the range, the chi2 is now", xFrame.chiSquare()                                                                               
    #    else:
    #        f = FWHM(sigma, gamma)
    #        chi2 = xFrame.chiSquare()
    #        efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)
    #        fromFit = True
    #        print 'got good chi2: ', xFrame.chiSquare() , ' on the first try, FWHM is ', f                                                                                                                                                                     
     
    if BKGSubtraction:
        plotda.save(0, lumi, 0, "", "RMS (hist) %.2f +- %.2f"%(hist.GetRMS(), hist.GetRMSError()), var, "", integral, fromFit)
    else:
        plotmc.save(0, lumi, 0, "", "RMS (hist) %.2f +- %.2f"%(hist.GetRMS(), hist.GetRMSError()), var, "", integral, fromFit)                                                                                                          

    print 'fwhm', f
    print 'error ', efwhm
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

    doBKGSubtraction = False
    doee = True
    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="just do a testrun. takes one variable in one eta for one region")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samplesPuppi.dat', help='the samples file. default \'samples.dat\'')
    (opts, args) = parser.parse_args()
    
    print 'Going to load DATA and MC trees...'

    if doBKGSubtraction: 
        if doee:
            dy = ['DYJetsToLL_M50_ee', 'ZZTo4L_ee', 'ZZTo2L2Q_ee', 'WZTo2L2Q_ee']
            tt = ['TTLepPow_ee',  'WWTo2L2Nu_ee',  'WZTo3LNu_amcatnlo_ee', 'WWW_ee', 'WWZ_ee', 'WZZ_ee', 'ZZZ_ee','T_tWch_ext_ee', 'TBar_tWch_ext_ee']
            da = ['DoubleEG_Run2016B_03Feb2017_v2', 'DoubleEG_Run2016C_03Feb2017', 'DoubleEG_Run2016D_03Feb2017', 'DoubleEG_Run2016E_03Feb2017', 'DoubleEG_Run2016F_03Feb2017', 'DoubleEG_Run2016G_03Feb2017', 'DoubleEG_Run2016H_03Feb2017_v2', 'DoubleEG_Run2016H_03Feb2017_v3']  
            channel = 'E'
            lumi =  35.9
        else:
            tt = ['TTLepPow_mm',  'WWTo2L2Nu_mm',  'WZTo3LNu_amcatnlo_mm', 'WWW_mm', 'WWZ_mm', 'WZZ_mm', 'ZZZ_mm']
            da = ['DoubleMuon_Run2016B_03Feb2017_v2', 'DoubleMuon_Run2016C_03Feb2017', 'DoubleMuon_Run2016D_03Feb2017', 'DoubleMuon_Run2016E_03Feb2017', 'DoubleMuon_Run2016F_03Feb2017', 'DoubleMuon_Run2016G_03Feb2017', 'DoubleMuon_Run2016H_03Feb2017_v2', 'DoubleEG_Run2016H_03Feb2017_v3']  
            channel = 'M'           
            lumi = 35.9
        plot_name = 'Data'
        destination = 'Not_BKG_Subtraction'
        treeTT = Sample.Tree(helper.selectSamples(opts.sampleFile, tt, 'tt'), 'tt', 0)
        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, da, 'da'), 'da', 1)
    else:
        if doee:
            dy = ['DYJetsToLL_M50_ee', 'ZZTo4L_ee', 'ZZTo2L2Q_ee', 'WZTo2L2Q_ee']
            channel = 'E'
            lumi =  35.9
        else:
            dy = ['DYJetsToLL_M50_mm', 'ZZTo4L_mm', 'ZZTo2L2Q_mm', 'WZTo2L2Q_mm' ]
            channel = 'M'
            lumi = 35.6
        plot_name =  'DY'
        treeDY = Sample.Tree(helper.selectSamples(opts.sampleFile, dy, 'dy'), 'dy', 0)

    if doBKGSubtraction:
        trees = [treeTT, treeDA] 
        updown = [""]  
        direction = [plot_name] 
        uPerpPuppi = [makeUperp('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi')] 
        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi')] 
        uPerpRaw = [makeUperp('met_rawPt', 'met_rawPhi', 'zll_pt', 'zll_phi')] 
        uParaRaw = [makeUpara('met_rawPt', 'met_rawPhi', 'zll_pt', 'zll_phi')] 
    else:
        trees = [treeDY]
        #direction = [plot_name]  
        direction = [plot_name,plot_name+'_up_jes_DY', plot_name+'_down_jes_DY', plot_name+'_up_jer_DY', plot_name+'_down_jer_DY',plot_name+'_up_uncl_DY', plot_name+'_down_uncl_DY']  
        #updown = [""]  
        updown = ["","_up", "_down",  "_jerUp", "_jerDown", "_unclUp", "_unclDown"]  
        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecUp_pt', 'metPuppi_jecUp_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecDown_pt', 'metPuppi_jecDown_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_shifted_JetResUp_pt', 'metPuppi_shifted_JetResUp_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_shifted_JetResDown_pt', 'metPuppi_shifted_JetResDown_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_shifted_UnclusteredEnUp_pt', 'metPuppi_shifted_UnclusteredEnUp_phi', 'zll_pt', 'zll_phi'),  makeUpara('metPuppi_shifted_UnclusteredEnDown_pt', 'metPuppi_shifted_UnclusteredEnDown_phi', 'zll_pt', 'zll_phi')] 
        uPerpPuppi = [makeUperp('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi'), makeUperp('metPuppi_jecUp_pt', 'metPuppi_jecUp_phi', 'zll_pt', 'zll_phi'), makeUperp('metPuppi_jecDown_pt', 'metPuppi_jecDown_phi', 'zll_pt', 'zll_phi'), makeUperp('metPuppi_shifted_JetResUp_pt', 'metPuppi_shifted_JetResUp_phi', 'zll_pt', 'zll_phi'), makeUperp('metPuppi_shifted_JetResDown_pt', 'metPuppi_shifted_JetResDown_phi', 'zll_pt', 'zll_phi'), makeUperp('metPuppi_shifted_UnclusteredEnUp_pt', 'metPuppi_shifted_UnclusteredEnUp_phi', 'zll_pt', 'zll_phi'),  makeUperp('metPuppi_shifted_UnclusteredEnDown_pt', 'metPuppi_shifted_UnclusteredEnDown_phi', 'zll_pt', 'zll_phi')] 

    variable = [uParaPuppi , uPerpPuppi]
    #variable = [uPerp]
    #variable = [uPerp, uPara, uPerpPuppiRaw, uParaPuppiRaw ]
    #variable = [uPerpRaw, uParaRaw, uPerpPuppi,uParaPuppi]
    #variablename = ['_metx_', '_mety_']
    variablename = ['_uParaPuppi_', '_uPerpPuppi_' ]
    #variablename = ['_uPerp_']
    #variablename = ['_uPerp', '_uPara', '_uPerpPuppiRaw_', '_uParaPuppiRaw_' ]
    #variablename = ['_uPerpRaw', '_uParaRaw','_uPerpPuppi_', '_uParaPuppi_']
    dependences = ['nVert']
    #dependences = ['nVert', 'zll_pt', 'met_sumEt-zll_pt']
    #dependences = ['zll_pt']
    print 'Trees successfully loaded...'
    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager.CutManager()

    regions = []
    region = Region.region('met' +variablename[0], 
            [cuts.leps()],
            'met_uPerp_zll',
            'zll_pt',
            variablename[0], 
            [range(-100,300,50)],
            False)
    regions.append(region)                                 
    
    vtxbins = [[4, 6],[6, 8],[8, 10], [10, 12],[12,14], [14 ,16],[16, 18], [18, 20], [20,  22], [22, 24], [24, 26], [26, 28], [28, 32], [32, 40]]
    qtbins = [[18, 30],[30, 51],  [51, 65],[65, 80],[80,110], [110, 140], [140, 170], [170, 200],[200, 250] ,[250, 330]]
    sumetbins = [ [400, 500],[500, 600], [600, 700], [700, 800],[800, 900],  [900, 1000],[1000, 1100], [1100, 1300],  [1300, 1600], [1600, 2500]]
    scalebins = [ [0,18], [18,24],[24, 30],[30, 38],[38, 46], [46, 52], [52, 60], [60, 68], [68, 76], [76, 84],[84,92],[92,100], [100, 115], [115, 130],  [130, 150], [150, 175], [175, 200], [200, 225], [225, 250], [250, 275],[275, 305], [305, 335], [335, 365], [365, 400], [400, 440],  [440, 500]]
    cutsList = []
    binposition = []
    binerror = []

    g_w = RooRealVar("g_w", "width Gaus", 10.,0. , 100., "GeV") # sigma
    gamma_Z0 = RooRealVar("gamma_Z0_U", "Z0 width", 2.3, 0., 100., "GeV") # gamma
    v_m = RooRealVar("v_m", "v_m",0,-10.,10.)
    for dependence in dependences :                                                                                                                                                                  
        if dependence == 'nVert':
            bins = vtxbins        
        if dependence == 'zll_pt':
            bins = qtbins       
        if dependence == 'met_sumEt-zll_pt':
            bins = sumetbins           
        for dire in direction:
            if doBKGSubtraction:
                if doee:
                    fileD =  TFile("tgraphs/DataEZllScaleMay25PuppiMean.root");
                else:
                    fileD =  TFile("tgraphs/DataMZllScaleMay25PuppiMean.root");
            else:
                if doee:
                    fileD =  TFile("tgraphs/DYEZllScaleMay25PuppiMean.root");
                else:
                    fileD =  TFile("tgraphs/DYMZllScaleMay25PuppiMean.root");
            if doee:
                hScale = fileD.Get("E_met_uParaPuppi_over_zll_pt");
            else:
                hScale = fileD.Get("M_met_uParaPuppi_over_zll_pt");
            a = "*( "
            for q in scalebins:   
                miniqt = float(min(scalebins[scalebins.index(q)]))
                maxiqt = float(max(scalebins[scalebins.index(q)]))
                midqt = float((miniqt+maxiqt)/2)
                x = hScale.GetY() 
                if scalebins.index(q)== 0:
                    a = a + " ("+ str(miniqt) +" < zll_pt && zll_pt < "+ str(maxiqt) +")*(1/ " + str(x[scalebins.index(q)]) +")" 
                else:
                    a = a + " + ("+ str(miniqt)+" < zll_pt && zll_pt <"+str(maxiqt)+")*(1/" + str(x[scalebins.index(q)]) +")"
            a = a+ ")"       
            print a
            fileD.Close()                                                                                                                
            f2 = TFile(dire+channel + "ZllResolutionJune06PuppiRMSAlpha.root", "UPDATE");                                                           
            upd = updown[direction.index(dire)]
            for vari in variable:
                var = vari[direction.index(dire)]
                for reg in regions:
                    cutsList = [];binposition = [];binerror = [];ratio = [];data_fwhms = [];data_fwhm = [];data_errors = [];data_error = [];mc_fwhm = [];mc_fwhms = [];mc_error = [];mc_errors = []
                    print 'doing variable: ', dire , variablename[variable.index(vari)]
                    for i in bins:
                        mini = float(min(bins[bins.index(i)]))
                        maxi = float(max(bins[bins.index(i)]))
                        mid = float((mini+maxi)/2)
                        binposition.append(mid)
                        binerror.append(0.0)
                        if ((dependence == 'nVert') or (dependence == 'met_sumEt-zll_pt')):
                            cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) + " &&  zll_pt > 50 && (jet2_pt/zll_pt)< 0.3"]))
                        else:
                            cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini)]))
                    for i in cutsList:
                        print i
                        binLow = -70.; binHigh = 70.; nbins = 220;
                        x = RooRealVar("x", "x", binLow, binHigh)
                        for tree in trees:
                            if doBKGSubtraction:
                                if tree.name == 'tt':
                                    tt_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'tt', var+a,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, True)    
                                    tt_Hist = RooDataHist("tt","tt"+i,RooArgList(x),tt_hist)                 
                                    m_tt = tt_hist.GetMean()
                                    um_tt = tt_hist.GetMean()-tt_hist.GetRMS()
                                    uM_tt = tt_hist.GetMean()+tt_hist.GetRMS()
                                if tree.name == 'da':
                                    data_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var+a, nbins, binLow, binHigh,  i , 'noOF', variablename[variable.index(vari)]+i, True)
                                    data_Hist = RooDataHist("da","da"+i, RooArgList(x), data_hist)                  
                                    m_da = data_hist.GetMean()  
                                    um_da = data_hist.GetMean()-data_hist.GetRMS()
                                    uM_da = data_hist.GetMean()+data_hist.GetRMS()                                                   
                            else:
                                dy_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'dy', var+a, nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, True)
                                dy_Hist = RooDataHist("dy","dy"+i, RooArgList(x), dy_hist)
                                dy_BkgHist = RooDataHist()                                                          
                                m_dy = dy_hist.GetMean() 
                                um_dy = dy_hist.GetMean()-dy_hist.GetRMS()
                                uM_dy = dy_hist.GetMean()+dy_hist.GetRMS()
                        
                        if doBKGSubtraction:
                            data_fwhm, data_error = constructModel(data_Hist,data_hist,  tt_Hist, m_da, um_da, uM_da, True, channel+dependence, upd,  str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            data_fwhms.append(data_fwhm) 
                            data_errors.append(data_error)
                        else:
                            mc_fwhm, mc_error = constructModel(dy_Hist, dy_hist, dy_BkgHist, m_dy, um_dy, uM_dy, False, channel+dependence, upd, str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            mc_fwhms.append(mc_fwhm)
                            mc_errors.append(mc_error)
                    if doBKGSubtraction:
                        graph = TGraphErrors(len(binposition), array("f", binposition), array("f", data_fwhms), array("f", binerror), array("f", data_errors))
                        graph.Write (channel+"_met" +variablename[variable.index(vari)]+ "_vs_" + dependence);
                    else:
                        graph_mc = TGraphErrors(len(binposition), array("f", binposition), array("f", mc_fwhms), array("f", binerror), array("f", mc_errors))
                        graph_mc.Write (channel+"_met"+variablename[variable.index(vari)] + "_vs_" + dependence);
        f2.Close()







