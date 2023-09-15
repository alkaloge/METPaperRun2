import sys
from ROOT import TCanvas, TLine, TGraphErrors, TH1F, TLegend, TLatex, gROOT
from array import array

def graph_scale(year):
    # SetTDRStyle()
    gROOT.SetBatch(True)

    c1 = TCanvas("c1", "", 0, 0, 700, 800)
    c1.Range(0, 0, 1, 1)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetBorderSize(2)
    c1.SetFrameBorderMode(0)
    c1.Draw()

    line = TLine(0, 1., 500, 1.)
    line.SetLineColor(1)
    line.SetLineWidth(1)
    line.SetLineStyle(3)

    f1 = open("raw_{}_dy_jgeq0_vspt.txt".format(year), "r")
    f2 = open("t1_{}_dy_jgeq0_vspt.txt".format(year), "r")
    f2s = open("t1smear_{}_dy_jgeq0_vspt.txt".format(year), "r")
    f3 = open("puppi_{}_dy_jgeq0_vspt.txt".format(year), "r")


    # f1 = open("raw_2018_dy_vspt.txt", "r")
    # f2 = open("t1_2018_dy_vspt.txt", "r")
    # f3 = open("puppi_2018_dy_vspt.txt", "r")

    f1d = open("raw_{}_alldata_vspt.txt".format(year), "r")
    f2d = open("t1_{}_alldata_vspt.txt".format(year), "r")
    f3d = open("puppi_{}_alldata_vspt.txt".format(year), "r")

    # f4 = open("scale_data_EGamma_2018D.txt", "r")

    bins = [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.]
    binnum = len(bins) - 1

    h1 = TH1F("h1", "h1", binnum, array('d', bins))
    h2 = TH1F("h2", "h2", binnum, array('d', bins))
    h2s = TH1F("h2s", "h2s", binnum, array('d', bins))
    h3 = TH1F("h3", "h3", binnum, array('d', bins))
    h4 = TH1F("h4", "h4", binnum, array('d', bins))
    h1d = TH1F("h1d", "h1d", binnum, array('d', bins))
    h2d = TH1F("h2d", "h2d", binnum, array('d', bins))
    h3d = TH1F("h3d", "h3d", binnum, array('d', bins))
    h4d = TH1F("h4d", "h4d", binnum, array('d', bins))

    for i in range(binnum + 1):

        yvalue1d, yerr1d, yvalue2d, yerr2d, yvalue3d, yerr3d = 0., 0., 0., 0., 0., 0.

        s1, yvalue1, yerr1, yvalue2, yerr2, yvalue3, yerr3 = f1.readline().split()
        h1.SetBinContent(i + 1, float(yvalue1))
        h1.SetBinError(i + 1, float(yerr1))

        s1, yvalue1d, yerr1d, yvalue2d, yerr2d, yvalue3d, yerr3d = f1d.readline().split()
        h1d.SetBinContent(i + 1, float(yvalue1d))
        h1d.SetBinError(i + 1, float(yerr1d))

        print(s1, yvalue1, yerr1, yvalue1d, yerr1d)

        s1, yvalue1, yerr1, yvalue2, yerr2, yvalue3, yerr3 = f2.readline().split()
        h2.SetBinContent(i + 1, float(yvalue1))
        h2.SetBinError(i + 1, float(yerr1))

        s1, yvalue1, yerr1, yvalue2, yerr2, yvalue3, yerr3 = f2s.readline().split()
        h2s.SetBinContent(i + 1, float(yvalue1))
        h2s.SetBinError(i + 1, float(yerr1))

        s1, yvalue1d, yerr1d, yvalue2d, yerr2d, yvalue3d, yerr3d = f2d.readline().split()
        h2d.SetBinContent(i + 1, float(yvalue1d))
        h2d.SetBinError(i + 1, float(yerr1d))

        s1, yvalue1, yerr1, yvalue2, yerr2, yvalue3, yerr3 = f3.readline().split()
        h3.SetBinContent(i + 1, float(yvalue1))
        h3.SetBinError(i + 1, float(yerr1))

        s1, yvalue1d, yerr1d, yvalue2d, yerr2d, yvalue3d, yerr3d = f3d.readline().split()
        h3d.SetBinContent(i + 1, float(yvalue1d))
        h3d.SetBinError(i + 1, float(yerr1d))
    print 'check1'

    gr1 = TGraphErrors(h1)
    gr2 = TGraphErrors(h2)
    gr2s = TGraphErrors(h2s)
    gr3 = TGraphErrors(h3)
    gr1d = TGraphErrors(h1d)
    gr2d = TGraphErrors(h2d)
    gr3d = TGraphErrors(h3d)

    gr1.SetTitle("")
    gr1.SetMarkerStyle(8)
    gr1.SetMarkerSize(0.8)
    gr1.SetMarkerColor(2)
    gr1.SetLineColor(2)
    gr1.SetLineWidth(2)

    gr1d.SetTitle("")
    gr1d.SetMarkerStyle(9)
    gr1d.SetMarkerSize(0.8)
    gr1d.SetMarkerColor(2)
    gr1d.SetLineColor(2)
    gr1d.SetLineWidth(2)
    gr1d.SetLineStyle(2)

    gr1.GetXaxis().SetTitle("q_{T} [GeV]")
    gr1.GetXaxis().SetRangeUser(0, 500)
    gr1.GetXaxis().SetTitleSize(0.04)

    gr1.GetYaxis().SetTitle("- <u_{||}>/<q_{T}>")
    gr1.GetYaxis().SetRangeUser(0., 1.2)
    gr1.GetYaxis().SetTitleSize(0.04)
    gr1.GetYaxis().SetTitleOffset(1.2)

    gr2.SetMarkerStyle(8)
    gr2.SetMarkerSize(0.8)
    gr2.SetMarkerColor(4)
    gr2.SetLineColor(4)
    gr2.SetLineWidth(2)

    gr2s.SetMarkerStyle(8)
    gr2s.SetMarkerSize(0.8)
    gr2s.SetMarkerColor(6)
    gr2s.SetLineColor(6)
    gr2s.SetLineWidth(2)

    gr3.SetMarkerStyle(8)
    gr3.SetMarkerSize(0.8)
    gr3.SetMarkerColor(3)
    gr3.SetLineColor(3)
    gr3.SetLineWidth(2)

    gr2d.SetMarkerStyle(9)
    gr2d.SetMarkerSize(0.8)
    gr2d.SetMarkerColor(4)
    gr2d.SetLineColor(4)
    gr2d.SetLineWidth(2)
    gr2d.SetLineStyle(2)

    gr3d.SetMarkerStyle(9)
    gr3d.SetMarkerSize(0.8)
    gr3d.SetMarkerColor(3)
    gr3d.SetLineColor(3)
    gr3d.SetLineWidth(2)
    gr3d.SetLineStyle(2)

    gr1.Draw("apz")
    gr2.Draw("pez same")
    gr2s.Draw("pez same")
    gr3.Draw("pez same")
    gr1d.Draw("pez same")
    gr2d.Draw("pez same")
    gr3d.Draw("pez same")

    line.Draw("same")


    print 'check1'
    legend1 = TLegend(0.65, 0.4, 0.85, 0.65)
    legend1.SetTextFont(42)
    legend1.SetLineColor(0)
    legend1.SetTextSize(0.04)
    legend1.SetFillColor(0)
    legend1.AddEntry(gr1, "raw MC", "lp")
    legend1.AddEntry(gr2, "T1 MC", "lp")
    legend1.AddEntry(gr2s, "T1Smear MC", "lp")
    legend1.AddEntry(gr3, "Puppi MC", "lp")
    legend1.AddEntry(gr1d, "raw Data", "lp")
    legend1.AddEntry(gr2d, "T1 Data", "lp")
    legend1.AddEntry(gr3d, "Puppi Data", "lp")
    legend1.Draw("same")

    t2a = TLatex(0.5, 0.9, " #bf{CMS} #it{Preliminary}          59.7 fb^{-1} (13 TeV, 2016) ")
    t2a.SetNDC()
    t2a.SetTextFont(42)
    t2a.SetTextSize(0.04)
    t2a.SetTextAlign(20)
    t2a.Draw("same")

    c1.SaveAs("scale_{0}_geq0_dy_MuMu.pdf".format(year))



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the year as a command-line argument.")
    else:
        year = sys.argv[1]
        graph_scale(year)







