#####################################################################
#################### MET SCALE ######################################
#####################################################################
# this one makes the tgraphs with the scale of the different met types, in ee/mumu 


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

def newbins(hist, nbins, doBKGSubtraction):
    print "hist has integral ", hist.Integral()
    print "mid bin ",  hist.GetBinContent(hist.FindBin(-1)) 
    if (hist.GetBinContent(hist.FindBin(-1) )> 1.0): 
        if (hist.Integral()/(hist.GetBinContent(hist.FindBin(-1)))> 0.3* nbins): 
            if doBKGSubtraction:
                newbins =5*hist.Integral()/(hist.GetBinContent(hist.FindBin(-1)))
            else:
                newbins =3*hist.Integral()/(hist.GetBinContent(hist.FindBin(-1)))
            print  "make new bins ", int(newbins)
            return  int(newbins)
        else:
            return nbins
    else:
        return nbins


def makeUpara(met, phi,boson, boson_phi):
    uPara = ( "((( -"+ met + "*cos("+phi +" ) "+ " - " +boson + "*cos( " + boson_phi +"))* " + boson + "*cos( " +boson_phi +" )+(- "+ met + "*sin( "+ phi+ " )- " +boson+"*sin(" + boson_phi +" ))* " +boson +"*sin( " +boson_phi +" ))/" +boson+")/zll_pt" )
    return uPara

def constructModel(Hist, bkg_hist,  m, um,uM, BKGSubtraction, eemm,  updo, cut, var, plot_name, lumi):
    plotda = Canvas.Canvas("met/zjets/scale/fit/OLD"+eemm+"_"+updo+"_"+cut , "png",0.6, 0.7, 0.8, 0.9)
    mean = 0.
    error = 0.
    v_m.setVal(Hist.mean(x) );
    print 'set mean to ', Hist.mean(x) ;
    v_m.setRange(Hist.mean(x) - Hist.sigma(x), Hist.mean(x) + Hist.sigma(x));
    voigt = RooVoigtian ("voigt", "Voigtian", x, v_m, gamma_Z0, g_w)
    xFrame = x.frame()
    Hist.plotOn(xFrame)
    if BKGSubtraction:
        bkg_pdf =  RooHistPdf("bkg_pdf","bkg_pdf",RooArgSet(x),bkg_hist)
        lAbkgFrac = RooRealVar("AbkgFrac","AbkgFrac",0.5,0.,1.)
        sigbkgFrac = RooFormulaVar("bkgfrac","@0",RooArgList(lAbkgFrac))
        model = RooAddPdf("modelSB","modelSB",voigt,bkg_pdf,sigbkgFrac)
        result = model.fitTo (Hist, RooFit.Minimizer("Minuit","Migrad"),RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel (-1)) 
        model.plotOn(xFrame)
        model.plotOn(xFrame, RooFit.Components("bkg_pdf"), RooFit.LineColor(r.kRed)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kRed)  ,RooFit.DrawOption("F"))
        model.plotOn(xFrame, RooFit.Components("voigt")  , RooFit.LineColor(r.kGreen)  ,RooFit.LineStyle(r.kDashed),RooFit.FillColor(r.kGreen)  ,RooFit.DrawOption("L")) 
        xFrame.Draw()
        print 'chi2', xFrame.chiSquare()
    else:    
        plotmc = Canvas.Canvas("met/zjets/scale/mcfit/OLD"+eemm+"_vs_"+ updo+cut , "png",0.6, 0.7, 0.8, 0.9)
        result = voigt.fitTo(Hist, RooFit.Minimizer("Minuit","Migrad"), RooFit.Strategy(2), RooFit.SumW2Error(False), RooFit.Save(True), RooFit.PrintLevel(-1)) 
        voigt.plotOn(xFrame,RooFit.FillColor(r.kGray),RooFit.VisualizeError(result,1),RooFit.Components("voigt"))
        voigt.plotOn(xFrame,RooFit.LineColor(r.kGray))  
        xFrame.Draw()
    mean = v_m.getVal()  
    print 'after fit, mean is ', mean
    error = v_m.getError()  
    if BKGSubtraction:
        plotda.save(0, lumi, 0, xFrame.chiSquare(), "mean = %.2f"%(mean), "u_{||}/q_{T}", "")
    else:
        if (upd ==""):
            plotmc.save(0, lumi, 0, xFrame.chiSquare(),  "mean = %.2f"%(mean), "u_{||}/q_{T}", "") 
    return mean, error

if __name__ == "__main__":
    
    ##################################################################################################################################
    # start here: pick if you want to make the tgraph of the scale for data or mc, and ee or mumu
    doBKGSubtraction = False
    doee = False
    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples.dat', help='the samples file. default \'samples.dat\'')
    (opts, args) = parser.parse_args()
    print 'Going to load DATA and MC trees...'
    # pick all the trees and samples
    if doBKGSubtraction:
        if doee:
            tt = ['TTJets_DiLepton_ee' , 'WWTo2L2Nu_ee', 'TBarToLep_tch_ee', 'TBar_tWch_ee', 'T_tWch_ee', 'TToLep_sch_ee','TToLep_tch_ee',  'ZZTo2L2Nu_ee', 'WZTo3LNu_ee', 'WWW_ee', 'WWZ_ee', 'WZZ_ee', 'ZZZ_ee']
            da = ['DoubleEG_Run2016B_PromptReco_v2', 'DoubleEG_Run2016C_PromptReco_v2', 'DoubleEG_Run2016D_PromptReco_v2']
            channel = 'E'
            lumi = 12.9
        else:
            tt = ['TTJets_DiLepton_mm', 'WWTo2L2Nu_mm', 'TBarToLep_tch_mm', 'TBar_tWch_mm', 'T_tWch_mm',  'WWW_mm', 'WWZ_mm', 'WZZ_mm', 'ZZZ_mm', 'WZTo3LNu_mm']
            #tt = ['TTJets_DiLepton_mm', 'WWTo2L2Nu_mm', 'TBarToLep_tch_mm', 'TBar_tWch_mm', 'T_tWch_mm', 'TToLep_sch_mm','TToLep_tch_mm',  'WWW_mm', 'WWZ_mm', 'WZZ_mm', 'ZZZ_mm', 'WZTo3LNu_mm', 'ZZTo2L2Nu_mm']
            da = ['DoubleMuon_Run2016G_PromptReco_v2OLD']
            channel = 'M'            
            lumi =  7.554
        plot_name = 'Data'
        treeTT = Sample.Tree(helper.selectSamples(opts.sampleFile, tt, 'tt'), 'tt', 0)
        treeDA = Sample.Tree(helper.selectSamples(opts.sampleFile, da, 'da'), 'da', 1)
    else:
        if doee:
            dy = ['DYJetsToLL_M50_ee', 'ZZTo4L_ee', 'ZZTo2L2Q_ee', 'WZTo2L2Q_ee']
            channel = 'E'                                                                 
            lumi =  11.9
        else:                                                                             
            #dy = ['DYJetsToLL_M50_mm']
            dy = ['DYJetsToLL_M50_mm', 'ZZTo4L_mm']
            #dy = ['DYJetsToLL_M50_mmNEW', 'ZZTo4L_mm', 'ZZTo2L2Q_mm', 'WZTo2L2Q_mm' ]
            channel = 'M'                                                                 
            lumi = 7.554
        plot_name =  'DY'                                                                 
        treeDY = Sample.Tree(helper.selectSamples(opts.sampleFile, dy, 'dy'), 'dy', 0)          
        
    if doBKGSubtraction:
        # when doing the background subtraction, you only need the data and the background trees
        trees = [treeDA, treeTT] 
        updown = [""]  # the "direction" is set to just the regular value (i.e. uPara, uParaPuppi), since for data we don't want the jec and unclustered energy errors, this is just done in mc
        direction = [plot_name] 
        # define the uPara and uParaPuppi
        uPara = [makeUpara('met_pt', 'met_phi', 'zll_pt', 'zll_phi')] 
        uParaRaw = [makeUpara('met_rawPt', 'met_rawPhi', 'zll_pt', 'zll_phi')] 
        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi')] 
        uParaPuppiRaw = [makeUpara('metPuppi_rawPt', 'metPuppi_rawPhi', 'zll_pt', 'zll_phi')] 
        metx = ['met_pt*sin(met_phi)']
        mety = ['met_pt*cos(met_phi)']
    else:    
        # in this option you only need the signal mc, i.e. dy
        trees = [treeDY]
        # here we need to make the tgraphs for jec up/down and unclustered energy up/down, this goes in to the error calculation later 
        #direction = [plot_name]  
        direction = [plot_name]  
        #direction = [plot_name,plot_name+'_up_jes_DY', plot_name+'_down_jes_DY', plot_name+'_up_uncl_DY', plot_name+'_down_uncl_DY']  
        #updown = [""]  
        updown = [""]  
        #updown = ["","_up", "_down", "_unclUp", "_unclDown"]  
        uPara = [makeUpara('met_pt', 'met_phi', 'zll_pt', 'zll_phi'), makeUpara('met_jecUp_pt', 'met_jecUp_phi', 'zll_pt', 'zll_phi'), makeUpara('met_jecDown_pt', 'met_jecDown_phi', 'zll_pt', 'zll_phi'), makeUpara('met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'zll_pt', 'zll_phi'),  makeUpara('met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'zll_pt', 'zll_phi')] 
        uParaRaw = [makeUpara('met_rawPt', 'met_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('met_jecUp_rawPt', 'met_jecUp_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('met_jecDown_rawPt', 'met_jecDown_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('met_shifted_UnclusteredEnUp_rawPt', 'met_shifted_UnclusteredEnUp_rawPhi', 'zll_pt', 'zll_phi'),  makeUpara('met_shifted_UnclusteredEnDown_rawPt', 'met_shifted_UnclusteredEnDown_rawPhi', 'zll_pt', 'zll_phi')] 
        uParaPuppi = [makeUpara('metPuppi_pt', 'metPuppi_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecUp_pt', 'metPuppi_jecUp_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecDown_pt', 'metPuppi_jecDown_phi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_shifted_UnclusteredEnUp_pt', 'metPuppi_shifted_UnclusteredEnUp_phi', 'zll_pt', 'zll_phi'),  makeUpara('metPuppi_shifted_UnclusteredEnDown_pt', 'metPuppi_shifted_UnclusteredEnDown_phi', 'zll_pt', 'zll_phi')] 
        uParaPuppiRaw = [makeUpara('metPuppi_rawPt', 'metPuppi_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecUp_rawPt', 'metPuppi_jecUp_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_jecDown_rawPt', 'metPuppi_jecDown_rawPhi', 'zll_pt', 'zll_phi'), makeUpara('metPuppi_shifted_UnclusteredEnUp_rawPt', 'metPuppi_shifted_UnclusteredEnUp_rawPhi', 'zll_pt', 'zll_phi'),  makeUpara('metPuppi_shifted_UnclusteredEnDown_rawPt', 'metPuppi_shifted_UnclusteredEnDown_rawPhi', 'zll_pt', 'zll_phi')] 
        metx = ['met_pt*sin(met_phi)',  'met_jecUp_pt*sin(met_jecUp_phi)','met_jecDown_pt*sin(met_jecDown_phi)', 'met_shifted_UnclusteredEnUp_pt*sin(met_shifted_UnclusteredEnUp_phi)','met_shifted_UnclusteredEnDown_pt*sin(met_shifted_UnclusteredEnDown_phi)']
        mety = ['met_pt*cos(met_phi)',  'met_jecUp_pt*cos(met_jecUp_phi)','met_jecDown_pt*cos(met_jecDown_phi)', 'met_shifted_UnclusteredEnUp_pt*cos(met_shifted_UnclusteredEnUp_phi)','met_shifted_UnclusteredEnDown_pt*cos(met_shifted_UnclusteredEnDown_phi)']    
    variable = [uParaPuppiRaw]
    variablename = ['_uParaPuppiRaw_']
    #variablename = ['_uPara_','_uParaRaw_', '_uParaPuppi_','_uParaPuppiRaw_']
    dependence = 'zll_pt'
    dependences = [ 'zll_pt']
    print 'Trees successfully loaded...'
    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager.CutManager()

    regions = []
    # this little thing with the regions is just a residue from how my code is set up, to deal with different control/singal regions, but for this case it is not really essential, but it is still here. the region here is just picking the right selection for the leptons, otherwise defined in the include/CutManager.py
    region = Region.region('met' +variablename[0], 
            [cuts.leps()],
            'met_uPerp_zll',
            'zll_pt',
            variablename[0], 
            [range(-100,300,50)],
            False)
    regions.append(region)
    qtbins = [ [20,24],[24, 28],[28, 35], [35, 42], [42, 50], [50, 58], [58, 66], [66, 74], [74, 82],[82,90],[90,100], [100, 120], [120, 150], [150, 175], [175, 200], [200, 225], [225, 250], [250, 275],[275, 305], [305, 335], [335, 365], [365, 395], [395, 430],  [430, 500]]
    vtxbins = [[2, 4],[4 ,6],[6, 8], [8,  10],[10, 12],[12, 14],[14 ,16],[16,  18], [18, 20], [20,  22],[22,  24], [24, 26],[26,  28], [28,  30], [30, 32],[32,  34], [34 ,36],[36, 38], [38,  40] ]

    cutsList = []; binposition = []; binerror = []
    g_w = RooRealVar("g_w", "width Gaus", 10.,0. , 100., "GeV") # sigma
    gamma_Z0 = RooRealVar("gamma_Z0_U", "Z0 width", 2.3, 0., 100., "GeV") # gamma
    v_m = RooRealVar("v_m", "v_m",0,-2.,2.)
    for dependence in dependences :                                                                                                                                                                  
        if dependence == 'nVert':
            bins = vtxbins        
        if dependence == 'zll_pt':
            bins = qtbins       
        for dire in direction:
            f2 = TFile(dire + channel +"ZllScaleOLD2.root", "UPDATE");   # this is the file where all the tgraphs end up
            upd = updown[direction.index(dire)]
            for vari in variable:
                var = vari[direction.index(dire)]
                for reg in regions:
                    cutsList = [];binposition = [];binerror = [];ratio = [];data_means = [];data_errors = [];mc_means = [];mc_errors = []
                    print 'doing variable: ', dire , variablename[variable.index(vari)]
                    for i in bins:
                        # in this little loop is I make the cuts that should be applied on the z pt for every bin, might be a smarter way to do this but I DON'T CARE!!! :)
                        mini = float(min(bins[bins.index(i)]))
                        maxi = float(max(bins[bins.index(i)]))
                        mid = float((mini+maxi)/2)
                        binposition.append(mid)
                        binerror.append(0.0)
                        # binposition and binerror are filled here, pretty self explanatory, used to fill the tgraphs later
                        cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) ] ))
                        #cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) +"&& (nVert < 12)"] ))
                        #cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) +"&& (nVert >= 12)"+ "&& (nVert < 18)"] ))
                        #cutsList.append(cuts.AddList(reg.cuts + [  dependence +  "<"+ str(maxi) + "&&" + dependence + " >" + str(mini) +"&& (nVert >= 18)"] ))
                    for i in cutsList:
                        print i
                        # this is the most annoying part, the fit parameters, depending on the variable and the bin. These values are optimized for 12.9 inv fbs, but will have to change later. n.b. that this might also give different results depending on the flavour. GOOD LUCK HAVE FUN!
                    #    binLow = -1.7; binHigh = -0.3; nbins = 150;
                    #    if ((cutsList.index(i) < 12) ):
                    #        binLow = -2; binHigh = 0; nbins = 150;
                    #    if ((cutsList.index(i) < 9) ):
                    #        binLow = -2.5; binHigh = 0.5; nbins = 150;
                    #    if ((cutsList.index(i) < 7) ):
                    #        binLow = -3.0; binHigh = 1.; nbins = 150;
                    #    if ((cutsList.index(i) < 2) ):
                    #        binLow = -3.5; binHigh = 1.5; nbins = 150;  
                        binLow = -1.7; binHigh = -0.3; nbins = 170; # works for data old
                        if ((cutsList.index(i) < 12) ):
                            binLow = -2; binHigh = 0; nbins = 170;
                        if ((cutsList.index(i) < 9) ):
                            binLow = -2.5; binHigh = 0.5; nbins = 170;
                        if ((cutsList.index(i) < 7) ):
                            binLow = -3.0; binHigh = 1.; nbins = 170;
                        if ((cutsList.index(i) < 2) ):
                            binLow = -3.; binHigh = 1.5; nbins = 175;  
                        
                        
                        
                        
                        x = RooRealVar("x", "x", binLow, binHigh)
                        for tree in trees:
                            # so here loop over the trees, and get the TH1s for bkg, data or signal
                            if doBKGSubtraction:
                                if tree.name == 'da':
                                    data_hist_orig = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var, nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i)    
                                    data_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'da', var,newbins(data_hist_orig, nbins, doBKGSubtraction), binLow, binHigh,  i , 'noOF', variablename[variable.index(vari)]+i)
                                    data_Hist = RooDataHist("da","da"+i, RooArgList(x), data_hist)                  
                                    m_da = data_hist.GetMean()
                                    um_da = data_hist.GetMean()-data_hist.GetRMS()
                                    uM_da = data_hist.GetMean()+data_hist.GetRMS()                                                                         
                                if tree.name == 'tt':
                                    tt_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'tt', var, newbins(data_hist_orig, nbins, doBKGSubtraction), binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i)    
                                    tt_Hist = RooDataHist("tt","tt"+i,RooArgList(x),tt_hist)                 
                                    m_tt = tt_hist.GetMean()
                                    um_tt = tt_hist.GetMean()-tt_hist.GetRMS()
                                    uM_tt = tt_hist.GetMean()+tt_hist.GetRMS()                                                                                                      
                            else:
                                dy_hist_orig = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'dy', var,nbins, binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i)
                                dy_hist = tree.getTH1F(lumi, variablename[variable.index(vari)]+i+'dy', var,newbins(dy_hist_orig, nbins, doBKGSubtraction), binLow, binHigh,  i, 'noOF', variablename[variable.index(vari)]+i)
                                dy_Hist = RooDataHist("dy","dy"+i, RooArgList(x), dy_hist)
                                dy_BkgHist = RooDataHist()
                                m_dy = dy_hist.GetMean()
                                um_dy = dy_hist.GetMean()-dy_hist.GetRMS()
                                uM_dy = dy_hist.GetMean()+dy_hist.GetRMS()
                        if doBKGSubtraction:
                            # and then get the fits here 
                            data_mean, data_error = constructModel(data_Hist, tt_Hist, m_da, um_da, uM_da, True, channel+variablename[variable.index(vari)]+dependence, upd,  str(cutsList.index(i)), dire, plot_name, lumi)
                            # fill some lists with all the fitted results
                            data_means.append(-data_mean)
                            data_errors.append(data_error)
                        else:
                            mc_mean, mc_error = constructModel(dy_Hist, dy_BkgHist, m_dy, um_dy, uM_dy, False, channel+variablename[variable.index(vari)] + dependence, upd, str(cutsList.index(i)), dire, plot_name, lumi)
                            mc_means.append(-mc_mean)
                            mc_errors.append(mc_error)                                                                                                                                                       
                    if doBKGSubtraction:
                        # make a little tgraph with the results
                        graph = TGraphErrors(len(binposition), array("f", binposition), array("f", data_means), array("f", binerror), array("f", data_errors))
                        graph.Write (channel + "_met" +variablename[variable.index(vari)]+ "over_"+dependence);
                    else:
                        graph_mc = TGraphErrors(len(binposition), array("f", binposition), array("f", mc_means), array("f", binerror), array("f", mc_errors))
                        graph_mc.Write (channel + "_met"+variablename[variable.index(vari)] + "over_"+dependence);
        f2.Close()







