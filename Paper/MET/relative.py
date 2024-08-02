

import ROOT
ROOT.gROOT.SetBatch(True)  # Prevents graphics from being displayed
# Open the ROOT file containing histograms
input_file = ROOT.TFile("plotS_2018_njetsgt0_nbtagl_cutbased_varbins_hitslt1_METCorGood_T1Smear_pt_Gjets.root", "READ")


# Create a canvas
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

canvas.cd()

# Create a THStack and add histograms from the file to it
stack = ROOT.THStack("stack", "Stacked Histograms")

# List of histogram names
histogram_names = [
    "histo_ewknlo_METCorGood_T1Smear_pt",
    "histo_ew_METCorGood_T1Smear_pt",
    "histo_gjets_METCorGood_T1Smear_pt",
    "histo_qcdmg_METCorGood_T1Smear_pt",
    "histo_tx_METCorGood_T1Smear_pt",
    # Add more histogram names as needed
]

histograms = []


histograms = []

# Loop through the list of histogram names and add them to the stack
for hist_name in histogram_names:
    hist = input_file.Get(hist_name)
    if hist:
        histograms.append(hist)
        stack.Add(hist)

# Draw the THStack
stack.Draw("hist")

# Create a legend to label the histograms
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for hist in histograms:
    legend.AddEntry(hist, hist.GetTitle(), "f")
legend.Draw()

# Create a new canvas for the relative contribution plot
canvas2 = ROOT.TCanvas("canvas2", "Relative Contribution", 800, 600)
canvas2.cd()

# Use the x-axis of the first histogram in the stack to determine the number of bins
num_bins = histograms[0].GetXaxis().GetNbins()

# Loop over the bins and calculate the relative contributions
relative_contributions = []

for bin in range(1, num_bins + 1):
    total_bin_content = stack.GetStack().Last().GetBinContent(bin)
    contributions = []

    for hist in histograms:
        bin_content = hist.GetBinContent(bin)
        contribution = bin_content / total_bin_content
        contributions.append(contribution)

    relative_contributions.append(contributions)

# Create a THStack to visualize relative contributions
relative_stack = ROOT.THStack("relative_stack", "Relative Contributions")
colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kViolet]  # Adjust colors as needed

for idx, contributions in enumerate(relative_contributions):
    hist_name = "Relative_Contribution_" + str(idx)
    hist = ROOT.TH1F(hist_name, "", len(contributions), 0, len(contributions))

    for i, contribution in enumerate(contributions):
        hist.SetBinContent(i + 1, contribution)
        hist.SetFillColor(colors[i])
        hist.SetLineColor(colors[i])
        hist.SetMarkerStyle(0)

    relative_stack.Add(hist)

# Draw the relative contribution THStack
relative_stack.Draw("hist")

# Create a legend for the relative contribution plot
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for hist in histograms:
    legend2.AddEntry(hist, hist.GetTitle(), "f")
legend2.Draw()

# Save the canvases as image files (optional)
canvas.SaveAs("stacked_histograms.png")
canvas2.SaveAs("relative_contributions.png")
