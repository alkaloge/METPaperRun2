import ROOT
import random

ROOT.gROOT.SetBatch(True)  # Prevents graphics from being displayed
# Create a canvas

# Create a canvas
canvas = ROOT.TCanvas("canvas", "Ratio Plot Example", 800, 600)

# Create THStack and add MC histograms
stack = ROOT.THStack("stack", "MC Stack")

# Create random MC histograms (processes)
random.seed(42)  # For reproducibility
for _ in range(2):
    mc_hist = ROOT.TH1F("mc_hist{}".format(_), "MC Process {}".format(_), 100, 0, 100)
    for bin in range(1, mc_hist.GetNbinsX() + 1):
        mc_hist.SetBinContent(bin, random.uniform(0, 1))
    stack.Add(mc_hist)

# Create data histogram
data_hist = ROOT.TH1F("data_hist", "Data Histogram", 100, 0, 100)
for bin in range(1, data_hist.GetNbinsX() + 1):
    data_hist.SetBinContent(bin, random.uniform(0, 1))

# Create systematic uncertainty histograms for MC
mc_syst_jer_up = ROOT.TH1F("mc_syst_jer_up", "MC JER Syst Up", 100, 0, 100)
mc_syst_jer_down = ROOT.TH1F("mc_syst_jer_down", "MC JER Syst Down", 100, 0, 100)
mc_syst_jes_up = ROOT.TH1F("mc_syst_jes_up", "MC JES Syst Up", 100, 0, 100)
mc_syst_jes_down = ROOT.TH1F("mc_syst_jes_down", "MC JES Syst Down", 100, 0, 100)
mc_syst_unclustered_up = ROOT.TH1F("mc_syst_unclustered_up", "MC Unclustered Syst Up", 100, 0, 100)
mc_syst_unclustered_down = ROOT.TH1F("mc_syst_unclustered_down", "MC Unclustered Syst Down", 100, 0, 100)

# Create a TH1 for the ratio (data/MC)
ratio_hist = data_hist.Clone("ratio_hist")
ratio_hist.Divide(stack.GetStack().Last())  # Divide by the total MC stack

# Create a TH1 for the systematic uncertainty band
syst_uncertainty_band = stack.GetStack().Last().Clone("syst_uncertainty_band")
syst_uncertainty_band.Reset()

# Fill the systematic uncertainty band with the maximum deviations
for bin in range(1, stack.GetStack().Last().GetNbinsX() + 1):
    max_up_deviation = max(
        mc_syst_jer_up.GetBinContent(bin),
        mc_syst_jes_up.GetBinContent(bin),
        mc_syst_unclustered_up.GetBinContent(bin)
    )
    max_down_deviation = max(
        mc_syst_jer_down.GetBinContent(bin),
        mc_syst_jes_down.GetBinContent(bin),
        mc_syst_unclustered_down.GetBinContent(bin)
    )
    syst_uncertainty_band.SetBinContent(bin, max(max_up_deviation, max_down_deviation))

# Customize the appearance of the histograms
stack.SetTitle("MC Stack;X-axis;Y-axis")
data_hist.SetMarkerStyle(ROOT.kFullCircle)
data_hist.SetMarkerSize(0.8)
data_hist.SetLineColor(ROOT.kBlack)
data_hist.SetMarkerColor(ROOT.kBlack)

# Draw the MC stack
stack.Draw("hist")
data_hist.Draw("sameE1")


# Customize the uncertainty band appearance
syst_uncertainty_band.SetFillColorAlpha(ROOT.kBlue, 0.3)  # Semi-transparent blue fill
syst_uncertainty_band.SetFillStyle(1001)  # Solid fill style
syst_uncertainty_band.Draw("e2same")

# Draw a line at ratio 1
line_at_one = ROOT.TLine(0, 1, 1, 1)
line_at_one.SetLineColor(ROOT.kRed)
line_at_one.SetLineWidth(2)
line_at_one.Draw("same")

# Draw the ratio as dots (markers)
ratio_hist.SetMarkerStyle(ROOT.kFullCircle)
ratio_hist.SetMarkerSize(0.8)
ratio_hist.SetMarkerColor(ROOT.kBlack)
ratio_hist.Draw("sameP")

# Add a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(data_hist, "Data", "lep")
legend.AddEntry(stack.GetStack().Last(), "Total MC", "f")
legend.AddEntry(syst_uncertainty_band, "Syst. Uncertainty", "f")
legend.Draw()

# Show the canvas
canvas.Draw()

# Save the plot as an image file (optional)
canvas.SaveAs("ratio_band_plot.png")


# Keep the program running to view the plot (close the plot window to exit)
#ROOT.gApplication.Run()
