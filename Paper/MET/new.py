import ROOT
import json

# Open JSON file
with open('data.json') as f:
    data = json.load(f)

# Create canvas
canvas = ROOT.TCanvas("canvas", "THStack with Bar Histograms", 800, 600)

# Create list of THStacks
stacks = []
colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta]

for i, d in enumerate(data):
    stack = ROOT.THStack("stack"+str(i), d['selection'])
    for key, val in d.items():
        if key != "selection":
            hist = ROOT.TH1F(key, key, 100, -5, 5)
            hist.FillRandom("gaus", int(val))
            hist.SetFillColor(colors[i])
            stack.Add(hist)
    stacks.append(stack)

# Create two bar histograms from the THStacks
bar_hists = []
for stack in stacks:
    hist = ROOT.TH1F(stack.GetName() + "_bar", stack.GetName() + "_bar", stack.GetNhists(), 0, stack.GetNhists())
    for i in range(stack.GetNhists()):
        hist.SetBinContent(i+1, stack.GetStack().Last().GetBinContent(i+1))
        hist.SetBinError(i+1, stack.GetStack().Last().GetBinError(i+1))
    bar_hists.append(hist)

# Draw the bar histograms
bar_hists[0].Draw("HIST")
bar_hists[1].Draw("HIST SAME")

# Set labels and legend
bar_hists[0].SetStats(0)
bar_hists[0].GetXaxis().SetTitle("THStacks")
bar_hists[0].GetYaxis().SetTitle("Events")
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for i, stack in enumerate(stacks):
    legend.AddEntry(bar_hists[i], stack.GetName(), "f")
legend.Draw()

# Show the canvas
canvas.Update()
canvas.Draw()
canvas.SaveAs("test.pdf")

