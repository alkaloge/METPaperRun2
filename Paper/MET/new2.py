import ROOT
import json
ROOT.gROOT.SetBatch(ROOT.kTRUE)
# Open and load the json file
with open('data.json') as f:
    data = json.load(f)

# Define the canvas and histograms
canvas = ROOT.TCanvas('canvas', 'THStack Example', 800, 600)
stack1 = ROOT.THStack('stack1', 'Stacked Histograms 1')
stack2 = ROOT.THStack('stack2', 'Stacked Histograms 2')

# Define the colors for each process
colors = {
    'top': ROOT.kRed,
    'ewk': ROOT.kBlue,
    'dy': ROOT.kGreen,
    'qcd': ROOT.kYellow,
    'ew': ROOT.kMagenta
}

# Fill the histograms from the data
for entry in data:
    label = entry['selection']
    hist1 = ROOT.TH1F(label+'_hist1', label, 5, 0, 5)
    hist2 = ROOT.TH1F(label+'_hist2', label, 5, 0, 5)
    for i, key in enumerate(colors.keys()):
        hist1.SetBinContent(i+1, entry[key])
        hist1.SetFillColor(colors[key])
        stack1.Add(hist1, 'bar')
        
        hist2.SetBinContent(i+1, entry[key])
        hist2.SetFillColor(colors[key])
        stack2.Add(hist2, 'bar')

# Draw the histograms on the canvas
stack1.Draw('bar')
stack2.Draw('bar SAME')

# Set the legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(stack1.GetStack().Last(), 'Stack 1', 'f')
legend.AddEntry(stack2.GetStack().Last(), 'Stack 2', 'f')
legend.Draw()

# Set the axis titles and range
stack1.GetXaxis().SetTitle('Process')
stack1.GetYaxis().SetTitle('Events')
stack1.SetMinimum(0)

# Update and display the canvas
canvas.Update()
canvas.Draw()
canvas.SaveAs("test.pdf")

