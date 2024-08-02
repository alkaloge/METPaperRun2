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

def constructModel(Hist, hist, bkg_hist, bkg,  m, um,uM, BKGSubtraction, eemm, upd,  cut, var, plot_name):
    f = 0
    efwhm = 0
    integral = hist.Integral()
    plotmc = Canvas.Canvas("met/gammajets/resolution/mcfit/"+dire+var+dependence+cut, "png,root",0.6, 0.7, 0.8, 0.9)
    plotda = Canvas.Canvas("met/gammajets/resolution/fit/"+dire+var+dependence+cut , "png,root",0.6, 0.7, 0.8, 0.9)
    v_m.setVal(Hist.mean(x) );
    v_m.setRange(Hist.mean(x) - Hist.sigma(x), Hist.mean(x) + Hist.sigma(x));
    voigt = RooVoigtian ("voigt", "Voigtian", x, v_m, gamma_Z0, g_w)
    xFrame = x.frame()
    Hist.plotOn(xFrame)
    if BKGSubtraction:
    
        
        plotda = Canvas.Canvas("met/gammajets/resolution/fit/"+dire+var+dependence+cut , "png,root",0.6, 0.7, 0.8, 0.9)
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
        integral = ""
        plotmc = Canvas.Canvas("met/gammajets/resolution/mcfit/"+dire+var+dependence+cut, "png,root",0.6, 0.7, 0.8, 0.9)
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
#    if BKGSubtraction:
#        integral = hist.Integral()
#        #if xFrame.chiSquare() > 87:
#        #plotda = Canvas.Canvas("met/gammajets/resolution/fit/"+dire+var+dependence +cut+"_restricted" , "png",0.6, 0.7, 0.8, 0.9)                                                     
#        #print "Bad chi2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#        #result = voigt.fitTo(Hist, RooFit.Range(hist.GetMean()-2*hist.GetRMS(), hist.GetMean()+2*hist.GetRMS()), RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1))           
#        #voigt.plotOn(xFrame,RooFit.FillColor(r.kBlue),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))                        
#        #voigt.plotOn(xFrame,RooFit.LineColor(r.kBlue))                                                                                                                   
#        #xFrame.Draw()                                                                                                                                      
#        #sigma = g_w.getVal()
#        #gamma = gamma_Z0.getVal()
#        #esigma = g_w.getError()
#        #egamma = gamma_Z0.getError()
#        #Vsg = result.correlation(g_w, gamma_Z0)
#        #Vgs = result.correlation(gamma_Z0, g_w)
#        #Vss = result.correlation(g_w, g_w)
#        #Vgg = result.correlation(gamma_Z0, gamma_Z0)                            
#        if dependence == "nVert" and var == "uPerp":
#            if xFrame.chiSquare() > 50:                                                              
    print "hist ", hist.Integral(), " hist rms ", hist.GetRMS()
    print "bkg  ", bkg.Integral(), " hist rms ", bkg.GetRMS()
    hist.Add(bkg, -1)  
    print "after subtraction ", hist.Integral(), " hist rms ", hist.GetRMS()
    integral = hist.Integral()
    f = hist.GetRMS()
    efwhm = hist.GetRMSError()
    fromFit = False                                                                                                                                                        
#            else:
#                fromFit = True                                                                
#                f = FWHM(sigma, gamma)                                                        
#                efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)    
#                chi2 = xFrame.chiSquare()                                                     
#        else:
#            if xFrame.chiSquare() > 85:                                                              
#                f = hist.GetRMS()
#                efwhm = hist.GetRMSError()
#                chi2 = hist.GetRMSError()
#                fromFit = False                    
#            else:
#                fromFit = True                                                                
#                f = FWHM(sigma, gamma)                                                        
#                efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)    
#                chi2 = xFrame.chiSquare()                                                     
#        #    print "after restricting the range, the chi2 is now", xFrame.chiSquare()      
#        #else:
#        #    if FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg) > 2: 
#        #        f = hist.GetRMS()
#        #        efwhm = hist.GetRMSError()
#        #        chi2 = hist.GetRMSError()
#        #        fromFit = False                                                                                                                                                        
#        #    else:
#        #        f = FWHM(sigma, gamma)
#        #        chi2 = xFrame.chiSquare()
#        #        efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)
#        #        fromFit = True                                                                                                                                                        
#    else:
#        integral = hist.Integral()
#        if xFrame.chiSquare() > 10:
#            plotmc = Canvas.Canvas("met/gammajets/resolution/mcfit/"+dire+var+dependence +cut+"_restricted" , "png",0.6, 0.7, 0.8, 0.9)                                                     
#            result = voigt.fitTo(Hist, RooFit.Range(hist.GetMean()-2*hist.GetRMS(), hist.GetMean()+2*hist.GetRMS()), RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1))                                                                                
#            voigt.plotOn(xFrame,RooFit.FillColor(r.kBlue),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))                        
#            voigt.plotOn(xFrame,RooFit.LineColor(r.kBlue))                                                                                                                   
#            xFrame.Draw()                                                                                                                                      
#            sigma = g_w.getVal()
#            gamma = gamma_Z0.getVal()
#            esigma = g_w.getError()
#            egamma = gamma_Z0.getError()
#            Vsg = result.correlation(g_w, gamma_Z0)
#            Vgs = result.correlation(gamma_Z0, g_w)
#            Vss = result.correlation(g_w, g_w)
#            Vgg = result.correlation(gamma_Z0, gamma_Z0)                                                                                                                                                                                                    
#            if xFrame.chiSquare() > 10:                                                                                                                                                         
#                f = hist.GetRMS()                                                                                                                                                          
#                efwhm = hist.GetRMSError()                                                                                                                                                   
#                chi2 = 0                                                                                                                                                         
#                fromFit = False                                                                                                                                                        
#                print "after restricting the range, bad chi2, take RMS from histogram ", f                                              
#            else:
#                fromFit = True                                                                   
#                f = FWHM(sigma, gamma)                                                           
#                efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)       
#                chi2 = xFrame.chiSquare()                                                        
#                print "after restricting the range, the chi2 is now", xFrame.chiSquare()         
#        else:                                                                                                                           
#            f = FWHM(sigma, gamma)                                                                                                                                                      
#            chi2 = xFrame.chiSquare()                                                                                                                                                           
#            efwhm = FWHMError_fixed (sigma, gamma, esigma, egamma, Vss, Vsg, Vgs, Vgg)                                                                             
#            fromFit = True                                                                                                                                           
#            print 'got good chi2: ', xFrame.chiSquare() , ' on the first try, FWHM is ', f                                                           
    
    if BKGSubtraction:
        plotda.save(0, lumi, 0, "", "RMS (hist) %.2f +- %.2f"%(hist.GetRMS(), hist.GetRMSError()), var, "", integral, fromFit)                                                                                                                 
    else:
        if (upd ==""):                                                                                                                                                                                                                                                                                                           
            plotmc.save(0, lumi, 0, "", "RMS (hist) %.2f +- %.2f"%(hist.GetRMS(), hist.GetRMSError()), var, "", integral, fromFit)                                                                                                             
            
    print 'fwhm ', f
    print 'err ', efwhm
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


    doBKGSubtraction =False
    doPostFix = True
    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="just do a testrun. takes one variable in one eta for one region")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples.dat', help='the samples file. default \'samples.dat\'')
    (opts, args) = parser.parse_args()
    print 'Going to load DATA and MC trees...'
    bkgDatasets = ['QCD_HT200to300_ext', 'QCD_HT300to500_ext', 'QCD_HT500to700_ext',  'QCD_HT700to1000_ext','QCD_HT1000to1500_ext', 'QCD_HT1500to2000_ext', 'QCD_HT2000toInf_ext', 'WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400_ext','WJetsToLNu_HT400to600_ext','WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT800to1200_ext','WJetsToLNu_HT2500toInf_ext']
    #bkgDatasets = ['QCD_HT200to300_ext', 'QCD_HT300to500_ext', 'QCD_HT500to700_ext',  'QCD_HT700to1000_ext','QCD_HT1000to1500_ext', 'QCD_HT1500to2000_ext', 'QCD_HT2000toInf_ext', 'TGJets_ext', 'TTGJets', 'WGToLNuG_amcatnlo_ext', 'ZGTo2LG_ext', 'ZGTo2NuG','WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400_ext','WJetsToLNu_HT400to600_ext','WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT800to1200_ext','WJetsToLNu_HT1200to2500_ext', 'WJetsToLNu_HT2500toInf_ext']
    gjetsDatasets = ['GJets_HT40to100_ext','GJets_HT100to200', 'GJets_HT200to400_ext', 'GJets_HT400to600_ext','GJets_HT600toInf_ext' ]
    daDatasets = ['SinglePhoton_Run2016B_03Feb2017_v2', 'SinglePhoton_Run2016C_03Feb2017', 'SinglePhoton_Run2016D_03Feb2017', 'SinglePhoton_Run2016E_03Feb2017', 'SinglePhoton_Run2016F_03Feb2017', 'SinglePhoton_Run2016G_03Feb2017', 'SinglePhoton_Run2016H_03Feb2017_v2']
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
        uPerp = [makeUperp('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi')] 
        uPara = [makeUpara('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi')]
        uPerpRaw = [makeUperp('met_rawPt', 'met_rawPhi', 'gamma_pt', 'gamma_phi')] 
        uParaRaw = [makeUpara('met_rawPt', 'met_rawPhi', 'gamma_pt', 'gamma_phi')]
    else:
        #direction = [plot_name]
        direction = [plot_name,plot_name+'_up_jes_DY', plot_name+'_down_jes_DY', plot_name+'_up_jer_DY', plot_name+'_down_jer_DY',plot_name+'_up_uncl_DY', plot_name+'_down_uncl_DY']
        #updown = [""]
        updown = ["","_up", "_down",  "_jerUp", "_jerDown", "_unclUp", "_unclDown"]

        #uPara = [makeUpara('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi')] 
        #uPerp = [makeUperp('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi')] 
        #uPara = [makeUpara('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        #uPara = [makeUpara('met_jecUp_pt', 'met_jecUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_jecDown_pt', 'met_jecDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResUp_pt', 'met_shifted_JetResUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResDown_pt', 'met_shifted_JetResDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUpara('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        #uPara = [makeUpara('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUpara('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        uPara = [makeUpara('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_jecUp_pt', 'met_jecUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_jecDown_pt', 'met_jecDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResUp_pt', 'met_shifted_JetResUp_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResDown_pt', 'met_shifted_JetResDown_phi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUpara('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        uPerpRaw = [makeUperp('met_rawPt', 'met_rawPhi', 'gamma_pt', 'gamma_phi'), makeUperp('met_jecUp_rawPt', 'met_jecUp_rawPhi', 'gamma_pt', 'gamma_phi'), makeUperp('met_jecDown_rawPt', 'met_jecDown_rawPhi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_JetResUp_rawPt', 'met_shifted_JetResUp_rawPhi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_JetResDown_rawPt', 'met_shifted_JetResDown_rawPhi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_UnclusteredEnUp_rawPt', 'met_shifted_UnclusteredEnUp_rawPhi', 'gamma_pt', 'gamma_phi'),  makeUperp('met_shifted_UnclusteredEnDown_rawPt', 'met_shifted_UnclusteredEnDown_rawPhi', 'gamma_pt', 'gamma_phi')]
        uParaRaw = [makeUpara('met_rawPt', 'met_rawPhi', 'gamma_pt', 'gamma_phi'), makeUpara('met_jecUp_rawPt', 'met_jecUp_rawPhi', 'gamma_pt', 'gamma_phi'), makeUpara('met_jecDown_rawPt', 'met_jecDown_rawPhi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResUp_rawPt', 'met_shifted_JetResUp_rawPhi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_JetResDown_rawPt', 'met_shifted_JetResDown_rawPhi', 'gamma_pt', 'gamma_phi'), makeUpara('met_shifted_UnclusteredEnUp_rawPt', 'met_shifted_UnclusteredEnUp_rawPhi', 'gamma_pt', 'gamma_phi'),  makeUpara('met_shifted_UnclusteredEnDown_rawPt', 'met_shifted_UnclusteredEnDown_rawPhi', 'gamma_pt', 'gamma_phi')]
        #uPerp = [makeUperp('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        #uPerp = [makeUperp('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUperp('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 
        uPerp = [makeUperp('met_pt', 'met_phi', 'gamma_pt', 'gamma_phi'), makeUperp('met_jecUp_pt', 'met_jecUp_phi', 'gamma_pt', 'gamma_phi'), makeUperp('met_jecDown_pt', 'met_jecDown_phi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_JetResUp_pt', 'met_shifted_JetResUp_phi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_JetResDown_pt', 'met_shifted_JetResDown_phi', 'gamma_pt', 'gamma_phi'), makeUperp('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'gamma_pt', 'gamma_phi'),  makeUperp('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'gamma_pt', 'gamma_phi')] 


    #variable = [uParaRaw]
    #variable = [uPerpRaw, uParaRaw]
    variable = [uPerp, uPara]
    #variablename = ['_uParaRaw_']
    #variablename = ['_uPerpRaw_', '_uParaRaw_']
    variablename = ['_uPerp_', '_uPara_']
    #dependences = [ 'gamma_pt']
    dependences = [ 'met_sumEt-gamma_pt']
    #dependences = ['met_sumEt-gamma_pt']
    #dependences = ['gamma_pt',  'nVert', 'met_sumEt-gamma_pt']
    #dependences = [  'nVert']
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
    
    vtxbins = [[4, 6],[6, 8],[8, 10], [10, 12],[12,14], [14 ,16],[16, 18], [18, 20], [20,  22], [22, 24], [24, 26], [26, 28], [28, 32], [32, 40]]
    qtbins = [[50, 60],[60, 70], [70, 80],[80,100], [100, 120], [120, 140], [140,170],[170, 200],[200, 260] ,[260, 400]]
    #sumetbins = [[50, 400],  [400, 500],[500, 600], [600, 700], [700, 800],[800, 900],  [900, 1000],[1000, 1100], [1100, 1300],  [1300, 1600], [1600, 2500]]
    #sumetbins = [[200, 360], [360, 410], [410, 460],[460, 510], [510, 570], [570, 630],[630, 690],  [690, 750],[750, 820], [820, 900],[900, 990],[990, 1090], [1090, 1210], [1210, 1400],[1400, 1700], [1700, 2400]]
    sumetbins = [[350, 500],[500, 600],[600, 700],[700, 800], [800, 900],[900, 1000],[1000, 1100], [1100, 1200], [1200, 1400],[1400, 1700], [    1700, 2400]]
    #sumetbins = [[350, 450],[450, 500],  [500, 550], [550, 650],[650, 750],[750, 820], [820, 900],[900, 990],[990, 1090], [1090, 1210], [1210, 1400],[1400, 1700], [    1700, 2400]] 
    #sumetbins = [[300, 450], [450, 550], [550, 650], [650, 750],[750, 820], [820, 900],[900, 990],[990, 1090], [1090, 1210], [1210, 1400],[1400, 1700], [    1700, 2400]]
    #sumetbins = [[50, 300], [300,400], [400, 500],[500, 600], [600, 700], [700, 800],[800, 900],  [900, 1000],[1000, 1100], [1100, 1300],  [1300, 1600], [1600, 2500]]
    #sumetbins = [[100, 250], [250, 400],  [400, 500],[500, 600], [600, 700], [700, 800],[800, 900],  [900, 1000],[1000, 1100], [1100, 1300],  [1300, 1600], [1600, 2500]]
    #sumetbins =  [[0, 320], [320, 420],  [420, 520],[520, 620], [620, 720], [720, 820],[820, 920],  [920, 1020],[1020, 1120], [1120, 1300],  [1300, 1500], [1500, 2000], [2000, 2700]]
    #sumetbins = [[100, 350], [350, 450],  [450, 550],[550, 650], [650, 750], [750, 850],[850, 950],  [950, 1050],[1050, 1150], [1150, 1300],  [1300, 1500], [1500, 2000], [2000, 2700]]
    #sumetbins = [ [400, 460],[460, 530], [530, 610], [610, 700],[700, 800],  [800, 910],[910, 1030], [1030, 1180],[1180, 1300],[1300, 1500], [1500, 2000],[ 2000,3000 ]]
    scalebins = [ [0, 18], [18,24],[24, 30],[30, 38],[38, 46], [46, 52], [52, 60], [60, 68], [68, 76], [76, 84],[84,92],[92,100], [100, 115], [115, 130],  [130, 150], [150, 175], [175, 200], [200, 225], [225, 250], [250, 275],[275, 305], [305, 335], [335, 365], [365, 400], [400, 440],  [440, 500]]
    cutsList = []
    binposition = []
    binerror = []
    g_w = RooRealVar("g_w", "width Gaus", 10.,0. , 100., "GeV") # sigma
    gamma_Z0 = RooRealVar("gamma_Z0_U", "Z0 width", 2.3, 0., 100., "GeV") # gamma
    v_m = RooRealVar("v_m", "v_m",0,-10.,10.)
    for dependence in dependences :                                                                                                                                                                  
        if dependence == 'nVert':
            bins = vtxbins       
            leo = "nVert"
        if dependence == 'gamma_pt':
            bins = qtbins       
            leo = "qT"
        if dependence == 'met_sumEt-gamma_pt':
            bins = sumetbins       
            leo = "sumEt"
        for dire in direction:
            if doBKGSubtraction:
                fileD =  TFile("tgraphs/DatagjetsScaleMay25Mean.root");
            else: 
                fileD =  TFile("tgraphs/GJetsgjetsScaleMay25Mean.root");
            hScale = fileD.Get("met_uPara_over_qt");
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
            f2 = TFile(dire + "gjetsResolutionJune06"+leo+"RMS_alpha.root", "UPDATE");   
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
                        cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) + " &&  gamma_pt > 50 && (jet2_pt/gamma_pt)< 0.3"]))
                    for i in cutsList:
                        print i
                        #if dependence == 'nVert' and doBKGSubtraction == False:
                        #    binLow = -90.; binHigh = 90.; nbins = 510;
                        #else:
                        binLow = -80.; binHigh = 80.; nbins = 300;
                        #if ((dependence == 'met_sumEt-gamma_pt')):
                        #    if vari == uPara:
                        #        binLow = -100.; binHigh = 100.; nbins = 500;
                        #        if ((cutsList.index(i) == 10) ):
                        #            binLow = -100.; binHigh = 100.; nbins = 400;
                        #        if ((cutsList.index(i) == 7) ):
                        #            binLow = -100.; binHigh = 100.; nbins = 300;
                        #        if ((cutsList.index(i) < 7) ):
                        #            binLow = -150.; binHigh = 150.; nbins = 700;
                        #    if vari == uPerp:
                        #        binLow = -100.; binHigh = 100.; nbins = 500;
                        #        if ((cutsList.index(i) == 10) ):
                        #            binLow = -100.; binHigh = 100.; nbins = 400;
                        #        if ((cutsList.index(i) == 7) ):
                        #            if doBKGSubtraction:
                        #                binLow = -100.; binHigh = 100.; nbins = 300;
                        #            else:
                        #                binLow = -100.; binHigh = 100.; nbins = 350;
                        #        if ((cutsList.index(i) == 5) ):
                        #            binLow = -100.; binHigh = 100.; nbins = 500;
                        #        if ((cutsList.index(i) < 5) ):
                        #            if doBKGSubtraction:
                        #                binLow = -150.; binHigh = 150.; nbins = 700;
                        #            else:
                        #                binLow = -100.; binHigh = 100.; nbins = 700;
                        
                        
                        x = RooRealVar("x", "x", binLow, binHigh)
                        print nbins
                        for tree in trees:
                            if doBKGSubtraction:
                                if tree.name == 'bkg':
                                    #bkg_hist=tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'bkg',var,nbins, binLow, binHigh,i,'noOF', variablename[variable.index(vari)]+i, doPostFix)    
                                    bkg_hist=tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'bkg',var+a,nbins, binLow, binHigh,i,'noOF', variablename[variable.index(vari)]+i, doPostFix)    
                                    bkg_Hist = RooDataHist("bkg","bkg"+i,RooArgList(x),bkg_hist)                 
                                    m_bkg = bkg_hist.GetMean()
                                    um_bkg = bkg_hist.GetMean()-bkg_hist.GetRMS()
                                    uM_bkg = bkg_hist.GetMean()+bkg_hist.GetRMS()
                                if tree.name == 'da':
                                    #data_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                    data_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var+a,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                    data_Hist = RooDataHist("da","da"+i, RooArgList(x), data_hist)                  
                                    m_da = data_hist.GetMean()  
                                    um_da = data_hist.GetMean()-data_hist.GetRMS()
                                    uM_da = data_hist.GetMean()+data_hist.GetRMS()                                                   
                            if tree.name == 'gjets':
                                #gjets_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'gjets', var, nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                gjets_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'gjets', var+a, nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i, doPostFix)
                                gjets_Hist = RooDataHist("gjets","gjets"+i, RooArgList(x), gjets_hist)
                                gjets_BkgHist = RooDataHist()                                                          
                                m_gjets = gjets_hist.GetMean() 
                                um_gjets = gjets_hist.GetMean()-gjets_hist.GetRMS()
                                uM_gjets = gjets_hist.GetMean()+gjets_hist.GetRMS()
                                                                                                                                                                                                                        
                        if doBKGSubtraction:
                            #data_fwhm, data_error = constructModel(data_Hist, data_hist, bkg_Hist, bkg_hist, m_da, um_da, uM_da, True, channel, upd,  str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            plot_var = Canvas.Canvas("met/gammajets/gamma_"+variablename[variable.index(vari)]+str(cutsList.index(i)), "png,root,pdf,C", 0.1, 0.5, 0.2, 0.6)
                            plot_var.addHisto(data_hist, "P"   , "" , "P", r.kGreen , 1, 0)
                            plot_var.addHisto(bkg_hist, "P, SAME"   , "" , "P", r.kRed , 1, 0)
                            plot_var.save(1,  lumi, 0,  "",  "RMS (hist) %.2f +- %.2f"%(data_hist.GetRMS(), data_hist.GetRMSError()), variablename[variable.index(vari)]+" #gamma+jets", data_hist.Integral(), "", "")
                            data_hist.Add(bkg_hist, -1)
                            data_fwhms.append(data_hist.GetRMS())
                            data_errors.append(data_hist.GetRMSError())
                            print "data_hist.GetRMS() ", data_hist.GetRMS()
                            print "bkg _hist          ", bkg_hist.Integral()
                            #data_fwhms.append(data_fwhm)
                            #data_errors.append(data_error)
                        else: 
                            #mc_fwhm, mc_error = constructModel(gjets_Hist,gjets_hist,  gjets_BkgHist, 0, m_gjets, um_gjets, uM_gjets, False, channel, upd, str(cutsList.index(i)), variablename[variable.index(vari)], plot_name)
                            
                            mc_fwhms.append(gjets_hist.GetRMS())
                            mc_errors.append(gjets_hist.GetRMSError())
                            #mc_fwhms.append(mc_fwhm)
                            #mc_errors.append(mc_error)
                    if doBKGSubtraction:
                        graph = TGraphErrors(len(binposition), array("f", binposition), array("f", data_fwhms), array("f", binerror), array("f", data_errors))
                        graph.Write (channel+"_met" +variablename[variable.index(vari)]+ "_vs_" + dependence);
                    else:
                        graph_mc = TGraphErrors(len(binposition), array("f", binposition), array("f", mc_fwhms), array("f", binerror), array("f", mc_errors))
                        graph_mc.Write (channel+"_met"+variablename[variable.index(vari)] + "_vs_" + dependence);
        f2.Close()







