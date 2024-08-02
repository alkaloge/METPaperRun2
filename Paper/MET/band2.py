import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Open the ROOT file
input_file = ROOT.TFile("plotS_2018_njetsgt0_nbtagl_cutbased_varbins_hitslt1_METCorGood_T1Smear_pt_Gjets.root")

# Get data histogram
data_hist = input_file.Get("histo_data")

# Create a canvas
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 800)
canvas.cd()

# Create the top pad for the main plot
top_pad = ROOT.TPad("top_pad", "Top Pad", 0.0, 0.3, 1.0, 1.0)
top_pad.SetBottomMargin(0.02)
top_pad.Draw()
top_pad.cd()

# Create the THStack for MC histograms
stack = ROOT.THStack("stack", "Stacked MC")

# List of MC processes
mc_processes = ["histo_ewknlo_METCorGood_T1Smear_pt", "histo_ew_METCorGood_T1Smear_pt", "histo_gjets_METCorGood_T1Smear_pt", "histo_qcdmg_METCorGood_T1Smear_pt", "histo_tx_METCorGood_T1Smear_pt"]

# List of systematic variations
systematics = ["", "JERDown", "JERUp", "JESDown", "JESUp", "UnclusteredDown", "UnclusteredUp", "PUDown", "PUUp", "IDDown", "IDUp"]

# Create a dictionary to store systematic histograms
systematic_histograms = {}

# Loop over MC processes and systematics
for process in mc_processes:
    mc_hist = input_file.Get(process)
    stack.Add(mc_hist)

    for sys in systematics:
        if sys:
            sys_hist = input_file.Get("{}{}".format(process, sys))
            sys_hist.SetLineColor(ROOT.kRed)  # Set line color for systematic variations
            sys_hist.SetLineStyle(ROOT.kDashed)  # Set line style for systematic variations
            sys_hist.SetLineWidth(2)  # Adjust line width for visibility
            systematic_histograms["{}{}".format(process, sys)] = sys_hist

# Draw the MC stack
stack.Draw("hist")
stack.GetXaxis().SetTitle("X-Axis Title")
stack.GetYaxis().SetTitle("Y-Axis Title")

# Draw data on top of the stack
data_hist.Draw("same")

# Create the bottom pad for the ratio plot
canvas.cd()
bottom_pad = ROOT.TPad("bottom_pad", "Bottom Pad", 0.0, 0.0, 1.0, 0.3)
bottom_pad.SetTopMargin(0.02)
bottom_pad.SetBottomMargin(0.3)
bottom_pad.Draw()
bottom_pad.cd()

# Create the ratio histogram
ratio_hist = data_hist.Clone("ratio_hist")
ratio_hist.Divide(stack.GetStack().Last())  # Divide data by the total MC

# Customize the ratio plot
ratio_hist.SetTitle("")
ratio_hist.GetYaxis().SetTitle("Data / MC")
ratio_hist.GetYaxis().SetTitleSize(0.15)
ratio_hist.GetYaxis().SetTitleOffset(0.4)
ratio_hist.GetYaxis().SetNdivisions(505)
ratio_hist.GetXaxis().SetTitleSize(0.15)
ratio_hist.GetXaxis().SetTitleOffset(0.9)
ratio_hist.GetXaxis().SetLabelSize(0.12)
ratio_hist.GetYaxis().SetLabelSize(0.12)
ratio_hist.GetYaxis().SetRangeUser(0.5, 1.5)

# Draw the ratio histogram

ratio_hist.Draw("ep")

# Create and draw the uncertainty band around the ratio
uncertainty_band = data_hist.Clone("uncertainty_band")#OOT.TH1F("uncertainty_band", "", data_hist.GetNbinsX(), data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
uncertainty_band.Reset()
uncertainty_band.SetFillStyle(3004)
uncertainty_band.SetMarkerSize(0)
uncertainty_band.SetFillColor(ROOT.kBlue)

for i in range(1, data_hist.GetNbinsX() + 1):
    print 'for bin', i, uncertainty_band.GetBinLowEdge(i)
    uncertainty_band.SetBinContent(i, 1)  # Set the band content to 1
    bin_error = ratio_hist.GetBinError(i)
    uncertainty_band.SetBinError(i, bin_error)

uncertainty_band.Draw("e2 same")



# Save the canvas as a PDF file
canvas.Print("ratio_plot_with_systematics.pdf")

# Close the input file
input_file.Close()


