import ROOT
import json

# Load the JSON data from file
with open('my_file.json', 'r') as f:
    data = json.load(f)

canvas = ROOT.TCanvas("canvas", "Stacked Histogram", 800, 600)
stack = ROOT.THStack("stack", "Stacked Histogram")

# Define the colors for each histogram
colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kMagenta, ROOT.kOrange]

# Get the selection label and histogram values
selection_label = data["selection"]
hist_values = []
for key, value in data.items():
    if key != "selection":
        hist_values.append(value)

# Create a histogram for each data series and add it to the stack
for i, value in enumerate(hist_values):
    hist = ROOT.TH1F("hist{}".format(i), "", 1, 0, 1)
    hist.SetBinContent(1, value)
    hist.SetFillColor(colors[i])
    stack.Add(hist)

# Draw the stacked histogram with the x-axis label
stack.Draw("HIST")
stack.GetXaxis().SetTitle(selection_label)

# Set the y-axis label and tick marks
stack.GetYaxis().SetTitle("count")
stack.GetYaxis().SetTickSize(0.02)

# Add legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for i, key in enumerate(data.keys()):
    if key != "selection":
        legend.AddEntry(stack.GetHists().At(i), key, "f")
legend.Draw()

# Save the plot to file
canvas.SaveAs("stacked_hist.png")

