import sys
import ROOT
from ROOT import gROOT, TLine, gPad
ROOT.gStyle.SetOptStat(0)

ROOT.gROOT.SetBatch(True)
gROOT.ProcessLine('.L include/tdrstyle.C')
gROOT.SetBatch(1)
ROOT.setTDRStyle()


# Check if the input file is given
if len(sys.argv) < 2:
    print "Please provide the input file name as an argument."
    sys.exit(1)

# Open the ROOT file
try:
    input_file = ROOT.TFile(sys.argv[1])
except Exception as ex:
    print "Failed to open file:", ex
    sys.exit(1)

processes = ["ew", "dy", "dynlo", "top", "data"]
processes = ["ew", "dy",  "top", "data"]
systematics = ["JES", "JER", "Unclustered"]

# Create a dictionary to store the results
results = {}
for proc in processes:
    results[proc] = {"Main": 0.0}
    for syst in systematics:
        results[proc]["{}_up".format(syst)] = 0.0
        results[proc]["{}_down".format(syst)] = 0.0

hist = input_file.Get("histo_data")
results['data']["Main"] = hist.GetSumOfWeights()

varr='METCorGood_T1_pt'
varr='u_perp_METCorGood_T1'

# Loop over all histograms in the ROOT file
for proc in processes:
    if "data" in proc.lower():
        # Only central value for data
        results[proc]["Main"] = input_file.Get("histo_data").GetSumOfWeights()
    else:
        # Get central value for the process
        print "histo_{0:s}_{1:s}".format(proc,varr)
        main = input_file.Get("histo_{0:s}_{1:s}".format(proc,varr)).GetSumOfWeights()
        results[proc]["Main"] = main
        # Get systematics up/down values for the process
        for syst in systematics:
            hist_up = input_file.Get("histo_{0:s}_{1:s}{2:s}Up".format(proc, varr,syst))
            hist_down = input_file.Get("histo_{0:s}_{1:s}{2:s}Down".format(proc, varr,syst))
            if hist_up and hist_down:
                up = hist_up.GetSumOfWeights()
                down = hist_down.GetSumOfWeights()
                results[proc]["{}_up".format(syst)] = up 
                results[proc]["{}_down".format(syst)] = down 

print("Process\tMain\tJES_up\tJES_down\tJER_up\tJER_down\tUnclustered_up\tUnclustered_down")
for proc in processes:
    values = [round(results[proc]["Main"], 2)]
    for syst in systematics:
        values.append(round(results[proc]["{}_up".format(syst)], 2))
        values.append(round(results[proc]["{}_down".format(syst)], 2))
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(proc, *values))




# Read the histograms
hist_mc_ew = input_file.Get("histo_ew_{0:s}".format(varr))
hist_mc_dy = input_file.Get("histo_dy_{0:s}".format(varr))
#hist_mc_dynlo = input_file.Get("histo_dynlo_METCorGood_T1Smear_pt")
hist_mc_top = input_file.Get("histo_top_{0:s}".format(varr))
data_hist = input_file.Get("histo_data")

# Number of bins, x-axis min and max for ratio plot
n_bins = data_hist.GetNbinsX()
x_min = data_hist.GetXaxis().GetXmin()
x_max = data_hist.GetXaxis().GetXmax()



# Create the main canvas
canvas = ROOT.TCanvas("canvas", "MC vs Data and Ratio Plot", 800, 800)

# Divide the canvas into two pads
pad1 = ROOT.TPad("pad1", "Data vs MC", 0, 0.3, 1, 1.0)
pad2 = ROOT.TPad("pad2", "Ratio plot", 0, 0.05, 1, 0.3)

# Set pad margins
pad1.SetBottomMargin(0)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.25)

pad1.SetLogy()
pad1.Draw()
pad2.Draw()


# Draw MC and Data histograms in the top pad
pad1.cd()
stack = ROOT.THStack("stack", "MC vs Data")

# Set different colors for the MC processes
hist_mc_ew.SetFillColor(ROOT.kRed)
hist_mc_dy.SetFillColor(ROOT.kBlue)
#hist_mc_dynlo.SetFillColor(ROOT.kGreen)
hist_mc_top.SetFillColor(ROOT.kYellow)

stack.Add(hist_mc_ew)
stack.Add(hist_mc_dy)
#stack.Add(hist_mc_dynlo)
stack.Add(hist_mc_top)

stack.Draw("HIST")
data_hist.Draw("SAME PE")

# Draw legends
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(data_hist, "Data", "PE")
legend.AddEntry(hist_mc_ew, "Electroweak", "F")
legend.AddEntry(hist_mc_dy, "Drell-Yan", "F")
#legend.AddEntry(hist_mc_dynlo, "Drell-Yan NLO", "F")
legend.AddEntry(hist_mc_top, "Top", "F")
legend.Draw()


# Calculate the sum of all MC histograms
mc_sum = hist_mc_ew.Clone("mc_sum")
mc_sum.Add(hist_mc_dy)
mc_sum.Add(hist_mc_top)


# Calculate the ratio plot in the bottom pad
pad2.cd()
ratio_hist = data_hist.Clone("ratio_hist")
ratio_hist.Divide(mc_sum)
# Set the y-axis range for the ratio pad
ratio_hist.SetMinimum(0.5)
ratio_hist.SetMaximum(2)



# Calculate uncertainty bands
stat_uncertainty = ROOT.TGraphAsymmErrors(ratio_hist)

# Add JES, Unclustered, and JER uncertainties

jes_band = ROOT.TGraphAsymmErrors()
unclustered_band = ROOT.TGraphAsymmErrors()
jer_band = ROOT.TGraphAsymmErrors()
total_uncertainty_band = ROOT.TGraphAsymmErrors()


for i in range(ratio_hist.GetNbinsX()):
    x = ratio_hist.GetBinCenter(i + 1)
    y = ratio_hist.GetBinContent(i + 1)

    stat_error = stat_uncertainty.GetErrorY(i)
    
    jes_uncertainty = 0.0
    unclustered_uncertainty = 0.0
    jer_uncertainty = 0.0

    for proc in processes[:-1]:  # exclude 'data'
        jes_uncertainty += (results[proc]['JES_up'] - results[proc]['JES_down'])**2
        unclustered_uncertainty += (results[proc]['Unclustered_up'] - results[proc]['Unclustered_down'])**2
        jer_uncertainty += (results[proc]['JER_up'] - results[proc]['JER_down'])**2

    jes_uncertainty = abs(jes_uncertainty)**0.5
    unclustered_uncertainty = abs(unclustered_uncertainty)**0.5
    jer_uncertainty = abs(jer_uncertainty)**0.5

    total_uncertainty = (stat_error**2 + jes_uncertainty**2 + unclustered_uncertainty**2 + jer_uncertainty**2)**0.5

    jes_band.SetPoint(i, x, y)
    jes_band.SetPointError(i, 0, 0, jes_uncertainty, jes_uncertainty)
    
    unclustered_band.SetPoint(i, x, y)
    unclustered_band.SetPointError(i, 0, 0, unclustered_uncertainty, unclustered_uncertainty)
    
    jer_band.SetPoint(i, x, y)
    jer_band.SetPointError(i, 0, 0, jer_uncertainty, jer_uncertainty)
    
    total_uncertainty_band.SetPoint(i, x, y)
    total_uncertainty_band.SetPointError(i, 0, 0, total_uncertainty, total_uncertainty)

# Set uncertainty band styles
stat_uncertainty.SetFillColor(ROOT.kGray)
stat_uncertainty.SetFillStyle(1001)

jes_band.SetFillColor(ROOT.kRed)
jes_band.SetFillStyle(3001)

unclustered_band.SetFillColor(ROOT.kBlue)
unclustered_band.SetFillStyle(3002)

jer_band.SetFillColor(ROOT.kGreen)
jer_band.SetFillStyle(3003)

total_uncertainty_band.SetFillColor(ROOT.kOrange)
total_uncertainty_band.SetFillStyle(3004)

line = TLine(ratio_hist.GetBinLowEdge(1), 1, ratio_hist.GetBinLowEdge(ratio_hist.GetNbinsX()+1), 1)
line.SetLineColor(ROOT.kRed)
#ratio_hist.Draw("PE")
ratio_hist.Draw()
line.Draw("same")
ratio_hist.Draw("same")
canvas.Update()

stat_uncertainty.Draw("2 same")
canvas.Update()

jes_band.Draw("2 same")
canvas.Update()

unclustered_band.Draw("2 same")
canvas.Update()

jer_band.Draw("2 same")
canvas.Update()

total_uncertainty_band.Draw("2 same")
gPad.RedrawAxis()
canvas.Update()

canvas.SaveAs("mc_vs_data_ratio_plot.pdf")





