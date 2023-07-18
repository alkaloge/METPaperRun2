from ROOT import TGraphErrors
import sys


class collection:
    def __init__(self, bins, vname):
        self.bins  = bins
        self.vname = vname
        self.cen_mc, self.cen_mc_gr = 0, 0
        self.fwd_mc, self.fwd_mc_gr = 0, 0
        self.cen_da, self.cen_da_gr = 0, 0
        self.fwd_da, self.fwd_da_gr = 0, 0

    def getHisto(self, dataMC, eta):
        if   (dataMC, eta) == ('MC'  , 'central'): 
            return self.cen_mc
        elif (dataMC, eta) == ('MC'  , 'forward'): 
            return self.fwd_mc
        elif (dataMC, eta) == ('DATA', 'central'): 
            return self.cen_da
        elif (dataMC, eta) == ('DATA', 'forward'): 
            return self.fwd_da

    def getGraph(self, dataMC, eta):
        if   (dataMC, eta) == ('MC'  , 'central'): 
            return self.cen_mc_gr
        elif (dataMC, eta) == ('MC'  , 'forward'): 
            return self.fwd_mc_gr
        elif (dataMC, eta) == ('DATA', 'central'): 
            return self.cen_da_gr
        elif (dataMC, eta) == ('DATA', 'forward'): 
            return self.fwd_da_gr

    def setHisto(self, histo, dataMC, eta):
        if   (dataMC, eta) == ('MC'  , 'central'): 
            self.cen_mc = histo
            self.cen_mc_gr = TGraphErrors(histo)
        elif (dataMC, eta) == ('MC'  , 'forward'): 
            self.fwd_mc = histo
            self.fwd_mc_gr = TGraphErrors(histo)
        elif (dataMC, eta) == ('DATA', 'central'): 
            self.cen_da = histo
            self.cen_da_gr = TGraphErrors(histo)
        elif (dataMC, eta) == ('DATA', 'forward'): 
            self.fwd_da = histo
            self.fwd_da_gr = TGraphErrors(histo)
        else:
            print 'you are not calling setHisto correctly'

    def printValues(self):
        for _histo in [self.cen_mc, self.cen_da, self.fwd_mc, self.fwd_da]:
            if _histo == 0: continue
            if _histo in [self.cen_mc, self.cen_da]:
                eta = 'central'
            else:
                eta = 'forward'
            for _bin in range(1,_histo.GetNbinsX()+1):
                print '%-6s in [%.0f, %.0f] in %s: %.3f +- %.3f' %( self.vname,
                      _histo.GetXaxis().GetBinLowEdge(_bin),
                      _histo.GetXaxis().GetBinUpEdge (_bin),
                      eta,
                      _histo.GetBinContent(_bin),
                      _histo.GetBinError(_bin))

    def saveInFile(self, pattern, systErr, findBin = 0):
        print 'writing calculated values into file...'
        filename = 'ingredients.dat'
        f = open(filename, 'r')
        lines = f.readlines()
        newlines = []
        for line in lines:
            appended = False
            for t in ['MC', 'DATA'] if self.cen_da else ['MC']:
                if all(s in line for s in pattern+[t]):
                    newlines.append('%-6s \t %-15s %-6s \t %.4f \t %.4f \t %-6s \t %.4f \t %.4f \t %-6s\n' %(
                            line.split()[0], line.split()[1], t,
                            self.getHisto(t, 'central').GetBinContent(1 if not findBin else self.getHisto(t, 'central').FindBin(findBin)),
                            self.getHisto(t, 'central').GetBinError  (1 if not findBin else self.getHisto(t, 'central').FindBin(findBin)),
                            str(systErr),
                            self.getHisto(t, 'forward').GetBinContent(1 if not findBin else self.getHisto(t, 'forward').FindBin(findBin)),
                            self.getHisto(t, 'forward').GetBinError  (1 if not findBin else self.getHisto(t, 'forward').FindBin(findBin)),
                            str(systErr) ))
                    appended = True
    
            if not appended:
                newlines.append(line)
        f.close()
        g = open(filename, 'w')
        g.writelines(newlines)

class region():
    def __init__(self, name, cuts, rvars, dependence, varname, bins,  doData):
        self.name      = name
        self.cuts      = cuts
        self.rvars     = rvars
        self.dependence = dependence
        self.varname   = varname
        self.bins      = bins
        self.doData    = doData
        #if len(rvars) is not len(bins):
        #    print 'length of variables and bins has to be equal'
        #    sys.exit('exiting!')
        self.setVariables()

    def setVariables(self):
        for v in self.rvars:

            
            if v == 'metPuppi_pt':
                self.metPuppi_pt   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_pt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_pt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_pt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_pt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_pt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_pt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_pt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_pt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_pt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_pt_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_pt_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'metPuppi_rawPt':
                self.metPuppi_rawPt   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'met_sig':
                self.met_sig   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_zg = collection(self.bins[self.rvars.index(v)], v)  
            if v == 'met_sig_1jet':
                self.met_sig_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sig_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sig_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sig_1jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'metPuppi_sig':
                self.metPuppi_sig   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_sig_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_sig_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_sig_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_sig_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_sig_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_sig_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_sig_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_sig_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_sig_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_sig_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_sig_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_x':
                self.met_x   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_y':
                self.met_y   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_x_0jet':
                self.met_x_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_0jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_0jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_y_0jet':
                self.met_y_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_0jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_0jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_x_1jet':                                                            
                self.met_x_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_x_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_x_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_x_1jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_y_1jet':
                self.met_y_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_y_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_y_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_y_1jet_da = collection(self.bins[self.rvars.index(v)], v)         
            
            if v == 'MET_pt'or v=='MET_T1_pt' :
                self.MET_T1_pt   = collection(self.bins[self.rvars.index(v)], v)
                #self.MET_T1_pt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_T1_pt_da = collection(self.bins[self.rvars.index(v)], v)    
                '''
                self.MET_pt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_da = collection(self.bins[self.rvars.index(v)], v)         
                '''


            if v == 'met_sumEt':
                self.met_sumEt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_zg = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'MET_pt_0jet':                                                            
                self.MET_pt_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_0jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_0jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_sumEt_0jet':
                self.met_sumEt_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_0jet_zg = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'MET_pt_1jet':
                self.MET_pt_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.MET_pt_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.MET_pt_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.MET_pt_1jet_da = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_sumEt_1jet':
                self.met_sumEt_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_sumEt_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_sumEt_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_sumEt_1jet_zg = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'met_rawSumEt':
                self.met_rawSumEt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawSumEt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawSumEt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawSumEt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawSumEt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawSumEt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawSumEt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawSumEt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawSumEt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawSumEt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawSumEt_zg = collection(self.bins[self.rvars.index(v)], v)        
            if v == 'met_rawPt_0jet':
                self.met_rawPt_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawpt_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawpt_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawpt_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_0jet_zg = collection(self.bins[self.rvars.index(v)], v)             
            if v == 'met_rawPt_1jet':
                self.met_rawPt_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawPt_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawPt_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawPt_1jet_zg = collection(self.bins[self.rvars.index(v)], v)             
            if v == 'met_rawPt':
                self.met_rawPt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawPt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawPt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.met_rawpt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawpt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_rawpt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_rawpt_zg = collection(self.bins[self.rvars.index(v)], v)                
            if v == 'metPuppi_rawPt':                                                                      
                self.metPuppi_rawPt   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_zg = collection(self.bins[self.rvars.index(v)], v)              
            if v == 'metPuppi_rawPt_0jet':                                                              
                self.metPuppi_rawPt_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_0jet_zg = collection(self.bins[self.rvars.index(v)], v)             
            if v == 'metPuppi_rawPt_1jet':                                                               
                self.metPuppi_rawPt_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_rawPt_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_rawPt_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.metPuppi_rawPt_1jet_zg = collection(self.bins[self.rvars.index(v)], v)             
            if v == 'lep_eta1':                                                       
                self.lep_eta1   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_eta1_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_eta1_da = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_eta1_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_eta1_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'lep_eta2':                                                      
                self.lep_eta2   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_eta2_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_eta2_da = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_eta2_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_eta2_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'zll_pt':
                self.zll_pt   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_pt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_pt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_pt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_pt_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'zll_phi':
                self.zll_phi   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_phi_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_phi_da = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_phi_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_phi_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'met_phi':
                self.met_phi   = collection(self.bins[self.rvars.index(v)], v)
                self.met_phi_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_phi_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_phi_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_phi_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'lep_pt':
                self.lep_pt   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_pt_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.lep_pt_da = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_pt_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.lep_pt_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'chi2':
                self.chi2   = collection(self.bins[self.rvars.index(v)], v)
                self.chi2_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.chi2_da = collection(self.bins[self.rvars.index(v)], v)    
                self.chi2_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.chi2_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'chi2_1jet':
                self.chi2_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.chi2_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.chi2_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.chi2_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.chi2_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'zll_eta':
                self.zll_eta   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_eta_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_eta_da = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_eta_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_eta_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'zll_mass':
                self.zll_mass   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_mass_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.zll_mass_da = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_mass_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.zll_mass_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'nVert':
                self.nVert   = collection(self.bins[self.rvars.index(v)], v)
                self.nVert_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.nVert_da = collection(self.bins[self.rvars.index(v)], v)    
                self.nVert_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.nVert_ewk = collection(self.bins[self.rvars.index(v)], v)    
                self.nVert_wg = collection(self.bins[self.rvars.index(v)], v) 
                self.nVert_zg = collection(self.bins[self.rvars.index(v)], v) 
                self.nVert_wj = collection(self.bins[self.rvars.index(v)], v) 
                self.nVert_ttg = collection(self.bins[self.rvars.index(v)], v) 
                self.nVert_qcd = collection(self.bins[self.rvars.index(v)], v) 
                self.nVert_gjets = collection(self.bins[self.rvars.index(v)], v) 
            if v == 'metPuppi_uPerp':
                self.metPuppi_uPerp   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_uPerp_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_uPerp_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_uPerp_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_uPerp_ewk = collection(self.bins[self.rvars.index(v)], v)    
            if v == 'metPuppi_uPara':
                self.metPuppi_uPara     = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_uPara_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.metPuppi_uPara_da = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_uPara_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.metPuppi_uPara_ewk = collection(self.bins[self.rvars.index(v)], v)         
            if v == 'met_uPara':
                self.met_uPara     = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_ewk = collection(self.bins[self.rvars.index(v)], v)         
                self.met_uPara_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_wj = collection(self.bins[self.rvars.index(v)], v)                 
            if v == 'met_uPara_0jet':
                self.met_uPara_0jet     = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_0jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_0jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_0jet_ewk = collection(self.bins[self.rvars.index(v)], v)         
                self.met_uPara_0jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_0jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_0jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_0jet_wj = collection(self.bins[self.rvars.index(v)], v)               
            if v == 'met_uPara_1jet':
                self.met_uPara_1jet     = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_1jet_da = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_1jet_tt = collection(self.bins[self.rvars.index(v)], v)    
                self.met_uPara_1jet_ewk = collection(self.bins[self.rvars.index(v)], v)         
                self.met_uPara_1jet_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_1jet_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPara_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPara_1jet_wj = collection(self.bins[self.rvars.index(v)], v)               
            if v == 'met_uPerp':                                                                                                 
                self.met_uPerp   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_da   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_tt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_ewk   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_qcd = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'met_uPerp_0jet':                                                          
                self.met_uPerp_0jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_0jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_0jet_da   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_0jet_tt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_0jet_ewk   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_0jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_0jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_0jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_0jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_0jet_qcd = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'met_uPerp_1jet':                                                         
                self.met_uPerp_1jet   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_1jet_dy   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_1jet_da   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_1jet_tt   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_1jet_ewk   = collection(self.bins[self.rvars.index(v)], v)
                self.met_uPerp_1jet_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_1jet_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_1jet_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_1jet_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.met_uPerp_1jet_qcd = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'metPuppi_pt_0jet':                                                
                self.metPuppi_pt_0jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metPuppi_pt_1jet':                                                
                self.metPuppi_pt_1jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metPuppi_sig_1jet':                                                                                                 
                self.metPuppi_sig_1jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPerp':                                                                                                 
                self.metRaw_uPerp   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPerp_0jet':                                                
                self.metRaw_uPerp_0jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPerp_1jet':                                                 
                self.metRaw_uPerp_1jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPara':                                                                                                 
                self.metRaw_uPara   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPara_0jet':                                                                                                 
                self.metRaw_uPara_0jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metRaw_uPara_1jet':                                                                                                 
                self.metRaw_uPara_1jet   = collection(self.bins[self.rvars.index(v)], v)
            if v == 'metPuppi_uPara':                                                                               
                self.metPuppi_uPara   = collection(self.bins[self.rvars.index(v)], v)                               
            if v == 'metPuppi_uPara_0jet':                                                       
                self.metPuppi_uPara_0jet   = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'metPuppi_uPara_1jet':                                                       
                self.metPuppi_uPara_1jet   = collection(self.bins[self.rvars.index(v)], v)       
            if v == 'metPuppi_uPerp':                                                                               
                self.metPuppi_uPerp   = collection(self.bins[self.rvars.index(v)], v)                               
            if v == 'metPuppi_uPerp_0jet':                                                                               
                self.metPuppi_uPerp_0jet   = collection(self.bins[self.rvars.index(v)], v)                               
            if v == 'metPuppi_uPerp_1jet':                                                                               
                self.metPuppi_uPerp_1jet   = collection(self.bins[self.rvars.index(v)], v)                               
            if v == 'metPuppiRaw_uPara':                                                                              
                self.metPuppiRaw_uPara   = collection(self.bins[self.rvars.index(v)], v)                              
            if v == 'metPuppiRaw_uPara_0jet':                                                                              
                self.metPuppiRaw_uPara_0jet   = collection(self.bins[self.rvars.index(v)], v)                              
            if v == 'metPuppiRaw_uPara_1jet':                                                                              
                self.metPuppiRaw_uPara_1jet   = collection(self.bins[self.rvars.index(v)], v)                              
            if v == 'metPuppiRaw_uPerp':                                                                              
                self.metPuppiRaw_uPerp   = collection(self.bins[self.rvars.index(v)], v)                              
            if v == 'metPuppiRaw_uPerp_0jet':                                                                              
                self.metPuppiRaw_uPerp_0jet   = collection(self.bins[self.rvars.index(v)], v)                              
            if v == 'metPuppiRaw_uPerp_1jet':                                                                              
                self.metPuppiRaw_uPerp_1jet   = collection(self.bins[self.rvars.index(v)], v)                              
           
           
            if v == 'gamma_pt':
                self.gamma_pt   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_pt_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_pt_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_pt_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_pt_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_pt_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_pt_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_pt_da = collection(self.bins[self.rvars.index(v)], v)      
            if v == 'gamma_r9':
                self.gamma_r9   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_r9_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_r9_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_r9_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_r9_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_r9_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_r9_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_r9_da = collection(self.bins[self.rvars.index(v)], v)      
            
            if v == 'gamma_sigmaIetaIeta':
                self.gamma_sigmaIetaIeta   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_sigmaIetaIeta_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_sigmaIetaIeta_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_sigmaIetaIeta_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_sigmaIetaIeta_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_sigmaIetaIeta_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_sigmaIetaIeta_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_sigmaIetaIeta_da = collection(self.bins[self.rvars.index(v)], v)      
            if v == 'gamma_hOverE':
                self.gamma_hOverE   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_hOverE_qcd   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_hOverE_gjets   = collection(self.bins[self.rvars.index(v)], v)
                self.gamma_hOverE_wg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_hOverE_zg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_hOverE_wj = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_hOverE_ttg = collection(self.bins[self.rvars.index(v)], v)  
                self.gamma_hOverE_da = collection(self.bins[self.rvars.index(v)], v)      


