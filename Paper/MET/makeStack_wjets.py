#!/usr/bin/env python

import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue, kTeal, kOrange
import math, sys, optparse, array, time, copy

import include.helper     as helper
#import include.Region     as Region
import include.Canvas     as Canvas
#import include.CutManager as CutManager
import include.Sample     as Sample
#import include.Rounder    as Rounder        


era='2017'
channel=''
if __name__ == "__main__":

    parser = optparse.OptionParser(usage="usage: %prog [opts] FilenameWithSamples", version="%prog 1.0")
    parser.add_option('-s', '--samples', action='store', type=str, dest='sampleFile', default='samples_2017.dat', help='the samples file. default \'samples.dat\'')
    parser.add_option('-y', '--year', action='store', type=str, dest='Year', default='2017', help='choose from 2016, 2017, 2018 \'samples.dat\'')
    parser.add_option('-v', '--variable', action='store', type=str, dest='varr', default='MET_T1_pt', help='variable to plot ')
    parser.add_option('-q', '--doqcd', action='store', type=str, dest='DoQCD', default=0, help='do data-driven QCD')
    parser.add_option('-e', '--extra', action='store', type=str, dest='ExtraTag', default='', help='extra Tag')
    parser.add_option('-c', '--channel', action='store', type=str, dest='Channel', default='', help='channel')
    parser.add_option('-l', '--local', action='store', type=str, dest='Local', default='', help='running local or on condor')
    parser.add_option('-f', '--file', action='store', type=str, dest='FileIn', default='', help='input file')
    (opts, args) = parser.parse_args()
    doDY = True
    doNPV = True
    doee = True
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : doee = False
    if 'el' in str(opts.Channel.lower()) : doee = True
    if doee :   channel = 'ElNu'
    else :   channel = 'MuNu'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    
    print 'will read Datasets from plotS.root'



    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':35.93, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.72, '2016postVFP':16.15,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    lumi = lumis[era]
    yields={}
    print 'Going to load DATA and MC trees...'

    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle()
    color = helper.color

    lumi_str =channel+ 'lumi'+str(lumi)

    #plotS_2018_data_njetsgeq0_hitslt2_METWmass_MuMu.root
    isLog = 1
    SR = "isolt0p15_mtmassgt80"
    B = "isolt0p15_mtmasslt80"
    D = "isogt0p15_mtmasslt80"
    C = "isogt0p15_mtmassgt80"

    fin ='{0:s}'.format(str(opts.FileIn))
    finB = fin.replace(SR, B)
    finC = fin.replace(SR, C)
    finD = fin.replace(SR, D)

    fIn = TFile.Open(fin, 'read')
    fInB = fInC = fInD = None
    doQCD = int(opts.DoQCD)
    #doQCD = True
    if doQCD: 
        print 'filenames in sideband', finB, finC, finD
	fInB = TFile.Open(finB, 'read')
	fInC = TFile.Open(finC, 'read')
	fInD = TFile.Open(finD, 'read')

    #fIn = TFile.Open('plotS.root'.format(str(opts.Year), str(opts.varr), str(opts.Channel)), 'read')
    print 'fIn is.......', fIn.GetName()
    fIn.ls()
    tmp_histo=0;mc_histo = 0; histo_err = 0; mc_up = 0; mc_down = 0; mc_puup=0; mc_pudown=0; mc_idup=0; mc_iddown=0;mc_jerup=0; mc_jerdown=0;mc_jesup = 0; mc_jesdown = 0; mc_unclup = 0; mc_uncldown = 0; mc_stack = r.THStack()
    #histo_dy_MET_T1_pt

    samples=['dy', 'qcd', 'top', 'ew', 'ewk']
    #ewk ewknlo61 ewkincl
    givein ='{0:s}'.format(str(opts.varr))
    inn = str(opts.ExtraTag).lower()
    if 'nlo' in inn :
        if '61' not in inn:  samples=['dy', 'qcd', 'top', 'ew', 'ewknlo']
        if '61' in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewknlo61']

    if 'winclwnjets' in inn : samples=['dy', 'qcd', 'top', 'ew', 'ewk']

    if 'incl' in inn and 'nlo' not in inn and 'wnjets' not in inn:
        if '61' not in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewkincl']
        if '61' in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewkincl61']
    
    if 'winclht' in inn :
        samples=['dy', 'qcd', 'top', 'ew', 'ewkht']

    if 'qcdpt' in inn : 
        samples[1]='qcdpt'
        inn = inn.replace('QCDHT', 'QCDPt')

    #varbs = ['MET_T1_pt', 'PuppiMET_pt', 'boson_pt']
    #if 'all' not in givein : 
    varbs=[]
    varbs.append(givein)
    print 'will do the following', varbs, fIn.GetName()
    systs =['JES', 'Unclustered', 'JER']
    Othersysts =['ID', 'PU']

    dirs = ['Up', 'Down']
    colors = {'dy':kYellow, 'dynlo':kYellow+1, 'qcd':kMagenta, 'top':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan+1}
    colors = {'dy':kYellow, 'qcd':kMagenta, 'qcdpt':kMagenta, 'top':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan+1, 'ewknlo61':kCyan+1, 'ewkincl':kTeal, 'ewkincl61':kTeal-4, 'ewkht':kCyan+1}
    channel=''
    doStat = True
    #doStat = False
    doStat = True
    doSyst = True
    #if 'mll' in givein or 'Raw' in givein or 'boson_pt' in givein or 'boson_phi' in givein or '_significance' in givein: doSyst = False
    if 'mll' in givein or 'Raw' in givein or '_significance' in givein or 'njets_' in givein: doSyst = False
    #if 'boson_pt' in givein or 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein: doSyst = False
    #if 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein or 'boson_pt' in givein: doSyst = False
    if 'Raw' in givein or 'mll' in givein or 'iso_1' in givein or 'Photon_' in givein : doSyst = False
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : channel = 'MuNu'
    else  : channel = 'ElNu'
    era = str(opts.Year)
    eras = str(opts.Year)
    run=era
    print 'lets see what syst you run doSyst', doSyst, 'doStat', doStat
    leg = [0.65, 0.6, 0.81, 0.9]
    puname=''
    data_hist = fIn.Get('histo_data')

    #data_hist.Sum2()
    varTitle    = 'p_{T}^{miss} [GeV]'
    if 'boson_pt' in givein: varTitle    = 'q_{T} [GeV]'
    if 'boson_phi' in givein : varTitle    = 'q_{#phi}'
    if 'PuppiMETmTmass' in givein : varTitle    = 'm_{T} [GeV]'
    if 'njets' in givein : varTitle    = 'njets'
    if 'DphiWMET' in givein : varTitle    = '#Delta#Phi(W,p_{T}^{miss})'
    if 'DphilMET' in givein : varTitle    = '#Delta#Phi(#mu,p_{T}^{miss})'
    if 'PuppiMET' in givein : varTitle    = 'p_{T}^{miss} [GeV]'
    if 'wtmass' in givein.lower() : varTitle    = 'W_{T} [GeV]'
    if 'wmass' in givein.lower() : varTitle    = 'W [GeV]'
    if 'pt_1' in givein : varTitle    = 'p_{T}(#mu)'
    if 'eta_1' in givein : varTitle    = '#eta(#mu)'
    if 'phi' in givein : varTitle    = '#phi'
    if 'mll' in givein : varTitle    = 'M(ll) [GeV]'
    if 'u_perp' in givein : varTitle    = 'u_{#perp} [GeV]'
    if 'u_par' in givein : varTitle    = 'u_{#parallel}  [GeV]'
    if 'u_par_boson' in givein or "u_parboson" in givein : varTitle    = 'u_{#parallel} + q_{T} [GeV]'
    if 'METCorGoodboson_pt' in givein: varTitle    = 'W q_{T} [GeV]'
    if 'METCorGoodboson_phi' in givein: varTitle    = 'W #phi '
    if 'METCorGoodboson_transm' in givein: varTitle    = '#W_T mass [GeV]'
    if 'METCorGoodboson_m' in givein: varTitle    = 'W mass [GeV]'
    
    kFactor=1.
    #if 'phi' in givein : 
    hMC_total = data_hist.Clone("hMC_total")
    hMC_total.Reset()


    contribution_dict = {}

    for v in varbs :
        #for s in samples :
        for i in range(0, len(samples)):
            s = str(samples[i])
            histo = fIn.Get("histo_"+s+"_"+v)
            hMC_total.Add(histo)

    for i in range(len(samples)):
	s = str(samples[i])
	histo = fIn.Get("histo_" + s + "_" + v)
	if '61' in s : 
	    #histo.Scale(kFactor) 
	    histo.SetTitle ( histo.GetTitle().replace("-61", "") )  #histo.GetTitleSetTitle("W + jets (NLO)")
	    histo.Sumw2()
	
	# Calculate the contribution of the current sample
	contribution = histo.Integral() / hMC_total.Integral() * 100
	contribution_dict[s] = contribution

	# Calculate the data/MC difference
	data_mc_difference = histo.Integral() - hMC_total.Integral()

    # Print the contribution table
    print "Contribution Table:"

    # Calculate the maximum length of process names for alignment
    max_length = max(len(str(sample)) for sample in samples)

    print '\033[91m' + "-------------------------------------------------------------------------" +  '\033[0m'
    # Print the process names as columns
    for sample in samples:
	process_name = str(sample)
	print process_name.ljust(max_length + 5),
    print "Total MC\t\tData\tData/MC"

    # Print the contribution values below each process
    for sample in samples:
	contribution = contribution_dict.get(str(sample), 0)
        print "{:.2f}".format(contribution).ljust(max_length + 5),

    # Print the total MC, data, and data/MC ratio
    # Print the total MC, data, and data/MC ratio with two significant digits
    print "{:.2f}\t".format(hMC_total.Integral()).ljust(max_length + 5),
    print "{:.2f}\t".format(data_hist.Integral()).ljust(max_length + 5),
    print "{:.2f}\t".format(data_hist.Integral() / hMC_total.Integral())



    print '\033[91m' + "-------------------------------------------------------------------------" +  '\033[0m'
    print '\033[91m' + "-------------------------------------------------------------------------" +  '\033[0m'


    kFactor = float(data_hist.GetSumOfWeights()/hMC_total.GetSumOfWeights())
    if 'noscale' in str(opts.ExtraTag).lower() :  kFactor=1.


    normQCD = 1.
    if doQCD : 
	for v in varbs :
            data_histB = data_histC = data_histD = None
	    histoB = histoC = histoD = None
	    data_histB = fInB.Get('histo_data')
	    data_histC = fInC.Get('histo_data')
	    data_histD = fInD.Get('histo_data')
            print 'data in sideband', data_histB.GetSumOfWeights(), data_histD.GetSumOfWeights(), 'shape', data_histC.GetSumOfWeights()
	    #for s in samples :
	    for i in range(0, len(samples)):
		s = str(samples[i])
		histo = fIn.Get("histo_"+s+"_"+v)
		if 'qcd' not in s:  #get all histograms in the SB regions but not QCD --> this is what you are going to calculate 
		    histoB = fInB.Get("histo_"+s+"_"+v)
                    data_histB.Add(histoB, -1)
		    histoC = fInC.Get("histo_"+s+"_"+v)
                    data_histC.Add(histoC, -1)
		    histoD = fInD.Get("histo_"+s+"_"+v)
                    data_histD.Add(histoD, -1)

            normQCD = data_histB.GetSumOfWeights()/data_histD.GetSumOfWeights()
            print 'some infor for QCD data driven', data_histC.GetSumOfWeights(), normQCD, data_histB.Integral()/data_histD.Integral()
    #exit()

    for v in varbs :
        #for s in samples :
        for i in range(0, len(samples)):
            s = str(samples[i])
            if 'qcd' not in s : 
                histo = fIn.Get("histo_"+s+"_"+v)
                histo.SetName("histo_"+s+"_"+v)
                print 'not qcd in current sample', doQCD, s, "histo_"+s+"_"+v

            if 'qcd' in s and not doQCD: histo = fIn.Get("histo_"+s+"_"+v)
            if 'qcd' in s and doQCD: 
                histo = data_histC.Clone("histo_"+s+"_"+v)
                histo.SetName("histo_"+s+"_"+v)
                histo.SetTitle("QCD multijet (ABCD)")
                histo.Scale(normQCD)
                print 'SHOULD REPLACE QCD with DATA ESTIMATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
                print 'datadriven QCD', histo.GetName(), histo.GetSumOfWeights()

            if kFactor !=1. : histo.Scale(kFactor)
            try : print histo.GetName(), histo.Integral()

            except ReferenceError : print 'something went wrong with', "histo_"+s+"_"+v
            histo.SetName("histo_"+s+"_"+v)
            histo.SetFillColorAlpha(colors[s],0.5)

            if not mc_histo: 
                mc_histo = copy.deepcopy(histo) 
            else : 
                #if 'qcd' not in histo.GetName() : 
		mc_histo.Add(histo, 1.)

            mc_stack.Add(histo)
	    print '<====================just added=====================> ', histo.GetName(), ' to the list...'
            #mc_stack.Draw()

            if doStat : 
		for sy in Othersysts : 
		    for d in dirs :
			hname = "histo_"+s+"_"+v+sy+d
			htemp=0
			htemp = fIn.Get(hname)   
                        print 'working on======================================>', hname
                        if kFactor !=1. : htemp.Scale(kFactor)
                        #htemp.Rebin(4)
			if 'PUUp' in hname : 
			    if not mc_puup : 
				mc_puup = copy.deepcopy(htemp)
				print 'should be puup integral', hname, mc_puup.Integral(), mc_puup.Integral()/mc_histo.Integral()
			    else : mc_puup.Add(htemp)

			if 'PUDown' in hname : 
			    if not mc_pudown : 
				mc_pudown = copy.deepcopy(htemp)
				print 'should be pudown', htemp.GetName(), mc_pudown.Integral(), mc_pudown.Integral()/mc_histo.Integral()
			    else : 
				mc_pudown.Add(htemp)
			if 'IDUp' in hname : 
			    if not mc_idup : 
				mc_idup = copy.deepcopy(htemp)
				print 'should be idup integral', hname, mc_idup.Integral(), mc_idup.Integral()/mc_histo.Integral()
			    else : mc_idup.Add(htemp)

			if 'IDDown' in hname : 
			    if not mc_iddown : 
				mc_iddown = copy.deepcopy(htemp)
				print 'should be iddown', htemp.GetName(), mc_iddown.Integral(), mc_iddown.Integral()/mc_histo.Integral()
			    else : 
				mc_iddown.Add(htemp)



            if doSyst : 
		for sy in systs : 
		    for d in dirs :
			hname = "histo_"+s+"_"+v+sy+d
			htemp=0
			htemp = fIn.Get(hname)   
                        print 'working on======================================>', hname
                        if kFactor !=1. : htemp.Scale(kFactor)
			if 'JESUp' in hname : 
			    if not mc_jesup : 
				mc_jesup = copy.deepcopy(htemp)
				print 'should be jesup integral', hname, mc_jesup.Integral(), mc_jesup.Integral()/mc_histo.Integral()
			    else : mc_jesup.Add(htemp)

			if 'JESDown' in hname : 
			    if not mc_jesdown : 
				mc_jesdown = copy.deepcopy(htemp)
				print 'should be jesdown', htemp.GetName(), mc_jesdown.Integral(), mc_jesdown.Integral()/mc_histo.Integral()
			    else : 
				mc_jesdown.Add(htemp)

			if 'JERUp' in hname : 
			    if not mc_jerup : 
				mc_jerup = copy.deepcopy(htemp)
				print 'should be jerup integral', hname, mc_jerup.Integral(), mc_jerup.Integral()/mc_histo.Integral()
			    else : mc_jerup.Add(htemp)

			if 'JERDown' in hname : 
			    if not mc_jerdown : 
				mc_jerdown = copy.deepcopy(htemp)
				print 'should be jerdown integral', hname, mc_jerdown.Integral(), mc_jerdown.Integral()/mc_histo.Integral()
			    else : 
				mc_jerdown.Add(htemp)

			if 'UnclusteredUp' in hname : 
			    if not mc_unclup : 
				mc_unclup = copy.deepcopy(htemp)
				print 'should be unclup integral', hname, mc_unclup.Integral(),  mc_unclup.Integral()/ mc_histo.Integral()
			    else : mc_unclup.Add(htemp)
			if 'UnclusteredDown' in hname : 
			    if not mc_uncldown : 
				mc_uncldown = copy.deepcopy(htemp)
				print 'should be uncldown integral', hname, mc_uncldown.Integral()
			    else : mc_uncldown.Add(htemp)
    if not doSyst:
	mc_jesup = mc_histo
	mc_jesdown = mc_histo
	mc_unclup = mc_histo
	mc_uncldown = mc_histo
        mc_jerup = mc_histo
        mc_jerdown = mc_histo
        mc_puup = mc_histo
        mc_pudown = mc_histo
        mc_idup = mc_histo
        mc_iddown = mc_histo
    #print data_hist.Integral(), mc_histo.Integral(), mc_jesup.Integral(), mc_jesdown.Integral()
    option=str(opts.varr)
    run_str =str(lumi)
    logcase=[0, 1]
    #logcase=[0]
    
    for ilog in logcase :
        isLog = ilog
	plot_var = Canvas.Canvas("test/paperv2/%s_%s%s%s%s_doQCD_%s%s_%sLog"%(str(opts.varr),puname, channel, puname ,str(era), str(int(doQCD)), str(opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])               

	plot_var.addStack(mc_stack  , "hist" , 1, 1)
	plot_var.addHisto(data_hist, "E,SAME"   , "Data"  , "PL", r.kBlack , 1, 0)

	plot_var.saveRatioGjets(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, mc_puup, mc_pudown, mc_idup, mc_iddown, varTitle , option, run_str)
	#plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, varTitle , option, run_str)


    print color.blue+'********************************************DONE***************************************************'+color.end

