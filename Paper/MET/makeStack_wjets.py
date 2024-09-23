#!/usr/bin/env python

import ROOT as r
from ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath, SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue, kTeal, kOrange, TH1D, TH1F, TF1, kRed, TLegend
import math
import sys
import optparse
import array
import time
import copy
import os,ROOT
from array import array
import numpy as np
#import cmsstyle as CMS
#import cmsstyle as CMS
#import CMS_lumi, tdrstyle

import include.helper as helper
#import include.Region     as Region
import include.Canvas as Canvas
#import include.CutManager as CutManager
import include.Sample as Sample
#import include.Rounder    as Rounder




def fit_func(x, params, year="2018", isMC=True):
    mean = params[0]
    width = params[1]
    norm = params[2]
    a = params[3]
    b = params[4]
    c = params[5]
    sigma = params[1]
    #ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")
    gaussian=None
    polynomial_background=None
    # Breit-Wigner for the signal (Jacobian peak)
    breit_wigner = norm * (width**2 / ((x[0] - mean)**2 + width**2))
    # Polynomial for any remaining background
    #if not isMC : 
    #    if '2017' in year : polynomial_background = a + b*x[0] + c*x[0]**2 + 2*x[0]**3
    #    if 'Run2' in year : polynomial_background = a - b*5*x[0] + c*x[0]**2 
    #if isMC : polynomial_background = a + b*x[0] + c*x[0]**2 
    polynomial_background = a + b*x[0] + c*x[0]**2 
    
    #if '2017' in year : polynomial_background = a + b*x[0] + c*x[0]**2 + 10*x[0]**3
    gaussian = norm * ROOT.TMath.Gaus(x[0], mean, sigma, True)
    # Polynomial for the background
    return breit_wigner + polynomial_background
    #return gaussian + polynomial_background

def fit_funcD(x, params, year="2018", isMC=True):
    mean = params[0]
    width = params[1]
    norm = params[2]
    a = params[3]
    b = params[4]
    c = params[5]
    sigma = params[1]
    #ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")
    gaussian=None
    polynomial_background=None
    # Breit-Wigner for the signal (Jacobian peak)
    breit_wigner = norm * (width**2 / ((x[0] - mean)**2 + width**2))
    # Polynomial for any remaining background
    #if not isMC : 
    #    if '2017' in year : polynomial_background = a + b*x[0] + c*x[0]**2 + 2*x[0]**3
    #    if 'Run2' in year : polynomial_background = a - b*5*x[0] + c*x[0]**2 
    #if isMC : polynomial_background = a + b*x[0] + c*x[0]**2 
    polynomial_background = a + b*x[0] + c*x[0]**2 
    
    #if '2017' in year : polynomial_background = a + b*x[0] + c*x[0]**2 + 10*x[0]**3
    gaussian = norm * ROOT.TMath.Gaus(x[0], mean, sigma, True)
    # Polynomial for the background
    #return breit_wigner + polynomial_background
    #return gaussian + polynomial_background
    return breit_wigner + polynomial_background

def fit_funcc(x, params):
    mean = params[0]
    sigma = params[1]
    norm = params[2]
    a = params[3]
    b = params[4]
    c = params[5]

    # Gaussian for the signal (Jacobian peak)
    gaussian = norm * ROOT.TMath.Gaus(x[0], mean, sigma, True)

    # Polynomial for the background
    polynomial_background = a + b*x[0] + c*x[0]**2 

    #return gaussian + polynomial_background
    return gaussian 


def rebinHisto(original_hist, new_bins, suffix):

    # Create the new histogram with the specified bin edges
    new_hist = ROOT.TH1F( original_hist.GetName() + "_" + suffix, original_hist.GetTitle(), len(new_bins) - 1, array('d', new_bins) )

    # Iterate over the original histogram's bins
    for ibin in range(1, original_hist.GetNbinsX() + 1):
        bin_content = original_hist.GetBinContent(ibin)
        bin_error = original_hist.GetBinError(ibin)
        bin_center = original_hist.GetBinCenter(ibin)

        # Find the corresponding bin in the new histogram
        new_bin_index = new_hist.FindBin(bin_center)

        if new_bin_index > 0 and new_bin_index <= new_hist.GetNbinsX():
            # Add the content to the corresponding new bin
            new_hist.SetBinContent( new_bin_index, new_hist.GetBinContent(new_bin_index) + bin_content)
            new_hist.SetBinError( new_bin_index, math.sqrt(new_hist.GetBinError(new_bin_index)**2 + bin_error**2))
        elif new_bin_index > new_hist.GetNbinsX():
            # Handle overflow content
            new_hist.SetBinContent( new_hist.GetNbinsX(), new_hist.GetBinContent(new_hist.GetNbinsX()) + bin_content)
            new_hist.SetBinError( new_hist.GetNbinsX(), math.sqrt(new_hist.GetBinError(new_hist.GetNbinsX())**2 + bin_error**2))
        elif new_bin_index == 0:
            # Handle underflow content (if needed)
            new_hist.SetBinContent( 1, new_hist.GetBinContent(1) + bin_content)
            new_hist.SetBinError( 1, math.sqrt(new_hist.GetBinError(1)**2 + bin_error**2))
    #if 'qcd' in original_hist.GetName().lower() or 'qcd' in  original_hist.GetTitle().lower(): print ('==^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6======> during rebin', new_hist.Integral(), original_hist.Integral(), new_hist.GetNbinsX(), original_hist.GetNbinsX(), new_hist.GetBinError(10), original_hist.GetBinError(10))
    return new_hist







def SumAboveThreshold(hist, threshold):
    # Find the bin number corresponding to the threshold value
    bin = hist.FindBin(threshold)
    
    # Check if the bin is within the range of the histogram
    if bin < 1 or bin > hist.GetNbinsX():
        print("Threshold is out of histogram bounds.")
        return 0.0

    # Initialize the sum
    sum = 0.0
    
    # Iterate from the threshold bin to the last bin
    for i in range(bin, hist.GetNbinsX() + 1):
        sum += hist.GetBinContent(i)
    
    return sum




era = '2017'
channel = ''
if __name__ == "__main__":

    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    #parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples_2017.dat', help='the samples file. default \'samples.dat\'')
    parser.add_option('-y', '--year', action='store', type=str, dest='Year', default='2017', help='choose from 2016, 2017, 2018 \'samples.dat\'')
    parser.add_option('-v', '--variable', action='store', type=str, dest='varr', default='MET_T1_pt', help='variable to plot ')
    parser.add_option('-q', '--doqcd', action='store', type=str, dest='DoQCD', default=0, help='do data-driven QCD')
    parser.add_option('-e', '--extra', action='store', type=str, dest='ExtraTag', default='', help='extra Tag')
    parser.add_option('-c', '--channel', action='store', type=str, dest='Channel', default='', help='channel')
    parser.add_option('-l', '--local', action='store', type=str, dest='Local', default='', help='running local or on condor')
    parser.add_option('-f', '--file', action='store', type=str, dest='FileIn', default='', help='input file')
    parser.add_option('-s', '--syst', action='store', type=int, dest='dummySyst', default=0, help='replace systematics with dummy ones')
    (opts, args) = parser.parse_args()
    doDY = True
    doNPV = True
    doee = True
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()):
        doee = False
    if 'el' in str(opts.Channel.lower()):
        doee = True
    if doee:
        channel = 'ElNu'
    else:
        channel = 'MuNu'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era

    print('will read Datasets from plotS.root')

    lumis = {'2016': 35.93, '2017': 41.48, '2018': 59.83}
    lumis = {
        '2016': 36.91,
        '2017': 41.48,
        '2018': 59.83,
        '2016BpreVFP': 5.825,
        '2016CpreVFP': 2.62,
        '2016DpreVFP': 4.286,
        '2016EpreVFP': 4.0659,
        '2016FpreVFP': 2.865,
        '2016F': 0.584,
        '2016G': 7.653,
        '2016H': 8.74,
        '2016preVFP': 19.33,
        '2016postVFP': 16.98,
        '2017B': 4.80,
        '2017C': 9.57,
        '2017D': 4.25,
        '2017E': 9.315,
        '2017F': 13.54,
        'dry': 10,
        '2018A': 14.03,
        '2018B': 7.07,
        '2018C': 6.895,
        '2018D': 31.84,
        'Run2': 137}
    lumi = lumis[era]
    yields = {}
    print('Going to load DATA and MC trees...')

    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle()
    color = helper.color

    lumi_str = channel + 'lumi' + str(lumi)

    # plotS_2018_data_njetsgeq0_hitslt2_METWmass_MuMu.root
    isLog = 1
    doNormPlot = 1
    #SR = "isolt0p15_mtmassgt80"
    #B = "isolt0p15_mtmasslt80"
    #D = "isogt0p15_mtmasslt80"
    #C = "isogt0p15_mtmassgt80"

    #finB = fin.replace(SR, B)
    #finC = fin.replace(SR, C)
    #finD = fin.replace(SR, D)

    fin = '{0:s}'.format(str(opts.FileIn))
    finB = fin.replace('mtmassgt', 'mtmasslt')
    finC = fin.replace('isolt0p15', 'isogt0p15')
    finD = fin.replace('isolt0p15', 'isogt0p15')
    finD = finD.replace('mtmassgt', 'mtmasslt')

    SRincl = "isolt0p15_mtmassincl_pt1gt35"
    B = "isolt0p15_mtmassincl_pt1lt35"
    C = "isogt0p15_mtmassincl_pt1gt35"
    D = "isogt0p15_mtmassincl_pt1lt35"

    finB = fin.replace(SRincl, B)
    finC = fin.replace(SRincl, C)
    finD = fin.replace(SRincl, D)

    fIn = TFile.Open(fin, 'update')
    fInB = fInC = fInD = None
    doQCD = int(opts.DoQCD)
    #doQCD = True

    #fIn = TFile.Open('plotS.root'.format(str(opts.Year), str(opts.varr), str(opts.Channel)), 'read')
    print('fIn is.......', fIn.GetName())
    fIn.ls()
    tmp_histo = 0
    mc_histo = 0
    histo_err = 0
    mc_up = 0
    mc_down = 0
    mc_puup = 0
    mc_pudown = 0
    mc_idup = 0
    mc_iddown = 0
    mc_jerup = 0
    mc_jerdown = 0
    mc_jesup = 0
    mc_jesdown = 0
    mc_unclup = 0
    mc_uncldown = 0
    mc_stack = r.THStack()
    mc_stack_norm = r.THStack()
    # histo_dy_MET_T1_pt

    samples = ['dy', 'qcd', 'top', 'ew', 'ewk']
    # ewk ewknlo61 ewkincl
    givein = '{0:s}'.format(str(opts.varr))
    inn = str(opts.ExtraTag).lower()
    option = str(opts.varr)
    run_str = str(lumi)
    if 'nlo' in inn:
        if '61' not in inn:
            samples = ['dy', 'qcd', 'top', 'ew', 'ewknlo']
        if '61' in inn:
            samples = ['dy', 'qcd', 'top', 'ew', 'ewknlo61']

    if 'winclwnjets' in inn:
        samples = ['dy', 'qcd', 'top', 'ew', 'ewk']

    if 'incl' in inn and 'nlo' not in inn and 'wnjets' not in inn:
        if '61' not in inn:
            samples = ['dy', 'qcd', 'top', 'ew', 'ewkincl']
        if '61' in inn:
            samples = ['dy', 'qcd', 'top', 'ew', 'ewkincl61']

    if 'winclht' in inn:
        samples = ['dy', 'qcd', 'top', 'ew', 'ewkht']

    if 'qcdpt' in inn:
        samples[1] = 'qcdpt'
        inn = inn.replace('QCDHT', 'QCDPt')

    samples = ['dy',  'qcd', 'top', 'ew', 'ewknlo61']
    #samples = ['dy',  'qcd', 'ew', 'ewknlo61']
    samples = ['top',  'ew', 'dy', 'qcd',  'ewknlo61']


    #varbs = ['MET_T1_pt', 'PuppiMET_pt', 'boson_pt']
    # if 'all' not in givein :
    varbs = []
    varbs.append(givein)
    print('will do the following', varbs, fIn.GetName())
    systs = ['JES', 'Unclustered', 'JER']
    systs = ['JES', 'Unclustered']
    Othersysts = ['ID', 'PU']

    dirs = ['Up', 'Down']
    colors = {'dy': kYellow,'dynlo': kYellow + 1,'qcd': kMagenta,        'top': kBlue,        'ew': kGreen + 2,        'ewk': kCyan,        'ewknlo': kCyan + 1}
    colors = {'dy': kYellow,'qcd': kMagenta,'qcdpt': kMagenta,        'top': kBlue,        'ew': kGreen + 2,        'ewk': kCyan,        'ewknlo': kCyan + 1,        'ewknlo61': kCyan + 1,        'ewkincl': kTeal,        'ewkincl61': kTeal - 4,        'ewkht': kCyan + 1}

    colors = {'dy': "#f89c20",  'dynlo': "#f89c20", 'qcd': "#832db6",'top': "#3f90da",  'ew': "#e42536",'ewknlo': "#92dadd",'ewknlo61': "#92dadd", 'ewk': "#92dadd", 'ewkincl': "#92dadd"}

    channel = ''
    doStat = True
    #doStat = False
    doSyst = True
    #doSyst = False
    doRebin = False
    extractJacob = False
    if '_mt' in givein or '_pt' in givein: extractJacob = True
    #extractJacob = False
    bins= []
    for ib in range(0,410,10): bins.append(ib)
    for ib in range(410,500,50): bins.append(ib)
    bins.append(1000)
    bins=[]
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150,160, 170,180,190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 350]
    binsmt = [0, 5,10, 15,20, 25,30,35, 40,45, 50,55, 60,65, 70, 75,80, 85,90,95, 100,105, 110, 120, 130, 140, 150,160, 170,180,190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 350]
    binsmt=list(range(0, 141, 5))
    binslpt=list(range(0, 141, 4))
    binslpt=list(np.arange(20, 141, 5))
    binspt=list(range(0, 241, 5))
    binsmt80=list(range(80, 141, 5))
    binsmt10=list(range(0, 141, 10))
    bins=binsmt
    if 'gt80' in inn and 'boson_mt' in givein: bins=binsmt80
    if '30to40' in inn or 'pugeq' in inn or '40to50' in inn: bins = binslpt
    if 'boson_pt' in givein : bins=binspt
    print (bins)
    if 'open' in fin :
        if '_transm' in givein or '_mt' in givein or '_pt' in givein : 
            doRebin = True

        if 'pt_1' in givein : 
            doRebin = True
            bins = binslpt

    #if 'mll' in givein or 'Raw' in givein or 'boson_pt' in givein or 'boson_phi' in givein or '_significance' in givein: doSyst = False
    if 'mll' in givein or 'Raw' in givein or '_significance' in givein or 'njets_' in givein:
        doSyst = False
    #if 'boson_pt' in givein or 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein: doSyst = False
    #if 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein or 'boson_pt' in givein: doSyst = False
    if 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein or 'pt_1' in givein:
        doSyst = False
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()):
        channel = 'MuNu'
    else:
        channel = 'ElNu'

    dodummySyst = opts.dummySyst
    if dodummySyst : 
        doSyst = False
        doStat = False
    print ('============================doStat', doStat, 'doSyst', doSyst, 'dodummySyst', dodummySyst)
    era = str(opts.Year)
    eras = str(opts.Year)
    run = era
    print('lets see what syst you run doSyst', doSyst, 'doStat', doStat)
    leg = [0.65, 0.6, 0.81, 0.9]
    puname = ''
    data_hist = fIn.Get('histo_data')
    data_hist_rebin = fIn.Get('histo_data')
    if 'openbin' in fin and doRebin:
        histo_rebin = rebinHisto(data_hist,bins,data_hist.GetName()+'_rebin')
        threshold = 300.0;
        sum = SumAboveThreshold(data_hist, threshold);
        print ('before rebin', data_hist.GetNbinsX(), data_hist.Integral(), data_hist.GetSumOfWeights(), data_hist.GetBinContent( data_hist.GetNbinsX()), 'sum above ', threshold, sum)
        data_hist_rebin = histo_rebin
        sum = SumAboveThreshold(data_hist_rebin, threshold);
        print ('after rebin', data_hist_rebin.GetNbinsX(),data_hist_rebin.Integral(), data_hist_rebin.GetSumOfWeights(), data_hist_rebin.GetBinContent( data_hist_rebin.GetNbinsX()), 'sum above ', threshold, sum)


    # data_hist.Sum2()
    varTitle = 'p_{T}^{miss} [GeV]'
    if 'boson_pt' in givein:
        varTitle = 'W q_{T} [GeV]'
    if 'boson_phi' in givein:
        varTitle = 'W #phi'
    if 'PuppiMETmTmass' in givein:
        varTitle = 'm_{T} [GeV]'
    if 'njets' in givein:
        varTitle = 'njets'
    if 'DphiWMET' in givein:
        varTitle = '#Delta#Phi(W,p_{T}^{miss})'
    if 'DphilMET' in givein:
        varTitle = '#Delta#Phi(#mu,p_{T}^{miss})'
    if 'PuppiMET' in givein:
        varTitle = 'p_{T}^{miss} [GeV]'
    if 'wtmass' in givein.lower():
        varTitle = 'W_{T} [GeV]'
    if 'wmass' in givein.lower():
        varTitle = 'W [GeV]'
    if 'pt_1' in givein:
        varTitle = 'p_{T}(#mu)'
    if 'eta_1' in givein:
        varTitle = '#eta(#mu)'
    if 'phi' in givein:
        varTitle = '#phi'
    if 'mll' in givein:
        varTitle = 'M(ll) [GeV]'
    if 'u_perp' in givein:
        varTitle = 'u_{#perp} [GeV]'
    if 'u_par' in givein:
        varTitle = 'u_{#parallel}  [GeV]'
    if 'u_par_boson' in givein or "u_parboson" in givein:
        varTitle = 'u_{#parallel} + q_{T} [GeV]'
    if 'METCorboson_pt' in givein:
        varTitle = 'W q_{T} [GeV]'
    if 'METCorboson_phi' in givein:
        varTitle = 'W #phi'
    if 'METCorboson_transm' in givein:
        varTitle = 'm_{T} [GeV]'
    if 'boson_mt' in givein:
        varTitle = 'm_{T} [GeV]'
    if '_transm' in givein:
        varTitle = 'm_{T} [GeV]'
    if 'boson_m' in givein and 'mt' not in givein:
        varTitle = 'W mass [GeV]'
    # and '_pt' in givein : varTitle = 'PUPPI-p_{T}^\rm{miss} [GeV]'
    if 'PuppiMET' in givein:
        varTitle = 'Puppi-' + varTitle
    if 'MET' in givein and 'Puppi' not in givein:
        if 'Smear' not in givein:
            varTitle = 'PF-' + varTitle
        if 'Smear' in givein:
            varTitle = 'PF-' + varTitle
    #if 'PuppiMET' not in givein and '_pt' in givein : varTitle = 'PUPPI-p_{T}^{miss} [GeV]'
    if 'Raw' in givein:
        varTitle = 'Raw-' + varTitle


    if 'dPhiPuppiMET' in givein or 'dPhiMET' in givein:
        if 'J1' in givein:
            varTitle = '#Delta#Phi(p_{T}^{miss}, J_{1})'
        if 'J2' in givein:
            varTitle = '#Delta#Phi(p_{T}^{miss}, J_{2})'
    if 'dRPuppiMET' in givein or 'dRMET' in givein:
        if 'J1' in givein:
            varTitle = '#DeltaR(p_{T}^{miss}, J_{1})'
        if 'J2' in givein:
            varTitle = '#DeltaR(p_{T}^{miss}, J_{2})'


    varTitle = varTitle.replace("[GeV] [GeV]", "[GeV]")
    kFactor = 1.
    #### Jacobian Fit
    hMC_total = data_hist.Clone("hMC_total")
    hMC_wjets = data_hist.Clone("hMC_wjets")
    hdata_wjets = data_hist.Clone("hdata_wjets")

    if doRebin : 
        hMC_total = data_hist_rebin.Clone("hMC_total")
        hMC_wjets = data_hist_rebin.Clone("hMC_wjets")
        hdata_wjets = data_hist_rebin.Clone("hdata_wjets")
    
    hMC_total.Reset()
    hMC_wjets.Reset()

    ## at this point we have a data histo, and two empty ones, one for total MC, another to fill Wjets only

    contribution_dict = {}

    v=varbs[0]
    for i in range(0, len(samples)):
        s = str(samples[i])
        histo = fIn.Get("histo_" + s + "_" + v)
        print("==================> histo_" + s + "_" + v)
        if doRebin : 
            histo_rebin = rebinHisto(histo,bins,histo.GetName()+'_rebin')
            histo = histo_rebin

        hMC_total.Add(histo)

    #hMC_total holds ALL MC now

    for i in range(len(samples)):
        s = str(samples[i])
        histo = fIn.Get("histo_" + s + "_" + v)
        if doRebin : 
            histo_rebin = rebinHisto(histo,bins,histo.GetName()+'_rebin')
            histo = histo_rebin
      
        if '61' in s:
            histo.SetTitle(histo.GetTitle().replace("-61", ""))
            histo.Scale(kFactor)
            hMC_wjets.Add(histo)
            # histo.Sumw2()
        #if 'dy' in s : histo.Scale(0.9)
        if '61' not in s and 'ewk' not in s:
            hdata_wjets.Add(histo,-1)
        
        # Calculate the contribution of the current sample
        contribution = histo.Integral() / hMC_total.Integral() * 100
        contribution_dict[s] = contribution

        # Calculate the data/MC difference
        data_mc_difference = histo.Integral() - hMC_total.Integral()

    print("Contribution Table:")

    # Calculate the maximum length of process names for alignment
    max_length = max(len(str(sample)) for sample in samples)

    print('\033[91m' + "-------------------------------------------------------------------------" + '\033[0m')
    # Print the process names as columns
    for sample in samples:
        process_name = str(sample)
        print(process_name.ljust(max_length + 5), end=' ')
    print("Total MC\t\tData\tData/MC")

    # Print the contribution values below each process
    for sample in samples:
        contribution = contribution_dict.get(str(sample), 0)
        print("{:.2f}".format(contribution).ljust(max_length + 5), end=' ')

    # Print the total MC, data, and data/MC ratio
    # Print the total MC, data, and data/MC ratio with two significant digits
    print("{:.2f}\t".format(hMC_total.Integral()).ljust(max_length + 5), end=' ')
    print("{:.2f}\t".format(data_hist.Integral()).ljust(max_length + 5), end=' ')
    print("{:.2f}\t".format(data_hist.Integral() / hMC_total.Integral()))

    print('\033[91m' + "-------------------------------------------------------------------------" + '\033[0m')
    print('\033[91m' + "-------------------------------------------------------------------------" + '\033[0m')

    kFactor = float(data_hist.GetSumOfWeights() / hMC_total.GetSumOfWeights())
    if 'noscale' in str(opts.ExtraTag).lower():
        kFactor = 1.

    # Print the contribution table
    normQCD = 1.
    if doQCD:

        print('filenames in sideband', finB, finC, finD)
        fInB = TFile.Open(finB, 'read')
        fInC = TFile.Open(finC, 'read')
        fInD = TFile.Open(finD, 'read')
        print('filenames in sideband', fInB.GetName(), fInC.GetName())
        v=varbs[0]

        data_histB = data_histC = data_histD = None
        data_histB_orig = data_histC_orig = data_histD_orig = None
        data_histB_syst = data_histC_syst = data_histD_syst =None
        histoB = histoC = histoD = None
        data_histB = fInB.Get('histo_dataB')
        #fInB.Close()
        data_histC = fInC.Get('histo_dataC')
        #data_histC = fInC.Get('histo_ewknlo61_METCorboson_mt')
        #fInC.Close()
        data_histD = fInD.Get('histo_dataD')
        #fInD.Close()
        print('data in sideband before rebin B', data_histB.GetSumOfWeights())
        print('data in sideband before rebin C', data_histC.GetSumOfWeights())
        print('data in sideband before rebin D', data_histD.GetSumOfWeights())

        if doRebin:
            data_histB_rebin = rebinHisto(data_histB,bins,data_histB.GetName()+'_rebin')
            data_histB =data_histB_rebin.Clone()

            data_histC_rebin = rebinHisto(data_histC,bins,data_histC.GetName()+'_rebin')
            data_histC = data_histC_rebin.Clone()

            data_histD_rebin = rebinHisto(data_histD,bins,data_histD.GetName()+'_rebin')
            data_histD = data_histD_rebin.Clone()

        data_histB_orig = data_histB.Clone()
        data_histC_orig = data_histC.Clone()
        data_histD_orig = data_histD.Clone()

        print ('reading from files', fInB.GetName(), fInC.GetName(), fInD.GetName())
        print('data in sideband B', data_histB.GetSumOfWeights(), 'D', data_histD.GetSumOfWeights(), 'shape C', data_histC.GetSumOfWeights(), data_histB.GetNbinsX())
        #print('data in sideband B', data_histB_orig.GetSumOfWeights(), 'D', data_histD_orig.GetSumOfWeights(), 'shape C ', data_histC_orig.GetSumOfWeights(), data_histB.GetNbinsX())
        # for s in samples :
        
        for i in range(0, len(samples)):
            s = str(samples[i])
            #histo = fIn.Get("histo_" + s + "_" + v)
            #if doRebin : 
            #    histo_rebin = rebinHisto(histo,bins,histo.GetName()+'_rebin')
            #    histo = histo_rebin.Clone()

            if 'qcd' not in s:  # get all histograms in the SB regions but not QCD --> this is what you are going to calculate
                histoB = fInB.Get("histo_" + s + "_" + v+"B")
                histoC = fInC.Get("histo_" + s + "_" + v+"C")
                histoD = fInD.Get("histo_" + s + "_" + v+"D")
                print ('reading auxiliary histograms for qcd datadriven', histoB.Integral(), histoC.Integral(), histoD.Integral())
                if doRebin : 
                    histoB_rebin = rebinHisto(histoB,bins,histoB.GetName()+'_rebin')
                    histoB = histoB_rebin
                    histoC_rebin = rebinHisto(histoC,bins,histoC.GetName()+'_rebin')
                    histoC = histoC_rebin
                    histoD_rebin = rebinHisto(histoD,bins,histoD.GetName()+'_rebin')
                    histoD = histoD_rebin
                print ('reading auxiliary histograms for qcd datadriven', histoB.Integral(), histoC.Integral(), histoD.Integral(), histoB.GetName(), histoB.GetTitle())

                data_histB.Add(histoB, -1)
                data_histC.Add(histoC, -1)
                data_histD.Add(histoD, -1)

                #### systematics
                if doStat:
                    for sy in Othersysts:
                        for d in dirs:
                            hname = "histo_" + s + "_" + v + sy + d
                            htemp = htemp=htempC=htempD= None
                            htemp = fIn.Get(hname)
                            htempB = fInB.Get(hname+"B")
                            htempC = fInC.Get(hname+"C")
                            htempD = fInD.Get(hname+"D")
                            if doRebin : 
                                htemp_rebin = rebinHisto(htemp,bins,htemp.GetName()+'_rebin')
                                htemp = htemp_rebin
                                htempB_rebin = rebinHisto(htempB,bins,htempB.GetName()+'_rebin')
                                htempB = htempB_rebin
                                htempC_rebin = rebinHisto(htempC,bins,htempC.GetName()+'_rebin')
                                htempC = htempC_rebin
                                htempD_rebin = rebinHisto(htempD,bins,htempD.GetName()+'_rebin')
                                htempD = htempD_rebin
                            data_histB_syst = data_histB_orig.Clone()
                            data_histC_syst = data_histC_orig.Clone()
                            data_histD_syst = data_histD_orig.Clone()

                            data_histB_syst.Add(htempB, -1)
                            data_histC_syst.Add(htempC, -1)
                            data_histD_syst.Add(htempD, -1)
                      
                            ###this is for the iso vs mT  method             
                            '''
                            normQCDs = float(data_histB_syst.Integral() / data_histD_syst.Integral())
                            data_histC_syst.Scale(normQCDs)
                            data_histC_syst.SetTitle("histo_qcd_datadriven_invIso")
                            data_histB_syst.SetTitle("histo_qcd_datadriven_invMt")
                            data_histD_syst.SetTitle("histo_qcd_datadriven_invIsoinvMt")
                            '''

                            normQCDs = float(data_histC_syst.Integral() / data_histD_syst.Integral())
                            data_histB_syst.Scale(normQCDs)

                            data_histB_syst.SetName("histo_qcd_data_B_" + v + sy +d)
                            data_histC_syst.SetName("histo_qcd_data_C_" + v + sy +d)
                            data_histD_syst.SetName("histo_qcd_data_D_" + v + sy +d)

                            data_histC_syst.SetTitle("histo_qcd_datadriven_invIso")
                            data_histB_syst.SetTitle("histo_qcd_datadriven_invpT")
                            data_histD_syst.SetTitle("histo_qcd_datadriven_invIsoinvpT")

                            fIn.cd()
                            data_histB_syst.Write()
                            data_histC_syst.Write()
                            data_histD_syst.Write()

                            print ('estimation of qcd datadriven B for systematics',  data_histB_syst.Integral(), 'C', data_histC_syst.Integral(), 'D', data_histD_syst.Integral(), sy, d, 'norm', normQCDs)

                if doSyst:
                    for sy in systs:
                        for d in dirs:
                            hname = "histo_" + s + "_" + v + sy + d
                            htemp = htemp=htempC=htempD= None
                            htemp = fIn.Get(hname)
                            htempB = fInB.Get(hname+"B")
                            htempC = fInC.Get(hname+"C")
                            htempD = fInD.Get(hname+"D")
                            if doRebin : 
                                htemp_rebin = rebinHisto(htemp,bins,htemp.GetName()+'_rebin')
                                htemp = htemp_rebin
                                htempB_rebin = rebinHisto(htempB,bins,htempB.GetName()+'_rebin')
                                htempB = htempB_rebin
                                htempC_rebin = rebinHisto(htempC,bins,htempC.GetName()+'_rebin')
                                htempC = htempC_rebin
                                htempD_rebin = rebinHisto(htempD,bins,htempD.GetName()+'_rebin')
                                htempD = htempD_rebin
                            data_histB_syst = data_histB_orig.Clone()
                            data_histC_syst = data_histC_orig.Clone()
                            data_histD_syst = data_histD_orig.Clone()

                            data_histB_syst.Add(htempB, -1)
                            data_histC_syst.Add(htempC, -1)
                            data_histD_syst.Add(htempD, -1)
                      
                            '''
                            normQCDs = float(data_histB_syst.Integral() / data_histD_syst.Integral())
                            data_histC_syst.Scale(normQCDs)
                            data_histB_syst.SetName("histo_qcd_data_B_" + v + sy +d)
                            data_histC_syst.SetName("histo_qcd_data_C_" + v + sy +d)
                            data_histD_syst.SetName("histo_qcd_data_D_" + v + sy +d)
                            data_histC_syst.SetTitle("histo_qcd_datadriven_invIso")
                            data_histB_syst.SetTitle("histo_qcd_datadriven_invMt")
                            data_histD_syst.SetTitle("histo_qcd_datadriven_invIsoinvMt")
                            '''


                            normQCDs = float(data_histC_syst.Integral() / data_histD_syst.Integral())
                            data_histB_syst.Scale(normQCDs)
                            data_histB_syst.SetName("histo_qcd_data_B_" + v + sy +d)
                            data_histC_syst.SetName("histo_qcd_data_C_" + v + sy +d)
                            data_histD_syst.SetName("histo_qcd_data_D_" + v + sy +d)
                            data_histC_syst.SetTitle("histo_qcd_datadriven_invIso")
                            data_histB_syst.SetTitle("histo_qcd_datadriven_invpT")
                            data_histD_syst.SetTitle("histo_qcd_datadriven_invIsoinvpT")

                            fIn.cd()
                            data_histB_syst.Write()
                            data_histC_syst.Write()
                            data_histD_syst.Write()

                            print ('estimation of qcd datadriven B for systematics',  data_histB_syst.Integral(), 'C', data_histC_syst.Integral(), 'D', data_histD_syst.Integral(), sy, d, 'norm', normQCDs)

        print ('estimation of qcd datadriven B',  data_histB.Integral(), 'C', data_histC.Integral(), 'D', data_histD.Integral())
        fIn.cd()
        for ibin in range(1, data_histB.GetNbinsX() + 1):
            if data_histB.GetBinContent(ibin)< 0. :
                data_histB.SetBinContent(ibin,0.)
                data_histB.SetBinError(ibin,0.)

            if data_histD.GetBinContent(ibin)< 0. :
                data_histD.SetBinContent(ibin,0.)
                data_histD.SetBinError(ibin,0.)

            if data_histC.GetBinContent(ibin)< 0. :
                data_histC.SetBinContent(ibin,0.)
                data_histC.SetBinError(ibin,0.)


        normQCD = float(data_histC.Integral() / data_histD.Integral())
        data_histB.Scale(normQCD)
        #normQCD = float(data_histB.Integral() / data_histD.Integral())
        #data_histC.Scale(normQCD)

        data_histC.SetName("histo_qcd_data_C_" + v)

        data_histB.SetName("histo_qcd_data_B_" + v)
        data_histD.SetName("histo_qcd_data_D_" + v)
        '''
        data_histC.SetTitle("histo_qcd_datadriven_invIso")
        data_histB.SetTitle("histo_qcd_datadriven_invMt")
        data_histD.SetTitle("histo_qcd_datadriven_invIsoinvMt")
        '''

        data_histC.SetTitle("histo_qcd_datadriven_invIso")
        data_histB.SetTitle("histo_qcd_datadriven_invpT")
        data_histD.SetTitle("histo_qcd_datadriven_invIsoinvpT")

        data_histB.Write()
        data_histC.Write()
        data_histD.Write()
        #fIn.Write()
        fIn.ls()
        print('some infor for QCD data driven', data_histC.GetSumOfWeights(), normQCD, 'B/D', data_histB.Integral() / data_histD.Integral() , 'C/D', data_histC.Integral() / data_histD.Integral())
    # exit()
   
        print('some info for QCD data driven outside the loop', data_histC.GetSumOfWeights(), normQCD, 'B/D', data_histB.Integral() / data_histD.Integral() , 'C/D', data_histC.Integral() / data_histD.Integral())
    print (samples)

    if extractJacob : 
        #reget data and subtract scaled MC now
        hdata_wjets = data_hist.Clone("hdata_wjets")
        hMC_wjets = data_hist.Clone("hMC_wjets")
        if doRebin : 
            hMC_wjets = data_hist_rebin.Clone("hMC_wjets")
            hdata_wjets = data_hist_rebin.Clone("hdata_wjets")
        
        hMC_wjets.Reset()
        for i in range(len(samples)):
            s = str(samples[i])
            histo= None
            if not doQCD : histo = fIn.Get("histo_" + s + "_" + v)
            if doQCD : 
                if 'qcd' not in s : histo = fIn.Get("histo_" + s + "_" + v)
                if 'qcd'  in s : histo = fIn.Get("histo_qcd_data_B_" + v)
            if doRebin : 
                histo_rebin = rebinHisto(histo,bins,histo.GetName()+'_rebin')
                histo = histo_rebin.Clone()

            if kFactor != 1 : histo.Scale(kFactor)

            if '61' in s and 'ewk' in s:
                histo.SetTitle(histo.GetTitle().replace("-61", ""))
                hMC_wjets.Add(histo)
            if '61' not in s and 'ewk' not in s:
                hdata_wjets.Add(histo,-1)
            #    for ibin in range(1, histo.GetNbinsX() + 1):
            #        hdata_wjets.SetBinContent(ibin,  hdata_wjets.GetBinContent(ibin) - histo.GetBinContent(ibin))
            #        hdata_wjets.SetBinError(ibin,  math.sqrt(hdata_wjets.GetBinContent(ibin)))

        fit_function = None
        fit_functionD = None
        xMin = 0
        xMax= 120
        if '_mt' in givein : 
            fit_function = TF1("fit_function", fit_func, 40, 135, 6)
            fit_function.SetParameters(80.4, 15.0, 2300000, 20000, 2, 200)  # Initial guesses for the parameters
            fit_functionD = TF1("fit_functionD", fit_funcD, 40, 135, 6)
            fit_functionD.SetParameters(80.4, 15.0, 2300000, 20000, 2, 200)  # Initial guesses for the parameters
            #fit_function.FixParameter(0, 40.2*2)
            #fit_functionD.FixParameter(0, 40.2*2)

        if '_pt' in givein and 'T1' not in givein: 
            fit_function = TF1("fit_function", fit_func, 0, 120, 6)
            fit_function.SetParameters(80.4/2, 15.0/2, 2300000, 20000, 2, 20)  # Initial guesses for the parameters
            fit_functionD = TF1("fit_functionD", fit_funcD, 0, 120, 6)
            fit_functionD.SetParameters(80.4/2, 15.0/2, 2300000, 20000, 2, 20)  # Initial guesses for the parameters
        if '_pt' in givein and 'T1' in givein: 
    
            fit_function = TF1("fit_function", fit_func, 10, 120, 6)
            fit_function.SetParameters(80.4/2, 15.0/2, 2300000, 0, 2, 20)  # Initial guesses for the parameters
            fit_functionD = TF1("fit_functionD", fit_funcD, 10, 120, 6)
            fit_functionD.SetParameters(80.4/2, 15.0/2, 2300000, 0, 2, 20)  # Initial guesses for the parameters
        ###fit MC histogram
        hdata_wjets.SetStats(0)
        #hMC_wjets.Scale(1.0 / hMC_wjets.Integral()*hMC_wjets.GetBinWidth(1))
        #hdata_wjets.Scale(1.0 / hdata_wjets.Integral()*hdata_wjets.GetBinWidth(1))
        #fit_function.FixParameter(0, 80/4/2);
        #fit_functionD.FixParameter(0, 80/4/2);
        
        hMC_wjets.Fit(fit_function, "R S", era, True)
        # Extract fit results
        peak_x = fit_function.GetMaximumX()
        mean_fit = fit_function.GetParameter(0)
        mean_error = fit_function.GetParError(0)
        width_fit = fit_function.GetParameter(1)
        width_error = fit_function.GetParError(1)

        
        norm_fit = fit_function.GetParameter(2)
        
        hdata_wjets.Fit(fit_functionD, "R S",era, False)
        peak_xD = fit_functionD.GetMaximumX()
        mean_fitD = fit_functionD.GetParameter(0)
        mean_errorD = fit_functionD.GetParError(0)
        width_fitD = fit_functionD.GetParameter(1)
        width_errorD = fit_functionD.GetParError(1)

        norm_fitD = fit_functionD.GetParameter(2)

        mean_str = f"{peak_x:.2f} {mean_fit:.2f}  {mean_error:.2f}"
        sigma_str = f"{width_fit:.2f}  {width_error:.2f}"
        mean_strD = f"{peak_xD:.2f} {mean_fitD:.2f}  {mean_errorD:.2f}"
        sigma_strD = f"{width_fitD:.2f}  {width_errorD:.2f}"

        #print(f"Fitted mean (Jacobian peak position): {mean_str} GeV", channel, v)
        #print(f"Fitted width: {sigma_str} GeV", channel, v)
        print(f"============================================================Fitted mean (Jacobian peak position): {mean_str}  {sigma_str}  {mean_strD}  {sigma_strD} {channel} {v} {inn}")
        jname="jacobian_peak_fit_"+era+"_"+v+"_"+inn+"_"+channel
        #canvas.SaveAs(jname+".png")a
        fit_function.SetMarkerSize(0.5)
        fit_functionD.SetMarkerSize(0.5)
        plot_jacob = Canvas.Canvas( jname, "png", leg[0], leg[1], leg[2], leg[3])
        plot_jacob.addHisto(hdata_wjets, "E", "Data", "pe", r.kBlack, 1, 0)
        plot_jacob.addHisto(hMC_wjets, "E,SAME", "MC W+jets", "pe", r.kBlue, 1, 1)
        plot_jacob.addHisto(fit_function, "SAME", "MC Fit", "l", r.kRed, 1, 2)
        plot_jacob.addHisto(fit_functionD, "SAME", "Data Fit", "pl", r.kGreen, 1, 3)
        plot_jacob.saveCanvas(1, 1, 0, peak_x, mean_fit, mean_error, width_fit, width_error, peak_xD, mean_fitD, mean_errorD, width_fitD, width_errorD,lumi, hdata_wjets, hMC_wjets,fit_function,  varTitle, jname, option, run_str)
        
        #canvas = ROOT.TCanvas("canvas", "Transverse Mass Distribution", 800, 600)
        #CMS.SetExtraText("")
        #CMS.SetCmsText("Private work (CMS simulation)")
        #CMS.SetCmsTextFont(52)
        #CMS.SetCmsTextSize(0.75*0.76)
        #CMS.SetLumi("50")
        #canvas = CMS.cmsCanvas('', 0, 1, 0, 1, '', '', square = CMS.kSquare, extraSpace=0.01, iPos=11)
        #legend = TLegend(0.6, 0.4, 0.9, 0.6)
        #legend.AddEntry(hMC_wjets, "MC W+jets", "l")
        #legend.AddEntry(hdata_wjets, "Data - nonW+jets", "p")
        #legend.AddEntry(fit_function, "Fit", "l")
        '''
        canvas.Draw()
        hMC_wjets.SetMarkerColor(kBlue)
        hMC_wjets.SetLineColor(kBlue)
        hMC_wjets.Draw("E")
        
        hdata_wjets.Draw("SAME ")
        fit_function.Draw("same")
        legend.Draw("same")

        canvas.Update()
        '''
        #plot_j = Canvas.Canvas( "jacobian_peak_fit_"+v+".png", "png", leg[0], leg[1], leg[2], leg[3])








    for v in varbs:
        for i in range(0, len(samples)):
            s = str(samples[i])
            if 'qcd' not in s:
                histo = fIn.Get("histo_" + s + "_" + v)
                histo.SetName("histo_" + s + "_" + v)
                print('not qcd in current sample', doQCD, s, "histo_" + s + "_" + v)

            if 'qcd' in s and not doQCD:
                histo = fIn.Get("histo_" + s + "_" + v)
            if 'qcd' in s and doQCD:
                #histo = data_histC.Clone("histo_" + s + "_" + v)
                #histo.SetName("histo_" + s + "_" + v)
                histo = fIn.Get("histo_qcd_data_B_" + v)
                histo.SetTitle("QCD multijet (ABCD)")
                #histo.Scale(normQCD)
                print('===========================datadriven QCD', histo.GetName(), histo.GetSumOfWeights())
                #print('\033[91m' + "-------QCD INFO------------------------------------------------------------------" + '\033[0m')

            if 'NLO' in str(histo.GetTitle()):
                histo.SetTitle(histo.GetTitle().replace('(NLO)', ''))
            if 'dy' in s:
                histo.SetTitle("Z/#gamma+jets")

            # print
            # 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss',
            # s, histo.GetName(), histo.GetTitle()

            if kFactor != 1.:
                histo.Scale(kFactor)
            try:
                print(histo.GetName(), histo.Integral())

            except ReferenceError:
                print('something went wrong with', "histo_" + s + "_" + v)
            histo.SetName("histo_" + s + "_" + v)


            #rebin histo
            if 'openbin' in fin and doRebin:
                histo_rebin = rebinHisto(histo,bins,histo.GetName()+'_rebin')
                histo_rebin.SetTitle(histo.GetTitle())
                histo = histo_rebin

            # histo.SetFillColorAlpha(colors[s],0.5)
            histo.SetFillColor(TColor.GetColor(colors[s]))

            if 'nlo61' in s:
            #    #histo.Scale(0.1)
                lb = histo.GetBinContent(histo.GetNbinsX())
                #histo.SetBinContent(histo.GetNbinsX(), lb*0.8)

            if not mc_histo:
                mc_histo = copy.deepcopy(histo)
            else:
                # if 'qcd' not in histo.GetName() :
                mc_histo.Add(histo, 1.)

            mc_stack.Add(histo)

            print('<====================just added=====================> ', histo.GetName(), ' to the list...', histo.GetNbinsX()), histo.Integral("width")
            # mc_stack.Draw()

            if doStat:
                for sy in Othersysts:
                    for d in dirs:
                        hname=None
                        hname = "histo_" + s + "_" + v + sy + d

                        if doQCD and 'qcd' in s: 
                            hname = "histo_qcd_data_B_" + v + sy +d
                           
                        htemp = 0
                        htemp = fIn.Get(hname)

                        if 'openbin' in fin and doRebin:
                            histo_rebin = rebinHisto(htemp,bins,htemp.GetName()+'_rebin')

                            htemp = histo_rebin

                        print('working on======================================>', hname, doQCD)
                        if kFactor != 1. and htemp:
                            print ('SCALINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG', kFactor)
                            htemp.Scale(kFactor)
                        if 'nlo61' in s:
                            lb = htemp.GetBinContent(htemp.GetNbinsX())
                            #htemp.SetBinContent(htemp.GetNbinsX(), lb*0.8)
                        # htemp.Rebin(4)
                        if 'PUUp' in hname:
                            if not mc_puup:
                                mc_puup = copy.deepcopy(htemp)
                                print('should be puup integral', hname, mc_puup.Integral(), mc_puup.Integral() / mc_histo.Integral())
                            else:
                                mc_puup.Add(htemp)

                        if 'PUDown' in hname:
                            if not mc_pudown:
                                mc_pudown = copy.deepcopy(htemp)
                                print('should be pudown', htemp.GetName(), mc_pudown.Integral(), mc_pudown.Integral() / mc_histo.Integral())
                            else:
                                mc_pudown.Add(htemp)
                        if 'IDUp' in hname:
                            if not mc_idup:
                                mc_idup = copy.deepcopy(htemp)
                                print('should be idup integral', hname, mc_idup.Integral(), mc_idup.Integral() / mc_histo.Integral())
                            else:
                                mc_idup.Add(htemp)

                        if 'IDDown' in hname:
                            if not mc_iddown:
                                mc_iddown = copy.deepcopy(htemp)
                                print('should be iddown', htemp.GetName(), mc_iddown.Integral(), mc_iddown.Integral() / mc_histo.Integral())
                            else:
                                mc_iddown.Add(htemp)

            if doSyst:
                for sy in systs:
                    for d in dirs:
                        hname = "histo_" + s + "_" + v + sy + d
                        if doQCD and 'qcd' in s: 
                            hname = "histo_qcd_data_B_" + v + sy +d
                        htemp = 0
                        htemp = fIn.Get(hname)
                        print('working on======================================>', hname)
                        if 'openbin' in fin and doRebin:
                            histo_rebin = rebinHisto(htemp,bins,htemp.GetName()+'_rebin')
                            htemp = histo_rebin

                        if kFactor != 1 and htemp:
                            htemp.Scale(kFactor)
                        if 'nlo61' in s:
                            lb = htemp.GetBinContent(htemp.GetNbinsX())
                            #htemp.SetBinContent(htemp.GetNbinsX(), lb*0.8)
                        if 'JESUp' in hname:
                            if not mc_jesup:
                                mc_jesup = copy.deepcopy(htemp)
                                print('should be jesup integral', hname, mc_jesup.Integral(), mc_jesup.Integral() / mc_histo.Integral())
                            else:
                                mc_jesup.Add(htemp)

                        if 'JESDown' in hname:
                            if not mc_jesdown:
                                mc_jesdown = copy.deepcopy(htemp)
                                print('should be jesdown', htemp.GetName(), mc_jesdown.Integral(), mc_jesdown.Integral() / mc_histo.Integral())
                            else:
                                mc_jesdown.Add(htemp)

                        if 'JERUp' in hname:
                            if not mc_jerup:
                                mc_jerup = copy.deepcopy(htemp)
                                print('should be jerup integral', hname, mc_jerup.Integral(), mc_jerup.Integral() / mc_histo.Integral())
                            else:
                                mc_jerup.Add(htemp)

                        if 'JERDown' in hname:
                            if not mc_jerdown:
                                mc_jerdown = copy.deepcopy(htemp)
                                print('should be jerdown integral', hname, mc_jerdown.Integral(), mc_jerdown.Integral() / mc_histo.Integral())
                            else:
                                mc_jerdown.Add(htemp)

                        if 'UnclusteredUp' in hname:
                            if not mc_unclup:
                                mc_unclup = copy.deepcopy(htemp)
                                print('should be unclup integral', hname, mc_unclup.Integral(), mc_unclup.Integral() / mc_histo.Integral())
                            else:
                                mc_unclup.Add(htemp)
                        if 'UnclusteredDown' in hname:
                            if not mc_uncldown:
                                mc_uncldown = copy.deepcopy(htemp)
                                print('should be uncldown integral', hname, mc_uncldown.Integral())
                            else:
                                mc_uncldown.Add(htemp)
    mc_jerup = mc_histo
    mc_jerdown = mc_histo
    #mc_jesup = mc_histo
    #mc_jesdown = mc_histo
    #mc_unclup = mc_histo
    #mc_uncldown = mc_histo
    #mc_idup = mc_histo
    #mc_iddown = mc_histo
    #mc_puup = mc_histo
    #mc_pudown = mc_histo
    #mc_stack_norm = mc_stack
    last_histogram = mc_stack.GetStack().Last()
    h = last_histogram.Clone("h")  # Clone and rename the histogram

    # Normalize the histogram
    integral_with_width = h.Integral("width")  # Calculate integral considering bin widths

    h.Scale(1.0 / integral_with_width)  # Normalize by the integral

    #ahisto_norm = histo.Clone()
    #histo_norm.Scale(1./histo.Integral("width"))
    mc_stack_norm.Add(h)

    if not doSyst :
        mc_jesup = mc_histo
        mc_jesdown = mc_histo
        mc_unclup = mc_histo
        mc_uncldown = mc_histo
        mc_jerup = mc_histo
        mc_jerdown = mc_histo

    if not doStat:
        mc_puup = mc_histo
        mc_pudown = mc_histo
        mc_idup = mc_histo
        mc_iddown = mc_histo


    if'smear' not in givein.lower():

        mc_jerup = mc_histo
        mc_jerdown = mc_histo

    # print data_hist.Integral(), mc_histo.Integral(), mc_jesup.Integral(),
    # mc_jesdown.Integral()
    logcase = [0, 1]
    # logcase=[0]

    if doNormPlot:
        for ilog in logcase:
            isLog = ilog
            plot_varr = Canvas.Canvas( "test/paperv2/%s_%s%s%s%s_doQCD_%s%s_%sLog_norm" % (str( opts.varr), puname, channel, puname, str(era), str( int(doQCD)), str( opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])


            plot_varr.addStack(mc_stack_norm, "hist", 1, 1)
            data_zero = data_hist_rebin.Clone()
            data_zero.Reset()
            plot_varr.addHisto( data_zero, "E,SAME", "Data", "PL", r.kBlack, 1, 0)
            plot_varr.saveRatioGjets( 1, 1, isLog, lumi, data_hist_rebin, mc_histo, mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, mc_puup, mc_pudown, mc_idup, mc_iddown, varTitle, option + "_norm", run_str)


    for ilog in logcase:
        isLog = ilog
        plot_var = Canvas.Canvas( "test/paperv2/%s_%s%s%s%s_doQCD_%s%s_%sLog" % (str( opts.varr), puname, channel, puname, str(era), str( int(doQCD)), str( opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])
        plot_var.addStack(mc_stack, "hist", 1, 1)
        plot_var.addHisto(data_hist_rebin, "E,SAME", "Data", "PL", r.kBlack, 1, 0)

        #plot_var.saveRatioGjets(1, 1, isLog, lumi, data_hist, mc_histo, mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, mc_puup, mc_pudown, mc_idup, mc_iddown, varTitle, option, run_str)
        plot_var.saveRatioGjets(1, 1, isLog, lumi, data_hist_rebin, mc_histo, mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, mc_idup, mc_iddown, mc_idup, mc_iddown, varTitle, option, run_str)
        #plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, varTitle , option, run_str)

    print(color.blue + '********************************************DONE***************************************************' + color.end)
