from ROOT import TCanvas, TLegend, TPad, TLine, TGraphAsymmErrors, TLatex, TH1F, THStack, TGraphErrors, TLine, TPaveStats, TGraph, TArrow, TFile, gPad
import ROOT as r
import os
import copy
import math
import array


class Canvas:
   'Common base class for all Samples'

   def __init__(self, name, format, x1, y1, x2, y2):
      self.name = name
      print('all CANVAS ======================>', name, format, x1, y1, x2, y2)
      self.format = format
      self.plotNames = [name + "." + i for i in format.split(',')]
      if ":" in self.plotNames: plotNAmes = plotNames.replace(":", "_vs_")
      self.myCanvas = TCanvas(name, name)
      self.ToDraw = []
      self.orderForLegend = []
      self.histos = []
      self.lines = []
      self.arrows = []
      self.latexs = []
      self.extra = []
      self.var = []
      extraa = ''
      if 'METCorGood' in name: self.var = 'PF T1 p_{T}^{miss}'
      if 'MET_p' in name: self.var = 'PF p_{T}^{miss}'
      if 'MET_T1' in name: self.var = 'PF T1 p_{T}^{miss}'
      if 'PuppiMET_p' in name: self.var = 'PUPPI p_{T}^{miss}'

      if 'Smear' in name: self.var = 'PF T1 Smear p_{T}^{miss}'
      if 'PuppiMETCor' in name: self.var = 'PUPPI T1 p_{T}^{miss}'

      if 'Raw' in name and 'MET' in self.var: self.var = 'Raw ' + str(self.var)
      if 'Raw' in name:
          if 'puppi' in name.lower(): self.var = 'Raw PUPPI p_{T}^{miss}'
          if 'puppi' not in name.lower() and 'met' in name.lower(): self.var = 'Raw PF p_{T}^{miss}'

      # str(self.var) = str(self.var).replace("[]","")

      if 'Mu' in name: self.extra = 'W #rightarrow #mu#nu'
      if 'El' in name: self.extra = 'W #rightarrow e#nu'
      if 'dy' in name and 'Mu' in name: self.extra = 'Z #rightarrow #mu#mu'
      if 'dy' in name and 'El' in name: self.extra = 'Z #rightarrow ee'
      if 'gjets' in name: self.extra = '#gamma+jets'
      # if 'njetsgt0' in name : self.extra += 'N_{jets}>0'
      # allpv=['_pult10', '_pu10to20', '_pu20to30', '_pu30to40', '_pu40to50', '_pugeq50']
      # self.extra = self.var+self.extra
      SR = "isolt0p15_mtmassgt80"
      B = "isolt0p15_mtmasslt80"
      D = "isogt0p15_mtmasslt80"
      C = "isogt0p15_mtmassgt80"

      if 'isvbf' in name:
          if 'njetsgt0' in name or 'eta_gt0' in name: self.extra = "#splitline{" + self.extra + "}{VBF}"
      if 'isnotvbf' in name:
          jetstext = "}{no VBF N_{jets}>0}"

      if 'vbf' not in name:
          if 'njetseq0' in name or 'eta_eq0' in name:
              if '_pu' not in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0}"
          if '_pult10' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0  - nVtx<10}"
          if '_pu10to20' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - 10<nVtx<20}"
          if '_pu20to30' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - 20<nVtx<30}"
          if '_pu30to40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - 30<nVtx<40}"
          if '_pu40to50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - 40<nVtx<50}"
          if '_pugeq50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - nVtx>50}"
          if '_pugeq40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=0 - nVtx>40}"
      if 'njetseq1' in name or 'eta_eq1' in name:
          if '_pu' not in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1}"
          if '_pult10' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - nVtx<10}"
          if '_pu10to20' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - 10<nVtx<20}"
          if '_pu20to30' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - 20<nVtx<30}"
          if '_pu30to40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - 30<nVtx<40}"
          if '_pu40to50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - 40<nVtx<50}"
          if '_pugeq50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - nVtx>50}"
          if '_pugeq40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}=1 - nVtx>40}"
      if 'njetsgt0' in name or 'eta_gt0' in name:
          if '_pu' not in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0}"
          if '_pult10' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - nVtx<10}"
          if '_pu10to20' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - 10<nVtx<20}"
          if '_pu20to30' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - 20<nVtx<30}"
          if '_pu30to40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - 30<nVtx<40}"
          if '_pu40to50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - 40<nVtx<50}"
          if '_pugeq50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - nVtx>50}"
          if '_pugeq40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}>0 - nVtx>40}"

      if 'njetsgeq0' in name or 'eta_geq0' in name:
          if '_pu' not in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0}"
          if '_pult10' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - nVtx<10}"
          if '_pu10to20' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - 10<nVtx<20}"
          if '_pu20to30' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - 20<nVtx<30}"
          if '_pu30to40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - 30<nVtx<40}"
          if '_pu40to50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - 40<nVtx<50}"
          if '_pugeq50' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - nVtx>50}"
          if '_pugeq40' in name: self.extra = "#splitline{" + self.extra + "}{N_{jets}#geq0 - nVtx>40}"

      if 'lpt' in name:
          if 'leta' in name: self.extra = self.extra.replace("N_{jets}", "pT<50, |#eta|<2.4, N_{jets}")
          if 'heta' in name: self.extra = self.extra.replace("N_{jets}", "pT<50, |#eta|>2.4, N_{jets}")
      if 'hpt' in name:
          if 'leta' in name: self.extra = self.extra.replace("N_{jets}", "pT>50, |#eta|<2.4, N_{jets}")
          if 'heta' in name: self.extra = self.extra.replace("N_{jets}", "pT>50, |#eta|>2.4, N_{jets}")
      # if SR in name : self.extra = self.extra + " SR "
      if B in name: self.extra = self.extra + " B- iso<.15, W_{T}<80 "
      if C in name: self.extra = self.extra + " C- iso>.15, W_{T}>80 "
      if D in name: self.extra = self.extra + " D- iso>.15, W_{T}<80 "

      self.bands = []
      self.options = []
      self.labels = []
      self.labelsOption = []
      self.myLegend = TLegend(x1, y1, x2, y2)
      self.myLegend.SetFillColor(0)
      self.myLegend.SetFillStyle(0)
      self.myLegend.SetTextFont(42)
      self.myLegend.SetTextSize(0.045)
      self.myLegend.SetLineWidth(0)
      self.myLegend.SetBorderSize(0)
      # self.myLegend.SetNColumns(2)

   def ratioHist(self, histNum, histDen, name):

       effHist = histNum.Clone(name);
       effHist = copy.deepcopy(histNum.Clone("num"))

       nBins = histNum.GetNbinsX()
       for iB in range(1, histNum.GetNbinsX() + 1):
           num = float(histNum.GetBinContent(iB))
       den = float(histDen.GetBinContent(iB))
       numE = float(histNum.GetBinError(iB))
       if den > 0:
               ratio = num / den
               ratioE = numE/den
               effHist.SetBinContent(iB,ratio)
               effHist.SetBinError(iB,ratioE)

       return effHist

   def banner(self, isData, lumi, isLog, event, isnVert, isSig1jet, run):
    
      latex = TLatex()                                
      latex.SetNDC();
      latex.SetTextAngle(0);
      latex.SetTextColor(r.kBlack);
      latex.SetTextFont(42);
      latex.SetTextAlign(31);
      latex.SetTextSize(0.08);
      if isnVert:
          latex.DrawLatex(0.28, 0.82, "#bf{CMS}")
      else:
          latex.DrawLatex(0.28, 0.82, "#bf{CMS}")

      latexb = TLatex()
      latexb.SetNDC();
      latexb.SetTextAngle(0);
      latexb.SetTextColor(r.kBlack);
      latexb.SetTextFont(42);
      latexb.SetTextAlign(31);
      latexb.SetTextSize(0.045);
 
      # if(isData):
          # if isnVert:
          #    #latexb.DrawLatex(0.485, 0.93, "#it{Preliminary}")
          # else:
          #    latexb.DrawLatex(0.42, 0.93, "#it{Preliminary}")
      # else:
      #  latexb.DrawLatex(0.42, 0.93, "#it{Simulation}")

      text_lumi = "35.9 fb^{-1} (13 TeV)"
      year = '2018 - '
      if '41' in str(lumi) : year = '2017 - '
      if '16' in str(lumi) : year = '2016postVFP - '
      if '19' in str(lumi) : year = '2016preVFP - '
      if '35' in str(lumi) : year = '2016 - '
      text_lumi = str(year) + str("%.1f" % float(lumi) )+" fb^{-1} (13 TeV)"
      if '137' in str(lumi) : 
          year = 'Run2 - '
          text_lumi = str(year) + "137 fb^{-1} (13 TeV)"
      # text_lumi = str(lumi)+" fb^{-1} (13 TeV, "+ run + ")"

      if '137' not in str(lumi) : latexb.DrawLatex(0.44, 0.82, "#it{Preliminary}")

      latexc = TLatex()
      latexc.SetNDC();
      latexc.SetTextAngle(0);
      latexc.SetTextColor(r.kBlack);
      latexc.SetTextFont(42);
      latexc.SetTextAlign(31);
      latexc.SetTextSize(0.06);
      latexc.DrawLatex(0.90, 0.93, text_lumi)          

      latexd = TLatex()
      latexd.SetNDC();
      latexd.SetTextAngle(90);
      latexd.SetTextColor(r.kBlack);
      latexd.SetTextFont(42);
      latexd.SetTextAlign(31);
      latexd.SetTextSize(0.06);
      if event == 0:
          latexd.DrawLatex(0.059, 0.93, "Events / GeV")          
      else:
          # latexd.DrawLatex(0.059, 0.93, "Events / " +str(event) + " GeV")          
          latexd.DrawLatex(0.059, 0.93, "Events ")          

      latexe = TLatex()
      latexe.SetNDC();
      latexe.SetTextColor(r.kBlack);
      latexe.SetTextFont(42);
      latexe.SetTextAlign(31);
      latexe.SetTextSize(0.045);         
      if isSig1jet:
          latexe.DrawLatex(0.86, 0.55, "p_{T}^{jet1} > 50 GeV")   


   def banner2(self, lumi, chisquare, mean, title, event, isNVert, isSig1jet, integral, fromFit):
    
      latex = TLatex()
      latex.SetNDC();
      latex.SetTextAngle(0);
      latex.SetTextColor(r.kBlack);
      latex.SetTextFont(42);
      latex.SetTextAlign(31);
      latex.SetTextSize(0.05);
      # if isNVert:
      #    latex.DrawLatex(0.28, 0.83, "#bf{CMS}")
      # else:
      #    latex.DrawLatex(0.28, 0.83, "#bf{CMS}")

      latexd = TLatex()
      latexd.SetNDC();
      latexd.SetTextAngle(90);
      latexd.SetTextColor(r.kBlack);
      latexd.SetTextFont(42);
      latexd.SetTextAlign(31);
      latexd.SetTextSize(0.045);
      if event == 0:
          latexd.DrawLatex(0.047, 0.93, "Events / GeV")          
      elif event == '':
          latexd.DrawLatex(0.047, 0.93, "")          
      else:
          latexd.DrawLatex(0.059, 0.93, "Events / " +str(event) + " GeV")        
      


      latexe = TLatex()
      latexe.SetNDC();
      latexe.SetTextColor(r.kBlack);
      latexe.SetTextFont(42);
      latexe.SetTextAlign(31);
      latexe.SetTextSize(0.041);         
      if isSig1jet:
          latexe.DrawLatex(0.86, 0.55, "p_{T}^{jet1} > 50 GeV")   
      
      latexb = TLatex()
      latexb.SetNDC();
      latexb.SetTextAngle(0);
      latexb.SetTextColor(r.kBlack);
      latexb.SetTextFont(42);
      latexb.SetTextAlign(31);
      latexb.SetTextSize(0.041);
 

      text_lumi = "35.9 fb^{-1} (13 TeV)"
      latexc = TLatex()
      latexc.SetNDC();
      latexc.SetTextAngle(0);
      latexc.SetTextColor(r.kBlack);
      latexc.SetTextFont(42);
      latexc.SetTextAlign(31);
      latexc.SetTextSize(0.041);
      latexc.DrawLatex(0.91, 0.93, text_lumi)
#      latexc.DrawLatex(0.6, 0.8,  mean)
#      latexc.DrawLatex(0.6, 0.55, chisquare)OA
      if integral == "":
          latexc.DrawLatex(0.39, 0.6,  "")
      else:
          latexc.DrawLatex(0.39, 0.6,  "Int %.2f " %(integral))

      latexf = TLatex()
      latexf.SetNDC();
      latexf.SetTextAngle(0);
      latexf.SetTextFont(42);
      latexf.SetTextAlign(31);
      latexh = TLatex()
      latexh.SetNDC();
      latexh.SetTextAngle(0);
      latexh.SetTextFont(42);
      latexh.SetTextAlign(31);
      if fromFit:
          latexh.SetTextColor(r.kGray);
          latexf.SetTextColor(r.kBlack);
          latexh.SetTextSize(0.037);         
          latexf.SetTextSize(0.037);         
      else:
          latexf.SetTextColor(r.kGray);
          latexh.SetTextColor(r.kBlack);
          latexf.SetTextSize(0.037);        
          latexh.SetTextSize(0.037);  
          
      latexf.DrawLatex(0.9, 0.85,   chisquare)
      latexh.DrawLatex(0.7, 0.8,  mean)

      latexd = TLatex()                                                  
      latexd.SetNDC();
      latexd.SetTextAngle(0);
      latexd.SetTextColor(r.kBlack);
      latexd.SetTextFont(42);
      latexd.SetTextAlign(31);
      latexd.SetTextSize(0.04);
      latexd.DrawLatex(0.89, 0.03,  title)




   def addBand(self, x1, y1, x2, y2, color, opacity):

      grshade = TGraph(4)
      grshade.SetPoint(0,x1,y1)
      grshade.SetPoint(1,x2,y1)
      grshade.SetPoint(2,x2,y2)
      grshade.SetPoint(3,x1,y2)
      # grshade.SetFillStyle(3001)
      grshade.SetFillColorAlpha(color, opacity)
      self.bands.append(grshade)

   def addLine(self, x1, y1, x2, y2, color, thickness = 0.):
      line = TLine(x1,y1,x2,y2)
      line.SetLineColor(color)
      if thickness:
          line.SetLineWidth(thickness)
      self.lines.append(line)

   def addArrow(self, x1, y1, x2, y2, color, option, thickness = 0.):
      arrow = TArrow(x1,y1,x2,y2, 0.05, option)
      arrow.SetLineColor(color)
      if thickness:
          arrow.SetLineWidth(thickness)
      self.arrows.append(arrow)

   def addLatex(self, x1, y1, text, font=42, size = 0.02):
      lat = [x1, y1, text, font, size]
      self.latexs.append(lat)

 
   def addHisto(self, h, option, label, labelOption, color, ToDraw, orderForLegend):

      if(color != ""):
          h.SetLineColor(color)
          h.SetMarkerColor(color)
      if(label == ""):
          label = h.GetTitle()

      self.histos.append(h)
      self.options.append(option)
      self.labels.append(label)
      self.labelsOption.append(labelOption)
      self.ToDraw.append(ToDraw)
      self.orderForLegend.append(orderForLegend)

   def addGraph(self, h, option, label, labelOption, color, ToDraw, orderForLegend):

      if(color != ""):
          h.SetLineColor(color)
          h.SetMarkerColor(color)
      if(label == ""):
          label = h.GetTitle()

      self.histos.append(h)
      self.options.append(option)
      self.labels.append(label)
      self.labelsOption.append(labelOption)
      self.ToDraw.append(ToDraw)
      self.orderForLegend.append(orderForLegend)


   def addStack(self, h, option, ToDraw, orderForLegend):

      legendCounter = orderForLegend
      if(orderForLegend < len(self.orderForLegend)):
          legendCounter = len(self.orderForLegend)

      self.addHisto(h, option, "", "", "", ToDraw, -1)  
      for h_c in h.GetHists():
          self.addHisto(h_c, "H", h_c.GetTitle(), "F", "", 0, legendCounter)
          legendCounter = legendCounter + 1
       

 
   def makeLegend(self, log):
      # if log:  
     for i in range(0, len(self.histos)):
         for j in range(0, len(self.orderForLegend)):
             if(self.orderForLegend[j] != -1 and self.orderForLegend[j] == i):
                 self.labels[j] = self.labels[j].replace('QCD MG', 'QCD')
                 self.labels[j] = self.labels[j].replace(' + jets', '+jets')
                 self.labels[j] = self.labels[j].replace('-61', '')
                 self.myLegend.AddEntry(self.histos[j], self.labels[j], self.labelsOption[j])
      # else:
      #    self.myLegend.AddEntry(self.histos[4], self.labels[4], self.labelsOption[4])
      #    self.myLegend.AddEntry(self.histos[3], self.labels[3], self.labelsOption[3])


          

   def ensurePath(self, _path):
      d = os.path.dirname(_path)
      if not os.path.exists(d):
         os.makedirs(d)

   def create_error_histogram(self, h_name, h_base, h_up, h_down, n_bins):
       h_error = h_base.Clone(h_name)
       for km in range(1, n_bins + 1):
           error = max(abs(h_up.GetBinContent(km) - h_base.GetBinContent(km)),  abs(h_down.GetBinContent(km) - h_base.GetBinContent(km)))
           h_error.SetBinContent(km, 1)
           h_error.SetBinError(km, error / h_base.GetBinContent(km))
       return h_error




   def saveRatioGjetsClean(self, legend, isData, log,  lumi, hdata, hMC, hjerUp, hjerDown ,  hjesUp, hjesDown ,hunclUp, hunclDown, hpuUp, hpuDown, hidUp, hidDown,title,  option, run = '2016',  r_ymin=0, r_ymax=2):

      
    print('=============>======', option, run, title, lumi)
    formatted_lumi = "%.1f" % float(lumi)
    lumi  = str(formatted_lumi)
    # plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle , option, run_str)
    print('inside Canvas' 'hdata, hMC, hjerUp, hjerDown ,  hjesUp, hjesDown ,hunclUp, hunclDown', hdata.GetSumOfWeights(), hMC.GetSumOfWeights(), hjerUp.GetSumOfWeights(), hjerDown.GetSumOfWeights(), hjesUp.GetSumOfWeights(), hjesDown.GetSumOfWeights(), hunclUp.GetSumOfWeights(), hunclDown.GetSumOfWeights())
    events = 5  
    events = hdata.GetBinWidth(1)
    setUpAxis = 1 
    setLowAxis = 1 
    # log = 1
    doAllErrors = 1
    doSomeErrors = 0
    isNVert = 0
    puppi = 0
    statOnly = 0
    tightRatio = 0
    isSig1jet = 0
    tightRatio = 1
    lowAxis = 0
    makeQCDuncert = 0
    doZ = 0
    lumiSys  = 0.012
    if '41' in run : lumiSys = 0.023
    if '59' in run : 
        print('change of lumiSyst') 
        lumiSys = 0.025
    leptSys  = 0.02
    trigSys  = 0.02
    # print 'some numbers mc, hdata{}, hMC{}, hjerUp{}, hjerDown{} ,  hjesUp{}, hjesDown{} ,hunclUp{}, hunclDown{}, hpuUp{}, hpuDown{}, hidUp{}, hidDown{}'.format(hdata.GetSumOfWeights(), hMC.GetSumOfWeights(), hjerUp.GetSumOfWeights(), hjerDown.GetSumOfWeights() ,  hjesUp.GetSumOfWeights(), hjesDown.GetSumOfWeights() ,hunclUp.GetSumOfWeights(), hunclDown.GetSumOfWeights(), hpuUp.GetSumOfWeights(), hpuDown.GetSumOfWeights(), hidUp.GetSumOfWeights(), hidDown.GetSumOfWeights())
    if 'phi' in title.lower() : 
        hMC.SetMaximum(hMC.GetMaximum()*15)
        hdata.SetMaximum(hMC.GetMaximum())


    # if 'smear' in option.lower() : doAllErrors=1
   
    # if 'smear' in option.lower() : 
    doAllErrors=0
    doSomeErrors=1

    if 'mll' in option  or ('boson_pt' in option and 'Goodboson_' not in option) or 'iso_' in option or 'Photon_' in option or 'Raw' in option: 
        statOnly = 1
        doAllErrors = 0
        doSomeErrors = 0

    if hMC.GetSumOfWeights() == hpuUp.GetSumOfWeights() and hMC.GetSumOfWeights() == hjesUp.GetSumOfWeights(): 
        statOnly = 1
        doAllErrors = 0
        doSomeErrors = 0

    for km in range(1, hMC.GetNbinsX()+1):

        binC = hMC.GetBinContent(km)
        binE = hMC.GetBinError(km)
        lumiErr = binC*lumiSys
        leptErr = binC*leptSys
        trigErr = binC*trigSys

        puErr = max( math.fabs(hpuUp.GetBinContent(km) - hMC.GetBinContent(km)), math.fabs(hpuDown.GetBinContent(km) - hMC.GetBinContent(km)))
        idErr = max( math.fabs(hidUp.GetBinContent(km) - hMC.GetBinContent(km)), math.fabs(hidDown.GetBinContent(km) - hMC.GetBinContent(km)))

        hMC.SetBinError(km, math.sqrt(binE**2 + lumiErr**2 + puErr**2 + idErr**2+leptErr**2 + trigErr**2))
    
    self.myCanvas.cd()

    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0) 
    pad2 = TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
    
    pad1.SetBottomMargin(0.01)
    pad2.SetTopMargin(0.1);
    pad2.SetBottomMargin(0.3);


    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    if(log):
        pad1.SetLogy(1)
    if '_norm' in option : 
        hh = hMC.Clone()
        hh.GetXaxis().SetTitle(title)
        hh.GetXaxis().SetTitleOffset(0.91)
        hh.GetXaxis().SetTitleSize(0.135)
        hh.Draw()
   
    for i in range(0, len(self.histos)):
        if(self.ToDraw[i] != 0):

            if lowAxis:         self.histos[i].SetMinimum(0.00001)
            if setLowAxis:        self.histos[i].SetMinimum(100.)
            if setUpAxis and not log:            self.histos[i].SetMaximum(hMC.Integral()*10)
            
            if log : self.histos[i].SetMaximum(hMC.GetMaximum()*100)
            else :  self.histos[i].SetMaximum(hMC.GetMaximum()*2)

            if log : self.histos[i].SetMinimum(10.)
            else : self.histos[i].SetMinimum(0.1)
            if 'boson' in title.lower() : 
                self.histos[i].SetMaximum(hMC.GetMaximum()*500)
            if '_norm' in option : 
                self.histos[i].SetMaximum(1.5)
                self.histos[i].SetMinimum(0.0001)
                       

            self.histos[i].Draw(self.options[i])
    if(legend):
        self.makeLegend(log)
        self.myLegend.Draw()


    lTex2 = TLatex()
    lTex2.SetNDC()
    lTex2.SetTextSize(0.045)
    # lTex2.SetTextFont(12)
    lTex2.DrawLatex(0.38, 0.75, '{0:s}'.format(self.extra))

    lTex2v = TLatex()
    lTex2v.SetNDC()
    lTex2v.SetTextSize(0.04)
    lTex2v.SetTextFont(42)
    if len(self.var)>2 : 
        if 'smear' not in str(self.var).lower() :  lTex2v.DrawLatex(0.17, 0.75, '{0:s}'.format(self.var))
        if 'smear' in str(self.var).lower()  : lTex2v.DrawLatex(0.15, 0.75, '{0:s}'.format(self.var))

    for band in self.bands:
        band.Draw('f')

    for line in self.lines:
        line.Draw()

    for arrow in self.arrows:
        arrow.Draw()

    for latex in self.latexs:
        lat = TLatex()
        lat.SetNDC()
        lat.SetTextSize(latex[-1])
        lat.SetTextFont(latex[-2])
        lat.DrawLatex(latex[0], latex[1], latex[2])

    hdata.Sumw2()
    hMC.Sumw2()

    ratio = copy.deepcopy(hdata.Clone("ratio"))
    ratio.Divide(hMC)  #here we make the ratio INFO
    # ratio = self.ratioHist(hdata, hMC, hMC.GetName())

    if tightRatio:    ratio.GetYaxis().SetRangeUser(0., 2.);
    else:    ratio.GetYaxis().SetRangeUser(r_ymin, r_ymax);
    if option == "test":
        ratio.GetYaxis().SetTitle("postfix/prefix")
    else:
        ratio.GetYaxis().SetTitle("Data / MC")
        ratio.GetYaxis().CenterTitle();
        ratio.GetYaxis().SetLabelSize(0.12);
        ratio.GetXaxis().SetLabelSize(0.12);
        ratio.GetXaxis().SetTitleOffset(0.91);
        ratio.GetYaxis().SetNdivisions(4);
        ratio.GetYaxis().SetTitleSize(0.13);
        ratio.GetXaxis().SetTitleSize(0.135);
        ratio.GetYaxis().SetTitleOffset(0.41);
        ratio.SetMarkerSize(0.6*ratio.GetMarkerSize());
        ratio.GetXaxis().SetTitle(title)
    
    den1tottot = copy.deepcopy(hMC.Clone("bkgden1"))
    den2tottot = copy.deepcopy(hMC.Clone("bkgden2"))
                                                                                               
    nvar = hMC.GetNbinsX()+1                                                                                                                                                           
    x = array.array('f', range(0, hMC.GetNbinsX()+1))
    y = array.array('f', range(0, hMC.GetNbinsX()+1))
    exl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyltottot = array.array('f', range(0, hMC.GetNbinsX()+1))
    exh = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhtottot = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratiouptottot = copy.deepcopy(hMC.Clone("ratiouptottot"))
    ratiodowntottot = copy.deepcopy(hMC.Clone("ratiodowntottot"))      
    ymax = 2.                                                                                                                                                              
    

    # make tot tot / JER, JES/ Uncl/ errors 

    for km in range(0, hMC.GetNbinsX()+1):

        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_up = hunclUp.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_down = hMC.GetBinContent(km) - hunclDown.GetBinContent(km)
        jer_diff_up = hjerUp.GetBinContent(km) - hMC.GetBinContent(km)
        jer_diff_down = hMC.GetBinContent(km) - hjerDown.GetBinContent(km)
        # jer_diff_up = 0
        # jer_diff_down = 0
        # if hMC.GetBinContent(km)> 0 : print 'diffs',  jer_diff_up/hMC.GetBinContent(km),  jer_diff_down/hMC.GetBinContent(km), km, jes_diff_up/hMC.GetBinContent(km), jes_diff_down/hMC.GetBinContent(km)
        conte1tottot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 + uncl_diff_up**2 + jer_diff_up**2 )
        conte2tottot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 + uncl_diff_down**2 + jer_diff_down**2 )

        if conte1tottot > conte2tottot:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot);                                                                                            
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte1tottot);                                                                                                                           
            ymax = hMC.GetBinContent(km) + conte1tottot;           
            eyltottot[km] = conte2tottot;                                                                                                                                                           
            eyhtottot[km] = conte1tottot;                                                                                                                         
        else:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte2tottot);  
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot);
            ymax = hMC.GetBinContent(km) + conte2tottot;           
            eyltottot[km] = conte1tottot;                                                                                                                                                           
            eyhtottot[km] = conte2tottot;                                                                                                                         

        exl[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        exh[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        
    ratiouptottot.Divide(den1tottot);                                                                                                                                                         
    ratiodowntottot.Divide(den2tottot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km);                                                                                                                                          
        y[km] = 1;                                                                                                                                                               
        exl[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
        exh[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
                                                                                                   
        if (ratiouptottot.GetBinContent (km) != 0):
            eyhtottot[km] = (1. / ratiouptottot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                    
        else:                                                                                                                                                                       
            eyhtottot[km] = 0;                                                                                                                                                                 
                                                                                                   
        if (ratiodowntottot.GetBinContent (km) != 0):
            eyltottot[km] = (1 - 1. / ratiodowntottot.GetBinContent (km))*ratiodata.GetBinContent (km);                                                              
        else:                                                                                                                                                                       
            eyltottot[km] = 0.                                                                                                                        
        errtottot = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltottot, eyhtottot);                                



    # make syst + jes errors 
    for km in range(0, hMC.GetNbinsX()+1):

        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)

        conte1tottot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 )
        conte2tottot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 )
        # den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot)
            # den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot)
        if conte1tottot > conte2tottot:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot);                                                                                            
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte1tottot);                                                                                                                           
            ymax = hMC.GetBinContent(km) + conte1tottot;           
            eyltottot[km] = conte2tottot;                                                                                                                                                           
            eyhtottot[km] = conte1tottot;                                                                                                                         
        else:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte2tottot);  
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot);
            ymax = hMC.GetBinContent(km) + conte2tottot;           
            eyltottot[km] = conte1tottot;                                                                                                                                                           
            eyhtottot[km] = conte2tottot;                                                                                                                         
        exl[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        exh[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
    ratiouptottot.Divide(den1tottot);                                                                                                                                                         
    ratiodowntottot.Divide(den2tottot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km);                                                                                                                                          
        y[km] = 1;                                                                                                                                                               
        exl[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
        exh[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
                                                                                                   
        if (ratiouptottot.GetBinContent (km) != 0):
            eyhtottot[km] = (1. / ratiouptottot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                    
        else:                                                                                                                                                                       
            eyhtottot[km] = 0;                                                                                                                                                                 
                                                                                                   
        if (ratiodowntottot.GetBinContent (km) != 0):
            eyltottot[km] = (1 - 1. / ratiodowntottot.GetBinContent (km))*ratiodata.GetBinContent (km);                                                              
        else:                                                                                                                                                                       
            eyltottot[km] = 0.                                                                                                                        
    err = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltottot, eyhtottot);                                



    # make tot errors
    den1tot = copy.deepcopy(hMC.Clone("bkgden1"))
    den2tot = copy.deepcopy(hMC.Clone("bkgden2"))
                                 
    nvar = hMC.GetNbinsX()+1                                       
    x = array.array('f', range(0, hMC.GetNbinsX()+1))
    y = array.array('f', range(0, hMC.GetNbinsX()+1))
    exl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyltot = array.array('f', range(0, hMC.GetNbinsX()+1))
    exh = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhtot = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratiouptot = copy.deepcopy(hMC.Clone("ratiouptot"))
    ratiodowntot = copy.deepcopy(hMC.Clone("ratiodowntot"))      
    
    # make syst + jes + uncl   
    for km in range(0, hMC.GetNbinsX()+1):

        # conte1tot =  math.sqrt( hMC.GetBinError (km) **2  + (hjesUp.GetBinContent (km) - hMC.GetBinContent   (km))**2 + (hunclUp.GetBinContent (km) - hMC.GetBinContent(km))**2 )       
        
        # conte2tot =  math.sqrt(hMC.GetBinError (km) **2 + (hMC.GetBinContent (km) - hjesDown.GetBinContent (km))**2 + (-hunclDown.GetBinContent (km) + hMC.GetBinContent(km))**2 )  
        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_up = hunclUp.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_down = hMC.GetBinContent(km) - hunclDown.GetBinContent(km)

        conte1tot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 + uncl_diff_up**2 )
        conte2tot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 + uncl_diff_down**2 )
        if conte1tot > conte2tot:
            den1tot.SetBinContent (km, hMC.GetBinContent (km) + conte1tot)
            den2tot.SetBinContent (km, hMC.GetBinContent (km) - conte1tot)
            ymax = hMC.GetBinContent(km) + conte1tot           
            eyltot[km] = conte2tot 
            eyhtot[km] = conte1tot                                                                                   
        else:
            den1tot.SetBinContent (km, hMC.GetBinContent (km) + conte2tot)
            den2tot.SetBinContent (km, hMC.GetBinContent (km) - conte2tot)

        ymax = hMC.GetBinContent(km) + conte2tot
        eyltot[km] = conte1tot
        eyhtot[km] = conte2tot                                                                                   
        exl[km] = hMC.GetBinWidth (km) / 2
        exh[km] = hMC.GetBinWidth (km) / 2                                                                                                                                 
        
    ratiouptot.Divide(den1tot);                                                                                                                                                         
    ratiodowntot.Divide(den2tot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                    
    # ratiodata = self.ratioHist(ratiodata, hMC, hMC.GetName())
                                                                                               
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km)
        y[km] = 1                                                                                                                                 
        exl[km] = ratiodata.GetBinWidth (km) / 2
        exh[km] = ratiodata.GetBinWidth (km) / 2                                                                                                                                     
                                                                                                   
        if (ratiouptot.GetBinContent (km) != 0):
            eyhtot[km] = (1. / ratiouptot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                                                   
        else:
            eyhtot[km] = 0;                                                                                                                                                                 
        if (ratiodowntot.GetBinContent (km) != 0):
            eyltot[km] = (1 - 1. / ratiodowntot.GetBinContent (km))*ratiodata.GetBinContent (km)
        else:
            eyltot[km] = 0.                                                                                                                                                                       
    errtot = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltot, eyhtot);                                                                                 
    
    # make some jec + stat errors     
    den1 = copy.deepcopy(hMC.Clone("bkgden1"))
    den2 = copy.deepcopy(hMC.Clone("bkgden2"))
                                                                                               
    nvar = hMC.GetNbinsX()+1                                                                                                                                                           
    eyl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyh = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratioup = copy.deepcopy(hMC.Clone("ratioup"))
    ratiodown = copy.deepcopy(hMC.Clone("ratiodown")) 
    
    for km in range(0, hMC.GetNbinsX()+1):
        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)

        conte1 = math.sqrt(mc_bin_error**2 + jes_diff_up**2 )
        conte2 = math.sqrt(mc_bin_error**2 + jes_diff_down**2 )
           
        '''
        den1.SetBinContent (km, hMC.GetBinContent (km) + conte1);                                                                                                                           
        den2.SetBinContent (km, hMC.GetBinContent (km) - conte2);                                                                                                                           
        '''
        if conte1 > conte2:
            den1.SetBinContent(km, hMC.GetBinContent(km) + conte1)
            den2.SetBinContent(km, hMC.GetBinContent(km) - conte1)
            ymax = hMC.GetBinContent(km) + conte1
            eyl[km] = conte2
            eyh[km] = conte1
        else:
            den1.SetBinContent(km, hMC.GetBinContent(km) + conte2)
            den2.SetBinContent(km, hMC.GetBinContent(km) - conte2)
            ymax = hMC.GetBinContent(km) + conte2
            eyl[km] = conte1
            eyh[km] = conte2
    
    ratioup.Divide(den1)
    ratiodown.Divide(den2)
                                                                                               
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratioup.GetBinContent (km) != 0):
            eyh[km] = (1. / ratioup.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                                                   
        else:                                                                                                                                                                      
            eyh[km] = 0                                                                                                                                                               
        if (ratiodown.GetBinContent (km) != 0):
            eyl[km] = (1 - 1. / ratiodown.GetBinContent (km))*ratiodata.GetBinContent (km)
        else: 
            eyl[km] = 0.                                                                                                                        

    err = TGraphAsymmErrors(nvar, x, y, exl, exh, eyl, eyh);                                                                                                                                         

    # make some stat errors
    dens1 = copy.deepcopy(hMC.Clone("bkgdens1"))
    dens2 = copy.deepcopy(hMC.Clone("bkgdens2"))
    eyls = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhs = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratioups = copy.deepcopy(hMC.Clone("ratioups"))
    ratiodowns = copy.deepcopy(hMC.Clone("ratiodowns"))
    ymaxs = 2.                                                     
    

    for km in range(0, hMC.GetNbinsX() + 1):
        contes1 = hMC.GetBinError(km)
        contes2 = hMC.GetBinError(km)
        dens1.SetBinContent(km, hMC.GetBinContent(km) + contes1)
        dens2.SetBinContent(km, hMC.GetBinContent(km) - contes2)
        ymaxs = hMC.GetBinContent(km) + contes1
        eyls[km] = conte2
        eyhs[km] = conte1

    ratioups.Divide(dens1)
    ratiodowns.Divide(dens2)
    for km in range(0, ratiodata.GetNbinsX() + 1):
        if (ratioups.GetBinContent(km) != 0):
            eyhs[km] = (1. / ratioups.GetBinContent(km) - 1) *  ratiodata.GetBinContent(km)
        else:
            eyhs[km] = 0

        if (ratiodowns.GetBinContent(km) != 0):
            eyls[km] = (1 - 1. / ratiodowns.GetBinContent(km)) * ratiodata.GetBinContent(km)
        else:
            eyls[km] = 0.

    staterr = TGraphAsymmErrors(nvar, x, y, exl, exh, eyls, eyhs);



    # colors = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]
    # gray ['#B3B3B3', '#8C8C8C',   '#666666'    #D9D9D9', '#B3B3B3', '#8C8C8C']
    errtottot.SetFillColor (r.TColor.GetColor("#bd1f01")); #cyan not used
    errtottot.SetFillStyle (1001)

    # errtot.SetFillColor(r.TColor.GetColor("#964a8b"))
    errtot.SetFillColor(r.TColor.GetColor("#e76300"))
    errtot.SetFillColor(r.TColor.GetColor("#ffa90e"))
    errtot.SetFillColor(r.TColor.GetColor("#666666"))
    errtot.SetFillColor(r.TColor.GetColor("#8C8C8C"))
    # errtot.SetFillColor(r.kBlack)
    # errtot.SetFillStyle (2001) 
    # errtot.SetFillColor(0);
    # errtot.SetFillStyle(0);
    # errtot.SetLineWidth(2);

    # err.SetFillColor (r.TColor.GetColor("#3f90da")); #717581 3f90da
    err.SetFillColor (r.TColor.GetColor("#8C8C8C")); #717581 3f90d
    err.SetFillColor (r.TColor.GetColor("#B3B3B3")); #717581 3f90d
    # err.SetFillStyle (3244);   

    # staterr.SetFillColor (r.TColor.GetColor("#92dadd"));#gray
    staterr.SetFillColor (r.TColor.GetColor("#B3B3B3"));#gray
    staterr.SetFillColor (r.TColor.GetColor("#D9D9D9"));#gray
    # staterr.SetFillStyle (3004);   
    h_err= hMC.Clone("h_err")

    h_err.SetFillStyle(3004)
    h_err.SetFillColor(r.kBlack)
    h_err.SetMarkerSize(0)
    h_err.Draw("e2same0")
    pad2.cd()

    line = TLine(ratio.GetBinLowEdge(1), 1, ratio.GetBinLowEdge(ratio.GetNbinsX()+1), 1)
    line.SetLineColor(r.kRed)
    line.SetLineStyle(2)

    # for iB in range(1, ratio.GetNbinsX()+1):
    #   ratio.SetBinError(iB,hdata.GetBinError(iB))
    ratio.SetMarkerSize(1)
    ratio.Draw()

    print('will I do the errors????', doAllErrors, doSomeErrors)
    if doAllErrors:
        legratio2 = TLegend(0.1,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(3);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        # legratio2.AddEntry(errtottot, "JER+Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(errtot, "Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(err, "JES+Stat/Other","f");
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        errtottot.Draw("E2 same")
        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()


    if doSomeErrors:
        legratio2 = TLegend(0.135,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(3);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        # legratio2.AddEntry(errtottot, "JER+Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(errtot, "Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(err, "JES+Stat/Other","f");
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        # errtottot.Draw("E2 same")

        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        # ratio.Draw("same");                                                      
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()





    if puppi: 
        legratio = TLegend(0.14,0.31,0.4,0.45);                                   
        legratio.SetFillColor(0);
        legratio.SetBorderSize(0);
        legratio.SetNColumns(2);
        legratio.AddEntry(err, "JES + Stat/Other","f");
        legratio.AddEntry(staterr, "Stat","f");                                  
        err.Draw("e2")
        staterr.Draw("2 same")
        legratio.Draw("same")
        line.Draw("same")
        ratio.Draw("same");      
    if statOnly:
        # legratio = TLegend(0.14,0.32,0.43,0.5);
        # legratio.SetFillColor(0);
        # legratio.SetBorderSize(0);
        # legratio.AddEntry(staterr, " ","f");                                  
        # errtottot.Draw("2 same")
        # staterr.Draw("2 same")
        # legratio.Draw("same")
        # line.Draw("same")
        # ratio.Draw("same");                                                      
        legratio2 = TLegend(0.45,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(4);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        errtottot.Draw("E2 same")
        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        # ratio.Draw("same");                                                      
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()


    if statOnly:
        #legratio = TLegend(0.14,0.32,0.43,0.5);
        #legratio.SetFillColor(0);
        #legratio.SetBorderSize(0);
        #legratio.AddEntry(staterr, " ","f");                                  
        #errtottot.Draw("2 same")
        #staterr.Draw("2 same")
        #legratio.Draw("same")
        #line.Draw("same")
        #ratio.Draw("same");                                                      
        legratio2 = TLegend(0.45,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(4);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        errtottot.Draw("E2 same")
        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        #ratio.Draw("same");                                                      
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()
       



       
    pad1.cd()
    legratio = TLegend(0.6,0.53,0.8,0.6);
    # legratio = TLegend(0.698,0.53,0.88,0.6);
    legratio.SetFillColor(r.kWhite);
    legratio.SetFillStyle(0)
    legratio.SetBorderSize(0)
    legratio.SetTextSize(0.045)
    legratio.SetTextFont(42)
    # legratio.AddEntry(errtottot, "Uncertainty","f");
    # legratio.Draw("same")
    # errtottot.Draw("hist same")
    # errtottot.Draw("2 same")
    self.banner(isData, lumi, log, events, isNVert, isSig1jet, run)
    for plotName in self.plotNames:
        path = 'plots/'+plotName
        self.ensurePath(path)
        self.myCanvas.SaveAs(path)

    self.myCanvas.SaveAs('./plots/test/paperv2/test.C')







   def saveRatioGjets(self, legend, isData, log,  lumi, hdata, hMC, hjerUp, hjerDown ,  hjesUp, hjesDown ,hunclUp, hunclDown, hpuUp, hpuDown, hidUp, hidDown,title,  option, run = '2016',  r_ymin=0, r_ymax=2):

      
    print('=============>======', option, run, title, lumi)
    formatted_lumi = "%.1f" % float(lumi)
    lumi  = str(formatted_lumi)
    # plot_var.saveRatio(1,1, isLog, lumi, data_hist, mc_histo, mc_up, mc_down, mc_jesup, mc_jesdown, mc_unclUp, mc_unclDown, varTitle , option, run_str)
    print('inside Canvas' 'hdata, hMC, hjerUp, hjerDown ,  hjesUp, hjesDown ,hunclUp, hunclDown', hdata.GetSumOfWeights(), hMC.GetSumOfWeights(), hjerUp.GetSumOfWeights(), hjerDown.GetSumOfWeights(), hjesUp.GetSumOfWeights(), hjesDown.GetSumOfWeights(), hunclUp.GetSumOfWeights(), hunclDown.GetSumOfWeights())
    events = 5  
    events = hdata.GetBinWidth(1)
    setUpAxis = 1 
    setLowAxis = 1 
    # log = 1
    doAllErrors = 1
    doSomeErrors = 0
    isNVert = 0
    puppi = 0
    statOnly = 0
    tightRatio = 0
    isSig1jet = 0
    tightRatio = 1
    lowAxis = 0
    makeQCDuncert = 0
    doZ = 0
    lumiSys  = 0.012
    if '41' in run : lumiSys = 0.023
    if '59' in run : 
        print('change of lumiSyst') 
        lumiSys = 0.025
    leptSys  = 0.02
    trigSys  = 0.02
    # print 'some numbers mc, hdata{}, hMC{}, hjerUp{}, hjerDown{} ,  hjesUp{}, hjesDown{} ,hunclUp{}, hunclDown{}, hpuUp{}, hpuDown{}, hidUp{}, hidDown{}'.format(hdata.GetSumOfWeights(), hMC.GetSumOfWeights(), hjerUp.GetSumOfWeights(), hjerDown.GetSumOfWeights() ,  hjesUp.GetSumOfWeights(), hjesDown.GetSumOfWeights() ,hunclUp.GetSumOfWeights(), hunclDown.GetSumOfWeights(), hpuUp.GetSumOfWeights(), hpuDown.GetSumOfWeights(), hidUp.GetSumOfWeights(), hidDown.GetSumOfWeights())
    if 'phi' in title.lower() : 
        hMC.SetMaximum(hMC.GetMaximum()*15)
        hdata.SetMaximum(hMC.GetMaximum())



    # if 'smear' in option.lower() : doAllErrors=1
   
    # if 'smear' in option.lower() : 
    doAllErrors=0
    doSomeErrors=1

    if 'mll' in option  or ('boson_pt' in option and 'Goodboson_' not in option) or 'iso_' in option or 'Photon_' in option or 'Raw' in option: 
        statOnly = 1
        doAllErrors = 0
        doSomeErrors=0

    if hMC.GetSumOfWeights() == hunclUp.GetSumOfWeights() and hMC.GetSumOfWeights() == hpuUp.GetSumOfWeights()  : 
        doSomeErrors=0
        doAllErrors = 0
        statOnly = 1


    for km in range(1, hMC.GetNbinsX()+1):

        binC = hMC.GetBinContent(km)
        binE = hMC.GetBinError(km)
        lumiErr = binC*lumiSys
        leptErr = binC*leptSys
        trigErr = binC*trigSys

        puErr = max( math.fabs(hpuUp.GetBinContent(km) - hMC.GetBinContent(km)), math.fabs(hpuDown.GetBinContent(km) - hMC.GetBinContent(km)))
        idErr = max( math.fabs(hidUp.GetBinContent(km) - hMC.GetBinContent(km)), math.fabs(hidDown.GetBinContent(km) - hMC.GetBinContent(km)))

        hMC.SetBinError(km, math.sqrt(binE**2 + lumiErr**2 + puErr**2 + idErr**2+leptErr**2 + trigErr**2))
        # hMC.SetBinError(km, math.sqrt(binE**2 + lumiErr**2 + puErr**2 ))
        # hMC.SetBinError(km, math.sqrt(binE*binE + lumiErr*lumiErr ))#+ leptErr*leptErr + trigErr*trigErr))
            # print 'bissssssssssssssssssssss', hMC.GetBinError(km), km, option
    
    self.myCanvas.cd()

    # if '_norm' in option : 
    #    pad1 = TPad("pad1", "pad1", 0, 0.1, 1, 1.0) 
    #    pad2 = TPad("pad2", "pad2", 0, 0.0, 1, 0.)
    # else : 
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0) 
    pad2 = TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
    
    # if "_norm" in option : 
    #   pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0) 
    #   pad2 = TPad("pad2", "pad2", 0, 0.0, 0, 0.)


    pad1.SetBottomMargin(0.01)
    pad2.SetTopMargin(0.1);
    pad2.SetBottomMargin(0.3);


    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    if(log):    pad1.SetLogy(1)
    if '_norm' in option : 
        hh = hMC.Clone()
        hh.GetXaxis().SetTitle(title)
        hh.GetXaxis().SetTitleOffset(0.91)
        hh.GetXaxis().SetTitleSize(0.135)
        hh.Draw()
   
    for i in range(0, len(self.histos)):
        if(self.ToDraw[i] != 0):

            if lowAxis:         self.histos[i].SetMinimum(0.00001)
            if setLowAxis:        self.histos[i].SetMinimum(100.)
            if setUpAxis and not log:            self.histos[i].SetMaximum(hMC.Integral()*10)
            
            # self.histos[i].SetMaximum(200)
            # self.histos[i].SetMaximum(hMC.Integral()*2)
            # self.histos[i].SetMaximum(hMC.Integral()*2)
            if log : self.histos[i].SetMaximum(hMC.GetMaximum()*100)
            else :  self.histos[i].SetMaximum(hMC.GetMaximum()*2)
            # self.histos[i].SetMinimum(0.001)
            if log : self.histos[i].SetMinimum(10.)
            else : self.histos[i].SetMinimum(0.1)
            if 'boson' in title.lower() : 
                self.histos[i].SetMaximum(hMC.GetMaximum()*500)
            if '_norm' in option : 
                self.histos[i].SetMaximum(1.5)
                self.histos[i].SetMinimum(0.0001)
                           
                # print '----------------------------========================= histo i', i, hMC.GetName(), hMC.GetMaximum(), 'histos name', self.histos[i].GetName(), self.histos[i].GetMaximum(), log, lowAxis, setLowAxis, setUpAxis 

                self.histos[i].Draw(self.options[i])
    # print '----------------------------=========================', hMC.GetMaximum(), log, lowAxis, setLowAxis, setUpAxis 
    if(legend):
        self.makeLegend(log)
        self.myLegend.Draw()


    # lTex2 = TLatex(hMC.GetBinLowEdge(2), hMC.GetMaximum()*0.85,'{0:s}'.format(self.extra))
    # lTex2 = TLatex(0.28, 0.75,'{0:s}'.format(self.extra))
    lTex2 = TLatex()
    lTex2.SetNDC()
    lTex2.SetTextSize(0.045)
    # lTex2.SetTextFont(12)
    lTex2.DrawLatex(0.38, 0.75, '{0:s}'.format(self.extra))

    lTex2v = TLatex()
    lTex2v.SetNDC()
    lTex2v.SetTextSize(0.04)
    lTex2v.SetTextFont(42)
    if len(self.var)>3 : 
        if 'smear' not in str(self.var).lower() :  lTex2v.DrawLatex(0.17, 0.75, '{0:s}'.format(self.var))
        if 'smear' in str(self.var).lower()  : lTex2v.DrawLatex(0.15, 0.75, '{0:s}'.format(self.var))

    for band in self.bands:
        band.Draw('f')

    for line in self.lines:
        line.Draw()

    for arrow in self.arrows:
        arrow.Draw()

    for latex in self.latexs:
        lat = TLatex()
        lat.SetNDC()
        lat.SetTextSize(latex[-1])
        lat.SetTextFont(latex[-2])
        lat.DrawLatex(latex[0], latex[1], latex[2])

    hdata.Sumw2()
    hMC.Sumw2()

    ratio = copy.deepcopy(hdata.Clone("ratio"))
    ratio.Divide(hMC)  #here we make the ratio INFO
    # ratio = self.ratioHist(hdata, hMC, hMC.GetName())

    if tightRatio:
        ratio.GetYaxis().SetRangeUser(0., 2.);
    else:
        ratio.GetYaxis().SetRangeUser(r_ymin, r_ymax);
    if option == "test":
        ratio.GetYaxis().SetTitle("postfix/prefix")
    else:
        ratio.GetYaxis().SetTitle("Data / MC")
    ratio.GetYaxis().CenterTitle();
    ratio.GetYaxis().SetLabelSize(0.12);
    ratio.GetXaxis().SetLabelSize(0.12);
    ratio.GetXaxis().SetTitleOffset(0.91);
    ratio.GetYaxis().SetNdivisions(4);
    ratio.GetYaxis().SetTitleSize(0.13);
    ratio.GetXaxis().SetTitleSize(0.135);
    ratio.GetYaxis().SetTitleOffset(0.41);
    ratio.SetMarkerSize(0.6*ratio.GetMarkerSize());
    ratio.GetXaxis().SetTitle(title)
    
    den1tottot = copy.deepcopy(hMC.Clone("bkgden1"))
    den2tottot = copy.deepcopy(hMC.Clone("bkgden2"))
                                                                                               
    nvar = hMC.GetNbinsX()+1                                                                                                                                                           
    x = array.array('f', range(0, hMC.GetNbinsX()+1))
    y = array.array('f', range(0, hMC.GetNbinsX()+1))
    exl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyltottot = array.array('f', range(0, hMC.GetNbinsX()+1))
    exh = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhtottot = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratiouptottot = copy.deepcopy(hMC.Clone("ratiouptottot"))
    ratiodowntottot = copy.deepcopy(hMC.Clone("ratiodowntottot"))      
    ymax = 2.                                                                                                                                                              
    

    # make tot tot / JER, JES/ Uncl/ errors 

    for km in range(0, hMC.GetNbinsX()+1):

        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_up = hunclUp.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_down = hMC.GetBinContent(km) - hunclDown.GetBinContent(km)
        jer_diff_up = hjerUp.GetBinContent(km) - hMC.GetBinContent(km)
        jer_diff_down = hMC.GetBinContent(km) - hjerDown.GetBinContent(km)
        # jer_diff_up = 0
        # jer_diff_down = 0
        # if hMC.GetBinContent(km)> 0 : print 'diffs',  jer_diff_up/hMC.GetBinContent(km),  jer_diff_down/hMC.GetBinContent(km), km, jes_diff_up/hMC.GetBinContent(km), jes_diff_down/hMC.GetBinContent(km)
        conte1tottot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 + uncl_diff_up**2 + jer_diff_up**2 )
        conte2tottot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 + uncl_diff_down**2 + jer_diff_down**2 )

        if conte1tottot > conte2tottot:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot);                                                                                            
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte1tottot);                                                                                                                           
            ymax = hMC.GetBinContent(km) + conte1tottot;           
            eyltottot[km] = conte2tottot;                                                                                                                                                           
            eyhtottot[km] = conte1tottot;                                                                                                                         
        else:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte2tottot);  
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot);

        ymax = hMC.GetBinContent(km) + conte2tottot;           
        eyltottot[km] = conte1tottot
        eyhtottot[km] = conte2tottot
        exl[km] = hMC.GetBinWidth (km) / 2
        exh[km] = hMC.GetBinWidth (km) / 2                                                                                                                                 
    
    ratiouptottot.Divide(den1tottot);                                                                                                                                                         
    ratiodowntottot.Divide(den2tottot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km);                                                                                                                                          
        y[km] = 1;                                                                                                                                                               
        exl[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
        exh[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
                                                                                                   
        if (ratiouptottot.GetBinContent (km) != 0):
            eyhtottot[km] = (1. / ratiouptottot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                    
        else:                                                                                                                                                                       
            eyhtottot[km] = 0;                                                                                                                                                                 
                                                                                                   
        if (ratiodowntottot.GetBinContent (km) != 0):
            eyltottot[km] = (1 - 1. / ratiodowntottot.GetBinContent (km))*ratiodata.GetBinContent (km);                                                              
        else:                                                                                                                                                                       
            eyltottot[km] = 0.                                                                                                                        
        errtottot = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltottot, eyhtottot);                                



    # make syst + jes errors 
    for km in range(0, hMC.GetNbinsX()+1):

        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)

        conte1tottot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 )
        conte2tottot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 )
        # den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot)
            # den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot)
        if conte1tottot > conte2tottot:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte1tottot);                                                                                            
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte1tottot);                                                                                                                           
            ymax = hMC.GetBinContent(km) + conte1tottot;           
            eyltottot[km] = conte2tottot;                                                                                                                                                           
            eyhtottot[km] = conte1tottot;                                                                                                                         
        else:
            den1tottot.SetBinContent (km, hMC.GetBinContent (km) + conte2tottot);  
            den2tottot.SetBinContent (km, hMC.GetBinContent (km) - conte2tottot);
            ymax = hMC.GetBinContent(km) + conte2tottot;           
            eyltottot[km] = conte1tottot;                                                                                                                                                           
            eyhtottot[km] = conte2tottot;                                                                                                                         
        exl[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        exh[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
    ratiouptottot.Divide(den1tottot);                                                                                                                                                         
    ratiodowntottot.Divide(den2tottot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km);                                                                                                                                          
        y[km] = 1;                                                                                                                                                               
        exl[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
        exh[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
                                                                                                   
        if (ratiouptottot.GetBinContent (km) != 0):
            eyhtottot[km] = (1. / ratiouptottot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                    
        else:                                                                                                                                                                       
            eyhtottot[km] = 0;                                                                                                                                                                 
                                                                                                   
        if (ratiodowntottot.GetBinContent (km) != 0):
            eyltottot[km] = (1 - 1. / ratiodowntottot.GetBinContent (km))*ratiodata.GetBinContent (km);                                                              
        else:                                                                                                                                                                       
            eyltottot[km] = 0.                                                                                                                        
        err = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltottot, eyhtottot);                                



    # make tot errors
    den1tot = copy.deepcopy(hMC.Clone("bkgden1"))
    den2tot = copy.deepcopy(hMC.Clone("bkgden2"))
                                 
    nvar = hMC.GetNbinsX()+1                                       
    x = array.array('f', range(0, hMC.GetNbinsX()+1))
    y = array.array('f', range(0, hMC.GetNbinsX()+1))
    exl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyltot = array.array('f', range(0, hMC.GetNbinsX()+1))
    exh = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhtot = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratiouptot = copy.deepcopy(hMC.Clone("ratiouptot"))
    ratiodowntot = copy.deepcopy(hMC.Clone("ratiodowntot"))      
    
    # make syst + jes + uncl   
    for km in range(0, hMC.GetNbinsX()+1):

        # conte1tot =  math.sqrt( hMC.GetBinError (km) **2  + (hjesUp.GetBinContent (km) - hMC.GetBinContent   (km))**2 + (hunclUp.GetBinContent (km) - hMC.GetBinContent(km))**2 )       
        
        # conte2tot =  math.sqrt(hMC.GetBinError (km) **2 + (hMC.GetBinContent (km) - hjesDown.GetBinContent (km))**2 + (-hunclDown.GetBinContent (km) + hMC.GetBinContent(km))**2 )  
        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_up = hunclUp.GetBinContent(km) - hMC.GetBinContent(km)
        uncl_diff_down = hMC.GetBinContent(km) - hunclDown.GetBinContent(km)

        conte1tot = math.sqrt(mc_bin_error**2 + jes_diff_up**2 + uncl_diff_up**2 )
        conte2tot = math.sqrt(mc_bin_error**2 + jes_diff_down**2 + uncl_diff_down**2 )
        if conte1tot > conte2tot:
            den1tot.SetBinContent (km, hMC.GetBinContent (km) + conte1tot)
            den2tot.SetBinContent (km, hMC.GetBinContent (km) - conte1tot)
            ymax = hMC.GetBinContent(km) + conte1tot;           
            eyltot[km] = conte2tot
            eyhtot[km] = conte1tot                                                                                   
        else:
            den1tot.SetBinContent (km, hMC.GetBinContent (km) + conte2tot)
            den2tot.SetBinContent (km, hMC.GetBinContent (km) - conte2tot)
            ymax = hMC.GetBinContent(km) + conte2tot;           
            eyltot[km] = conte1tot                                                                                                                   
            eyhtot[km] = conte2tot                                                                                   


        exl[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        exh[km] = hMC.GetBinWidth (km) / 2;                                                                                                                                 
        
    ratiouptot.Divide(den1tot);                                                                                                                                                         
    ratiodowntot.Divide(den2tot);                   
    ratiodata = copy.deepcopy(hdata.Clone("ratiodata"))
    ratiodata.Divide (hMC);                                                                                                                                                    
    # ratiodata = self.ratioHist(ratiodata, hMC, hMC.GetName())
                                                                                               
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratiodata.GetBinContent (km) > ymax):
            ymax = ratiodata.GetBinContent (km) + ratiodata.GetBinError (km);                                                                                                              
        x[km] = ratiodata.GetBinCenter (km);                                                                                                                                          
        y[km] = 1;                                                                                                                                                               
        exl[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
        exh[km] = ratiodata.GetBinWidth (km) / 2;                                                                                                                                     
                                                                                                   
        if (ratiouptot.GetBinContent (km) != 0):
            eyhtot[km] = (1. / ratiouptot.GetBinContent (km) - 1)*ratiodata.GetBinContent (km);                                                                                                   
        else:                                                                                                                                                                       
            eyhtot[km] = 0;                                                                                                                                                                 
                                                                                                   
        if (ratiodowntot.GetBinContent (km) != 0):
            eyltot[km] = (1 - 1. / ratiodowntot.GetBinContent (km))*ratiodata.GetBinContent (km);                                                                                                   
        else:                                                                                                                                                                       
            eyltot[km] = 0.                                                                                                                        
        errtot = TGraphAsymmErrors(nvar, x, y, exl, exh, eyltot, eyhtot);                                                                                 
        
    # make some jec + stat errors     
    den1 = copy.deepcopy(hMC.Clone("bkgden1"))
    den2 = copy.deepcopy(hMC.Clone("bkgden2"))
                                                                                               
    nvar = hMC.GetNbinsX()+1                                                                                                                                                           
    eyl = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyh = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratioup = copy.deepcopy(hMC.Clone("ratioup"))
    ratiodown = copy.deepcopy(hMC.Clone("ratiodown")) 
    
    for km in range(0, hMC.GetNbinsX()+1):
        mc_bin_error = hMC.GetBinError(km)
        jes_diff_up = hjesUp.GetBinContent(km) - hMC.GetBinContent(km)
        jes_diff_down = hjesDown.GetBinContent(km) - hMC.GetBinContent(km)

        conte1 = math.sqrt(mc_bin_error**2 + jes_diff_up**2 )
        conte2 = math.sqrt(mc_bin_error**2 + jes_diff_down**2 )
           
        '''
        den1.SetBinContent (km, hMC.GetBinContent (km) + conte1);                                                                                                                           
        den2.SetBinContent (km, hMC.GetBinContent (km) - conte2);                                                                                                                           
           '''
        if conte1 > conte2:
            den1.SetBinContent (km, hMC.GetBinContent (km) + conte1);                                                                                                                           
            den2.SetBinContent (km, hMC.GetBinContent (km) - conte1);                                                                                                                           
            ymax = hMC.GetBinContent(km) + conte1;           
            eyl[km] = conte2
            eyh[km] = conte1                                                                                                                                                                        
        else:
            den1.SetBinContent (km, hMC.GetBinContent (km) + conte2);  
            den2.SetBinContent (km, hMC.GetBinContent (km) - conte2);
            ymax = hMC.GetBinContent(km) + conte2
            eyl[km] = conte1
            eyh[km] = conte2

    ratioup.Divide(den1)
    ratiodown.Divide(den2)                   
                                                                                               
    for km in range(0, ratiodata.GetNbinsX()+1):
        if (ratioup.GetBinContent (km) != 0):
            eyh[km] = (1. / ratioup.GetBinContent (km) - 1)*ratiodata.GetBinContent (km)                                                                                                   
        else:  eyh[km] = 0
        if (ratiodown.GetBinContent (km) != 0):
            eyl[km] = (1 - 1. / ratiodown.GetBinContent (km))*ratiodata.GetBinContent (km) 
        else: 
            eyl[km] = 0.                                                                                                                        
        err = TGraphAsymmErrors(nvar, x, y, exl, exh, eyl, eyh)

    # make some stat errors
    dens1 = copy.deepcopy(hMC.Clone("bkgdens1"))
    dens2 = copy.deepcopy(hMC.Clone("bkgdens2"))
    eyls = array.array('f', range(0, hMC.GetNbinsX()+1))
    eyhs = array.array('f', range(0, hMC.GetNbinsX()+1))
    ratioups = copy.deepcopy(hMC.Clone("ratioups"))
    ratiodowns = copy.deepcopy(hMC.Clone("ratiodowns"))
    ymaxs = 2.                                                     
    
    for km in range(0, hMC.GetNbinsX()+1):
        contes1 =  hMC.GetBinError(km);      
        contes2 =  hMC.GetBinError(km);      
        dens1.SetBinContent (km, hMC.GetBinContent (km) + contes1);                                                                                                                           
        dens2.SetBinContent (km, hMC.GetBinContent (km) - contes2);                                                                                                                           
        ymaxs = hMC.GetBinContent(km) + contes1;                                                                                                                         
        eyls[km] = conte2;                                                                                                                                                           
        eyhs[km] = conte1;

        ratioups.Divide(dens1);                                           
        ratiodowns.Divide(dens2);                                             

        for km in range(0, ratiodata.GetNbinsX()+1):                                                       
            if (ratioups.GetBinContent (km) != 0):
                eyhs[km] = (1. / ratioups.GetBinContent (km) - 1)*ratiodata.GetBinContent (km)
            else:                                                                                       
                eyhs[km] = 0           
                                                            
            if (ratiodowns.GetBinContent (km) != 0):
                eyls[km] = (1 - 1. / ratiodowns.GetBinContent (km))*ratiodata.GetBinContent (km)
            else:                                                                                       
                eyls[km] = 0.                                                                            
       
    staterr = TGraphAsymmErrors(nvar, x, y, exl, exh, eyls, eyhs)



    # colors = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]
    # gray ['#B3B3B3', '#8C8C8C',   '#666666'    #D9D9D9', '#B3B3B3', '#8C8C8C']
    errtottot.SetFillColor (r.TColor.GetColor("#bd1f01")); #cyan not used
    errtottot.SetFillStyle (1001)

    # errtot.SetFillColor(r.TColor.GetColor("#964a8b"))
    errtot.SetFillColor(r.TColor.GetColor("#e76300"))
    errtot.SetFillColor(r.TColor.GetColor("#ffa90e"))
    errtot.SetFillColor(r.TColor.GetColor("#666666"))
    errtot.SetFillColor(r.TColor.GetColor("#8C8C8C"))
    # errtot.SetFillColor(r.kBlack)
    # errtot.SetFillStyle (2001) 
    # errtot.SetFillColor(0);
    # errtot.SetFillStyle(0);
    # errtot.SetLineWidth(2);

    # err.SetFillColor (r.TColor.GetColor("#3f90da")); #717581 3f90da
    err.SetFillColor (r.TColor.GetColor("#8C8C8C")); #717581 3f90d
    err.SetFillColor (r.TColor.GetColor("#B3B3B3")); #717581 3f90d
    # err.SetFillStyle (3244);   

    # staterr.SetFillColor (r.TColor.GetColor("#92dadd"));#gray
    staterr.SetFillColor (r.TColor.GetColor("#B3B3B3"));#gray
    staterr.SetFillColor (r.TColor.GetColor("#D9D9D9"));#gray
    # staterr.SetFillStyle (3004);   
    h_err= hMC.Clone("h_err")

    h_err.SetFillStyle(3004)
    h_err.SetFillColor(r.kBlack)
    h_err.SetMarkerSize(0)
    h_err.Draw("e2same0")
    pad2.cd()

    line = TLine(ratio.GetBinLowEdge(1), 1, ratio.GetBinLowEdge(ratio.GetNbinsX()+1), 1)
    line.SetLineColor(r.kRed)
    line.SetLineStyle(2)

    # for iB in range(1, ratio.GetNbinsX()+1):
    #   ratio.SetBinError(iB,hdata.GetBinError(iB))
    ratio.SetMarkerSize(1)
    ratio.Draw()

    print('will I do the errors????', doAllErrors, doSomeErrors)
    if doAllErrors:
        legratio2 = TLegend(0.1,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(3);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        # legratio2.AddEntry(errtottot, "JER+Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(errtot, "Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(err, "JES+Stat/Other","f");
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        errtottot.Draw("E2 same")
        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()


    if doSomeErrors:
        legratio2 = TLegend(0.135,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(3);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        # legratio2.AddEntry(errtottot, "JER+Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(errtot, "Uncl+JES+Stat/Other","f");
        legratio2.AddEntry(err, "JES+Stat/Other","f");
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        # errtottot.Draw("E2 same")

        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        # ratio.Draw("same");                                                      
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()





    if puppi: 
        legratio = TLegend(0.14,0.31,0.4,0.45);                                   
        legratio.SetFillColor(0);
        legratio.SetBorderSize(0);
        legratio.SetNColumns(2);
        legratio.AddEntry(err, "JES + Stat/Other","f");
        legratio.AddEntry(staterr, "Stat","f");                                  
        err.Draw("e2")
        staterr.Draw("2 same")
        legratio.Draw("same")
        line.Draw("same")
        ratio.Draw("same");      
    if statOnly:
        # legratio = TLegend(0.14,0.32,0.43,0.5);
        # legratio.SetFillColor(0);
        # legratio.SetBorderSize(0);
        # legratio.AddEntry(staterr, " ","f");                                  
        # errtottot.Draw("2 same")
        # staterr.Draw("2 same")
        # legratio.Draw("same")
        # line.Draw("same")
        # ratio.Draw("same");                                                      
        legratio2 = TLegend(0.45,0.8,0.9,0.9);
        legratio2.SetFillColor(0);
        legratio2.SetFillStyle(0);
        legratio2.SetBorderSize(0);
        legratio2.SetNColumns(4);
        legratio2.SetTextSize(0.065)
        legratio2.SetTextFont(42)
        legratio2.AddEntry(staterr, "Stat/Other","f");                                         
        ratio.Draw();                                                      
        errtottot.Draw("E2 same")
        errtot.Draw("E2 same")
        err.Draw("2 same")
        staterr.Draw("2 same")

        line.Draw("same")
        # ratio.Draw("same");                                                      
        ratio.Draw(" E1X0 same");                                                      
        legratio2.Draw("same")
        gPad.RedrawAxis()
       
    pad1.cd()
    legratio = TLegend(0.6,0.53,0.8,0.6);
    # legratio = TLegend(0.698,0.53,0.88,0.6);
    legratio.SetFillColor(r.kWhite);
    legratio.SetFillStyle(0)
    legratio.SetBorderSize(0)
    legratio.SetTextSize(0.045)
    legratio.SetTextFont(42)
    # legratio.AddEntry(errtottot, "Uncertainty","f");
    # legratio.Draw("same")
    # errtottot.Draw("hist same")
    # errtottot.Draw("2 same")
    self.banner(isData, lumi, log, events, isNVert, isSig1jet, run)
    for plotName in self.plotNames:
        path = 'plots/'+plotName
        self.ensurePath(path)
        self.myCanvas.SaveAs(path)

    self.myCanvas.SaveAs('./plots/test/paperv2/test.C')



   def save(self, legend, lumi, log,chisquare, value, title, option, integral, fromFit):

      events = "" 
      setUpAxis = 1 
      setLowAxis = 1 
      log = 1
      isNVert = 0
      puppi = 0
      isSig1jet = 0
      logx = 0
      if option == '':  
          events  = ''
          lumi  = 2017
      if option == 'nvert1':
          log = 0
          setLowAxis = 1
      if option == 'nvert':
          log = 0
          setUpAxis = 0
      if option == 'sig0':
          log =1
          events = 2
      if option == 'sig1':
          log =1
          events = 2
          isSig1jet = 1      
      if option == 'qt':
          log = 1        
          setUpAxis = 0
          setLowAxis = 0 
          events  =  0           
      if option == 'uParavsuPerp':
          log = 0        
      if option == 'met':
          log = 0        
      if option == 'qtgamma':
          log = 1        
          setUpAxis = 0           
          setLowAxis = 0          
          events  =  0            
      if option == 'legacy':
          setLowAxis = 0
          setUpAxis = 1
          log = 1         
          events = ''          
      if option == 'legacy2':
          setLowAxis = 0
          setUpAxis = 1
          log = 1         
          events = ''          
      if option == '4':
          setLowAxis = 0
          setUpAxis = 1
          log = 0         
          events = ''          
      if option == 'legacy3':    
          setLowAxis = 0
          setUpAxis = 1
          log = 1         
          events = ''          
      if option == 'legacy5':  
          setLowAxis = 0
          setUpAxis = 1
          log = 1         
          events = ''          
      if option == 'legacy6':  
          setLowAxis = 0
          setUpAxis = 1
          log = 1         
          events = ''          
      if option == 'comp':
          setLowAxis = 1
          setUpAxis = 1
          log = 1           
          events  = ''      
      if option == 'jet':
          setLowAxis = 1
          setUpAxis = 1
          log = 1           
          events  = ''      
      if option == 'rereco':      
          setLowAxis = 1
          setUpAxis = 1
          log = 1           
          logx = 1           
      if option == 'chs': 
          setLowAxis = 1
          setUpAxis = 1
          log = 0           
          logx = 0          
      if option == 'tailsE':    
          settailsAxis =1 
          lumi  = "Run E"       
          setLowAxis = 0
          events  = ''  
          log = 1        
      if option == 'tailsH':    
          settailsAxis =1 
          lumi  = "Run H"
          setLowAxis = 0
          events  = ''  
          log = 1               
      if option == 'tails':   
          settailsAxis =1 
          lumi  = "35.9"
          setLowAxis = 0
          events  = ''  
          log = 1            
      if option == 'tails05':    
          lumi  = ""
          events  = ''  
          log = 0            
      self.myCanvas.cd()
      if(log):
          self.myCanvas.GetPad(0).SetLogy(1)
      if(logx):
          self.myCanvas.GetPad(0).SetLogx(1)

      for i in range(0, len(self.histos)):
          self.histos[i].SetMinimum(0.001)
          if setLowAxis:
              self.histos[i].SetMinimum(0.01)
              print("doing this==============================================================", int(option))
              # self.histos[i].SetMaximum(10)
              # self.histos[i].SetMaximum(10)
              # self.histos[i].SetMaximum(int(option))
              # self.histos[i].SetMaximum(int(option)/800.)
              self.histos[i].SetMaximum(int(option)*100)
          if option == 'legacy2':
              self.histos[i].SetMinimum(0.00001)
              self.histos[i].SetMaximum(10.)          
              # self.histos[i].SetMaximum(5000000.)          
          if option == '4':
              self.histos[i].SetMinimum(0.)
              self.histos[i].SetMaximum(1000000)          
              # self.histos[i].SetMaximum(5000000.)     
          if option == 'legacy3':
              self.histos[i].SetMinimum(0.1)
              self.histos[i].SetMaximum(10.)          
          if option == 'legacy5':
              self.histos[i].SetMinimum(0.001)
              self.histos[i].SetMaximum(1.)     
          if option == 'legacy6':
              self.histos[i].SetMinimum(0.00001)
              self.histos[i].SetMaximum(0.5)    
          if option == 'tailsH':
              self.histos[i].SetMaximum(10)
              self.histos[i].SetMinimum(0.0001)
          if option == 'tailsE':
              self.histos[i].SetMaximum(10)
              self.histos[i].SetMinimum(0.0001)
          if option == 'tails':
              self.histos[i].SetMaximum(10)
              self.histos[i].SetMinimum(0.0001)
          if option == 'tails05':                  
              self.histos[i].SetMaximum(0.3)
              self.histos[i].SetMinimum(0)    
          if option == 'qt':               
              self.histos[i].SetMaximum(8572719)
              self.histos[i].SetMinimum(0.01)    
          if option == 'qtgamma':               
              self.histos[i].SetMaximum(50000000)
              self.histos[i].SetMinimum(1)    
          if option == 'legacy':
              self.histos[i].SetMinimum(0.00001)
              self.histos[i].SetMaximum(10.)          
          if option == 'jet':
              self.histos[i].SetMinimum(10)
              self.histos[i].SetMaximum(100000000.)          
          if option == 'uParavsuPerp':                           
              self.histos[i].SetMinimum(0)
              self.histos[i].SetMaximum(6000.)   
          if option == 'met':                           
              # self.histos[i].SetMinimum(0.1)
              self.histos[i].SetMinimum(0.001)
              self.histos[i].SetMaximum(10000.)   
              # self.histos[i].SetMaximum(1000000.)   

          if isNVert:
              self.histos[i].SetMaximum(10000000.)

          if not log :  self.histos[i].SetMaximum(self.histos[i].GetBinContent(1)*20)

          if(self.ToDraw[i] != 0):        
              self.histos[i].Draw(self.options[i])

      for band in self.bands:
          band.Draw('f')
  
      for line in self.lines:
          line.Draw()
  
      for arrow in self.arrows:
          arrow.Draw()
  
      for latex in self.latexs:
          lat = TLatex()
          lat.SetNDC()
          lat.SetTextSize(latex[-1])
          lat.SetTextFont(latex[-2])
          lat.DrawLatex(latex[0], latex[1], latex[2])
  
      if(legend):
          self.makeLegend(log)
          self.myLegend.Draw()

      self.banner2(lumi, chisquare, value , title, events, isNVert, isSig1jet, integral, fromFit)
      for plotName in self.plotNames:
          path = 'plots/'+plotName
          self.ensurePath(path)
          self.myCanvas.SaveAs(path)


