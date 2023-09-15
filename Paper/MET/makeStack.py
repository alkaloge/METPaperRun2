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
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue, kOrange, kTeal
import math, sys, optparse, array, time, copy

import include.helper     as helper
import include.Region     as Region
import include.Canvas     as Canvas
import include.CutManager as CutManager
import include.Sample     as Sample
import include.Rounder    as Rounder        


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
    parser.add_option('-f', '--file', action='store', type=str, dest='fileIn', default='test.root', help='input file')
    (opts, args) = parser.parse_args()
    doDY = True
    doNPV = True
    doee = True
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : doee = False
    if 'el' in str(opts.Channel.lower()) : doee = True
    if doee :   channel = 'ElEl'
    else :   channel = 'MuMu'
    era = str(opts.Year)
    eras = str(opts.Year)
    ee = era
    
    print 'will read Datasets from plotS.root'

    lumis={'2016':35.93, '2017':41.48, '2018':59.83}
    lumis={'2016':35.93, '2017':41.48, '2018':59.83, '2016BpreVFP':5.825, '2016CpreVFP':2.62, '2016DpreVFP':4.286, '2016EpreVFP':4.0659, '2016FpreVFP':2.865, '2016F':0.584, '2016G':7.653, '2016H':8.74, '2016preVFP':19.351, '2016postVFP':16.9777,  '2017B':4.80, '2017C':9.57, '2017D':4.25, '2017E':9.315, '2017F':13.54, 'dry':10, '2018A':14.03, '2018B':7.07, '2018C':6.895, '2018D':31.84}
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
    inn = str(opts.ExtraTag).lower()
    innOr = str(opts.ExtraTag)
    #fin = "plotS_{0:s}_njetsgt0_etaveto_hitslt2_{1:s}_{2:s}.root".format(str(opts.Year), str(opts.varr), str(opts.Channel))
    #fin = "plotS_{0:s}_njetsgt0_hitslt2_{1:s}_{2:s}.root".format(str(opts.Year), str(opts.varr), str(opts.Channel))
    #fin = "plotS_{0:s}_{1:s}_{2:s}_{3:s}.root".format(str(opts.Year), innOr, str(opts.varr), str(opts.Channel))
    #fin = "plotS_{0:s}_{1:s}_{2:s}.root".format(str(opts.Year), str(opts.varr), str(opts.Channel))
    fin = str(opts.fileIn)
    #fin = "plotS_in.root".format(str(opts.Year), str(opts.varr), str(opts.Channel))
    if 'njetsgeq0' in inn :  fin = fin.replace("njetsgeq0","njetsgt0")
    if 'hitslt1' in inn  : fin = fin.replace("hitslt2","hitslt1")
    fIn = TFile.Open(fin, 'read')
    print fin
    print 'fIn is.......', fin, innOr
    #fIn.ls()
    tmp_histo=0;mc_histo = 0; histo_err = 0; mc_up = 0; mc_down = 0; mc_jerup=0; mc_jerdown=0;mc_jesup = 0; mc_jesdown = 0; mc_unclup = 0; mc_uncldown = 0; mc_stack = r.THStack()
    #histo_dy_MET_T1_pt
    nscale = 1.
    samples=['dy', 'qcd', 'top', 'ew', 'ewk']
    #ewk ewknlo61 ewkincl
    givein ='{0:s}'.format(str(opts.varr))
    if 'nlo' in inn :
        if '61' not in inn:  samples=['dy', 'qcd', 'top', 'ew', 'ewknlo']
        if '61' in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewknlo61']

    if 'incl' in inn and 'nlo' not in inn and 'wnjets' not in inn:
        if '61' not in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewkincl']
        if '61' in inn:   samples=['dy', 'qcd', 'top', 'ew', 'ewkincl61']
    if 'qcdpt' in inn : 
        samples[1]='qcdpt'
        inn = inn.replace('QCDHT', 'QCDPt')
        
    

    print 'LETS SEE THE SAMPLES!!!!!!!!!!!1', samples
    #if '67' in str(opts.ExtraTag).lower() : nscale = 67350.7
    #if '61' in str(opts.ExtraTag).lower() : nscale = float(61526.7/67350.7)
    #if '61' in str(opts.ExtraTag).lower() : 
    #    nscale = float(0.9135272536142905)
    #    print 'XOXOXOXOXOXOXOXOXOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXXXXXXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXXXXXXXXXx', str(opts.ExtraTag), nscale
    varbs=[]
    varbs.append(givein)
    print 'will do the following', varbs, fIn.GetName()
    systs =['JES', 'Unclustered']
    dirs = ['Up', 'Down']
    colors = {'dy':kYellow, 'qcd':kMagenta, 'qcdpt':kMagenta, 'top':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan+1, 'ewknlo61':kCyan+1, 'ewkincl':kTeal, 'ewkincl61':kTeal-4}
    channel=''
    doQCD = int(opts.DoQCD)
    doSyst = True
    if 'raw' in givein or 'Raw'in givein: doSyst = False
    if 'mm' in str(opts.Channel.lower()) or 'mu' in str(opts.Channel.lower()) : channel = 'MuMu'
    else  : channel = 'ElEl'
    era = str(opts.Year)
    eras = str(opts.Year)
    run=era
    kFactor=1
    if '2016' in era : kFactor=0.9
    if '2017' in era : kFactor=0.95
    if '2018' in era : kFactor=0.9
    reBin=1
    leg = [0.65, 0.6, 0.81, 0.9]
    puname=''
    data_hist = fIn.Get('histo_data')
    #data_hist.Sum2()
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
    #if 'phi' in givein : 
    #if reBin > 1 : data_hist.Rebin(reBin)
	#data_hist.SetMaximum(data_hist.GetMaximum()*100)
    #mc_stack=0;histo=0;
    #data_hist.Rebin(4)
    # samples=['dy', 'qcd', 'top', 'ew', 'ewkincl61']
    #purity={"string":[], "{0:s}".format(samples[0]):[], "{1:s}".format(samples[0]):[], "{2:s}".format(samples[0]):[], "{3:s}".format(samples[0]):[], "{4:s}".format(samples[0]):[]  }
    allh1 =0
    purity={}
    norm_purity={}
    purity["selection"]="{0:s}".format(inn)
    norm_purity["selection"]="{0:s}".format(inn)
    for v in varbs :
        #for s in samples :
        for i in range(0, len(samples)):
            s = str(samples[i])
            histo = fIn.Get("histo_"+s+"_"+v)
            try : 
                sh = histo.GetSumOfWeights()
                if histo.GetSumOfWeights()<0.0001 : histo.SetBinContent(1,0.0001)
                purity["{0:s}".format(samples[i])] = float(histo.GetSumOfWeights())
            except AttributeError : continue
            if 'nlo61' in s : 
                histo.Scale(kFactor) 
                histo.SetTitle ( histo.GetTitle().replace("-61", "") )  #histo.GetTitleSetTitle("W + jets (NLO)")
                histo.Sumw2()
            
                print '------------------------------------------------------------> SCALINGGGGG', histo.GetName()
            #if reBin > 1 :histo.Rebin(reBin)
            #if 'ewk' in s and 'nlo' not in s and 'incl' in s and nscale != 1: 
            #if 'ewk' in s and nscale != 1: 
            #    print 'found EWKKKKKKKKKKKKKKKKKKKKKKK', s, histo.GetName(), histo.GetTitle(), float(nscale), 'WILLLLLL SCALEEEE', 

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
                print 'will DO SYSTEMATICS AS WELL-----------------------------------------------------------------------------'
		for sy in systs : 
		    for d in dirs :
			hname = "histo_"+s+"_"+v+sy+d
			htemp=0
			htemp = fIn.Get(hname)   
                        #if reBin > 1 :htemp.Rebin(reBin)
                              
			if 'nlo61' in  s: 
			    htemp.Scale(kFactor) 
			    htemp.Sumw2()
                            print '------------------------------------------------------------> SCALINGGGGG', htemp.GetName()

			#print 'will get', hname, htemp.Integral(), s, v, sy, d
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

        print purity
        sum_values=0
        norm_purity = purity
	for value in purity.values():
	    if isinstance(value, (int, float)):
		sum_values += value
    
	for key in norm_purity.keys():
	    if 'selection' not in str(key) : norm_purity[key] /=sum_values
                
	#sum_values= sum( [purity[key] for key in range(1, 6)]) #in samples[0] + samples['qcd']  + samples['top'] + samples['ew'], +samples['ewk']
        #sum_values = sum([purity[key] for key in samples])
	#for key in samples : 
	#    norm_purity['{0:s}'.format(samples[key])] = purity[int('{0:s}'.format(purity[key]))]/sum_values
	print color.red+ '********************  sums '+color.end,  sum_values , purity, ' norm purity',  norm_purity
    if not doSyst:
	mc_jesup = mc_histo
	mc_jesdown = mc_histo
	mc_unclup = mc_histo
	mc_uncldown = mc_histo
    mc_jerup = mc_histo
    mc_jerdown = mc_histo
    print data_hist.Integral(), mc_histo.Integral(), mc_jesup.Integral(), mc_jesdown.Integral()
    option='met'
    run_str =str(lumi)
    logcase=[0,1]
    #nscale= ( data_hist.GetSumOfWeights()/mc_histo.GetSumOfWeights())
    print 'some testttttttttt', mc_histo.GetName(), mc_histo.GetSumOfWeights(), mc_histo.GetTitle(), data_hist.GetSumOfWeights()
    #mc_stack.Scale( nscale)
    #mc_jesup.Scale( nscale)
    #mc_jesdown.Scale( nscale)
    #mc_jesup.Scale( data_hist.GetSumOfWeights()/hjesUp.GetSumOfWeights())
    #  hjesDown.Scale( data_hist.GetSumOfWeights()/hjesDown.GetSumOfWeights())
    #  hunclUp.Scale( data_hist.GetSumOfWeights()/hunclUp.GetSumOfWeights())
    #  hunclDown.Scale( data_hist.GetSumOfWeights()/hunclDown.GetSumOfWeights())
    for ilog in logcase :
        isLog = ilog
	plot_var = Canvas.Canvas("test/paperPaper/%s_%s%s%s%s_doQCD_%s%s_%sLog"%(str(opts.varr),puname, channel, puname ,str(era), str(int(doQCD)), innOr, str(isLog)), "png,root,pdf,C", leg[0], leg[1], leg[2], leg[3])               
	plot_var.addStack(mc_stack  , "hist" , 1, 1)
	plot_var.addHisto(data_hist, "E,SAME"   , "Data"  , "PL", r.kBlack , 1, 0)

	plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo,  mc_jerup, mc_jerdown, mc_jesup, mc_jesdown, mc_unclup, mc_uncldown, varTitle , option, run_str)


    print color.blue+'********************************************DONE***************************************************'+color.end
