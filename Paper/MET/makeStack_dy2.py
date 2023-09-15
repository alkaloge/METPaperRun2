##############################################################
##############################################################
######                                                 #######
######  |##\     /##|      |########| |##############| #######
######  |###\   /###|      |##|             |##|       #######
######  |####\_/####|      |##|             |##|       #######
######  |##|\###/|##|      |######|         |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |##|             |##|       #######
######  |##|     |##|      |########|       |##|       #######
######                                                 #######             
##############################################################
##############################################################

import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue
import math, sys, optparse, array, time, copy

import include.helper     as helper
import include.Region     as Region
import include.Canvas     as Canvas
import include.CutManager as CutManager
import include.Sample     as Sample
import include.Rounder    as Rounder        
import numpy as np

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
    channel='gjets'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    
    print 'will read Datasets from plotS.root'
    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':35.93, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.72, '2016postVFP':16.15,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
    lumi = lumis[era]
    #lumi=1
    yields={}
    print 'Going to load DATA and MC trees...'

    gROOT.ProcessLine('.L include/tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle()
    color = helper.color

    lumi_str =channel+ 'lumi'+str(lumi)

    #plotS_2018_data_njetsgeq0_hitslt2_METWmass_MuMu.root
    isLog = 1
    fin = "plotS_{0:s}_njetsgt0_nbtagl_10bins_hitslt1_{1:s}_{2:s}.root".format(str(opts.Year), str(opts.varr), str(opts.Channel))
    #plotS_2018_njetsgeq0_nbtagl_10bins_hitslt1_METCorGood_T1_pt_Gjets.root
    fin ='{0:s}'.format(str(opts.FileIn))
    fIn = TFile.Open(fin, 'read')
    print 'fIn is.......', fIn.GetName()
    fIn.ls()
    tmp_histo=0;mc_histo = 0; histo_err = 0; mc_up = 0; mc_down = 0; mc_jerup=0; mc_jerdown=0;mc_jesup = 0; mc_jesdown = 0; mc_unclup = 0; mc_uncldown = 0; mc_stack = r.THStack()
    #histo_dy_MET_T1_pt

    samples=['tx', 'qcd', 'ewknlo', 'ew', 'gjets' ]
    samples=['ewknlo', 'tx', 'qcd','ew', 'gjets' ]
    #samples=['tx', 'qcd', 'ew', 'gjets' ]
    givein ='{0:s}'.format(str(opts.varr))

    varbs=[]
    if 'all' not in givein : 
        varbs.append(givein)
    print 'will do the following', varbs, fIn.GetName()
    systs =['JES', 'Unclustered', 'JER']
    dirs = ['Up', 'Down']
    colors = {'gjets':kYellow, 'dynlo':kYellow+1, 'qcd':kMagenta, 'tx':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan}
    channel=''
    doQCD = int(opts.DoQCD)
    doSyst = True
    if 'boson_pt' in varbs : doSyst = False
    #doSyst = False
    doScaleToData = False
    channel='gjets'
    era = str(opts.Year)
    eras = str(opts.Year)
    run=era
    leg = [0.65, 0.6, 0.81, 0.9]
    puname=''
    data_hist = fIn.Get('histo_data')
    
    #data_hist.Scale(0.5)
    varTitle    = 'p_{T}^{miss} [GeV]'
    if 'boson_pt' in givein.lower() : varTitle    = 'q_{T} [GeV]'
    if 'boson_phi' in givein : varTitle    = 'q_{#phi}'
    if 'PuppiMETmTmass' in givein : varTitle    = 'm_{T} [GeV]'
    if 'njets' in givein : varTitle    = 'njets'
    if 'DphiWMET' in givein : varTitle    = '#Delta#Phi(W,p_{T}^{miss})'
    if 'DphilMET' in givein : varTitle    = '#Delta#Phi(#mu,p_{T}^{miss})'
    if 'PuppiMET' in givein : varTitle    = 'p_{T}^{miss}'
    if 'wtmass' in givein.lower() : varTitle    = 'W_{T} [GeV]'
    if 'wmass' in givein.lower() : varTitle    = 'W [GeV]'
    if 'pt_1' in givein : varTitle    = 'p_{T}(#mu)'
    if 'eta_1' in givein : varTitle    = '#eta(#mu)'
    if 'phi' in givein : varTitle    = '#phi'
    allh1 =0
    nscale = 1.


    kFactor=1.
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
	
	# Calculate the contribution of the current sample
	contribution = histo.Integral() / hMC_total.Integral() * 100
	contribution_dict[s] = contribution

	# Calculate the data/MC difference
	data_mc_difference = histo.Integral() - hMC_total.Integral()

    # Print the contribution table
    print "Contribution Table:"
    print "------------------------------"

    # Calculate the maximum length of process names for alignment
    max_length = max(len(str(sample)) for sample in samples)

    # Print the process names as columns
    for sample in samples:
	process_name = str(sample)
	print process_name.ljust(max_length + 5),
    print "Total MC\t\tData\tData/MC"

    # Print the contribution values below each process
    for sample in samples:
	contribution = contribution_dict.get(str(sample), 0)
        print "{:.3f}".format(contribution).ljust(max_length + 5),

    # Print the total MC, data, and data/MC ratio
    # Print the total MC, data, and data/MC ratio with two significant digits
    print "{:.3f}\t".format(hMC_total.Integral()).ljust(max_length + 5),
    print "{:.3f}\t".format(data_hist.Integral()).ljust(max_length + 5),
    print "{:.3f}\t".format(data_hist.Integral() / hMC_total.Integral())



    print "------------------------------"


            
    kFactor = float(data_hist.GetSumOfWeights()/hMC_total.GetSumOfWeights())
    if 'noscale' in str(opts.ExtraTag).lower() :  kFactor=1.
    for v in varbs :
        #for s in samples :
        for i in range(0, len(samples)):
            s = str(samples[i])
            histo = fIn.Get("histo_"+s+"_"+v)
            #histo.Rebin(4)
            if kFactor !=1. : histo.Scale(kFactor)
            try : print histo.GetName(), histo.Integral()

            except ReferenceError : print 'something went wrong with', "histo_"+s+"_"+v
            histo.SetFillColorAlpha(colors[s],0.5)
            #allh1.Add(histo)
            #    print 'SCaling MC to Data........................'
            #    allh1.Add(histo)
            if not mc_histo: mc_histo = copy.deepcopy(histo) 
            else : mc_histo.Add(histo, 1.)
            mc_stack.Add(histo)
            mc_stack.Draw()
            #if 'Cor' in v : v = v.replace("METCor","MET")
            if doSyst : 
		for sy in systs : 
		    for d in dirs :
			hname = "histo_"+s+"_"+v+sy+d
			htemp=0
			htemp = fIn.Get(hname)   
                        print 'working on======================================>', hname
                        if kFactor !=1. : htemp.Scale(kFactor)
                        #htemp.Rebin(4)
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
    #print data_hist.Integral(), mc_histo.Integral(), mc_jesup.Integral(), mc_jesdown.Integral()
    option='met'
    run_str =str(lumi)
    logcase=[0,1]
    nscale=1
    nscale= ( data_hist.GetSumOfWeights()/mc_histo.GetSumOfWeights())
    print 'some testttttttttt', mc_histo.GetName(), mc_histo.GetSumOfWeights(), mc_histo.GetTitle(), data_hist.GetSumOfWeights(), nscale
    
    if doScaleToData :
	mc_histo.Scale( nscale)
	mc_jesup.Scale( nscale)
	mc_jesdown.Scale( nscale)
	mc_unclup.Scale( nscale)
	mc_uncldown.Scale( nscale)
    for ilog in logcase :
        isLog = ilog
	plot_var = Canvas.Canvas("test/paperv2/%s_%s%s%s%s_doQCD_%s%s_%sLog"%(str(opts.varr),puname, channel, puname ,str(era), str(int(doQCD)), str(opts.ExtraTag), str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])               
	plot_var.addStack(mc_stack  , "hist" , 1, 1)
	plot_var.addHisto(data_hist, "E,SAME"   , "Data"  , "PL", r.kBlack , 1, 0)

	plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, varTitle , option, run_str)


    print color.blue+'********************************************DONE***************************************************'+color.end
